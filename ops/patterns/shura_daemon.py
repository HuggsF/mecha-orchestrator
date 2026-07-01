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
from collections import Counter
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
_OPS_ENV = os.path.join(_WORKSPACE_ROOT, ".mecha", "ops", ".env")


def _load_dotenv(path: str) -> None:
    """Carrega KEY=VALUE do .env do .mecha em os.environ (sem sobrescrever o ja definido).
    Chamado so no __main__ (producao) -> nao afeta testes que importam o modulo."""
    if not os.path.exists(path):
        return
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())
    except Exception:
        pass

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
        self._orch06_streak = 0   # Item 4: recorrencia de ORCH-06 entre execucoes consecutivas
        self._orch06_threshold = max(1, int(os.environ.get("SHURA_ORCH06_RECURRENCE", "3")))
        self._fix_squad = os.environ.get("SHURA_FIX_SQUAD", "dev")
        os.makedirs(_REPORTS_DIR, exist_ok=True)
        self._register()
        # Item 5: espelhamento ao vivo p/ o Digital Twin Neo4j (opt-in; fail-safe se Neo4j off)
        self.bridge = None
        if os.environ.get("SHURA_NEO4J_BRIDGE", "0") == "1":
            try:
                from neo4j_orchestration_bridge import Neo4jOrchestrationBridge
                self.bridge = Neo4jOrchestrationBridge(self.bus)
            except Exception as e:
                logger.warning("[SHURA] Bridge Neo4j nao iniciada: %s", e)

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
            "started_at": None,
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
        if st.get("started_at") is None:
            st["started_at"] = getattr(msg, "timestamp", time.time())
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
        elif event == "build.result":
            # ORCH-06 quick-fail: build nao-verde bloqueia o handoff na fonte (sem verde, nao avanca da fase Garantir)
            status = (payload.get("status") or "").lower()
            if status not in ("green", "passed", "success", "ok"):
                squad = payload.get("squad", "?")
                reason = "build '%s' no squad %s (ORCH-06 quick-fail)" % (status or "desconhecido", squad)
                st["handoffs_blocked"] += 1
                st["blocks"].append(reason)
                logger.warning("[SHURA] QUICK-FAIL de build (ORCH-06): %s", reason)
                self.bus.publish(SHURA_ID, "pipeline.events", {
                    "event": "handoff.blocked", "rule": "ORCH-06", "squad": squad,
                    "reason": reason, "thread_id": thread_id
                })

    # ------------------------------------------------------------------ ORCH-06
    def run_build_tests(self) -> Dict[str, Any]:
        """
        Gate de build + testes (ORCH-06), com SUBSTATUS por nivel (unit/integration/e2e)
        e cobertura. HOOK SEGURO: por padrao NAO executa nada (not_configured).
        Configure via env para ligar execucao real:
          SHURA_BUILD_CMD, SHURA_TEST_UNIT_CMD, SHURA_TEST_INTEGRATION_CMD,
          SHURA_TEST_E2E_CMD, SHURA_TEST_CMD (generico), SHURA_COVERAGE_CMD.
        """
        build, _ = self._run_cmd(os.environ.get("SHURA_BUILD_CMD"))
        levels: Dict[str, str] = {}
        agg_out = ""
        for level, env in (("unit", "SHURA_TEST_UNIT_CMD"),
                           ("integration", "SHURA_TEST_INTEGRATION_CMD"),
                           ("e2e", "SHURA_TEST_E2E_CMD"),
                           ("generic", "SHURA_TEST_CMD")):
            status, out = self._run_cmd(os.environ.get(env))
            levels[level] = status
            agg_out += out
        cov_cmd = os.environ.get("SHURA_COVERAGE_CMD")
        if cov_cmd:
            _, cov_out = self._run_cmd(cov_cmd)
            agg_out += cov_out
        return {"build": build, "tests": levels,
                "coverage": self._parse_coverage(agg_out),
                "summary": self._parse_pytest_summary(agg_out)}

    def _run_cmd(self, cmd: Optional[str]):
        """Roda um comando shell (cwd=workspace) e devolve (status, stdout+stderr). not_configured se vazio."""
        if not cmd:
            return "not_configured", ""
        import subprocess
        try:
            p = subprocess.run(cmd, shell=True, cwd=self.workspace_root,
                               capture_output=True, text=True, timeout=900)
            return ("passed" if p.returncode == 0 else "failed"), ((p.stdout or "") + (p.stderr or ""))
        except Exception as e:
            return ("error: %s" % e), ""

    @staticmethod
    def _parse_coverage(text: str) -> Optional[float]:
        """Extrai % de cobertura (linha TOTAL do coverage.py/pytest-cov; fallback: ultimo % do output)."""
        import re
        m = re.search(r'TOTAL[^\n]*?(\d+(?:\.\d+)?)%', text)
        if m:
            return float(m.group(1))
        allp = re.findall(r'(\d+(?:\.\d+)?)%', text)
        return float(allp[-1]) if allp else None

    @staticmethod
    def _parse_pytest_summary(text: str) -> Optional[Dict[str, int]]:
        """Extrai 'N passed, M failed' do resumo do pytest, se presente."""
        import re
        passed = re.search(r'(\d+)\s+passed', text)
        failed = re.search(r'(\d+)\s+failed', text)
        if not passed and not failed:
            return None
        return {"passed": int(passed.group(1)) if passed else 0,
                "failed": int(failed.group(1)) if failed else 0}

    @staticmethod
    def _is_green(bt: Dict[str, Any]) -> bool:
        """Verde = build + todos os niveis de teste em passed/not_configured."""
        passing = ("passed", "not_configured")
        if bt.get("build") not in passing:
            return False
        for st in (bt.get("tests") or {}).values():
            if st not in passing:
                return False
        return True

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
        self._check_recurrence(thread_id, st)   # Item 4: detector de recorrencia ORCH-06
        verdict = "[1] Entregue" if self._is_green(bt) and st["handoffs_blocked"] == 0 else "[0] Bloqueado"
        self.bus.publish(SHURA_ID, "pipeline.events",
                         {"event": "consolidated", "thread_id": thread_id, "report_path": path,
                          "verdict": verdict, "handoffs_blocked": st["handoffs_blocked"]})
        return report

    def _check_recurrence(self, thread_id: str, st: Dict[str, Any]) -> None:
        """
        Item 4 (CI reativo ao ORCH-09, grounded): se ORCH-06 (quick-fail de build)
        recorrer em >= N execucoes CONSECUTIVAS, emite alerta 'rule.recurrence' +
        pedido de correcao ao squad de fix (default 'dev'; o 'code-fixing-squad' do
        plano original nao existe). NAO cria PR de verdade (sem infra de PR wired) —
        emite o evento acionavel para automacao/operador. Run verde reseta o streak.
        """
        had = any("ORCH-06" in b for b in st.get("blocks", []))
        if not had:
            self._orch06_streak = 0
            return
        self._orch06_streak += 1
        if self._orch06_streak >= self._orch06_threshold:
            reason = next((b for b in st.get("blocks", []) if "ORCH-06" in b), "ORCH-06")
            logger.warning("[SHURA] RECORRENCIA ORCH-06: %d execucoes consecutivas (limite %d) -> fix em '%s'",
                           self._orch06_streak, self._orch06_threshold, self._fix_squad)
            self.bus.publish(SHURA_ID, "pipeline.events", {
                "event": "rule.recurrence", "rule": "ORCH-06",
                "streak": self._orch06_streak, "threshold": self._orch06_threshold,
                "fix_squad": self._fix_squad, "recommended_action": "route_fix",
                "reason": reason, "thread_id": thread_id
            })

    def _render_report(self, thread_id: str, st: Dict[str, Any], bt: Dict[str, Any]) -> str:
        squads = ", ".join(sorted(st["squads"].keys())) or "(nenhum)"
        outputs = ", ".join(st["outputs"]) or "(nenhum)"
        build = bt.get("build", "?")
        green = self._is_green(bt)
        verdict = "[1] Entregue" if green and st["handoffs_blocked"] == 0 else "[0] Bloqueado"
        blocks = "; ".join(st["blocks"]) if st["blocks"] else "nenhum"
        tests = bt.get("tests") or {}
        levels = " | ".join("%s=%s" % (k, v) for k, v in tests.items() if v != "not_configured") or "not_configured"
        cov = bt.get("coverage")
        cov_s = ("%.0f%%" % cov) if cov is not None else "n/d"
        summ = bt.get("summary")
        summ_s = ("%d passed / %d failed" % (summ.get("passed", 0), summ.get("failed", 0))) if summ else "n/d"
        report = (
            "# Relatorio de Consolidacao - Shura 255\n\n"
            "Thread: %s  |  Gerado: %s  |  Governanca: ADR-001 (ORCH-01..13)\n\n"
            "## 1. Codigo\nSquads concluidos: %s.\nOutputs: %s.\n\n"
            "## 2. Arquitetura\nHandoffs aprovados: %d | bloqueados: %d.\nMotivos de bloqueio: %s.\n\n"
            "## 3. Engenharia\nEventos processados: %d.\n\n"
            "## 4. Testes\nBuild: %s | Niveis: %s | Cobertura: %s | Resumo: %s.\n\n"
            "## 5. Produto\nPipeline: %s.\n\n"
            "## Veredito Final\n%s\n"
            % (thread_id, time.strftime("%Y-%m-%d %H:%M:%S"), squads, outputs,
               st["handoffs_approved"], st["handoffs_blocked"], blocks,
               len(st["events"]), build, levels, cov_s, summ_s,
               "completo" if "devops" in st["squads"] else "incompleto", verdict)
        )
        # ORCH-08 reforcado: camadas analiticas (insights + risk_flags) derivadas de dados REAIS
        return report + self._render_insights(st, bt, green, verdict)

    def _read_spend(self) -> Optional[float]:
        """Custo FinOps acumulado real (config_db.json gerado pelo SquadOrchestrator/CostTracker)."""
        path = os.path.join(self.workspace_root, ".mecha", "ops", "config_db.json")
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f).get("current_spend")
        except Exception:
            return None

    def _render_insights(self, st: Dict[str, Any], bt: Dict[str, Any], green: bool, verdict: str) -> str:
        """Camada de insights orientada a causa-efeito, derivada de eventos reais do AgentBus + custo + duracao."""
        ev = Counter(e for e in st.get("events", []) if e)
        n_rebal = ev.get("route.rebalanced", 0)
        blocks = st.get("blocks", [])
        n_orch12 = sum(1 for b in blocks if "ORCH-12" in b)
        n_orch06 = sum(1 for b in blocks if "ORCH-06" in b)
        spend = self._read_spend()
        spend_s = ("$%.4f USD" % spend) if spend is not None else "n/d"
        dur = (time.time() - st["started_at"]) if st.get("started_at") else None
        dur_s = ("~%.1fs" % max(0.0, dur)) if dur is not None else "n/d"
        ev_summary = ", ".join("%s=%d" % (k, v) for k, v in ev.most_common()) or "(nenhum)"
        build, tests = bt.get("build", "?"), bt.get("tests", "?")

        flags: List[str] = []
        if not green:
            flags.append("- [HIGH] Build/Testes nao-verde (build=%s, tests=%s)" % (build, tests))
        if st.get("handoffs_blocked", 0) > 0:
            flags.append("- [HIGH] %d handoff(s) bloqueado(s): %s" % (st["handoffs_blocked"], "; ".join(blocks) or "?"))
        if n_orch06 > 0:
            flags.append("- [MED] ORCH-06 quick-fail de build acionado (%d)" % n_orch06)
        if n_orch12 > 0:
            flags.append("- [MED] ORCH-12 pre-verificacao de dominio bloqueou handoff (%d)" % n_orch12)
        if n_rebal > 0:
            flags.append("- [INFO] ORCH-13 rebalanceou rota %d vez(es) (balanceamento de carga ativo)" % n_rebal)
        if verdict.startswith("[0]"):
            flags.append("- [HIGH] Veredito final BLOQUEADO")
        if not flags:
            flags.append("- [OK] Nenhuma flag de risco. Entrega limpa.")

        return (
            "\n## Insights\n"
            "- Eventos (por tipo): %s\n"
            "- Orquestracao: %d aprovados, %d bloqueados | ORCH-12: %d | ORCH-06: %d | ORCH-13 rebalance: %d\n"
            "- Engenharia: custo FinOps acumulado %s | duracao do pipeline %s\n"
            "- Codigo: %d outputs em %d squads\n"
            "- Prontidao p/ release: %s\n\n"
            "## Risk Flags\n%s\n"
            % (ev_summary, st.get("handoffs_approved", 0), st.get("handoffs_blocked", 0),
               n_orch12, n_orch06, n_rebal, spend_s, dur_s,
               len(st.get("outputs", [])), len(st.get("squads", {})),
               ("PRONTO" if green and st.get("handoffs_blocked", 0) == 0 else "BLOQUEADO"),
               "\n".join(flags))
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
    _load_dotenv(_OPS_ENV)   # producao: honra SHURA_* (ex.: SHURA_NEO4J_BRIDGE) do .mecha/ops/.env
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
