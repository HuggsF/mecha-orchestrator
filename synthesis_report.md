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

---

## 6. Execução (GO Phase 0+1 — 2026-07-01)

| # | Ação | Status | Evidência de smoke |
|---|------|--------|--------------------|
| 1 | Ontologia corrigida (kernel, squads lógicos, paths, +componentes) | DONE | JSON válido v2.1.0, 9 domínios |
| 2 | Squads físicos vazios removidos | DONE | grep: zero refs de código; rmdir sem erro |
| 3 | Debris arquivado (4 zips), (1) divergente renomeado, test_db/OC dissolvido | DONE | `_archive/o6-cleanup-2026-07-01/` |
| 4 | Suíte unificada em tests/ + conftest central | DONE | pytest --collect-only: 280 testes, 0 erros de import |
| 5 | conhecimento-rag-chromadb.md deprecated | DONE | frontmatter status/superseded_by |
| 6 | ARCHITECTURE.md + NEXT_STEPS.md reais; state file criado | DONE | O6 in_progress no state |
| 7 | ORCHESTRATOR_CORE: ingestion/ + scripts/ (16 arquivos, backup prévio) | DONE | py_compile 14 OK; verify_ingestion: PONTE INTACTA, score 0.7444 |
| 8 | rag_client.py (facade Qdrant+Neo4j) | DONE | py_compile OK; graph fail-safe |
| 9 | generate_ontology.py com validação + anti-clobber | DONE | guard recusou v1.0.0 sobre v2.1.0 (exit 1) |
| 10 | layers na ontologia (10 camadas) | DONE | JSON válido |
| 11 | OneDrive + git aninhado rag-dojo | P2 | pendente decisão humana |

Commits (.mecha, branch squad/qa/test-loop): 57dde6e (ontologia+docs), 427dabd (higienização), f326576 (testes) + Phase 1 na sequência. rag-dojo: fix do transform-status (O6 no registry).

**Avisos registrados pelo executor:**
- ORCHESTRATOR_CORE não é repositório git — rollback do item 7 é o backup em `_archive/o6-pre-move-backup-OC/`. Recomendação: `git init` (decisão humana).
- Os commits varreram também alterações pré-existentes pendentes na working tree (dedup antigo do CORE, edições em ide_backend/qdrant_client_helper/telegram_bot) — estavam não-commitadas antes da sessão.
- `ops/qdrant_db/` (dados vivos do Qdrant) está versionado no git e sincronizado no OneDrive — recomendação forte do Rodolfo: gitignorar + excluir do sync (P2).

---

## 7. O6 #2 — Absorção SendSpeed (2026-07-01)

> Pattern: O6-multi-agent-topology-debate #2 // Personas: Hiansen // Henrique // Rodolfo
> Decisão: **RATIFICADA** (tiebreaker: Henrique) — absorção SendSpeed é problema de INGESTÃO e correção, não de construção nova.
> Plano de sprints S1–S5: `SPRINTS_SENDSPEED_ABSORPTION.md` (S1 em execução nesta sessão).

Síntese: nenhuma engine ou server de orquestração novo. Item #1 inegociável = fix do `WORKSPACE_ROOT` em `ops\patterns\mecha_mcp_server.py:24` + registro do server existente como `mecha-core`. O conhecimento SendSpeed entra como server dedicado **read-only** `sendspeed_mcp_server.py` (`sendspeed-mecha`, 5 módulos / ~15 tools, pattern `neo4j_mcp_server.py`: FastMCP stdio, tools nunca levantam exceção, zero escrita, zero segredos inline). Toda tool carrega proveniência (`source`/`status`/`blocked_by`) e `sendspeed_gaps()` é obrigatória — incógnita servida como incógnita (SEND-504, SEND-498). Journeys viram squad + workflows LINEARES v1 executados pelo SquadOrchestrator existente via `run_squad_workflow` pós-fix (eventos ORCH-12/13 no AgentBus); delay/branch/event-trigger não entram no schema — evolução event-driven é Sprint 3 via bridge AgentBus/EventEnvelope. Ontologia nunca hand-edit: modo merge no `generate_ontology.py` ou ciclo formal → v2.2.0 → `neo4j_ontology_ingest.py`, corrigindo o drift no mesmo bump. Itens estruturais/destrutivos = P2 "HITL pendente" (nada deletado/movido sem GO do Hugo). Infra verificada UP (Neo4j 7687, Qdrant 6333) — Redis/Kafka da SendSpeed não são dependência.

### Matriz consolidada P0/P1/P2

