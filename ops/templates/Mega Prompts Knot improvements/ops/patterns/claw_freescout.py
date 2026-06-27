#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
claw_freescout.py — cliente FreeScout do MECHA Claw (Fase B/C). stdlib, best-effort.

Quando o firewall bloqueia uma ação ou a auto-recuperação dispara, o Claw abre (ou
comenta) um CHAMADO no FreeScout — o mesmo sistema usado pelo HuggsBot — unificando
os incidentes de automação com a operação de comunicação.

Dedup: o primeiro incidente de cada "kind" (firewall, recovery) na sessão cria uma
conversation; os seguintes viram NOTAS na mesma conversation (evita spam).

Variáveis de ambiente (.env em .mecha/):
  FREESCOUT_URL          ex: http://localhost:8080
  FREESCOUT_API_KEY      API Key (Manage → API & Webhooks)
  FREESCOUT_MAILBOX_ID   mailbox dos chamados (default 1)
"""

import os
import json
import urllib.request
import urllib.error
import urllib.parse

URL = os.environ.get("FREESCOUT_URL", "http://localhost:8080").rstrip("/")
API_KEY = os.environ.get("FREESCOUT_API_KEY", "").strip()
MAILBOX_ID = int(os.environ.get("FREESCOUT_MAILBOX_ID", "1") or "1")
TIMEOUT = 8.0

# Cliente sintético do robô no FreeScout
CUSTOMER_EMAIL = "mecha-claw@telegram.local"

# Incidentes abertos nesta sessão: kind -> {"id":..., "number":...}
_OPEN = {}


def enabled() -> bool:
    return bool(URL and API_KEY)


def _req(method: str, path: str, body=None, params=None):
    if not enabled():
        return (0, None)
    full = URL + path
    if params:
        full += "?" + urllib.parse.urlencode(params)
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(full, data=data, method=method)
    req.add_header("X-FreeScout-API-Key", API_KEY)
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            raw = resp.read().decode("utf-8") or "{}"
            try:
                return (resp.status, json.loads(raw))
            except Exception:
                return (resp.status, None)
    except urllib.error.HTTPError as e:
        try:
            err = e.read().decode("utf-8")
        except Exception:
            err = ""
        print(f"  [FreeScout] HTTP {e.code} em {method} {path}: {err[:160]}")
        try:
            return (e.code, json.loads(err))
        except Exception:
            return (e.code, None)
    except Exception as e:
        print(f"  [FreeScout] Conexão falhou em {method} {path}: {e}")
        return (0, None)


def _create_conversation(subject: str, body_html: str, tags=None):
    payload = {
        "type": "email",
        "mailboxId": MAILBOX_ID,
        "subject": subject,
        "status": "active",
        "imported": True,
        "customer": {"email": CUSTOMER_EMAIL, "firstName": "MECHA", "lastName": "Claw"},
        "threads": [{
            "type": "customer", "text": body_html,
            "customer": {"email": CUSTOMER_EMAIL}, "imported": True,
        }],
    }
    if tags:
        payload["tags"] = tags
    status, data = _req("POST", "/api/conversations", body=payload)
    if status not in (200, 201) and tags:
        payload.pop("tags", None)
        status, data = _req("POST", "/api/conversations", body=payload)
    if status in (200, 201) and isinstance(data, dict):
        return {"id": data.get("id"), "number": data.get("number")}
    return None


def _add_note(conversation_id: int, text_html: str) -> bool:
    if not conversation_id:
        return False
    body = {"type": "note", "text": text_html, "imported": True}
    status, _ = _req("POST", f"/api/conversations/{conversation_id}/threads", body=body)
    return status in (200, 201)


def conversation_url(conversation_id) -> str:
    return f"{URL}/conversation/{conversation_id}" if conversation_id else URL


def open_or_update_incident(kind: str, title: str, detail_html: str):
    """
    Abre o incidente do tipo `kind` (firewall/recovery) ou, se já houver um aberto
    nesta sessão, adiciona uma nota. Retorna {"number","id","url"} ou None.
    """
    if not enabled():
        return None

    existing = _OPEN.get(kind)
    if existing and existing.get("id"):
        _add_note(existing["id"], f"<b>Novo evento:</b><br>{detail_html}")
        return {"number": existing["number"], "id": existing["id"],
                "url": conversation_url(existing["id"])}

    conv = _create_conversation(
        subject=title,
        body_html=detail_html,
        tags=["mecha-claw", kind],
    )
    if conv and conv.get("id"):
        _OPEN[kind] = {"id": conv["id"], "number": conv["number"]}
        return {"number": conv["number"], "id": conv["id"],
                "url": conversation_url(conv["id"])}
    return None
