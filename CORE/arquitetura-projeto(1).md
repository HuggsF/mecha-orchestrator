# Arquitetura do Projeto — OmegaHuggsTeam

## 3 Repositorios

### 1. ai_first_crm (Frontend)
- Repo: OmegaHuggsTeam/ai_first_crm
- Local: C:\labs\crm_hggs\
- Stack: React 18 + Vite + TypeScript + TailwindCSS + shadcn/ui
- 35+ paginas: Dashboard, Audience, Segments, Campaigns, Conversions, Analytics, Flows
- AI: GPT-4o-mini apenas para gerar regras de segmentacao
- Neo4j: NAO | ChromaDB: NAO | RAG: NAO
- Deploy: Docker + Fly.io (dev/staging/prod)
- Backend APIs: platform-api (Fly.io), behavior-agent-api, analytics-tracker-api

### 2. huggsai-crm (Backend CRM)
- Repo: OmegaHuggsTeam/huggsai-crm
- Local: C:\labs\huggsai-crm\
- Stack: Express + TypeScript + MongoDB 7 + Redis 7 + BullMQ
- Implementado: Auth JWT, Contacts CRUD, Companies, Dashboard, tenant-middleware
- 91.47% cobertura testes (51 testes)
- 9 microservicos PLANEJADOS (Tracker, Segments, Behavior, Ingestion, Workers, Scoring, Journey AI, Integrations)
- Neo4j/ChromaDB/RAG: apenas no blueprint, nao implementado
- DDD: 7 bounded contexts (Identity, Audience, Engage, Insight, Capture, Connect, Platform)
- Producao: crm.huggs.tech (VPS Hostinger porta 3010)

### 3. engine-service (Cerebro IA)
- Repo: OmegaHuggsTeam/engine-service
- Local: C:\labs\inteligence\chunk-generator\
- Stack: Python 3.11+ + FastAPI + Neo4j 5 + ChromaDB + Groq
- Sovereign Gateway: porta 8766, 47 REST + 5 WebSocket
- Pipeline 4 layers: Cache -> Triage -> RAG -> Full LLM
- Hybrid RAG: ChromaDB (0.4) + Neo4j 2-hop (0.3) + TF-IDF (0.3)
- 19+ agentes especializados
- CRM self-sovereign: Lead/Flow/Interaction como nos Neo4j
- Trust scoring automatico (0-1)
- Producao: api.huggs.tech (VPS Hostinger porta 8766)

## Fluxo de dados
```
Frontend (ai_first_crm:5173)
    -> Backend (huggsai-crm:3010)
        -> Engine (engine-service:8766)
            -> ChromaDB (:8000) + Neo4j (:7474/7687)
```

## Gap de integracao
- huggsai-crm e engine-service NAO se comunicam automaticamente
- Dados CRM precisam ser pushed via REST API ou webhook
- Vanessa vai desenhar essa ponte (webhook/event bridge)

## Divisao de trabalho
- Amanda (@Mendasz): frontend + backend CRM (produto, UI/UX, fluxos)
- Vanessa (@Vr-Farias): engine-service (dados, Neo4j, ChromaDB, RAG, pipelines)

## Infraestrutura
- VPS Hostinger: 187.124.88.71, Ubuntu 24.04, 32GB RAM
- Dominios: huggs.tech (principal), huggsai.com (secundario)
- Docker em producao: Neo4j, ChromaDB, Evidence, Gateway
- SSL: Certbot/Let's Encrypt
- Acesso SSH: ssh -i ~/.ssh/omegahuggsai-vps root@187.124.88.71
