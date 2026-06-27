# Roteiro de Aprendizado — Vanessa

## Base de conhecimento ja consolidada
- SQL avancado: PostgreSQL, MySQL, Oracle
- NoSQL: MongoDB
- Teoria: CAP Theorem, PACELC
- Dados: analise, engenharia, ETL

## 6 Blocos de aprendizado (definidos em 2026-03-05)

### Bloco 1: Neo4j (modelagem + Cypher) — PRIORIDADE ALTA
- Status: EXPLICADO, exercicios propostos
- Coberto: modelo mental (nos/relacionamentos vs tabelas/JOINs), index-free adjacency
- Cypher: MATCH, CREATE, MERGE (upsert), SET, DELETE, DETACH DELETE
- Travessias: 1-hop, 2-hop, N-hop variavel (*1..3)
- Fulltext search (Lucene), comparacao com ts_vector do PostgreSQL
- Constraints e indexes, comparacao com PRIMARY KEY/UNIQUE do SQL
- Exercicios propostos: 5 queries no console Neo4j (http://localhost:7474)

### Bloco 2: Embeddings e Vetores — PRIORIDADE ALTA
- Status: EXPLICADO
- Coberto: o que e embedding, dimensoes, distancia coseno, score de similaridade
- Modelos: all-MiniLM-L6-v2 (384d, gratis), OpenAI text-embedding-3-small (1536d, pago)
- Regra critica: mesmo modelo na indexacao e na consulta

### Bloco 3: ChromaDB (operacoes + busca) — PRIORIDADE ALTA
- Status: EXPLICADO, exercicios propostos
- CRUD completo: add, query, get, upsert, delete, count
- Filtros: $and, $or, $eq, $ne, $gt, $gte, $lt, $lte, $in, $nin
- Comparacao com pgvector (PostgreSQL) — pros e contras
- Exercicios propostos: buscas em PT e EN no terminal Python

### Bloco 4: RAG (conceito + arquitetura) — PRIORIDADE MEDIA
- Status: EXPLICADO
- Coberto: problema que resolve (alucinacao), 3 passos (Retrieval, Augmentation, Generation)
- Dois momentos: Indexacao (offline) vs Consulta (online)
- Fatores de qualidade: chunks, embeddings, retrieval, grafo

### Bloco 5: Hybrid RAG (3 motores + merge) — PRIORIDADE MEDIA
- Status: EXPLICADO com exemplo numerico completo
- Query Router: regex patterns, pesos adaptativos por tipo de query
- 3 motores: ChromaDB (semantico 0.4), Neo4j (relacional 0.3), TF-IDF (keyword 0.3)
- Result Merger: normalizacao, pesos, dedup, cross-engine boost (+15%)
- Exemplo calculado passo a passo com scores reais

### Bloco 6: Pipeline de Orquestracao — PRIORIDADE APOS OS OUTROS
- Status: EXPLICADO
- 4 layers: Cache ($0) -> Triage (~$0.0001) -> RAG (~$0.01) -> Full LLM (~$0.50)
- Cache: exato (SHA-256) + semantico (embedding similarity)
- Triage: regex shortcuts que evitam LLM
- Economia: ~90% vs mandar tudo pro LLM

## Trilha Alpha TM (Alura / Prefeitura) — separada do Omega

### Bloco 1: Modelagem e Logica Relacional — CONCLUIDO (22/03/2026)
- Status: REVISADO via audio NotebookLM + transcricao
- Coberto: MER (conceitual), logico (tipos/chaves), fisico (DDL)
- Normalizacao ate 3FN, atributos derivados (calcular vs armazenar)
- Desnormalizacao proposital em cenarios de alto trafego
- Caso real: incidente da virgula (2012) — modelagem como seguranca
- Audio original: `G:\Meu Drive\Estudo\A_arquitetura_invisível_dos_bancos_de_dados.m4a`
- Transcricao: `C:\Users\vanes\OneDrive\Documentos\claude\transcricao.md`
- Gemini cobre esta trilha (suporte emocional + fundamentacao teorica)

## Proximos topicos (ainda nao cobertos) — Omega
1. Estrategias de chunking avancado (por paragrafos, headers, AST)
2. Re-ranking de resultados RAG
3. Concept extraction automatico (popular Neo4j automaticamente)
4. Evaluation de RAG (recall@k, precision@k, MRR)
5. Integracao CRM<->Engine (webhook/event bridge) — Vanessa vai desenhar

## Estilo de ensino que funciona com Vanessa
- Analogias com o mundo real (biblioteca, GPS, especialistas)
- Comparacoes constantes com PostgreSQL/SQL (ela domina)
- Exemplos numericos calculados passo a passo
- Codigo real do projeto, nao exemplos genericos
- Fundamentos antes de execucao — ela nao aceita "confia em mim"
