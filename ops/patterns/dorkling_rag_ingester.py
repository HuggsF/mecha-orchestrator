import os
import sys
from typing import List
from qdrant_client_helper import QdrantRAGClient

# Setup paths
PATTERNS_DIR = os.path.dirname(os.path.abspath(__file__))
OPS_DIR = os.path.dirname(PATTERNS_DIR)
MECHA_DIR = os.path.dirname(OPS_DIR)
WORKSPACE_ROOT = os.path.dirname(MECHA_DIR)

DOCS_DIR = os.path.join(WORKSPACE_ROOT, "docs")
CORE_DIR = os.path.join(WORKSPACE_ROOT, ".mecha", "CORE")
OBSIDIAN_DIR = os.environ.get("OBSIDIAN_DIR") or os.path.join(WORKSPACE_ROOT, "Obsidian")
SUPERPOWERS_DIR = os.path.join(WORKSPACE_ROOT, ".superpowers")

# Enforce UTF-8 encoding output for Windows terminals (Bug CP1252 bypass)
sys.stdout.reconfigure(encoding='utf-8')

class DorklingRagIngester:
    def __init__(self):
        print("[Ingester] Inicializando QdrantRAGClient...")
        self.rag_client = QdrantRAGClient()

    def chunk_text(self, text: str, max_chars: int = 800, overlap: int = 150) -> List[str]:
        chunks = []
        start = 0
        text_len = len(text)
        
        while start < text_len:
            end = min(start + max_chars, text_len)
            # Tenta alinhar o fim do chunk com pontuação ou quebra de linha
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

    def ingest_directory(self, directory_path: str, source_label: str):
        if not os.path.exists(directory_path):
            print(f"[Ingester] Diretório não encontrado: {directory_path}. Pulando.")
            return

        print(f"[Ingester] Iniciando varredura recursiva de {directory_path} ({source_label})...")
        file_count = 0
        chunk_count = 0
        
        for root, dirs, files in os.walk(directory_path):
            # Ignora pastas ocultas (como .obsidian e .git)
            dirs[:] = [d for d in dirs if not d.startswith(".")]
            for file in files:
                if file.endswith((".md", ".txt")):
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, WORKSPACE_ROOT)
                    file_count += 1
                    
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            content = f.read()
                            
                        if not content.strip():
                            continue
                            
                        chunks = self.chunk_text(content)
                        for idx, chunk in enumerate(chunks):
                            metadata = {
                                "source": source_label,
                                "file_name": file,
                                "file_path": rel_path.replace("\\", "/"),
                                "chunk_index": idx,
                                "total_chunks": len(chunks)
                            }
                            # Inserindo no Qdrant
                            self.rag_client.upsert(chunk, metadata)
                            chunk_count += 1
                    except Exception as e:
                        print(f"[Ingester] Erro ao processar arquivo {file_path}: {e}")
                        
        print(f"[Ingester] Concluído: {file_count} arquivos lidos, {chunk_count} chunks indexados para {source_label}.")

    def run(self):
        # Ingest docs
        self.ingest_directory(DOCS_DIR, "docs")
        # Ingest DNA Core engrams
        self.ingest_directory(CORE_DIR, "dna_core")
        # Ingest Obsidian Second Brain
        self.ingest_directory(OBSIDIAN_DIR, "second_brain")
        # Ingest Superpowers
        self.ingest_directory(SUPERPOWERS_DIR, "superpowers")
        print("[Ingester] Ingestão em lote concluída com sucesso no Qdrant.")

if __name__ == "__main__":
    ingester = DorklingRagIngester()
    ingester.run()
