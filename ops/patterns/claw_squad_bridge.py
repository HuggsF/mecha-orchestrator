# ==============================================================================
# 🖱️ MECHA CLAW↔SQUAD BRIDGE + MCP BUS TOOLS
# ==============================================================================
# Bridges the hardware Claw agent with squad-based AI workflows via AgentBus.
# Also exposes bus operations as MCP tools for IDE integration.
# Resolves GAP 6 (no Claw↔Squad feedback) and GAP 7 (MCP fire-and-forget).
# ==============================================================================

import os
import sys
import json
import time
import asyncio
import logging
from typing import Dict, Any, List, Optional

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger("MECHA_ClawBridge")

from agent_bus import AgentBus, BusMessage, MessageType, AgentStatus
from cross_squad_router import CrossSquadRouter
from hermes_auditor import HermesAuditor
from telegram_relay import TelegramRelay


# =============================================================================
# FILE-BASED IPC PATHS (legacy — bridge reads/writes these for Claw compat)
# =============================================================================

OPS_DIR = os.path.dirname(os.path.abspath(__file__))
LOGS_DIR = os.path.join(OPS_DIR, "logs")
STATUS_FILE = os.path.join(LOGS_DIR, "claw_status.json")
PREEMPT_FILE = os.path.join(LOGS_DIR, "claw_preempt.json")


# =============================================================================
# RISK ASSESSMENT
# =============================================================================

RISKY_ACTIONS = {
    "click": {"risk": "low", "consult_squad": False},
    "type": {"risk": "low", "consult_squad": False},
    "delete": {"risk": "high", "consult_squad": True},
    "install": {"risk": "high", "consult_squad": True},
    "execute": {"risk": "medium", "consult_squad": True},
    "download": {"risk": "medium", "consult_squad": True},
    "login": {"risk": "high", "consult_squad": True},
    "submit": {"risk": "medium", "consult_squad": True},
    "send": {"risk": "medium", "consult_squad": True},
    "close": {"risk": "low", "consult_squad": False},
    "navigate": {"risk": "low", "consult_squad": False},
}


