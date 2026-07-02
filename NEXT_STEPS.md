# 📝 Próximos Passos

> Derivado da matriz do `synthesis_report.md` (debate O6, 2026-07-01). Phase 0 executada.

## Phase 1 (aprovada — em execução)

- [ ] Item 7 — ORCHESTRATOR_CORE: `scripts/` + `ingestion/`, mover 15 scripts da raiz sem renomear (backup em `_archive/`, py_compile + verify pós-move)
- [ ] Item 8 — Materializar `rag_client.py` (facade Qdrant+Neo4j) em `ops/patterns/`
- [ ] Item 9 — `generate_ontology.py`: validação estrutural + diff contra filesystem antes de escrever
- [ ] Item 10 — Mapear domínio→camada na `mecha_ontology.json` (bloco `layers`)

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
