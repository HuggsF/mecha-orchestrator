# ==============================================================================
# 🤖 MECHA QASQUAD - QUALITY ASSURANCE PIPELINE RUNNER (REFACTORED)
# ==============================================================================
# System Architecture: QA Audit Pipeline | Delegated to SquadOrchestrator
# Roles: SonarBot (Lints), Martin Fowler (Design), LocustBot (Perf), Kent Beck (QA Lead)
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

class QASquadRunner:
    """Wrapper that executes QA audit pipelines using SquadOrchestrator."""
    def __init__(self, workspace_root: str):
        self.workspace_root = workspace_root
        self.orchestrator = SquadOrchestrator(workspace_root)
        self.tracker = self.orchestrator.tracker

    async def run_qa_audit(self, source_code: str, test_code: str = "") -> Dict[str, str]:
        """Executes the QA audit pipeline via the dynamic DAG orchestrator."""
        inputs = {
            "source_code": source_code,
            "test_code": test_code if test_code else "Nenhum código de teste fornecido."
        }
        results = await self.orchestrator.run_workflow(
            squad_name="qa_squad",
            workflow_name="qa_workflows",
            pipeline_key="qa_audit_pipeline",
            initial_inputs=inputs
        )
        return {
            "lint_report": results.get("lint_report", ""),
            "design_report": results.get("design_report", ""),
            "perf_report": results.get("perf_report", ""),
            "qa_final_report": results.get("qa_final_report", "")
        }


if __name__ == "__main__":  # pragma: no cover
    parser = argparse.ArgumentParser(description="MECHA QASquad Pipeline Runner")
    parser.add_argument("--source", type=str, help="Caminho do arquivo de código fonte para analisar")
    parser.add_argument("--tests", type=str, help="Caminho opcional do arquivo de testes unitários")
    parser.add_argument("--test-pipeline-qa", action="store_true", help="Executa um teste simulado da pipeline do QASquad")
    args = parser.parse_args()
    
    workspace_root = "c:\\Users\\huggs\\OneDrive\\Documentos\\workspace"
    runner = QASquadRunner(workspace_root)
    
    if args.test_pipeline_qa:
        print("[*] Iniciando teste unitário de pipeline do QASquad...")
        test_source = "def add(a, b):\n    sys.path.append('.') # redundant\n    return a + b"
        results = asyncio.run(runner.run_qa_audit(test_source))
        if "[APROVADO]" in results["qa_final_report"]:
            print(f"{Verde}[+] Teste de pipeline do QASquad concluído com sucesso!{Reset}")
            sys.exit(0)
        else:
            print(f"{Carmesim}[!] Falha no teste de pipeline do QASquad.{Reset}")
            sys.exit(1)
            
    elif args.source:
        if not os.path.exists(args.source):
            print(f"{Carmesim}[!] Arquivo de código fonte '{args.source}' não encontrado.{Reset}")
            sys.exit(1)
            
        with open(args.source, "r", encoding="utf-8") as f:
            source_content = f.read()
            
        test_content = ""
        if args.tests:
            if os.path.exists(args.tests):
                with open(args.tests, "r", encoding="utf-8") as ft:
                    test_content = ft.read()
            else:
                print(f"{Carmesim}[!] Arquivo de testes '{args.tests}' não encontrado. Rodando auditoria apenas com o código de produção.{Reset}")
                
        asyncio.run(runner.run_qa_audit(source_content, test_content))
    else:
        parser.print_help()
