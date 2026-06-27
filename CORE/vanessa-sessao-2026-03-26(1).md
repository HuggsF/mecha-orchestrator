---
name: Sessao 2026-03-26
description: ETL CNES sem views + frontend responsivo cgm_etl_gdrive + PIPE-001 e PIPE-002 do Omega implementados
type: project
---

# Sessao 2026-03-26 — Historico

## Prefeitura — cgm_etl_govfed_cnes
- Views eliminadas do pipeline
- Nova funcao etl_dw_estabelecimento(): materializa tabela direto (210 linhas)
- etl_consulta_portal() reescrito com CTEs sobre tabelas brutas (7988 linhas, 0% diff)
- _contagem_sanidade adaptada: compara com tabelas em vez de views
- Pipeline: etl_cnes -> etl_unidades_pcr -> etl_dw_estabelecimento -> etl_consulta_portal
- Pasta data_checks (Soda Core) verificada -- existe, valida tabelas brutas

## Prefeitura — cgm_etl_gdrive
- venv criada com todas as dependencias
- Frontend: janelas dinamicas proporcionais ao monitor
- Cards responsivos com QGraphicsDropShadowEffect (substituiu setGeometry fixo)
- Testado visualmente -- funciona no notebook e monitor externo

## Omega — engine-service (projeto separado)
- PIPE-001 Cache Layer 0: PR #43 aberto
  - Redis 7 Alpine no docker-compose
  - src/cache/cache_layer.py (SHA-256 + TF-IDF + TTL + metricas)
  - src/middleware/cache_middleware.py
  - Gateway integrado (POST /tasks, GET /rag/search, GET /cache/health)
- PIPE-002 Triage Layer 1: PR #44 aberto
  - src/triage/rules.yml (7 dominios, keywords + regex)
  - src/triage/domain_router.py (classificador sem LLM)
  - src/middleware/triage_middleware.py
  - Gateway integrado (POST /tasks, GET /triage/domains, GET /triage/classify)

## Feedback registrado
- Tom Jarvis + Visao + Marvin definido e sincronizado em todos os pontos
- Vanessa e humana, vai falhar, trabalho continua igual

## Pendencias
- [ ] PIPE-003 RAG Layer 2 (depende de ingestores PIPE-005/006)
- [ ] PIPE-005 Ingestor GitHub Issues -> ChromaDB
- [ ] PIPE-006 Ingestor Docs/Wiki -> Neo4j
- [ ] Testar v2 do cgm_etl_gdrive com banco
- [ ] Deploy Claud-IO na Oracle Cloud
- [ ] Deadline M1 MVP Omega: 14/04/2026 (19 dias)
