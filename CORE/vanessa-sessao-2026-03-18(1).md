---
name: Sessao 2026-03-18
description: Projeto ArcGIS/PostGIS CNES — DDL, scripts max_length, planilha de controle validada
type: project
---

# Sessao 2026-03-18 — Historico

## O que aconteceu nesta sessao

### 1. Contexto de inicio
- Lida ultima sessao (17-18/03) e relatorio de eventos (limpo)
- Rotina de inicio funcionando conforme definido

### 2. Projeto ArcGIS/PostGIS — Base CNES
- Vanessa precisa migrar tabelas do PostgreSQL para PostGIS (ArcGIS Pro)
- Base: `govfed_cnes` (Cadastro Nacional de Estabelecimentos de Saude)
- DDL fonte: `~/Documents/ddls/DDL BASE CNES.sql`
- 8 tabelas no DDL, 7 com campos varchar (109 campos total)
- Problema: todos os campos sao `varchar` sem length definido — precisa medir max_length real

### 3. Script de verificacao gerado
- Arquivo: `~/Documents/ddls/verificacao_max_length_cnes.sql`
- 7 queries SELECT com MAX(LENGTH(campo)) para cada campo varchar
- Sem UNION ALL — campo a campo como colunas separadas
- Tabelas cobertas: tb_atividade_profissional, tb_carga_horaria_sus, tb_controle_gerencia, tb_dados_profissionais_sus, tb_estabelecimento, tb_municipio, tb_turno_atendimento

### 4. Planilha de controle preenchida e validada
- Google Sheets: https://docs.google.com/spreadsheets/d/1sl8ftVgIxZyOcZFh-TCNtjTtYegelqi6JNl33_Cv0cs/
- Vanessa executou as queries e preencheu campo a campo
- Validacao: 109 campos conferidos, nenhum faltando, nenhum sobrando
- 3 typos corrigidos: cb_cbo->co_cbo, st_cbo_regulamento->st_cbo_regulamentado, nu_cpnj->nu_cnpj
- 7 campos com max_length=0 (dados NULL/vazios na base)

### 5. Proximo passo
- Vanessa vai trocar de maquina
- Continuar: usar os max_length da planilha para criar as tabelas no PostGIS com varchar(N) dimensionado
- Considerar margem de ~20-30% acima do max encontrado

### Pendencias gerais
- [ ] Clone dos repos Omega
- [ ] /gsd:new-project
- [ ] Criar tabelas PostGIS com base na planilha de controle
