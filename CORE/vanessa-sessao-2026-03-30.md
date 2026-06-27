---
name: Sessao 2026-03-30
description: RAG-Vanessa criado, curriculo jr montado, cgm_etl_convenios criado (3 tabelas galito->lhama), ChromaDB explicado
type: project
---

# Sessao 2026-03-30 — Historico

## O que aconteceu nesta sessao

### 1. RAG-Vanessa — Second Brain
- Vanessa queria entender RAG como objetivo concreto antes de executar
- Explicado como "SELECT antes do prompt" com analogia SQL (Retrieval = SELECT, Augmented = JOIN no prompt, Generation = LLM responde)
- ChromaDB explicado como "PostgreSQL dos vetores" — guarda embeddings, busca por similaridade semantica
- Decisao: criar como repo privado no GitHub, nao atrelado ao notebook do trabalho
- Repo criado: https://github.com/Vr-Farias/rag-vanessa
- Estrutura: ingestors/ (base.py + markdown.py), search/ (query.py), config/ (sources.yml), tests/
- Embeddings locais (all-MiniLM-L6-v2), zero API paga
- Base ChromaDB configurada pra ficar no Google Drive: G:\Meu Drive\Claudio\rag-data\chromadb\
- Fontes planejadas: memorias Claudio, Notion, GitHub Issues, .txt/.sql/.py
- Preocupacao com seguranca do Drive levantada — Cryptomator sugerido como solucao curto prazo

### 2. Curriculo para Junior (Mateus Basilio)
- Vanessa auxiliando um jr que ta comecando do zero (1o periodo ADS SENAC, Alura, sem experiencia tech)
- Diagnosticado: curriculo sem objetivo, sem projetos, skills genericas, sem GitHub/LinkedIn
- Curriculo reformulado: objetivo claro, experiencia de pizzaria incluida, conhecimentos por area
- HTML estilizado gerado (curriculo-mateus-basilio.html), salvo em Downloads
- Design: ATS-friendly, 1 pagina, cor unica, grid de skills, sem graficos
- Lista de acoes urgentes pro jr: subir repos no GitHub, arrumar perfil, LinkedIn ativo, 1 projeto simples
- GitHub dele: github.com/mateusbasilio53-cmd (0 repos, criado 07/03/2026)
- LinkedIn: 3 conexoes, zero publicacoes, Hugo e conexao em comum

### 3. cgm_etl_convenios — ETL galito -> lhama
- Novo projeto criado em ~/Documents/gitana/cgm_etl_convenios/
- Padrao de ETL tipo B (script separado, galito -> lhama) — mesmo estilo do etl_consulta_portal do CNES
- Opcao A (dual write) descartada por risco de acoplar o ETL de planilhas a dois bancos

**3 tabelas configuradas:**
- bi_portal.ext_convenios_finaceiros (1863 linhas) — galito -> lhama
- bi_portal.ext_convenios_nao_finaceiros (75 linhas) — galito -> lhama
- pcr_siconv.vw_portal_consulta_convenios_receita (357 linhas) — view no galito -> tabela materializada no lhama

**Analise de max_length realizada nas 3:**
- Todas as colunas TEXT mapeadas pra VARCHAR com folga (~20-40%)
- Colunas de data padronizadas pra DATE em todas as tabelas
- Tabela nao_finaceiros tinha data_inicio/fim como TEXT, convertida pra DATE
- objeto_proposta da view tem max 3190 chars, definido VARCHAR(4000)

**Estrutura do projeto (padrao cgm_etl_*):**
- codigos/app/ — bd.py (2 conexoes), etl.py (extract/transform/load), main.py (orquestrador com --dry-run e --tabela)
- codigos/database/ — create_tables.sql (DDL das 3 tabelas)
- Jenkinsfile, docker-compose.yml, Dockerfile, README.md, .gitignore
- .venv criada com dependencias instaladas

**Decisao tecnica:**
- ETL faz TRUNCATE + COPY (limpa e recarrega) — mesmo padrao do CNES
- Cada tabela tem config independente (origin_query, dest_schema, dest_tabela, colunas_date)
- Pode rodar tudo junto ou tabela individual

**Fix aplicado na sessao anterior (27/03) no cgm_etl_gdrive:**
- expire_on_commit=False no SessionLocal — resolveu DetachedInstanceError

### 4. Permissoes no galito
- Usuario usr_gti_etl agora tem SELECT na view pcr_siconv.vw_portal_consulta_convenios_receita
- Nao tem acesso a tb_propostas, tb_convenios, tb_desembolsos (tabelas fonte da view)
- Tem acesso a tb_portal_consulta_convenios_receita (203 linhas)

### Pendencias
- [ ] RAG-Vanessa: clonar no desktop e rodar primeiro teste
- [ ] cgm_etl_convenios: preencher .env do lhama e testar dry-run
- [ ] cgm_etl_convenios: rodar ETL completo quando tabelas existirem no lhama
- [ ] Claud-IO: PR #3 aberta, deploy Railway pendente
- [ ] Omega: PIPE-003/005/006 + clone repos + /gsd:new-project
- [ ] Deadline M1 MVP Omega: 14/04/2026 (15 dias)
- [ ] Relatorio de eventos: verificar task agendada
