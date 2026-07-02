# -*- coding: utf-8 -*-
# ==============================================================================
# SENDSPEED MCP SERVER - cerebro de dominio SendSpeed do MECHA (FastMCP / stdio)
# ==============================================================================
# Ratificado pelo debate O6: serve o conhecimento absorvido do linear-export
# (317 issues do time SEND) e a configuracao das journeys multi-agent
# (intelligence/squads/sendspeed_*.json). NAO chama os servicos antigos da
# SendSpeed (sms-api, api-legada, callback-sms) — onde uma tool dependeria de
# API externa, ela devolve o conhecimento estruturado + um campo
# "integration_stub" documentando a integracao futura.
#
# 5 modulos absorvidos: sendspeed_catalog, sendspeed_callbacks,
# sendspeed_journeys, sendspeed_channels, sendspeed_integrations.
# Leitura: read-only sobre arquivos locais (linear-export + squads). Escrita: nunca.
# ==============================================================================

from __future__ import annotations

import json
import os
from typing import Any, Dict, List, Optional

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("MECHA SendSpeed Domain")

MECHA_ROOT = os.environ.get(
    "MECHA_ROOT", r"C:\Users\huggs\OneDrive\Documentos\workspace\.mecha"
)
LINEAR_EXPORT = os.environ.get(
    "SENDSPEED_LINEAR_EXPORT", os.path.join(MECHA_ROOT, "CORE", "sendspeed", "linear-export")
)
SQUADS_DIR = os.environ.get(
    "SENDSPEED_SQUADS_DIR", os.path.join(MECHA_ROOT, "intelligence", "squads")
)
SQUAD_FILE = os.path.join(SQUADS_DIR, "sendspeed_squad.json")
WORKFLOWS_FILE = os.path.join(SQUADS_DIR, "sendspeed_workflows.json")

# Limite de caracteres por documento embutido — nao estourar contexto do cliente.
_DOC_MAX = 8000

# Topologia ratificada (debate O6): modulo -> tools expostas + issues-fonte.
MODULES: Dict[str, Dict[str, List[str]]] = {
    "sendspeed_catalog": {
        "tools": ["sendspeed_status", "sendspeed_module_map", "sendspeed_find_issue",
                  "sendspeed_search", "sendspeed_gaps"],
        "source_issues": ["SEND-488", "SEND-504", "SEND-511", "SEND-498", "SEND-475",
                          "SEND-471", "SEND-476", "SEND-487"],
    },
    "sendspeed_callbacks": {
        "tools": ["crm_postback_contract", "crm_status_depara", "callback_pipeline_map"],
        "source_issues": ["SEND-488", "SEND-490", "SEND-491", "SEND-492", "SEND-493",
                          "SEND-495", "SEND-496", "SEND-497", "SEND-498", "SEND-500",
                          "SEND-502", "SEND-483", "SEND-479"],
    },
    "sendspeed_journeys": {
        "tools": ["journey_engine_map", "journey_trigger_contract",
                  "journey_objective_attribution", "journey_catalog"],
        "source_issues": ["SEND-477", "SEND-478", "SEND-391", "SEND-450", "SEND-446",
                          "SEND-449", "SEND-479"],
    },
    "sendspeed_channels": {
        "tools": ["channel_send_spec", "otp_flow_spec"],
        "source_issues": ["SEND-505", "SEND-508", "SEND-429", "SEND-452", "SEND-446",
                          "SEND-478"],
    },
    "sendspeed_integrations": {
        "tools": ["igaming_webhook_pattern", "webhook_security_spec", "crm_adapter_registry"],
        "source_issues": ["SEND-510", "SEND-516", "SEND-515", "SEND-517", "SEND-506",
                          "SEND-499", "SEND-501", "SEND-503", "SEND-502"],
    },
    "sendspeed_userin": {
        "tools": ["userin_rbac_spec", "smartflow_dashboard_spec", "billing_reporting_spec"],
        "source_issues": ["SEND-367", "SEND-414", "SEND-354", "SEND-471", "SEND-475",
                          "SEND-476", "SEND-487", "SEND-512", "SEND-513", "SEND-514"],
    },
}

# ------------------------------------------------------------------------------
# Recursos lazy fail-safe (index.json pode estar em sync do OneDrive — tolerar).
# ------------------------------------------------------------------------------

_index_cache: Optional[Dict[str, Any]] = None


def _index() -> Dict[str, Any]:
    """Carrega linear-export/index.json (UTF-8) uma unica vez, indexado por id."""
    global _index_cache
    if _index_cache is None:
        path = os.path.join(LINEAR_EXPORT, "index.json")
        with open(path, "r", encoding="utf-8") as fh:
            raw = json.load(fh)
        _index_cache = {
            "generated_at": raw.get("generatedAt"),
            "total": raw.get("total"),
            "by_id": {i["id"]: i for i in raw.get("issues", [])},
        }
    return _index_cache


