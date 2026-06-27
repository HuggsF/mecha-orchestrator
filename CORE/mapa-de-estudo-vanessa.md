# Mapa de Estudo Completo — Engenharia de Dados com Neo4j, ChromaDB, RAG e Pipelines de IA

## Contexto do Aluno

**Vanessa R. Silva** — Engenheira de Dados com experiencia solida em bancos relacionais (PostgreSQL, MySQL, Oracle) e NoSQL documental (MongoDB). Domina SQL avancado, modelagem relacional, CAP Theorem e PACELC. Trabalha no projeto OmegaHuggsTeam, especificamente no **engine-service**: um pipeline de IA construido com FastAPI + Neo4j + ChromaDB + Groq que implementa Hybrid RAG com 3 motores de busca.

**Dedicacao**: 1 hora por dia de estudo planejado.

**Pre-requisitos ja cumpridos**: Na sessao anterior (05/03/2026), Vanessa recebeu explicacao conceitual dos 6 blocos fundamentais (Neo4j, Embeddings, ChromaDB, RAG, Hybrid RAG, Pipeline de Orquestracao). Este mapa organiza a **pratica, aprofundamento e aplicacao** desses conceitos.

---

## Visao Geral do Mapa

| Fase | Tema | Duracao | Semanas |
|------|------|---------|---------|
| 1 | Neo4j: Cypher na pratica | 10 dias | Semanas 1-2 |
| 2 | ChromaDB: operacoes e busca semantica | 5 dias | Semana 3 |
| 3 | Embeddings: teoria e experimentos | 5 dias | Semana 4 |
| 4 | RAG: construir do zero | 7 dias | Semanas 5-6 (1a metade) |
| 5 | Hybrid RAG: entender e modificar o engine-service | 8 dias | Semanas 6-7 |
| 6 | Topicos avancados (chunking, re-ranking, evaluation) | 10 dias | Semanas 8-9 |
| 7 | Integracao CRM <-> Engine (projeto pratico) | 10 dias | Semanas 10-11 |
| **Total** | | **~55 dias uteis** | **~11 semanas** |

---

## FASE 1 — Neo4j: Cypher na Pratica (10 dias)

### Por que comecar aqui

Neo4j e o banco de grafos que sustenta o engine-service. Ele armazena chunks de conhecimento, conceitos e seus relacionamentos, e tambem todo o grafo CRM (leads, flows, interactions). Sem dominar Cypher (a linguagem de consulta do Neo4j), voce nao consegue debugar, otimizar ou estender o pipeline.

A analogia direta: Neo4j esta para grafos assim como PostgreSQL esta para tabelas. Cypher esta para Neo4j assim como SQL esta para PostgreSQL. A diferenca fundamental e que no SQL voce pensa em tabelas e JOINs; no Cypher voce pensa em nos (vertices) e relacionamentos (arestas) -- e as travessias sao nativas, sem precisar de JOINs.

### Conceitos fundamentais

**Modelo de dados do Neo4j:**
- **No (Node)**: equivalente a uma linha numa tabela. Tem labels (como se fosse o nome da tabela) e properties (como se fossem colunas). Exemplo: `(:Lead {name: "Maria", trust_score: 0.82})`
- **Relacionamento (Relationship)**: equivalente a uma foreign key + JOIN, mas e um cidadao de primeira classe -- tem tipo, direcao e pode ter properties proprias. Exemplo: `(:Lead)-[:PART_OF_FLOW {joined_at: "2026-01-15"}]->(:Flow)`
- **Label**: classifica o no. Um no pode ter multiplos labels. Equivale ao nome da tabela no SQL.
- **Property**: par chave-valor dentro de um no ou relacionamento. Equivale a uma coluna no SQL.

**Comparacao direta SQL vs Cypher:**

| Operacao | SQL (PostgreSQL) | Cypher (Neo4j) |
|----------|-----------------|----------------|
| Buscar todos | `SELECT * FROM leads` | `MATCH (l:Lead) RETURN l` |
| Filtrar | `SELECT * FROM leads WHERE trust > 0.8` | `MATCH (l:Lead) WHERE l.trust_score > 0.8 RETURN l` |
| JOIN | `SELECT l.name, f.name FROM leads l JOIN flows f ON l.flow_id = f.id` | `MATCH (l:Lead)-[:PART_OF_FLOW]->(f:Flow) RETURN l.name, f.name` |
| INSERT | `INSERT INTO leads (name) VALUES ('Ana')` | `CREATE (l:Lead {name: "Ana"})` |
| UPSERT | `INSERT ... ON CONFLICT DO UPDATE` | `MERGE (l:Lead {name: "Ana"}) SET l.trust_score = 0.91` |
| DELETE | `DELETE FROM leads WHERE name = 'Ana'` | `MATCH (l:Lead {name: "Ana"}) DETACH DELETE l` |
| Contar | `SELECT COUNT(*) FROM leads` | `MATCH (l:Lead) RETURN count(l)` |
| Agrupar | `SELECT status, COUNT(*) FROM leads GROUP BY status` | `MATCH (l:Lead) RETURN l.status, count(l)` |

