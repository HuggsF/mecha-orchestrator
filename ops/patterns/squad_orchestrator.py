# ==============================================================================
# 🤖 MECHA SQUAD ORCHESTRATOR - DAG-BASED MULTI-AGENT ENGINE
# ==============================================================================
# System Architecture: DAG Execution | OpenRouter Gateway | FinOps Cost Tracking
# Supported Squads: DevSquad, QASquad, Hermes Tribunal
# ==============================================================================

import os
import sys
import json
import time
import requests
import asyncio
from typing import Dict, Any, List, Optional, Set

# Enforce UTF-8 encoding output for Windows terminals (Bug CP1252 bypass)
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# ANSI colors matching the Soul palettes of Anubis
Obsidian = "\033[38;5;234m"
Ouro = "\033[38;5;220m"
Carmesim = "\033[38;5;197m"
Ciano = "\033[38;5;39m"
Roxo = "\033[38;5;99m"
Verde = "\033[38;5;40m"
Reset = "\033[0m"

# OpenRouter Models config
MODEL_CODER = "qwen/qwen-2.5-coder-32b-instruct"
MODEL_DEFAULT = "meta-llama/llama-3.3-70b-instruct"

# Pricing rates per 1M tokens (in USD)
PRICING = {
    MODEL_CODER: {"input": 0.07, "output": 0.16},
    MODEL_DEFAULT: {"input": 0.59, "output": 0.79}
}