def _meta(issue_id: str) -> Dict[str, Any]:
    """Metadados enxutos de uma issue a partir do index (sem descricao longa)."""
    it = _index()["by_id"].get(issue_id)
    if not it:
        return {"id": issue_id, "error": "issue nao encontrada no index.json"}
    return {
        "id": it["id"],
        "title": it.get("title"),
        "status": it.get("status"),
        "status_type": it.get("statusType"),
        "priority": (it.get("priority") or {}).get("name"),
        "labels": it.get("labels") or [],
        "project": it.get("project"),
        "url": it.get("url"),
        "updated_at": it.get("updatedAt"),
    }


def _issue_md(issue_id: str, max_chars: int = _DOC_MAX) -> Dict[str, Any]:
    """Le linear-export/issues/<ID>.md em UTF-8, truncando para nao estourar contexto."""
    path = os.path.join(LINEAR_EXPORT, "issues", f"{issue_id}.md")
    if not os.path.isfile(path):
        return {"id": issue_id, "error": f"arquivo nao encontrado: {path}"}
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        text = fh.read()
    truncated = len(text) > max_chars
    return {
        "id": issue_id,
        "chars": len(text),
        "truncated": truncated,
        "content": text[:max_chars] + ("\n\n[... truncado ...]" if truncated else ""),
    }


def _bundle(topic: str, module: str, doc_ids: List[str],
            extra_ids: Optional[List[str]] = None) -> Dict[str, Any]:
    """Pacote padrao de conhecimento: docs completos + metadados das issues de apoio."""
    docs = [_issue_md(i) for i in doc_ids]
    related = [_meta(i) for i in (extra_ids or []) if i not in doc_ids]
    return {"topic": topic, "module": module, "documents": docs,
            "related_issues": related, "count": len(docs) + len(related)}


def _load_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


# ==============================================================================
# MODULO 1: sendspeed_catalog — mapa geral do conhecimento absorvido
# ==============================================================================

@mcp.tool()
def sendspeed_status() -> Dict[str, Any]:
    """Status do cerebro de dominio SendSpeed: total de issues absorvidas, contagens
    por status, modulos disponiveis e presenca dos arquivos de squad/workflow.
    Use PRIMEIRO para saber o que este MCP conhece antes de consultar as outras tools.
    Obs: e o status do CONHECIMENTO (linear-export), nao a saude dos servicos em
    producao — health-check das APIs SendSpeed e integracao futura (ver stub)."""
    try:
        ix = _index()
        by_status: Dict[str, int] = {}
        for it in ix["by_id"].values():
            key = it.get("statusType") or "unknown"
            by_status[key] = by_status.get(key, 0) + 1
        return {
            "status": "ONLINE",
            "linear_export": LINEAR_EXPORT,
            "generated_at": ix["generated_at"],
            "total_issues": ix["total"],
            "issues_by_status_type": by_status,
            "monitoring": {
                "started_issues": [_meta("SEND-515"), _meta("SEND-516"), _meta("SEND-517")],
                "note": "Apenas 3 issues em status Started. Mantenha os testes e implementacoes dessas ativas."
            },
            "modules": list(MODULES.keys()),
            "squad_file_present": os.path.isfile(SQUAD_FILE),
            "workflows_file_present": os.path.isfile(WORKFLOWS_FILE),
            "integration_stub": "FUTURO: health-check real das APIs SendSpeed "
                                "(api.sendspeed / status.sendspeed) via HTTP — "
                                "hoje os servicos antigos sao ignorados por decisao do debate O6.",
        }
    except Exception as exc:  # noqa: BLE001
        return {"status": "OFFLINE", "error": str(exc)}


@mcp.tool()
def sendspeed_module_map() -> Dict[str, Any]:
    """Mapa dos 5 modulos absorvidos do dominio SendSpeed com suas tools e
    issues-fonte (id + titulo + status). Use para descobrir qual tool serve
    cada assunto (callbacks CRM, journeys, canais, integracoes iGaming)."""
    try:
        out = {}
        for name, spec in MODULES.items():
            out[name] = {
                "tools": spec["tools"],
                "source_issues": [_meta(i) for i in spec["source_issues"]],
            }
        return {"count": len(out), "modules": out}
    except Exception as exc:  # noqa: BLE001
        return {"error": str(exc)}


@mcp.tool()
def sendspeed_find_issue(issue_id: str) -> Dict[str, Any]:
    """Retorna uma issue SEND completa: metadados do index + markdown integral
    do linear-export (issues/<ID>.md). Ex.: 'SEND-488', '488', 'send-483'.

    Args:
        issue_id: identificador da issue (aceita 'SEND-488', '488').
    """
    try:
        iid = issue_id.strip().upper()
        if not iid.startswith("SEND-"):
            iid = f"SEND-{iid.lstrip('SEND').lstrip('-') or issue_id.strip()}"
        return {"meta": _meta(iid), "document": _issue_md(iid, max_chars=20000)}
    except Exception as exc:  # noqa: BLE001
        return {"error": str(exc)}


