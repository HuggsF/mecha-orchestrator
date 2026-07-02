import os
import sys
import glob
import sqlite3
import re
from typing import List

# Setup paths to ensure we can import qdrant_client_helper
PATTERNS_DIR = os.path.dirname(os.path.abspath(__file__))
if PATTERNS_DIR not in sys.path:
    sys.path.append(PATTERNS_DIR)

from qdrant_client_helper import QdrantRAGClient

# Enforce UTF-8 encoding output for Windows terminals (Bug CP1252 bypass)
sys.stdout.reconfigure(encoding='utf-8')

class ConversationIngester:
    def __init__(self):
        print("[Conversation Ingester] Inicializando QdrantRAGClient...")
        self.rag_client = QdrantRAGClient()
        self.printable_re = re.compile(rb'[^\x00-\x1F\x7F-\xFF]{20,}')

    def chunk_text(self, text: str, max_chars: int = 1000, overlap: int = 150) -> List[str]:
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

    def extract_db_text(self, db_path: str) -> str:
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Check table existence
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='steps'")
            if not cursor.fetchone():
                conn.close()
                return ""
                
            cursor.execute("SELECT idx, step_payload FROM steps ORDER BY idx")
            rows = cursor.fetchall()
            
            transcript_parts = []
            for idx, payload in rows:
                if not payload or not isinstance(payload, bytes):
                    continue
                # Extract printable strings
                matches = self.printable_re.findall(payload)
                step_text = []
                for match in matches:
                    try:
                        decoded = match.decode('utf-8', errors='ignore').strip()
                        # Ignore system error info / UUID format noise
                        if len(decoded) > 25 and not decoded.startswith("type.googleapis.com"):
                            step_text.append(decoded)
                    except Exception:
                        pass
                if step_text:
                    transcript_parts.append(f"--- Step {idx} ---\n" + "\n".join(step_text))
            
            conn.close()
            return "\n\n".join(transcript_parts)
        except Exception as e:
            print(f"[Conversation Ingester] Erro ao ler DB {db_path}: {e}")
            return ""

    def ingest_conversations(self, conversations_dir: str):
        db_files = glob.glob(os.path.join(conversations_dir, "*.db"))
        # Sort by modification time so we get most recent first
        db_files.sort(key=os.path.getmtime, reverse=True)
        
        if not db_files:
            print("[Conversation Ingester] Nenhum arquivo .db encontrado.")
            return

        print(f"[Conversation Ingester] Encontrados {len(db_files)} bancos de dados de conversa.")
        
        total_chunks = 0
        for db_path in db_files:
            db_name = os.path.basename(db_path)
            print(f"[Conversation Ingester] Processando: {db_name}...")
            
            raw_text = self.extract_db_text(db_path)
            if not raw_text.strip():
                print(f"[Conversation Ingester] Sem conteúdo útil em {db_name}. Pulando.")
                continue
                
            chunks = self.chunk_text(raw_text)
            print(f"[Conversation Ingester] Conteúdo extraído: {len(raw_text)} chars. Gerados {len(chunks)} chunks.")
            
            for idx, chunk in enumerate(chunks):
                metadata = {
                    "source": "conversation_history",
                    "db_file": db_name,
                    "chunk_index": idx,
                    "total_chunks": len(chunks)
                }
                self.rag_client.upsert(chunk, metadata)
                total_chunks += 1
                
        print(f"[Conversation Ingester] Concluído! Ingeridos {total_chunks} chunks de conversas no Qdrant.")

if __name__ == "__main__":
    # Standard conversations directory path in Gemini/Antigravity config
    conv_dir = os.path.join(os.path.expanduser("~"), ".gemini", "antigravity", "conversations")
    ingester = ConversationIngester()
    ingester.ingest_conversations(conv_dir)