**Index-Free Adjacency**: No PostgreSQL, um JOIN entre leads e flows precisa consultar um indice ou fazer um scan. No Neo4j, cada no tem um ponteiro direto para seus vizinhos na memoria. Isso significa que travessias (ir de A para B para C) sao O(1) por salto, independente do tamanho do banco. E por isso que grafos sao mais rapidos para queries de relacionamento.

**Travessias (o superpoder do Neo4j):**
- 1-hop: `MATCH (a)-[:KNOWS]->(b) RETURN b` — vizinhos diretos
- 2-hop: `MATCH (a)-[:KNOWS]->(b)-[:KNOWS]->(c) RETURN c` — amigos de amigos
- N-hop variavel: `MATCH (a)-[:KNOWS*1..3]->(x) RETURN x` — de 1 a 3 saltos
- No SQL, cada "hop" e um JOIN adicional. Com 3 hops, voce ja tem 3 JOINs. Com N variavel, precisa de recursive CTE (WITH RECURSIVE). No Cypher, e so `*1..N`.

**Fulltext Search**: Neo4j usa Apache Lucene por baixo (o mesmo motor do Elasticsearch). Voce cria um indice fulltext e busca com score de relevancia. Equivalente ao `ts_vector + ts_query` do PostgreSQL, mas com menos configuracao.

### Dia a dia da Fase 1

**Dia 1 — Setup e primeiras queries**
- Verificar que Docker esta rodando com bunker-neo4j ativo
- Acessar http://localhost:7474 (login: neo4j / neural_link_2024)
- Executar queries basicas: MATCH, WHERE, RETURN, LIMIT, ORDER BY
- Exercicio: listar todos os nos por label, contar nos de cada tipo

**Dia 2 — CRUD completo**
- CREATE, SET, REMOVE, DELETE, DETACH DELETE
- MERGE (upsert) — entender a diferenca entre CREATE e MERGE
- Exercicio: criar 5 leads novos, atualizar properties, deletar 2

**Dia 3 — Relacionamentos**
- Criar relacionamentos entre nos existentes
- Query por padrao de relacionamento: `(a)-[r:TIPO]->(b)`
- Filtrar por properties do relacionamento
- Exercicio: criar flows e linkar leads a flows com data de entrada

**Dia 4 — Travessias 1-hop e 2-hop**
- Buscar vizinhos diretos de um no
- Buscar vizinhos de vizinhos (2-hop)
- Entender a direcao: `->` vs `<-` vs `-` (qualquer direcao)
- Exercicio aplicado ao engine-service: dado um Chunk, encontrar todos os Concepts que ele menciona, e depois todos os outros Chunks que mencionam esses mesmos Concepts

**Dia 5 — Travessias de profundidade variavel**
- Sintaxe `*1..N` para travessias de comprimento variavel
- SHORTEST PATH e ALL SHORTEST PATHS
- Exercicio: encontrar o caminho mais curto entre dois Concepts no grafo do engine-service

**Dia 6 — Agregacoes e transformacoes**
- count(), collect(), sum(), avg(), min(), max()
- UNWIND (equivalente ao UNNEST do PostgreSQL)
- WITH (subquery/pipeline — equivalente a CTE)
- Exercicio: para cada Concept, listar quantos Chunks o mencionam e quais sao

**Dia 7 — Fulltext Search**
- Criar indice fulltext: `CREATE FULLTEXT INDEX`
- Buscar com `db.index.fulltext.queryNodes()`
- Entender o score de relevancia (Lucene scoring)
- Exercicio: buscar chunks por texto e comparar resultados fulltext vs CONTAINS

**Dia 8 — Constraints e Indexes**
- UNIQUE constraints, NODE KEY constraints
- Indexes compostos e indexes de property
- EXPLAIN e PROFILE para analisar planos de execucao (equivalente ao EXPLAIN ANALYZE do PostgreSQL)
- Exercicio: analisar o schema do engine-service (47 constraints/indexes) e entender cada um

**Dia 9 — Patterns avancados do engine-service**
- Estudar as queries reais do codigo Python do engine-service
- Entender como o 2-hop expansion e implementado no RAG
- Entender como o trust scoring e calculado no grafo CRM
- Exercicio: reproduzir no console as queries que o engine-service faz programaticamente

**Dia 10 — Revisao e mini-projeto**
- Criar um grafo novo do zero: modelar um dominio que voce conhece (ex: orgaos da Prefeitura, setores, servidores, projetos) como grafo
- Praticar travessias e agregacoes nesse grafo
- Documentar as 10 queries Cypher mais uteis que voce aprendeu

### Referencias — Fase 1

1. **Neo4j Graph Academy** (gratuito, oficial): https://graphacademy.neo4j.com/
   - Curso recomendado: "Neo4j Fundamentals" e "Cypher Fundamentals"
   - Possui certificacao gratuita ao final
