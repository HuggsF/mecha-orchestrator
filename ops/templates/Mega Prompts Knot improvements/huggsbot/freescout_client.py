#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
freescout_client.py — cliente REST mínimo para o FreeScout (stdlib, sem dependências extras).

Usado pelo HuggsBot para persistir chamados no FreeScout em vez de memória.
Tudo é best-effort: qualquer falha retorna None/[] para o bot cair no fallback em memória.

Variáveis de ambiente (.env):
  FREESCOUT_URL          ex: http://localhost:8080   (sem barra no fim)
  FREESCOUT_API_KEY      a API Key (Manage → API & Webhooks)
  FREESCOUT_MAILBOX_ID   id do mailbox onde os chamados entram (default 1)
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


def enabled() -> bool:
    """True se houver URL + API Key configuradas."""
    return bool(URL and API_KEY)


def _req(method: str, path: str, body=None, params=None):
    """Faz uma requisição à API. Retorna (status_code, parsed_json|None). Nunca levanta."""
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
            err_body = e.read().decode("utf-8")
        except Exception:
            err_body = ""
        print(f"  [FreeScout] HTTP {e.code} em {method} {path}: {err_body[:200]}")
        try:
            return (e.code, json.loads(err_body))
        except Exception:
            return (e.code, None)
    except Exception as e:
        print(f"  [FreeScout] Falha de conexão em {method} {path}: {e}")
        return (0, None)


def create_conversation(subject: str, body_html: str, customer_email: str,
                        customer_first: str = "Telegram", customer_last: str = "User",
                        tags=None, urgent: bool = False):
    """
    Cria um chamado (conversation) no FreeScout. Retorna dict com {id, number} ou None.
    Tenta com tags; se o módulo de Tags não existir e a API recusar, repete sem tags.
    'imported=true' evita que o FreeScout dispare e-mail para o endereço sintético do Telegram.
    """
    payload = {
        "type": "email",
        "mailboxId": MAILBOX_ID,
        "subject": subject,
        "status": "active",
        "imported": True,
        "customer": {
            "email": customer_email,
            "firstName": customer_first,
            "lastName": customer_last,
        },
        "threads": [{
            "type": "customer",
            "text": body_html,
            "customer": {"email": customer_email},
            "imported": True,
        }],
    }
    if urgent:
        payload["status"] = "active"
    if tags:
        payload["tags"] = tags

    status, data = _req("POST", "/api/conversations", body=payload)

    # Se falhou por causa das tags (módulo ausente), tenta de novo sem elas.
    if status not in (200, 201) and tags:
        payload.pop("tags", None)
        status, data = _req("POST", "/api/conversations", body=payload)

    if status in (200, 201) and isinstance(data, dict):
        return {"id": data.get("id"), "number": data.get("number")}
    return None


def add_note(conversation_id: int, text_html: str) -> bool:
    """Adiciona uma nota interna (note) a um chamado existente. Usado pela integração com o MECHA."""
    if not conversation_id:
        return False
    body = {"type": "note", "text": text_html, "imported": True}
    status, _ = _req("POST", f"/api/conversations/{conversation_id}/threads", body=body)
    return status in (200, 201)


def list_conversations(customer_email: str, limit: int = 10):
    """Lista os chamados de um cliente (mais recentes primeiro). Retorna lista de dicts simplificados."""
    status, data = _req("GET", "/api/conversations", params={
        "mailboxId": MAILBOX_ID,
        "customerEmail": customer_email,
        "pageSize": limit,
        "sortField": "createdAt",
        "sortOrder": "desc",
    })
    if status != 200 or not isinstance(data, dict):
        return []
    convs = (data.get("_embedded", {}) or {}).get("conversations", []) or []
    out = []
    for c in convs[:limit]:
        out.append({
            "number": c.get("number"),
            "subject": c.get("subject", ""),
            "status": c.get("status", ""),
            "id": c.get("id"),
        })
    return out


def conversation_url(conversation_id) -> str:
    """URL da conversa no FreeScout (para mandar no Telegram)."""
    return f"{URL}/conversation/{conversation_id}" if conversation_id else URL
