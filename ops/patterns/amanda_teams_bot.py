import os
import sys
import json
import hmac
import hashlib
import base64
import time
import logging
import asyncio
import re
import threading
import requests
from typing import Dict, Any, List, Optional, Tuple
from fastapi import FastAPI, Request, Header, HTTPException, BackgroundTasks
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.concurrency import run_in_threadpool
import uvicorn
from pydantic import BaseModel, Field

# Alias semântico para um item de tarefa persistido
Task = Dict[str, Any]

# Setup paths (PyInstaller-aware)
def _resolve_base_dirs() -> Tuple[str, str, str]:
    """Resolve os diretórios PATTERNS/OPS/BASE.

    Sob PyInstaller (sys.frozen), `__file__` aponta para o diretório temporário
    `_MEIPASS`, o que quebra a resolução relativa e faz com que .env, logs e
    tasks sejam gravados em um diretório efêmero (perdido ao encerrar). Quando
    empacotado, ancoramos os caminhos no diretório do executável real.
    """
    if getattr(sys, "frozen", False):
        exe_dir = os.path.dirname(os.path.abspath(sys.executable))
        ops_dir = os.path.dirname(exe_dir)
        base_dir = os.path.dirname(ops_dir)
        return exe_dir, ops_dir, base_dir
    patterns_dir = os.path.dirname(os.path.abspath(__file__))
    ops_dir = os.path.dirname(patterns_dir)
    base_dir = os.path.dirname(ops_dir)
    return patterns_dir, ops_dir, base_dir


PATTERNS_DIR, OPS_DIR, BASE_DIR = _resolve_base_dirs()

# Escape hatch: permite fixar a raiz de dados via env (útil em onefile/Docker)
BASE_DIR = os.environ.get("MECHA_BASE_DIR", BASE_DIR)
OPS_DIR = os.environ.get("MECHA_OPS_DIR", OPS_DIR)

# Em build congelado os módulos auxiliares são embutidos; só ajustamos sys.path
# durante a execução a partir do fonte.
if not getattr(sys, "frozen", False):
    sys.path.insert(0, PATTERNS_DIR)
    _orch_src = os.path.join(os.path.dirname(BASE_DIR), "ORCHESTRATOR_CORE", "src")
    if os.path.exists(_orch_src):
        sys.path.insert(0, _orch_src)



# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger("AmandaTeamsAgent")

# Força saída UTF-8 em terminais Windows (evita UnicodeEncodeError com CP1252).
# Sob PyInstaller --noconsole, sys.stdout/err podem ser None; sob redirecionamento
# podem não ser um TextIOWrapper. Por isso protegemos a chamada.
for _stream_name in ("stdout", "stderr"):
    _stream = getattr(sys, _stream_name, None)
    if _stream is not None and hasattr(_stream, "reconfigure"):
        try:
            _stream.reconfigure(encoding="utf-8")
        except Exception:  # pragma: no cover - depende do ambiente de runtime
            pass

# Load environment
def load_dotenv() -> None:
    env_path = os.path.join(OPS_DIR, ".env")
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

load_dotenv()

# Setup central status file path for Dashboard logs
STATUS_FILE = os.path.join(OPS_DIR, "logs", "claw_status.json")

# Configs
PORT = int(os.environ.get("TEAMS_PORT", "8686"))
SHARED_SECRET = os.environ.get("TEAMS_SHARED_SECRET", "")
OPENROUTER_KEY = os.environ.get("OPENROUTER_API_KEY", "")
MODEL_AMANDA = "meta-llama/llama-3.3-70b-instruct"
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")
LLM_TIMEOUT = int(os.environ.get("AMANDA_LLM_TIMEOUT", "20"))
# Fail-closed por padrão: sem SHARED_SECRET o webhook é recusado, a menos que
# o operador habilite explicitamente o modo inseguro (somente dev/teste local).
ALLOW_INSECURE = os.environ.get("MECHA_ALLOW_INSECURE", "").strip().lower() in ("1", "true", "yes", "on")

