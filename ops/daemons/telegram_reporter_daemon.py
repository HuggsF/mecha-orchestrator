#!/usr/bin/env python3
"""
telegram_reporter_daemon.py - Daemon de envio de relatórios agregados via Telegram.

Lê os status de `.state/digital_twin.status.json` e `.state/cost-optimize.status.json`,
formata um report executivo e envia para o Telegram.

Uso via daemon:
python mecha_daemon.py --name telegram-reporter --interval 24h --cmd "python telegram_reporter_daemon.py"
"""
import os
import json
import sys
import requests
import datetime
import re

DAEMONS_DIR = os.path.dirname(os.path.abspath(__file__))
OPS_DIR = os.path.dirname(DAEMONS_DIR)
STATE_DIR = os.path.join(DAEMONS_DIR, ".state")
ENV_PATH = os.path.join(OPS_DIR, ".env")

def load_dotenv(path: str) -> None:
    if not os.path.exists(path):
        return
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

def read_json(filepath):
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            pass
    return None

def build_report():
    twin_data = read_json(os.path.join(STATE_DIR, "digital_twin.status.json"))
    cost_data = read_json(os.path.join(STATE_DIR, "cost-optimize.status.json"))
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    report = f"🤖 **MECHA INFRASTRUCTURE HARNESS** 🤖\n"
    report += f"📅 Data: `{timestamp}`\n\n"
    
    # Seção Gêmeo Digital
    report += "🌐 **Gêmeo Digital (Neo4j)**\n"
    if twin_data:
        verdict = twin_data.get("verdict", {})
        status = verdict.get("status", "UNKNOWN")
        nodes = verdict.get("max_nodes_running", 0)
        
        icon = "🟢" if status == "OK" else "🔴"
        report += f"{icon} Status: `{status}`\n"
        report += f"📊 Nós Ativos: `{nodes}`\n"
        
        if status == "ALERT" and verdict.get("reasons"):
            report += "⚠️ **Motivos de Alerta:**\n"
            for r in verdict["reasons"]:
                report += f" - {r}\n"
    else:
        report += "⚪ Sem dados coletados.\n"
        
    report += "\n"
        
    # Seção Custos
    report += "💰 **Otimização de Custos**\n"
    if cost_data:
        # A depender da estrutura do cost_data
        report += "🟢 Dados coletados (Detalhes no Painel Electron).\n"
    else:
        report += "⚪ Sem dados coletados ainda.\n"
        
    report += "\n---\n*Harness gerado automaticamente pelo squad de infraestrutura MECHA.*"
    return report

def send_telegram(text: str):
    token = os.environ.get("TELEGRAM_BOT_TOKEN") or os.environ.get("MECHAHUGGIES_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    
    if not token or not chat_id:
        print("ERRO: TELEGRAM_BOT_TOKEN e TELEGRAM_CHAT_ID ausentes.")
        return False
        
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        r = requests.post(url, json={"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}, timeout=15)
        if r.status_code == 200:
            print("Relatório enviado com sucesso via Telegram.")
            return True
        else:
            print(f"Falha ao enviar: HTTP {r.status_code} - {r.text}")
            return False
    except Exception as e:
        print(f"Erro de rede ao enviar telegram: {e}")
        return False

def main():
    load_dotenv(ENV_PATH)
    report = build_report()
    success = send_telegram(report)
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
