# ==============================================================================
# SHURA DAEMON - MASTER ORCHESTRATOR (consumidor do AgentBus)
# ==============================================================================
# Implementa ORCH-05..09 do ADR-001 em CODIGO:
#   ORCH-05 monitora o AgentBus o tempo todo
#   ORCH-06 gate de build + testes antes da entrega (hook seguro)
#   ORCH-07 resposta final e a agregacao do Shura
#   ORCH-08 relatorio de consolidacao dos 5 dominios
#   ORCH-09 orquestracao e daemon event-driven (nao one-shot)
#
# NOTA ARQUITETURAL: o AgentBus e um singleton IN-PROCESS. Para monitorar de
# verdade, este daemon deve rodar no MESMO processo do orquestrador/router
# (ex.: iniciado pelo backend FastAPI) compartilhando get_instance(). Em modo
# cross-process, adapte para tailar o log do bus (flush_log/load_log).
#
# Fonte legivel: docs/decisions/ADR-001-shura-orquestrador-mestre.md
# Fonte executavel: .mecha/intelligence/rules/orchestration_rules.json
# ==============================================================================

import os
import sys
import time
import json
import logging
import argparse
from typing import Dict, Any, List, Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from agent_bus import AgentBus, BusMessage, MessageType, AgentStatus
import shura_gate

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    level=logging.INFO)
logger = logging.getLogger("MECHA_ShuraDaemon")

_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_WORKSPACE_ROOT = os.path.abspath(os.path.join(_THIS_DIR, "..", "..", ".."))
_REPORTS_DIR = os.path.join(_WORKSPACE_ROOT, ".mecha", "ops", "logs", "reports")

SHURA_ID = "tribunal.shura_255"
MONITORED_CHANNELS = ["pipeline.events", "squad.dev", "squad.qa",
                      "squad.devops", "squad.product"]
# Sequencia esperada de squads para detectar fim de pipeline (ORCH-08)
PIPELINE_TERMINAL_SQUAD = "devops"