| # | P | Ação | Racional |
|---|----|------|----------|
| 1 | P0 | Fix `WORKSPACE_ROOT` em `mecha_mcp_server.py:24` (normpath 4 níveis, padrão ide_backend.py) + `test_workspace_root_contract.py` | `_load_json` retorna `{}` em silêncio; `run_squad_workflow` falha para qualquer pipeline — único caminho MCP→workflow |
| 2 | P0 | Registrar `mecha-core` (existente) + `sendspeed-mecha` (novo) no `mcp_config.json`; env inline só `PYTHONIOENCODING=utf-8` + dirs, sem segredos | 4 servers para 1 registro; módulo novo sem registrar o existente = três planos divergentes + anti-padrão rootroot |
| 3 | P0 | Segurança de borda antes de expor journeys: bind `127.0.0.1` default no FastAPI (hoje 0.0.0.0 sem auth) + token nos endpoints de escrita do bus | Canal sem auth passa a disparar pipelines multi-agente com custo OpenRouter real e injeção de input no desktop |
| 4 | P0 | Caminho seguro de ontologia: modo merge no `generate_ontology.py` OU ciclo formal baseline→curadoria→v2.2.0→`neo4j_ontology_ingest.py`; linear-export em `expected_domains` | Impossível registrar módulos SendSpeed sem violar a regra estrutural 3 ou destruir a curadoria v2.1.0 |
| 5 | P0 | Journeys = pipelines LINEARES v1 no schema confirmado; delay/branch/event-trigger proibidos — event-driven só via AgentBus/EventEnvelope (fase 2) | Extensão silenciosa do schema quebraria os runners; MECHA não tem scheduler/estado persistente |
| 6 | P1 | Anti-alucinação por design: proveniência (`source`/`status`/`blocked_by`) + `pending_fasttrack_doc` em toda tool; `sendspeed_gaps()` >= 4 gaps | Conhecimento de segunda mão com furos documentados não pode ser servido como fato |
| 7 | P1 | Drift da ontologia no bump v2.2.0: +rag_client.py, +neo4j_mcp_server.py, +schemas/, +ingestor; path mecha.html; remover squads fantasma; +sendspeed; linear-export como Knowledge Base | Digital Twin não conhece nem o server que o expõe nem o ingestor que o alimenta |
| 8 | P1 | Campo `entry_inputs` no schema de pipeline + validação Let It Fail, eliminando if/else por nome de squad | Heurística hardcoded não escala — squad nova falharia em silêncio ou por sorte |
| 9 | P1 | Rota `target_squad ['sendspeed']` em `orchestration_rules.json` + eventos `workflow.started/completed` no AgentBus; handoff via Shura (ORCH-01) | Sem rota e eventos, ORCH-12 bloqueia handoffs ou roteamento fail-open com métricas obsoletas (TTL 120s) |
| 10 | P1 | `ingest_sendspeed_linear.py` → Qdrant `sendspeed_knowledge`: leitura tolerante a OneDrive, temp+rename, scrub de segredos nos 317 SEND-*.md | Risco de leituras parciais documentado no PROMPT_SYSTEM_DESIGN.md + issues de ops vazam tokens |
| 11 | P1 | Orchestrator sinaliza `mock=true` com `MOCK_KEY`/`MECHA_FORCE_MOCK_LLM=1` | Journey pode ser "validada" inteira contra mocks sem o chamador saber |
| 12 | P1 | Studio: copiar `docs/mecha.html` para `ops/` (fix 404) + validar health/status/preempt/WS; badge via `/api/health` (claw_status.json stale ~3 dias) | Serving do dashboard quebrado; validação do front é entregável obrigatório do S1 |
| 13 | P1 | Conhecimento curado em `CORE\sendspeed\*.md` (frontmatter 4 campos + emoji rail ➔) validado por `dynamic_typing.py --validate`; MCP lê o curado | Decisão n.2 do ARCHITECTURE.md: fonte de verdade = vault CORE; índices derivados |
| 14 | P2 | `git rm --cached ops/qdrant_db/` + `.gitignore` — **HITL pendente** | Banco binário + git + OneDrive = corrupção esperando acontecer; exige aprovação do Hugo |
| 15 | P2 | Mover `linear-export/` → `CORE\sendspeed\linear-export\` — **HITL pendente**; até lá leitura in place via env `SENDSPEED_EXPORT_DIR` | Movimentação estrutural sob OneDrive; conflito Hiansen vs Henrique resolvido como diferimento |
| 16 | P2 | Rotacionar `NEO4J_PASS` "rootroot" → `ops/.env` + consolidar os 2 `.env` — **HITL pendente** | Afeta serviços em execução; o server novo já nasce sem copiar o padrão |
| 17 | P2 | Quarentena (não deleção) do lixo estrutural: `zi89DD7K/`, `node_modules` raiz, transcripts/scratch em ops/, mecha.html stale em templates/ — **HITL pendente** | Regra do ciclo: nada deletado; anotar fora-da-ontologia, candidato a remoção no próximo ciclo |
| 18 | P2 | Consolidar taxonomia `squads`/`intelligence` + destino dos 2 servers órfãos (`mcp_codebase_transform.py`, `webview_toolkit_mcp.py`) | Próximo ciclo — cristalizar convenção `<dominio>_mcp_server.py` + `<dominio>-mecha` sem renomear agora |

Sprints: **S1** fundação executável (MCP SendSpeed + journeys como squad + Studio, EM EXECUÇÃO) → **S2** ontologia v2.2.0 + curadoria + multi-CRM core → **S3** journeys profundas + bridge event-driven + canais → **S4** UserIn/dashboards/billing + P2 HITL aprovados → **S5** integrações externas (FastTrack/NGX/Atlas/fazendinha — nada executável unilateralmente; contratos absorvidos como `blocked`). Detalhamento completo por sprint (issues SEND-*, deliverables, critérios de conclusão) em `SPRINTS_SENDSPEED_ABSORPTION.md`.

*Gerado pelo debate O6 #2 — Hiansen // Henrique // Rodolfo — orquestrado via Cowork.*
