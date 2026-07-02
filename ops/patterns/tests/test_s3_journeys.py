# -*- coding: utf-8 -*-
"""
test_s3_journeys — Sprint S3: pipelines novos + handler AgentBus + gaps consolidation.

Cobre:
  (a) journey_batch_trigger_pipeline e journey_otp_fallback_pipeline
      existem e parseiam corretamente no sendspeed_workflows.json
  (b) entry_inputs declarados nos 2 pipelines novos
  (c) SendSpeedJourneyHandler: attach/detach, mapa de tópicos, dispatch smoke
  (d) EventEnvelope emitido pelo handler é válido via dynamic_typing
  (e) workflow.started e workflow.completed publicados no pipeline.events
  (f) sendspeed_gaps() retorna campo 'consolidations' com nota 449⊂446
  (g) run_squad_workflow com pipelines novos via mock (MECHA_FORCE_MOCK_LLM=1)
"""

import asyncio
import json
import os
import time

import pytest

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
_TESTS_DIR   = os.path.dirname(__file__)
_PATTERNS    = os.path.abspath(os.path.join(_TESTS_DIR, ".."))
_MECHA       = os.path.abspath(os.path.join(_PATTERNS, "..", ".."))
_WORKSPACE   = os.path.abspath(os.path.join(_MECHA, ".."))   # pai do .mecha
WORKFLOWS_F  = os.path.join(_MECHA, "intelligence", "squads", "sendspeed_workflows.json")

NEW_PIPELINES = ["journey_batch_trigger_pipeline", "journey_otp_fallback_pipeline"]


def _load(path):
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


# ---------------------------------------------------------------------------
# (a) Pipelines novos existem e parseiam
# ---------------------------------------------------------------------------

def test_new_pipelines_exist_in_workflows():
    wf = _load(WORKFLOWS_F)
    for pid in NEW_PIPELINES:
        assert pid in wf, f"pipeline ausente: {pid}"
        pipe = wf[pid]
        assert pipe.get("name"), f"{pid} sem name"
        assert pipe.get("description"), f"{pid} sem description"
        steps = pipe.get("steps")
        assert isinstance(steps, list) and steps, f"{pid} sem steps"


def test_new_pipelines_have_valid_dag():
    """Steps dependem apenas de outputs anteriores ou de user_prompt."""
    wf = _load(WORKFLOWS_F)
    for pid in NEW_PIPELINES:
        outputs = set()
        for step in wf[pid]["steps"]:
            srcs = step.get("input_sources") or (
                [step["input_source"]] if step.get("input_source") else []
            )
            assert srcs, f"{pid} step {step['step_id']}: sem inputs"
            for src in srcs:
                assert src == "user_prompt" or src in outputs, (
                    f"{pid} step {step['step_id']}: '{src}' não produzido antes"
                )
            outputs.add(step["output_var"])


def test_new_pipelines_end_with_smartflowbot():
    wf = _load(WORKFLOWS_F)
    for pid in NEW_PIPELINES:
        last = wf[pid]["steps"][-1]
        assert last["agent"] == "SmartFlowBot", (
            f"{pid}: último step deve ser SmartFlowBot, veio {last['agent']}"
        )


# ---------------------------------------------------------------------------
# (b) entry_inputs declarados nos 2 pipelines novos
# ---------------------------------------------------------------------------

def test_new_pipelines_have_entry_inputs():
    wf = _load(WORKFLOWS_F)
    for pid in NEW_PIPELINES:
        meta = wf[pid].get("metadata") or {}
        entry = meta.get("entry_inputs")
        assert entry, f"{pid}: entry_inputs ausente no metadata"
        assert isinstance(entry, dict) and entry, f"{pid}: entry_inputs vazio"


# ---------------------------------------------------------------------------
# (c) SendSpeedJourneyHandler: attach/detach, mapa de tópicos
# ---------------------------------------------------------------------------

def test_handler_imports_and_has_topic_map():
    import sendspeed_journey_handler as sjh
    assert sjh.TOPIC_TO_PIPELINE
    assert "journey.trigger" in sjh.TOPIC_TO_PIPELINE
    assert "journey.otp"     in sjh.TOPIC_TO_PIPELINE
    assert "journey.batch_trigger_pipeline" not in sjh.TOPIC_TO_PIPELINE  # nome antigo


def test_handler_attach_detach():
    from agent_bus import AgentBus
    AgentBus.reset()
    bus = AgentBus.get_instance()

    import sendspeed_journey_handler as sjh
    h = sjh.SendSpeedJourneyHandler(workspace_root=_WORKSPACE, bus=bus)
    assert not h._attached
    h.attach()
    assert h._attached
    assert bus.get_agent(sjh.HANDLER_AGENT_ID) is not None
    h.detach()
    assert not h._attached


