# ==============================================================================
# 🤖 MECHA DEVSQUAD - SPEC-DRIVEN PIPELINE RUNNER (REFACTORED)
# ==============================================================================
# System Architecture: Spec-Driven Pipeline | Delegated to SquadOrchestrator
# Roles: Uncle Bob (Architect), Linus (Coder), Kent Beck (QA), Mitnick (Auditor)
# ==============================================================================

import os
import sys
import asyncio
import argparse
from typing import Dict

# Enforce UTF-8 encoding output for Windows terminals (Bug CP1252 bypass)
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Import the unified orchestrator
from squad_orchestrator import SquadOrchestrator, Verde, Carmesim, Reset

class CodeSquadRunner:
    """Wrapper that executes spec-driven pipelines using SquadOrchestrator."""
    def __init__(self, workspace_root: str):
        self.workspace_root = workspace_root
        self.orchestrator = SquadOrchestrator(workspace_root)
        self.tracker = self.orchestrator.tracker

    async def run_spec_driven_dev(self, user_prompt: str) -> Dict[str, str]:
        """Executes the spec-driven dev workflow via the dynamic DAG orchestrator."""
        inputs = {"user_prompt": user_prompt}
        results = await self.orchestrator.run_workflow(
            squad_name="dev_squad",
            workflow_name="code_workflows",
            pipeline_key="spec_driven_dev",
            initial_inputs=inputs
        )
        return {
            "specification": results.get("specification", ""),
            "implementation": results.get("implementation", ""),
            "tests": results.get("tests", ""),
            "audit_report": results.get("audit_report", "")
        }


if __name__ == "__main__":  # pragma: no cover
    parser = argparse.ArgumentParser(description="MECHA DevSquad Spec-Driven Execution Engine")
    parser.add_argument("--prompt", type=str, help="Prompt de entrada de código para iniciar a pipeline")
    parser.add_argument("--test-pipeline-spec", action="store_true", help="Roda o teste unitário de pipeline do DevSquad")
    args = parser.parse_args()
    
    workspace_root = "c:\\Users\\huggs\\OneDrive\\Documentos\\workspace"
    runner = CodeSquadRunner(workspace_root)
    
    if args.test_pipeline_spec:
        print("[*] Iniciando teste unitário de pipeline do DevSquad...")
        test_prompt = "Crie uma classe Calculator para realizar soma e subtração simples com verificação de tipo."
        results = asyncio.run(runner.run_spec_driven_dev(test_prompt))
        
        if "[APROVADO]" in results["audit_report"] and "class Calculator" in results["implementation"]:
            print(f"{Verde}[+] Teste de pipeline concluído com sucesso!{Reset}")
            sys.exit(0)
        else:
            print(f"{Carmesim}[!] Falha no teste de pipeline do DevSquad.{Reset}")
            sys.exit(1)
            
    elif args.prompt:
        asyncio.run(runner.run_spec_driven_dev(args.prompt))
    else:
        parser.print_help()
