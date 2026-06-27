---
name: ETL Consulta Portal - Trabalho em andamento
description: Contexto do etl_consulta_portal integrado ao etl.py para tb_dw_profissionais_saude (projeto cgm_etl_govfed_cnes da Prefeitura)
type: project
---

# ETL Consulta Portal — Contexto de trabalho

## Onde fica

- Projeto: `C:\Users\vanessa.rsilva\Documents\gitana\cgm_etl_govfed_cnes\`
- Funcao: `etl_consulta_portal()` em `codigos/app/etl.py`
- Orquestrador: `codigos/app/main.py` (chama etl_cnes -> etl_unidades_pcr -> etl_consulta_portal)
- .venv: `codigos/.venv/` (Python 3.11, pandas, psycopg2, sqlalchemy)
- Branch da Vanessa: `branch-gti-vanessa`

## O que faz

Materializa dados das views encadeadas do CNES na tabela `govfed_cnes.tb_dw_profissionais_saude` (alimenta o ArcGIS).

## Tabela destino (DDL)

```sql
CREATE TABLE govfed_cnes.tb_dw_profissionais_saude (
    seq int8 NOT NULL,
    co_unidade varchar(31) NULL,
    no_bairro varchar(40) NULL,
    no_fantasia varchar(60) NULL,
    co_profissional_sus varchar(16) NULL,
    no_profissional varchar(60) NULL,
    co_cbo varchar(6) NULL,
    ds_atividade_profissional varchar(150) NULL
);
```

## Cascata de views

```
vw_dw_estabelecimento (210 linhas)
    JOIN vw_dw_carga_horaria_sus (7988) ON co_unidade
        JOIN vw_dw_dados_profissionais_sus (7872) ON co_profissional_sus
        JOIN vw_dw_atividade_profissional (88, com DISTINCT) ON co_cbo
    = 7988 linhas -> tb_dw_profissionais_saude
```

## Decisoes tecnicas (25/03/2026)

- **Abordagem B escolhida** (query unica com CTE). Abordagem A (4 DataFrames + merge) removida.
- **DISTINCT seguro**: verificado que cada co_cbo tem exatamente uma ds_atividade_profissional (88=88=88)
- **SQLAlchemy** para pd.read_sql (sem warnings), psycopg2 para COPY
- **View de sanidade**: vw_dw_profissionais_saude (7988 linhas, espelha a tabela destino)
- **View incorreta descartada**: pcr_profissionais_saude_cnes (17225 linhas, 23 colunas — granularidade diferente)

## Status: FUNCIONAL

- 7988 linhas, 0% diferenca, zero truncamentos, zero warnings
- Integrado ao pipeline principal (etl.py + main.py)
