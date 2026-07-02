# 🧬 Alinhamento de Backends — MECHA ⊕ Omega RAG → Estrutura Unificada

**Data:** 20/06/2026 · **Objetivo:** unir o melhor das duas estruturas, em ciclos de melhoria, até uma topologia canônica única que sirva de base para o System Design.

---

## 1. Pontos fortes de cada estrutura

### MECHA (`.mecha`) — o cérebro de execução
- **M1 · Governança rígida:** contratos Pydantic, validação AST de hierarquia (H1→H2→H3), *emoji rails* semânticos para roteamento e compressão de atenção.
- **M2 · RAG-first ("Lei 2"):** o conhecimento vive em notas/RAG (Obsidian + Qdrant), nunca escondido em configs.
- **M3 · Execução madura e funcional:** Claw (RPA, visão, firewall cognitivo, auto-recuperação), squads multi-agente (Tribunal Hermes, CodeSquad, QASquad), bots Telegram/Teams, dashboard de telemetria. *(209 arquivos reais em `ops`)*
- **M4 · Resiliência local:** Ephemeral Asset Pruning (kill-lixo), escrita atômica, Secure Default State (fail-closed), recuperação automática.
- **M5 · Memória rica:** `CORE` com ~97 notas — base de conhecimento real e versionada.

### Omega RAG — a plataforma de dados/produto
- **O1 · Taxonomia de dados explícita:** `OmegaData/` separa claramente o *data lake* (KnowledgeBase, Intelligence, Inbox, ParentStore, NetworkLogs, Error, Fakes, VectorStore).
- **O2 · Observabilidade nativa:** Grafana + Prometheus já previstos.
- **O3 · Separação produto/consumo:** frontend dedicado (`omega-frontend`, Next.js) + `omega_sdk` (cliente).
- **O4 · Knowledge graph:** `tools/graphify` → `graphify-out/wiki` (visão de grafo do conhecimento).
- **O5 · Segurança proativa:** `honeypots/` + `Fakes/` (iscas/decoys).
- **O6 · Multicanal + ingestão:** Signal CLI + `Omega_Handover_Ingests` (pipeline de entrada).
- **O7 · Topologia intencional:** vault `Topologia_Omega` desenhado antes do código.

> **Observação factual:** hoje o Omega é um **esqueleto vazio** (≈7 arquivos reais; todas as pastas de código/dados sem conteúdo) + venv + config Signal. O MECHA também tem pastas-esqueleto vazias (`kernel/governance/foundation/squads/boxes/behavior`). Ambos seguem o padrão "desenhar a topologia primeiro".

---

## 2. Ciclos de melhoria (fusão)

### Ciclo 0 — Baseline
MECHA = execução + governança concentradas; Omega = dados/observabilidade/UI planejados (vazios). **Costura já existente:** o Claw do MECHA grava *navigation-states* no vault do Omega → prova de que devem se conectar.

### Ciclo 1 — Superposição (união ingênua)
Sobrepor as duas árvores revela **4 conflitos** a resolver:
1. **Dois RAGs:** Qdrant (MECHA) vs `VectorStore` genérico (Omega) / ChromaDB+Neo4j (engine OmegaHuggs).
2. **Duas bases de conhecimento:** `CORE` vs `OmegaData/KnowledgeBase` + dois vaults Obsidian.
3. **Duas convenções de nome:** minúsculas-semânticas (MECHA) vs `PascalCase` (Omega).
4. **Canais espalhados:** Telegram/Teams (MECHA) vs Signal (Omega).

### Ciclo 2 — Resolução de conflitos (decisões)
- **Vetor+Grafo (híbrido):** padronizar **Qdrant** (vetorial, já implementado no MECHA) **+ Neo4j** (grafo, já na visão do `graphify`/engine). Descartar ChromaDB para não manter 3 stores. Tudo atrás de **uma interface `rag_client`** (generalizar o `qdrant_client_helper`).
- **Conhecimento único:** `CORE`/vault Obsidian é a **fonte de verdade**; `OmegaData/KnowledgeBase` vira **derivado/índice** (não duplica). Consolidar os dois vaults em um.
- **Convenção única:** adotar a governança do MECHA (minúsculas + `emoji_rail` + frontmatter + Pydantic/AST) como padrão; preservar os "domínios de dados" legíveis do Omega como subpastas dentro de `data/`.
- **Canais unificados:** camada `interface/channels` (telegram, teams, signal) com adaptador comum.

