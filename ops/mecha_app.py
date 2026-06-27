import os
import sys
import argparse

# Configurar UTF-8 no stdout/stderr no Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

# Mapeia caminhos
if getattr(sys, 'frozen', False):
    # Executável compilado (dados mutáveis na pasta do executável, recursos na temporária)
    BASE_DIR = os.path.dirname(sys.executable)
    STATIC_DIR = getattr(sys, '_MEIPASS', BASE_DIR)
else:
    # Script normal
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    STATIC_DIR = BASE_DIR

# Insere a pasta de recursos/patterns no path de imports para o PyInstaller
sys.path.insert(0, os.path.join(STATIC_DIR, "patterns"))

try:
    import telegram_bot
    import claw_loop
except ImportError as e:
    print(f"Erro ao importar módulos internos do MECHA: {e}")
    sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="MECHA Action Agent & Telemetry Server")
    subparsers = parser.add_subparsers(dest="command", help="Subcomandos disponíveis")

    # Comando: run-bot
    parser_bot = subparsers.add_parser("run-bot", help="Inicializa o Bot do Telegram e servidor web do Dashboard")

    # Comando: run-claw
    parser_claw = subparsers.add_parser("run-claw", help="Executa o loop de ações cognitivas do Claw")
    parser_claw.add_argument("--target", type=str, required=True, help="Título parcial da janela a ser focada")
    parser_claw.add_argument("--goal", type=str, help="Meta/objetivo em linguagem natural para a IA")

    args = parser.parse_args()

    if args.command == "run-bot":
        print("==========================================================")
        print("          INICIALIZANDO MECHA BOT & DASHBOARD WEB          ")
        print("==========================================================")
        print(f" [*] Diretorio do Executavel: {BASE_DIR}")
        print(f" [*] Recursos Estaticos: {STATIC_DIR}")
        print("==========================================================")
        telegram_bot.main()

    elif args.command == "run-claw":
        print("==========================================================")
        print("          INICIALIZANDO MECHA CLAW ACTION LOOP            ")
        print("==========================================================")
        print(f" [*] Diretorio de Trabalho: {BASE_DIR}")
        print(f" [*] Janela Alvo: '{args.target}'")
        print(f" [*] Objetivo: '{args.goal}'")
        print("==========================================================")
        
        # Cria configuração do loop
        cfg = claw_loop.LoopConfig(
            target_window_title=args.target,
            goal=args.goal
        )
        loop = claw_loop.ClawActionLoop(cfg)
        loop.start_loop()

    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