class ShuraDaemon:
    """Orquestrador-Mestre como consumidor do AgentBus (ORCH-05..09)."""

    def __init__(self, bus: AgentBus = None, workspace_root: str = None):
        self.bus = bus or AgentBus.get_instance()
        self.workspace_root = workspace_root or _WORKSPACE_ROOT
        self.rules = shura_gate.load_rules()
        self.threads: Dict[str, Dict[str, Any]] = {}
        self._running = False
        os.makedirs(_REPORTS_DIR, exist_ok=True)
        self._register()

    def _register(self):
        if not self.bus.get_agent(SHURA_ID):
            self.bus.register(SHURA_ID, "Shura 255", squad="tribunal",
                              role="Master Orchestrator",
                              capabilities=["orchestration", "judgment", "consolidation"])
        for ch in MONITORED_CHANNELS:
            self.bus.subscribe(SHURA_ID, ch)          # ORCH-05
        logger.info("[SHURA] Monitorando %d canais (ORCH-05)", len(MONITORED_CHANNELS))

    def _state(self, thread_id: str) -> Dict[str, Any]:
        return self.threads.setdefault(thread_id, {
            "squads": {}, "outputs": [], "events": [],
            "handoffs_approved": 0, "handoffs_blocked": 0, "blocks": [],
        })

    def poll_once(self) -> int:
        """ORCH-05: drena o inbox do Shura e processa cada evento."""
        inbox = self.bus.get_inbox(SHURA_ID, unread_only=True)
        for msg in inbox:
            try:
                self._handle(msg)
            finally:
                self.bus.acknowledge(SHURA_ID, msg.msg_id)
        return len(inbox)

    def _handle(self, msg: BusMessage):
        payload = msg.payload or {}
        event = payload.get("event", "")
        thread_id = payload.get("thread_id") or msg.thread_id or "global"
        st = self._state(thread_id)
        st["events"].append(event)

        if event == "workflow.completed":
            squad = (payload.get("squad") or "").replace("_squad", "")
            st["squads"][squad] = "completed"
            for v in payload.get("output_vars", []):
                st["outputs"].append("%s:%s" % (squad, v))
            if squad == PIPELINE_TERMINAL_SQUAD:
                self.consolidate(thread_id)            # ORCH-07/08
        elif event == "handoff.approved":
            st["handoffs_approved"] += 1
        elif event in ("handoff.blocked",):
            st["handoffs_blocked"] += 1
            st["blocks"].append(payload.get("reason", "?"))
            logger.warning("[SHURA] Handoff BLOQUEADO (ORCH-03): %s", payload.get("reason"))

    # ------------------------------------------------------------------ ORCH-06
    def run_build_tests(self) -> Dict[str, Any]:
        """
        Gate de build + testes (ORCH-06). HOOK SEGURO: por padrao NAO executa
        comandos (evita efeitos colaterais). Configure BUILD_CMD / TEST_CMD via
        env para ligar a execucao real (ex.: 'npm run build', 'pytest -q').
        """
        build_cmd = os.environ.get("SHURA_BUILD_CMD")
        test_cmd = os.environ.get("SHURA_TEST_CMD")
        if not build_cmd and not test_cmd:
            return {"build": "not_configured", "tests": "not_configured",
                    "note": "defina SHURA_BUILD_CMD / SHURA_TEST_CMD para executar"}
        import subprocess
        out = {}
        for label, cmd in (("build", build_cmd), ("tests", test_cmd)):
            if not cmd:
                out[label] = "skipped"
                continue
            try:
                p = subprocess.run(cmd, shell=True, cwd=self.workspace_root,
                                   capture_output=True, text=True, timeout=900)
                out[label] = "passed" if p.returncode == 0 else "failed"
            except Exception as e:
                out[label] = "error: %s" % e
        return out

    # --------------------------------------------------------------- ORCH-07/08
    def consolidate(self, thread_id: str) -> str:
        """Agrega (ORCH-07) e emite o relatorio dos 5 dominios (ORCH-08)."""
        st = self._state(thread_id)
        bt = self.run_build_tests()
        report = self._render_report(thread_id, st, bt)
        ts = time.strftime("%Y%m%d-%H%M%S")
        path = os.path.join(_REPORTS_DIR, "shura_%s_%s.md" % (thread_id.replace('/', '_'), ts))
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(report)
            logger.info("[SHURA] Relatorio consolidado (ORCH-08): %s", path)
        except Exception as e:
            logger.warning("[SHURA] Falha ao gravar relatorio: %s", e)
        self.bus.publish(SHURA_ID, "pipeline.events",
                         {"event": "consolidated", "thread_id": thread_id, "report_path": path})
        return report

    def _render_report(self, thread_id: str, st: Dict[str, Any], bt: Dict[str, Any]) -> str:
        squads = ", ".join(sorted(st["squads"].keys())) or "(nenhum)"
        outputs = ", ".join(st["outputs"]) or "(nenhum)"
        build, tests = bt.get("build", "?"), bt.get("tests", "?")
        green = build in ("passed", "not_configured") and tests in ("passed", "not_configured")
        verdict = "[1] Entregue" if green and st["handoffs_blocked"] == 0 else "[0] Bloqueado"
        blocks = "; ".join(st["blocks"]) if st["blocks"] else "nenhum"
        return (
            "# Relatorio de Consolidacao - Shura 255\n\n"
            "Thread: %s  |  Gerado: %s  |  Governanca: ADR-001 (ORCH-01..10)\n\n"
            "## 1. Codigo\nSquads concluidos: %s.\nOutputs: %s.\n\n"
            "## 2. Arquitetura\nHandoffs aprovados: %d | bloqueados: %d.\nMotivos de bloqueio: %s.\n\n"
            "## 3. Engenharia\nEventos processados: %d.\n\n"
            "## 4. Testes\nBuild: %s | Tests: %s.\n\n"
            "## 5. Produto\nPipeline: %s.\n\n"
            "## Veredito Final\n%s\n"
            % (thread_id, time.strftime("%Y-%m-%d %H:%M:%S"), squads, outputs,
               st["handoffs_approved"], st["handoffs_blocked"], blocks,
               len(st["events"]), build, tests,
               "completo" if "devops" in st["squads"] else "incompleto", verdict)
        )

    # ------------------------------------------------------------------ ORCH-09
    def run_forever(self, interval: float = 2.0):
        self._running = True
        logger.info("[SHURA] Daemon iniciado (ORCH-09, event-driven). Ctrl+C para sair.")
        try:
            while self._running:
                self.poll_once()
                time.sleep(interval)
        except KeyboardInterrupt:
            logger.info("[SHURA] Daemon encerrado pelo usuario.")
        self._running = False

    def run_once(self) -> int:
        """Excecao ORCH-09: modo CI/teste one-shot."""
        return self.poll_once()


def _demo():
    """Demonstra o daemon end-to-end publicando eventos sinteticos no bus."""
    bus = AgentBus.get_instance()
    d = ShuraDaemon(bus=bus)
    tid = "demo_thread"
    bus.publish("router", "pipeline.events",
                {"event": "workflow.completed", "squad": "dev_squad",
                 "output_vars": ["implementation"], "thread_id": tid})
    bus.publish("router", "pipeline.events",
                {"event": "handoff.approved", "route": "dev_to_qa", "thread_id": tid})
    bus.publish("router", "pipeline.events",
                {"event": "workflow.completed", "squad": "qa_squad",
                 "output_vars": ["qa_final_report"], "thread_id": tid})
    bus.publish("router", "pipeline.events",
                {"event": "handoff.approved", "route": "qa_to_devops", "thread_id": tid})
    bus.publish("router", "pipeline.events",
                {"event": "workflow.completed", "squad": "devops_squad",
                 "output_vars": ["deploy_manifest"], "thread_id": tid})
    processed = d.run_once()   # drena e consolida ao ver devops
    print("Eventos processados:", processed)
    print("--- RELATORIO ---")
    print(d._render_report(tid, d._state(tid), d.run_build_tests()))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Shura Daemon - Master Orchestrator")
    ap.add_argument("--mode", choices=["run", "once", "demo"], default="demo")
    args = ap.parse_args()
    if args.mode == "demo":
        _demo()
    elif args.mode == "once":
        n = ShuraDaemon().run_once()
        print("Processados:", n)
    else:
        ShuraDaemon().run_forever()