@mcp.tool()
def sendspeed_search(query: str, limit: int = 20,
                     status_type: Optional[str] = None) -> Dict[str, Any]:
    """Busca issues SEND por texto (case-insensitive) em titulo, descricao e labels
    do index.json. Use para localizar conhecimento por assunto: 'crm_postback',
    'fasttrack', 'journey', 'OTP', 'NGX', 'RCS'.

    Args:
        query: termo de busca (substring, sem regex).
        limit: maximo de resultados (default 20).
        status_type: filtro opcional — 'completed', 'started', 'unstarted', 'backlog'.
    """
    try:
        q = query.strip().lower()
        hits: List[Dict[str, Any]] = []
        for it in _index()["by_id"].values():
            if status_type and (it.get("statusType") or "") != status_type:
                continue
            hay = " ".join([
                it.get("title") or "",
                it.get("description") or "",
                " ".join(it.get("labels") or []),
                it["id"],
            ]).lower()
            if q in hay:
                hits.append(_meta(it["id"]))
        return {"query": query, "count": len(hits), "results": hits[:limit]}
    except Exception as exc:  # noqa: BLE001
        return {"error": str(exc)}


@mcp.tool()
def sendspeed_gaps() -> Dict[str, Any]:
    """Lacunas de execucao por modulo: issues-fonte da topologia que AINDA NAO
    foram concluidas (statusType != completed), agrupadas por modulo absorvido.
    Use para priorizar trabalho pendente do dominio SendSpeed (ex.: contrato
    FastTrack aguardando documentacao, de-para de status nao padronizado).

    Consolidacoes conhecidas (S3):
      - SEND-449 e subconjunto quase total do escopo RCS de SEND-446 —
        consolidar antes de implementar (nao duplicar esforco)."""
    try:
        gaps: Dict[str, List[Dict[str, Any]]] = {}
        total = 0
        for name, spec in MODULES.items():
            pending = [_meta(i) for i in spec["source_issues"]
                       if _meta(i).get("status_type") not in ("completed", "canceled")]
            if pending:
                gaps[name] = pending
                total += len(pending)
        return {
            "total_gaps": total,
            "gaps_by_module": gaps,
            "consolidations": [
                {
                    "note": "SEND-449 subconjunto de SEND-446",
                    "detail": "SEND-449 (Encurtamento automático de links nos botões de RCS) cobre "
                              "quase totalmente o escopo RCS de SEND-446 (encurtador SMS+RCS+atribuição). "
                              "Consolidar em SEND-446 antes de implementar — não duplicar builders.",
                    "action": "Fechar SEND-449 como subconjunto; toda implementação vai em SEND-446.",
                    "status": "pending_consolidation",
                },
                {
                    "note": "Riscos SLA/Performance em Billing (SEND-512, 513, 514)",
                    "detail": "Relatórios de 30 dias com total cobrado (joins pesados). "
                              "O export não define SLA ou tempo de resposta esperado.",
                    "action": "Acordar SLA com a equipe de produto; provável necessidade de materialização.",
                    "status": "pending_sla_definition",
                }
            ],
            "external_blockers": [
                {
                    "issue": "SEND-504",
                    "reason": "Aguardando documentacao FastTrack — ajustar payload, auth e campos",
                    "impact": "Bloqueia tools crm_adapter_registry, webhook_security_spec, crm_postback_contract"
                },
                {
                    "issue": "SEND-438",
                    "reason": "MongoDB DEV read-only — user govtech sem permissão de escrita",
                    "impact": "Bloqueia fluxos de inserção de dados de infra"
                },
                {
                    "issue": "SEND-509",
                    "reason": "Fazendinha Automatizada de Qualidade de Rota (Bloqueio de infra / setup de terceiros)",
                    "impact": "Bloqueia validacoes fim-a-fim do pipeline NGX"
                }
            ]
        }
    except Exception as exc:  # noqa: BLE001
        return {"error": str(exc)}


# ==============================================================================
# MODULO 2: sendspeed_callbacks — contrato multi-CRM de postback/status
# ==============================================================================

@mcp.tool()
def crm_postback_contract() -> Dict[str, Any]:
    """Contrato oficial `crm_postback` multi-CRM (Smartico legado + FastTrack):
    estrutura JSON salva em sms.crm_postback, campo `crm`, tipos CrmPostback e
    SmsSentInfo. Fontes: SEND-488 (historia macro FastTrack) e SEND-498 (tipos).
    Use antes de tocar qualquer builder/consumer de callback."""
    try:
        m = MODULES["sendspeed_callbacks"]
        bundle = _bundle("Contrato crm_postback multi-CRM", "sendspeed_callbacks",
                         ["SEND-488", "SEND-498", "SEND-490"], m["source_issues"])
        bundle["status"] = "blocked"
        bundle["blocked_by"] = "pending_fasttrack_doc"
        return bundle
    except Exception as exc:  # noqa: BLE001
        return {"error": str(exc)}


@mcp.tool()
def crm_status_depara() -> Dict[str, Any]:
    """De-para de status de callback por cliente/CRM: padronizacao dos status de
    entrega (incluindo o status 'Pendente' em mensageria). Fontes: SEND-483
    (padronizacao e de-para por cliente) e SEND-479 (status Pendente).
    Use ao mapear status internos SendSpeed -> status esperados pelo CRM destino."""
    try:
        m = MODULES["sendspeed_callbacks"]
        return _bundle("De-para de status de callback por CRM/cliente",
                       "sendspeed_callbacks", ["SEND-483", "SEND-479"],
                       m["source_issues"])
    except Exception as exc:  # noqa: BLE001
        return {"error": str(exc)}


