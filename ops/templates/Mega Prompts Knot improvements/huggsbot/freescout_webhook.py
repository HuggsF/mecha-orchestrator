#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
freescout_webhook.py — receptor de webhooks do FreeScout → notifica no Telegram. (OPCIONAL)

Quando um agente responde ou muda o status de um chamado no FreeScout, este servidor
recebe o evento e manda uma mensagem para o chat do Telegram que abriu o chamado.

Como o cliente foi criado com e-mail sintético tg<chat_id>@telegram.local, conseguimos
recuperar o chat_id a partir do e-mail do cliente no payload do webhook.

Rodar (em paralelo ao huggsbot.py):
    python freescout_webhook.py        # escuta em 0.0.0.0:FREESCOUT_WEBHOOK_PORT

No FreeScout (Manage → API & Webhooks → Webhooks), aponte os eventos
'convo.agent.replied' e 'convo.updated' para:
    http://SEU_HOST:8765/freescout
(precisa de host acessível pelo FreeScout — localhost serve se ambos na mesma máquina)
"""

import os
import re
import json
import urllib.request
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

TOKEN = os.environ.get("TELEGRAM_TOKEN", "").strip()
PORT = int(os.environ.get("FREESCOUT_WEBHOOK_PORT", "8765") or "8765")


def send_telegram(chat_id: int, text: str) -> None:
    if not TOKEN:
        print("  [Webhook] TELEGRAM_TOKEN ausente — não enviei.")
        return
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = urllib.parse.urlencode({
        "chat_id": chat_id, "text": text,
        "parse_mode": "Markdown", "disable_web_page_preview": "true",
    }).encode("utf-8")
    try:
        urllib.request.urlopen(urllib.request.Request(url, data=data), timeout=8)
    except Exception as e:
        print(f"  [Webhook] Erro ao enviar Telegram: {e}")


def extract_chat_id(payload: dict):
    """Procura o e-mail tg<chat_id>@telegram.local em qualquer lugar do payload."""
    blob = json.dumps(payload)
    m = re.search(r"tg(-?\d+)@telegram\.local", blob)
    return int(m.group(1)) if m else None


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def do_POST(self):
        if self.path.rstrip("/") != "/freescout":
            self.send_response(404); self.end_headers(); return
        try:
            n = int(self.headers.get("Content-Length", 0))
            payload = json.loads(self.rfile.read(n).decode("utf-8") or "{}")
        except Exception:
            self.send_response(400); self.end_headers(); return

        chat_id = extract_chat_id(payload)
        conv = payload.get("conversation") or payload
        number = conv.get("number", "?")
        subject = conv.get("subject", "")
        status = conv.get("status", "")
        event = payload.get("event") or self.headers.get("X-FreeScout-Event", "atualização")

        if chat_id:
            if "replied" in str(event):
                msg = f"💬 *Resposta no chamado* `#{number}`\n_{subject}_\nA equipe respondeu — confira."
            else:
                msg = f"🔄 *Chamado* `#{number}` atualizado\n_{subject}_\nStatus: *{status}*"
            send_telegram(chat_id, msg)
            print(f"  [Webhook] Notificado chat {chat_id} sobre #{number} ({event})")
        else:
            print("  [Webhook] Sem chat_id no payload (cliente não é do Telegram). Ignorado.")

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(b'{"ok":true}')


if __name__ == "__main__":
    print(f"[*] Webhook FreeScout→Telegram ouvindo em http://0.0.0.0:{PORT}/freescout")
    ThreadingHTTPServer(("", PORT), Handler).serve_forever()
