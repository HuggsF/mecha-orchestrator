# -*- coding: utf-8 -*-
# ==============================================================================
# TEST SENDSPEED ABSORPTION - Sprint 1 da absorcao SendSpeed no MECHA
# ==============================================================================
# Cobre (topologia O6):
#   (a) sendspeed_mcp_server importa sem erro e expoe as 20 tools esperadas;
#   (b) busca de issues encontra SEND-488 e SEND-515 no linear-export;
#   (c) sendspeed_squad.json / sendspeed_workflows.json parseiam e todos os
#       agentes referenciados nos workflows existem no squad;
#   (d) mcp_config.json parseia e contem 'sendspeed-mecha' E 'neo4j-mecha';
#   (e) tools de dominio respondem sem excecao (dict, sem 'error' inesperado).
#
# Sem dependencia de infra externa (Neo4j/Qdrant/APIs SendSpeed): tudo e
# read-only sobre arquivos locais. Recursos ausentes => pytest.skip gracioso.
# Paths de import resolvidos pelo conftest.py da suite (ops/patterns em sys.path).
# ==============================================================================

import asyncio
import json
import os

import pytest

pytest.importorskip("mcp.server.fastmcp", reason="pacote 'mcp' (FastMCP) nao instalado")

import sendspeed_mcp_server as sss  # noqa: E402  (depende do sys.path do conftest)

# ------------------------------------------------------------------------------
# Paths (mesma convencao do conftest: tests/ -> patterns/ -> ops/ -> .mecha)
# ------------------------------------------------------------------------------
_PATTERNS = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_MECHA = os.path.abspath(os.path.join(_PATTERNS, "..", ".."))
SQUADS_DIR = os.path.join(_MECHA, "intelligence", "squads")
SQUAD_FILE = os.path.join(SQUADS_DIR, "sendspeed_squad.json")
WORKFLOWS_FILE = os.path.join(SQUADS_DIR, "sendspeed_workflows.json")
MCP_CONFIG = os.path.join(_MECHA, "mcp_config.json")
LINEAR_INDEX = os.path.join(sss.LINEAR_EXPORT, "index.json")

# Topologia ratificada: 17 tools em 5 modulos.
EXPECTED_TOOLS = {
    # sendspeed_catalog
    "sendspeed_status", "sendspeed_module_map", "sendspeed_find_issue",
    "sendspeed_search", "sendspeed_gaps",
    # sendspeed_callbacks
    "crm_postback_contract", "crm_status_depara", "callback_pipeline_map",
    # sendspeed_journeys
    "journey_engine_map", "journey_trigger_contract",
    "journey_objective_attribution", "journey_catalog",
    # sendspeed_channels
    "channel_send_spec", "otp_flow_spec",
    # sendspeed_integrations
    "igaming_webhook_pattern", "webhook_security_spec", "crm_adapter_registry",
    # sendspeed_userin
    "userin_rbac_spec", "smartflow_dashboard_spec", "billing_reporting_spec",
}


def _require_linear_export():
    """Skip gracioso se o linear-export nao estiver disponivel (OneDrive sync etc.)."""
    if not os.path.isfile(LINEAR_INDEX):
        pytest.skip(f"linear-export indisponivel: {LINEAR_INDEX}")


def _load(path):
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


# ==============================================================================
# (a) Server importa e expoe as tools esperadas
# ==============================================================================

def test_server_imports_and_has_fastmcp_instance():
    assert sss.mcp is not None
    assert sss.mcp.name == "MECHA SendSpeed Domain"


def test_server_exposes_all_20_tools():
    tools = asyncio.run(sss.mcp.list_tools())
    names = {t.name for t in tools}
    assert names == EXPECTED_TOOLS, (
        f"faltando: {sorted(EXPECTED_TOOLS - names)} | "
        f"extras: {sorted(names - EXPECTED_TOOLS)}"
    )


def test_module_topology_tools_match_registered_tools():
    """Toda tool declarada em MODULES existe de fato registrada no FastMCP."""
    declared = {t for spec in sss.MODULES.values() for t in spec["tools"]}
    assert declared == EXPECTED_TOOLS


def test_tools_have_ptbr_docstrings():
    tools = asyncio.run(sss.mcp.list_tools())
    for t in tools:
        assert t.description and t.description.strip(), f"tool sem docstring: {t.name}"


# ==============================================================================
# (b) Busca de issues encontra SEND-488 e SEND-515
# ==============================================================================

