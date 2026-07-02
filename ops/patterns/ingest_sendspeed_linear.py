"""MECHA-S1-04 — Ingestao do conhecimento SendSpeed (Linear export) no Qdrant.

Clona o padrao de ingest_conversations_qdrant.py / qdrant_client_helper.py:
- Mesmo mecanismo de embeddings (sentence-transformers all-MiniLM-L6-v2,
  com fallback/forcamento mock via MECHA_FORCE_MOCK_EMBEDDINGS=1).
- Chunking com overlap identico ao ingester de conversas.
- Idempotente: IDs deterministicos uuid5(issue_id + chunk_n) com upsert.
- Scrub de segredos (tokens, api keys, senhas, connection strings) -> [REDACTED].
- Leitura tolerante a OneDrive: retry 1x em falha de I/O.

Collection alvo: sendspeed_knowledge
"""

import json
import os
import re
import sys
import time
import uuid
from typing import Any, Dict, List, Optional

# Setup paths to ensure we can import qdrant_client_helper
PATTERNS_DIR = os.path.dirname(os.path.abspath(__file__))
if PATTERNS_DIR not in sys.path:
    sys.path.append(PATTERNS_DIR)

from qdrant_client import QdrantClient  # noqa: E402
from qdrant_client.models import Distance, PointStruct, VectorParams  # noqa: E402

from qdrant_client_helper import QdrantRAGClient  # noqa: E402

# Enforce UTF-8 encoding output for Windows terminals (Bug CP1252 bypass)
sys.stdout.reconfigure(encoding="utf-8")

COLLECTION_NAME = "sendspeed_knowledge"
LINEAR_EXPORT_DIR = os.path.join(
    os.path.expanduser("~"),
    "OneDrive",
    "Documentos",
    "workspace",
    ".mecha",
    "linear-export",
)
UUID_NAMESPACE = uuid.uuid5(uuid.NAMESPACE_URL, "mecha://sendspeed_knowledge")

# Labels que representam modulos do produto (o export nao tem campo module).
MODULE_LABELS = {
    "Tracker",
    "Behavior",
    "Buyer",
    "UserIn",
    "Roleta",
    "Regras",
    "Jornadas",
    "Templates",
    "Bibliotecas",
    "Sendspeed",
    "Componente",
    "Smart Block",
    "Mini Games",
    "Modal",
    "Analytics",
}

