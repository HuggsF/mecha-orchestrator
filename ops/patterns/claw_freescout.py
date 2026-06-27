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
import queue
import threading

# Configuration Globals (read dynamically inside functions with env overrides)
URL = os.environ.get("FREESCOUT_URL", "http://localhost:8080").rstrip("/")
API_KEY = os.environ.get("FREESCOUT_API_KEY", "").strip()
MAILBOX_ID = int(os.environ.get("FREESCOUT_MAILBOX_ID", "1") or "1")
TIMEOUT = 8.0
CUSTOMER_EMAIL = "mecha-claw@telegram.local"

# Incidentes abertos nesta sessão: kind -> {"id":..., "number":...}
_OPEN = {}

# Background thread queue and worker setup
_task_queue = queue.Queue()
_worker_thread = None
_worker_lock = threading.Lock()

def get_config() -> dict:
    """Retorna as configurações atuais baseadas nas variáveis de ambiente com fallbacks seguros."""
    url = os.environ.get("FREESCOUT_URL", URL).rstrip("/")
    api_key = os.environ.get("FREESCOUT_API_KEY", API_KEY).strip()
    
    try:
        mailbox_id = int(os.environ.get("FREESCOUT_MAILBOX_ID", str(MAILBOX_ID)) or "1")
    except ValueError:
        mailbox_id = 1
        
    try:
        timeout = float(os.environ.get("FREESCOUT_TIMEOUT", str(TIMEOUT)))
    except ValueError:
        timeout = 8.0
        
    cust_email = os.environ.get("FREESCOUT_CUSTOMER_EMAIL", CUSTOMER_EMAIL).strip()
    cust_first = os.environ.get("FREESCOUT_CUSTOMER_FIRST_NAME", "MECHA").strip()
    cust_last = os.environ.get("FREESCOUT_CUSTOMER_LAST_NAME", "Claw").strip()
    
    return {
        "url": url,
        "api_key": api_key,
        "mailbox_id": mailbox_id,
        "timeout": timeout,
        "customer_email": cust_email,
        "customer_first_name": cust_first,
        "customer_last_name": cust_last,
    }


def enabled() -> bool:
    """Verifica se o cliente FreeScout está configurado e se a URL é válida."""
    cfg = get_config()
    if not (cfg["url"] and cfg["api_key"]):
        return False
    parsed = urllib.parse.urlparse(cfg["url"])
    return parsed.scheme in ("http", "https") and bool(parsed.netloc)


def _worker():
    while True:
        task = _task_queue.get()
        if task is None:
            break
        func, args, kwargs, callback = task
        try:
            res = func(*args, **kwargs)
            if callback:
                try:
                    callback(res)
                except Exception as cb_err:
                    print(f"  [FreeScout] Erro no callback: {cb_err}")
        except Exception as err:
            print(f"  [FreeScout] Erro na execução da tarefa em background: {err}")
        finally:
            _task_queue.task_done()


def _enqueue_task(func, args, kwargs, callback):
    global _worker_thread
    with _worker_lock:
        if _worker_thread is None or not _worker_thread.is_alive():
            _worker_thread = threading.Thread(target=_worker, name="FreeScoutWorker", daemon=True)
            _worker_thread.start()
    _task_queue.put((func, args, kwargs, callback))


def wait_for_pending_tasks():
    """Aguarda a fila de tarefas em background ser esvaziada (útil para testes)."""
    _task_queue.join()


def _req(method: str, path: str, body=None, params=None):
    if not enabled():
        return (0, None)
    cfg = get_config()
    full = cfg["url"] + path
    if params:
        full += "?" + urllib.parse.urlencode(params)
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(full, data=data, method=method)
    req.add_header("X-FreeScout-API-Key", cfg["api_key"])
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=cfg["timeout"]) as resp:
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
    cfg = get_config()
    payload = {
        "type": "email",
        "mailboxId": cfg["mailbox_id"],
        "subject": subject,
        "status": "active",
        "imported": True,
        "customer": {
            "email": cfg["customer_email"], 
            "firstName": cfg["customer_first_name"], 
            "lastName": cfg["customer_last_name"]
        },
        "threads": [{
            "type": "customer", "text": body_html,
            "customer": {"email": cfg["customer_email"]}, "imported": True,
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
    cfg = get_config()
    return f"{cfg['url']}/conversation/{conversation_id}" if conversation_id else cfg['url']


def open_or_update_incident(kind: str, title: str, detail_html: str, callback=None, sync=False):
    """
    Abre o incidente do tipo `kind` (firewall/recovery) ou, se já houver um aberto
    nesta sessão, adiciona uma nota. Retorna {"number","id","url"} ou None.
    Se sync for False, agenda a operação de rede em thread de background.
    """
    if not enabled():
        if callback:
            try:
                callback(None)
            except Exception as cb_err:
                print(f"  [FreeScout] Erro no callback (não configurado): {cb_err}")
        return None

    def task_action():
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

    if sync:
        return task_action()
    else:
        _enqueue_task(task_action, (), {}, callback)
        return None
