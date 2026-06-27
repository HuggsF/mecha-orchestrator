# ==============================================================================
# 🤖 MECHA DEVOPS_SQUAD - DEPLOY & INFRASTRUCTURE PIPELINE RUNNER
# ==============================================================================
# System Architecture: DevOps Pipeline | Delegated to SquadOrchestrator
# Roles: TerraformBot (IaC), KubernetesBot (Orchestration), GitLabCI (CI/CD), SRE_Bot (Ops)
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

class DevOpsSquadRunner:
    """Wrapper that executes DevOps deployment pipelines using SquadOrchestrator."""
    def __init__(self, workspace_root: str):
        self.workspace_root = workspace_root
        self.orchestrator = SquadOrchestrator(workspace_root)
        self.tracker = self.orchestrator.tracker

    async def run_devops_deploy(self, user_prompt: str) -> Dict[str, str]:
        """Executes the DevOps pipeline via the dynamic DAG orchestrator."""
        inputs = {"user_prompt": user_prompt}
        results = await self.orchestrator.run_workflow(
            squad_name="devops_squad",
            workflow_name="devops_workflows",
            pipeline_key="devops_deploy_pipeline",
            initial_inputs=inputs
        )
        return {
            "infra_plan": results.get("infra_plan", ""),
            "k8s_manifests": results.get("k8s_manifests", ""),
            "ci_pipeline": results.get("ci_pipeline", ""),
            "sre_report": results.get("sre_report", "")
        }


if __name__ == "__main__":  # pragma: no cover
    parser = argparse.ArgumentParser(description="MECHA DevOpsSquad Pipeline Runner")
    parser.add_argument("--prompt", type=str, help="Prompt de infraestrutura para provisionar e implantar")
    parser.add_argument("--test-pipeline-devops", action="store_true", help="Executa um teste simulado da pipeline do DevOpsSquad")
    args = parser.parse_args()
    
    workspace_root = "c:\\Users\\huggs\\OneDrive\\Documentos\\workspace"
    runner = DevOpsSquadRunner(workspace_root)
    
    if args.test_pipeline_devops:
        print("[*] Iniciando teste unitário de pipeline do DevOpsSquad...")
        test_prompt = "Provisione um cluster EKS na AWS para rodar a aplicação mecha-app."
        results = asyncio.run(runner.run_devops_deploy(test_prompt))
        if "[SRE_REPORT_OK]" in results["sre_report"] and "[INFRA_PLAN_OK]" in results["infra_plan"]:
            print(f"{Verde}[+] Teste de pipeline do DevOpsSquad concluído com sucesso!{Reset}")
            sys.exit(0)
        else:
            print(f"{Carmesim}[!] Falha no teste de pipeline do DevOpsSquad.{Reset}")
            sys.exit(1)
            
    elif args.prompt:
        asyncio.run(runner.run_devops_deploy(args.prompt))
    else:
        parser.print_help()