@mcp.tool()
def callback_pipeline_map() -> Dict[str, Any]:
    """Mapa do pipeline de callbacks SendSpeed -> CRM: quais servicos/componentes
    participam (sms-api, api-legada, callback-sms) e o que cada issue tecnica
    muda em cada um (parsing centralizado, roteamento por CRM, workers).
    Use para entender a arquitetura ponta-a-ponta antes de propor mudancas."""
    try:
        pipeline = {
            "sms-api": {
                "papel": "recebe envio, monta crm_postback nos DTOs/builders, "
                         "consumers RCS/SMS fazem forwardCrmPostback",
                "issues": [_meta(i) for i in
                           ["SEND-490", "SEND-491", "SEND-492", "SEND-493"]],
            },
            "api-legada": {
                "papel": "fluxo legado: HandleApi/ValidationService/SmsService + "
                         "SmsConsumer com roteamento Smartico/Fasttrack",
                "issues": [_meta(i) for i in ["SEND-495", "SEND-496"]],
            },
            "callback-sms": {
                "papel": "workers de callback: parsing unico do crm_postback, "
                         "CallbackGrouper/BatchProcessor por CRM, decisao worker "
                         "compartilhado vs dedicado",
                "issues": [_meta(i) for i in
                           ["SEND-497", "SEND-498", "SEND-500", "SEND-502"]],
            },
        }
        return {"topic": "Pipeline de callbacks multi-CRM", "pipeline": pipeline,
                "architecture_decision": _issue_md("SEND-502")}
    except Exception as exc:  # noqa: BLE001
        return {"error": str(exc)}


# ==============================================================================
# MODULO 3: sendspeed_journeys — engine de jornadas + journeys multi-agent MECHA
# ==============================================================================

@mcp.tool()
def journey_engine_map() -> Dict[str, Any]:
    """Mapa do engine de jornadas SendSpeed: SendSmsExecutor com API real no
    journey backend (SEND-391), acionamento de journey com array de entrada
    (SEND-477), status 'Pendente' em mensageria (SEND-479) e envio de lista
    fria via API com arquivo (SEND-478).

    Enriquecido em S3 com:
    - Contrato POST /journey/trigger com array de entries e batchId
    - Invariante de status: Enviado = Falha + Rejeitado + Pendente
    - Rastreabilidade: journeyId / executionId / nodeId / batchId / trace_id

    Use para entender como o backend de jornadas dispara envios em lote
    e como o pipeline DLR registra o status Pendente."""
    try:
        m = MODULES["sendspeed_journeys"]
        bundle = _bundle("Engine de jornadas SendSpeed", "sendspeed_journeys",
                         ["SEND-391", "SEND-477", "SEND-479"], m["source_issues"])
        bundle["batch_trigger_contract"] = {
            "endpoint": "POST /journey/trigger",
            "payload": {
                "journey_id": "string",
                "entries": [{"phone": "+55...", "attrs": {}}],
            },
            "batch_id": "compartilhado por todos os items da chamada",
            "execution_model": "cada item → execucao independente com trace_id proprio",
            "tracing_fields": ["journeyId", "executionId", "nodeId", "batchId", "trace_id"],
        }
        bundle["pending_status"] = {
            "description": "Novo status intermediario 'Pendente' entre Enviado e Entregue (SEND-479)",
            "invariant": "Enviado = Falha + Rejeitado + Pendente",
            "impact_lead_time": "Pendente NAO entra no calculo de latencia de entrega",
            "impact_dlr": "crm_postback propaga Pendente via campo status no de-para por CRM",
        }
        bundle["cold_list_upload"] = {
            "description": "Envio de lista fria via API com arquivo (SEND-478)",
            "format": "CSV ou JSON",
            "progress": "consultavel por batchId",
            "status": _meta("SEND-478").get("status_type"),
        }
        return bundle
    except Exception as exc:  # noqa: BLE001
        return {"error": str(exc)}


@mcp.tool()
def journey_trigger_contract() -> Dict[str, Any]:
    """Contrato de acionamento (trigger) de jornadas: acionar journey com array
    de entrada via API (SEND-477) e envio de lista fria via API com arquivo
    (SEND-478). Use ao integrar sistemas externos que disparam jornadas."""
    try:
        m = MODULES["sendspeed_journeys"]
        return _bundle("Contrato de trigger de jornadas", "sendspeed_journeys",
                       ["SEND-477", "SEND-478"], m["source_issues"])
    except Exception as exc:  # noqa: BLE001
        return {"error": str(exc)}