@pytest.mark.parametrize("issue_id", ["SEND-488", "SEND-515"])
def test_find_issue_returns_meta_and_document(issue_id):
    _require_linear_export()
    result = sss.sendspeed_find_issue(issue_id)
    assert "error" not in result, result.get("error")
    meta = result["meta"]
    assert meta.get("id") == issue_id
    assert "error" not in meta, meta.get("error")
    assert meta.get("title"), f"{issue_id} sem titulo no index.json"
    doc = result["document"]
    assert "error" not in doc, doc.get("error")
    assert doc.get("chars", 0) > 0
    assert doc.get("content")


def test_find_issue_accepts_bare_number():
    _require_linear_export()
    result = sss.sendspeed_find_issue("488")
    assert result["meta"].get("id") == "SEND-488"


@pytest.mark.parametrize("issue_id", ["SEND-488", "SEND-515"])
def test_search_locates_issue_by_id(issue_id):
    _require_linear_export()
    result = sss.sendspeed_search(issue_id)
    assert "error" not in result, result.get("error")
    ids = {hit["id"] for hit in result["results"]}
    assert issue_id in ids


def test_search_respects_limit_and_status_filter():
    _require_linear_export()
    result = sss.sendspeed_search("a", limit=5)
    assert len(result["results"]) <= 5
    filtered = sss.sendspeed_search("callback", status_type="completed")
    assert "error" not in filtered
    for hit in filtered["results"]:
        assert hit.get("status_type") == "completed"


# ==============================================================================
# (c) JSONs de squad/workflows parseiam; agentes dos workflows existem no squad
# ==============================================================================

def test_squad_json_parses_and_has_expected_agents():
    if not os.path.isfile(SQUAD_FILE):
        pytest.skip(f"squad ainda nao criado: {SQUAD_FILE}")
    squad = _load(SQUAD_FILE)
    assert isinstance(squad, dict) and squad
    expected_agents = {"CatalogBot", "CallbackBot", "JourneyBot",
                       "ChannelBot", "IntegrationBot", "SmartFlowBot"}
    assert expected_agents <= set(squad.keys()), (
        f"agentes ausentes: {sorted(expected_agents - set(squad.keys()))}"
    )
    for name, cfg in squad.items():
        assert cfg.get("role"), f"{name} sem role"
        assert cfg.get("system_prompt"), f"{name} sem system_prompt"


def test_squad_tools_match_mcp_topology():
    """Campo aditivo 'tools' dos agentes so referencia tools reais do MCP."""
    if not os.path.isfile(SQUAD_FILE):
        pytest.skip(f"squad ainda nao criado: {SQUAD_FILE}")
    squad = _load(SQUAD_FILE)
    for name, cfg in squad.items():
        for tool in cfg.get("tools", []):
            assert tool in EXPECTED_TOOLS, (
                f"agente {name} referencia tool inexistente: {tool}"
            )


def test_workflows_json_parses_with_valid_steps():
    if not os.path.isfile(WORKFLOWS_FILE):
        pytest.skip(f"workflows ainda nao criados: {WORKFLOWS_FILE}")
    workflows = _load(WORKFLOWS_FILE)
    assert isinstance(workflows, dict) and workflows
    for wid, pipe in workflows.items():
        assert pipe.get("name"), f"{wid} sem name"
        assert pipe.get("description"), f"{wid} sem description"
        steps = pipe.get("steps")
        assert isinstance(steps, list) and steps, f"{wid} sem steps"
        outputs = set()
        for step in steps:
            assert step.get("step_id"), f"{wid}: step sem step_id"
            assert step.get("agent"), f"{wid}: step sem agent"
            assert step.get("output_var"), f"{wid}: step sem output_var"
            sources = step.get("input_sources") or (
                [step["input_source"]] if step.get("input_source") else []
            )
            assert sources, f"{wid} step {step['step_id']}: sem input_source(s)"
            for src in sources:
                assert src == "user_prompt" or src in outputs, (
                    f"{wid} step {step['step_id']}: input '{src}' nao produzido antes"
                )
            outputs.add(step["output_var"])


def test_workflow_agents_exist_in_squad():
    if not (os.path.isfile(WORKFLOWS_FILE) and os.path.isfile(SQUAD_FILE)):
        pytest.skip("squad/workflows sendspeed ainda nao criados")
    squad = _load(SQUAD_FILE)
    workflows = _load(WORKFLOWS_FILE)
    for wid, pipe in workflows.items():
        for step in pipe.get("steps", []):
            agent = step.get("agent")
            assert agent in squad, (
                f"workflow {wid} step {step.get('step_id')}: "
                f"agente '{agent}' nao existe em sendspeed_squad.json"
            )


