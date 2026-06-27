# ==============================================================================
# 🛡️ MECHA HERMES AUDITOR - REAL-TIME BUS AUDIT + TACP VALIDATION
# ==============================================================================
# Intercepts all AgentBus messages, validates TACP conformance, generates
# structured audit logs, and publishes compliance events.
# Resolves GAP 4: Hermes was placeholder — now real.
# ==============================================================================

import os
import sys
import json
import time
import re
import logging
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field, asdict
from enum import Enum

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger("MECHA_HermesAuditor")

from agent_bus import AgentBus, BusMessage, MessageType, AgentStatus


# =============================================================================
# AUDIT SEVERITY & RESULT MODELS
# =============================================================================

class AuditSeverity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    VIOLATION = "violation"
    CRITICAL = "critical"


@dataclass
class AuditEntry:
    timestamp: float
    message_id: str
    sender: str
    recipient: str
    msg_type: str
    rule_id: str
    rule_name: str
    severity: str
    passed: bool
    detail: str
    payload_preview: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


# =============================================================================
# AUDIT RULES
# =============================================================================

class AuditRule:
    """Base class for audit rules."""
    rule_id: str = "R000"
    rule_name: str = "Base Rule"
    severity: str = AuditSeverity.INFO.value

    def check(self, msg: BusMessage, bus: AgentBus) -> AuditEntry:
        raise NotImplementedError


class R001_SenderRegistered(AuditRule):
    rule_id = "R001"
    rule_name = "Sender must be registered on bus"
    severity = AuditSeverity.VIOLATION.value

    def check(self, msg: BusMessage, bus: AgentBus) -> AuditEntry:
        agent = bus.get_agent(msg.sender)
        passed = agent is not None
        return AuditEntry(
            timestamp=time.time(), message_id=msg.msg_id,
            sender=msg.sender, recipient=msg.recipient or "",
            msg_type=msg.msg_type.value if hasattr(msg.msg_type, 'value') else str(msg.msg_type),
            rule_id=self.rule_id, rule_name=self.rule_name,
            severity=self.severity, passed=passed,
            detail="" if passed else f"Sender '{msg.sender}' not registered"
        )


class R002_RecipientExists(AuditRule):
    rule_id = "R002"
    rule_name = "Recipient must exist for direct messages"
    severity = AuditSeverity.WARNING.value

    def check(self, msg: BusMessage, bus: AgentBus) -> AuditEntry:
        if msg.msg_type not in (MessageType.DIRECT, MessageType.REQUEST):
            return AuditEntry(
                timestamp=time.time(), message_id=msg.msg_id,
                sender=msg.sender, recipient=msg.recipient or "",
                msg_type=msg.msg_type.value if hasattr(msg.msg_type, 'value') else str(msg.msg_type),
                rule_id=self.rule_id, rule_name=self.rule_name,
                severity=self.severity, passed=True,
                detail="N/A for non-direct messages"
            )
        agent = bus.get_agent(msg.recipient) if msg.recipient else None
        passed = agent is not None
        return AuditEntry(
            timestamp=time.time(), message_id=msg.msg_id,
            sender=msg.sender, recipient=msg.recipient or "",
            msg_type=msg.msg_type.value if hasattr(msg.msg_type, 'value') else str(msg.msg_type),
            rule_id=self.rule_id, rule_name=self.rule_name,
            severity=self.severity, passed=passed,
            detail="" if passed else f"Recipient '{msg.recipient}' not found"
        )


class R003_PayloadNotEmpty(AuditRule):
    rule_id = "R003"
    rule_name = "Payload must not be empty"
    severity = AuditSeverity.INFO.value

    def check(self, msg: BusMessage, bus: AgentBus) -> AuditEntry:
        passed = msg.payload is not None and msg.payload != {} and msg.payload != ""
        return AuditEntry(
            timestamp=time.time(), message_id=msg.msg_id,
            sender=msg.sender, recipient=msg.recipient or "",
            msg_type=msg.msg_type.value if hasattr(msg.msg_type, 'value') else str(msg.msg_type),
            rule_id=self.rule_id, rule_name=self.rule_name,
            severity=self.severity, passed=passed,
            detail="" if passed else "Empty payload detected",
            payload_preview=str(msg.payload)[:100] if msg.payload else ""
        )


