# Synthesis Report — Debate de Topologia Estrutural (O6)

> Data: 2026-07-01 // Pattern: O6-multi-agent-topology-debate (modo cirúrgico)
> Personas: Hiansen (Topology Architect), Henrique (Execution & Data Validator), Rodolfo (Devil's Advocate & QA)
> Alvo: harmonizar a árvore física (workspace/.mecha + ORCHESTRATOR_CORE) com mecha_ontology.json v2.0.0 — Phase 0/1
> Status: AGUARDANDO GO/NO-GO HUMANO — nenhuma deleção ou movimentação foi executada.

---

## 1. Contexto factual comum (varredura)

- Ontologia: mecha_ontology.json v2.0.0 (236 linhas, 8 domínios: ops, rag-dojo, CORE,
  intelligence, squads, docs, test_db, orchestrator-core). root declarado: `.mecha`.
- System Design: SYSTEM_DESIGN_INICIAL.md (319 linhas, 2026-06-20). Decisões ratificadas:
  Qdrant+Neo4j híbrido via interface única `rag_client`; ChromaDB descartado; CORE/Obsidian
  como fonte de verdade; governança Pydantic+AST transversal; migração incremental.
- Docs de fundação: ARCHITECTURE.md e NEXT_STEPS.md são stubs de template (S1 incompleto).
- Execução real concentrada em `.mecha/ops/patterns/` (~36 módulos py) e ORCHESTRATOR_CORE
  (CDC, ingestão, observabilidade, SaaS).
- Baseline de infra validado na sessão anterior: 36.580 chunks no Qdrant (mecha_collection),
  Neo4j neo4j/rootroot OK, verify_ingestion.py casando IDs Qdrant<->Neo4j.

---

## 2. Findings por persona

### 2.1 Hiansen — Topology Architect (estrutura canônica)

- H1. **Ontologia não reflete a árvore**: `kernel/validators/dynamic_typing.py` existe
  fisicamente, mas o domínio `kernel` NÃO está na ontologia — e `dynamic_typing.py` segue
  listado em `ops/patterns`, de onde já saiu. Ontologia v2.0.0 nasceu defasada.
- H2. **Squads são placeholders aspiracionais**: `squads/FRONT_VANGUARD|INFRA_LEGION|
  VECTOR_CORPS` estão VAZIOS (0 arquivos), porém declarados como Core Domain. Viola a regra
  anti-esqueleto. As definições reais vivem em `intelligence/squads/*.json`.
- H3. **Escopo do root inconsistente**: ontologia declara `root: .mecha`, mas o domínio
  orchestrator-core aponta `path: ORCHESTRATOR_CORE` — fora do root. Ou o root vira o
  workspace, ou o path vira relativo explícito (`../ORCHESTRATOR_CORE`).
- H4. **Raiz do ORCHESTRATOR_CORE sem taxonomia**: ~15 scripts soltos na raiz (probe_*.py,
  identify_model*.py x3, graphrag_ingester.py, kafka_consumer.py, verify_ingestion.py,
  check_counts.py, test_producer.py, middleware_run.py, *.ps1) sem camada declarada.
- H5. **Camadas canônicas ausentes**: a ontologia lista domínios mas não mapeia layers
  (kernel/execution/knowledge/index/data/ingestion/observability/interface/security).
  O System Design C4 já nomeia os containers — falta o de-para domínio→camada.
- H6. **Módulos fora da ontologia**: `ops/patterns/mcp_codebase_transform.py`,
  `PHASE7_NOTES.md`, `PHASE_BCD_NOTES.md`, `schemas/`, `dummy_vault/` não constam.

### 2.2 Henrique — Execution & Data Validator (realidade do código)

- E1. **Testes com convenção dupla**: 6 `test_*.py` na raiz de `ops/patterns/` E outros 6 em
  `ops/patterns/tests/`. A ontologia só enxerga os da raiz. Duas fontes de verdade.
- E2. **`rag_client` é paperware**: o System Design ratifica interface única de busca
  híbrida, mas só existe `qdrant_client_helper.py` + `neo4j_orchestration_bridge.py`
  separados. Nenhum `rag_client.py` materializado.
- E3. **Iteração-debris na raiz do ORCHESTRATOR_CORE**: `identify_model.py`, `_v2.py`,
  `_ollama.py` são três gerações do mesmo experimento convivendo sem marcação.
- E4. **Duplicações e artefatos de sync**: `CORE/vanessa-sessao-2026-03-26(1).md` (artefato
  OneDrive), `test_db/ORCHESTRATOR_CORE/` (cópia aninhada dentro do .mecha), zips de export
  na raiz (`CORE-20260617T220059Z-3-001.zip`, `mecha_full_export.zip`,
  `mecha_rules_and_lore_clean.zip` no workspace) e `Mega Prompts Knot improvements.zip`
  dentro de `ops/patterns/`.
- E5. **Execução funciona onde está**: os runners de squad (`code|qa|devops_squad_runner.py`,
  `squad_orchestrator.py`, `cross_squad_router.py`) rodam a partir de `ops/patterns` com as
  configs JSON de `intelligence/squads`. Não há necessidade FUNCIONAL dos diretórios
  `squads/*` físicos hoje — arquitetura por demanda diz: remova ou dê função.
- E6. **Pipeline de dados está saudável**: 36.580 chunks + verify OK. A prioridade não é
  refazer ingestão, é não quebrá-la ao mover scripts (verify_ingestion.py, graphrag_ingester.py).

### 2.3 Rodolfo — Devil's Advocate & QA (riscos e contradições)

- R1. **Contradição doc vs base de conhecimento**: System Design descarta ChromaDB, mas
  `CORE/conhecimento-rag-chromadb.md` segue como nota viva na fonte de verdade do RAG —
  risco de o retriever responder com stack morta. Marcar como legado/deprecated no frontmatter.
- R2. **Gerador de ontologia sem validação**: `ops/generate_ontology.py` produziu v2.0.0 já
  divergente (H1). Não há schema JSON nem validação AST na geração — o Auditor deveria
  recusar ontologia que não bate com o filesystem.
- R3. **Workspace inteiro dentro do OneDrive**: locking e artefatos `(1)` já observados (E4).
  `node_modules/`, `ops/qdrant_db/`, `ops/venv_build/` sincronizando é risco de corrupção
  e custo de I/O. Ponto cego confirmado do meu DNA.
- R4. **Git aninhado sem submódulo**: `.mecha` é repo git e `rag-dojo/` tem `.git` próprio
  dentro dele (e `.git/worktrees` no .mecha). Estado de versionamento ambíguo — commits
  podem estar silenciosamente ignorando o rag-dojo.
- R5. **Pré-requisitos do O6 não atendidos formalmente**: S1 (ARCHITECTURE.md stub) e S6
  (sem ADR-001 no .mecha; só ADR-002 no ORCHESTRATOR_CORE). Este debate roda em modo
  cirúrgico com WARNING — mas o próximo O6 deve rodar com S1/S6 completos.
- R6. **Zero cobertura nos scripts críticos do ORCHESTRATOR_CORE**: verify_ingestion.py e
  graphrag_ingester.py não têm teste algum; mover/renomear sem smoke test é aposta cega.
  E `.codebase-transform-state.json` não existe — progresso dos patterns não é rastreado.

---

## 3. Conflitos e resolução (tiebreaker: Henrique)

### Conflito A — Destino dos diretórios squads/ vazios
- Hiansen: hidratar conforme taxonomia canônica (cada squad com manifest + runbook) — a
  estrutura declarada deve existir de verdade.
- Henrique: as definições JÁ vivem em `intelligence/squads/*.json` e os runners em
  `ops/patterns`. Diretórios vazios são ruído; remover até que haja código que os exija.
- Rodolfo: nenhum dos dois sem antes varrer referências — se algum runner resolve path
  `squads/FRONT_VANGUARD`, a remoção quebra silenciosamente.
- **Resolução (Henrique)**: grep por referências aos três nomes; zero refs → remover em
  Phase 0 e registrar na ontologia que squads são entidades LÓGICAS (JSON), não pastas.

### Conflito B — Raiz poluída do ORCHESTRATOR_CORE
- Hiansen: migrar já para camadas (`ingestion/`, `observability/`, `tools/`) — Phase 1 de verdade.
- Henrique: são ferramentas em uso diário (verify acabou de ser corrigido); mover o mínimo,
  em um passo só, sem renomear, com smoke test antes/depois.
- Rodolfo: sem testes, qualquer movimentação exige prova de execução pós-move e commit
  isolado para rollback barato.
- **Resolução (Henrique)**: Phase 1 — criar `scripts/` (probes+diag) e `ingestion/`
  (graphrag_ingester, kafka_consumer, verify_ingestion), preservar nomes, rodar
  `python -m py_compile` + verify_ingestion.py pós-move, commit único.

### Conflito C — Corrigir a ontologia à mão ou regenerar
- Hiansen: corrigir manualmente agora (kernel, paths, componentes faltantes) — precisão primeiro.
- Henrique: correção manual morre em uma semana; consertar `generate_ontology.py` e regenerar.
- Rodolfo: regenerar com um gerador sem validação (R2) só automatiza o erro.
- **Resolução (Henrique, incorporando R2)**: Phase 0 corrige a MÃO os 4 erros factuais
  (kernel, dynamic_typing, mcp_codebase_transform, path orchestrator-core) para desbloquear;
  Phase 1 adiciona validação (JSON Schema + diff contra filesystem) ao generate_ontology.py
  e ele passa a ser a única fonte de escrita.

---

## 4. Matriz de Priorização — Phase 0 (higienização) / Phase 1 (harmonização)

| # | P | Fase | Ação | Evidência | Owner |
|---|----|------|------|-----------|-------|
| 1 | P0 | 0 | Corrigir mecha_ontology.json: +domínio kernel; dynamic_typing.py para kernel/validators; +mcp_codebase_transform.py, schemas/, PHASE*_NOTES; path orchestrator-core explícito | H1, H3, H6 | Hiansen |
| 2 | P0 | 0 | Grep refs a FRONT_VANGUARD/INFRA_LEGION/VECTOR_CORPS; zero refs → remover pastas vazias e documentar squads como entidades lógicas | H2, E5 | Henrique |
| 3 | P0 | 0 | Higienizar debris: zips de export, (1) dupes no CORE, test_db/ORCHESTRATOR_CORE aninhado, zip dentro de ops/patterns | E4 | Henrique |
| 4 | P0 | 0 | Unificar testes em ops/patterns/tests/ (mover os 6 da raiz; ajustar pytest.ini/paths) | E1 | Henrique |
| 5 | P0 | 0 | Marcar conhecimento-rag-chromadb.md como deprecated no frontmatter (não deletar — histórico) | R1 | Rodolfo |
| 6 | P0 | 0 | Preencher ARCHITECTURE.md (C4 resumido do System Design) e NEXT_STEPS.md real; criar .codebase-transform-state.json via transform-status.py | R5, R6 | Hiansen |
| 7 | P1 | 1 | ORCHESTRATOR_CORE: criar scripts/ e ingestion/, mover os 15 soltos sem renomear, py_compile + verify pós-move, commit único | H4, E3, E6, R6 | Henrique |
| 8 | P1 | 1 | Materializar rag_client.py (facade Qdrant+Neo4j) em ops/patterns; probes passam a consumi-lo | E2 | Henrique |
| 9 | P1 | 1 | generate_ontology.py: validação JSON Schema + diff filesystem antes de escrever; recusar componente inexistente | R2, H1 | Rodolfo |
| 10 | P1 | 1 | Mapear domínio→camada canônica na ontologia (kernel, execution, knowledge, index, data, ingestion, observability, interface, security) | H5 | Hiansen |
| 11 | P2 | 1+ | Resolver git aninhado do rag-dojo (submodule ou vendor) e plano de saída do OneDrive (ou exclusões de sync p/ node_modules, qdrant_db, venv_build) | R3, R4 | Rodolfo |

Smoke test dos itens estruturais (2, 3, 4, 7): suíte `ops/patterns/tests` verde +
`verify_ingestion.py` OK (36.580 chunks casando) antes e depois de cada commit.

---

## 5. Gate HITL

Nenhuma ação da matriz foi executada. Aguardando Go/No-Go do líder técnico:

- **GO Phase 0** → executo itens 1-6 (higienização, sem tocar em código executável).
- **GO Phase 0+1** → executo 1-10 com commits isolados e smoke tests.
- **NO-GO** → relatório permanece como registro; nada muda.

Rollback: `git reset --hard` no commit anterior à execução (por item, commits isolados).

*Gerado pelo debate O6 — Hiansen // Henrique // Rodolfo — orquestrado via Cowork.*