def test_workflows_end_with_smartflowbot_validation():
    """Padrao qa_workflows: todo pipeline termina com validacao do SmartFlowBot."""
    if not os.path.isfile(WORKFLOWS_FILE):
        pytest.skip(f"workflows ainda nao criados: {WORKFLOWS_FILE}")
    workflows = _load(WORKFLOWS_FILE)
    for wid, pipe in workflows.items():
        last = pipe["steps"][-1]
        assert last.get("agent") == "SmartFlowBot", (
            f"{wid}: ultimo step deve ser SmartFlowBot, veio {last.get('agent')}"
        )


# ==============================================================================
# (d) mcp_config.json contem a entrada nova E a antiga
# ==============================================================================

def test_mcp_config_has_sendspeed_and_neo4j_entries():
    assert os.path.isfile(MCP_CONFIG), f"mcp_config.json nao encontrado: {MCP_CONFIG}"
    config = _load(MCP_CONFIG)
    servers = config.get("mcpServers", config)
    assert "sendspeed-mecha" in servers, "entrada sendspeed-mecha ausente"
    assert "neo4j-mecha" in servers, "entrada neo4j-mecha foi removida/renomeada"
    entry = servers["sendspeed-mecha"]
    assert entry.get("command"), "sendspeed-mecha sem command"
    args = " ".join(entry.get("args", []))
    assert "sendspeed_mcp_server.py" in args, (
        "args de sendspeed-mecha nao apontam para sendspeed_mcp_server.py"
    )


# ==============================================================================
# (e) Tools de dominio respondem sem excecao
# ==============================================================================

_NOARG_TOOLS = [
    "sendspeed_status", "sendspeed_module_map", "sendspeed_gaps",
    "crm_postback_contract", "crm_status_depara", "callback_pipeline_map",
    "journey_engine_map", "journey_trigger_contract",
    "journey_objective_attribution", "otp_flow_spec",
    "igaming_webhook_pattern", "webhook_security_spec", "crm_adapter_registry",
    "userin_rbac_spec", "smartflow_dashboard_spec", "billing_reporting_spec"
]


@pytest.mark.parametrize("tool_name", _NOARG_TOOLS)
def test_noarg_domain_tools_respond_without_error(tool_name):
    _require_linear_export()
    result = getattr(sss, tool_name)()
    assert isinstance(result, dict)
    assert "error" not in result, f"{tool_name} retornou erro: {result.get('error')}"


def test_sendspeed_status_reports_online():
    _require_linear_export()
    status = sss.sendspeed_status()
    assert status["status"] == "ONLINE"
    assert status["total_issues"] and status["total_issues"] > 0
    assert set(status["modules"]) == set(sss.MODULES.keys())


@pytest.mark.parametrize("channel", ["sms", "rcs", "whatsapp", "all"])
def test_channel_send_spec_valid_channels(channel):
    _require_linear_export()
    result = sss.channel_send_spec(channel)
    assert isinstance(result, dict)
    assert "error" not in result, result.get("error")
    assert result.get("documents"), f"canal {channel} sem documentos"
    assert "integration_stub" in result


def test_channel_send_spec_invalid_channel_graceful():
    result = sss.channel_send_spec("pombo-correio")
    assert "error" in result
    assert "all" in result.get("available", [])


def test_journey_catalog_lists_journeys():
    if not os.path.isfile(WORKFLOWS_FILE):
        pytest.skip(f"workflows ainda nao criados: {WORKFLOWS_FILE}")
    result = sss.journey_catalog()
    assert "error" not in result, result.get("error")
    assert result["count"] > 0
    for journey in result["journeys"]:
        assert journey["journey_id"]
        assert journey["agents"]


def test_journey_catalog_unknown_journey_graceful():
    if not os.path.isfile(WORKFLOWS_FILE):
        pytest.skip(f"workflows ainda nao criados: {WORKFLOWS_FILE}")
    result = sss.journey_catalog("journey_inexistente_xyz")
    assert "error" in result
    assert isinstance(result.get("available"), list) and result["available"]


def test_journey_catalog_specific_journey_resolves_agents():
    if not (os.path.isfile(WORKFLOWS_FILE) and os.path.isfile(SQUAD_FILE)):
        pytest.skip("squad/workflows sendspeed ainda nao criados")
    workflows = _load(WORKFLOWS_FILE)
    journey_id = sorted(workflows.keys())[0]
    result = sss.journey_catalog(journey_id)
    assert "error" not in result, result.get("error")
    assert result["definition"].get("steps")
    for name, agent in result["agents"].items():
        assert "error" not in agent, f"agente {name} nao resolvido no squad"
        assert agent.get("role") and agent.get("system_prompt")
