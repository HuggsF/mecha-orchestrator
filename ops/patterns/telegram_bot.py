import os
import re
import sys
import json
import time
import requests
import logging
import threading
import asyncio
from typing import Optional, List, Dict, Any, Tuple
from pydantic import BaseModel, Field
import collections
import socket
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Configuração de logs
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger("MECHA_TelegramBot")


def _scrub_token(value) -> str:
    """Mascara tokens de bot do Telegram em mensagens de log (evita vazamento de credencial)."""
    return re.sub(r"bot\d+:[A-Za-z0-9_-]+", "bot***", str(value))

# Caminhos dos arquivos IPC de controle
if getattr(sys, 'frozen', False):
    # Executável compilado (dados mutáveis na pasta do executável, recursos na temporária)
    BASE_DIR = os.path.dirname(sys.executable)
    STATIC_DIR = getattr(sys, '_MEIPASS', BASE_DIR)
else:
    # Script normal
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    STATIC_DIR = BASE_DIR

STATUS_FILE = os.path.join(BASE_DIR, "logs", "claw_status.json")
PREEMPT_FILE = os.path.join(BASE_DIR, "logs", "claw_preempt.json")

# Identidade do produto (frontend = Mecha Huggs Workforce Studio / HWorkforceStudio)
PRODUCT_NAME = "Mecha Huggs Workforce Studio"
PRODUCT_SLUG = "HWorkforceStudio"

# Lock de IO + escrita atômica para os JSONs que o Studio lê via /api/status.
_IO_LOCK = threading.RLock()


def _atomic_write_json(path: str, data) -> None:
    """Escrita atômica (tmp + os.replace) para evitar leituras parciais no /api/status."""
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    tmp_path = f"{path}.{os.getpid()}.tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp_path, path)

# Adiciona o diretório atual ao sys.path para imports locais
if getattr(sys, 'frozen', False):
    sys.path.insert(0, os.path.join(STATIC_DIR, "patterns"))
else:
    sys.path.insert(0, os.path.join(BASE_DIR, "patterns"))

try:
    from dynamic_typing import validate_event_envelope
except ImportError:
    def validate_event_envelope(data: dict):
        return True, "Fallback"

_UVICORN_LOOP = None

class EventHub:
    def __init__(self):
        self.lock = threading.Lock()
        self.connections: List[WebSocket] = []
        self.buffer = collections.deque(maxlen=100)

    def subscribe(self, websocket: WebSocket):
        with self.lock:
            self.connections.append(websocket)

    def unsubscribe(self, websocket: WebSocket):
        with self.lock:
            if websocket in self.connections:
                self.connections.remove(websocket)

    def publish(self, event: dict) -> Tuple[bool, str]:
        # Validate using dynamic_typing
        success, err_msg = validate_event_envelope(event)
        if not success:
            logger.error(f"[BUS:VALIDATION_ERROR] Evento inválido rejeitado: {err_msg}. Evento: {event}")
            return False, err_msg

        # Add to buffer
        with self.lock:
            self.buffer.append(event)

        # Broadcast to websockets
        topic = event.get("topic")
        sender = event.get("sender")
        logger.info(f"🌸 [BUS:{topic}] sender={sender} | payload={event.get('payload')}")
        
        with self.lock:
            active = list(self.connections)
            
        dead_connections = []
        for ws in active:
            try:
                if _UVICORN_LOOP and _UVICORN_LOOP.is_running():
                    asyncio.run_coroutine_threadsafe(ws.send_json(event), _UVICORN_LOOP)
            except Exception as e:
                logger.error(f"Erro ao transmitir para WebSocket: {e}")
                dead_connections.append(ws)

        if dead_connections:
            with self.lock:
                for ws in dead_connections:
                    if ws in self.connections:
                        self.connections.remove(ws)

        return True, "Broadcast finalizado."

    def get_events(self, since_ms: int = 0) -> list:
        with self.lock:
            return [e for e in self.buffer if e.get("timestamp", 0) >= since_ms]

event_hub = EventHub()


def load_dotenv() -> None:
    """Carrega variáveis de ambiente de um arquivo .env se existir."""
    env_path = os.path.join(BASE_DIR, ".env")
    if os.path.exists(env_path):
        logger.info(f"Carregando configurações de {env_path}")
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    parts = line.split("=", 1)
                    if len(parts) == 2:
                        key = parts[0].strip()
                        val = parts[1].strip().strip('"').strip("'")
                        os.environ[key] = val

# Carrega ambiente
load_dotenv()

def select_working_token() -> str:
    t1 = os.environ.get("TELEGRAM_BOT_TOKEN")
    t2 = os.environ.get("MECHAHUGGIES_BOT_TOKEN")
    if not t1 and not t2:
        return ""
    if t1 and not t2:
        return t1
    if t2 and not t1:
        return t2
    try:
        r = requests.get(f"https://api.telegram.org/bot{t1}/getMe", timeout=3)
        if r.status_code == 200:
            logger.info("Usando TELEGRAM_BOT_TOKEN (T1) validado com sucesso.")
            return t1
        else:
            logger.warning(f"TELEGRAM_BOT_TOKEN (T1) inválido (Status {r.status_code}). Testando MECHAHUGGIES_BOT_TOKEN (T2)...")
    except Exception as e:
        logger.error(f"Erro ao testar TELEGRAM_BOT_TOKEN: {_scrub_token(e)}")
    try:
        r = requests.get(f"https://api.telegram.org/bot{t2}/getMe", timeout=3)
        if r.status_code == 200:
            logger.info("Usando MECHAHUGGIES_BOT_TOKEN (T2) validado com sucesso.")
            return t2
    except Exception as e:
        logger.error(f"Erro ao testar MECHAHUGGIES_BOT_TOKEN: {_scrub_token(e)}")
    return t1 or ""