# ---------------------------------------------------------------------------
# Scrub de segredos
# ---------------------------------------------------------------------------
SECRET_PATTERNS = [
    # Connection strings com credenciais: postgres://user:pass@host, mongodb+srv://...
    re.compile(
        r"\b(?:postgres(?:ql)?|mysql|mongodb(?:\+srv)?|redis|amqps?|mssql|ftp)"
        r"://[^\s'\"@]+:[^\s'\"@]+@[^\s'\"]+",
        re.IGNORECASE,
    ),
    # Tokens conhecidos (GitHub, Slack, OpenAI/Anthropic, AWS, Linear, Telegram bot)
    re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b"),
    re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    re.compile(r"\blin_(?:api|oauth)_[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"\b\d{8,10}:AA[A-Za-z0-9_-]{30,}\b"),  # Telegram bot token
    # JWTs
    re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{5,}\b"),
    # Bearer <token>
    re.compile(r"(?i)\bbearer\s+[A-Za-z0-9._~+/=-]{16,}"),
    # Atribuicoes de api key / token / senha / secret (env, json, yaml, code)
    re.compile(
        r"(?i)\b([A-Z0-9_.-]*(?:api[_-]?key|apikey|secret|token|senha|password|passwd|pwd)"
        r"[A-Z0-9_.-]*)(\s*[:=]\s*)(['\"]?)[^\s'\",;]{6,}\3"
    ),
]


def scrub_secrets(text: str) -> str:
    """Substitui possiveis segredos por [REDACTED]."""
    if not text:
        return text
    for pattern in SECRET_PATTERNS:
        if pattern.groups >= 3:
            # Preserva o nome da chave, redige apenas o valor
            text = pattern.sub(lambda m: f"{m.group(1)}{m.group(2)}[REDACTED]", text)
        else:
            text = pattern.sub("[REDACTED]", text)
    return text


# ---------------------------------------------------------------------------
# Leitura tolerante a OneDrive (retry 1x)
# ---------------------------------------------------------------------------
def read_text_tolerant(path: str) -> Optional[str]:
    for attempt in (1, 2):
        try:
            with open(path, "r", encoding="utf-8") as fh:
                return fh.read()
        except (OSError, UnicodeDecodeError) as exc:
            if attempt == 1:
                print(f"[SendSpeed Ingester] Falha lendo {os.path.basename(path)} "
                      f"({exc}). Retry em 1s (OneDrive)...")
                time.sleep(1.0)
            else:
                print(f"[SendSpeed Ingester] ERRO definitivo lendo {path}: {exc}")
    return None


# ---------------------------------------------------------------------------
# Chunking (mesmo padrao do ingest_conversations_qdrant.py)
# ---------------------------------------------------------------------------
def chunk_text(text: str, max_chars: int = 1000, overlap: int = 150) -> List[str]:
    chunks = []
    start = 0
    text_len = len(text)

    while start < text_len:
        end = min(start + max_chars, text_len)
        if end < text_len:
            last_period = text.rfind(".", start, end)
            last_newline = text.rfind("\n", start, end)
            boundary = max(last_period, last_newline)
            if boundary > start + (max_chars // 2):
                end = boundary + 1

        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start += max_chars - overlap

    return chunks


def derive_module(labels: List[str]) -> Optional[str]:
    for label in labels or []:
        if label in MODULE_LABELS:
            return label
    return None


class SendSpeedLinearIngester:
    def __init__(self, export_dir: str = LINEAR_EXPORT_DIR):
        print("[SendSpeed Ingester] Inicializando QdrantRAGClient...")
        self.export_dir = export_dir
        self.issues_dir = os.path.join(export_dir, "issues")
        # Reusa o mecanismo de embeddings da casa (mock via
        # MECHA_FORCE_MOCK_EMBEDDINGS=1, sentence-transformers quando disponivel).
        self.rag_client = QdrantRAGClient()
        self.client: QdrantClient = self.rag_client.client
        # Timeout maior que o default (5s) para create_collection/upsert em lote
        try:
            qdrant_url = os.environ.get("QDRANT_URL", "http://localhost:6333")
            import urllib.request
            urllib.request.urlopen(qdrant_url, timeout=1.0)
            self.client = QdrantClient(url=qdrant_url, timeout=60)
        except Exception:
            pass  # mantem o client do helper (modo local em disco)
        self.vector_size = self.rag_client.vector_size
        self._init_collection()

    def _init_collection(self):
        collections = self.client.get_collections().collections
        if not any(c.name == COLLECTION_NAME for c in collections):
            self.client.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=VectorParams(
                    size=self.vector_size, distance=Distance.COSINE
                ),
            )
            print(f"[SendSpeed Ingester] Colecao '{COLLECTION_NAME}' criada.")
        else:
            print(f"[SendSpeed Ingester] Colecao '{COLLECTION_NAME}' ja existente.")

    def _load_index(self) -> List[Dict[str, Any]]:
        index_path = os.path.join(self.export_dir, "index.json")
        raw = read_text_tolerant(index_path)
        if raw is None:
            raise RuntimeError(f"Nao foi possivel ler {index_path}")
        data = json.loads(raw)
        issues = data.get("issues", [])
        print(f"[SendSpeed Ingester] index.json: {data.get('total')} issues "
              f"(geradas em {data.get('generatedAt')}).")
        return issues

    @staticmethod
    def point_id(issue_id: str, chunk_n: int) -> str:
        """ID deterministico derivado de issue_id + chunk_n (idempotente)."""
        return str(uuid.uuid5(UUID_NAMESPACE, f"{issue_id}:{chunk_n}"))

    def build_points(self, meta: Dict[str, Any]) -> List[PointStruct]:
        issue_id = meta.get("id")
        if not issue_id:
            return []

        md_path = os.path.join(self.issues_dir, f"{issue_id}.md")
        content = read_text_tolerant(md_path)
        if content is None:
            # Fallback: usa descricao (possivelmente truncada) do index.json
            content = f"# {meta.get('title', '')}\n\n{meta.get('description') or ''}"
            print(f"[SendSpeed Ingester] {issue_id}: usando descricao do index.json "
                  f"(md indisponivel).")

        content = scrub_secrets(content)
        chunks = chunk_text(content)
        if not chunks:
            return []

        base_payload = {
            "source": "linear_export_sendspeed",
            "issue_id": issue_id,
            "title": scrub_secrets(meta.get("title") or ""),
            "status": meta.get("status"),
            "statusType": meta.get("statusType"),
            "module": derive_module(meta.get("labels") or []),
            "project": meta.get("project"),
            "url": meta.get("url"),
            "labels": meta.get("labels") or [],
            "total_chunks": len(chunks),
        }

        points = []
        for chunk_n, chunk in enumerate(chunks):
            payload = dict(base_payload)
            payload["chunk_n"] = chunk_n
            payload["text"] = chunk
            points.append(
                PointStruct(
                    id=self.point_id(issue_id, chunk_n),
                    vector=self.rag_client._get_embedding(chunk),
                    payload=payload,
                )
            )
        return points

    def ingest(self, batch_size: int = 64) -> int:
        issues = self._load_index()
        buffer: List[PointStruct] = []
        total_points = 0
        total_issues = 0

        def flush():
            nonlocal buffer, total_points
            if buffer:
                self.client.upsert(collection_name=COLLECTION_NAME, points=buffer)
                total_points += len(buffer)
                print(f"[SendSpeed Ingester] Upsert de {len(buffer)} pontos "
                      f"(acumulado: {total_points}).")
                buffer = []

        for meta in issues:
            points = self.build_points(meta)
            if points:
                total_issues += 1
                buffer.extend(points)
            if len(buffer) >= batch_size:
                flush()
        flush()

        print(f"[SendSpeed Ingester] Concluido: {total_issues} issues, "
              f"{total_points} chunks indexados em '{COLLECTION_NAME}'.")
        return total_points


if __name__ == "__main__":
    ingester = SendSpeedLinearIngester()
    ingester.ingest()
