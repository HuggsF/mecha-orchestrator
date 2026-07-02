# 🧬 Sprints — Absorção SendSpeed ➔ MECHA

> Data: 2026-07-01 // Pattern: O6 #2 — multi-agent-topology-debate (Ingestão SendSpeed)
> Personas: Hiansen (Topology Architect) // Henrique (Execution & Data Validator) // Rodolfo (Devil's Advocate & QA)
> Decisão: **RATIFICADA** (tiebreaker: Henrique) — registro completo em `synthesis_report.md` §7 e `agent_dashboard.md`

| Campo | Valor |
|---|---|
| Escopo | Absorver o conhecimento SendSpeed (317 issues SEND-* do linear-export) no MECHA como problema de **ingestão e correção**, não de construção nova |
| Sprints | S1 🟢 EM EXECUÇÃO · S2 ⏸️ · S3 ⏸️ · S4 ⏸️ · S5 ⏸️ (dependências externas) |
| Infra verificada | Neo4j :7687 UP · Qdrant :6333 UP · `ops/.env` OK — Redis/Kafka da SendSpeed **não** são dependência |
| Fonte bruta | `linear-export/` (lido in place via env `SENDSPEED_EXPORT_DIR`, default `<root>\linear-export`) |
| Fonte curada | `CORE\sendspeed\*.md` (frontmatter 4 campos + emoji rail ➔, validado por `kernel/validators/dynamic_typing.py`) |
| Regra do ciclo | Nada é deletado/movido sem aprovação do Hugo (itens estruturais = P2 "HITL pendente") |

---

## 🎯 Visão geral da absorção

A SendSpeed entra no MECHA em três camadas, todas sobre infraestrutura **existente**:

1. **Conhecimento** — os 317 `SEND-*.md` do linear-export são indexados no Qdrant (collection `sendspeed_knowledge`) e registrados no Neo4j via ingestores dedicados; a versão curada vive em `CORE\sendspeed\`.
2. **Serviço** — um MCP server dedicado **read-only** (`sendspeed_mcp_server.py`, registrado como `sendspeed-mecha`) expõe 5 módulos / ~15 tools seguindo estritamente o pattern do `neo4j_mcp_server.py`: FastMCP stdio, docstrings PT-BR, tools nunca levantam exceção, truncamento com count, **zero escrita** (Qdrant/Neo4j só via ingestores) e **zero segredos inline** no `mcp_config.json`.
3. **Execução** — as journeys SendSpeed viram squad + workflows **LINEARES v1** no schema confirmado (`step_id`/`input_source`/`input_sources`/`output_var`), executados pelo `SquadOrchestrator` existente via `run_squad_workflow` pós-fix, emitindo `workflow.started`/`workflow.completed` no AgentBus (ORCH-12/13). Delay/branch/event-trigger **não entram no schema** — a evolução event-driven é Sprint 3, via bridge AgentBus (EventEnvelope) reaproveitando `shura_daemon` + `cross_squad_router`.

Regra de QA inegociável (Rodolfo): toda tool carrega proveniência (`source`, `status: confirmed|blocked|contradictory`, `blocked_by`) e `sendspeed_gaps()` é obrigatória — **incógnita servida como incógnita** (FastTrack SEND-504, nomenclatura SEND-498), nunca como fato.

---

## ⚖️ Decisão do debate O6 #2

### Resumo ratificado

- Regra de desempate aplicada — **Henrique vence execução**: absorção é INGESTÃO + correção; nenhuma engine ou server de orquestração novo será criado.
- Item #1 inegociável do ciclo é o **P0 factual de Henrique/Rodolfo**: corrigir `WORKSPACE_ROOT` em `ops\patterns\mecha_mcp_server.py` (linha 24, 3 dirnames em vez de 4 — hoje `run_squad_workflow` carrega config vazia em silêncio) e registrar o server existente como `mecha-core` no `mcp_config.json`.
- O conhecimento SendSpeed entra como **server dedicado read-only** `sendspeed_mcp_server.py` (convergência Hiansen+Rodolfo, compatível com a cláusula do próprio Henrique "isolamento em server próprio se o módulo crescer" — são 5 módulos e ~15 tools).
- Env inline no `mcp_config.json`: apenas `PYTHONIOENCODING=utf-8` + dirs de dados via env — **quebra deliberada do anti-padrão rootroot**.
- Ontologia: **nunca hand-edit**; passo 0 é modo merge no `generate_ontology.py` (ou ciclo formal baseline → curadoria → v2.2.0 → `neo4j_ontology_ingest.py`), corrigindo no mesmo bump o drift (rag_client.py, neo4j_mcp_server.py, fantasmas FRONT_VANGUARD/INFRA_LEGION/VECTOR_CORPS, mecha.html em docs/, linear-export como Knowledge Base).
- Itens estruturais/destrutivos ficam **P2 "HITL pendente"** — Sprint 1 lê linear-export in place via env var e nada é deletado/movido sem aprovação do Hugo.
- Sprint 1 é **100% executável nesta sessão** com a infra verificada UP.

### Matriz de priorização P0/P1/P2

| # | P | Item | Racional |
|---|----|------|----------|
| 1 | P0 | Fix `WORKSPACE_ROOT` em `ops\patterns\mecha_mcp_server.py:24` (normpath de `ide_backend.py`, 4 níveis) + `test_workspace_root_contract.py` provando que o SquadOrchestrator carrega `dev_squad.json` real via MCP | Bug verificado por Henrique e Rodolfo: `_load_json` retorna `{}` em silêncio e `run_squad_workflow` falha para QUALQUER pipeline — único caminho MCP→workflow das journeys |
| 2 | P0 | Resolver sprawl de MCP servers: registrar `mecha-core` (existente) e `sendspeed-mecha` (novo) no `mcp_config.json`; env inline só `PYTHONIOENCODING=utf-8` + dirs — nenhum segredo | Henrique/Rodolfo: 4 servers para 1 registro; criar módulo novo sem registrar o existente gera três planos divergentes e institucionaliza o anti-padrão rootroot |
| 3 | P0 | Segurança de borda ANTES de expor execução de journeys: bind `127.0.0.1` default no backend FastAPI (hoje `0.0.0.0` sem auth com `/api/preempt` e `/api/bus/publish` abertos à LAN) + token compartilhado mínimo nos endpoints de escrita do bus | P0 de segurança do Rodolfo: canal sem auth passa a disparar pipelines multi-agente com custo OpenRouter real e injeção de input no desktop |
| 4 | P0 | Caminho seguro de ontologia: modo merge em `ops/generate_ontology.py` (preserva layers/curated_*) OU ciclo formal baseline → curadoria por debate → bump v2.2.0 → reingestão via `neo4j_ontology_ingest.py`; adicionar linear-export a `expected_domains` | P0 do Hiansen: hoje é impossível registrar os módulos SendSpeed sem violar a regra estrutural 3 ou destruir a curadoria v2.1.0 |
| 5 | P0 | Representação ratificada: journeys = pipelines **LINEARES v1** no schema confirmado (fan-out/fan-in padrão tribunal); delay/branch/event-trigger proibidos no schema — evolução event-driven só via AgentBus/EventEnvelope na fase 2 | Consenso das 3 personas: extensão silenciosa do schema quebraria os runners existentes; MECHA não tem scheduler/estado persistente |
| 6 | P1 | Anti-alucinação por design: toda tool SendSpeed retorna proveniência (`source`, `status: confirmed\|blocked\|contradictory`, `blocked_by: ['SEND-504']`) e flag `pending_fasttrack_doc`; `sendspeed_gaps()` obrigatória com >= 4 gaps conhecidos | Rodolfo: conhecimento de segunda mão com furos documentados (FastTrack indefinida, `callback_url` vs `crm_callback_url`) não pode ser servido como fato |
| 7 | P1 | Corrigir drift da ontologia no bump v2.2.0: incluir `neo4j_mcp_server.py`, `rag_client.py`, `schemas/`, `neo4j_ontology_ingest.py`; corrigir path de `mecha.html` (docs/); remover squads fantasma; listar squads reais + sendspeed; registrar linear-export como Knowledge Base | Hiansen: o Digital Twin não conhece nem o server que o expõe nem o ingestor que o alimenta; ontologia declara o que não existe |
| 8 | P1 | Campo `entry_inputs` no schema de pipeline + validação Let It Fail no orchestrator, eliminando o if/else por nome de squad em `run_squad_workflow` (qa_squad→source_code, else→user_prompt) | Henrique/Rodolfo: heurística hardcoded não escala — squad nova de journey falharia em silêncio ou por sorte |
| 9 | P1 | Rota em `intelligence/rules/orchestration_rules.json` com `target_squad ['sendspeed']` (pool-ready ORCH-13) + runner emitindo `workflow.started`/`workflow.completed` no AgentBus; handoff sempre via Shura (ORCH-01) | Hiansen: sem rota e eventos, ORCH-12 bloqueia handoffs ou o roteamento opera fail-open com métricas obsoletas (TTL 120s) |
| 10 | P1 | Ingestão Qdrant (`ingest_sendspeed_linear.py` clonando `ingest_conversations_qdrant.py`): leitura tolerante a sync OneDrive, escrita atômica temp+rename, scrub de segredos nos 317 SEND-*.md antes de indexar em `sendspeed_knowledge` | Risco documentado no PROMPT_SYSTEM_DESIGN.md (leituras parciais) + issues de ops costumam vazar tokens |
| 11 | P1 | Resposta do orchestrator sinaliza `mock=true` quando rodar com `MOCK_KEY`/`MECHA_FORCE_MOCK_LLM=1` | Rodolfo: uma journey pode ser "validada" inteira contra mocks sem o chamador saber |
| 12 | P1 | Studio front: copiar `docs/mecha.html` para `ops/` (raiz estática) destravando o 404; validar `/api/health`, `/api/status`, `/api/preempt` e WS; badge passa a checar frescor via `/api/health` (hoje confia em `claw_status.json` stale ~3 dias) | Serving do dashboard está quebrado hoje; validação do front é entregável obrigatório do S1 |
| 13 | P1 | Conhecimento curado em `CORE\sendspeed\*.md` (frontmatter 4 campos + emoji rail ➔, hierarquia H1→H2→H3) validado com `kernel/validators/dynamic_typing.py --validate` antes de commit; MCP lê o curado, export bruto permanece insumo de ingestão | Decisão n.2 do ARCHITECTURE.md: fonte de verdade = vault CORE; índices são derivados |
| 14 | P2 🙋 | `git rm --cached ops/qdrant_db/` (242 binários trackeados, storage.sqlite vivo) + `.gitignore` | HITL pendente — altera o repo git; banco binário + git + OneDrive é corrupção esperando acontecer |
| 15 | P2 🙋 | Mover `linear-export/` para `CORE\sendspeed\linear-export\` (proposta Henrique); até lá S1 lê in place via env `SENDSPEED_EXPORT_DIR` | HITL pendente — movimentação estrutural sob OneDrive; conflito Hiansen (intocado) vs Henrique (mover) resolvido como diferimento com default de env |
| 16 | P2 🙋 | Rotacionar `NEO4J_PASS` "rootroot" e mover para `ops/.env`; consolidar os dois `.env` divergentes (raiz vs ops/) | HITL pendente — afeta serviços em execução (Neo4j, MCP neo4j-mecha, ingestores); o server novo já nasce sem copiar o padrão |
| 17 | P2 🙋 | Quarentena (não deleção) do lixo estrutural: `zi89DD7K/`, `node_modules` na raiz do .mecha, `recovered_transcripts_code.txt` e `scratch_brain_matches.txt` em ops/, cópia stale de `mecha.html` em `ops/templates/` | HITL pendente — regra do ciclo: nada deletado; anotar como fora-da-ontologia e candidato a remoção no próximo ciclo |
| 18 | P2 | Consolidar taxonomia duplicada `squads`/`intelligence` (dois donos de `intelligence/squads`) e destino dos 2 servers órfãos (`mcp_codebase_transform.py`, `webview_toolkit_mcp.py`): registrar ou anotar deprecated | Próximo ciclo — cristalizar convenção `<dominio>_mcp_server.py` + entrada `<dominio>-mecha` sem renomear nada agora |

---

## 🗺️ Topologia ratificada

| Campo | Valor |
|---|---|
| MCP server (novo) | `ops\patterns\sendspeed_mcp_server.py` — read-only, pattern `neo4j_mcp_server.py` |
| Registro mcp_config | `sendspeed-mecha` (novo) + `mecha-core` (existente, hoje sem registro) |
| Squad | `intelligence\squads\sendspeed_squad.json` |
| Workflows | `intelligence\squads\sendspeed_workflows.json` (lineares v1) |
| Collection Qdrant | `sendspeed_knowledge` (via `ingest_sendspeed_linear.py`) |
| Neo4j | nós `:Module`/`:Service`/`:Contract` via `neo4j_sendspeed_ingest.py` (S2) — escrita só via ingestor |

### Módulos e tools (5 módulos / ~15 tools, flat `sendspeed_*` em ops/patterns)

| Módulo | Tools | Issues-fonte |
|---|---|---|
| `sendspeed_catalog` | `sendspeed_status`, `sendspeed_module_map`, `sendspeed_find_issue`, `sendspeed_search`, `sendspeed_gaps` | SEND-488, 504, 511, 498, 475, 471, 476, 487 |
| `sendspeed_callbacks` | `crm_postback_contract`, `crm_status_depara`, `callback_pipeline_map` | SEND-488, 490–493, 495–498, 500, 502, 483, 479 |
| `sendspeed_journeys` | `journey_engine_map`, `journey_trigger_contract`, `journey_objective_attribution`, `journey_catalog` | SEND-477, 478, 391, 450, 446, 449, 479 |
| `sendspeed_channels` | `channel_send_spec`, `otp_flow_spec` | SEND-505, 508, 429, 452, 446, 478 |
| `sendspeed_integrations` | `igaming_webhook_pattern`, `webhook_security_spec`, `crm_adapter_registry` | SEND-510, 516, 515, 517, 506, 499, 501–503 |

---

## 🚀 Sprint S1 — Fundação executável 🟢 EM EXECUÇÃO (nesta sessão)

**Título:** MCP SendSpeed + journeys como squad + Studio validado

**Objetivo:** Tudo executável NESTA sessão com infra verificada UP (Neo4j 7687, Qdrant 6333, ops/.env): destravar o caminho MCP→workflow, subir o server SendSpeed read-only com anti-alucinação, journeys achatadas em pipelines lineares e dashboard do Studio servindo.

### Issues

| ID | Título |
|---|---|
| MECHA-S1-01 | Fix `WORKSPACE_ROOT` em `mecha_mcp_server.py` + `test_workspace_root_contract.py` |
| MECHA-S1-02 | Registrar `mecha-core` e `sendspeed-mecha` no `mcp_config.json` (sem segredos inline) |
| MECHA-S1-03 | `sendspeed_mcp_server.py` + 5 módulos flat `sendspeed_*` em ops/patterns |
| MECHA-S1-04 | `ingest_sendspeed_linear.py` → collection Qdrant `sendspeed_knowledge` (scrub de segredos, temp+rename) |
| MECHA-S1-05 | `sendspeed_squad.json` + `sendspeed_workflows.json` + rota ORCH `target_squad ['sendspeed']` |
| MECHA-S1-06 | Smoke E2E `run_squad_workflow('sendspeed_squad','sendspeed_workflows','crm_callback_routing_pipeline')` com `MECHA_FORCE_MOCK_LLM=1` sinalizando `mock=true` |
| MECHA-S1-07 | Copiar `docs/mecha.html` para `ops/` + validar front (health/status/preempt/WS, teste negativo) |
| MECHA-S1-08 | Bind `127.0.0.1` default + token nos endpoints de escrita do bus |

### Deliverables

- `run_squad_workflow` carregando e executando `tribunal_pipeline` real (critério de aceite global do Rodolfo)
- `sendspeed-mecha` respondendo `sendspeed_status`/`sendspeed_search`/`sendspeed_find_issue`/`sendspeed_gaps` (>= 4 gaps)
- `crm_callback_routing_pipeline` validado ponta a ponta (Journey Router → Delivery Analyst → Compliance Gate com saída [1]/[0])
- Dashboard `mecha.html` servido sem 404 com badge e WS conectado
- Testes em `ops/patterns/tests/` (`test_sendspeed_mcp.py`, `test_sendspeed_workflows.py`)
- Nenhum segredo novo em arquivo trackeado

### ✅ Critério de conclusão

As 8 issues MECHA-S1 fechadas; `tribunal_pipeline` real executando via MCP pós-fix; smoke E2E do `crm_callback_routing_pipeline` verde com `mock=true` sinalizado; suíte `ops/patterns/tests/` verde incluindo os 2 arquivos novos; dashboard respondendo sem 404; scan de segredos limpo nos arquivos tocados.

---

## 🧠 Sprint S2 — Ontologia v2.2.0 + conhecimento curado + multi-CRM core ⏸️

**Título:** Ontologia v2.2.0 + conhecimento curado + multi-CRM core (não bloqueado por FastTrack)

**Objetivo:** Registrar a absorção no Digital Twin sem destruir a curadoria e cobrir o núcleo da épica multi-CRM que NÃO depende da doc FastTrack: parsing centralizado, tipos, de-para de status, parametrização Redis/DB e roteamento com stub logado.

### Issues

| ID | Título |
|---|---|
| SEND-488 | Integração com CRM Fasttrack (epic macro) |
| SEND-497 | [callback-sms] Centralizar parsing do crm_postback em utilitário único |
| SEND-498 | [callback-sms] Atualizar tipos CrmPostback e SmsSentInfo para contrato multi-CRM |
| SEND-483 | Padronização e de-para de status de callback por cliente |
| SEND-502 | [callback-sms] Definir arquitetura: worker compartilhado com routing vs. worker-fasttrack dedicado |
| SEND-490 | [sms-api] Adicionar campo `crm` ao crm_postback nos DTOs e builders |
| SEND-491 | [sms-api] CrmCallbackConfigService — parametrizar CRM nas chaves Redis e queries DB |
| SEND-492 | [sms-api] RcsCallbackService — roteamento Smartico/Fasttrack no forwardCrmPostback |
| SEND-495 | [api-legada] Adicionar campo `crm` ao crm_postback — HandleApi, ValidationService e SmsService |
| SEND-489 | [Backoffice] Suporte ao CRM Fasttrack nas telas de crm-callback-config |
| SEND-493 | [sms-api] Consumer SMS — implementar forwardCrmPostback equivalente ao fluxo RCS |
| SEND-496 | [api-legada] SmsConsumer — implementar forwardCrmPostback com roteamento Smartico/Fasttrack |
| SEND-494 | [sms-api] Testes — specs e e2e para cobertura multi-CRM (Smartico + Fasttrack) |

### Deliverables

- Modo merge no `generate_ontology.py` (ou ciclo formal de curadoria) + bump v2.2.0 + reingestão via `neo4j_ontology_ingest.py`
- Drift corrigido: `rag_client.py`, `neo4j_mcp_server.py`, `schemas/`, `neo4j_ontology_ingest.py`, `mecha.html`, fantasmas removidos, squads reais + sendspeed, linear-export como Knowledge Base
- `CORE\sendspeed\{callbacks,journeys,channels,integrations,contracts}.md` com frontmatter validado
- Tools de callbacks refletindo o contrato consolidado (crm default smartico, invariante Enviado = Falha + Rejeitado + Pendente, chaves Redis parametrizadas)
- `neo4j_sendspeed_ingest.py` (nós `:Module`/`:Service`/`:Contract`) — escrita só via ingestor

### ✅ Critério de conclusão

Ontologia v2.2.0 gerada exclusivamente via `generate_ontology.py` (guard anti-clobber intacto) e reingerida no Neo4j sem perda de curadoria v2.1.0; os 5 docs curados de `CORE\sendspeed\` passando `dynamic_typing.py --validate`; tools de `sendspeed_callbacks` servindo o contrato consolidado com proveniência; zero escrita direta no Qdrant/Neo4j fora dos ingestores.

---

## 🔗 Sprint S3 — Journeys profundas + bridge event-driven + canais ⏸️

**Objetivo:** Absorver o coração do Journey Builder (envio real, batch trigger, atribuição, encurtador, templates RCS, OTP Infobip) e construir a bridge AgentBus `sendspeed.event.*` → disparo de pipeline via `shura_daemon`/`cross_squad_router` — a fase 2 event-driven prometida, sem engine nova.

### Issues

| ID | Título |
|---|---|
| SEND-391 | [Tech] SendSmsExecutor — integração API real no journey backend |
| SEND-477 | MAI 05.1 — Acionar Journey com Array de Entrada |
| SEND-479 | MAI 05.2 — Status "Pendente" em Mensageria |
| SEND-450 | Objetivos funcionais — metas que validam o desempenho de uma jornada |
| SEND-446 | Integrar encurtador de links em SMS e RCS (botões de carrossel) para metrificação de cliques |
| SEND-449 | Encurtamento automático de links nos botões de RCS (subconjunto de SEND-446) |
| SEND-429 | RCS em Jornadas — seleção de template com busca, filtros e navegação para edição |
| SEND-452 | Preview fiel do RCS no editor de template e suporte a emojis |
| SEND-478 | MAI [BACKLOG] — Envio de Lista Fria via API com Arquivo |
| SEND-505 | Implementar OTP WhatsApp Infobip |

### Deliverables

- `journey_batch_trigger_pipeline` e `journey_otp_fallback_pipeline` validados (semântica SEND-477/505 como workflows lineares)
- Handler AgentBus tópico `journey.*` com EventEnvelope validado por `dynamic_typing.py`
- Tools `journey_objective_attribution` e `journey_engine_map` enriquecidas com dados de SEND-450/446/449
- Campo `entry_inputs` implementado + validação Let It Fail no orchestrator
- Nota de consolidação SEND-449 como subconjunto de SEND-446 registrada via `sendspeed_gaps()`

### ✅ Critério de conclusão

Os 2 pipelines novos rodando via `run_squad_workflow` com eventos `workflow.started`/`completed` no AgentBus; handler `journey.*` disparando pipeline via bridge (sem scheduler/estado persistente novo); `entry_inputs` substituindo o if/else por nome de squad com teste de regressão; `sendspeed_gaps()` refletindo a consolidação 449⊂446.

---

## 🏢 Sprint S4 — Plataforma UserIn, dashboards e monetização ⏸️

**Objetivo:** Absorver o conhecimento de plataforma (RBAC, segmentação, onboarding), dashboards SmartFlow e a trilogia de billing — domínios de menor acoplamento com o pipeline de callback, priorizados por RICE (SEND-450 já coberto no S3).

### Issues

| ID | Título |
|---|---|
| SEND-367 | EPIC — Equipe & Permissões (RBAC UserIn, 10 user stories) |
| SEND-414 | Operadores numéricos para regras de Atributo de Perfil |
| SEND-354 | 🐞 Primeiros Passos — criar componentes não marca como concluído |
| SEND-471 | Dashboard Geral da SmartFlow |
| SEND-475 | feat/smartflow-profile (issue vazia — refinar ou fechar) |
| SEND-476 | Dashboard Geral SmartFlow — Upgrade (Fase 2) |
| SEND-487 | Alerta adicional de saldo na SS Control |
| SEND-512 | Propagar o valor cobrado do cliente por mensagem na consulta de dados |
| SEND-513 | Incluir o total cobrado no relatório |
| SEND-514 | Aumentar o filtro de período do relatório para até 30 dias |

### Deliverables

- Módulo de conhecimento `userin_platform` (RBAC 10 user stories, operadores numéricos, multi-tenancy user/company/visitor)
- Tools de dashboards/billing com flags de inconsistência (SEND-471/475/476/487 arquivadas-mas-listadas-abertas no export)
- Registro dos riscos de performance (relatório 30 dias + total cobrado, SLA [a decidir]) em `sendspeed_gaps()`
- Execução dos itens P2 HITL aprovados pelo Hugo até aqui (qdrant_db, linear-export move, rootroot)

### ✅ Critério de conclusão

Módulo `userin_platform` servido pelo `sendspeed-mecha` com proveniência; inconsistências do export (arquivada vs aberta) sinalizadas via flag em vez de silenciadas; gaps de SLA/performance registrados; P2 aprovados executados com smoke verde (suíte tests + verify de ingestão) — os não aprovados permanecem listados em HITL pendente.

---

## 🌐 Sprint S5 — Integração externa (bloqueios fora do controle do MECHA) ⏸️

> **NOTA:** sprint de dependências externas — doc FastTrack inexistente (SEND-504 bloqueia a cadeia), decisões de produto em aberto (o que é FastTrack/NGX, BSP WhatsApp), homologação Apostou/NGX, MongoDB Atlas e sistema de fazendinha do Bruno. O MECHA absorve os contratos conhecidos com status `blocked` e atualiza as tools quando os bloqueios caírem; **nada aqui é executável unilateralmente**.

### Issues

| ID | Título |
|---|---|
| SEND-504 | ⏳ Aguardar documentação FastTrack — ajustar payload, auth e campos |
| SEND-499 | [callback-sms] Implementar FastTrackClient — cliente HTTP para callbacks FastTrack |
| SEND-500 | [callback-sms] Atualizar CallbackGrouper e BatchProcessor para roteamento por CRM |
| SEND-501 | [callback-sms] Estender SonaMessageProcessor para roteamento FastTrack no fallback por phone |
| SEND-503 | [callback-sms] Atualizar SmarticoPayloadBuilder ou criar CrmPayloadBuilder por CRM |
| SEND-511 | Integração FastTrack (discovery de produto) |
| SEND-508 | Integração de OTP via WhatsApp (user story — alinhar com SEND-505) |
| SEND-510 | 🧩 Integração com API de Eventos NGX — 16 eventos de iGaming |
| SEND-506 | Mapeamento NGX para integração ao UserIn |
| SEND-516 | Ingestão de eventos via webhooks da NGX na UserIn |
| SEND-515 | Validar use case de recuperação de cadastro na UserIn — cliente Apostou |
| SEND-517 | Mapear e validar os gatilhos de UI do front da NGX (spike) |
| SEND-438 | MongoDB DEV read-only — user `govtech` sem permissão de escrita |
| SEND-509 | Fazendinha Automatizada de Qualidade de Rota |

### Deliverables

- Tools do lado FastTrack permanentemente marcadas `pending_fasttrack_doc` até a doc chegar (espelho do `TODO(fasttrack-doc)`)
- `igaming_webhook_pattern` consolidado NGX+FastTrack (HMAC-SHA256, idempotência, DLQ 1/5/15min, gatekeepers LGPD/KYC/blocklist) como spec do adaptador genérico recomendado em SEND-510
- Monitoramento dos 3 únicos Started do workspace (SEND-515/516/517) via `sendspeed_status`
- Atualização de `sendspeed_gaps()` e reingestão Qdrant/Neo4j a cada bloqueio externo resolvido

### ✅ Critério de conclusão

Todo contrato conhecido absorvido com `status: blocked` + `blocked_by` correto (nunca servido como fato); spec do adaptador genérico iGaming publicada nas tools; rotina de atualização gap→reingestão exercitada ao menos 1 vez. O sprint fecha por **cobertura do conhecimento bloqueado**, não pela queda dos bloqueios (que dependem de terceiros).

---

## 🙋 HITL pendente — aguardando aprovação do Hugo

Nenhum item abaixo será executado sem GO explícito. Regra do ciclo: **nada deletado ou movido sem aprovação**.

| # | Item | Risco/Impacto | Status |
|---|------|---------------|--------|
| 1 | `git rm --cached ops/qdrant_db/` (242 binários trackeados, storage.sqlite vivo) + `.gitignore` | Altera o repo git; banco binário + git + OneDrive = corrupção esperando acontecer | ⏳ Aguardando GO |
| 2 | Mover `linear-export/` → `CORE\sendspeed\linear-export\` | Movimentação estrutural sob OneDrive; até o GO, leitura in place via env `SENDSPEED_EXPORT_DIR` | ⏳ Aguardando GO |
| 3 | Rotacionar `NEO4J_PASS` "rootroot" → `ops/.env` + consolidar os dois `.env` divergentes (raiz vs ops/) | Afeta serviços em execução: Neo4j, MCP neo4j-mecha, ingestores | ⏳ Aguardando GO |
| 4 | Quarentena (não deleção) do lixo estrutural: `zi89DD7K/`, `node_modules` na raiz, `recovered_transcripts_code.txt`, `scratch_brain_matches.txt`, `mecha.html` stale em `ops/templates/` | Itens fora da ontologia; candidatos a remoção no próximo ciclo | ⏳ Aguardando GO |

**Próximo ciclo (P2 sem HITL):** consolidar taxonomia duplicada `squads`/`intelligence` e decidir destino dos 2 servers órfãos (`mcp_codebase_transform.py`, `webview_toolkit_mcp.py`) — registrar ou anotar deprecated, sem renomear nada agora.

---

*Gerado pelo debate O6 #2 — Hiansen // Henrique // Rodolfo — orquestrado via Cowork em 2026-07-01.*
