---
name: Projeto ArcGIS Prefeitura
description: Migracao de dashboards Power BI para ArcGIS/PostGIS — base CNES (govfed_cnes) na Prefeitura do Recife
type: project
---

Vanessa esta migrando dashboards de Power BI para ArcGIS na Prefeitura do Recife.

**Status (2026-03-18):**
- Banco original: PostgreSQL, schema `govfed_cnes` (CNES — Cadastro Nacional de Estabelecimentos de Saude)
- DDL fonte: `~/Documents/ddls/DDL BASE CNES.sql`
- 8 tabelas, 109 campos varchar mapeados
- Script de max_length gerado: `~/Documents/ddls/verificacao_max_length_cnes.sql`
- Planilha de controle preenchida e validada: https://docs.google.com/spreadsheets/d/1sl8ftVgIxZyOcZFh-TCNtjTtYegelqi6JNl33_Cv0cs/
- Proximo passo: criar tabelas no PostGIS com varchar(N) dimensionado a partir da planilha

**Estrategia:** criar paineis com views/copia agora, trocar pra fonte original depois. Manter schema identico.

**Why:** projeto do trabalho na Prefeitura, paralelo ao OmegaHuggsTeam.

**How to apply:** quando Vanessa perguntar sobre ArcGIS, PostGIS, CNES, ou base da Prefeitura, este e o contexto. Banco e PostgreSQL. Consultar a planilha de controle para os tamanhos definidos.
