# Fase 3 — Knowledge & Index (camada RAG)

> Objetivo: toda busca de conhecimento passa por **um único** `rag_client`, com
> **Qdrant** (vetorial) + **Neo4j** (grafo). ChromaDB fica depreciado.
> Vault Obsidian/`CORE` é a fonte de verdade; `data/knowledge_base` é derivado.
>
> Fonte de verdade do desenho: `.mecha/design/SYSTEM_DESIGN_INICIAL.md`.

## Arquitetura

```
ingestion/ (handover, graphify)
      │  chunk + embed + extrai entidades
      ▼
  ┌─────────┐        ┌─────────┐
  │ Qdrant  │  ←──→  │  Neo4j  │
  │ :6333   │        │ :7687   │
  │ vetor   │        │ grafo   │
  └─────────┘        └─────────┘
      ▲  busca híbrida
      │
  index/rag_client.py  ← interface ÚNICA (search / upsert / graph_query)
      ▲
 Squads · Amanda · Claw  (consumidores — nenhum fala com os bancos direto)
```

## Contrato — `index/rag_client.py`

```python
from typing import Protocol, Optional, Sequence
from pydantic import BaseModel

class Document(BaseModel):
    doc_id: str
    file_name: str
    source: str            # "vault" | "freescout" | "telegram" | ...
    emoji_rail: str        # governança MECHA (frontmatter)
    text: str
    tags: list[str] = []

class Chunk(BaseModel):
    chunk_id: str          # f"{doc_id}::{i}"
    doc_id: str
    text: str
    emoji_rail: str
    tags: list[str] = []

class Hit(BaseModel):
    chunk_id: str
    doc_id: str
    score: float           # similaridade (cosine)
    text: str
    file_name: str
    source: str
    tags: list[str] = []

class RagClient(Protocol):
    def search(self, query: str, limit: int = 3,
               filters: Optional[dict] = None) -> list[Hit]: ...
    def upsert(self, docs: Sequence[Document]) -> int: ...   # nº de chunks gravados
    def graph_query(self, cypher: str,
                    params: Optional[dict] = None) -> list[dict]: ...
    def health(self) -> dict: ...   # {"qdrant": bool, "neo4j": bool, "degraded": bool}
```

## Modelo de dados — Qdrant

| Campo | Valor |
|---|---|
| Coleção | `knowledge` |
| Distância | `Cosine` |
| Vetor | embedding do `chunk.text` |
| `payload.file_name` | nome do arquivo origem |
| `payload.doc_id` / `chunk_id` | rastreabilidade |
| `payload.emoji_rail` | rail de governança (filtrável) |
| `payload.source` | origem (`vault`/`freescout`/…) |
| `payload.tags[]` | filtros temáticos |
| `payload.created_at` | ISO-8601 |

`filters` em `search()` mapeia 1:1 para `Filter` do Qdrant
(ex.: `{"source": "vault", "tags": ["dev"]}`).

## Modelo de dados — Neo4j (via `graphify`)

```cypher
(:Document {doc_id, file_name, emoji_rail})
   -[:HAS_CHUNK]->(:Chunk {chunk_id})
   -[:MENTIONS]->(:Entity {name, type})

(:Document)-[:ROUTES_TO]->(:Window {state_id})   // liga ao navigation_graph
```

## ⚠ Decisão pendente (ratificar ANTES de codar)

- **Embedding model + dimensão** da coleção. Default proposto para rodar local:
  `all-MiniLM-L6-v2` ou `bge-small-en` (**384 dims**).
  Defina e congele — mudar depois exige **reindexar tudo**.

## Degradação (sem Docker/Qdrant)

`health().degraded == True` → `search()` retorna `[]` sem quebrar; consumidores
caem para resposta sem RAG. O dashboard continua servindo.

## Variáveis de ambiente (`.env`, fora do git)

```
QDRANT_URL=http://localhost:6333
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=...
EMBEDDING_MODEL=all-MiniLM-L6-v2      # confirme dim = 384
```

---

## Prompt para o Antigravity — Fase 3

```
# Tarefa: Implementar a Fase 3 (Knowledge & Index / rag_client)
#         do Mecha Huggs Workforce Studio

## Contexto
Fonte de verdade do desenho: .mecha/design/SYSTEM_DESIGN_INICIAL.md.
Migração incremental — o MECHA segue EM PRODUÇÃO; cada fase tem rollback,
a árvore antiga permanece até validar. Não quebre .mecha/ops/patterns/.
Depende da Fase 1 (kernel/contracts). Se ela não existir, crie os modelos aqui.

## Decisões ratificadas (invioláveis)
1. Busca híbrida = Qdrant (vetor) + Neo4j (grafo). ChromaDB depreciado.
   Acesso ÚNICO via index/rag_client.py — nenhum consumidor fala com os bancos direto.
2. Vault Obsidian/CORE é a fonte; data/knowledge_base é derivado.
3. Governança MECHA: todo Document/Chunk carrega emoji_rail (frontmatter) + valida Pydantic.
4. Escrita atômica em qualquer JSON lido pela UI.

## Parâmetro a confirmar comigo ANTES de codar
- embedding_model e VECTOR_SIZE (dimensão da coleção 'knowledge').
  Default proposto: all-MiniLM-L6-v2 (384). Aguarde meu OK.

## Entregáveis
1. index/rag_client.py
   - Protocol RagClient: search(query, limit=3, filters=None)->list[Hit];
     upsert(docs)->int; graph_query(cypher, params=None)->list[dict]; health()->dict.
   - Impl QdrantRagClient: coleção 'knowledge', distance=Cosine, payload
     {file_name, doc_id, chunk_id, emoji_rail, source, tags[], created_at}.
     filters mapeia p/ qdrant_client Filter. Cria a coleção se não existir.
   - Neo4j OPCIONAL e degradável: graph_query usa driver bolt; sem Neo4j, health.degraded=True.
2. index/models.py (ou kernel/contracts) — Document, Chunk, Hit (Pydantic v2).
3. ingestion/indexer.py — varre o vault, faz chunk (com overlap), embed e upsert;
   idempotente por chunk_id; respeita emoji_rail do frontmatter.
4. ingestion/graphify.py — popula Neo4j: Document-HAS_CHUNK->Chunk-MENTIONS->Entity,
   Document-ROUTES_TO->Window (liga ao navigation_graph.json).
5. Testes:
   - unit: serialização dos contratos; _atomic_write_json; mapeamento de filters.
   - integração: Qdrant local :6333 (docker), upsert→search caminho feliz com top-k.
   - smoke: health() com e sem Neo4j.

## Restrições
- Python 3.11, Pydantic v2, qdrant-client, neo4j-driver. asyncio onde fizer sentido.
- Sem credencial em log (scrub). Segredos só via .env: QDRANT_URL, NEO4J_URI,
  NEO4J_USER, NEO4J_PASSWORD, EMBEDDING_MODEL.
- Erros padrão: 400 payload, 503 fail-closed (banco obrigatório ausente), 500 interno.

## Critério de pronto
- rag_client.search() responde de Qdrant local com top-k ordenado por score;
- upsert idempotente (reindexar não duplica);
- Neo4j opcional não derruba o serviço (degraded mode);
- suíte verde; nada da árvore antiga deixou de funcionar.

Antes de codar, gere o Implementation Plan (arquivos, ordem, pontos de rollback)
e aguarde meu OK — inclusive sobre embedding_model/VECTOR_SIZE.
```