@mcp.tool()
def journey_objective_attribution() -> Dict[str, Any]:
    """Objetivos funcionais e atribuicao de jornadas: metas que validam o
    desempenho de uma jornada (SEND-450) e metrificacao de cliques via
    encurtador de links em SMS e RCS (SEND-446, SEND-449).

    Enriquecido em S3 com:
    - Janela de atribuicao: 24h last touch (SEND-450)
    - Campos de rastreabilidade no ShortLink/ClickEvent
    - Consolidacao: SEND-449 e subconjunto quase total de SEND-446 —
      toda implementacao do encurtador RCS vai em SEND-446
    - Taxa de Entrega = entregue / (disparado - rejeitados)
    - Metricas de clique: totais vs unicos por botao (campanha RCS)

    Use ao definir como medir sucesso/conversao de uma journey e ao
    integrar o encurtador de links no Journey Builder."""
    try:
        m = MODULES["sendspeed_journeys"]
        bundle = _bundle("Objetivos e atribuicao de jornadas", "sendspeed_journeys",
                         ["SEND-450", "SEND-446", "SEND-449"], m["source_issues"])
        bundle["attribution_model"] = {
            "window": "24h last touch",
            "tracking_fields": ["journeyId", "executionId", "nodeId",
                                 "channel", "userId", "metadata"],
            "click_event_fields": ["cardIndex", "buttonText", "shortLinkId"],
            "metrics": {
                "taxa_entrega": "entregue / (disparado - rejeitados)",
                "cliques_totais": "por botao em toda a campanha",
                "cliques_unicos": "por botao por usuario",
                "conversoes": "configuradas como meta da jornada (SEND-450)",
            },
        }
        bundle["shortener_consolidation"] = {
            "note": "SEND-449 subconjunto de SEND-446",
            "rule": "Toda implementacao do encurtador (SMS + RCS + botoes de carrossel) "
                    "vai em SEND-446. SEND-449 pode ser fechada como duplicata.",
            "functions": {
                "shortenUrlsInMessage": "encurtamento no momento do envio (SMS e RCS)",
                "shortenRcsButtonUrls": "encurtamento nos botoes de carrossel RCS",
            },
            "invariant": "URL original preservada no editor — nao re-encurtar link "
                         "ja curto da plataforma",
            "status": "pending_consolidation",
        }
        bundle["rcs_templates"] = {
            "source": "SEND-429 + SEND-452",
            "features": [
                "selecao de template com busca + filtros + navegacao para edicao",
                "template obrigatorio para salvar o no no Journey Builder",
                "preview fiel no editor com suporte a emojis (SEND-452)",
            ],
        }
        return bundle
    except Exception as exc:  # noqa: BLE001
        return {"error": str(exc)}


@mcp.tool()
def journey_catalog(journey_id: Optional[str] = None) -> Dict[str, Any]:
    """Catalogo das journeys MULTI-AGENT do squad SendSpeed no MECHA, lidas de
    intelligence/squads/sendspeed_workflows.json + sendspeed_squad.json.
    Sem argumento: lista todas as pipelines com steps e agentes. Com journey_id
    (ex.: 'sendspeed_callback_pipeline'): retorna a definicao completa dos steps
    e o role/system_prompt de cada agente envolvido.

    Args:
        journey_id: id snake_case da pipeline no workflows.json (opcional).
    """
    try:
        if not os.path.isfile(WORKFLOWS_FILE):
            return {"error": f"arquivo de workflows ainda nao criado: {WORKFLOWS_FILE}. "
                             "As journeys multi-agent SendSpeed serao definidas em "
                             "intelligence/squads/sendspeed_workflows.json."}
        workflows = _load_json(WORKFLOWS_FILE)
        squad: Dict[str, Any] = {}
        squad_error = None
        if os.path.isfile(SQUAD_FILE):
            squad = _load_json(SQUAD_FILE)
        else:
            squad_error = f"arquivo de squad ainda nao criado: {SQUAD_FILE}"

        if journey_id is None:
            listing = []
            for pid, pipe in workflows.items():
                steps = pipe.get("steps", [])
                listing.append({
                    "journey_id": pid,
                    "name": pipe.get("name"),
                    "description": pipe.get("description"),
                    "steps": len(steps),
                    "agents": sorted({s.get("agent") for s in steps if s.get("agent")}),
                })
            return {"count": len(listing), "journeys": listing,
                    "squad_agents": sorted(squad.keys()),
                    "squad_error": squad_error}

        pipe = workflows.get(journey_id)
        if pipe is None:
            return {"error": f"journey '{journey_id}' nao encontrada",
                    "available": sorted(workflows.keys())}
        agents = {}
        for step in pipe.get("steps", []):
            name = step.get("agent")
            if name and name not in agents:
                agents[name] = squad.get(name) or {
                    "error": f"agente '{name}' nao encontrado em sendspeed_squad.json"
                }
        return {"journey_id": journey_id, "definition": pipe, "agents": agents,
                "squad_error": squad_error}
    except Exception as exc:  # noqa: BLE001
        return {"error": str(exc)}


# ==============================================================================
# MODULO 4: sendspeed_channels — especificacao de envio por canal + OTP
# ==============================================================================