if not SHARED_SECRET:
    if ALLOW_INSECURE:
        logger.warning(
            "TEAMS_SHARED_SECRET ausente e MECHA_ALLOW_INSECURE habilitado — o webhook "
            "aceitará requisições NÃO assinadas (modo dev). NÃO utilize assim em produção."
        )
    else:
        logger.error(
            "TEAMS_SHARED_SECRET ausente — o webhook /webhook/teams responderá 503 (fail-closed). "
            "Defina TEAMS_SHARED_SECRET ou, apenas para dev local, MECHA_ALLOW_INSECURE=1."
        )


def _safe_chat_id() -> int:
    """Converte TELEGRAM_CHAT_ID em int de forma resiliente (evita 500 no webhook)."""
    raw = os.environ.get("TELEGRAM_CHAT_ID", "")
    try:
        return int(raw)
    except (TypeError, ValueError):
        return 0


# Load dependencies safely
try:
    from antigravity_sdk.rag_client import QdrantNeo4jRagClient
    rag_client = QdrantNeo4jRagClient()
    logger.info("QdrantNeo4jRagClient (RAG Híbrido) carregado com sucesso.")
except Exception as e:
    logger.warning(f"Erro ao carregar QdrantNeo4jRagClient: {e}. Tentando fallback local para QdrantRAGClient...")
    try:
        from qdrant_client_helper import QdrantRAGClient
        rag_client = QdrantRAGClient()
        logger.info("QdrantRAGClient local carregado com sucesso como fallback.")
    except Exception as e_local:
        rag_client = None
        logger.error(f"Erro crítico: Ambos os clientes Qdrant (Híbrido e Local) falharam ao carregar. RAG desativado. Detalhes: {e_local}")

try:
    from awesome_bots_orchestrator import AwesomeBotsOrchestrator
    orchestrator = AwesomeBotsOrchestrator(BASE_DIR)
    logger.info("AwesomeBotsOrchestrator carregado com sucesso.")
except Exception as e:
    orchestrator = None
    logger.error(f"Erro ao carregar AwesomeBotsOrchestrator: {e}")

try:
    from code_squad_runner import CodeSquadRunner
    dev_squad_runner = CodeSquadRunner(BASE_DIR)
    logger.info("CodeSquadRunner carregado com sucesso.")
except Exception as e:
    dev_squad_runner = None
    logger.error(f"Erro ao carregar CodeSquadRunner: {e}")

try:
    from qa_squad_runner import QASquadRunner
    qa_squad_runner = QASquadRunner(BASE_DIR)
    logger.info("QASquadRunner carregado com sucesso.")
except Exception as e:
    qa_squad_runner = None
    logger.error(f"Erro ao carregar QASquadRunner: {e}")

app = FastAPI(title="Amanda MS Teams Agent", version="1.0.0")

from fastapi.middleware.cors import CORSMiddleware
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

# Serializa o acesso de leitura/escrita aos JSONs locais (tasks/status) no processo.
_FILE_LOCK = threading.RLock()


def _read_json(path: str, default: Any) -> Any:
    """Lê um JSON de forma tolerante a falhas, retornando `default` em erro."""
    if not os.path.exists(path):
        return default
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError, UnicodeDecodeError) as e:
        logger.error(f"Falha ao ler JSON {path}: {e}")
        return default


def _atomic_write_json(path: str, data: Any) -> None:
    """Escreve JSON de forma atômica (tmp + os.replace) para evitar corrupção e
    leituras parciais sob concorrência. Mantém UTF-8 sem escapes (ensure_ascii=False)."""
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    tmp_path = f"{path}.{os.getpid()}.tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp_path, path)  # atômico no mesmo filesystem (Windows e POSIX)


def log_event_to_dashboard(level: str, msg: str) -> None:
    """Registra eventos de Amanda no painel MECHA (telemetria rolante de 30 itens)."""
    with _FILE_LOCK:
        data = _read_json(STATUS_FILE, {})
        if not isinstance(data, dict):
            data = {}
        events = data.get("events", [])
        if not isinstance(events, list):
            events = []

        events.append({
            "time": time.strftime("%H:%M:%S"),
            "level": level,  # info, ok, warn, danger
            "msg": f"[Amanda Teams] {msg}",
            "id": f"amanda_{time.time()}_{abs(hash(msg))}",
        })
        data["events"] = events[-30:]

        try:
            _atomic_write_json(STATUS_FILE, data)
        except OSError as e:
            logger.error(f"Erro ao logar no dashboard: {e}")