TOKEN = select_working_token()
CHAT_ID_ENV = os.environ.get("TELEGRAM_CHAT_ID")
AUTHORIZED_CHAT_ID = int(CHAT_ID_ENV) if CHAT_ID_ENV else None

def send_message(chat_id: int, text: str) -> None:
    """Envia mensagem de texto via API do Telegram."""
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}, timeout=5)
    except Exception as e:
        logger.error(f"Erro ao enviar mensagem: {_scrub_token(e)}")

def send_photo(chat_id: int, photo_path: str, caption: str) -> None:
    """Envia imagem via API do Telegram."""
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
        with open(photo_path, "rb") as photo:
            requests.post(url, data={"chat_id": chat_id, "caption": caption, "parse_mode": "Markdown"}, files={"photo": photo}, timeout=8)
    except Exception as e:
        logger.error(f"Erro ao enviar foto: {_scrub_token(e)}")

def send_preempt_command(action: str, params: dict = None) -> None:
    """Grava uma instrução de preempção em claw_preempt.json."""
    if params is None:
        params = {}
    data = {
        "action": action,
        "params": params,
        "processed": False,
        "timestamp": time.time()
    }
    with _IO_LOCK:
        _atomic_write_json(PREEMPT_FILE, data)
    logger.info(f"Comando de preempção enviado: {action} com {params}")

