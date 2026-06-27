---
name: Padrao de codigo da Vanessa
description: Mapa de estilo de codigo analisado em 02/04/2026 — pandas, SQL, classes por dominio, pipelines sequenciais, config externalizada
type: feedback
---

# Padrao de Codigo da Vanessa — Guia pro Claudio

Analisado em 02/04/2026 a partir de: obras_etl (Drive), RelatorioAuxMoradia (Drive), rag-vanessa (GitHub), claudio-bot (GitHub), CGM_etl_base (GitHub).

## Estilo natural

- **Pandas e SQL sao a lingua nativa.** Pensar em DataFrames, merges, groupby, filtros. Queries SQL bem identadas, com CTEs quando precisa.
- **Classes orientadas a dominio.** Cada classe tem responsabilidade clara. Metodos fazem uma coisa. Nao e GOD class.
- **Nomes descritivos.** Prioriza clareza sobre brevidade. Nomes longos sao aceitaveis se dizem o que fazem.
- **Pipeline sequencial.** Processos passo-a-passo numerados, com contagem de registros em cada etapa.
- **Metodos retornam DataFrames ou dicts**, nunca prints soltos.
- **Config externalizada**: YAML (preferido), .env, dataclass. Nunca hardcoded.
- **Heranca simples**: BaseClass -> EspecificaClass. Nao over-engineer.
- **Nomes em portugues** pros logs/output do usuario, **ingles pro codigo** (variaveis, classes, metodos).
- **SQL embutido em strings multi-linha** — jeito natural dela de escrever queries.

## Evolucao observada (antigo -> atual)

- Config: hardcoded -> @dataclass+env -> YAML externo
- Exceptions: nenhuma -> hierarquia completa -> herda do framework
- Logging: zero/print -> Logger com retry -> Rich console
- Type hints: nenhum -> sim (Dict, Set) -> minimo (codigo enxuto)
- Docstrings: curtas PT -> completas Args/Returns/Raises -> pragmaticas
- Pandas: .iterrows()+append (lento) -> operacoes vetorizadas (isin, masks, drop_duplicates)

## Regras pro Claudio ao escrever codigo com ela

1. Respeitar pipeline sequencial — nao abstrair demais
2. Manter config em YAML quando possivel
3. Retornar DataFrames, nao prints
4. Logging com Rich quando for output pro usuario
5. SQL em strings multi-linha, nao ORMs complexos (SQLAlchemy so pra conexao/engine)
6. Explicar decisoes de design com analogias SQL/PostgreSQL
7. Nao forcar type hints pesados — usar quando clarifica, nao por obrigacao
8. Nao adicionar docstrings enormes — pragmaticas, direto ao ponto

**Why:** codigo deve parecer que ela escreveu, nao que um framework gerou. Consistencia com o estilo existente facilita manutencao e aprendizado.

**How to apply:** antes de escrever qualquer codigo novo, verificar se o padrao ta alinhado com essas regras. Se precisar desviar, explicar o motivo.
