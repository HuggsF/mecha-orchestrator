# 🏗️ Arquitetura — MECHA (HWorkforceStudio)

> Resumo operacional do C4 completo em `SYSTEM_DESIGN_INICIAL.md`. Atualizado no Phase 0 do debate O6 (2026-07-01).

## Decisões ratificadas

1. Busca híbrida: **Qdrant** (vetorial, mecha_collection, 36.580 chunks) + **Neo4j** (grafo) atrás de interface única `rag_client` (Phase 1, item 8 da matriz).
2. Fonte de verdade do conhecimento: vault **Obsidian/CORE** — índices são derivados.
3. Governança transversal: Pydantic + validação AST + emoji rails + frontmatter (`kernel/validators/dynamic_typing.py`).
4. ChromaDB **descartado** (confinado ao rag-dojo como material de treino).
5. Migração incremental — MECHA segue em produção durante a harmonização.

## Camadas (domínio → camada canônica)

| Camada | Onde vive |
|---|---|
| kernel (governança/validação) | `kernel/validators/` |
| execution (runners, bots, Claw, bus) | `ops/patterns/` |
| knowledge (fonte de verdade) | `CORE/` (Obsidian) |
| index (vetorial + grafo) | Qdrant (docker) + Neo4j (docker) |
| ingestion | `ops/patterns/dorkling_rag_ingester.py`, `ingest_conversations_qdrant.py`, `../ORCHESTRATOR_CORE/` (graphrag, kafka, verify) |
| observability | `../ORCHESTRATOR_CORE/observability_api` + frontend observability-portal |
| interface | Studio (Next.js), Teams (8686), Telegram, `ops/mecha.ps1` CLI |
| orchestration (lógica de squads) | `intelligence/squads/*.json` + `ops/patterns/squad_orchestrator.py` |

## Containers principais (C4-L2)

Studio Frontend (Next.js) · Control/Dashboard API (FastAPI 8585) · Amanda Teams API (FastAPI 8686) · Claw Engine (RPA loop) · Squads Orchestrator · rag_client → Qdrant+Neo4j · Ingestion (handover+graphify) · Knowledge Vault (Obsidian/CORE) · Observability (Prometheus/Grafana).

## Regras estruturais (pós-O6)

- Squads são entidades lógicas (JSON em `intelligence/squads/`) — sem diretórios físicos vazios.
- Toda a suíte de testes vive em `ops/patterns/tests/` (conftest.py resolve paths).
- `mecha_ontology.json` só é alterado via `ops/generate_ontology.py` (com validação — item 9).
- Debate de topologia: pattern O6 do codebase-transform; relatórios em `synthesis_report.md`.
