---
name: Conhecimento RAG e ChromaDB
description: Fundamentos de RAG explicados com analogias SQL, ChromaDB como PostgreSQL dos vetores, chunking, embeddings, busca semantica
type: project
---

# Conhecimento Tecnico — RAG e ChromaDB

## RAG em uma frase

E um SELECT antes do prompt. Busca contexto relevante na base de conhecimento e cola junto com a pergunta antes de enviar pro LLM.

## Anatomia

- **R** (Retrieval) = SELECT (buscar trechos relevantes)
- **A** (Augmented) = JOIN (colar trechos no prompt)
- **G** (Generation) = LLM gera resposta com base no contexto recebido

## ChromaDB = PostgreSQL dos vetores

| PostgreSQL | ChromaDB |
|-----------|----------|
| INSERT INTO | collection.add() |
| SELECT WHERE = | collection.query() (por similaridade) |
| Busca exata por valor | Busca aproximada por significado |
| Indice B-tree | Indice HNSW (vizinhos mais proximos) |
| Coluna TEXT | Embedding (vetor de 384 numeros) |
| Schema rigido | Schema flexivel (metadata livre) |

## Embeddings

Texto -> modelo -> vetor numerico (384 floats com all-MiniLM-L6-v2).
Textos semanticamente similares geram vetores proximos no espaco vetorial.
A busca calcula distancia entre o vetor da pergunta e os vetores armazenados.

## Chunking

Textos longos sao fatiados em pedacos (chunks) com sobreposicao.
Analogia: window function com LAG — cada chunk carrega pedaco do anterior pra nao perder contexto.
Config padrao do RAG-Vanessa: chunk_size=500, chunk_overlap=50.

## Metadata e filtros

Equivalente ao WHERE do SQL. Cada documento pode ter tags e metadados.
Combina busca semantica (distancia vetorial) com filtro exato (tag, fonte, tipo).

## Armazenamento

ChromaDB persiste em pasta local (SQLite + indices HNSW).
RAG-Vanessa configurado pra persistir em G:\Meu Drive\Claudio\rag-data\chromadb\.
Zero dependencia de API paga — embeddings rodam local com sentence-transformers.

## Modelo de embeddings escolhido

all-MiniLM-L6-v2: leve (~80MB), rapido, 384 dimensoes, bom pra texto geral em ingles/portugues.
Alternativas futuras: multilingual-e5-large (melhor pra PT-BR, mais pesado).
