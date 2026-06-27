---
name: Projeto RAG-Vanessa
description: Second brain pessoal — repo privado com busca semantica sobre conhecimento proprio (ChromaDB + embeddings locais)
type: project
---

# RAG-Vanessa — Second Brain

**Repositorio:** https://github.com/Vr-Farias/rag-vanessa (privado)
**Criado em:** 30/03/2026
**Status:** estrutura inicial commitada, pronto pra primeiro teste

## O que e

Sistema RAG pessoal que indexa conhecimento de diversas fontes e permite busca por similaridade semantica em linguagem natural. Funciona como extensao da cabeca da Vanessa — pergunta em texto livre, recebe trechos relevantes do proprio conhecimento.

## Stack

- Python 3.11+
- ChromaDB (banco de vetores, persistente local)
- Sentence-Transformers modelo `all-MiniLM-L6-v2` (embeddings locais, zero API paga)
- Rich (output formatado no terminal)
- PyYAML (config)

## Estrutura

```
rag-vanessa/
  ingestors/base.py         # Motor: ChromaDB, chunking, upsert
  ingestors/markdown.py     # Ingestor de .md (implementado)
  search/query.py           # Busca semantica com filtro por tag
  config/sources.yml        # Fontes, ChromaDB, modelo embeddings
  tests/test_ingestor.py    # Testes basicos
  data/                     # Base ChromaDB (local, fora do git)
```

## Fontes planejadas

| Ingestor | Fonte | Status |
|----------|-------|--------|
| markdown.py | Arquivos .md (memorias, notas, docs) | Implementado |
| notion.py | Paginas do Notion via API | Planejado |
| github_issues.py | Issues/PRs de repos | Planejado |
| text_files.py | .txt, .sql, .py | Planejado |

## Como rodar (no desktop de casa)

```bash
git clone https://github.com/Vr-Farias/rag-vanessa.git
cd rag-vanessa
python -m venv .venv && source .venv/Scripts/activate
pip install -r requirements.txt
python -m ingestors.markdown --source "G:/Meu Drive/Claudio/memory" --tag memoria-claudio
python -m search.query "como resolvi o problema de duplicata no CNES?"
```

## Principios

- Zero dependencia de API paga (embeddings locais)
- Fontes intactas (RAG indexa, nao move nada)
- Modular (cada fonte e um ingestor independente)
- Privado (repo privado, base de dados fora do git)
- NAO rodar no notebook do trabalho (projeto pessoal)

## Contexto

Vanessa queria um "second brain" que juntasse conhecimento espalhado (memorias Claudio, Notion, projetos pessoais, queries SQL) num lugar so com busca inteligente. O RAG-Vanessa e esse lugar.

**Why:** conhecimento ta fragmentado em muitos lugares. Precisa de um ponto unico de busca que entenda linguagem natural.

**How to apply:** comecar ingerindo memorias do Drive, depois expandir pra Notion e outros. Cada fonte nova e so um arquivo em ingestors/.