def test_handler_stats_initial():
    from agent_bus import AgentBus
    AgentBus.reset()
    bus = AgentBus.get_instance()

    import sendspeed_journey_handler as sjh
    h = sjh.SendSpeedJourneyHandler(workspace_root=_WORKSPACE, bus=bus)
    h.attach()
    s = h.stats()
    assert s["attached"]
    assert s["processed"] == 0
    assert s["errors"] == 0
    assert len(s["topics"]) == 5


# ---------------------------------------------------------------------------
# (d) EventEnvelope emitido: valid via dynamic_typing
# ---------------------------------------------------------------------------

def test_journey_event_envelope_is_valid():
    """O payload que o handler publica deve passar no validate_event_envelope."""
    import sys as _sys
    _sys.path.insert(0, os.path.join(_MECHA, "kernel", "validators"))
    try:
        from dynamic_typing import validate_event_envelope
    except ImportError:
        pytest.skip("dynamic_typing indisponível")

    envelope = {
        "topic":     "journey.otp",
        "sender":    "test.agent",
        "timestamp": int(time.time()),
        "payload":   {"user_prompt": "teste", "thread_id": "t_001"},
    }
    ok, msg = validate_event_envelope(envelope)
    assert ok, f"EventEnvelope inválido: {msg}"


# ---------------------------------------------------------------------------
# (e) workflow.started e workflow.completed publicados
# ---------------------------------------------------------------------------

def test_bus_events_published_on_dispatch(monkeypatch):
    """
    Verifica que o handler emite workflow.started e workflow.completed
    no canal pipeline.events durante um dispatch com mock LLM.
    """
    import sendspeed_journey_handler as sjh
    from agent_bus import AgentBus

    AgentBus.reset()
    bus = AgentBus.get_instance()
    monkeypatch.setenv("MECHA_FORCE_MOCK_LLM", "1")

    h = sjh.SendSpeedJourneyHandler(workspace_root=_WORKSPACE, bus=bus)
    h.attach()

    # Registra observer no canal pipeline.events
    events_received = []
    bus.on_channel(sjh.PIPELINE_CHANNEL, lambda msg: events_received.append(msg.payload.copy()))

    # Dispara via asyncio.run (síncrono)
    asyncio.run(h._dispatch(
        pipeline_key="journey_otp_fallback_pipeline",
        prompt="smoke started/completed",
        thread_id="test_bus_t001",
        topic="journey.otp",
    ))

    event_types = [e.get("event") for e in events_received]
    assert "workflow.started"   in event_types, f"workflow.started ausente: {event_types}"
    assert "workflow.completed" in event_types, f"workflow.completed ausente: {event_types}"

    # Verifica mock flag no completed
    completed = next(e for e in events_received if e.get("event") == "workflow.completed")
    assert completed.get("mock") is True


# ---------------------------------------------------------------------------
# (f) sendspeed_gaps() retorna campo 'consolidations' com nota 449⊂446
# ---------------------------------------------------------------------------

pytest.importorskip("mcp.server.fastmcp", reason="pacote mcp não instalado")
import sendspeed_mcp_server as sss  # noqa: E402


def test_sendspeed_gaps_has_consolidation_note():
    result = sss.sendspeed_gaps()
    assert "error" not in result, result.get("error")
    assert "consolidations" in result, "campo consolidations ausente"
    notes = [c.get("note", "") for c in result["consolidations"]]
    assert any("449" in n and "446" in n for n in notes), (
        f"nota 449⊂446 não encontrada em consolidations: {notes}"
    )


def test_sendspeed_gaps_consolidation_has_action():
    result = sss.sendspeed_gaps()
    for c in result.get("consolidations", []):
        assert c.get("action"), f"consolidation sem action: {c}"
        assert c.get("status"), f"consolidation sem status: {c}"


# ---------------------------------------------------------------------------
# (g) run_squad_workflow com pipelines novos via mock
# ---------------------------------------------------------------------------

import mecha_mcp_server as mms  # noqa: E402


@pytest.mark.parametrize("pipeline_key,expected_var", [
    ("journey_batch_trigger_pipeline",   "batch_trigger_verdict"),
    ("journey_otp_fallback_pipeline",    "otp_fallback_verdict"),
])
def test_run_squad_workflow_new_pipelines_mock(pipeline_key, expected_var, monkeypatch):
    monkeypatch.setenv("MECHA_FORCE_MOCK_LLM", "1")
    result = mms.run_squad_workflow(
        squad_name="sendspeed_squad",
        workflow_name="sendspeed_workflows",
        pipeline_key=pipeline_key,
        prompt=f"smoke {pipeline_key}",
    )
    assert "error" not in result, f"ERRO em {pipeline_key}: {result.get('error')}"
    assert expected_var in result, f"output_var '{expected_var}' ausente em {pipeline_key}: {list(result.keys())}"
    assert result.get("mock") is True, f"mock=True ausente em {pipeline_key}"


# ===========================================================================
# Regressão entry_inputs — Let It Fail no SquadOrchestrator (S3)
# ===========================================================================

import sys as _sys
_sys.path.insert(0, _PATTERNS)
from squad_orchestrator import SquadOrchestrator  # noqa: E402


def _orch():
    return SquadOrchestrator(_WORKSPACE)


