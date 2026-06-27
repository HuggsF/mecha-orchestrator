# ==============================================================================
# 🤖 AWESOME-BOTS MULTI-AGENT ORCHESTRATOR (REFACTORED)
# ==============================================================================
# System Architecture: Parallel Debate | Delegated to SquadOrchestrator
# Roles: Warlock (Hermes/Acusação), Amanda (Defesa), Shura 255 (Juiz)
# ==============================================================================

import os
import sys
import asyncio
from typing import Dict

# Enforce UTF-8 encoding output for Windows terminals (Bug CP1252 bypass)
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Import the unified orchestrator
from squad_orchestrator import SquadOrchestrator, Obsidian, Carmesim, Ouro, Roxo, Ciano, Reset

class AwesomeBotsOrchestrator:
    """Manages the parallel multi-agent debate (The Tribunal) using SquadOrchestrator."""
    def __init__(self, workspace_root: str):
        self.workspace_root = workspace_root
        self.orchestrator = SquadOrchestrator(workspace_root)
        self.tracker = self.orchestrator.tracker

        # Load local daemon to process Context7 (Chomsky Regex Grammar / 0x07)
        local_dir = os.path.dirname(os.path.abspath(__file__))
        if local_dir not in sys.path:
            sys.path.insert(0, local_dir)
            
        try:
            from antigravity import AntigravityDaemon
        except ImportError:
            from antigravity_sdk.antigravity import AntigravityDaemon
        
        self.daemon = AntigravityDaemon(chiplet_name="TRIBUNAL_INPUT_CLEANER")

    async def run_tribunal(self, topic: str) -> Dict[str, str]:
        """Runs the debate concurrently between Warlock and Amanda, then Shura judges."""
        print(f"\n{Obsidian}============================================================{Reset}")
        print(f"{Carmesim}      ⚖️ [ TRIBUNAL DOS AWESOME-BOTS - PROTOCOLO NIKA ] ⚖️{Reset}")
        print(f"{Obsidian}============================================================{Reset}")
        print(f"{Ouro}> TÓPICO EM JULGAMENTO: {topic}{Reset}\n")
        
        # 0. Context7 Chomsky Regex Grammar (0x07)
        clean_result = self.daemon.drop_bullshit(topic)
        collapsed_matrix = clean_result.get("matrix", [])
        
        if collapsed_matrix:
            sanitized_topic = clean_result.get("clean_text")
            print(f"{Ouro}> TÓPICO SANITIZADO (Context7):{Reset}\n{sanitized_topic}\n")
        else:
            print(f"{Carmesim}[X_DROP_SYNTAX]{Reset} Sem símbolos estruturados. Usando payload cru.")
            sanitized_topic = topic

        # Execute using dynamic orchestrator
        inputs = {"user_prompt": sanitized_topic}
        results = await self.orchestrator.run_workflow(
            squad_name="tribunal_squad",
            workflow_name="tribunal_workflows",
            pipeline_key="tribunal_pipeline",
            initial_inputs=inputs
        )
        
        return {
            "warlock": results.get("accusation", ""),
            "amanda": results.get("defense", ""),
            "shura": results.get("verdict", "")
        }

if __name__ == "__main__":
    # Test runner
    orchestrator = AwesomeBotsOrchestrator("c:\\Users\\huggs\\OneDrive\\Documentos\\workspace")
    test_topic = (
        "Olá, pessoal! Queria ver se a gente consegue aprovar esse setup do Kafka.\n"
        "#{2} {REATOR_KAFKA_SINCRONIZADO}\n"
        "- {Fator}:{Alta latência no barramento}\n"
        "- {Mitigação}:{Thread Ghost Workers}\n"
        "> {1}\n"
        "[x]\n"
        "Tenho certeza que isso vai resolver. Valeu!"
    )
    asyncio.run(orchestrator.run_tribunal(test_topic))