def verify_teams_signature(body: bytes, authorization: Optional[str]) -> bool:
    """Verifica a assinatura HMAC-SHA256 enviada pelo Microsoft Teams."""
    if not SHARED_SECRET:
        # Fail-closed: só aceita sem assinatura quando o modo inseguro é explícito.
        return ALLOW_INSECURE
    if not authorization:
        logger.warning("Verificação de assinatura falhou: Cabeçalho de autorização ausente.")
        return False
    try:
        key = base64.b64decode(SHARED_SECRET)
        computed_hmac = hmac.new(key, body, hashlib.sha256).digest()
        computed_signature = base64.b64encode(computed_hmac).decode("utf-8")
        actual_signature = authorization.replace("HMAC ", "").strip()
        return hmac.compare_digest(computed_signature, actual_signature)
    except Exception as e:
        logger.error(f"Falha na verificação de assinatura: {e}")
        return False

def clean_teams_mention(text: str) -> str:
    """Remove tags html de menção do Teams (ex: <at id="0">Amanda</at>).

    O Teams emite a tag <at> com atributos (id, etc.), então o padrão precisa
    aceitar atributos e quebras de linha.
    """
    clean = re.sub(r"<at\b[^>]*>.*?</at>", "", text, flags=re.IGNORECASE | re.DOTALL)
    return clean.strip()

def publish_to_bus(topic: str, payload: dict) -> None:
    try:
        url = "http://localhost:8585/api/bus/publish"
        event = {
            "topic": topic,
            "sender": "amanda_teams_bot",
            "timestamp": int(time.time() * 1000),
            "payload": payload
        }
        requests.post(url, json=event, timeout=1.5)
    except Exception as e:
        logger.error(f"Erro ao publicar evento no bus: {e}")

def send_telegram_notification(message: str, parse_mode: Optional[str] = None) -> None:
    """Envia mensagem ao Telegram em blocos seguros.

    `parse_mode` é None por padrão: os relatórios de DevSquad/QASquad embutem código
    bruto (com `_`, `*`, crases) que quebra o parser legado "Markdown" do Telegram e
    faz a API retornar 400, descartando a notificação silenciosamente. Texto puro é
    entregue de forma confiável.
    """
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        return
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    # Limite do Telegram é 4096 chars; fatiamos com margem.
    chunks = [message[i:i + 3900] for i in range(0, len(message), 3900)] or [""]
    for chunk in chunks:
        payload: Dict[str, Any] = {"chat_id": chat_id, "text": chunk}
        if parse_mode:
            payload["parse_mode"] = parse_mode
        try:
            requests.post(url, json=payload, timeout=8)
        except requests.RequestException as e:
            logger.error(f"Erro ao enviar notificação ao Telegram: {e}")

def run_async_tribunal(topic: str, chat_id: int) -> None:
    """Executa o debate do Tribunal Hermes em background e publica o veredito no Telegram."""
    if not orchestrator:
        logger.error("AwesomeBotsOrchestrator não inicializado!")
        send_telegram_notification(f"❌ [Tribunal Hermes] Orchestrator indisponível para o tópico: {topic}")
        return
    try:
        # Cria um novo event loop para rodar a tarefa assíncrona na thread em background
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        debate = loop.run_until_complete(orchestrator.run_tribunal(topic))
        loop.close()

        # run_tribunal retorna {"warlock", "amanda", "shura"}; o veredito do Shura
        # contém "[1]" (aprovar) ou "[0]" (abortar).
        debate = debate or {}
        veredito = str(debate.get("shura", "")).strip()
        aprovado = "[1]" in veredito
        status_txt = "APROVADO [1]" if aprovado else "REJEITADO [0]"
        level = "ok" if aprovado else "danger"

        msg = (
            f"⚖️ [TRIBUNAL HERMES — VEREDITO: {status_txt}]\n\n"
            f"Tópico: {topic}\n\n"
            f"😈 Warlock (Acusação/Segurança):\n{debate.get('warlock', '—')}\n\n"
            f"🛡️ Amanda (Defesa/Conformidade):\n{debate.get('amanda', '—')}\n\n"
            f"👑 Shura 255 (Juiz/Lead):\n{veredito or '—'}"
        )
        send_telegram_notification(msg)
        log_event_to_dashboard(level, f"Tribunal finalizado via Teams. Veredito: {status_txt}")
    except Exception as e:
        logger.error(f"Erro no thread do Tribunal Hermes: {e}")
        log_event_to_dashboard("danger", f"Erro na execução do Tribunal (Teams): {e}")
        send_telegram_notification(f"❌ [Tribunal Hermes] Erro ao processar '{topic}': {e}")