@mcp.tool()
def channel_send_spec(channel: str = "all") -> Dict[str, Any]:
    """Especificacao de envio por canal (sms | rcs | whatsapp | all): templates
    RCS em jornadas com busca/filtros (SEND-429), preview fiel do RCS + emojis
    (SEND-452), encurtador de links (SEND-446) e lista fria via API (SEND-478).
    Envio REAL pelos gateways e integracao futura — esta tool serve a spec.

    Args:
        channel: 'sms', 'rcs', 'whatsapp' ou 'all' (default).
    """
    try:
        by_channel = {
            "rcs": ["SEND-429", "SEND-452", "SEND-449"],
            "sms": ["SEND-446", "SEND-478"],
            "whatsapp": ["SEND-505", "SEND-508"],
        }
        ch = channel.strip().lower()
        if ch == "all":
            ids: List[str] = []
            for lst in by_channel.values():
                ids.extend(i for i in lst if i not in ids)
        elif ch in by_channel:
            ids = by_channel[ch]
        else:
            return {"error": f"canal desconhecido: '{channel}'",
                    "available": sorted(by_channel.keys()) + ["all"]}
        bundle = _bundle(f"Spec de envio — canal {ch}", "sendspeed_channels",
                         ids[:3], ids)
        bundle["integration_stub"] = (
            "FUTURO: disparo real de mensagens via API SendSpeed "
            "(POST /sms, /rcs, gateway WhatsApp Infobip). Os servicos antigos "
            "sao ignorados nesta fase — tool serve apenas conhecimento."
        )
        return bundle
    except Exception as exc:  # noqa: BLE001
        return {"error": str(exc)}


@mcp.tool()
def otp_flow_spec() -> Dict[str, Any]:
    """Especificacao do fluxo OTP via WhatsApp (Infobip): SEND-505 (implementacao)
    e SEND-508 (integracao). Use ao desenhar autenticacao por OTP nos canais
    SendSpeed. Geracao/validacao real de OTP e integracao futura (ver stub)."""
    try:
        m = MODULES["sendspeed_channels"]
        bundle = _bundle("Fluxo OTP WhatsApp (Infobip)", "sendspeed_channels",
                         ["SEND-505", "SEND-508"], m["source_issues"])
        bundle["integration_stub"] = (
            "FUTURO: emissao/validacao de OTP via API Infobip WhatsApp — "
            "requer credenciais em .env (nunca hardcoded) e endpoint SendSpeed."
        )
        return bundle
    except Exception as exc:  # noqa: BLE001
        return {"error": str(exc)}


# ==============================================================================
# MODULO 5: sendspeed_integrations — iGaming (NGX/UserIn) + adapters de CRM
# ==============================================================================

@mcp.tool()
def igaming_webhook_pattern() -> Dict[str, Any]:
    """Spec consolidada do adaptador generico iGaming (NGX + FastTrack): 16 eventos
    NGX (SEND-510), ingestao na UserIn (SEND-516), recuperacao de cadastro Apostou
    (SEND-515), gatilhos de UI front NGX (SEND-517), mapeamento NGX (SEND-506).

    Spec do adaptador generico recomendado em SEND-510 (S5):
    - HMAC-SHA256 com X-Auth-Signature Base64, secret por cliente/ambiente
    - Idempotencia via external_id — reentrega nao duplica
    - DLQ com retry exponencial: 1min / 5min / 15min
    - Gatekeepers obrigatorios: consentimento, KYC, blocklist pos USER_DELETE, is_test

    Issues SEND-515/516/517 estao em status 'started' — monitorar progresso."""
    try:
        m = MODULES["sendspeed_integrations"]
        bundle = _bundle("Spec iGaming NGX + FastTrack (adaptador generico)",
                         "sendspeed_integrations",
                         ["SEND-510", "SEND-516", "SEND-506"], m["source_issues"])
        bundle["generic_adapter_spec"] = {
            "auth": {
                "header": "X-Auth-Signature",
                "algorithm": "HMAC-SHA256",
                "encoding": "Base64",
                "secret_scope": "por cliente e ambiente — nunca hardcoded",
                "on_failure": "401 sem persistencia do evento",
            },
            "idempotency": {
                "field": "external_id",
                "rule": "reentrega com mesmo external_id e ignorada silenciosamente",
            },
            "dlq": {
                "retries": [1, 5, 15],
                "unit": "minutos",
                "on_exhaustion": "dead-letter com alerta para ops",
            },
            "gatekeepers": [
                "user_accepted_notifications = true (consentimento LGPD)",
                "KYC verificado antes de qualquer jornada",
                "blocklist: bloquear apos USER_DELETE",
                "is_test = true => fora de producao",
            ],
            "events_ngx": 16,
            "source_issue": "SEND-510",
        }
        bundle["started_issues_monitor"] = {
            "note": "Apenas 3 issues em status 'started' no workspace — monitorar",
            "issues": [_meta(i) for i in ["SEND-515", "SEND-516", "SEND-517"]],
        }
        bundle["fasttrack_side"] = {
            "status": "blocked",
            "blocked_by": ["SEND-504"],
            "pending_fasttrack_doc": True,
            "note": "Auth/payload/retry FastTrack aguardam documentacao oficial. "
                    "TODO(fasttrack-doc) em todos os pontos de integracao.",
        }
        return bundle
    except Exception as exc:  # noqa: BLE001
        return {"error": str(exc)}