class R004_TTLValid(AuditRule):
    rule_id = "R004"
    rule_name = "Message TTL must be reasonable (0-3600s)"
    severity = AuditSeverity.WARNING.value

    def check(self, msg: BusMessage, bus: AgentBus) -> AuditEntry:
        passed = 0 <= msg.ttl <= 3600
        return AuditEntry(
            timestamp=time.time(), message_id=msg.msg_id,
            sender=msg.sender, recipient=msg.recipient or "",
            msg_type=msg.msg_type.value if hasattr(msg.msg_type, 'value') else str(msg.msg_type),
            rule_id=self.rule_id, rule_name=self.rule_name,
            severity=self.severity, passed=passed,
            detail="" if passed else f"TTL={msg.ttl}s exceeds 3600s limit"
        )


class R005_TACPCompliance(AuditRule):
    rule_id = "R005"
    rule_name = "TACP format compliance check"
    severity = AuditSeverity.INFO.value

    TACP_MARKERS = ["MECHA_EVENT", "Origem:", "Destino:", "Timestamp:", "Status:"]

    def check(self, msg: BusMessage, bus: AgentBus) -> AuditEntry:
        content = str(msg.payload) if msg.payload else ""
        if len(content) < 50:
            return AuditEntry(
                timestamp=time.time(), message_id=msg.msg_id,
                sender=msg.sender, recipient=msg.recipient or "",
                msg_type=msg.msg_type.value if hasattr(msg.msg_type, 'value') else str(msg.msg_type),
                rule_id=self.rule_id, rule_name=self.rule_name,
                severity=self.severity, passed=True,
                detail="Short message — TACP check skipped"
            )
        markers_found = sum(1 for m in self.TACP_MARKERS if m in content)
        passed = markers_found >= 3 or len(content) < 200
        return AuditEntry(
            timestamp=time.time(), message_id=msg.msg_id,
            sender=msg.sender, recipient=msg.recipient or "",
            msg_type=msg.msg_type.value if hasattr(msg.msg_type, 'value') else str(msg.msg_type),
            rule_id=self.rule_id, rule_name=self.rule_name,
            severity=self.severity, passed=passed,
            detail=f"TACP markers: {markers_found}/5" if not passed else "",
            payload_preview=content[:100]
        )


class R006_CrossSquadAuth(AuditRule):
    rule_id = "R006"
    rule_name = "Cross-squad messages require router origin"
    severity = AuditSeverity.VIOLATION.value

    def check(self, msg: BusMessage, bus: AgentBus) -> AuditEntry:
        sender_agent = bus.get_agent(msg.sender)
        recipient_agent = bus.get_agent(msg.recipient) if msg.recipient else None

        if not sender_agent or not recipient_agent:
            return AuditEntry(
                timestamp=time.time(), message_id=msg.msg_id,
                sender=msg.sender, recipient=msg.recipient or "",
                msg_type=msg.msg_type.value if hasattr(msg.msg_type, 'value') else str(msg.msg_type),
                rule_id=self.rule_id, rule_name=self.rule_name,
                severity=self.severity, passed=True,
                detail="Agents not fully resolved — skipped"
            )

        if sender_agent.squad == recipient_agent.squad:
            return AuditEntry(
                timestamp=time.time(), message_id=msg.msg_id,
                sender=msg.sender, recipient=msg.recipient or "",
                msg_type=msg.msg_type.value if hasattr(msg.msg_type, 'value') else str(msg.msg_type),
                rule_id=self.rule_id, rule_name=self.rule_name,
                severity=self.severity, passed=True,
                detail="Same-squad message — no auth required"
            )

        passed = sender_agent.squad == "system" or sender_agent.role == "Message Router"
        return AuditEntry(
            timestamp=time.time(), message_id=msg.msg_id,
            sender=msg.sender, recipient=msg.recipient or "",
            msg_type=msg.msg_type.value if hasattr(msg.msg_type, 'value') else str(msg.msg_type),
            rule_id=self.rule_id, rule_name=self.rule_name,
            severity=self.severity, passed=passed,
            detail="" if passed else f"Cross-squad msg from non-router agent '{msg.sender}'"
        )


