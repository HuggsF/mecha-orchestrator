import os
import sys
from typing import List

# Add parent directory to path so we can import qdrant_client_helper
PATTERNS_DIR = os.path.dirname(os.path.abspath(__file__))
if PATTERNS_DIR not in sys.path:
    sys.path.append(PATTERNS_DIR)

from qdrant_client_helper import QdrantRAGClient

# Setup paths
WORKSPACE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(PATTERNS_DIR)))
GEMINI_DIR = os.path.join(os.path.expanduser("~"), ".gemini")

SKILL_DIRS = [
    os.path.join(WORKSPACE_ROOT, ".agents", "skills"),
    os.path.join(WORKSPACE_ROOT, ".claude", "skills"),
    os.path.join(WORKSPACE_ROOT, ".openskills"),
    os.path.join(GEMINI_DIR, "config", "skills"),
]

# Add plugin skill directories
PLUGINS_DIR = os.path.join(GEMINI_DIR, "config", "plugins")
if os.path.exists(PLUGINS_DIR):
    for plugin in os.listdir(PLUGINS_DIR):
        plugin_path = os.path.join(PLUGINS_DIR, plugin)
        if os.path.isdir(plugin_path):
            plugin_skills = os.path.join(plugin_path, "skills")
            if os.path.exists(plugin_skills):
                SKILL_DIRS.append(plugin_skills)

# Enforce UTF-8 encoding output for Windows terminals (Bug CP1252 bypass)
sys.stdout.reconfigure(encoding='utf-8')

class SkillIngester:
    def __init__(self):
        print("[Skill Ingester] Inicializando QdrantRAGClient...")
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

    def parse_skill_md(self, file_path: str):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            name = os.path.basename(os.path.dirname(file_path))
            description = ""
            body = content
            
            if content.startswith("---"):
                parts = content.split("---", 2)
                if len(parts) >= 3:
                    frontmatter = parts[1]
                    body = parts[2].strip()
                    for line in frontmatter.splitlines():
                        if ":" in line:
                            k, v = line.split(":", 1)
                            k = k.strip().lower()
                            v = v.strip()
                            if k == "name":
                                name = v
                            elif k == "description":
                                description = v
            return name, description, body
        except Exception as e:
            print(f"[Skill Ingester] Erro ao ler {file_path}: {e}")
            return None, None, None

    def ingest_skills(self):
        file_count = 0
        chunk_count = 0
        
        for skill_dir in SKILL_DIRS:
            if not os.path.exists(skill_dir):
                continue
                
            print(f"[Skill Ingester] Varrendo {skill_dir}...")
            for root, dirs, files in os.walk(skill_dir):
                for file in files:
                    if file == "SKILL.md":
                        file_path = os.path.join(root, file)
                        name, description, body = self.parse_skill_md(file_path)
                        
                        if body is None or not body.strip():
                            continue
                            
                        file_count += 1
                        chunks = self.chunk_text(body)
                        
                        for idx, chunk in enumerate(chunks):
                            metadata = {
                                "source": "agent_skills",
                                "skill_name": name,
                                "skill_description": description,
                                "file_path": file_path.replace("\\", "/"),
                                "chunk_index": idx,
                                "total_chunks": len(chunks)
                            }
                            self.rag_client.upsert(chunk, metadata)
                            chunk_count += 1
                            
        print(f"[Skill Ingester] Concluído: {file_count} skills indexadas, {chunk_count} chunks no total.")

    def run(self):
        self.ingest_skills()

if __name__ == "__main__":
    ingester = SkillIngester()
    ingester.run()
