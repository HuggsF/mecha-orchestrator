# Mecha Huggs Workforce Studio (HWS)

> Plataforma unificada **MECHA ⊕ Omega**: agentes (Squads/Amanda) + automação de
> desktop (Claw) + conhecimento (RAG) sobre o vault Obsidian/`CORE`.
> Migração **incremental** — o MECHA segue **em produção** enquanto migramos camada a camada.

<!-- TODO: 1 parágrafo de pitch — o que é, para quem, qual problema resolve. -->

---

## 📑 Índice
- [Visão geral](#-visão-geral)
- [Arquitetura (C4 L2)](#-arquitetura-c4-l2)
- [Status da migração](#-status-da-migração-fases-07)
- [Fase atual — 3 · RAG](#-fase-atual--3--rag)
- [Como rodar](#-como-rodar)
- [Variáveis de ambiente](#-variáveis-de-ambiente-env)
- [Artefatos de design](#-artefatos-de-design)
- [Avisos importantes](#-avisos-importantes)

---

## 🧭 Visão geral

Dois mundos que convergem na plataforma:

| Subsistema | O quê | Onde |
|---|---|---|
| **MECHA Claw** | Robô See-Think-Act de automação de desktop + telemetria | `.mecha/ops/patterns/` |
| **HuggsBot** | Chamados de comunicação via Telegram (SLA PR.COM.001) | `huggsbot/` |
| **FreeScout** | Help desk — persistência dos chamados (:8080) | externo |
| **HWS (alvo)** | Studio + APIs + Squads + RAG (Qdrant/Neo4j) | em migração |

> Fonte de verdade do desenho: [`.mecha/design/SYSTEM_DESIGN_INICIAL.md`](.mecha/design/SYSTEM_DESIGN_INICIAL.md)

---

## 🏗 Arquitetura (C4 L2)

```
Studio (Next.js :3000) ──→ Control API :8585 ──→ Claw Engine (RPA)
Teams ──→ Amanda API :8686 ──→ Squads ──→ rag_client ──→ Qdrant + Neo4j
Ingestion ──→ Vault (CORE) ──→ rag_client ──→ Agents ──→ Telegram / FreeScout
```

**Decisões ratificadas (invioláveis)**
1. Busca híbrida = **Qdrant** (vetor) + **Neo4j** (grafo); ChromaDB depreciado. Acesso único via `rag_client`.
2. Conhecimento único: vault Obsidian/`CORE` é a fonte; `data/knowledge_base` é derivado.
3. Governança MECHA transversal: `emoji_rail` no frontmatter + Pydantic + validação AST.
4. Escrita **atômica** em todo JSON lido pela UI (`claw_status.json`, `claw_preempt.json`).

---

## 🚦 Status da migração (fases 0–7)

| Fase | Camada | Status |
|---|---|---|
| 0 | baseline + smoke | <!-- TODO --> |
| 1 | kernel (contracts + AST) | <!-- TODO --> |
| 2 | execution (Claw, squads, agents) | ✅ MECHA em produção |
| **3** | **knowledge + index (RAG)** | 🟡 **em andamento — ver abaixo** |
| 4 | data + ingestion | ⏳ |
| 5 | observability (Prometheus/Grafana) | ⏳ |
| 6 | interface (Studio + SDK + canais) | ⏳ |
| 7 | security (HMAC, segredos, firewall) | ✅ firewall do Claw pronto |

<!-- TODO: marcar ✅/🟡/⏳ conforme o real de cada fase. -->

---

## 🧠 Fase atual — 3 · RAG

A camada de conhecimento: **um** `rag_client` sobre Qdrant + Neo4j.

- 📄 **Spec completa:** [`docs/FASE_3_RAG.md`](docs/FASE_3_RAG.md) — contrato, payload do Qdrant, grafo Neo4j, `.env`, prompt do Antigravity.
- 🤖 **Prompt pronto:** dentro da IDE → **LEGION → Antigravity Handoff → Fase 3**.
- ⚠️ **Decisão pendente:** `embedding_model` + dimensão da coleção `knowledge` (default proposto: `all-MiniLM-L6-v2`, 384). **Congelar antes de indexar.**

```python
class RagClient(Protocol):
    def search(self, query, limit=3, filters=None) -> list[Hit]: ...
    def upsert(self, docs) -> int: ...
    def graph_query(self, cypher, params=None) -> list[dict]: ...
    def health(self) -> dict: ...   # {qdrant, neo4j, degraded}
```

---

## ▶️ Como rodar

### Produção atual — MECHA Claw + chamados
```powershell
net stop nginx                         # porta 8000 livre p/ o servidor Python
ollama serve                           # firewall cognitivo (1x: ollama pull llama3)
set GEMINI_API_KEY=sua_chave           # opcional · visão multimodal
cd .mecha\ops\patterns
python telegram_bot.py                 # dashboard → http://localhost:8000/mecha.html
python claw_loop.py --target "Obsidian" --goal "abrir a busca global"
```
```bash
# HuggsBot (token SEPARADO do MECHA)
cd huggsbot
python -m venv .venv && .venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env                 # TELEGRAM_TOKEN + (opcional) FREESCOUT_*
python huggsbot.py                     # @Huggies_bbot → /start → /novo
```

### Alvo — HWS (ordem de boot)
```powershell
docker run -p 6333:6333 qdrant/qdrant         # índice vetorial
ollama serve                                  # firewall :11434
uvicorn control_api:app --port 8585           # Control/Dashboard API → Claw
uvicorn amanda_api:app   --port 8686          # Amanda Teams API (HMAC fail-closed)
python -m execution.claw_loop                 # RPA loop
cd interface/studio && npm run dev            # Studio Next.js :3000
# VPS huggs.tech:
docker compose up engine neo4j prometheus grafana   # :8766 / :7687 / :9090 / :3001
```
**Boot:** Qdrant → Ollama → Neo4j → Control/Amanda → Claw → Studio.
**Degradado:** sem Docker/Qdrant, RAG vira opcional e o dashboard segue servindo.

> ⚠️ **1 token por bot:** `telegram_bot.py` usa `TELEGRAM_BOT_TOKEN`; `huggsbot.py` usa `TELEGRAM_TOKEN`. Polling simultâneo no mesmo token derruba o `getUpdates`.
> ⚠️ **nginx ≠ :8000** — senão o servidor Python não sobe (404).

---

## 🔐 Variáveis de ambiente (`.env`)

```
# LLM / visão
OPENROUTER_API_KEY=sk-or-...
GEMINI_API_KEY=...
# RAG
QDRANT_URL=http://localhost:6333
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=...
EMBEDDING_MODEL=all-MiniLM-L6-v2        # confirme dim = 384
# Canais
TELEGRAM_BOT_TOKEN=...                  # MECHA
TELEGRAM_TOKEN=...                      # HuggsBot
AUTHORIZED_CHAT_ID=...
FREESCOUT_URL=http://localhost:8080
FREESCOUT_API_KEY=...
FREESCOUT_MAILBOX_ID=...
# Segurança
TEAMS_WEBHOOK_SECRET=...                # sem ele → 503 fail-closed
```

> Segredos **só** no `.env` (já no `.gitignore`). Nunca cole token em chat/print.

---

## 🎨 Artefatos de design

- **`MECHA IDE.dc.html`** — cockpit da plataforma (Explorer, LEGION, Grafo, Chamados, Claw, Infra).
- `KNOT Studio.dc.html` + `KNOT Studio Playbook.dc.html` — cockpit de megaprompts.
- `Mendas Studio Chamados*.dc.html` — wireframes do sistema de chamados (Teams/Telegram).
- `Mendas Studio Setup.dc.html` + `export/…Como Configurar.pptx` — deck "Como Configurar".

---

## ⚠️ Avisos importantes

- **Token exposto:** revogue no `@BotFather` (`/revoke`) qualquer token que apareceu em chat/print.
- **2 bots, 1 token:** não faça polling simultâneo (MECHA × HuggsBot) no mesmo token.

<!-- TODO: licença, contato, contribuição. -->