def run_async_dev_squad(prompt: str, chat_id: int) -> None:
    """Executa o pipeline do DevSquad em background e notifica via Telegram."""
    if not dev_squad_runner:
        logger.error("CodeSquadRunner não inicializado!")
        return
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        results = loop.run_until_complete(dev_squad_runner.run_spec_driven_dev(prompt))
        loop.close()
        
        # Formatar mensagem final para o Telegram
        msg = (
            f"🛠️ **[DevSquad - Pipeline Spec-Driven Concluído]**\n\n"
            f"**Meta:** {prompt}\n\n"
            f"**1. ESPECIFICAÇÃO (Uncle Bob):**\n"
            f"```markdown\n{results['specification'][:800]}...\n```\n\n"
            f"**2. IMPLEMENTAÇÃO (Linus):**\n"
            f"```python\n{results['implementation'][:800]}...\n```\n\n"
            f"**3. TESTES (Kent Beck):**\n"
            f"```python\n{results['tests'][:800]}...\n```\n\n"
            f"**4. AUDITORIA (Mitnick):**\n"
            f"```text\n{results['audit_report']}\n```"
        )
        send_telegram_notification(msg)
    except Exception as e:
        logger.error(f"Erro no thread do DevSquad: {e}")

def run_async_qa_squad(source_path: str, tests_path: str, chat_id: int) -> None:
    """Executa o pipeline do QASquad em background e notifica via Telegram."""
    if not qa_squad_runner:
        logger.error("QASquadRunner não inicializado!")
        return
    try:
        # Resolve caminhos relativos ao workspace_root
        abs_source = os.path.join(BASE_DIR, source_path) if not os.path.isabs(source_path) else source_path
        abs_tests = ""
        if tests_path:
            abs_tests = os.path.join(BASE_DIR, tests_path) if not os.path.isabs(tests_path) else tests_path
            
        if not os.path.exists(abs_source):
            send_telegram_notification(f"❌ **[QASquad - Erro]** Arquivo fonte `{source_path}` não foi localizado.")
            return
            
        with open(abs_source, "r", encoding="utf-8") as f:
            source_content = f.read()
            
        test_content = ""
        if abs_tests and os.path.exists(abs_tests):
            with open(abs_tests, "r", encoding="utf-8") as ft:
                test_content = ft.read()
                
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        results = loop.run_until_complete(qa_squad_runner.run_qa_audit(source_content, test_content))
        loop.close()
        
        # Formatar mensagem final para o Telegram
        msg = (
            f"🧪 **[QASquad - Relatório de Auditoria de QA]**\n\n"
            f"**Arquivo Fonte:** `{source_path}`\n"
            f"**Arquivo Testes:** `{tests_path if tests_path else 'Não fornecido'}`\n\n"
            f"**1. ESTILO & LINTS (SonarBot):**\n"
            f"```text\n{results['lint_report'][:600]}...\n```\n\n"
            f"**2. PROJETO & CODE SMELLS (Martin Fowler):**\n"
            f"```text\n{results['design_report'][:600]}...\n```\n\n"
            f"**3. PERFORMANCE & RECURSOS (LocustBot):**\n"
            f"```text\n{results['perf_report'][:600]}...\n```\n\n"
            f"**4. VEREDITO FINAL (Kent Beck):**\n"
            f"```text\n{results['qa_final_report']}\n```"
        )
        send_telegram_notification(msg)
    except Exception as e:
        logger.error(f"Erro no thread do QASquad: {e}")

