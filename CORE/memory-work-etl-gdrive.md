---
name: ETL GDrive - Trabalho em andamento
description: Contexto dos projetos cgm_etl_gdrive (v1 e v2) - ETL de planilhas locais para PostgreSQL (Prefeitura)
type: project
---

# ETL GDrive — Contexto de trabalho

## Projetos

- **v1 (original)**: `C:\Users\vanessa.rsilva\Documents\gitana\cgm_etl_gdrive\`
  - Branch: `branch-vanessa` (8 commits a frente da master)
  - 3 bugs corrigidos (sem commit): continue, chave_planilha, col_date
  - SQL validation e session close adicionados
  - Assertividade: ~97-98%

- **v2 (reestruturado)**: `C:\Users\vanessa.rsilva\Documents\gitana\cgm_etl_gdrive_v2\`
  - Copia do original com modelo reestruturado
  - Config de mapeamento movida de carga para planilha
  - Frontend reescrito sem Google Drive
  - Tela nova: config_planilha.py (mapeamento individual)
  - venv: `codigos/venv/`
  - Assertividade: ~96-97%

## Modelo v2 (diferenca principal)

```
v1: carga (pasta + schema + tabela + col_map) -> planilha (nome, data)
v2: carga (pasta + descricao + setor) -> planilha (nome, data, schema, tabela, col_map, col_date, col_int, col_required)
```

## Pendencias

- [ ] Conectar v2 ao banco e testar fluxo completo
- [ ] Testar config_planilha.py com dados reais
- [ ] Comparar v1 vs v2 com Vanessa
- [ ] Decidir qual versao seguir
- [ ] Commitar fixes do v1