# =============================================================================
# HERMES AUDITOR
# =============================================================================

DEFAULT_RULES = [
    R001_SenderRegistered(),
    R002_RecipientExists(),
    R003_PayloadNotEmpty(),
    R004_TTLValid(),
    R005_TACPCompliance(),
    R006_CrossSquadAuth(),
]


class HermesAuditor:
    """
    Real-time message auditor for the MECHA AgentBus.

    - Intercepts all messages via on_message handler
    - Runs configurable audit rules against each message
    - Persists structured audit logs (JSON)
    - Publishes compliance events to bus channel
    - Provides compliance reports and stats
    """

    def __init__(self, bus: AgentBus = None, log_dir: str = None,
                 rules: List[AuditRule] = None):
        self.bus = bus or AgentBus.get_instance()
        self.log_dir = log_dir or os.path.join(
            os.path.dirname(__file__), "logs", "hermes_audit"
        )
        os.makedirs(self.log_dir, exist_ok=True)
        self.rules = rules or list(DEFAULT_RULES)
        self._audit_log: List[AuditEntry] = []
        self._stats = {
            "messages_audited": 0,
            "rules_passed": 0,
            "rules_failed": 0,
            "violations": 0,
            "warnings": 0
        }
        self._active = False

    def start(self):
        if not self.bus.get_agent("hermes"):
            self.bus.register(
                "hermes", "Hermes Auditor",
                squad="system", role="Compliance Auditor",
                capabilities=["audit", "compliance", "tacp_validation"]
            )
        self.bus.subscribe("hermes", "audit.events")
        self._active = True
        logger.info("[HERMES] Auditor started — intercepting bus messages")

    def stop(self):
        self._active = False
        self.flush_log()
        logger.info("[HERMES] Auditor stopped")

    # -------------------------------------------------------------------------
    # MESSAGE INTERCEPTION
    # -------------------------------------------------------------------------

    def audit_message(self, msg: BusMessage):
        if not self._active:
            return
        if msg.sender == "hermes":
            return

        self._stats["messages_audited"] += 1
        entries = []

        for rule in self.rules:
            try:
                entry = rule.check(msg, self.bus)
                entries.append(entry)
                if entry.passed:
                    self._stats["rules_passed"] += 1
                else:
                    self._stats["rules_failed"] += 1
                    if entry.severity == AuditSeverity.VIOLATION.value:
                        self._stats["violations"] += 1
                    elif entry.severity == AuditSeverity.WARNING.value:
                        self._stats["warnings"] += 1
            except Exception as e:
                logger.error(f"[HERMES] Rule {rule.rule_id} error: {e}")

        self._audit_log.extend(entries)

        failed = [e for e in entries if not e.passed]
        if failed:
            self.bus.publish("hermes", "audit.events", {
                "event": "audit.findings",
                "message_id": msg.msg_id,
                "sender": msg.sender,
                "findings": [e.to_dict() for e in failed]
            })

    # -------------------------------------------------------------------------
    # AUDIT LOG PERSISTENCE
    # -------------------------------------------------------------------------

    def flush_log(self) -> str:
        if not self._audit_log:
            return ""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        path = os.path.join(self.log_dir, f"audit_{timestamp}.json")
        data = {
            "flushed_at": time.time(),
            "stats": dict(self._stats),
            "entries": [e.to_dict() for e in self._audit_log]
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        count = len(self._audit_log)
        self._audit_log.clear()
        logger.info(f"[HERMES] Flushed {count} entries to {path}")
        return path

    # -------------------------------------------------------------------------
    # COMPLIANCE REPORTS
    # -------------------------------------------------------------------------

    def compliance_report(self) -> Dict[str, Any]:
        total_checks = self._stats["rules_passed"] + self._stats["rules_failed"]
        compliance_rate = (
            (self._stats["rules_passed"] / total_checks * 100) if total_checks > 0 else 100.0
        )

        by_rule = {}
        for entry in self._audit_log:
            rid = entry.rule_id
            if rid not in by_rule:
                by_rule[rid] = {"rule_name": entry.rule_name, "passed": 0, "failed": 0}
            if entry.passed:
                by_rule[rid]["passed"] += 1
            else:
                by_rule[rid]["failed"] += 1

        recent_violations = [
            e.to_dict() for e in self._audit_log
            if not e.passed and e.severity in (AuditSeverity.VIOLATION.value, AuditSeverity.CRITICAL.value)
        ][-10:]

        return {
            "stats": dict(self._stats),
            "compliance_rate": round(compliance_rate, 1),
            "by_rule": by_rule,
            "recent_violations": recent_violations
        }

    def stats(self) -> Dict[str, Any]:
        return dict(self._stats)

    # -------------------------------------------------------------------------
    # RULE MANAGEMENT
    # -------------------------------------------------------------------------

    def add_rule(self, rule: AuditRule):
        self.rules.append(rule)

    def remove_rule(self, rule_id: str) -> bool:
        before = len(self.rules)
        self.rules = [r for r in self.rules if r.rule_id != rule_id]
        return len(self.rules) < before

    def list_rules(self) -> List[Dict[str, str]]:
        return [
            {"rule_id": r.rule_id, "rule_name": r.rule_name, "severity": r.severity}
            for r in self.rules
        ]


# =============================================================================
# TESTS
# =============================================================================

def _run_tests():  # pragma: no cover
    import shutil

    print("=" * 60)
    print("  MECHA HERMES AUDITOR — UNIT TESTS")
    print("=" * 60)

    test_log_dir = os.path.join(os.path.dirname(__file__), "_test_hermes_logs")

    AgentBus.reset()
    bus = AgentBus.get_instance()
    auditor = HermesAuditor(bus=bus, log_dir=test_log_dir)
    auditor.start()
    results = {}

    # Register test agents
    bus.register("alice", "Alice", squad="dev_squad", role="Developer")
    bus.register("bob", "Bob", squad="dev_squad", role="Architect")
    bus.register("router", "CrossSquadRouter", squad="system", role="Message Router")
    bus.register("warlock", "Warlock", squad="tribunal_squad", role="Accuser")

    # Test 1: Clean message passes all rules
    try:
        msg = bus.send("alice", "bob", {"action": "review", "file": "main.py"})
        auditor.audit_message(msg)
        report = auditor.compliance_report()
        assert report["stats"]["messages_audited"] == 1
        assert report["stats"]["violations"] == 0
        results["clean_message"] = True
        print(f" [OK] Test 1: Clean message passes all rules (rate={report['compliance_rate']}%)")
    except Exception as e:
        results["clean_message"] = False
        print(f" [FAIL] Test 1: {e}")

    # Test 2: Unregistered sender triggers R001
    try:
        fake_msg = BusMessage(
            sender="ghost_agent", recipient="alice",
            msg_type=MessageType.DIRECT,
            payload={"action": "hack"}
        )
        auditor.audit_message(fake_msg)
        violations = [e for e in auditor._audit_log if not e.passed and e.rule_id == "R001"]
        assert len(violations) >= 1
        results["unregistered_sender"] = True
        print(f" [OK] Test 2: Unregistered sender triggers R001 ({len(violations)} violations)")
    except Exception as e:
        results["unregistered_sender"] = False
        print(f" [FAIL] Test 2: {e}")

    # Test 3: Missing recipient triggers R002
    try:
        fake_msg = BusMessage(
            sender="alice", recipient="nonexistent",
            msg_type=MessageType.DIRECT,
            payload={"action": "ping"}
        )
        auditor.audit_message(fake_msg)
        warnings = [e for e in auditor._audit_log if not e.passed and e.rule_id == "R002"]
        assert len(warnings) >= 1
        results["missing_recipient"] = True
        print(f" [OK] Test 3: Missing recipient triggers R002")
    except Exception as e:
        results["missing_recipient"] = False
        print(f" [FAIL] Test 3: {e}")

    # Test 4: Empty payload triggers R003
    try:
        msg = bus.send("alice", "bob", {})
        auditor.audit_message(msg)
        empties = [e for e in auditor._audit_log if not e.passed and e.rule_id == "R003"]
        assert len(empties) >= 1
        results["empty_payload"] = True
        print(f" [OK] Test 4: Empty payload triggers R003")
    except Exception as e:
        results["empty_payload"] = False
        print(f" [FAIL] Test 4: {e}")

    # Test 5: Cross-squad without router triggers R006
    try:
        fake_msg = BusMessage(
            sender="alice", recipient="warlock",
            msg_type=MessageType.DIRECT,
            payload={"action": "cross_squad_hack"}
        )
        auditor.audit_message(fake_msg)
        xsquad = [e for e in auditor._audit_log if not e.passed and e.rule_id == "R006"]
        assert len(xsquad) >= 1
        results["cross_squad_auth"] = True
        print(f" [OK] Test 5: Cross-squad without router triggers R006")
    except Exception as e:
        results["cross_squad_auth"] = False
        print(f" [FAIL] Test 5: {e}")

    # Test 6: Router cross-squad is allowed
    try:
        msg = bus.send("router", "warlock", {"action": "legitimate_route"})
        auditor.audit_message(msg)
        router_violations = [
            e for e in auditor._audit_log
            if not e.passed and e.rule_id == "R006" and e.sender == "router"
        ]
        assert len(router_violations) == 0
        results["router_allowed"] = True
        print(f" [OK] Test 6: Router cross-squad is allowed")
    except Exception as e:
        results["router_allowed"] = False
        print(f" [FAIL] Test 6: {e}")

    # Test 7: Audit log flush persistence
    try:
        path = auditor.flush_log()
        assert path and os.path.exists(path)
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        assert "entries" in data
        assert len(data["entries"]) > 0
        results["log_persistence"] = True
        print(f" [OK] Test 7: Audit log flush ({len(data['entries'])} entries)")
    except Exception as e:
        results["log_persistence"] = False
        print(f" [FAIL] Test 7: {e}")

    # Test 8: Compliance report structure
    try:
        msg = bus.send("alice", "bob", {"action": "final_check"})
        auditor.audit_message(msg)
        report = auditor.compliance_report()
        assert "compliance_rate" in report
        assert "by_rule" in report
        assert "stats" in report
        assert report["compliance_rate"] >= 0
        results["compliance_report"] = True
        print(f" [OK] Test 8: Compliance report (rate={report['compliance_rate']}%)")
    except Exception as e:
        results["compliance_report"] = False
        print(f" [FAIL] Test 8: {e}")

    # Test 9: Rule management
    try:
        initial_count = len(auditor.rules)
        removed = auditor.remove_rule("R005")
        assert removed
        assert len(auditor.rules) == initial_count - 1
        rules_list = auditor.list_rules()
        assert all(r["rule_id"] != "R005" for r in rules_list)
        auditor.add_rule(R005_TACPCompliance())
        assert len(auditor.rules) == initial_count
        results["rule_management"] = True
        print(f" [OK] Test 9: Rule management (add/remove)")
    except Exception as e:
        results["rule_management"] = False
        print(f" [FAIL] Test 9: {e}")

    # Test 10: Audit events published to bus channel
    try:
        events_received = []
        bus.on_channel("audit.events", lambda msg: events_received.append(msg))
        fake_msg = BusMessage(
            sender="intruder", recipient="alice",
            msg_type=MessageType.DIRECT,
            payload={"action": "unauthorized"}
        )
        auditor.audit_message(fake_msg)
        assert len(events_received) >= 1
        assert events_received[-1].payload["event"] == "audit.findings"
        results["audit_events"] = True
        print(f" [OK] Test 10: Audit events published to bus channel")
    except Exception as e:
        results["audit_events"] = False
        print(f" [FAIL] Test 10: {e}")

    # Cleanup
    try:
        shutil.rmtree(test_log_dir, ignore_errors=True)
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