class ClawSquadBridge:
    """
    Bridge between Claw hardware agent and Squad AI workflows.

    - Claw publishes intended actions to the bus
    - Bridge evaluates risk and optionally consults a squad
    - Squad verdict flows back to Claw via bus or preempt file
    - All interactions are audited by Hermes
    """

    def __init__(self, workspace_root: str, bus: AgentBus = None):
        self.workspace_root = workspace_root
        self.bus = bus or AgentBus.get_instance()
        self.router = CrossSquadRouter(workspace_root, self.bus)
        self.auditor = HermesAuditor(bus=self.bus)
        self.auditor.start()
        
        # Initialize and start the Telegram Relay for real-time AgentBus monitoring
        try:
            self.relay = TelegramRelay(bus=self.bus)
            self.relay.start()
        except Exception as e:
            logger.error(f"[BRIDGE] Failed to initialize TelegramRelay: {e}")
            
        self._register_claw()

    def _register_claw(self):
        if not self.bus.get_agent("claw"):
            self.bus.register(
                "claw", "Claw Hardware Agent",
                squad="system", role="Hardware Controller",
                capabilities=["vision", "ocr", "mouse", "keyboard", "screenshot"]
            )
        self.bus.subscribe("claw", "claw.commands")
        self.bus.subscribe("claw", "claw.verdicts")

    # -------------------------------------------------------------------------
    # RISK ASSESSMENT
    # -------------------------------------------------------------------------

    def assess_risk(self, action: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        action_lower = action.lower()
        risk_info = RISKY_ACTIONS.get(action_lower, {"risk": "unknown", "consult_squad": True})

        keywords_high = ["admin", "root", "sudo", "password", "credential", "rm -rf", "format"]
        if context:
            ctx_str = json.dumps(context).lower()
            if any(kw in ctx_str for kw in keywords_high):
                risk_info = {"risk": "critical", "consult_squad": True}

        return {
            "action": action,
            "risk_level": risk_info["risk"],
            "requires_consultation": risk_info["consult_squad"],
            "context": context
        }

    # -------------------------------------------------------------------------
    # SQUAD CONSULTATION
    # -------------------------------------------------------------------------

    async def consult_squad(self, action: str, context: Dict[str, Any],
                             squad: str = "tribunal", thread_id: str = None) -> Dict[str, Any]:
        if not thread_id:
            thread_id = f"claw_consult_{int(time.time())}"

        prompt = (
            f"O agente Claw deseja executar a acao: '{action}'.\n"
            f"Contexto: {json.dumps(context, ensure_ascii=False)}\n"
            f"Avalie o risco e emita um veredito: [1] = APROVADO, [0] = BLOQUEADO."
        )

        self.bus.publish("claw", "claw.commands", {
            "event": "claw.consultation_requested",
            "action": action,
            "context": context,
            "target_squad": squad,
            "thread_id": thread_id
        })

        result = await self.router.request_squad(
            "claw", squad, prompt, thread_id=thread_id
        )

        verdict_text = str(result.get("verdict", result.get("assessment", "")))
        approved = "[1]" in verdict_text or "[APROVADO]" in verdict_text.upper()

        verdict = {
            "action": action,
            "approved": approved,
            "verdict_text": verdict_text,
            "squad": squad,
            "thread_id": thread_id,
            "timestamp": time.time()
        }

        self.bus.publish("claw", "claw.verdicts", {
            "event": "claw.verdict_received",
            **verdict
        })

        return verdict

    # -------------------------------------------------------------------------
    # ACTION PIPELINE (assess → consult if needed → execute or block)
    # -------------------------------------------------------------------------

    async def evaluate_action(self, action: str, context: Dict[str, Any] = None,
                               auto_consult: bool = True) -> Dict[str, Any]:
        context = context or {}
        assessment = self.assess_risk(action, context)

        if not assessment["requires_consultation"]:
            return {
                "decision": "approved",
                "reason": f"Low-risk action '{action}' — auto-approved",
                "assessment": assessment
            }

        if auto_consult:
            verdict = await self.consult_squad(action, context)
            return {
                "decision": "approved" if verdict["approved"] else "blocked",
                "reason": verdict["verdict_text"],
                "assessment": assessment,
                "verdict": verdict
            }

        return {
            "decision": "pending",
            "reason": f"Action '{action}' requires squad consultation",
            "assessment": assessment
        }

    # -------------------------------------------------------------------------
    # CLAW STATUS SYNC (file → bus bridge)
    # -------------------------------------------------------------------------

    def sync_claw_status(self) -> Dict[str, Any]:
        if os.path.exists(STATUS_FILE):
            try:
                with open(STATUS_FILE, "r", encoding="utf-8") as f:
                    status = json.load(f)
                self.bus.publish("claw", "claw.commands", {
                    "event": "claw.status_sync",
                    "status": status
                })
                return status
            except Exception as e:
                logger.error(f"[BRIDGE] Error reading claw status: {e}")
        return {"state": "unknown"}

    def send_preempt(self, command: str, args: Dict[str, Any] = None):
        preempt = {
            "command": command,
            "args": args or {},
            "timestamp": time.time(),
            "source": "agent_bus"
        }
        os.makedirs(os.path.dirname(PREEMPT_FILE), exist_ok=True)
        with open(PREEMPT_FILE, "w", encoding="utf-8") as f:
            json.dump(preempt, f, indent=2, ensure_ascii=False)

        self.bus.publish("claw", "claw.commands", {
            "event": "claw.preempt_sent",
            "command": command,
            "args": args
        })

    # -------------------------------------------------------------------------
    # BUS OPERATIONS (for MCP tool exposure)
    # -------------------------------------------------------------------------

    def bus_send_message(self, sender: str, recipient: str,
                         payload: Dict[str, Any]) -> Dict[str, Any]:
        try:
            if payload is None:
                raise ValueError("Payload cannot be None")
            msg = self.bus.send(sender, recipient, payload)
            self.auditor.audit_message(msg)
            return {"ok": True, "msg_id": msg.msg_id}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def bus_broadcast(self, sender: str, squad: str,
                       payload: Dict[str, Any]) -> Dict[str, Any]:
        try:
            if payload is None:
                raise ValueError("Payload cannot be None")
            msg = self.bus.broadcast(sender, payload, squad=squad)
            self.auditor.audit_message(msg)
            return {"ok": True, "msg_id": msg.msg_id}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def bus_get_inbox(self, agent_id: str) -> List[Dict[str, Any]]:
        messages = self.bus.get_inbox(agent_id)
        return [
            {
                "msg_id": m.msg_id,
                "sender": m.sender,
                "msg_type": m.msg_type.value if hasattr(m.msg_type, 'value') else str(m.msg_type),
                "payload": m.payload,
                "timestamp": m.timestamp
            }
            for m in messages
        ]

    def bus_list_agents(self, squad: str = None) -> List[Dict[str, Any]]:
        agents = self.bus.list_agents(squad=squad)
        return [
            {
                "agent_id": a.agent_id,
                "name": a.name,
                "squad": a.squad,
                "role": a.role,
                "status": a.status.value if hasattr(a.status, 'value') else str(a.status),
                "capabilities": a.capabilities
            }
            for a in agents
        ]

    def bus_compliance_report(self) -> Dict[str, Any]:
        return self.auditor.compliance_report()

    def bus_stats(self) -> Dict[str, Any]:
        return {
            "bus": self.bus.stats(),
            "auditor": self.auditor.stats(),
            "router_routes": list(self.router.routes.keys()),
            "conversations": len(self.router.list_conversations())
        }

    def get_conversation(self, thread_id: str) -> List[Dict[str, Any]]:
        return self.router.get_conversation(thread_id)

    def search_conversations(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        return self.router.search_conversations(query, limit)


# =============================================================================
# TESTS
# =============================================================================

def _run_tests():  # pragma: no cover
    import shutil

    print("=" * 60)
    print("  MECHA CLAW↔SQUAD BRIDGE — UNIT TESTS")
    print("=" * 60)

    workspace = "c:\\Users\\huggs\\OneDrive\\Documentos\\workspace"
    test_conv_dir = os.path.join(os.path.dirname(__file__), "_test_bridge_convs")

    AgentBus.reset()
    bus = AgentBus.get_instance()
    bridge = ClawSquadBridge(workspace, bus)
    bridge.router.history.store_dir = test_conv_dir
    os.makedirs(test_conv_dir, exist_ok=True)
    results = {}

    # Test 1: Claw registered on bus
    try:
        claw = bus.get_agent("claw")
        assert claw is not None
        assert "vision" in claw.capabilities
        results["claw_registered"] = True
        print(f" [OK] Test 1: Claw registered on bus (caps={claw.capabilities})")
    except Exception as e:
        results["claw_registered"] = False
        print(f" [FAIL] Test 1: {e}")

    # Test 2: Risk assessment — low risk
    try:
        assessment = bridge.assess_risk("click", {"target": "button_ok"})
        assert assessment["risk_level"] == "low"
        assert not assessment["requires_consultation"]
        results["risk_low"] = True
        print(f" [OK] Test 2: Low risk assessment (click)")
    except Exception as e:
        results["risk_low"] = False
        print(f" [FAIL] Test 2: {e}")

    # Test 3: Risk assessment — high risk
    try:
        assessment = bridge.assess_risk("delete", {"target": "database_records"})
        assert assessment["risk_level"] == "high"
        assert assessment["requires_consultation"]
        results["risk_high"] = True
        print(f" [OK] Test 3: High risk assessment (delete)")
    except Exception as e:
        results["risk_high"] = False
        print(f" [FAIL] Test 3: {e}")

    # Test 4: Risk assessment — critical (keyword escalation)
    try:
        assessment = bridge.assess_risk("execute", {"command": "rm -rf /important"})
        assert assessment["risk_level"] == "critical"
        assert assessment["requires_consultation"]
        results["risk_critical"] = True
        print(f" [OK] Test 4: Critical risk escalation (keyword)")
    except Exception as e:
        results["risk_critical"] = False
        print(f" [FAIL] Test 4: {e}")

    # Test 5: Auto-approve low-risk action
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(
            bridge.evaluate_action("click", {"target": "ok_button"})
        )
        assert result["decision"] == "approved"
        results["auto_approve"] = True
        print(f" [OK] Test 5: Auto-approve low-risk (decision={result['decision']})")
    except Exception as e:
        results["auto_approve"] = False
        print(f" [FAIL] Test 5: {e}")

    # Test 6: Pending consultation for high-risk (auto_consult=False)
    try:
        result = loop.run_until_complete(
            bridge.evaluate_action("install", {"package": "unknown_pkg"}, auto_consult=False)
        )
        assert result["decision"] == "pending"
        results["pending_consult"] = True
        print(f" [OK] Test 6: Pending consultation (decision={result['decision']})")
    except Exception as e:
        results["pending_consult"] = False
        print(f" [FAIL] Test 6: {e}")

    # Test 7: Squad consultation (full pipeline, mock mode)
    try:
        verdict = loop.run_until_complete(
            bridge.consult_squad("execute", {"script": "deploy.sh"})
        )
        assert "approved" in verdict
        assert "verdict_text" in verdict
        assert verdict["squad"] == "tribunal"
        results["squad_consult"] = True
        print(f" [OK] Test 7: Squad consultation (approved={verdict['approved']})")
    except Exception as e:
        results["squad_consult"] = False
        print(f" [FAIL] Test 7: {e}")

    # Test 8: Bus operations (send/inbox/list)
    try:
        bus.register("test_agent", "Test Agent", squad="test")
        r = bridge.bus_send_message("claw", "test_agent", {"action": "ping"})
        assert r["ok"]
        inbox = bridge.bus_get_inbox("test_agent")
        assert len(inbox) >= 1
        agents = bridge.bus_list_agents()
        assert len(agents) >= 3
        results["bus_ops"] = True
        print(f" [OK] Test 8: Bus operations (agents={len(agents)}, inbox={len(inbox)})")
    except Exception as e:
        results["bus_ops"] = False
        print(f" [FAIL] Test 8: {e}")

    # Test 9: Compliance report
    try:
        report = bridge.bus_compliance_report()
        assert "compliance_rate" in report
        assert "stats" in report
        results["compliance"] = True
        print(f" [OK] Test 9: Compliance report (rate={report['compliance_rate']}%)")
    except Exception as e:
        results["compliance"] = False
        print(f" [FAIL] Test 9: {e}")

    # Test 10: Full stats
    try:
        stats = bridge.bus_stats()
        assert "bus" in stats
        assert "auditor" in stats
        assert "router_routes" in stats
        results["stats"] = True
        print(f" [OK] Test 10: Full stats ({stats['bus']['agents_registered']} agents)")
    except Exception as e:
        results["stats"] = False
        print(f" [FAIL] Test 10: {e}")

    # Cleanup
    loop.close()
    try:
        shutil.rmtree(test_conv_dir, ignore_errors=True)
        hermes_log = os.path.join(OPS_DIR, "logs", "hermes_audit")
        shutil.rmtree(hermes_log, ignore_errors=True)
    except Exception:
        pass

    # Summary
    print("\n" + "=" * 60)
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    for name, ok in results.items():
        print(f"  {'[PASS]' if ok else '[FAIL]'} {name}")
    print(f"\n  RESULT: {passed}/{total} tests passed")
    print("=" * 60)
    return passed == total


if __name__ == "__main__":  # pragma: no cover
    success = _run_tests()
    sys.exit(0 if success else 1)
