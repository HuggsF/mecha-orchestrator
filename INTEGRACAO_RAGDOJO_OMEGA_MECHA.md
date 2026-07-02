---
titulo: "Integração RAG Dojo ⊕ Omega/Mecha — Pipeline de Graduação"
emoji_rail: "📓 ➔ 🧬 ➔ 🌌 ➔ ⚙️ ➔ 🛡️"
fluxo_semantico:
  - "📓 documentação / decisão de arquitetura"
  - "🧬 contratos de tipo (Pydantic / Protocols) como ABI compartilhada"
  - "🌌 indexação canônica (Qdrant + Neo4j)"
  - "⚙️ execução (economics, orchestration, cognitive) graduada p/ produção"
  - "🛡️ guardrail clean-room (carta de segurança do dojo preservada)"
data: "2026-06-22"
status: "proposta — aguarda ratificação no System Design"
autor: "Henrique (@Bh0bh11) via assistente"
valida_ast: true
relacionados:
  - ".mecha/ALINHAMENTO_MECHA_OMEGA.md"
  - ".mecha/SYSTEM_DESIGN_INICIAL.md"
  - ".mecha/rag-dojo/CLAUDE.md"
  - ".mecha/rag-dojo/contracts.py"
---

# 🧬 Integração RAG Dojo ⊕ Omega/Mecha — Pipeline de Graduação

> **Objetivo:** definir como o `rag-dojo` (hoje uma ilha desacoplada em `.mecha/rag-dojo`)
> se conecta à topologia canônica do `ALINHAMENTO_MECHA_OMEGA`, **sem violar a carta de
> segurança do dojo** e **sem reintroduzir o ChromaDB** já descartado pela decisão canônica.

## 1. Contexto e diagnóstico

### 1.1 O que o rag-dojo é (e o que ele não é)

O `rag-dojo` é um **laboratório de R&D em clean-room** — *"RAG Spiral Training, do zero ao
estado da arte em 6 espirais"*. Ele **não é** um serviço de produção nem a fonte de verdade
do conhecimento da org. Ele é onde técnicas de RAG são desenvolvidas, testadas e **pontuadas**
(ledger `rag-score`) contra **dados públicos**.

As 6 espirais formam uma stack progressiva, já com contratos formais (`contracts.py`) e um
"linker" (`pipeline_factory.py`):

| Espiral | Capacidade entregue | Componentes-chave |
|---|---|---|
| 01 — Chunks | Retrieval vetorial | `VectorStore` (ChromaDB), `embedder` (MiniLM 384d), `Generator` (Groq), `reranker`, `query_expander`, `context_compressor` |
| 02 — Graph | Retrieval híbrido vetor+grafo | `GraphStore` (Neo4j), `hybrid_retriever`, `entity_extractor` |
| 03 — Tensão | Orquestração com campo de tensão | `orchestrator`, `tension`, `confidence`, `fallback` |
| 04 — Cognitivo | Memória + detecção de padrões | `cognitive_layer`, `memory_store` (SQLite), `pattern_detector` |
| 05 — Economia | Roteamento por custo + budget | `model_router`, `budget_tracker`, `circuit_breaker`, `cost_calculator` |
| 06 — Estado da arte | Auto-melhoria + benchmark | `cycle_manager`, `benchmark_suite`, `guardrails`, `proposer` |

### 1.2 Estado atual: ilha bidirecionalmente desacoplada

Auditoria de acoplamento (ambos os sentidos) confirma isolamento total:

- **Saída (workspace → dojo):** nenhum projeto, `CLAUDE.md` raiz, `MECHA_GUIDE` ou `.mecha`
  referencia o dojo. As 27 ocorrências de "rag-dojo" estão todas dentro da própria pasta.
- **Entrada (dojo → workspace):** o dojo não lê nada de fora. Corpus = `./data/fastapi_docs/`
  (amostra pública, não versionada); "DNA do Henrique" está **vendorizado** em `anamnese/`,
  não puxado do vault; dependências externas são **serviços** (Groq, Neo4j, ChromaDB, Ollama)
  em pod próprio (`rag-test`), com `.env` vivendo **dentro do pod**.
- **Única ponte hoje:** *exportação* — o dojo serviu de bancada para empacotar a skill
  `codebase-transform.skill` (22/06). Isso é graduação de artefato, não acoplamento de código.

### 1.3 A restrição inviolável que muda a abordagem

O `rag-dojo/CLAUDE.md` define **regras de segurança INVIOLÁVEIS**: *"APENAS dados públicos
open-source; ZERO chunks sensíveis de Hugo/Felipe/org; ZERO modelos de negócio; ZERO acesso
ao sec-forge"*. **Consequência direta:** a ideia intuitiva de "fazer o dojo ingerir o vault
Obsidian" **viola a carta** (regra #2). O vault real **não pode** entrar no dojo. Portanto a
integração tem de ser feita pela **direção oposta**: o dojo exporta capacidade, e o stack
canônico — onde os dados reais legitimamente vivem — a consome.