class CostTracker:
    """Tracks token consumption and dollar costs for FinOps compliance."""
    def __init__(self, db_path: str, budget_limit: float = 20.0):
        self.db_path = db_path
        self.budget_limit = budget_limit
        self.current_spend = self._load_spend()

    def _load_spend(self) -> float:
        if os.path.exists(self.db_path):
            try:
                with open(self.db_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return data.get("current_spend", 0.0)
            except Exception:
                pass
        return 0.0

    def _save_spend(self):
        data = {}
        if os.path.exists(self.db_path):
            try:
                with open(self.db_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception:
                pass
        data["current_spend"] = self.current_spend
        try:
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            with open(self.db_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"{Carmesim}[!] Erro ao salvar telemetria financeira: {e}{Reset}")

    def estimate_tokens(self, text: str) -> int:
        return max(1, len(text) // 4)

    def register_call(self, model: str, prompt: str, response: str) -> float:
        input_tokens = self.estimate_tokens(prompt)
        output_tokens = self.estimate_tokens(response)
        rates = PRICING.get(model, {"input": 0.59, "output": 0.79})
        cost = ((input_tokens * rates["input"]) + (output_tokens * rates["output"])) / 1_000_000.0
        self.current_spend += cost
        self._save_spend()
        return cost


class SquadOrchestrator:
    """DAG-based Orchestration Engine for any Squad and Workflow config."""
    def __init__(self, workspace_root: str):
        self.workspace_root = workspace_root
        self.db_path = os.path.join(workspace_root, ".mecha", "ops", "config_db.json")
        self.tracker = CostTracker(self.db_path)
        self.api_key = self._load_api_key()

    def _load_api_key(self) -> str:
        key = os.getenv("OPENROUTER_API_KEY")
        if key:
            return key
        ops_env = os.path.join(self.workspace_root, ".mecha", "ops", ".env")
        if os.path.exists(ops_env):
            try:
                with open(ops_env, "r", encoding="utf-8") as f:
                    for line in f:
                        if line.startswith("OPENROUTER_API_KEY="):
                            return line.strip().split("=", 1)[1]
            except Exception:
                pass
        return "MOCK_KEY"

    def load_squad_config(self, squad_name: str) -> Dict[str, Any]:
        path = os.path.join(self.workspace_root, ".mecha", "intelligence", "squads", f"{squad_name}.json")
        return self._load_json(path)

    def load_workflow_config(self, workflow_name: str) -> Dict[str, Any]:
        path = os.path.join(self.workspace_root, ".mecha", "intelligence", "squads", f"{workflow_name}.json")
        return self._load_json(path)

    def _load_json(self, path: str) -> dict:
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"{Carmesim}[!] Erro ao carregar {path}: {e}{Reset}")
        return {}

    def _get_mock_response(self, agent_name: str, topic_context: str) -> str:
        # Mock responses matching all original runners
        agent_upper = agent_name.upper()
        if "BOB" in agent_upper:
            return (
                f"# SPECIFICATION: {topic_context}\n\n"
                "## 1. Arquitetura\n"
                "O componente deve ser um script Python independente.\n\n"
                "## 2. API Pública / Assinaturas\n"
                "* `class Calculator`:\n"
                "  * `def add(a: float, b: float) -> float`: Retorna a soma de a e b.\n"
                "  * `def subtract(a: float, b: float) -> float`: Retorna a diferença de a e b.\n\n"
                "## 3. Restrições e Casos de Borda\n"
                "* Entradas devem ser numéricas (float ou int). Se não forem, deve levantar `TypeError`."
            )
        elif "LINUS" in agent_upper:
            return (
                "```python\n"
                "class Calculator:\n"
                "    def add(self, a: float, b: float) -> float:\n"
                "        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):\n"
                "            raise TypeError(\"Inputs must be numeric\")\n"
                "        return float(a + b)\n\n"
                "    def subtract(self, a: float, b: float) -> float:\n"
                "        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):\n"
                "            raise TypeError(\"Inputs must be numeric\")\n"
                "        return float(a - b)\n"
                "```"
            )
        elif "SONAR" in agent_upper:
            return (
                "### Relatório SonarBot - Lints & Estilo\n"
                "- Nenhuma infração grave do PEP8 encontrada.\n"
                "- Importação redundante de `sys` removível na linha 4.\n"
                "- Sugestão: Adicionar anotações de tipo de forma mais abrangente."
            )
        elif "FOWLER" in agent_upper:
            return (
                "### Relatório Martin Fowler - Design & Code Smells\n"
                "- O design está limpo, porém a classe possui acoplamento temporal.\n"
                "- Sugestão: Separar a lógica de escrita em arquivo de forma assíncrona.\n"
                "- SOLID: Excelente aplicação do princípio de responsabilidade única."
            )
        elif "LOCUST" in agent_upper:
            return (
                "### Relatório LocustBot - Otimização & Performance\n"
                "- Complexidade de tempo nos loops principais é O(1) devido ao uso de hashmap.\n"
                "- Sugestão: Adicionar pool de conexões SQLite para evitar concorrência no arquivo local."
            )
        elif "BECK" in agent_upper:
            # Check if this is code runner (tests author) or QA lead
            if "QA Lead" in topic_context or "PARECER" in topic_context or "REPORT" in topic_context or "lint_report" in topic_context:
                return (
                    "### Relatório Final Kent Beck - Testes & Cobertura\n"
                    "1. **Cobertura**: 100% do código de produção possui testes correspondentes.\n"
                    "2. **Lacunas**: Nenhuma lacuna crítica de cobertura encontrada.\n"
                    "3. **Decisão**: Cobertura de testes e conformidade impecáveis.\n\n"
                    "[APROVADO]"
                )
            else:
                return (
                    "```python\n"
                    "import pytest\n"
                    "from implementation import Calculator\n\n"
                    "def test_calculator_add():\n"
                    "    calc = Calculator()\n"
                    "    assert calc.add(2, 3) == 5.0\n"
                    "    assert calc.add(-1, 1) == 0.0\n\n"
                    "def test_calculator_subtract():\n"
                    "    calc = Calculator()\n"
                    "    assert calc.subtract(5, 3) == 2.0\n\n"
                    "def test_calculator_type_error():\n"
                    "    calc = Calculator()\n"
                    "    with pytest.raises(TypeError):\n"
                    "        calc.add(\"2\", 3)\n"
                    "```"
                )
        elif "MITNICK" in agent_upper:
            return (
                "### Relatório de Auditoria e Segurança - DevSquad\n"
                "1. **Conformidade Funcional**: A implementação do Linus atende perfeitamente a especificação de interface de assinaturas de `Calculator` do Uncle Bob.\n"
                "2. **Segurança**: Higienização correta de tipos via `isinstance` para evitar race-conditions ou tipos incompatíveis.\n"
                "3. **Qualidade dos Testes**: O Kent Beck cobriu os caminhos normais e o caso de borda do erro de tipo.\n\n"
                "[APROVADO]"
            )
        elif "WARLOCK" in agent_upper:
            return (
                "[WARLOCK (KNOT) - ACUSAÇÃO]\n"
                "Essa premissa de configuração está cheia de furos, mano. Thread Ghost Workers? Papo furado, tlg.\n"
                "Isso viola o princípio de determinismo do Ring 0 e abre brecha para injeção de race-condition no Tartarus!\n"
                "O Velvet Room não aprova essa latência. Recomendo abortar [0] imediatamente."
            )
        elif "AMANDA" in agent_upper:
            return (
                "[AMANDA (SHADOW PROCESSOR) - DEFESA]\n"
                "Discordo do Warlock. O padrão proposto higieniza perfeitamente os dados no SQLite Cold Storage.\n"
                "As threads Ghost Workers mitigam a latência sob alta concorrência e o Terminal Akasha sincroniza as chaves com Irminsul.\n"
                "Segurança garantida via hashes de integridade em config_db.json. Procede [1]."
            )
        elif "SHURA" in agent_upper:
            return (
                "[SHURA 255 (THE ARCHITECT) - VEREDITO]\n"
                "Aprecio os argumentos do SECURITY_AUDITOR (Warlock) e da COMPLIANCE_REVIEWER (Amanda).\n"
                "A defesa provou que os Ghost Workers possuem integridade de memória via SQLite, neutralizando os furos lógicos.\n"
                "VEREDITO: Aprovado. [1]\n"
                "Asura Strike concluído. Ring 0 operacional."
            )
        elif "TERRAFORM" in agent_upper:
            return (
                "```hcl\n"
                "resource \"aws_eks_cluster\" \"mecha_cluster\" {\n"
                "  name     = \"mecha-production-cluster\"\n"
                "  role_arn = aws_iam_role.eks_role.arn\n"
                "  vpc_config {\n"
                "    subnet_ids = [aws_subnet.pub_a.id, aws_subnet.pub_b.id]\n"
                "  }\n"
                "}\n"
                "```\n"
                "[INFRA_PLAN_OK]"
            )
        elif "KUBERNETES" in agent_upper:
            return (
                "```yaml\n"
                "apiVersion: apps/v1\n"
                "kind: Deployment\n"
                "metadata:\n"
                "  name: mecha-deployment\n"
                "spec:\n"
                "  replicas: 3\n"
                "  template:\n"
                "    spec:\n"
                "      containers:\n"
                "      - name: mecha-app\n"
                "        image: mecha-app:latest\n"
                "```\n"
                "[K8S_MANIFESTS_OK]"
            )
        elif "GITLAB" in agent_upper:
            return (
                "```yaml\n"
                "stages:\n"
                "  - build\n"
                "  - deploy\n"
                "deploy_job:\n"
                "  stage: deploy\n"
                "  script:\n"
                "    - kubectl apply -f k8s/\n"
                "```\n"
                "[CI_PIPELINE_OK]"
            )
        elif "SRE" in agent_upper:
            return (
                "### Relatório SRE - Observabilidade & SLOs\n"
                "1. **Métricas**: Configurado scrapers para `mecha-app` na porta 8080.\n"
                "2. **SLI**: Latência do endpoint `/api` < 200ms.\n"
                "3. **Decisão**: Monitoramento integrado via Prometheus/Loki.\n\n"
                "[SRE_REPORT_OK]"
            )
        else:
            return f"[MOCK] Resposta simulada para o agente {agent_name} sobre o tema: {topic_context[:50]}"

    def _is_mock_mode(self) -> bool:
        """True when LLM calls are mocked (no API key or forced via MECHA_FORCE_MOCK_LLM=1)."""
        return self.api_key == "MOCK_KEY" or not self.api_key or os.getenv("MECHA_FORCE_MOCK_LLM") == "1"

    async def _call_openrouter(self, model: str, system_prompt: str, user_content: str, agent_name: str, topic_context: str) -> str:
        if self._is_mock_mode():
            await asyncio.sleep(0.5)
            return self._get_mock_response(agent_name, user_content)

        if self.tracker.current_spend >= self.tracker.budget_limit:
            return f"[LIMIT EXCEEDED]: Orçamento de FinOps excedido (${self.tracker.current_spend:.4f} USD)."

        def make_request():
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://github.com/google/antigravity",
                "X-Title": f"MECHA SDK {agent_name}"
            }
            payload = {
                "model": model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_content}
                ],
                "temperature": 0.2,
                "max_tokens": 1500
            }
            return requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload, timeout=45)

        try:
            loop = asyncio.get_running_loop()
            response = await loop.run_in_executor(None, make_request)
            response.raise_for_status()
            res_content = response.json()['choices'][0]['message']['content']
            cost = self.tracker.register_call(model, system_prompt + user_content, res_content)
            print(f"{Obsidian}[AAA FINANCIALS] Call {model} ({agent_name}) Cost: ${cost:.6f} USD | Total: ${self.tracker.current_spend:.4f} USD{Reset}")
            return res_content
        except Exception as e:
            print(f"{Carmesim}[!] Falha na conexão OpenRouter ({e}). Usando mock fallback para {agent_name}.{Reset}")
            return self._get_mock_response(agent_name, user_content)

    async def run_workflow(self, squad_name: str, workflow_name: str, pipeline_key: str, initial_inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Loads the configs and executes the pipeline dynamically resolving DAG dependencies."""
        personas = self.load_squad_config(squad_name)
        workflow_data = self.load_workflow_config(workflow_name)
        
        pipeline = workflow_data.get(pipeline_key)
        if not pipeline:
            raise ValueError(f"Pipeline '{pipeline_key}' não encontrado no workflow '{workflow_name}'.")

        # ── Validação Let It Fail: entry_inputs (S3) ───────────────────────────
        # Coleta todos os inputs exigidos pelo step 1 (ou steps sem dependências
        # externas além de user_prompt). Se algum input esperado estiver ausente
        # em initial_inputs, falha explicitamente — sem adivinhar por nome de squad.
        first_step_deps: List[str] = []
        for step in pipeline.get("steps", []):
            # Coleta deps deste step
            deps = []
            if step.get("input_source"):
                deps.append(step["input_source"])
            if step.get("input_sources"):
                deps.extend(step["input_sources"])
            # Step raiz: deps que não são output de nenhum step anterior
            step_output_vars = {s.get("output_var") for s in pipeline.get("steps", [])}
            root_deps = [d for d in deps if d not in step_output_vars]
            first_step_deps.extend(root_deps)
        
        missing = [dep for dep in first_step_deps if dep not in initial_inputs]
        if missing:
            raise RuntimeError(
                f"[Let It Fail] Pipeline '{pipeline_key}' exige inputs {missing} "
                f"que não foram fornecidos. Recebidos: {list(initial_inputs.keys())}. "
                f"Declare entry_inputs no metadata do pipeline ou ajuste o chamador."
            )

        print(f"\n{Obsidian}============================================================{Reset}")
        print(f"{Roxo}      📡 [ MECHA DELEGATOR - SQUAD: {squad_name.upper()} ] 📡{Reset}")
        print(f"{Obsidian}============================================================{Reset}")
        print(f"{Ciano}> Executando: {pipeline.get('name')}...{Reset}\n")

        # Variables environment for outputs
        env = {**initial_inputs}
        steps = pipeline.get("steps", [])
        
        # Sort steps by dependency or execute iteratively
        executed_steps: Set[int] = set()
        
        while len(executed_steps) < len(steps):
            # Find all steps that are ready to run in parallel
            ready_steps = []
            for step in steps:
                step_id = step.get("step_id")
                if step_id in executed_steps:
                    continue
                
                # Check dependencies
                deps = []
                if step.get("input_source"):
                    deps.append(step.get("input_source"))
                if step.get("input_sources"):
                    deps.extend(step.get("input_sources"))
                
                # Step is ready if all its dependencies are present in env
                if all(dep in env for dep in deps):
                    ready_steps.append(step)
            
            if not ready_steps:
                # Circular dependency or missing initial inputs
                unexecuted = [s.get("agent") for s in steps if s.get("step_id") not in executed_steps]
                raise RuntimeError(f"Gargalo de dependência detectado! Não foi possível executar: {unexecuted}")

            # Execute all ready steps concurrently
            tasks = []
            for step in ready_steps:
                agent_name = step.get("agent")
                agent_config = personas.get(agent_name, {})
                system_prompt = agent_config.get("system_prompt", "")
                
                # Retrieve inputs
                step_inputs = []
                if step.get("input_source"):
                    step_inputs.append(f"[{step.get('input_source').upper()}]:\n{env[step.get('input_source')]}")
                if step.get("input_sources"):
                    for src in step.get("input_sources"):
                        step_inputs.append(f"[{src.upper()}]:\n{env[src]}")
                
                user_content = "\n\n".join(step_inputs)
                
                # Determine model
                model = MODEL_CODER if agent_name in ["Linus", "Kent Beck"] else MODEL_DEFAULT
                
                print(f"{Ouro}[{agent_name} - {agent_config.get('role', 'Agente')}] Iniciando processamento...{Reset}")
                
                # Schedule task
                tasks.append(
                    (step, self._call_openrouter(model, system_prompt, user_content, agent_name, str(initial_inputs)))
                )
            
            # Await all tasks concurrently
            results = await asyncio.gather(*(t[1] for t in tasks))
            
            # Save results into variables environment
            for (step, _), result in zip(tasks, results):
                agent_name = step.get("agent")
                out_var = step.get("output_var")
                env[out_var] = result
                executed_steps.add(step.get("step_id"))
                print(f"{Verde}[{agent_name} - Concluído]{Reset}\n{result}\n")
        
        print(f"{Obsidian}============================================================{Reset}\n")
        if self._is_mock_mode():
            env["mock"] = True
        return env

if __name__ == "__main__":  # pragma: no cover
    # Test runner
    orchestrator = SquadOrchestrator("c:\\Users\\huggs\\OneDrive\\Documentos\\workspace")
    print("[*] Testando carregamento de configs...")
    print("DevSquad config:", list(orchestrator.load_squad_config("dev_squad").keys()))
    print("QA Workflows config:", list(orchestrator.load_workflow_config("qa_workflows").keys()))
