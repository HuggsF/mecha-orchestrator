import os
import sys
import argparse
import subprocess
from pathlib import Path

# Calcula a raiz do diretorio ops/ onde os patterns estao
OPS_ROOT = Path(__file__).resolve().parent.parent

def run_pattern_script(script_name, args):
    """Executa um script da pasta ops/patterns repassando os argumentos."""
    script_path = OPS_ROOT / "patterns" / script_name
    
    cmd = [sys.executable, str(script_path)] + args
    print(f"[*] Executando: {' '.join(cmd)}")
    try:
        res = subprocess.run(cmd)
        sys.exit(res.returncode)
    except KeyboardInterrupt:
        sys.exit(1)
    except Exception as e:
        print(f"[!] Erro ao executar {script_name}: {e}")
        sys.exit(1)

def handle_sdk(args):
    """Lida com comandos originais do 'mecha sdk'."""
    cmd = args.sdk_cmd
    
    if cmd == "check-plan":
        if not args.target:
            print("Caminho do arquivo Markdown nao fornecido.")
            sys.exit(1)
        run_pattern_script("dynamic_typing.py", ["--validate", args.target])
    
    elif cmd == "draw":
        if not args.target:
            print("Caminho do arquivo JSON nao fornecido.")
            sys.exit(1)
        run_pattern_script("claw_canvas.py", ["--draw", args.target])
    
    elif cmd == "draw-test":
        run_pattern_script("claw_canvas.py", ["--test"])
    
    elif cmd == "scan":
        run_pattern_script("claw_vision.py", [])
        
    elif cmd == "graph":
        run_pattern_script("claw_graph.py", [])
        
    elif cmd == "run-claw":
        if not args.target:
            print("Titulo da janela alvo nao fornecido.")
            sys.exit(1)
        call_args = ["--target", args.target]
        if args.goal:
            call_args.extend(["--goal", args.goal])
        run_pattern_script("claw_loop.py", call_args)
        
    elif cmd == "find-icon":
        if not args.target:
            print("Nome do template visual nao fornecido.")
            sys.exit(1)
        run_pattern_script("claw_cv.py", ["--find", args.target])
        
    elif cmd == "comfy-render":
        if not args.target:
            print("Caminho do arquivo JSON de request nao fornecido.")
            sys.exit(1)
        run_pattern_script("claw_comfy.py", ["--render", args.target])
        
    elif cmd == "find-text":
        if not args.target:
            print("Texto-alvo nao fornecido.")
            sys.exit(1)
        run_pattern_script("claw_ocr.py", ["--find-text", args.target])
        
    elif cmd == "sync-obsidian":
        run_pattern_script("claw_graph.py", ["--sync-obsidian"])
        
    elif cmd == "run-bot":
        run_pattern_script("telegram_bot.py", [])
        
    elif cmd == "tribunal-test":
        run_pattern_script("test_e2e_tribunal.py", [])
        
    else:
        print(f"Subcomando SDK '{cmd}' desconhecido.")
        sys.exit(1)

def handle_squads(args):
    """Stub para interacao com os Squads (ex: MECHA_GLOBAL_SQUAD)."""
    print(f"[*] Modulo SQUADS ativado. Comando: {args.squads_cmd}")
    if args.squads_cmd == "list":
        print(" - MECHA_GLOBAL_SQUAD")
        print(" - ORCHESTRATOR_CORE")
    else:
        print("  (Ainda nao implementado. Prontos para ligar backend de squads).")

def handle_workflows(args):
    """Stub para os Workflows (Mecha / Antigravity)."""
    print(f"[*] Modulo WORKFLOWS ativado. Comando: {args.workflows_cmd}")
    print("  (Ainda nao implementado).")

def handle_skills(args):
    """Stub para as Skills do ecossistema Mecha."""
    print(f"[*] Modulo SKILLS ativado. Comando: {args.skills_cmd}")
    if args.skills_cmd == "list":
        print(" - mcp-gold-pattern")
        print(" - memory-mesh")
        print(" - mecha-orchestration")
    else:
        print("  (Ainda nao implementado).")

def handle_backend(args):
    """Stub para comunicacao direta com AgentBus/Antigravity."""
    print(f"[*] Modulo BACKEND ativado. Comando: {args.backend_cmd}")
    if args.backend_cmd == "ping":
        print(" [+] AgentBus: OFFLINE (Mock)")
    else:
        print("  (Ainda nao implementado).")

def main():
    parser = argparse.ArgumentParser(description="MECHA SYSTEM CLI")
    subparsers = parser.add_subparsers(dest="module", required=True, help="Modulos do Mecha")
    
    # --- Módulo SDK (Legado) ---
    parser_sdk = subparsers.add_parser("sdk", help="Ferramentas legado e de padroes")
    parser_sdk.add_argument("sdk_cmd", help="Subcomando do SDK (ex: check-plan, run-claw)")
    parser_sdk.add_argument("target", nargs="?", help="Alvo do comando (arquivo, titulo, etc)")
    parser_sdk.add_argument("-goal", help="Instrucao de goal para run-claw", default=None)
    
    # --- Módulo Squads ---
    parser_squads = subparsers.add_parser("squads", help="Gestao de Squads (Times de Agentes)")
    parser_squads.add_argument("squads_cmd", choices=["list", "run", "handoff"], help="Acao")
    
    # --- Módulo Workflows ---
    parser_workflows = subparsers.add_parser("workflows", help="Gestao de Workflows")
    parser_workflows.add_argument("workflows_cmd", choices=["start", "status"], help="Acao")
    
    # --- Módulo Skills ---
    parser_skills = subparsers.add_parser("skills", help="Execucao e gerencia de Skills")
    parser_skills.add_argument("skills_cmd", choices=["list", "run"], help="Acao")
    
    # --- Módulo Backend ---
    parser_backend = subparsers.add_parser("backend", help="AgentBus e Antigravity API")
    parser_backend.add_argument("backend_cmd", choices=["ping", "sync", "status"], help="Acao")
    
    args = parser.parse_args()
    
    if args.module == "sdk":
        handle_sdk(args)
    elif args.module == "squads":
        handle_squads(args)
    elif args.module == "workflows":
        handle_workflows(args)
    elif args.module == "skills":
        handle_skills(args)
    elif args.module == "backend":
        handle_backend(args)

if __name__ == "__main__":
    main()
