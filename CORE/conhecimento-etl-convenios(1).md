---
name: Conhecimento ETL Convenios
description: Padroes tecnicos do ETL galito->lhama — dual write vs script separado, TRUNCATE+COPY, max_length analysis, VARCHAR sizing
type: project
---

# Conhecimento Tecnico — ETL Convenios

## Padrao arquitetural escolhido

**Script separado (Opcao B)** em vez de dual write (Opcao A).

- Opcao A (dual write): ETL de planilhas escreve em 2 bancos simultaneamente. Risco: se destino cair, ETL inteiro falha. Correcoes diretas na origem nao propagam.
- Opcao B (script separado): processo independente faz SELECT na origem e INSERT no destino. Zero impacto no ETL original. Correcoes na origem propagam no proximo ciclo.

Analogia: Opcao A e um trigger de replicacao. Opcao B e um job de ETL classico com schedule.

## Padrao de carga: TRUNCATE + COPY

Mesmo padrao do etl_consulta_portal do CNES:
1. TRUNCATE na tabela destino
2. SELECT * da origem via SQLAlchemy (pd.read_sql)
3. Transforma tipos (TEXT->DATE, ajustes)
4. COPY via psycopg2 copy_expert (StringIO buffer, tab-separated)

Escolhido por simplicidade e idempotencia. Volume e pequeno (<2000 linhas), nao justifica CDC ou merge incremental.

## Analise de VARCHAR — metodologia

Pra cada coluna TEXT no PostgreSQL:
1. SELECT MAX(LENGTH(coluna)), MIN(LENGTH(coluna)), AVG(LENGTH(coluna)), COUNT nulls
2. VARCHAR definido com ~20-40% folga sobre o max real
3. Campos descritivos (objeto, nomes longos): folga maior (~40%)
4. Campos curtos e estaveis (CNPJ, codigos): folga menor (~30%)

Regra: arredondar pra cima pro multiplo de 10 mais proximo, nunca abaixo do max real.

## Padronizacao de tipos entre bancos

Problema encontrado: mesma coluna (data_inicio_vigencia) era DATE no banco de financeiros e TEXT no de nao financeiros. Padronizado pra DATE em ambos. A conversao acontece no transform (pd.to_datetime com errors='coerce').

## Conexao dual no bd.py

Padrão pra ETL entre bancos diferentes:
- get_origin_conn() -> galito (leitura)
- get_dest_conn() -> lhama (escrita)
- Cada um com suas credenciais no .env
- SQLAlchemy connection string pra pd.read_sql
- psycopg2 direto pra COPY (mais performatico)

## expire_on_commit (fix do cgm_etl_gdrive)

Bug: DetachedInstanceError ao iterar objetos SQLAlchemy apos commit intermediario.
Causa: expire_on_commit=True (padrao) invalida objetos em memoria apos qualquer commit.
Fix: SessionLocal = sessionmaker(expire_on_commit=False)
Analogia: manter resultado de SELECT em variavel local em vez de depender de cursor aberto.
