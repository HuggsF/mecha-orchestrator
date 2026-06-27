#!/usr/bin/env python3
"""Envia o relatório para leigo (RELATORIO_LEIGO_TELEGRAM.txt) via Telegram.

Uso (na sua máquina, com rede para api.telegram.org):
    python .mecha/ops/enviar_relatorio_telegram.py

Lê credenciais de .mecha/ops/.env:
    TELEGRAM_BOT_TOKEN (ou MECHAHUGGIES_BOT_TOKEN) + TELEGRAM_CHAT_ID
"""
import os
import re
import sys
import requests

OPS_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(OPS_DIR)
ENV_PATH = os.path.join(OPS_DIR, ".env")
REPORT_PATH = os.path.join(BASE_DIR, "RELATORIO_LEIGO_TELEGRAM.txt")


def load_dotenv(path: str) -> None:
    if not os.path.exists(path):
        return
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def scrub(text: str) -> str:
    """Mascara tokens de bot em mensagens de erro."""
    return re.sub(r"bot\d+:[A-Za-z0-9_-]+", "bot***", str(text))


def main() -> int:
    load_dotenv(ENV_PATH)
    token = os.environ.get("TELEGRAM_BOT_TOKEN") or os.environ.get("MECHAHUGGIES_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        print("ERRO: defina TELEGRAM_BOT_TOKEN (ou MECHAHUGGIES_BOT_TOKEN) e TELEGRAM_CHAT_ID no .env")
        return 2
    if not os.path.exists(REPORT_PATH):
        print(f"ERRO: relatório não encontrado em {REPORT_PATH}")
        return 2

    with open(REPORT_PATH, "r", encoding="utf-8") as f:
        message = f.read()

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    chunks = [message[i:i + 3900] for i in range(0, len(message), 3900)] or [""]
    for idx, chunk in enumerate(chunks, 1):
        try:
            r = requests.post(url, json={"chat_id": chat_id, "text": chunk}, timeout=15)
            if r.status_code != 200:
                print(f"Falha no bloco {idx}/{len(chunks)}: HTTP {r.status_code} — {scrub(r.text)}")
                return 1
            print(f"Bloco {idx}/{len(chunks)} enviado.")
        except requests.RequestException as e:
            print(f"Erro de rede no bloco {idx}/{len(chunks)}: {scrub(e)}")
            return 1
    print("✅ Relatório enviado ao Telegram com sucesso.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
