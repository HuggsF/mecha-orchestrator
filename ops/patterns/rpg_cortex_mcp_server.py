# -*- coding: utf-8 -*-
# ==============================================================================
# RPG CORTEX MCP SERVER — cerebro de dominio rpg_cortex (FastMCP / stdio)
# ==============================================================================
# Serve o conhecimento arquitetural do modulo rpg_cortex: hardware automation
# local (PyAutoGUI, Jitbit, macros .mcr/.jmb), contratos de integracao e gaps
# do checklist plug-and-play.
#
# O modulo fisico (src/extracted/rpg_cortex/) foi extraido e e dependencia
# opcional — este MCP serve apenas o CONHECIMENTO curado, nao executa
# automacoes. Zero chamadas a PyAutoGUI, Jitbit ou subprocess.
#
# 4 tools em 1 modulo: rpg_cortex_status, rpg_cortex_hardware_spec,
#                      rpg_cortex_integration_contract, rpg_cortex_gaps
# ==============================================================================

from __future__ import annotations

import os
from typing import Any, Dict, List

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("MECHA RPG Cortex Domain")

# ---------------------------------------------------------------------------
# Conhecimento curado (inline — nao depende de linear-export nem filesystem)
# ---------------------------------------------------------------------------

_STATUS = {
    "status": "EXTRACTED",
    "description": (
        "Modulo rpg_cortex extraido para src/extracted/rpg_cortex/ e registrado "
        "como dependencia opcional. Nao executa em producao — consumidores usam "
        "import dinamico com fallback gracioso."
    ),
    "physical_path": "src/extracted/rpg_cortex/",
    "consumers": [
        "src/neural_link/telemetry/jitbit_connector.py",
        "src/agents/computer_use_agent.py",
    ],
    "integration_mode": "opcional (import dinamico + fallback)",
    "execution": "nenhuma — este MCP serve apenas o conhecimento da spec",
}

_HARDWARE_SPEC = {
    "module": "rpg_cortex",
    "submodule": "hardware",
    "components": {
        "JitbitWrapper": {
            "file": "hardware/jitbit_wrapper.py",
            "purpose": "Execucao de macros .mcr/.jmb via Jitbit Macro Recorder",
            "dependencies": ["Jitbit Macro Recorder instalado em C:/Program Files/Jitbit/"],
            "di_pattern": "lazy init — instanciado apenas quando jitbit_path valido",
        },
        "MacroExecutor": {
            "file": "hardware/macro_executor.py",
            "purpose": "Orquestrador de execucao de macros: fila, retry, timeout",
            "di_pattern": "parâmetro opcional jitbit_wrapper=None",
        },
        "CartographerRPG": {
            "file": "hardware/cartographer.py",
            "purpose": "Mapeamento de tela e coordenadas para automacao visual",
            "di_pattern": "import dinamico de PyAutoGUI",
        },
        "EmergencyStop": {
            "file": "hardware/emergency.py",
            "purpose": "Para todas as automacoes via _emergency_stop global",
            "state": "estado global (_emergency_stop: bool)",
        },
        "RpgControls": {
            "file": "hardware/rpg_controls.py",
            "purpose": "Controles de teclado/mouse para automacao de RPG",
        },
        "SmoothMovement": {
            "file": "hardware/smooth_movement.py",
            "purpose": "Movimentos suaves de mouse com interpolacao",
        },
    },
    "knowledge": {
        "MacroKnowledgeBase": {
            "file": "knowledge/macro_knowledge_base.py",
            "purpose": "Base de conhecimento de macros: lookup por nome/categoria",
        },
        "macros_map": "knowledge/macros_map.yaml — mapa macro_id -> arquivo .mcr",
        "mapa_interface": "knowledge/mapa_interface.json — coordenadas de UI mapeadas",
        "rpg_skills": "knowledge/rpg_skills.txt — lista de skills mapeadas",
    },
    "graph_nodes": {
        "ExternalSync": {
            "relation": "(ExternalSync)-[:TRIGGERED]->(Task)",
            "writer": "TelemetryProvider (nao o JitbitConnector)",
            "note": "JitbitConnector de macros NAO escreve no grafo Neo4j",
        }
    },
}

