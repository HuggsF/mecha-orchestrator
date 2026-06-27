# Estado da Validacao — Engine Service Pipeline

## Data: 2026-03-05

## Ambiente local
- Docker Desktop: rodando
- bunker-chroma: healthy, porta 8000
- bunker-neo4j: healthy, porta 7474 (HTTP) / 7687 (Bolt)
- Python venv: C:/labs/inteligence/chunk-generator/venv (Python 3.13.1)
- .env criado com NEO4J e CHROMA apontando para localhost

## Neo4j
- Schema: 47 items criados (constraints + indexes + fulltext)
- Dados de teste inseridos:
  - 4 Chunks (contacts, segments, campaigns, rag)
  - 7 Concepts (CRM, Contacts, Segmentation, Campaigns, RAG, Neo4j, Multi-Tenancy)
  - 9 MENTIONS relationships
  - 7 RELATED_TO relationships
  - 3 Leads (Maria/0.82/GREEN, Joao/0.45/AMBER, Ana/0.91/GREEN)
  - 2 Flows (Onboarding Enterprise/active, Re-engagement Cold/draft)
  - 3 Interactions (campaign_sent, form_submitted, message_received)
  - 2 PART_OF_FLOW, 3 FOR_LEAD relationships
- Login console: http://localhost:7474 — neo4j / neural_link_2024

## ChromaDB
- Collection: course_chunks (10 chunks de teste)
- Embedding: all-MiniLM-L6-v2 (384 dims, local, gratis)
- Busca semantica validada com scores 0.67-0.83

## Testes validados (8/9)
1. ChromaDB insert + search: OK
2. Neo4j schema creation: OK
3. Neo4j data population: OK
4. Fulltext search: OK
5. 2-hop expansion: OK
6. Query Router intent detection: OK
7. Hybrid merge simulation: OK
8. CRM graph (leads + flows + interactions): OK
9. LLM Layer 3: SKIPPED (sem GROQ_API_KEY)

## Gap critico
- Neo4j chunks (4) e ChromaDB chunks (10) sao datasets diferentes
- Para cross-engine boost funcionar em producao, mesmo conteudo precisa estar em AMBOS
- Nao existe sync automatico huggsai-crm <-> engine-service

## Scripts de validacao criados
- C:/labs/inteligence/chunk-generator/validate_neo4j.py
- C:/labs/inteligence/chunk-generator/validate_hybrid_rag.py
