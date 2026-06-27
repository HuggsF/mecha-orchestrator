# ==============================================================================
# 🤖 MECHA MCP SERVER - IDE AI CONNECTOR
# ==============================================================================
# Exposes MECHA Squad Orchestration and Qdrant RAG tools directly to the IDE.
# Built with Model Context Protocol (FastMCP) Python SDK.
# ==============================================================================

import os
import sys
import asyncio
from typing import Dict, Any, List

# Add parent directories to path to ensure correct imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from mcp.server.fastmcp import FastMCP
from squad_orchestrator import SquadOrchestrator
from qdrant_client_helper import QdrantRAGClient

# Initialize FastMCP Server
mcp = FastMCP("MECHA Core Orchestrator")

# Initialize workspace root
WORKSPACE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Helper to run async functions synchronously inside tools
def run_async(coro):
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(coro)


@mcp.tool()
def get_qdrant_status() -> Dict[str, Any]:
    """Retorna o status de conexão da base vetorial RAG (Qdrant).
    Exibe a quantidade de pontos indexados, modo de conexão e tamanho do vetor.
    """
    try:
        client = QdrantRAGClient()
        # Fetching status requires checking collection details
        collections = client.client.get_collections().collections
        exists = any(c.name == "mecha_collection" for c in collections)
        count = 0
        if exists:
            count = client.client.get_collection("mecha_collection").points_count
        
        return {
            "status": "ONLINE",
            "collection": "mecha_collection",
            "total_points": count,
            "vector_size": client.vector_size,
            "mock_embeddings": os.environ.get("MECHA_FORCE_MOCK_EMBEDDINGS") == "1"
        }
    except Exception as e:
        return {
            "status": "OFFLINE",
            "error": str(e)
        }


@mcp.tool()
def search_rag(query: str, limit: int = 3) -> List[Dict[str, Any]]:
    """Realiza uma busca semântica na base RAG do MECHA.
    
    Args:
        query: O termo ou texto de busca semântica.
        limit: Quantidade máxima de resultados (padrão: 3).
    """
    try:
        client = QdrantRAGClient()
        return client.search(query, limit=limit)
    except Exception as e:
        return [{"error": str(e)}]


@mcp.tool()
def index_engram(text: str, topic: str = "general") -> str:
    """Insere um novo fragmento de conhecimento (engram) no RAG.
    
    Args:
        text: O conteúdo textual a ser indexado.
        topic: Tópico/categoria do metadado para indexação.
    """
    try:
        client = QdrantRAGClient()
        point_id = client.upsert(text, {"topic": topic})
        return f"[+] Sucesso! Engram indexado com ID: {point_id}"
    except Exception as e:
        return f"[-] Erro ao indexar engram: {e}"


@mcp.tool()
def run_squad_workflow(
    squad_name: str,
    workflow_name: str,
    pipeline_key: str,
    prompt: str
) -> Dict[str, Any]:
    """Executa um fluxo de trabalho (workflow) de agentes de forma concorrente em DAG.
    
    Args:
        squad_name: O nome da squad (ex: 'dev_squad', 'qa_squad', 'devops_squad', 'tribunal_squad').
        workflow_name: Nome do arquivo JSON de fluxos (ex: 'code_workflows', 'qa_workflows', 'devops_workflows', 'tribunal_workflows').
        pipeline_key: Chave identificadora do pipeline (ex: 'spec_driven_dev', 'qa_audit_pipeline', 'devops_deploy_pipeline', 'verdict_pipeline').
        prompt: O prompt de entrada ou código inicial para alimentar os agentes.
    """
    try:
        orchestrator = SquadOrchestrator(WORKSPACE_ROOT)
        
        # Determine the initial variable key based on the pipeline's expected inputs
        # DevSquad and DevOpsSquad expect 'user_prompt', QASquad expects 'source_code'
        if squad_name == "qa_squad":
            initial_inputs = {"source_code": prompt, "test_code": ""}
        else:
            initial_inputs = {"user_prompt": prompt}
            
        results = run_async(
            orchestrator.run_workflow(
                squad_name=squad_name,
                workflow_name=workflow_name,
                pipeline_key=pipeline_key,
                initial_inputs=initial_inputs
            )
        )
        # Filter out heavy system prompts and return clean output values
        return {k: v for k, v in results.items() if not k.startswith("_")}
    except Exception as e:
        return {"error": str(e)}


# =============================================================================
# BUS + BRIDGE MCP TOOLS (Ciclo 4 — GAP 6 & 7)
# =============================================================================

from agent_bus import AgentBus
from claw_squad_bridge import ClawSquadBridge

_bridge = None

def _get_bridge():
    global _bridge
    if _bridge is None:
        _bridge = ClawSquadBridge(WORKSPACE_ROOT)
    return _bridge


@mcp.tool()
def bus_list_agents(squad: str = None) -> List[Dict[str, Any]]:
    """Lista todos os agentes registrados no AgentBus.

    Args:
        squad: Filtra por squad (opcional). Ex: 'dev_squad', 'tribunal_squad', 'system'.
    """
    return _get_bridge().bus_list_agents(squad=squad)


@mcp.tool()
def bus_send_message(sender: str, recipient: str, payload_json: str) -> Dict[str, Any]:
    """Envia uma mensagem direta entre agentes via AgentBus.

    Args:
        sender: ID do agente remetente.
        recipient: ID do agente destinatario.
        payload_json: Payload em formato JSON string.
    """
    import json as _json
    try:
        payload = _json.loads(payload_json)
    except Exception:
        payload = {"raw": payload_json}
    return _get_bridge().bus_send_message(sender, recipient, payload)


@mcp.tool()
def bus_get_inbox(agent_id: str) -> List[Dict[str, Any]]:
    """Retorna mensagens pendentes na inbox de um agente.

    Args:
        agent_id: ID do agente (ex: 'claw', 'router', 'dev_squad.uncle_bob').
    """
    return _get_bridge().bus_get_inbox(agent_id)


@mcp.tool()
def bus_compliance_report() -> Dict[str, Any]:
    """Retorna o relatorio de compliance do Hermes Auditor.
    Inclui taxa de conformidade, violacoes e detalhamento por regra.
    """
    return _get_bridge().bus_compliance_report()


@mcp.tool()
def bus_stats() -> Dict[str, Any]:
    """Retorna estatisticas completas do sistema de comunicacao.
    Inclui bus, auditor, rotas e conversas ativas.
    """
    return _get_bridge().bus_stats()


@mcp.tool()
def claw_evaluate_action(action: str, context_json: str = "{}") -> Dict[str, Any]:
    """Avalia o risco de uma acao do Claw e consulta squad se necessario.

    Args:
        action: Tipo de acao (click, type, delete, install, execute, etc).
        context_json: Contexto da acao em JSON (target, command, etc).
    """
    import json as _json
    try:
        context = _json.loads(context_json)
    except Exception:
        context = {"raw": context_json}
    return run_async(_get_bridge().evaluate_action(action, context))


@mcp.tool()
def get_conversation(thread_id: str) -> List[Dict[str, Any]]:
    """Retorna o historico completo de uma conversa/thread.

    Args:
        thread_id: ID do thread de conversa.
    """
    return _get_bridge().get_conversation(thread_id)


@mcp.tool()
def search_conversations(query: str, limit: int = 10) -> List[Dict[str, Any]]:
    """Busca em todas as conversas persistidas por um termo.

    Args:
        query: Termo de busca.
        limit: Maximo de resultados (padrao: 10).
    """
    return _get_bridge().search_conversations(query, limit)


if __name__ == "__main__":
    # Start the stdin/stdout MCP server connection
    mcp.run()