def test_entry_inputs_let_it_fail_missing_input(monkeypatch):
    """
    Orchestrator deve falhar com RuntimeError explícito quando initial_inputs
    não contém o input raiz exigido pelo pipeline — sem adivinhar por nome de squad.
    """
    import asyncio
    monkeypatch.setenv("MECHA_FORCE_MOCK_LLM", "1")
    orch = _orch()
    with pytest.raises((RuntimeError, ValueError)):
        asyncio.run(orch.run_workflow(
            squad_name="sendspeed_squad",
            workflow_name="sendspeed_workflows",
            pipeline_key="journey_otp_fallback_pipeline",
            initial_inputs={"wrong_key": "nada aqui"},   # user_prompt ausente → Let It Fail
        ))


def test_entry_inputs_qa_squad_regression(monkeypatch):
    """
    qa_squad ainda funciona com source_code explícito em initial_inputs —
    o mecanismo genérico não quebra squads que não usam entry_inputs.
    """
    import asyncio
    monkeypatch.setenv("MECHA_FORCE_MOCK_LLM", "1")
    orch = _orch()
    result = asyncio.run(orch.run_workflow(
        squad_name="qa_squad",
        workflow_name="qa_workflows",
        pipeline_key="qa_audit_pipeline",
        initial_inputs={"source_code": "def foo(): pass", "test_code": ""},
    ))
    assert isinstance(result, dict)
    assert "error" not in result
    assert result.get("mock") is True


def test_entry_inputs_sendspeed_user_prompt(monkeypatch):
    """
    Pipelines sendspeed que usam user_prompt como raiz funcionam com
    initial_inputs={"user_prompt": "..."}.
    """
    import asyncio
    monkeypatch.setenv("MECHA_FORCE_MOCK_LLM", "1")
    orch = _orch()
    result = asyncio.run(orch.run_workflow(
        squad_name="sendspeed_squad",
        workflow_name="sendspeed_workflows",
        pipeline_key="journey_batch_trigger_pipeline",
        initial_inputs={"user_prompt": "regressao entry_inputs"},
    ))
    assert isinstance(result, dict)
    assert "error" not in result
    assert result.get("mock") is True


# ===========================================================================
# Tools enriquecidas — journey_engine_map e journey_objective_attribution (S3)
# ===========================================================================

def test_journey_engine_map_enriched():
    """journey_engine_map deve conter batch_trigger_contract e pending_status (S3)."""
    result = sss.journey_engine_map()
    assert "error" not in result, result.get("error")
    assert "batch_trigger_contract" in result, "batch_trigger_contract ausente"
    assert "pending_status" in result, "pending_status ausente"
    assert "cold_list_upload" in result, "cold_list_upload ausente"
    # Verifica campos do contrato de batch trigger
    btc = result["batch_trigger_contract"]
    assert btc.get("endpoint"), "endpoint ausente"
    assert "batchId" in str(btc), "batchId ausente no contrato"
    # Verifica invariante do status Pendente
    ps = result["pending_status"]
    assert "Enviado" in ps.get("invariant", ""), "invariante Enviado ausente"


def test_journey_objective_attribution_enriched():
    """journey_objective_attribution deve conter attribution_model e shortener_consolidation (S3)."""
    result = sss.journey_objective_attribution()
    assert "error" not in result, result.get("error")
    assert "attribution_model" in result, "attribution_model ausente"
    assert "shortener_consolidation" in result, "shortener_consolidation ausente"
    assert "rcs_templates" in result, "rcs_templates ausente"
    # Verifica janela de atribuição
    am = result["attribution_model"]
    assert "24h" in am.get("window", ""), "janela 24h ausente"
    assert "taxa_entrega" in am.get("metrics", {}), "taxa_entrega ausente"
    # Verifica consolidação 449⊂446
    sc = result["shortener_consolidation"]
    assert "449" in sc.get("note", ""), "nota 449 ausente"
    assert "446" in sc.get("note", ""), "nota 446 ausente"
    assert sc.get("status") == "pending_consolidation"


def test_journey_engine_map_documents_present():
    """journey_engine_map deve retornar documentos das issues SEND-391, SEND-477, SEND-479."""
    result = sss.journey_engine_map()
    assert "error" not in result
    docs = result.get("documents", [])
    ids_in_docs = {d.get("id") for d in docs}
    for expected in ["SEND-391", "SEND-477", "SEND-479"]:
        assert expected in ids_in_docs, f"{expected} ausente nos documentos de journey_engine_map"


def test_journey_objective_attribution_documents_present():
    """journey_objective_attribution deve retornar documentos de SEND-450, SEND-446, SEND-449."""
    result = sss.journey_objective_attribution()
    assert "error" not in result
    docs = result.get("documents", [])
    ids_in_docs = {d.get("id") for d in docs}
    for expected in ["SEND-450", "SEND-446", "SEND-449"]:
        assert expected in ids_in_docs, f"{expected} ausente nos documentos de journey_objective_attribution"