def query_openrouter_amanda(query: str, retrieved_context: str) -> str:
    """Gera resposta da Amanda via OpenRouter (com fallback mockado)."""
    system_prompt = (
        "Você é a Shadow Processor (Amanda), um agente de conformidade e defesa cognitiva do ecossistema MECHA.\n"
        "Seu papel é responder dúvidas de forma prestativa, extremamente organizada, lógica e limpa.\n"
        "Utilize termos de Genshin Impact/Honkai (como 'Irminsul', 'Terminal Akasha') sutilmente para ilustrar os conceitos do sistema.\n"
        "Responda utilizando o contexto da base de dados vetorial (RAG) fornecido abaixo sempre que relevante.\n"
        "Seja direta, técnica e evite preâmbulos longos."
    )
    
    user_content = (
        f"CONTEXTO RECUPERADO (RAG - IRMINSUL):\n{retrieved_context}\n\n"
        f"DÚVIDA DO OPERADOR:\n{query}"
    )

    if not OPENROUTER_KEY or OPENROUTER_KEY == "MOCK_KEY":
        time.sleep(1.2)  # Simula latência de chamada
        return (
            "🌸 *[Amanda - Shadow Processor]*\n\n"
            "Saudações, Operador. Acessando os registros do *Terminal Akasha*...\n"
            f"Com base na minha busca local, aqui está a diretriz para a sua solicitação sobre `{query}`:\n\n"
            "• Os Ghost Workers operam sob o Ring 0 com persistência local em SQLite.\n"
            "• As políticas de conformidade do tribunal exigem validação estrita de tipos.\n\n"
            "Se precisar de uma auditoria formal, utilize `/tribunal <tópico>`."
        )

    headers = {
        "Authorization": f"Bearer {OPENROUTER_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/google/antigravity",
        "X-Title": "Amanda MECHA Agent"
    }
    payload = {
        "model": MODEL_AMANDA,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content}
        ],
        "temperature": 0.5,
        "max_tokens": 1000
    }
    
    try:
        resp = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload, timeout=LLM_TIMEOUT)
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]
    except Exception as e:
        logger.error(f"Erro ao chamar OpenRouter: {e}")
        return f"⚠️ *[Amanda - Falha Akasha]*: Não consegui me conectar a Irminsul para processar a resposta: {e}"


def handle_task_command(text: str) -> Dict[str, str]:
    """Gerencia a stack de tarefas da Amanda (/task, /todo).

    Toda a sequência ler-modificar-gravar roda sob _FILE_LOCK e usa escrita
    atômica, evitando race conditions e corrupção do amanda_tasks.json. O espelho
    Markdown (AMANDA_TASKS.md) é regenerado a cada mutação.
    """
    prefix = "/task" if text.startswith("/task") else "/todo"
    rest = text[len(prefix):].strip()
    parts = rest.split(maxsplit=1)
    action = parts[0].lower() if parts else "list"
    args = parts[1].strip() if len(parts) > 1 else ""

    tasks_file = os.path.join(OPS_DIR, "logs", "amanda_tasks.json")
    tasks_md = os.path.join(BASE_DIR, "AMANDA_TASKS.md")

    def render_markdown(task_list: List[Task]) -> str:
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

    def persist(task_list: List[Task]) -> None:
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

    with _FILE_LOCK:
        tasks = _read_json(tasks_file, [])
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


# --- Pydantic Models for OpenAPI / Swagger ---

class TeamsHealthResponse(BaseModel):
    status: str = Field(..., description="Status geral do agente Teams")
    agent: str = Field(..., description="Nome do agente")
    qdrant_connected: bool = Field(..., description="Status da conexão com o cliente RAG Qdrant")
    orchestrator_loaded: bool = Field(..., description="Status de carregamento do AwesomeBotsOrchestrator")

class TeamsMessageFrom(BaseModel):
    name: str = Field(default="Operador", description="Nome visível do remetente")
    id: Optional[str] = Field(default=None, description="Identificador único do remetente")