def log_event_to_dashboard(level: str, msg: str) -> None:
    """Registra um evento de telemetria em claw_status.json para o Dashboard/Studio."""
    with _IO_LOCK:
        data = {}
        if os.path.exists(STATUS_FILE):
            try:
                with open(STATUS_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception:
                data = {}
        if not isinstance(data, dict):
            data = {}

        events = data.get("events", [])
        if not isinstance(events, list):
            events = []
        events.append({
            "time": time.strftime("%H:%M:%S"),
            "level": level,  # info, ok, warn, danger, vision
            "msg": msg,
            "id": f"bot_{time.time()}_{abs(hash(msg))}",
        })
        data["events"] = events[-30:]  # Mantém as últimas 30

        try:
            _atomic_write_json(STATUS_FILE, data)
        except OSError as e:
            logger.error(f"Erro ao logar no dashboard: {e}")

        # Publish to event bus too!
        event = {
            "topic": "claw.log",
            "sender": "telegram_bot",
            "timestamp": int(time.time() * 1000),
            "payload": {
                "level": level,
                "msg": msg,
                "time": time.strftime("%H:%M:%S")
            }
        }
        try:
            event_hub.publish(event)
        except Exception as e:
            logger.error(f"Erro ao publicar claw.log no bus: {e}")


def wait_for_preempt_processed(timeout: float = 10.0) -> bool:
    """Aguarda o processamento de um comando pelo loop do Claw (verificando o arquivo IPC)."""
    start = time.time()
    while time.time() - start < timeout:
        if os.path.exists(PREEMPT_FILE):
            try:
                with open(PREEMPT_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if data.get("processed", False):
                        return True
            except Exception:
                pass
        time.sleep(0.5)
    return False

# --- Threads de Execução Assíncrona ---

def run_tribunal_thread(chat_id: int, topic: str):
    send_message(chat_id, "⚖️ *Iniciando Tribunal dos Awesome-Bots (Auditoria Context7)...*")
    log_event_to_dashboard("info", f"Auditoria do Tribunal Hermes iniciada: {topic[:50]}...")
    
    try:
        from awesome_bots_orchestrator import AwesomeBotsOrchestrator
        from ghost_worker import GhostWorker
        import re
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        # O workspace root é um nível acima do ops
        workspace_root = os.path.dirname(BASE_DIR)
        orchestrator = AwesomeBotsOrchestrator(workspace_root)
        debate = loop.run_until_complete(orchestrator.run_tribunal(topic))
        
        veredito = debate["shura"]
        approved = "[1]" in veredito
        level = "ok" if approved else "danger"
        status_txt = "APROVADO [1]" if approved else "REJEITADO [0]"
        
        log_event_to_dashboard(level, f"Tribunal Hermes finalizado. Veredito: {status_txt}")
        
        # Extrai nome do lead para o Ghost Worker
        scope_match = re.search(r'#\{\d+\}\s*\{([^}]+)\}', topic)
        if scope_match:
            lead_name = scope_match.group(1).strip()
        else:
            lead_match = re.search(r'(?:lead|lead_name|nome|nome_do_lead)\s*[:=]\s*([^\n]+)', topic, re.IGNORECASE)
            if lead_match:
                lead_name = lead_match.group(1).strip()
            else:
                first_line = topic.split('\n')[0].strip()
                lead_name = first_line[:47] + "..." if len(first_line) > 50 else first_line
        
        # Aciona o Ghost Worker
        worker = GhostWorker(workspace_root)
        worker_msg = worker.process_audit(lead_name, veredito)
        
        # Envia transcrição de volta ao chat do Telegram
        msg = (
            f"⚖️ **TRIBUNAL HERMES — VEREDITO: {status_txt}** ⚖️\n\n"
            f"😈 *Warlock (Acusação / Segurança)*:\n{debate['warlock']}\n\n"
            f"🛡️ *Amanda (Defesa / Conformidade)*:\n{debate['amanda']}\n\n"
            f"👑 *Shura 255 (Juiz / Lead Arquiteto)*:\n{veredito}\n\n"
            f"⚙️ **Ação pós-auditoria (Ghost Worker)**:\n{worker_msg}"
        )
        send_message(chat_id, msg)
    except Exception as e:
        logger.error(f"Erro no Tribunal: {e}")
        log_event_to_dashboard("danger", f"Erro na execução do Tribunal: {e}")
        send_message(chat_id, f"❌ Erro ao rodar o Tribunal: {e}")

def run_rag_thread(chat_id: int, query: str):
    send_message(chat_id, "🔍 *Consultando base de conhecimento vetorial do Qdrant...*")
    log_event_to_dashboard("info", f"Qdrant RAG: Buscando '{query}'...")
    
    try:
        from qdrant_client_helper import QdrantRAGClient
        client = QdrantRAGClient()
        hits = client.search(query, limit=3)
        
        if not hits:
            send_message(chat_id, "🔍 *Qdrant RAG:* Nenhum contexto correspondente encontrado na base local.")
            log_event_to_dashboard("warn", f"Qdrant RAG: Nenhum resultado para '{query}'")
            return
            
        msg = "🔍 **Resultados da Busca Semântica no Qdrant** 🔍\n\n"
        for idx, hit in enumerate(hits):
            score = hit["score"]
            text = hit["text"]
            meta = hit["metadata"]
            msg += f"📄 *Documento {idx+1}* [Cosine Score: {score:.4f}]\n`{text}`\n"
            if meta:
                msg += f"🏷️ _Metadados:_ `{meta}`\n"
            msg += "\n"
            
        send_message(chat_id, msg)
        log_event_to_dashboard("ok", f"Qdrant RAG: {len(hits)} hits retornados para '{query}'")
    except Exception as e:
        logger.error(f"Erro no RAG: {e}")
        send_message(chat_id, f"❌ Erro ao consultar RAG: {e}")

def run_playbook_thread(chat_id: int, playbook_name: str):
    playbook_dirs = [
        os.path.join(BASE_DIR, "intelligence", "playbooks"),
        os.path.join(os.path.dirname(BASE_DIR), ".claw", "playbooks")
    ]
    
    playbook_path = None
    for folder in playbook_dirs:
        candidate = os.path.join(folder, f"{playbook_name}.md")
        if os.path.exists(candidate):
            playbook_path = candidate
            break
            
    if not playbook_path:
        send_message(chat_id, f"❌ Playbook `{playbook_name}` não encontrado nas pastas de playbooks.")
        log_event_to_dashboard("danger", f"Erro: Playbook '{playbook_name}' não encontrado.")
        return
        
    send_message(chat_id, f"🎬 *Iniciando Playbook:* `{playbook_name}`")
    log_event_to_dashboard("warn", f"Executando Playbook RPA: {playbook_name}")
    
    try:
        with open(playbook_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            
        steps = []
        for line in lines:
            line = line.strip()
            if line.startswith("-"):
                steps.append(line[1:].strip())
                
        if not steps:
            send_message(chat_id, f"⚠️ Playbook `{playbook_name}` não contém instruções executáveis no formato `- <comando>`.")
            return
            
        for idx, step in enumerate(steps):
            send_message(chat_id, f"⚙️ *Passo {idx+1}/{len(steps)}:* `{step}`")
            log_event_to_dashboard("info", f"Playbook [{playbook_name}]: {step}")
            
            parts = step.split(maxsplit=1)
            action = parts[0].lower() if parts else ""
            param_str = parts[1].strip() if len(parts) > 1 else ""
            
            if action == "click":
                coords = param_str.split()
                if len(coords) >= 2:
                    x, y = int(coords[0]), int(coords[1])
                    send_preempt_command("click", {"x": x, "y": y})
                    wait_for_preempt_processed()
                else:
                    send_message(chat_id, "❌ Coordenadas do click inválidas.")
            elif action == "type":
                text_to_type = param_str.strip('"').strip("'")
                send_preempt_command("type", {"text": text_to_type})
                wait_for_preempt_processed()
            elif action == "set_goal":
                goal_text = param_str.strip('"').strip("'")
                send_preempt_command("set_goal", {"goal": goal_text})
                wait_for_preempt_processed()
            elif action == "wait":
                try:
                    seconds = int(param_str)
                    time.sleep(seconds)
                except ValueError:
                    time.sleep(2)
            else:
                send_preempt_command(action, {"params": param_str})
                wait_for_preempt_processed()
                
            time.sleep(1.5)
            
        send_message(chat_id, f"✅ *Playbook `{playbook_name}` finalizado com sucesso!*")
        log_event_to_dashboard("ok", f"Playbook '{playbook_name}' concluído com sucesso.")
    except Exception as e:
        logger.error(f"Erro no Playbook: {e}")
        send_message(chat_id, f"❌ Erro ao rodar playbook: {e}")
        log_event_to_dashboard("danger", f"Erro no Playbook '{playbook_name}': {e}")


def is_claw_loop_online() -> bool:
    """Verifica se o loop do robô Claw está rodando (atualizado nos últimos 45 segundos)"""
    try:
        return os.path.exists(STATUS_FILE) and (time.time() - os.path.getmtime(STATUS_FILE) < 45)
    except OSError:
        return False


# --- Gestão de Tarefas da Amanda (/task, /todo) ---

def handle_task_command(text: str) -> Dict[str, str]:
    prefix = "/task" if text.startswith("/task") else "/todo"
    rest = text[len(prefix):].strip()
    parts = rest.split(maxsplit=1)
    action = parts[0].lower() if parts else "list"
    args = parts[1].strip() if len(parts) > 1 else ""

    tasks_file = os.path.join(BASE_DIR, "logs", "amanda_tasks.json")
    tasks_md = os.path.join(os.path.dirname(BASE_DIR), "AMANDA_TASKS.md")

    def render_markdown(task_list: List[Dict[str, Any]]) -> str:
        lines: List[str] = [
            "# 🌸 STACK DE TASKS DA AMANDA (Shadow Processor)\n\n",
            "> **\"Conformidade e tarefas registradas no Terminal Akasha.\"**\n\n",
            "## 📌 Tarefas Pendentes\n",
        ]
        pending = [t for t in task_list if t.get("status") == "pending"]
        if not pending:
            lines.append("_Nenhuma tarefa pendente no momento._\n")
        for t in pending:
            lines.append(
                f"- [ ] `#{t.get('id')}`: {t.get('description', '')} "
                f"*(Criado em: {t.get('created_at', '?')})*\n"
            )
        lines.append("\n## 🟢 Tarefas Concluídas\n")
        completed = [t for t in task_list if t.get("status") == "completed"]
        if not completed:
            lines.append("_Nenhuma tarefa concluída ainda._\n")
        for t in completed:
            lines.append(
                f"- [x] `#{t.get('id')}`: {t.get('description', '')} "
                f"*(Concluído em: {t.get('completed_at', '?')})*\n"
            )
        return "".join(lines)

    def _read_json_safe(path: str, default: Any) -> Any:
        if not os.path.exists(path):
            return default
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Falha ao ler JSON {path}: {e}")
            return default

    def persist(task_list: List[Dict[str, Any]]) -> None:
        try:
            _atomic_write_json(tasks_file, task_list)
        except OSError as e:
            logger.error(f"Erro ao salvar amanda_tasks.json: {e}")
            return
        try:
            os.makedirs(os.path.dirname(tasks_md) or ".", exist_ok=True)
            tmp_md = f"{tasks_md}.{os.getpid()}.tmp"
            with open(tmp_md, "w", encoding="utf-8") as f:
                f.write(render_markdown(task_list))
            os.replace(tmp_md, tasks_md)
        except OSError as e:
            logger.error(f"Erro ao gerar AMANDA_TASKS.md: {e}")

    def publish_to_bus(topic: str, payload: dict) -> None:
        try:
            event = {
                "topic": topic,
                "sender": "telegram_bot",
                "timestamp": int(time.time() * 1000),
                "payload": payload
            }
            event_hub.publish(event)
        except Exception as e:
            logger.error(f"Erro ao publicar no bus: {e}")

    def log_event_to_dashboard(level: str, msg: str) -> None:
        with _IO_LOCK:
            data = _read_json_safe(STATUS_FILE, {})
            if not isinstance(data, dict):
                data = {}
            events = data.get("events", [])
            if not isinstance(events, list):
                events = []
            events.append({
                "time": time.strftime("%H:%M:%S"),
                "level": level,
                "msg": f"[Amanda Bot] {msg}",
                "id": f"amanda_{time.time()}_{abs(hash(msg))}",
            })
            data["events"] = events[-30:]
            try:
                _atomic_write_json(STATUS_FILE, data)
            except OSError as e:
                logger.error(f"Erro ao logar no dashboard: {e}")

    with _IO_LOCK:
        tasks = _read_json_safe(tasks_file, [])
        if not isinstance(tasks, list):
            tasks = []

        if action == "add":
            if not args:
                return {"type": "message", "text": "❌ **Amanda:** Por favor, descreva a tarefa. Uso: `/task add <descrição>`"}
            new_id = max([int(t.get("id", 0)) for t in tasks], default=0) + 1
            tasks.append({
                "id": new_id,
                "description": args,
                "status": "pending",
                "created_at": time.strftime("%d/%m/%Y %H:%M:%S"),
                "completed_at": "",
            })
            persist(tasks)
            log_event_to_dashboard("ok", f"Nova task #{new_id} adicionada para Amanda")
            publish_to_bus("task.created", {"id": new_id, "description": args})
            return {
                "type": "message",
                "text": f"🌸 **Amanda:** Tarefa registrada com sucesso no Terminal Akasha!\n• **ID:** `#{new_id}`\n• **Descrição:** {args}\n\n*A tarefa foi empilhada e atualizada no arquivo `AMANDA_TASKS.md`.*",
            }

        if action in ("done", "complete"):
            if not args:
                return {"type": "message", "text": "❌ **Amanda:** Por favor, especifique o ID da tarefa. Uso: `/task done <ID>`"}
            try:
                task_id = int(args.replace("#", "").strip())
            except ValueError:
                return {"type": "message", "text": "❌ **Amanda:** O ID da tarefa precisa ser um número inteiro."}
            for t in tasks:
                if t.get("id") == task_id and t.get("status") == "pending":
                    t["status"] = "completed"
                    t["completed_at"] = time.strftime("%d/%m/%Y %H:%M:%S")
                    persist(tasks)
                    log_event_to_dashboard("ok", f"Task #{task_id} marcada como concluída")
                    publish_to_bus("task.completed", {"id": task_id})
                    return {"type": "message", "text": f"🌸 **Amanda:** Excelente! Tarefa `#{task_id}` marcada como concluída e arquivada."}
            return {"type": "message", "text": f"❌ **Amanda:** Tarefa pendente com ID `#{task_id}` não encontrada."}

        if action == "clear":
            tasks = [t for t in tasks if t.get("status") == "pending"]
            persist(tasks)
            log_event_to_dashboard("info", "Fila de tarefas limpa (removidas concluídas)")
            publish_to_bus("task.cleared", {})
            return {"type": "message", "text": "🌸 **Amanda:** Fila de tarefas limpa. Apenas tarefas pendentes foram mantidas."}

        # list (default)
        pending = [t for t in tasks if t.get("status") == "pending"]
        if not pending:
            return {"type": "message", "text": "🌸 **Amanda:** Minha stack de tarefas está limpa! Não há pendências registradas."}
        reply = "🌸 **Amanda - Stack de Tarefas Ativas** 🌸\n\n"
        for t in pending:
            reply += f"• `#{t.get('id')}` - {t.get('description', '')} *(Criado em: {t.get('created_at', '?')})*\n"
        reply += "\n*Comandos úteis: `/task add <desc>`, `/task done <id>`*"
        return {"type": "message", "text": reply}


def handle_update(update: dict) -> None:
    """Processa e executa comandos vindos do update do Telegram."""
    message = update.get("message")
    if not message or "text" not in message:
        return
    
    chat_id = message["chat"]["id"]
    text = message["text"].strip()
    user = message["from"].get("username", "N/A")
    
    logger.info(f"[*] Mensagem recebida: '{text}' | Chat ID: {chat_id} | Usuário: @{user}")
    
    # Validação de segurança do Chat ID autorizado
    if AUTHORIZED_CHAT_ID is not None and chat_id != AUTHORIZED_CHAT_ID:
        logger.warning(f"⚠️ Acesso bloqueado para Chat ID: {chat_id} (Usuário: @{user})")
        send_message(chat_id, "⚠️ Acesso não autorizado. Suas credenciais foram registradas no log do Firewall.")
        return

    # Validação de atividade do Loop do Claw para comandos de controle
    is_control_cmd = any(text.startswith(cmd) for cmd in ["/pause", "/resume", "/stop", "/set_goal", "/click", "/type", "/run_playbook"])
    if is_control_cmd and not is_claw_loop_online():
        logger.warning(f"⚠️ Comando de controle '{text.split()[0]}' rejeitado: Claw Loop está offline.")
        send_message(
            chat_id, 
            "⚠️ *Comando Rejeitado: O robô Claw está OFFLINE.*\n\n"
            "Ative o loop do robô no servidor antes de interagir:\n"
            "`python .mecha/ops/patterns/claw_loop.py --target \"Window Name\"`"
        )
        return

    # Processamento de comandos
    if text.startswith("/start"):
        help_text = (
            "🤖 **Mecha Huggs Workforce Studio (HWorkforceStudio) — Claw Control** 🤖\n\n"
            "Comandos do Loop:\n"
            "📊 `/status` - Mostra o estado atual do robô e tela ativa\n"
            "⏸️ `/pause` - Pausa temporariamente o loop do Claw\n"
            "▶️ `/resume` - Retoma a execução do loop do Claw\n"
            "🛑 `/stop` - Aborta imediatamente a execução\n"
            "🎯 `/set_goal <instrução>` - Atualiza a meta cognitiva da IA\n"
            "🖱️ `/click <x> <y>` - Efetua um clique manual na tela\n"
            "⌨️ `/type <texto>` - Simula digitação na janela atual\n\n"
            "Novas Integrações:\n"
            "🔍 `/rag <query>` - Consulta a base vetorial local do Qdrant\n"
            "⚖️ `/tribunal <tema>` - Evoca debate do Tribunal Hermes\n"
            "🎬 `/run_playbook <nome>` - Executa um playbook de RPA\n"
            "🌸 `/task <add|done|clear|list>` - Gerencia tarefas da Amanda"
        )
        send_message(chat_id, help_text)
    
    elif text.startswith("/status"):
        if not os.path.exists(STATUS_FILE):
            send_message(chat_id, "❌ Nenhum status registrado. O robô Claw parece offline.")
            return
        
        mtime = os.path.getmtime(STATUS_FILE)
        age = time.time() - mtime
        status_indicator = "🟢 ONLINE" if age < 45 else "🔴 OFFLINE / INATIVO"
        
        try:
            with open(STATUS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            send_message(chat_id, f"❌ Erro ao ler arquivo de status: {e}")
            return
            
        msg = (
            f"🤖 **Status do MECHA Claw**: {status_indicator}\n"
            f"⏱️ *Atualizado há*: {int(age)} segundos\n"
            f"🏁 *Estado do Loop*: `{data.get('loop_state', 'unknown')}`\n"
            f"📊 *Ciclo*: `{data.get('step', 0)}` / `{data.get('max_steps', 0)}`\n"
            f"🖼️ *Janela*: `{data.get('last_seen_title', 'N/A')}`\n"
            f"🎯 *Objetivo Ativo*: `{data.get('current_goal', 'Sem meta')}`\n"
        )
        
        thumbnail_path = data.get("last_thumbnail")
        if thumbnail_path and os.path.exists(thumbnail_path):
            send_photo(chat_id, thumbnail_path, msg)
        else:
            send_message(chat_id, msg)

    elif text.startswith("/pause"):
        send_preempt_command("pause")
        send_message(chat_id, "⏸️ Solicitando PAUSA ao loop do Claw...")
        
    elif text.startswith("/resume"):
        send_preempt_command("resume")
        send_message(chat_id, "▶️ Solicitando RETOMADA ao loop do Claw...")
        
    elif text.startswith("/stop"):
        send_preempt_command("stop")
        send_message(chat_id, "🛑 Solicitando PARADA DE EMERGÊNCIA imediata!")
        
    elif text.startswith("/set_goal"):
        goal = text[len("/set_goal"):].strip()
        if not goal:
            send_message(chat_id, "❌ Uso correto: `/set_goal <sua nova meta>`")
            return
        send_preempt_command("set_goal", {"goal": goal})
        send_message(chat_id, f"🎯 Atualizando objetivo para: `{goal}`")

    elif text.startswith("/click"):
        parts = text.split()
        if len(parts) < 3:
            send_message(chat_id, "❌ Uso correto: `/click <x> <y>`")
            return
        try:
            x, y = int(parts[1]), int(parts[2])
        except ValueError:
            send_message(chat_id, "❌ Coordenadas precisam ser números inteiros.")
            return
        send_preempt_command("click", {"x": x, "y": y})
        send_message(chat_id, f"🖱️ Solicitando clique remoto em ({x}, {y})...")

    elif text.startswith("/type"):
        val = text[len("/type"):].strip()
        if not val:
            send_message(chat_id, "❌ Uso correto: `/type <texto a digitar>`")
            return
        send_preempt_command("type", {"text": val})
        send_message(chat_id, f"⌨️ Solicitando digitação de: `{val}`")

    # --- Comandos Integrados ---
    elif text.startswith("/rag"):
        query = text[len("/rag"):].strip()
        if not query:
            send_message(chat_id, "❌ Uso correto: `/rag <termo de busca>`")
            return
        threading.Thread(target=run_rag_thread, args=(chat_id, query), daemon=True).start()

    elif text.startswith("/tribunal"):
        topic = text[len("/tribunal"):].strip()
        if not topic:
            send_message(chat_id, "❌ Uso correto: `/tribunal <tema para debate>`")
            return
        threading.Thread(target=run_tribunal_thread, args=(chat_id, topic), daemon=True).start()

    elif text.startswith("/run_playbook"):
        name = text[len("/run_playbook"):].strip()
        if not name:
            send_message(chat_id, "❌ Uso correto: `/run_playbook <nome_do_playbook>`")
            return
        threading.Thread(target=run_playbook_thread, args=(chat_id, name), daemon=True).start()

    elif text.startswith("/task") or text.startswith("/todo"):
        res = handle_task_command(text)
        send_message(chat_id, res.get("text", ""))
        
    else:
        logger.info(f"[*] Mensagem não tratada de Chat ID {chat_id}: '{text}'")
        send_message(chat_id, "Olá! Eu sou o assistente do Claw. Digite `/start` para ver a lista de comandos.")


# --- Pydantic Models for OpenAPI / Swagger ---

class EventPublishRequest(BaseModel):
    topic: str = Field(..., description="Tópico do evento no barramento", examples=["node.select"])
    sender: str = Field(..., description="Emissor do evento", examples=["test_suite"])
    timestamp: int = Field(..., description="Carimbo de data/hora Unix em milissegundos", examples=[1700000000000])
    payload: Dict[str, Any] = Field(..., description="Dados payload específicos do evento", examples=[{"node_id": "dashboard", "title": "Dashboard Admin"}])

class EventPublishResponse(BaseModel):
    ok: bool = Field(..., description="Status indicando sucesso")
    message: str = Field(..., description="Mensagem de retorno")

class APIErrorResponse(BaseModel):
    error: str = Field(..., description="Mensagem detalhada do erro")

class EventPollResponse(BaseModel):
    events: List[Dict[str, Any]] = Field(..., description="Eventos transmitidos no barramento")

class APIHealthResponse(BaseModel):
    product: str = Field(..., description="Nome do produto")
    slug: str = Field(..., description="Slug de identificação do produto")
    status: str = Field(..., description="Overall bot server health status")
    claw_loop: str = Field(..., description="Status de conexão com o loop do robô Claw")

class TaskItem(BaseModel):
    id: int = Field(..., description="Identificador único da tarefa")
    description: str = Field(..., description="Descrição da tarefa")
    status: str = Field(..., description="Estado atual da tarefa (pending/completed)")
    created_at: str = Field(..., description="Data de criação da tarefa")
    completed_at: str = Field(..., description="Data de conclusão da tarefa ou vazio")

class TaskCreateRequest(BaseModel):
    description: str = Field(..., description="Descrição da nova tarefa a ser adicionada", examples=["Sincronizar logs da base do Qdrant"])

class TaskCreateResponse(BaseModel):
    ok: bool = Field(..., description="Status de sucesso")
    result: str = Field(..., description="Mensagem descritiva resultante")

class TaskDoneRequest(BaseModel):
    id: int = Field(..., description="ID numérico da tarefa a ser concluída", examples=[1])

class PreemptCommandRequest(BaseModel):
    action: str = Field(..., description="Comando de ação de controle (click, type, set_goal, pause, resume, stop)", examples=["click"])
    params: Dict[str, Any] = Field(default={}, description="Parâmetros adicionais para a ação", examples=[{"x": 100, "y": 200}])

class PreemptCommandResponse(BaseModel):
    ok: bool = Field(..., description="Status de sucesso")

app = FastAPI(title="Mecha Huggs Workforce Studio Backend", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["X-Download-Options"] = "noopen"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net; "
        "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
        "img-src 'self' data: https://fastapi.tiangolo.com; "
        "frame-ancestors 'none';"
    )
    return response

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Retorna HTTP 400 em vez de 422 para manter compatibilidade com testes legados."""
    return JSONResponse(
        status_code=400,
        content={"error": str(exc.errors())}
    )

@app.websocket("/ws/bus")
async def websocket_endpoint(websocket: WebSocket):
    global _UVICORN_LOOP
    _UVICORN_LOOP = asyncio.get_running_loop()
    await websocket.accept()
    event_hub.subscribe(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            if isinstance(data, dict):
                action = data.get("action")
                if action == "publish":
                    event = data.get("event")
                    if isinstance(event, dict):
                        event_hub.publish(event)
                elif action == "subscribe":
                    logger.info(f"Cliente WS inscrito nos tópicos: {data.get('topics')}")
    except WebSocketDisconnect:
        pass
    except Exception as e:
        logger.error(f"Erro no WebSocket do barramento: {e}")
    finally:
        event_hub.unsubscribe(websocket)

@app.post("/api/bus/publish", response_model=EventPublishResponse, responses={400: {"model": APIErrorResponse}}, tags=["Event Bus"], summary="Publicar Evento", description="Publica um novo evento envelope estruturado no barramento de eventos.")
async def publish_event(event: EventPublishRequest):
    event_dict = event.model_dump()
    success, msg = event_hub.publish(event_dict)
    if success:
        return {"ok": True, "message": msg}
    else:
        return Response(content=json.dumps({"error": msg}), media_type="application/json", status_code=400)

@app.get("/api/bus/poll", response_model=EventPollResponse, tags=["Event Bus"], summary="Poll de Eventos", description="Busca eventos publicados a partir de um timestamp inicial em milissegundos.")
async def poll_events(since: Optional[int] = 0):
    events = event_hub.get_events(since)
    return {"events": events}

@app.get("/api/health", response_model=APIHealthResponse, tags=["Health & Status"], summary="Health Check", description="Retorna informações de saúde do servidor HTTP e da thread Claw.")
async def api_health():
    try:
        fresh = os.path.exists(STATUS_FILE) and (time.time() - os.path.getmtime(STATUS_FILE) < 45)
    except OSError:
        fresh = False
    return {
        "product": PRODUCT_NAME,
        "slug": PRODUCT_SLUG,
        "status": "online",
        "claw_loop": "online" if fresh else "offline",
    }

@app.get("/api/status", tags=["Health & Status"], summary="Obter Status do Robô", description="Retorna o arquivo JSON de telemetria atualizado pelo robô Claw.")
async def api_status():
    if os.path.exists(STATUS_FILE):
        try:
            with open(STATUS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            return {"error": str(e)}
    else:
        return {"error": "No status found", "loop_state": "offline"}

@app.get("/api/tasks", response_model=List[TaskItem], tags=["Amanda Tasks"], summary="Listar Tarefas", description="Retorna todas as tarefas registradas da Amanda (ativas e arquivadas).")
async def api_get_tasks():
    tasks_file = os.path.join(BASE_DIR, "logs", "amanda_tasks.json")
    if os.path.exists(tasks_file):
        try:
            with open(tasks_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            return []
    return []

@app.post("/api/tasks", response_model=TaskCreateResponse, responses={400: {"model": APIErrorResponse}}, tags=["Amanda Tasks"], summary="Adicionar Tarefa", description="Adiciona uma nova tarefa pendente para Amanda.")
async def api_add_task(payload: TaskCreateRequest):
    description = payload.description.strip()
    if not description:
        return Response(content=json.dumps({"error": "Missing description"}), media_type="application/json", status_code=400)
    res = handle_task_command(f"/task add {description}")
    return {"ok": True, "result": res.get("text", "")}

@app.post("/api/tasks/done", response_model=TaskCreateResponse, responses={400: {"model": APIErrorResponse}}, tags=["Amanda Tasks"], summary="Concluir Tarefa", description="Marca uma tarefa como concluída a partir do ID fornecido.")
async def api_complete_task(payload: TaskDoneRequest):
    task_id = payload.id
    res = handle_task_command(f"/task done {task_id}")
    return {"ok": True, "result": res.get("text", "")}

@app.post("/api/tasks/clear", response_model=TaskCreateResponse, responses={500: {"model": APIErrorResponse}}, tags=["Amanda Tasks"], summary="Limpar Fila", description="Remove tarefas concluídas da fila da Amanda.")
async def api_clear_tasks():
    try:
        res = handle_task_command("/task clear")
        return {"ok": True, "result": res.get("text", "")}
    except Exception as e:
        return Response(content=json.dumps({"error": str(e)}), media_type="application/json", status_code=500)

@app.post("/api/preempt", response_model=PreemptCommandResponse, responses={400: {"model": APIErrorResponse}}, tags=["Control & RPA"], summary="Injetar Comando", description="Injeta um comando de controle (click, type, etc.) a ser processado pelo Claw.")
async def api_preempt(payload: PreemptCommandRequest):
    action = payload.action.strip()
    params = payload.params
    send_preempt_command(action, params)
    return {"ok": True}

app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")

def is_port_available(port: int) -> bool:
    if not (0 <= port <= 65535):
        return False
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(("0.0.0.0", port))
            return True
        except OSError:
            return False

def start_http_server() -> None:
    """Thread que inicializa o servidor HTTP/WS do dashboard do MECHA, buscando portas livres."""
    os.chdir(STATIC_DIR)
    ports_to_try = [8585, 8282, 8181, 9999]
    active_port = None
    
    for port in ports_to_try:
        if is_port_available(port):
            active_port = port
            break
            
    if active_port is None:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("0.0.0.0", 0))
            active_port = s.getsockname()[1]
            
    logger.info(f"Inicializando {PRODUCT_NAME} ({PRODUCT_SLUG}) — Dashboard HTTP/WS em http://localhost:{active_port} ...")
    try:
        uvicorn.run(app, host="0.0.0.0", port=active_port, log_level="warning")
    except Exception as e:
        logger.critical(f"CRITICAL: Servidor HTTP falhou com erro: {e}")
        raise



def main():
    # Inicializa o servidor HTTP do dashboard em segundo plano (Sempre ativo!)
    http_thread = threading.Thread(target=start_http_server, daemon=True)
    http_thread.start()
    
    # Valida a autenticidade do token do Telegram
    is_token_valid = False
    if TOKEN:
        try:
            r = requests.get(f"https://api.telegram.org/bot{TOKEN}/getMe", timeout=3)
            if r.status_code == 200:
                is_token_valid = True
        except Exception:
            pass

    if not is_token_valid:
        logger.warning("==========================================================================")
        logger.warning(" [⚠️ AVISO] Ambas as chaves de API do Telegram (T1 e T2) são inválidas ou")
        logger.warning(" retornaram 401 (Não autorizado). O Polling do Telegram estará desativado.")
        logger.warning(" O Servidor HTTP do Dashboard CONTINUARÁ rodando em http://localhost:8585.")
        logger.warning("==========================================================================")
        # Mantém a thread principal viva para o Dashboard continuar servindo as requisições
        while True:
            time.sleep(3600)
        
    logger.info("Inicializando MECHA Telegram Bot (API Requests síncrono)...")
    
    # Limpa atualizações anteriores para não reprocessar mensagens velhas
    offset = 0
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
        requests.get(url, params={"offset": -1, "timeout": 1}, timeout=5)
    except Exception as e:
        logger.error(f"Erro ao limpar fila inicial: {_scrub_token(e)}")

    logger.info("Bot ativo e em modo polling síncrono. Ouvindo mensagens...")
    
    while True:
        try:
            url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
            r = requests.get(url, params={"offset": offset, "timeout": 20}, timeout=25)
            if r.status_code == 200:
                data = r.json()
                if data.get("ok"):
                    for update in data["result"]:
                        offset = update["update_id"] + 1
                        handle_update(update)
            else:
                logger.error(f"Erro na API getUpdates: status {r.status_code}")
                time.sleep(5)
        except KeyboardInterrupt:
            logger.info("Polling interrompido pelo operador.")
            break
        except Exception as e:
            logger.error(f"Erro no loop de polling: {_scrub_token(e)}")
            time.sleep(5)

if __name__ == "__main__":  # pragma: no cover
    main()