@mcp.tool()
def webhook_security_spec() -> Dict[str, Any]:
    """Requisitos de seguranca para webhooks de integracao (NGX/UserIn e CRMs).

    Status: PARCIALMENTE BLOQUEADO — lado FastTrack aguarda SEND-504.
    Lado NGX: spec confirmada (HMAC-SHA256, allowlist de IPs, secret por cliente).

    pending_fasttrack_doc = True ate a documentacao oficial cair.
    Nunca servir o contrato FastTrack como fato — sempre como 'blocked'."""
    try:
        m = MODULES["sendspeed_integrations"]
        bundle = _bundle("Seguranca de webhooks (auth, payload, assinatura)",
                         "sendspeed_integrations",
                         ["SEND-504", "SEND-510"], m["source_issues"])
        bundle["ngx_side"] = {
            "status": "confirmed",
            "auth_header": "X-Auth-Signature: Base64(HMAC-SHA256(body, secret))",
            "secret_rotation": "por cliente, por ambiente (.env, nunca hardcoded)",
            "allowlist": "IPs NGX por ambiente (a configurar por cliente)",
            "on_invalid_sig": "HTTP 401 — sem persistencia, sem retry",
        }
        bundle["fasttrack_side"] = {
            "status": "blocked",
            "blocked_by": ["SEND-504"],
            "pending_fasttrack_doc": True,
            "known_fields": ["callback_url", "api_key"],
            "unknown_fields": ["auth_header_format", "payload_schema", "retry_policy"],
            "note": "TODO(fasttrack-doc) — substituir este bloco quando a doc chegar",
        }
        bundle["integration_stub"] = (
            "FUTURO: validacao real de assinatura/HMAC e allowlist de IPs nos "
            "endpoints de webhook — depende da documentacao FastTrack (SEND-504). "
            "Segredos via .env, nunca no codigo."
        )
        return bundle
    except Exception as exc:  # noqa: BLE001
        return {"error": str(exc)}


@mcp.tool()
def crm_adapter_registry() -> Dict[str, Any]:
    """Registro dos adapters de CRM do pipeline de callbacks: Smartico (legado,
    em producao) e FastTrack (em construcao — FastTrackClient SEND-499,
    SonaMessageProcessor SEND-501, CrmPayloadBuilder SEND-503, decisao de worker
    SEND-502). Use para saber quais CRMs existem e o estado de cada adapter."""
    try:
        registry = {
            "smartico": {
                "state": "producao (legado)",
                "notes": "callback_url + crm_message_id + api_key no crm_postback; "
                         "SmarticoPayloadBuilder atual",
                "issues": [_meta("SEND-503")],
            },
            "fasttrack": {
                "state": "em construcao",
                "notes": "FastTrackClient HTTP, roteamento no fallback por phone, "
                         "payload/auth aguardando documentacao oficial",
                "issues": [_meta(i) for i in
                           ["SEND-499", "SEND-501", "SEND-503", "SEND-502", "SEND-504"]],
            },
        }
        return {"topic": "Registro de adapters de CRM", "count": len(registry),
                "adapters": registry,
                "status": "blocked",
                "blocked_by": "pending_fasttrack_doc",
                "contract_reference": "use crm_postback_contract para o contrato multi-CRM"}
    except Exception as exc:  # noqa: BLE001
        return {"error": str(exc)}


# ==============================================================================
# MODULO 6: sendspeed_userin — Plataforma, Dashboards e Billing
# ==============================================================================

@mcp.tool()
def userin_rbac_spec() -> Dict[str, Any]:
    """Especificacao do controle de acesso (RBAC) e segmentacao na plataforma UserIn:
    EPIC Equipe & Permissoes (SEND-367) com 10 user stories (backlog), operadores
    numericos para regras de Atributo de Perfil (SEND-414) e bug Primeiros Passos
    (SEND-354). Multi-tenancy user/company/visitor.

    Use ao projetar autorizacao, convites, API Keys, SSO ou segmentacao avancada
    na UserIn. Proveniencia: linear-export curado em CORE/sendspeed/userin_platform.md."""
    try:
        m = MODULES["sendspeed_userin"]
        bundle = _bundle("Plataforma UserIn: RBAC e Segmentacao", "sendspeed_userin",
                         ["SEND-367", "SEND-414", "SEND-354"], m["source_issues"])
        bundle["source"] = "linear-export + CORE/sendspeed/userin_platform.md"
        bundle["rbac_user_stories"] = [
            {"id": 1, "story": "Criar usuario com perfil e papel",     "status": "backlog"},
            {"id": 2, "story": "Convidar membro para empresa",         "status": "backlog"},
            {"id": 3, "story": "Listar membros da empresa",            "status": "backlog"},
            {"id": 4, "story": "Editar papel de membro",               "status": "backlog"},
            {"id": 5, "story": "Remover membro",                       "status": "backlog"},
            {"id": 6, "story": "Transferir ownership",                 "status": "backlog"},
            {"id": 7, "story": "Permissoes granulares por modulo",     "status": "backlog"},
            {"id": 8, "story": "API Key por empresa",                  "status": "backlog"},
            {"id": 9, "story": "SSO / OAuth2",                        "status": "backlog"},
            {"id": 10,"story": "Logs de auditoria de acesso",          "status": "backlog"},
        ]
        bundle["multitenancy_model"] = {
            "entities": ["Company (tenant)", "User (member)", "Visitor (anonimo)"],
            "isolation": "company_id em todas as queries — sem crossleak entre tenants",
            "roles": ["admin", "operator", "viewer"],
        }
        bundle["numeric_operators"] = {
            "source": "SEND-414",
            "operators": [">", ">=", "<", "<=", "between"],
            "example": "saldo_wallet >= 100 AND num_depositos >= 3",
            "status": _meta("SEND-414").get("status_type"),
        }
        bundle["bug_primeiros_passos"] = {
            "source": "SEND-354",
            "description": "Criar componentes na tela Primeiros Passos nao marca o passo como concluido",
            "status": _meta("SEND-354").get("status_type"),
        }
        return bundle
    except Exception as exc:  # noqa: BLE001
        return {"error": str(exc)}

