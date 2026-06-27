# ==============================================================================
# SHURA GATE - HANDOFF VALIDATION (ORCH-02 / ORCH-03 / ORCH-04)
# ==============================================================================
# Modulo aditivo de enforcement da governanca de orquestracao Mecha.
# Implementa as regras RIGIDAS de handoff do ADR-001 em CODIGO (ORCH-10).
#
# Fonte legivel:   docs/decisions/ADR-001-shura-orquestrador-mestre.md
# Fonte executavel: .mecha/intelligence/rules/orchestration_rules.json
#
# Integracao: chamado por CrossSquadRouter._check_and_chain ANTES de encadear
# para o squad de destino. Ver bloco INTEGRATION no fim deste arquivo.
# ==============================================================================

import os
import json
import time
import logging
from dataclasses import dataclass, field, asdict
from typing import Dict, Any, List, Optional

logger = logging.getLogger("MECHA_ShuraGate")

# Resolve workspace root: .mecha/ops/patterns/ -> workspace root
_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_WORKSPACE_ROOT = os.path.abspath(os.path.join(_THIS_DIR, "..", "..", ".."))
_RULES_PATH = os.path.join(_WORKSPACE_ROOT, ".mecha", "intelligence", "rules",
                           "orchestration_rules.json")


def load_rules(path: str = _RULES_PATH) -> Dict[str, Any]:
    """Carrega as regras rigidas (ORCH-01..10). Nunca levanta excecao."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.warning("[SHURA_GATE] Falha ao carregar regras de %s: %s", path, e)
        return {"version": "0", "rules": []}


# Mapa de dominios: qual squad e dono de qual dominio e de quem aceita handoff.
# Espelha SQUAD_ROUTES em cross_squad_router.py (ORCH-04).
DOMAIN_MAP: Dict[str, Dict[str, Any]] = {
    "dev":      {"domain": "development", "accepts_from": ["*"]},
    "qa":       {"domain": "quality",     "accepts_from": ["dev"]},
    "devops":   {"domain": "operations",  "accepts_from": ["qa"]},
    "product":  {"domain": "product",     "accepts_from": ["devops", "qa"]},
    "tribunal": {"domain": "governance",  "accepts_from": ["*"]},
}


@dataclass
class GateResult:
    verdict: int               # 1 = aprova (avanca), 0 = bloqueia (volta a origem)
    from_squad: str
    to_squad: str
    route_name: str
    reason: str
    rules_applied: List[str] = field(default_factory=list)
    timestamp: float = field(default_factory=time.time)

    @property
    def approved(self) -> bool:
        return self.verdict == 1

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def _norm(squad: str) -> str:
    return (squad or "").replace("_squad", "").strip().lower()


def validate_domain(from_squad: str, to_squad: str) -> Optional[str]:
    """ORCH-04: destino deve ter dominio que aceita a origem. Retorna motivo se INVALIDO."""
    t = _norm(to_squad)
    s = _norm(from_squad)
    spec = DOMAIN_MAP.get(t)
    if not spec:
        return "ORCH-04: squad de destino '%s' sem dominio declarado" % t
    accepts = spec.get("accepts_from", [])
    if "*" in accepts or s in accepts:
        return None
    return "ORCH-04: dominio '%s' nao aceita handoff de '%s'" % (t, s)


def validate_exit_criteria(artifacts: Dict[str, Any], trigger_condition: Optional[str],
                           trigger_output_value: Optional[str]) -> Optional[str]:
    """ORCH-02: origem deve ter produzido artefatos / passado o gatilho. Motivo se INVALIDO."""
    if not artifacts:
        return "ORCH-02: nenhum artefato de entrega produzido pela origem"
    if trigger_condition:
        if trigger_condition not in (trigger_output_value or ""):
            return "ORCH-02: condicao de gatilho '%s' nao atendida" % trigger_condition
    return None


def validate_handoff(task: Any, from_squad: str, to_squad: str,
                     route_name: str = "",
                     artifacts: Optional[Dict[str, Any]] = None,
                     trigger_condition: Optional[str] = None,
                     trigger_output_value: Optional[str] = None) -> GateResult:
    """
    O gate de handoff. Retorna GateResult com verdict 1 (aprova) ou 0 (bloqueia).

    ORCH-02: handoff exige artefatos produzidos / gatilho atendido.
    ORCH-04: dominio de destino deve aceitar a origem.
    ORCH-03 (bloqueia -> volta a origem) e aplicado pelo CHAMADOR no verdict==0.
    """
    artifacts = artifacts or {}
    rules_applied: List[str] = []
    reasons: List[str] = []

    dom_reason = validate_domain(from_squad, to_squad)   # ORCH-04
    rules_applied.append("ORCH-04")
    if dom_reason:
        reasons.append(dom_reason)

    exit_reason = validate_exit_criteria(artifacts, trigger_condition,
                                         trigger_output_value)   # ORCH-02
    rules_applied.append("ORCH-02")
    if exit_reason:
        reasons.append(exit_reason)

    if reasons:
        result = GateResult(0, from_squad, to_squad, route_name,
                            " | ".join(reasons), rules_applied)
        logger.info("[SHURA_GATE] BLOCKED %s->%s: %s", from_squad, to_squad, result.reason)
        return result

    result = GateResult(1, from_squad, to_squad, route_name,
                        "Handoff aprovado: dominio e criterios de saida OK", rules_applied)
    logger.info("[SHURA_GATE] APPROVED %s->%s via %s", from_squad, to_squad, route_name)
    return result


# ==============================================================================
# INTEGRATION (cross_squad_router.py :: CrossSquadRouter._check_and_chain)
# ------------------------------------------------------------------------------
# Inserir ANTES da chamada:
#     chain_result = await self.run_squad_workflow(target_squad_file, ...)
# (depois de montar `target_inputs`, dentro do loop de rotas), o bloco:
#
#     import shura_gate
#     gate = shura_gate.validate_handoff(
#         task=results, from_squad=source_squad, to_squad=target_squad_file,
#         route_name=route_name, artifacts=target_inputs,
#         trigger_condition=route.get("trigger_condition"),
#         trigger_output_value=str(results.get(route.get("trigger_output", ""), "")),
#     )
#     self.bus.publish("router", "pipeline.events", {
#         "event": "handoff.approved" if gate.approved else "handoff.blocked",
#         "route": route_name, "from": source_squad, "to": target_squad_file,
#         "reason": gate.reason, "thread_id": thread_id,
#     })
#     if not gate.approved:                  # ORCH-03: bloqueia + volta a origem
#         return {"_handoff_blocked": gate.to_dict()}
#
# Isso torna ORCH-02/03/04 aplicadas em CODIGO (ORCH-10), nao so no prompt.
# ==============================================================================


if __name__ == "__main__":
    # Smoke test (seguro, sem efeitos colaterais)
    logging.basicConfig(level=logging.INFO)
    r = load_rules()
    print("Loaded %d rules, version %s" % (len(r.get("rules", [])), r.get("version")))

    ok = validate_handoff({}, "dev", "qa", "dev_to_qa",
                          artifacts={"implementation": "code"},
                          trigger_condition="[APROVADO]",
                          trigger_output_value="status: [APROVADO]")
    print("dev->qa (OK esperado=1):", ok.verdict, "|", ok.reason)

    skip = validate_handoff({}, "dev", "devops", "x",
                            artifacts={"implementation": "code"})
    print("dev->devops pula qa (esperado=0):", skip.verdict, "|", skip.reason)

    noart = validate_handoff({}, "dev", "qa", "dev_to_qa", artifacts={})
    print("dev->qa sem artefatos (esperado=0):", noart.verdict, "|", noart.reason)
