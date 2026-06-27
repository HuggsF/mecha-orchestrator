import os
import sys
import uuid
from typing import List, Dict, Any
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

# Base path setup
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "qdrant_db")
COLLECTION_NAME = "mecha_collection"

# Enforce UTF-8 encoding output for Windows terminals (Bug CP1252 bypass)
sys.stdout.reconfigure(encoding='utf-8')

# Load .env variables locally
env_path = os.path.join(BASE_DIR, ".env")
if os.path.exists(env_path):
    try:
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    parts = line.split("=", 1)
                    if len(parts) == 2:
                        os.environ[parts[0].strip()] = parts[1].strip().strip('"').strip("'")
    except Exception:
        pass

class QdrantRAGClient:
    def __init__(self):
        # Initialize client in disk path (persistence on disk)
        os.makedirs(DB_PATH, exist_ok=True)
        self.client = QdrantClient(path=DB_PATH)
        self.model = None
        self.vector_size = 384  # Default MiniLM embedding size
        self._init_model()
        self._init_collection()

    def _init_model(self):
        if os.environ.get("MECHA_FORCE_MOCK_EMBEDDINGS") == "1":
            print("[Qdrant RAG] Modo MECHA_FORCE_MOCK_EMBEDDINGS=1 ativo. Ignorando imports de sentence-transformers.")
            self.model = None
            return

        try:
            # Enforce offline mode to prevent downloads hanging
            os.environ["HF_HUB_OFFLINE"] = "1"
            from sentence_transformers import SentenceTransformer
            # MiniLM is 384 dimensional, very fast
            # We wrap it in a try-catch to allow mock fallback if downloading fails
            print("[Qdrant RAG] Carregando modelo sentence-transformers (all-MiniLM-L6-v2) local...")
            self.model = SentenceTransformer("all-MiniLM-L6-v2")
            print("[Qdrant RAG] Modelo sentence-transformers carregado com sucesso.")
        except Exception as e:
            print(f"[Qdrant RAG] Aviso ao carregar sentence-transformers: {e}. Usando Mock hashing de resiliência.")
            self.model = None

    def _init_collection(self):
        try:
            collections = self.client.get_collections().collections
            exists = any(c.name == COLLECTION_NAME for c in collections)
            if not exists:
                self.client.create_collection(
                    collection_name=COLLECTION_NAME,
                    vectors_config=VectorParams(size=self.vector_size, distance=Distance.COSINE),
                )
                print(f"[Qdrant RAG] Coleção '{COLLECTION_NAME}' criada com sucesso.")
            else:
                print(f"[Qdrant RAG] Coleção '{COLLECTION_NAME}' já existente.")
        except Exception as e:
            print(f"[Qdrant RAG] Erro ao inicializar coleção: {e}")

    def _get_embedding(self, text: str) -> List[float]:
        if self.model:
            try:
                embedding = self.model.encode(text).tolist()
                return embedding
            except Exception as e:
                print(f"[Qdrant RAG] Erro ao gerar embedding real: {e}. Fallback para Mock.")
        
        # Deterministic hashing embedding fallback
        # Generates a pseudo-random float vector based on string hash
        import random
        random.seed(hash(text))
        return [random.uniform(-1.0, 1.0) for _ in range(self.vector_size)]

    def upsert(self, text: str, metadata: Dict[str, Any] = None) -> str:
        if metadata is None:
            metadata = {}
        point_id = str(uuid.uuid4())
        vector = self._get_embedding(text)
        
        payload = {"text": text}
        payload.update(metadata)
        
        try:
            self.client.upsert(
                collection_name=COLLECTION_NAME,
                points=[
                    PointStruct(
                        id=point_id,
                        vector=vector,
                        payload=payload
                    )
                ]
            )
            print(f"[Qdrant RAG] Chunk indexado com ID: {point_id}")
            return point_id
        except Exception as e:
            print(f"[Qdrant RAG] Erro ao realizar upsert: {e}")
            return ""

    def search(self, query: str, limit: int = 3) -> List[Dict[str, Any]]:
        vector = self._get_embedding(query)
        try:
            results = self.client.query_points(
                collection_name=COLLECTION_NAME,
                query=vector,
                limit=limit
            )
            return [
                {
                    "id": hit.id,
                    "score": hit.score,
                    "text": hit.payload.get("text", ""),
                    "metadata": {k: v for k, v in hit.payload.items() if k != "text"}
                }
                for hit in results.points
            ]
        except Exception as e:
            print(f"[Qdrant RAG] Erro ao pesquisar: {e}")
            return []

if __name__ == "__main__":  # pragma: no cover
    # Test runner
    client = QdrantRAGClient()
    
    # Adicionar alguns dados de teste
    print("\n[*] Inserindo dados de teste...")
    client.upsert("O reator do Kafka sincronizado foi projetado usando thread ghost workers.", {"topic": "kafka"})
    client.upsert("O Tribunal dos Awesome-Bots audita código e schemas TOML.", {"topic": "tribunal"})
    client.upsert("O firewall cognitivo utiliza o Ollama para validar as ações do operador.", {"topic": "firewall"})
    
    # Realizar pesquisa
    query = "reator kafka ghost workers"
    print(f"\n[*] Pesquisando por: '{query}'")
    hits = client.search(query, limit=2)
    for idx, hit in enumerate(hits):
        print(f"Hit {idx+1} [Score {hit['score']:.4f}]: {hit['text']} (Metadata: {hit['metadata']})")