_INTEGRATION_CONTRACT = {
    "topic": "Contratos de integracao rpg_cortex com consumidores",
    "consumers": {
        "jitbit_connector": {
            "file": "src/neural_link/telemetry/jitbit_connector.py",
            "import_pattern": "import dinamico com fallback",
            "code_pattern": (
                "def _resolve_jitbit_wrapper():\n"
                "    try:\n"
                "        from src.extracted.rpg_cortex.hardware.jitbit_wrapper import JitbitWrapper\n"
                "        return JitbitWrapper\n"
                "    except ImportError:\n"
                "        return None\n"
                "# ...\n"
                "\"JitbitWrapper nao disponivel. Instale rpg_cortex ou passe jitbit_wrapper.\""
            ),
            "behavior_without_rpg_cortex": {
                "execute_macro_sync": "FALHA — ImportError se JitbitWrapper indisponivel",
                "run_macro": "OK (subprocess ou Virtual Driver)",
                "telemetria": "OK",
            },
        },
        "computer_use_agent": {
            "file": "src/agents/computer_use_agent.py",
            "dependency": "TEMP_DIR = PROJECT_ROOT / 'src' / 'extracted' / 'rpg_cortex' / 'temp'",
            "behavior_without_rpg_cortex": (
                "OK — TEMP_DIR.mkdir(exist_ok=True) cria a pasta se nao existir"
            ),
            "configurability": "TEMP_DIR configuravel via env COMPUTER_USE_TEMP (checklist aberto)",
        },
    },
    "graph_independence": (
        "KPI Intelligence e RPG Cortex sao independentes no grafo Neo4j. "
        "KPI usa ModelMetric/ToolReview/RequestMetric/DailyAggregate. "
        "RPG usa ExternalSync -[:TRIGGERED]-> Task. Nenhuma aresta entre os dois."
    ),
    "docker": {
        "dockerfile": "COPY src/extracted/rpg_cortex/ /app/rpg_cortex/",
        "compose_volume": "../src/extracted/rpg_cortex:/app/rpg_cortex",
        "note": "Referenciado em infra/ — restaurar a partir do zip se necessario",
    },
}

_GAPS = [
    {
        "id": "rpg-gap-1",
        "title": "execute_macro_sync: fallback para subprocess quando JitbitWrapper indisponivel",
        "status": "open",
        "priority": "P1",
        "detail": (
            "Hoje execute_macro_sync falha com ImportError quando rpg_cortex nao esta instalado. "
            "Implementar fallback via subprocess para o executavel Jitbit diretamente."
        ),
    },
    {
        "id": "rpg-gap-2",
        "title": "TEMP_DIR configuravel via env COMPUTER_USE_TEMP",
        "status": "open",
        "priority": "P1",
        "detail": (
            "computer_use_agent.py hardcoda TEMP_DIR como subpasta de src/extracted/rpg_cortex/. "
            "Expor como variavel de ambiente COMPUTER_USE_TEMP para desacoplar do modulo."
        ),
    },
    {
        "id": "rpg-gap-3",
        "title": "rpg_cortex como dependencia opcional em requirements.txt",
        "status": "open",
        "priority": "P2",
        "detail": (
            "Marcar rpg_cortex (PyAutoGUI, pywin32) como extras_require opcionais "
            "para nao quebrar ambientes sem GUI (CI/CD headless, Docker sem display)."
        ),
    },
    {
        "id": "rpg-gap-4",
        "title": "Thread safety nas chamadas PyAutoGUI em rpg_cortex",
        "status": "open",
        "priority": "P2",
        "detail": (
            "audit/SUMMARY.md identifica: 'Add thread safety to pyautogui calls in rpg_cortex'. "
            "Chamadas concorrentes a PyAutoGUI sem lock podem causar race conditions na UI."
        ),
    },
]


# ==============================================================================
# TOOLS
# ==============================================================================

@mcp.tool()
def rpg_cortex_status() -> Dict[str, Any]:
    """Status do modulo rpg_cortex: estado de extracao, consumidores, modo de
    integracao e nota de execucao.
    Use PRIMEIRO para entender o estado do modulo antes de consultar as outras tools.
    Este MCP serve apenas o CONHECIMENTO — nao executa automacoes."""
    return dict(_STATUS)


@mcp.tool()
def rpg_cortex_hardware_spec() -> Dict[str, Any]:
    """Spec do submodulo hardware do rpg_cortex: JitbitWrapper, MacroExecutor,
    CartographerRPG, EmergencyStop, RpgControls, SmoothMovement e a base de
    conhecimento de macros (MacroKnowledgeBase, macros_map, mapa_interface).

    Inclui padroes de DI (lazy init, parametros opcionais, import dinamico,
    estado global _emergency_stop) e os nos Neo4j gerados (ExternalSync)."""
    return dict(_HARDWARE_SPEC)


@mcp.tool()
def rpg_cortex_integration_contract() -> Dict[str, Any]:
    """Contratos de integracao rpg_cortex com os consumidores:
    - jitbit_connector.py: import dinamico com fallback gracioso (ImportError)
    - computer_use_agent.py: TEMP_DIR como subpasta do modulo

    Inclui comportamento sem rpg_cortex instalado, independencia no grafo Neo4j
    (KPI e RPG nao compartilham arestas) e snapshots Docker."""
    return dict(_INTEGRATION_CONTRACT)


@mcp.tool()
def rpg_cortex_gaps() -> Dict[str, Any]:
    """Gaps abertos do checklist plug-and-play rpg_cortex:
    4 itens identificados na auditoria (fallback subprocess, TEMP_DIR via env,
    dependencia opcional, thread safety PyAutoGUI).

    Use para priorizar o trabalho de desacoplamento do modulo."""
    open_gaps = [g for g in _GAPS if g["status"] == "open"]
    return {
        "total_gaps": len(open_gaps),
        "gaps": open_gaps,
        "source": "EXTRACTION_RPG.md + REFERENCIAS_REMOVIDAS.md (CORE do .mecha)",
    }


if __name__ == "__main__":
    mcp.run()