@mcp.tool()
def smartflow_dashboard_spec() -> Dict[str, Any]:
    """Especificacao dos dashboards da SmartFlow: Dashboard Geral (SEND-471),
    feat/smartflow-profile (SEND-475), Upgrade Fase 2 (SEND-476) e alerta de
    saldo SS Control (SEND-487).

    ATENCAO — inconsistencias de export:
    - SEND-471, SEND-475 e SEND-476 constam como 'backlog' no export mas foram
      relatadas como arquivadas/canceladas em ciclos anteriores. Cada item carrega
      flag 'export_inconsistency: true' — servido como incognita, nao como fato.
    - SEND-487 esta em 'unstarted' (To-do) sem inconsistencia.

    Use para entender o estado dos dashboards antes de qualquer planejamento."""
    try:
        m = MODULES["sendspeed_userin"]
        bundle = _bundle("Dashboards SmartFlow", "sendspeed_userin",
                         ["SEND-471", "SEND-476", "SEND-487"], m["source_issues"])
        bundle["source"] = "linear-export + CORE/sendspeed/userin_platform.md"
        bundle["issues_detail"] = [
            {
                "id": "SEND-471",
                "title": _meta("SEND-471").get("title"),
                "status_type": _meta("SEND-471").get("status_type"),
                "export_inconsistency": True,
                "inconsistency_note": "Backlog no export, possivelmente arquivada. Confirmar com produto antes de implementar.",
            },
            {
                "id": "SEND-475",
                "title": _meta("SEND-475").get("title"),
                "status_type": _meta("SEND-475").get("status_type"),
                "export_inconsistency": True,
                "inconsistency_note": "Issue vazia no export — sem descricao nem criterios de aceite. Refinar ou fechar.",
            },
            {
                "id": "SEND-476",
                "title": _meta("SEND-476").get("title"),
                "status_type": _meta("SEND-476").get("status_type"),
                "export_inconsistency": True,
                "inconsistency_note": "Backlog no export, possivelmente arquivada. Extensao do SEND-471 — alinhar status primeiro.",
            },
            {
                "id": "SEND-487",
                "title": _meta("SEND-487").get("title"),
                "status_type": _meta("SEND-487").get("status_type"),
                "export_inconsistency": False,
                "inconsistency_note": None,
            },
        ]
        return bundle
    except Exception as exc:  # noqa: BLE001
        return {"error": str(exc)}

@mcp.tool()
def billing_reporting_spec() -> Dict[str, Any]:
    """Especificacao de billing e relatorios financeiros: propagar valor cobrado
    por mensagem (SEND-512), total cobrado no relatorio (SEND-513) e ampliar
    filtro de periodo para ate 30 dias (SEND-514).

    Riscos de performance registrados (SLA a definir com produto):
    - JOIN pesado mensagens x planos x clientes sem indice composto
    - SUM total_cobrado em 30 dias com alto volume
    - Sem SLA de resposta definido no export (sugestao: < 5s/7d, < 30s/30d)

    Use ao projetar queries de relatorio ou cache de agregacao."""
    try:
        m = MODULES["sendspeed_userin"]
        bundle = _bundle("Billing e Relatorios", "sendspeed_userin",
                         ["SEND-512", "SEND-513", "SEND-514"], m["source_issues"])
        bundle["source"] = "linear-export + CORE/sendspeed/userin_platform.md"
        bundle["performance_risks"] = [
            {
                "risk": "JOIN pesado (mensagens x planos x clientes) sem indice composto",
                "impact": "Timeout em janela de 30 dias",
                "recommendation": "Materializar view diaria OU indice composto (client_id, sent_at, crm)",
                "sla": "a_definir",
            },
            {
                "risk": "SUM total_cobrado em 30 dias com volume alto",
                "impact": "Lentidao visivel no frontend",
                "recommendation": "Pre-agregacao em job noturno OU cache Redis TTL 1h",
                "sla": "a_definir",
            },
            {
                "risk": "SLA de resposta do relatorio nao definido",
                "impact": "Sem criterio de aceite mensuravel",
                "recommendation": "Acordar com produto — sugestao: < 5s para 7 dias, < 30s para 30 dias",
                "sla": "a_definir",
            },
        ]
        bundle["issues_status"] = {
            i: _meta(i).get("status_type") for i in ["SEND-512", "SEND-513", "SEND-514"]
        }
        return bundle
    except Exception as exc:  # noqa: BLE001
        return {"error": str(exc)}


if __name__ == "__main__":
    # Transport stdio (padrao FastMCP) — plugavel em Antigravity/Claude via mcp_config.
    mcp.run()