class TeamsWebhookRequest(BaseModel):
    type: str = Field(default="message", description="Tipo de atividade do Teams (ex: message)")
    text: str = Field(..., description="Conteúdo textual da mensagem enviada", examples=["/task list"])
    from_user: TeamsMessageFrom = Field(default_factory=TeamsMessageFrom, alias="from", description="Perfil do remetente da mensagem")

class TeamsWebhookResponse(BaseModel):
    type: str = Field(default="message", description="Tipo de resposta enviada ao Teams")
    text: str = Field(..., description="Conteúdo textual da resposta")

class APIErrorResponse(BaseModel):
    error: str = Field(..., description="Detalhes da mensagem de erro")

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Retorna HTTP 400 em vez de 422 para manter compatibilidade com testes legados."""
    return JSONResponse(
        status_code=400,
        content={"error": str(exc.errors())}
    )


@app.get("/health", response_model=TeamsHealthResponse, tags=["Health"], summary="Health Check", description="Retorna o estado de saúde do bot Amanda Teams.")
def health() -> Dict[str, Any]:
    return {
        "status": "online",
        "agent": "Amanda Teams Bot",
        "qdrant_connected": rag_client is not None,
        "orchestrator_loaded": orchestrator is not None
    }


@app.post("/webhook/teams", response_model=TeamsWebhookResponse, responses={400: {"model": APIErrorResponse}, 401: {"model": APIErrorResponse}, 403: {"model": APIErrorResponse}, 503: {"model": APIErrorResponse}}, tags=["Webhook"], summary="Teams Webhook", description="Recebe mensagens do MS Teams, valida a assinatura HMAC e processa a requisição.")
async def teams_webhook(
    request: Request,
    background_tasks: BackgroundTasks,
    payload: TeamsWebhookRequest,
    authorization: Optional[str] = Header(None)
) -> Dict[str, Any]:
    body = await request.body()

    # 0. Fail-closed: recusa se o servidor está sem segredo e sem modo inseguro explícito.
    if not SHARED_SECRET and not ALLOW_INSECURE:
        raise HTTPException(
            status_code=503,
            detail="Webhook não configurado: defina TEAMS_SHARED_SECRET (ou MECHA_ALLOW_INSECURE=1 apenas para dev).",
        )

    # 1. Validar assinatura do Teams
    if SHARED_SECRET and not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    if not verify_teams_signature(body, authorization):
        logger.warning("Assinatura HMAC inválida ou recusada.")
        raise HTTPException(status_code=403, detail="Invalid HMAC signature")

    raw_text = payload.text or ""
    sender_name = payload.from_user.name if payload.from_user else "Operador"
    clean_text = clean_teams_mention(raw_text)

    logger.info(f"[Teams Webhook] Mensagem de @{sender_name}: '{clean_text}'")
    log_event_to_dashboard("info", f"Mensagem recebida de @{sender_name}: {clean_text[:40]}")

    # 3. Tratamento de Comandos Especiais (/tribunal e /dev)
    if clean_text.startswith("/tribunal"):
        topic = clean_text[len("/tribunal"):].strip()
        if not topic:
            return {
                "type": "message",
                "text": "❌ **Amanda:** Por favor, especifique o tópico para debate. Uso: `/tribunal <tema>`"
            }
        
        chat_id = _safe_chat_id()
        # Executa em background para responder ao Teams imediatamente e não estourar o limite de 5 segundos
        background_tasks.add_task(run_async_tribunal, topic, chat_id)
        
        reply = (
            f"⚖️ **Amanda (Shadow Processor):**\n"
            f"Entendido. Evocando o **Tribunal Hermes** em segundo plano para debater o tópico:\n"
            f"`{topic}`\n\n"
            f"O debate ocorrerá em paralelo. O veredito final do juiz Shura 255 será disparado para o canal de "
            f"Telegram e registrado na telemetria do Dashboard do MECHA."
        )
        log_event_to_dashboard("warn", f"Tribunal evocado via Teams para: {topic[:40]}")
        return {"type": "message", "text": reply}

    elif clean_text.startswith("/dev"):
        rest = clean_text[len("/dev"):].strip()
        if rest.startswith("spec-driven"):
            rest = rest[len("spec-driven"):].strip()
            
        prompt = rest
        if not prompt:
            return {
                "type": "message",
                "text": "❌ **Amanda:** Por favor, especifique o prompt para o DevSquad. Uso: `/dev [spec-driven] <prompt>`"
            }
        
        chat_id = _safe_chat_id()
        # Executa em background para responder ao Teams imediatamente e não estourar o limite de 5 segundos
        background_tasks.add_task(run_async_dev_squad, prompt, chat_id)
        
        reply = (
            f"🛠️ **Amanda (Shadow Processor):**\n"
            f"Entendido. Ativando o **DevSquad (Spec-Driven)** para a meta:\n"
            f"`{prompt}`\n\n"
            f"Os agentes Uncle Bob (Arquiteto), Linus (Implementador), Kent Beck (QA) e Mitnick (Auditor) "
            f"foram engajados. O progresso será logado no dashboard e o relatório final enviado ao Telegram."
        )
        log_event_to_dashboard("info", f"DevSquad ativado via Teams para: {prompt[:40]}")
        return {"type": "message", "text": reply}

    elif clean_text.startswith("/qa"):
        rest = clean_text[len("/qa"):].strip()
        parts = rest.split()
        if not parts:
            return {
                "type": "message",
                "text": "❌ **Amanda:** Por favor, especifique o arquivo de código fonte para auditar. Uso: `/qa <caminho_codigo> [caminho_testes]`"
            }
        source_path = parts[0]
        tests_path = parts[1] if len(parts) > 1 else ""
        
        chat_id = _safe_chat_id()
        # Executa em background para responder ao Teams imediatamente e não estourar o limite de 5 segundos
        background_tasks.add_task(run_async_qa_squad, source_path, tests_path, chat_id)
        
        reply = (
            f"🧪 **Amanda (Shadow Processor):**\n"
            f"Entendido. Ativando o **QASquad (Audit & Quality)** para auditar:\n"
            f"• Código Fonte: `{source_path}`\n"
            f"• Testes: `{tests_path if tests_path else 'Não fornecido'}`\n\n"
            f"Os agentes SonarBot (Lints), Martin Fowler (Refatoração), LocustBot (Perf) e Kent Beck (QA Lead) "
            f"foram ativados. O relatório consolidado de QA será enviado ao Telegram."
        )
        log_event_to_dashboard("info", f"QASquad ativado via Teams para: {source_path}")
        return {"type": "message", "text": reply}

    elif clean_text.startswith("/task") or clean_text.startswith("/todo"):
        return handle_task_command(clean_text)

    # 4. Fluxo Normal: Busca RAG no Qdrant + Resposta LLM
    context_str = ""
    if rag_client:
        try:
            # Offload para threadpool: a busca é I/O-bound e bloquearia o event loop.
            hits = await run_in_threadpool(lambda: rag_client.search(clean_text, limit=3))
            ctx_lines: List[str] = []
            for h in hits:
                meta = h.get("metadata") or {}
                fname = meta.get("file_name", "Sem Fonte")
                ctx_lines.append(f"- Hit [{fname}]: {h.get('text', '')}")
            context_str = "\n".join(ctx_lines)
            logger.info(f"Busca RAG concluída. Chunks retornados: {len(hits)}")
        except Exception as e:
            logger.error(f"Erro na busca RAG: {e}")
            context_str = f"Falha na busca RAG: {e}"

    # Executa a geração da resposta em threadpool para não bloquear o event loop
    # (requests é síncrono). Atenção: o Teams encerra ~5s; veja AMANDA_LLM_TIMEOUT
    # e a recomendação de migrar este fluxo para ack + push no Telegram.
    reply_text = await run_in_threadpool(query_openrouter_amanda, clean_text, context_str)
    
    log_event_to_dashboard("ok", f"Amanda respondeu a @{sender_name}")
    return {
        "type": "message",
        "text": reply_text
    }


def start_server() -> None:
    logger.info(f"Iniciando Amanda Teams Webhook na porta {PORT}...")
    uvicorn.run(app, host="0.0.0.0", port=PORT)


if __name__ == "__main__":  # pragma: no cover
    start_server()