## 2. Princípio de integração: graduação, não acoplamento

### 2.1 Por que não "apontar o dojo para o vault"

Apontar o dojo para dados reais quebraria três coisas ao mesmo tempo: a carta de segurança
(#2), a pureza do `rag-score` (que mede maestria sobre *dados públicos reproduzíveis*) e a
decisão canônica de store único. O dojo perde valor justamente se deixar de ser clean-room.

### 2.2 O modelo "dojo → graduação → produção"

A costura é um **pipeline de graduação** em que a unidade que cruza a fronteira é o
**contrato + componente provado**, nunca o dado:

```
[ dojo / clean-room ]            [ fronteira de graduação ]          [ Omega/Mecha / produção ]
 dados públicos          →  contrato (Protocol/Pydantic)      →   knowledge/rag + index/*
 técnica provada         →  componente hardened + benchmark   →   execution/* consome
 rag-score ≥ gate        →  PR revisado (Hugo E Felipe)        →   roda sobre dados reais (vault)
```

### 2.3 Aderência ao ALINHAMENTO_MECHA_OMEGA

O `ALINHAMENTO` já cita o dojo como *"engine OmegaHuggs (ChromaDB+Neo4j)"* e decide:
**padronizar Qdrant + Neo4j atrás de uma interface `rag_client` única, descartando o ChromaDB.**
Esta proposta respeita isso: o ChromaDB **fica restrito ao dojo** (custo zero de migração lá
dentro); na graduação, o `RetrievalBackend` ganha uma implementação Qdrant. O Neo4j já é comum
às duas pontas — é o ponto de menor atrito.

## 3. Pontos de plug (superfície de contato)

### 3.1 Contratos — `kernel/contracts` como ABI compartilhada

`contracts.py` já define os `Protocol`s certos: `RetrievalBackend`, `GenerationBackend`,
`CostTracker`, `SelfImprover`, `SpiralModule`. **Ação:** promover esses Protocols para
`kernel/contracts/` (camada canônica), endurecidos como modelos Pydantic onde houver payload
(coords, RAG hits) — aderente ao debate Henrique vs. Hiansen (tipagem estrita) e ao playbook
`devsquad_pydantic_contracts.md`. O dojo passa a **importar do kernel**, virando consumidor
do mesmo contrato que a produção.

### 3.2 Índice — `index/vector` + `index/graph` via `rag_client`

O `hybrid_retriever` do dojo é o protótipo natural do `rag_client` canônico. **Ação:** generalizar
o `qdrant_client_helper` do Mecha numa implementação `QdrantStore` que satisfaça
`RetrievalBackend`; manter o `GraphStore`/Neo4j como está. O `rag_client` expõe
`retrieve(query, top_k)` + `format_context(...)` — exatamente a assinatura já contratada.

### 3.3 Execução — graduar economics, orchestration e cognitive

Três espirais entregam infra transversal que a produção não tem ainda e ganharia muito:

- **Economics (05):** `model_router` (roteamento por complexidade), `budget_tracker` e
  `circuit_breaker` viram serviço cross-cutting em `execution/` (ou `kernel/economics`). É o
  maior ganho de curto prazo: controle de custo para todo o stack.
- **Orchestration (03):** `orchestrator` + campo de `tension`/`confidence`/`fallback` alimenta
  `execution/squads` (Tribunal Hermes, CodeSquad) com lógica de retry e parada por zero-delta.
- **Cognitive (04):** `memory_store` + `pattern_detector` reforçam `execution/agents`
  (Amanda / Ghost Workers) com memória e detecção de padrões.

### 3.4 Governança — `rag-score` como quality gate

O ledger `rag-score` (5 dimensões: D1 RAG Mastery, D2 AI-OS Architecture, D3 Cost Economics,
D4 Implementation, D5 Orchestration) deixa de ser só métrica de treino e vira **gate de
maturidade**: um componente só **gradua** (entra em produção) se sua dimensão correspondente
estiver acima de um piso. Ex.: `QdrantStore` só promove com D1 ≥ 70. Registrar isso em
`.mecha/governance/`.

### 3.5 Ownership — squad VECTOR_CORPS

A camada de índice/RAG tem dono natural: o squad **VECTOR_CORPS** (`.mecha/squads/`). Ele
assume a fronteira de graduação (revisão de contrato + benchmark), com PRs sempre revisados
por Hugo **e** Felipe (regra #7 do dojo). INFRA_LEGION cuida dos pods (Qdrant/Neo4j).

## 4. Mapa de migração (de → para)

| rag-dojo (origem) | Camada canônica (destino) | Tratamento |
|---|---|---|
| `contracts.py` (Protocols) | `kernel/contracts` | **Move** — fonte de verdade da ABI; dojo importa de volta |
| `spiral_01.VectorStore` (ChromaDB) | `index/vector` (Qdrant) | **Reimplementa** sob `RetrievalBackend`; ChromaDB fica só no dojo |
| `spiral_02.GraphStore` (Neo4j) | `index/graph` (Neo4j) | **Reusa** — já canônico |
| `spiral_02.hybrid_retriever` | `knowledge/rag` (`rag_client`) | **Generaliza** como interface única |
| `spiral_05.{model_router,budget_tracker,circuit_breaker}` | `execution` / `kernel/economics` | **Gradua** como serviço transversal |
| `spiral_03.{orchestrator,tension,fallback}` | `execution/squads` | **Gradua** lógica de orquestração |
| `spiral_04.{cognitive_layer,memory_store}` | `execution/agents` | **Gradua** memória + padrões |
| `spiral_06.{cycle_manager,benchmark_suite,guardrails}` | `observability` + `ops` (CI) | **Gradua** como gates de benchmark/auto-melhoria |
| `rag-score` ledger | `.mecha/governance` | **Promove** a quality gate de maturidade |
| `./data/fastapi_docs/` (corpus) | — | **NUNCA migra** — produção usa o vault canônico |
| `anamnese/` (DNA vendorizado) | `knowledge/vault` | DNA **real** vive no vault; cópia pública fica no dojo |

## 5. Roadmap incremental por fases

> Princípio do ALINHAMENTO: migração **camada por camada, não big-bang**, com o Mecha em
> produção o tempo todo. Cada fase tem checkpoint humano (HITL) e definição de pronto (DoD).

### 5.1 Fase 0 — Contratos como fonte de verdade

Promover os `Protocol`s para `kernel/contracts`, com validação Pydantic/AST.
**DoD:** dojo importa do kernel e `verify_all_spirals()` passa verde. **HITL:** revisão da ABI.

### 5.2 Fase 1 — `rag_client` com backend Qdrant

Implementar `QdrantStore : RetrievalBackend` e plugar o `rag_client` no `index/vector`.
**DoD:** mesma suíte de retrieval do dojo passa contra Qdrant (paridade com ChromaDB).
**HITL:** aprovar provisionamento do pod Qdrant (INFRA_LEGION).

### 5.3 Fase 2 — Graduar Economics

Subir `model_router` + `budget_tracker` como serviço transversal de execução.
**DoD:** queries de produção passam pelo roteador com teto de budget ativo e dashboard de custo.
**HITL:** ratificar limites (`ECONOMICS_DAILY_BUDGET`, thresholds de alerta).

### 5.4 Fase 3 — Graduar Orchestration + Cognitive

Conectar `orchestrator`/tensão aos squads e `memory_store` aos agents.
**DoD:** um squad real usa parada por zero-delta e memória persistente. **HITL:** revisão de squad.

### 5.5 Fase 4 — `rag-score` como gate + observabilidade

Ligar o ledger ao pipeline de PR (piso por dimensão) e exportar telemetria das espirais
graduadas → Prometheus/Grafana. **DoD:** PR é bloqueado se a dimensão correspondente < piso.

### 5.6 Fase 5 — Auto-melhoria sobre o stack canônico

Rodar `cycle_manager` (spiral_06) sobre o stack de produção em modo *guardrailed* (limites
`SOTA_MAX_*`). **DoD:** um ciclo de melhoria roda contra dados reais sem violar guardrails.

## 6. Guardrails e decisões a ratificar

### 6.1 Guardrails de segurança (clean-room preservado)

1. **Fronteira de sentido único:** dado real **nunca** entra no dojo; só contrato/componente sai.
2. **Carta do dojo intacta:** as 7 regras invioláveis continuam valendo dentro de `.mecha/rag-dojo`.
3. **Ephemeral Asset Pruning (Kill-lixo):** artefatos de graduação (zips, capturas) são removidos após o PR — Lei do Claw.
4. **Segredos:** `.env` permanece no pod; nada de credencial real no repo do dojo.

### 6.2 Decisões que o System Design precisa bater o martelo

1. **Qdrant + Neo4j** como índice canônico, ChromaDB confinado ao dojo? *(recomendado — segue o ALINHAMENTO)*
2. **`kernel/contracts`** como dono único da ABI (Protocols → Pydantic)?
3. **`rag-score` como gate de merge** (piso por dimensão) — quem define os pisos?
4. **VECTOR_CORPS** como dono da fronteira de graduação?

### 6.3 Validação (AST + Pydantic + emoji rails)

Este doc deve passar pelo validador de governança antes do merge:
`python .mecha/kernel/validators/dynamic_typing.py --validate .mecha/INTEGRACAO_RAGDOJO_OMEGA_MECHA.md`
— hierarquia H1→H2→H3 sem saltos, frontmatter `emoji_rail` presente.

## 7. Próximo passo

Ratificar as 4 decisões da seção 6.2 no `SYSTEM_DESIGN_INICIAL` e, se aprovado, abrir a
**Fase 0** (promover `contracts.py` → `kernel/contracts`) como primeira PR de graduação,
revisada por Hugo e Felipe.