2. **Neo4j Cypher Manual** (referencia oficial): https://neo4j.com/docs/cypher-manual/current/
3. **Cypher Cheat Sheet**: https://neo4j.com/docs/cypher-cheat-sheet/
4. **Livro**: "Graph Databases" de Ian Robinson, Jim Webber e Emil Eifrem (O'Reilly) — disponivel gratuitamente no site da Neo4j
5. **YouTube**: Canal oficial Neo4j — playlist "Getting Started with Neo4j"

---

## FASE 2 — ChromaDB: Operacoes e Busca Semantica (5 dias)

### Por que estudar ChromaDB

ChromaDB e o banco de vetores do engine-service. Ele armazena embeddings (representacoes numericas de texto) e permite busca semantica — ou seja, encontrar textos similares por significado, nao por palavras exatas. No pipeline Hybrid RAG, ChromaDB e o motor semantico (peso 0.4, o maior dos 3 motores).

A analogia com PostgreSQL: imagine que voce tem uma tabela `chunks` com uma coluna `embedding` do tipo `vector(384)` (como no pgvector). O ChromaDB e basicamente um banco especializado nisso — so armazena vetores e faz busca por similaridade. E mais simples que pgvector em setup, mas menos flexivel (nao tem SQL, nao tem JOINs, nao tem transacoes).

### Conceitos fundamentais

**Collection**: equivalente a uma tabela. Tem um nome e um embedding function associado.

**Document**: o texto original que voce quer indexar.

**Embedding**: o vetor numerico gerado a partir do documento. Exemplo: o texto "Como cadastrar um lead no CRM" vira um array de 384 numeros decimais como `[0.023, -0.118, 0.045, ...]`.

**Metadata**: pares chave-valor associados a cada documento (como colunas extras). Permitem filtrar resultados.

**ID**: identificador unico de cada documento (como uma primary key).

**Operacoes CRUD:**

| Operacao | SQL (PostgreSQL) | ChromaDB (Python) |
|----------|------------------|--------------------|
| Criar tabela | `CREATE TABLE chunks (...)` | `client.create_collection("chunks")` |
| Inserir | `INSERT INTO chunks VALUES (...)` | `collection.add(ids=["1"], documents=["texto"], metadatas=[{"tipo": "crm"}])` |
| Buscar por similaridade | `SELECT * FROM chunks ORDER BY embedding <=> query_vec LIMIT 5` (pgvector) | `collection.query(query_texts=["minha pergunta"], n_results=5)` |
| Buscar por ID | `SELECT * FROM chunks WHERE id = '1'` | `collection.get(ids=["1"])` |
| Atualizar | `UPDATE chunks SET ... WHERE id = '1'` | `collection.upsert(ids=["1"], documents=["novo texto"])` |
| Deletar | `DELETE FROM chunks WHERE id = '1'` | `collection.delete(ids=["1"])` |
| Contar | `SELECT COUNT(*) FROM chunks` | `collection.count()` |

**Filtros (equivalente a WHERE):**
- `$eq`: igual (`=`)
- `$ne`: diferente (`!=`)
- `$gt`, `$gte`, `$lt`, `$lte`: comparacoes numericas (`>`, `>=`, `<`, `<=`)
- `$in`, `$nin`: lista de valores (`IN`, `NOT IN`)
- `$and`, `$or`: combinacoes logicas (`AND`, `OR`)

**Distancia coseno**: quando voce faz uma busca, o ChromaDB calcula a distancia entre o vetor da sua pergunta e todos os vetores armazenados. Distancia menor = mais similar. O score retornado e essa distancia (0 = identico, 2 = oposto). No engine-service, scores entre 0.3 e 0.8 sao considerados bons resultados.

### Dia a dia da Fase 2

**Dia 11 — Setup e operacoes basicas**
- Verificar que bunker-chroma esta rodando na porta 8000
- Conectar via Python: `chromadb.HttpClient(host="localhost", port=8000)`
- CRUD completo: create_collection, add, get, query, upsert, delete, count
- Exercicio: criar uma collection de teste, inserir 10 documentos em portugues sobre temas variados

**Dia 12 — Busca semantica na pratica**
- Fazer buscas com query_texts em portugues e ingles
- Observar e interpretar os scores de distancia
- Testar: mesma pergunta em PT e EN retorna resultados diferentes?
- Exercicio: criar 5 perguntas e analisar os top-3 resultados de cada uma, explicando por que o ChromaDB retornou aqueles documentos

**Dia 13 — Filtros e metadados**
- Inserir documentos com metadados ricos (categoria, idioma, data, fonte)
- Combinar busca semantica com filtros: "encontre documentos similares a X, mas apenas da categoria Y"
- Exercicio: simular uma busca no engine-service — buscar chunks sobre "segmentacao" filtrando por tenant_id

**Dia 14 — ChromaDB vs pgvector**
- Entender quando usar ChromaDB e quando usar pgvector
- ChromaDB: prototipacao rapida, projetos Python, sem infraestrutura SQL
- pgvector: quando voce ja tem PostgreSQL, quer JOINs com dados relacionais, quer transacoes ACID
- Exercicio: escrever a mesma busca em ChromaDB (Python) e em SQL com pgvector (conceitual), comparar

**Dia 15 — Explorando a collection real do engine-service**
- Conectar na collection `course_chunks` que ja existe
- Explorar os 10 chunks de teste inseridos na validacao
- Fazer buscas que simulam perguntas reais de um usuario do CRM
- Documentar: quais tipos de perguntas retornam bons resultados e quais nao

### Referencias — Fase 2

1. **ChromaDB Documentation** (oficial): https://docs.trychroma.com/
2. **ChromaDB GitHub**: https://github.com/chroma-core/chroma
3. **pgvector** (para comparacao): https://github.com/pgvector/pgvector
4. **Artigo**: "Vector Databases Explained" — Pinecone Learning Center (conceitos transferiveis): https://www.pinecone.io/learn/vector-database/
5. **YouTube**: "ChromaDB Tutorial" — canal Prompt Engineering (pratico, com codigo)

---

## FASE 3 — Embeddings: Teoria e Experimentos (5 dias)

### Por que entender embeddings a fundo

Embeddings sao a ponte entre texto humano e matematica. Toda busca semantica depende da qualidade dos embeddings. Se os embeddings sao ruins, o RAG inteiro e ruim — nao importa quao sofisticado e o resto do pipeline.

A analogia: embeddings estao para busca semantica assim como indexes estao para busca SQL. Um indice ruim faz queries lentas; um embedding ruim faz buscas irrelevantes.

### Conceitos fundamentais

**O que e um embedding**: uma funcao que transforma texto em um vetor de numeros reais de dimensao fixa. O texto "Como cadastrar um lead" vira algo como `[0.023, -0.118, 0.045, ..., 0.067]` — um array de 384 numeros (no caso do all-MiniLM-L6-v2) ou 1536 numeros (no caso do OpenAI text-embedding-3-small).

**Por que funciona**: o modelo de embedding e treinado com bilhoes de textos. Ele aprende que "cachorro" e "cao" devem ter vetores proximos, e que "cachorro" e "hipoteca" devem ter vetores distantes. Isso vale para frases inteiras: "Como cadastrar um lead no CRM" e "Qual o processo para adicionar um novo contato" ficam proximos no espaco vetorial, mesmo sem compartilhar nenhuma palavra.

**Dimensoes**: cada numero no vetor e uma "dimensao". O modelo all-MiniLM-L6-v2 usa 384 dimensoes — ou seja, ele posiciona cada texto num espaco de 384 eixos. Mais dimensoes geralmente capturam mais nuances, mas custam mais espaco e processamento.

**Distancia coseno**: mede o angulo entre dois vetores. Se dois vetores apontam na mesma direcao, a distancia coseno e 0 (identicos). Se apontam em direcoes opostas, e 2 (opostos). Na pratica, textos com distancia < 0.5 sao "sobre o mesmo assunto", e distancia > 1.0 sao "assuntos totalmente diferentes".

**Regra critica**: o modelo usado para gerar embeddings na indexacao DEVE ser o mesmo usado na consulta. Se voce indexou com all-MiniLM-L6-v2 (384 dims) e buscar com OpenAI text-embedding-3-small (1536 dims), os vetores nem tem o mesmo tamanho — nao vai funcionar. Mesmo entre modelos de mesma dimensao, os espacos vetoriais sao diferentes.

**Modelos de embedding usados no projeto:**
- **all-MiniLM-L6-v2**: 384 dimensoes, gratuito, roda local, bom para ingles e razoavel para portugues. Usado no engine-service.
- **OpenAI text-embedding-3-small**: 1536 dimensoes, pago ($0.02/1M tokens), melhor qualidade. Alternativa para producao.
- **multilingual-e5-large**: 1024 dimensoes, gratuito, otimizado para multiplos idiomas incluindo portugues. Boa alternativa para considerar.

### Dia a dia da Fase 3

**Dia 16 — Gerando e visualizando embeddings**
- Instalar sentence-transformers (ja no venv do engine-service)
- Gerar embeddings de frases simples e inspecionar os vetores
- Calcular distancia coseno manualmente (com numpy) entre pares de frases
- Exercicio: gerar embeddings de 10 frases (5 sobre CRM, 5 sobre culinaria) e verificar que as de CRM ficam proximas entre si

**Dia 17 — Comparando modelos**
- Testar all-MiniLM-L6-v2 vs paraphrase-multilingual-MiniLM-L12-v2
- Observar diferencas nos scores para textos em portugues
- Exercicio: mesma busca com modelos diferentes — qual retorna resultados melhores para portugues?

**Dia 18 — Impacto do pre-processamento**
- Testar como limpeza de texto afeta embeddings
- Comparar: texto com acentos vs sem, maiusculas vs minusculas, com stop words vs sem
- Exercicio: gerar embeddings do mesmo texto com diferentes pre-processamentos e medir distancias

**Dia 19 — Embeddings no contexto do engine-service**
- Ler o codigo do engine-service que gera embeddings
- Entender em que momento do pipeline os embeddings sao criados (indexacao vs consulta)
- Mapear: que modelo esta configurado, com que dimensao, onde e chamado no codigo

**Dia 20 — Limites e armadilhas**
- Testar com textos muito longos (o que acontece quando o texto excede o limite do modelo?)
- Testar com textos muito curtos (uma palavra gera embedding util?)
- Testar sinonimos, negacoes e ambiguidades
- Documentar: "o que os embeddings capturam bem" e "o que eles perdem"

### Referencias — Fase 3

1. **SBERT Documentation** (sentence-transformers): https://www.sbert.net/
2. **Hugging Face Model Hub** — buscar modelos de embedding: https://huggingface.co/models?pipeline_tag=sentence-similarity
3. **Artigo**: "What Are Embeddings?" — Vicki Boykis (excelente explicacao visual): https://vickiboykis.com/what_are_embeddings/
4. **Artigo**: "The Illustrated Word2Vec" — Jay Alammar: https://jalammar.github.io/illustrated-word2vec/
5. **Video**: "Embeddings - What they are and why they matter" — canal 3Blue1Brown (visual, matematico)

---

## FASE 4 — RAG: Construir do Zero (7 dias)

### Por que construir do zero

Voce ja entendeu o conceito de RAG (Retrieval-Augmented Generation). Agora vai construir um mini-RAG do zero, sem framework, so com Python + ChromaDB + uma API de LLM. Isso e fundamental para entender o que cada peca faz antes de lidar com a complexidade do engine-service.

### Conceitos fundamentais

**O problema que RAG resolve**: LLMs (como GPT, Claude, Groq) tem conhecimento congelado no tempo do treinamento. Eles nao sabem nada sobre seus dados internos (leads, chunks, regras de negocio do CRM). RAG resolve isso em 3 passos:

1. **Retrieval (Recuperacao)**: buscar nos seus dados (ChromaDB, Neo4j) os trechos mais relevantes para a pergunta do usuario
2. **Augmentation (Aumento)**: montar um prompt que inclui a pergunta + os trechos encontrados
3. **Generation (Geracao)**: enviar esse prompt aumentado para o LLM gerar a resposta

**Analogia com SQL**: RAG e como se voce fizesse um `SELECT` para buscar contexto, depois passasse o resultado como parametro para uma funcao que gera a resposta. O "SELECT" e o Retrieval, os dados retornados sao o Augmentation, e a funcao e o Generation.

**Dois momentos distintos:**
- **Indexacao (offline)**: acontece antes de qualquer pergunta. Voce pega seus documentos, quebra em chunks, gera embeddings, e armazena no ChromaDB. Equivalente a criar a tabela e popular com dados.
- **Consulta (online)**: acontece quando o usuario pergunta algo. Voce gera o embedding da pergunta, busca chunks similares, monta o prompt, e chama o LLM.

### Dia a dia da Fase 4

**Dia 21 — Indexacao: chunking + embedding + armazenamento**
- Pegar um documento real (pode ser uma pagina de documentacao do CRM)
- Quebrar em chunks de 300-500 caracteres com overlap de 50 caracteres
- Gerar embeddings e armazenar no ChromaDB
- Exercicio: indexar pelo menos 3 documentos (15+ chunks)

**Dia 22 — Consulta: busca + montagem de prompt**
- Implementar a busca: receber pergunta, gerar embedding, buscar top-5 chunks
- Montar o prompt: "Com base nos seguintes trechos: [chunks], responda: [pergunta]"
- Exercicio: testar com 5 perguntas e inspecionar o prompt montado (sem chamar LLM ainda)

**Dia 23 — Geracao: chamar o LLM**
- Configurar uma API key (Groq e gratuita para testes: https://console.groq.com/)
- Enviar o prompt aumentado para o LLM e obter a resposta
- Exercicio: fazer 5 perguntas end-to-end e avaliar a qualidade das respostas

**Dia 24 — Melhorando o retrieval**
- Experimentar: n_results=3 vs n_results=5 vs n_results=10
- Observar: mais contexto melhora a resposta ou confunde o LLM?
- Implementar filtro por metadata: buscar apenas chunks de uma categoria especifica
- Exercicio: comparar respostas com diferentes quantidades de contexto

**Dia 25 — Melhorando o chunking**
- Testar diferentes tamanhos de chunk: 200, 500, 1000 caracteres
- Testar com e sem overlap
- Observar o impacto na qualidade da busca e da resposta
- Exercicio: rechunkear os mesmos documentos com 3 estrategias e comparar resultados

**Dia 26 — Tratando falhas**
- O que acontece quando nenhum chunk relevante e encontrado? (score muito alto)
- Implementar threshold: se o melhor score > 1.0, nao usar RAG, responder "nao sei"
- Implementar fallback: se RAG nao encontra nada, responder com conhecimento geral do LLM
- Exercicio: testar com perguntas fora do dominio e verificar que o sistema se comporta bem

**Dia 27 — Revisao: seu mini-RAG completo**
- Documentar a arquitetura: fluxo de indexacao e fluxo de consulta
- Listar as decisoes que voce tomou (tamanho de chunk, modelo de embedding, n_results, threshold)
- Comparar seu mini-RAG com a arquitetura do engine-service: o que o engine-service faz a mais?

### Referencias — Fase 4

1. **Artigo**: "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks" — paper original do RAG (Lewis et al., 2020): https://arxiv.org/abs/2005.11401
2. **Tutorial**: "Build a RAG from Scratch" — LangChain Blog (conceitos transferiveis mesmo sem usar LangChain)
3. **Groq API** (LLM gratuito para testes): https://console.groq.com/docs/quickstart
4. **Video**: "RAG from Scratch" — canal LangChain no YouTube (serie completa, 14 videos)
5. **Artigo**: "Chunking Strategies for LLM Applications" — Pinecone: https://www.pinecone.io/learn/chunking-strategies/

---

## FASE 5 — Hybrid RAG: Entender e Modificar o Engine-Service (8 dias)

### Por que esta fase importa

O engine-service nao usa RAG simples — usa **Hybrid RAG** com 3 motores de busca simultaneos. Essa e a parte mais sofisticada do projeto e a que voce vai manter e evoluir. Aqui voce vai passar de "entender o conceito" para "ler o codigo, entender cada decisao, e ser capaz de modificar".

### Conceitos fundamentais

**3 Motores de Busca:**
1. **ChromaDB (semantico, peso 0.4)**: busca por significado. "Como adicionar contato" encontra "Processo de cadastro de leads". Melhor para perguntas conceituais.
2. **Neo4j 2-hop (relacional, peso 0.3)**: busca por relacionamentos no grafo. Encontra chunks conectados a concepts relacionados. Melhor para perguntas que envolvem relacoes entre entidades.
3. **TF-IDF (keyword, peso 0.3)**: busca por palavras-chave exatas. "configurar webhook" encontra documentos que contem exatamente essas palavras. Melhor para termos tecnicos e nomes proprios.

**Query Router**: antes de buscar, o sistema analisa a pergunta e classifica a intencao:
- `conceptual`: perguntas teoricas ("O que e segmentacao?") — ChromaDB recebe peso maior
- `error`: problemas tecnicos ("Erro ao conectar Neo4j") — TF-IDF recebe peso maior
- `documentation`: como fazer algo ("Como configurar webhook") — pesos equilibrados
- `general`: perguntas genericas — pesos padrao

**Result Merger**: depois que os 3 motores retornam seus resultados, o merger combina tudo:
1. Normaliza os scores de cada motor para escala 0-1
2. Aplica os pesos (0.4, 0.3, 0.3) configurados
3. Remove duplicatas (mesmo chunk retornado por 2+ motores)
4. Aplica **cross-engine boost**: se um chunk aparece em 2+ motores, ganha +15% no score (porque se dois metodos diferentes concordam que ele e relevante, provavelmente e mesmo)

**Exemplo numerico (do que explicamos na sessao anterior):**
- ChromaDB retorna Chunk_A com score 0.72
- Neo4j retorna Chunk_A com score 0.65 e Chunk_B com score 0.80
- TF-IDF retorna Chunk_B com score 0.55
- Apos merge: Chunk_A tem score ponderado + boost (apareceu em 2 motores), Chunk_B tambem tem boost
- Resultado final: ranking combinado que e melhor do que qualquer motor individual

### Dia a dia da Fase 5

**Dia 28 — Mapa do codigo: leitura guiada**
- Ler os arquivos principais do engine-service relacionados ao RAG
- Identificar: onde esta o Query Router, onde estao os 3 motores, onde esta o Merger
- Criar um diagrama (mesmo que textual) do fluxo de uma query pelo pipeline

**Dia 29 — Query Router em detalhe**
- Ler o codigo do router: que regex patterns usa, como decide os pesos
- Testar manualmente: enviar 10 perguntas diferentes e ver como o router classifica cada uma
- Exercicio: identificar 3 tipos de pergunta que o router classifica errado e propor melhoria

**Dia 30 — Motor 1: ChromaDB search no engine-service**
- Ler o codigo que faz a busca no ChromaDB
- Entender: que collection usa, como trata os resultados, como normaliza scores
- Exercicio: adicionar log temporario para ver os resultados brutos do ChromaDB

**Dia 31 — Motor 2: Neo4j 2-hop expansion**
- Ler o codigo que faz a busca no Neo4j
- Entender o padrao: pergunta -> fulltext search -> Chunks encontrados -> Concepts mencionados -> Chunks vizinhos (2-hop)
- Exercicio: executar a query Cypher equivalente no console e comparar com o resultado do codigo

**Dia 32 — Motor 3: TF-IDF**
- Ler o codigo do motor TF-IDF
- Entender: TF (term frequency) e IDF (inverse document frequency)
- Comparacao com SQL: TF-IDF e como um `ts_rank()` do PostgreSQL, mas implementado em Python
- Exercicio: calcular TF-IDF manualmente para 3 documentos e 1 query

**Dia 33 — Result Merger**
- Ler o codigo do merger
- Entender: normalizacao, aplicacao de pesos, dedup, cross-engine boost
- Exercicio: pegar resultados dos 3 motores e calcular o merge manualmente (na mao, com calculadora)

**Dia 34 — Pipeline 4 Layers**
- Ler o codigo completo do pipeline: Cache -> Triage -> RAG -> Full LLM
- Entender: como o cache funciona (SHA-256 exato + embedding semantico)
- Entender: como a triage funciona (regex shortcuts que evitam LLM)
- Exercicio: enviar a mesma pergunta 2x e verificar que a segunda usa cache

**Dia 35 — Modificacao pratica**
- Escolher uma melhoria pequena e implementar (ex: ajustar pesos do Query Router, adicionar novo padrao regex na triage, mudar o threshold de cross-engine boost)
- Testar a mudanca e documentar o impacto
- Exercicio: comparar resultados antes e depois da mudanca com 5 queries de teste

### Referencias — Fase 5

1. **Paper**: "Hybrid Search for RAG" — conceitos de busca hibrida
2. **Codigo-fonte do engine-service**: `C:\labs\inteligence\chunk-generator\` — a melhor referencia e o proprio projeto
3. **TF-IDF explicado**: https://en.wikipedia.org/wiki/Tf%E2%80%93idf (artigo Wikipedia surpreendentemente bom)
4. **Video**: "Building Production RAG Applications" — canal AI Engineer (avancado, pratico)
5. **Artigo**: "Cross-Encoder vs Bi-Encoder for Retrieval" — SBERT docs (para entender trade-offs)

---

## FASE 6 — Topicos Avancados (10 dias)

### Chunking Avancado (Dias 36-38)

**O que e**: estrategias de como quebrar documentos em pedacos menores para indexacao. A qualidade do chunking impacta diretamente a qualidade do RAG.

**Estrategias:**
- **Fixed-size**: chunks de N caracteres com overlap. Simples, mas pode cortar no meio de uma frase.
- **Sentence-based**: cada chunk e um conjunto de frases completas. Respeita limites linguisticos.
- **Paragraph-based**: cada paragrafo e um chunk. Bom para textos bem estruturados.
- **Header-based (Markdown/HTML)**: quebra por headers (H1, H2, H3). Cada secao vira um chunk. Ideal para documentacao tecnica.
- **Semantic chunking**: usa embeddings para detectar mudancas de topico e quebrar ali. Mais sofisticado, mais caro.
- **AST-based (para codigo)**: usa a Abstract Syntax Tree para quebrar codigo por funcao/classe. Relevante se voce indexar codigo-fonte.

**Dia 36**: implementar chunking por sentenca e por paragrafo
**Dia 37**: implementar chunking por headers (Markdown)
**Dia 38**: comparar todas as estrategias no mini-RAG: qual produz melhores resultados?

### Re-ranking (Dias 39-40)

**O que e**: depois da busca retornar os top-N resultados, usar um modelo mais sofisticado (cross-encoder) para reordenar esses resultados. E mais caro, mas mais preciso.

**Analogia SQL**: e como se voce fizesse um `SELECT ... ORDER BY relevance LIMIT 20` (busca rapida), depois aplicasse uma funcao mais cara para reordenar esses 20 resultados antes de pegar os top-5 finais.

**Dia 39**: entender cross-encoder vs bi-encoder, implementar re-ranking com cross-encoder
**Dia 40**: integrar re-ranking no mini-RAG e medir o impacto na qualidade

### RAG Evaluation (Dias 41-43)

**O que e**: metricas para medir se seu RAG esta retornando bons resultados. Sem metricas, voce esta no escuro — nao sabe se uma mudanca melhorou ou piorou o sistema.

**Metricas fundamentais:**
- **Recall@K**: dos documentos relevantes, quantos apareceram nos top-K resultados? (Se tem 3 chunks relevantes e o top-5 retornou 2 deles, recall@5 = 2/3 = 0.67)
- **Precision@K**: dos K resultados retornados, quantos sao realmente relevantes? (Se top-5 retornou 2 relevantes, precision@5 = 2/5 = 0.40)
- **MRR (Mean Reciprocal Rank)**: em que posicao aparece o primeiro resultado relevante? (Se o primeiro relevante esta na posicao 3, RR = 1/3. MRR e a media disso para varias queries)
- **NDCG (Normalized Discounted Cumulative Gain)**: similar a MRR mas considera a posicao de todos os resultados relevantes, nao so o primeiro

**Dia 41**: criar um dataset de avaliacao: 10 perguntas com respostas "corretas" (chunks que deveriam aparecer)
**Dia 42**: implementar calculo de Recall@K, Precision@K e MRR
**Dia 43**: avaliar o engine-service com essas metricas, documentar baseline

### Concept Extraction Automatico (Dias 44-45)

**O que e**: popular o Neo4j automaticamente com concepts extraidos dos chunks, em vez de fazer manualmente. Essencial para escalar o grafo de conhecimento.

**Dia 44**: entender tecnicas de extracao: NER (Named Entity Recognition), keyword extraction (RAKE, YAKE), LLM-based extraction
**Dia 45**: implementar extracao automatica de concepts de novos chunks e inserir no Neo4j

### Referencias — Fase 6

1. **Chunking**: "Chunking Strategies" — Pinecone: https://www.pinecone.io/learn/chunking-strategies/
2. **Re-ranking**: SBERT Cross-Encoders: https://www.sbert.net/examples/applications/cross-encoder/README.html
3. **RAG Evaluation**: RAGAS framework: https://docs.ragas.io/ (framework Python para avaliar RAG)
4. **Concept Extraction**: spaCy NER: https://spacy.io/usage/linguistic-features#named-entities
5. **Paper**: "Evaluating Retrieval-Augmented Generation" — survey de metricas

---

## FASE 7 — Integracao CRM <-> Engine: Projeto Pratico (10 dias)

### O problema

Hoje, huggsai-crm (backend CRM, MongoDB) e engine-service (cerebro IA, Neo4j/ChromaDB) sao ilhas isoladas. Quando um lead e criado no CRM, o engine-service nao sabe. Quando um chunk e adicionado no engine-service, o CRM nao sabe. Essa ponte precisa ser construida.

### O que voce vai desenhar e implementar

Um **event bridge** — um mecanismo de comunicacao assincrono entre os dois sistemas. Quando algo acontece no CRM (lead criado, interaction registrada, flow ativado), um evento e disparado e o engine-service recebe e processa.

**Opcoes de arquitetura:**
1. **Webhooks diretos**: CRM faz POST para engine-service quando algo acontece. Simples, acoplado.
2. **Message queue (Redis/BullMQ)**: CRM publica evento numa fila, engine-service consome. Desacoplado, resiliente. O huggsai-crm ja usa BullMQ.
3. **Change Data Capture (CDC)**: MongoDB Change Streams detecta mudancas e notifica o engine-service. Automatico, mas mais complexo.

### Dia a dia da Fase 7

**Dia 46-47**: Mapear todos os eventos CRM que o engine-service precisa saber (lead criado/atualizado, interaction registrada, flow criado/ativado, contact importado)
**Dia 48-49**: Mapear os endpoints REST do engine-service que recebem esses dados (dos 47 endpoints, quais sao relevantes?)
**Dia 50-51**: Desenhar a arquitetura do event bridge (escolher entre webhooks, BullMQ ou CDC)
**Dia 52-53**: Implementar um POC (Proof of Concept) para o evento mais simples (ex: lead criado no CRM -> no Lead criado no Neo4j)
**Dia 54-55**: Testar end-to-end e documentar a arquitetura para o time

### Referencias — Fase 7

1. **MongoDB Change Streams**: https://www.mongodb.com/docs/manual/changeStreams/
2. **BullMQ Documentation**: https://docs.bullmq.io/
3. **Artigo**: "Event-Driven Architecture" — Martin Fowler: https://martinfowler.com/articles/201701-event-driven.html
4. **Webhooks vs Message Queues**: quando usar cada um, trade-offs
5. **Codigo do huggsai-crm**: `C:\labs\huggsai-crm\` — ver como BullMQ ja e usado

---

## Resumo Visual do Mapa

```
Semana 1-2:  [===== Neo4j/Cypher =====]
Semana 3:    [== ChromaDB ==]
Semana 4:    [== Embeddings ==]
Semana 5-6:  [==== RAG do Zero ====]
Semana 6-7:  [===== Hybrid RAG / Engine =====]
Semana 8-9:  [======= Topicos Avancados =======]
Semana 10-11:[======= Integracao CRM<->Engine =======]
```

## Dicas de uso com NotebookLM

Para cada fase, voce pode criar uma fonte no NotebookLM com:
- Este documento completo (como fonte principal)
- As referencias listadas (artigos, documentacao)
- Suas anotacoes e exercicios resolvidos
- Trechos de codigo do engine-service relevantes para a fase

O NotebookLM vai gerar resumos e podcasts que voce pode ouvir no caminho do trabalho, reforçando os conceitos enquanto a pratica acontece na hora de estudo dedicada.

---

*Documento gerado em 06/03/2026 por Claudio, assistente de engenharia de dados da Vanessa.*
*Projeto: OmegaHuggsTeam/engine-service*