### Ciclo 3 — Otimização e endurecimento (a "cola")
- **Camadas explícitas** (kernel → execução → conhecimento → índice → dados → ingestão → observabilidade → interface → segurança).
- **Contrato de ingestão único:** fontes → `ingestion` (handover + graphify) → `knowledge` (vault/CORE) → `index` (Qdrant+Neo4j) → consumido por execução/SDK/Studio.
- **Governança transversal:** emoji rails + Pydantic + AST aplicados a **todas** as camadas (inclusive Omega).
- **Observabilidade ligada à execução:** telemetria do Claw (`claw_status.json`) exporta métricas → Prometheus → Grafana.
- **Segurança unificada:** honeypots/Fakes + firewall cognitivo + gestão de segredos (.gitignore/secret manager) numa só camada.
- **Ownership por camada** (ex.: Amanda = interface/execução; Vanessa = índice/dados/ingestão).

---

## 3. Estrutura canônica unificada (proposta)

```
workspace/
├─ kernel/             # contratos + governança + tipos  [MECHA kernel/governance]
│  ├─ contracts/       #   modelos Pydantic compartilhados (coords, payloads, RAG hits)
│  ├─ governance/      #   Lei 2, Ephemeral Asset Pruning (kill-lixo), Secure Default State (fail-closed), vocabulário de emoji rails
│  └─ validators/      #   dynamic_typing.py (AST), checagem de schema
├─ execution/          # cérebro de execução  [MECHA ops/patterns]
│  ├─ claw/            #   loop, visão, firewall cognitivo, recuperação
│  ├─ squads/          #   Tribunal Hermes, CodeSquad, QASquad, orchestrators
│  └─ agents/          #   Amanda (Shadow Processor), Ghost Workers
├─ knowledge/          # FONTE DE VERDADE do conhecimento  [MECHA CORE + Omega KnowledgeBase/Topologia]
│  ├─ vault/           #   Obsidian único (notas + topologia) c/ frontmatter emoji_rail
│  └─ rag/             #   interface rag_client + jobs de ingestão p/ index
├─ index/              # stores de busca  [DECISÃO: Qdrant + Neo4j]
│  ├─ vector/          #   Qdrant
│  └─ graph/           #   Neo4j (alimentado pelo graphify)
├─ data/               # data lake operacional  [Omega OmegaData/*]
│  ├─ inbox/  parent_store/  intelligence/  network_logs/  errors/  fakes/
├─ ingestion/          # pipelines de entrada  [Omega Handover + graphify]
│  ├─ handover/  graphify/  connectors/
├─ observability/      # métricas e saúde  [Omega Grafana/Prometheus + MECHA telemetry]
│  ├─ prometheus/  grafana/  telemetry/   (claw_status, dashboard 8585)
├─ interface/          # consumo  [Omega frontend/SDK + MECHA bots]
│  ├─ studio/          #   Mecha Huggs Workforce Studio (HWorkforceStudio)
│  ├─ sdk/             #   omega_sdk (cliente)
│  └─ channels/        #   telegram, teams, signal (adaptador comum)
├─ security/           # honeypots, decoys (Fakes), segredos  [Omega honeypots + MECHA firewall]
└─ ops/                # build, deploy, .env.example, runbooks
```

### Mapa de migração (de → para)

| MECHA / Omega (origem) | Camada unificada |
|---|---|
| `.mecha/ops/patterns/claw_*` | `execution/claw` |
| `.mecha/ops/patterns/*squad*, *orchestrator*` | `execution/squads` |
| `.mecha/ops/patterns/amanda_*, ghost_worker` | `execution/agents` |
| `.mecha/CORE` + `Omega/Obsidian/*` | `knowledge/vault` |
| `qdrant_client_helper` + `OmegaData/VectorStore` | `index/vector` (Qdrant) |
| `graphify` + engine Neo4j | `index/graph` (Neo4j) |
| `OmegaData/{Inbox,Intelligence,…}` | `data/*` |
| `Omega_Handover_Ingests`, `tools/graphify` | `ingestion/*` |
| `OmegaData/{Grafana,Prometheus}` + dashboard MECHA | `observability/*` |
| `omega-frontend` + `mecha.html`/Studio + `omega_sdk` + bots | `interface/*` |
| `honeypots`, `Fakes`, firewall do Claw, `.gitignore` | `security/*` |

---

## 4. Decisões-chave que o System Design precisa ratificar
1. **Vetor+Grafo = Qdrant + Neo4j** (descartar ChromaDB)? *(recomendado)*
2. **Conhecimento único** com `CORE`/vault como fonte e `OmegaData/KnowledgeBase` como derivado?
3. **Governança do MECHA** (emoji rails + Pydantic + AST) como padrão para tudo?
4. **Migração incremental** (não big-bang), camada por camada, com MECHA em produção?

---

## 5. Próximo passo
Com este alinhamento, seguem os dois entregáveis pedidos: **(a)** relatório para leigo (via Telegram) e **(b)** prompt para o System Design inicial.
