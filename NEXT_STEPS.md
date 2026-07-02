# 📝 Próximos Passos

> Derivado da matriz do `synthesis_report.md` (debate O6, 2026-07-01). Phase 0 executada.

## Phase 1 (executada em 2026-07-01)

- [x] Item 7 — ORCHESTRATOR_CORE reorganizado: `ingestion/` (graphrag, kafka, verify, middleware, test_producer) + `scripts/` (11 probes/diag). py_compile 14 OK; verify_ingestion PONTE INTACTA + score 0.74
- [x] Item 8 — `rag_client.py` materializado em `ops/patterns/` (vector_search, graph_query, hybrid_search; fail-safe)
- [x] Item 9 — `generate_ontology.py` blindado: validação contra filesystem + guard anti-clobber de versão curada (+ backup .bak). Guard testado: recusou v1.0.0 sobre v2.1.0
- [x] Item 10 — Bloco `layers` (10 camadas) na `mecha_ontology.json` v2.1.0

## P2 (backlog — exige decisão humana)

- [ ] Item 11a — rag-dojo git aninhado: submodule ou vendor (decisão)
- [ ] Item 11b — Plano OneDrive: mover workspace OU excluir do sync `node_modules/`, `ops/qdrant_db/`, `ops/venv_build/`
- [ ] Completar S1/S6 formais (ADR-001 no .mecha) para o próximo O6 rodar sem WARNING
- [ ] Re-rodar debate O6 pós-Phase 1 para validar harmonização

## Concluído (Phase 0 — 2026-07-01)

- [x] Ontologia corrigida: +kernel, dynamic_typing realocado, +mcp_codebase_transform, path orchestrator-core, squads lógicos
- [x] Squads físicos vazios removidos (zero refs de código)
- [x] Debris arquivado em `../_archive/o6-cleanup-2026-07-01/` (4 zips); `(1)` divergente renomeado; `test_db/ORCHESTRATOR_CORE` dissolvido
- [x] Suíte unificada em `ops/patterns/tests/` + conftest.py (280 testes coletados)
- [x] `conhecimento-rag-chromadb.md` marcado deprecated
- [x] ARCHITECTURE.md real + este arquivo; state file criado (O6 in_progress)
