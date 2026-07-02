import os
import sys
import argparse

# Enforce UTF-8 encoding output for Windows terminals (Bug CP1252 bypass)
sys.stdout.reconfigure(encoding='utf-8')

def create_file_if_not_exists(path: str, content: str):
    if not os.path.exists(path):
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  [+] Criado: {os.path.basename(path)}")
    else:
        print(f"  [~] Ignorado (já existe): {os.path.basename(path)}")

def bootstrap_project(target_dir: str):
    print(f"\n[🚀] Iniciando Bootstrap MECHA no projeto: {target_dir}\n")
    os.makedirs(target_dir, exist_ok=True)
    
    # 1. ROOT DOCS
    readme_content = f"# {os.path.basename(target_dir)}\n\nVisão geral e objetivo principal deste projeto sob o ecossistema MECHA.\n"
    create_file_if_not_exists(os.path.join(target_dir, "README.md"), readme_content)
    
    arch_content = "# ARCHITECTURE\n\nDescreva o fluxo de dados, serviços principais e a ontologia local deste projeto.\n"
    create_file_if_not_exists(os.path.join(target_dir, "ARCHITECTURE.md"), arch_content)
    
    stack_content = "# STACK\n\nDefinição estrita das tecnologias base.\n- Linguagem:\n- Framework:\n- DB:\n"
    create_file_if_not_exists(os.path.join(target_dir, "STACK.md"), stack_content)
    
    next_steps_content = "# NEXT STEPS\n\n- [ ] Definir o primeiro checklist do projeto.\n"
    create_file_if_not_exists(os.path.join(target_dir, "NEXT_STEPS.md"), next_steps_content)
    
    # 2. CUSTOMIZATIONS & RULES (.agents)
    agents_dir = os.path.join(target_dir, ".agents")
    os.makedirs(agents_dir, exist_ok=True)
    
    agents_rules_content = """# MECHA Lore & Regras de Ouro (Project Rules)

Estas regras governam o comportamento dos Agentes Antigravity neste projeto:

1. **Fail First (Let it Fail)**: 
   É estritamente proibido encobrir erros usando blocos `try/except` vazios. Falhas devem quebrar a execução imediatamente e ser logadas de forma explícita.

2. **Trash Dump**: 
   Todo arquivo temporário, log inútil, código depreciado ou de rascunho deve ser jogado em uma pasta `scratch/` ou `_archive/`. Não polua a raiz.

3. **Consulta Determinística (RAG-First)**: 
   Antes de refatorar código legado, os agentes devem ler o contexto via RAG e consultar arquivos da raiz (`ARCHITECTURE.md`, `STACK.md`).
"""
    create_file_if_not_exists(os.path.join(agents_dir, "AGENTS.md"), agents_rules_content)

    print("\n[✔] Scaffolding MECHA injetado com sucesso!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Aplica o Scaffolding Padrão MECHA num projeto.")
    parser.add_argument("project_path", help="Caminho relativo ou absoluto para a pasta do projeto")
    args = parser.parse_args()
    
    target_path = os.path.abspath(args.project_path)
    bootstrap_project(target_path)
