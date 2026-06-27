---
name: Conhecimento ArcGIS + SDE + PostgreSQL
description: Tipos de data (DATE vs TIMESTAMPTZ), registro geodatabase enterprise, limpeza SDE metadata, Arcade formatacao
type: project
---

# Conhecimento Tecnico — ArcGIS + SDE + PostgreSQL

## Tipos de data: PostgreSQL vs ArcGIS

| Tipo PostgreSQL | Bytes | ArcGIS reconhece como |
|----------------|-------|----------------------|
| DATE | 4 | "Somente Data" |
| TIMESTAMP | 8 | Pode nao reconhecer corretamente |
| TIMESTAMPTZ | 8 | "Data e Hora" (correto) |

**Regra:** sempre usar TIMESTAMPTZ pra campos de data em tabelas que serao registradas como geodatabase no ArcGIS Enterprise.

## Conversao DATE -> TIMESTAMPTZ

```sql
ALTER TABLE schema.tabela
    ALTER COLUMN coluna TYPE TIMESTAMPTZ USING coluna::timestamptz;
```

- Reversivel: `ALTER ... TYPE DATE USING coluna::date`
- Nao perde dados: DATE vira `2025-12-31 00:00:00-03`
- Se nao tem hora, fica 00:00:00 (meia-noite)

## Registro geodatabase enterprise (SDE)

O ArcGIS Enterprise armazena metadata em 4 tabelas no schema `sde`:

| Tabela | O que guarda |
|--------|-------------|
| sde.sde_table_registry | Tabelas registradas (registration_id, table_name, owner) |
| sde.sde_column_registry | Colunas de cada tabela (column_name, sde_type, column_size) |
| sde.gdb_items | Items do geodatabase (objectid, uuid, name, type) |
| sde.gdb_itemrelationships | Relacoes entre items (destid, originid como UUID varchar) |

**CRITICO:** O sde_column_registry guarda `column_size` que prevalece sobre o tipo real do PostgreSQL. Se voce faz ALTER no banco mas nao atualiza o SDE registry, o ArcGIS continua usando o tipo antigo.

## Problema: apagar projeto local NAO limpa o banco

Apagar a pasta `.aprx` no desktop remove o projeto local, mas o registro geodatabase fica no PostgreSQL. O ArcGIS nao oferece "Register with Geodatabase" de novo porque pra ele ja ta registrado.

## Solucao: limpeza manual do registro SDE

Ordem de DELETE (dependencias primeiro):
1. `DELETE FROM sde.gdb_itemrelationships WHERE destid = ANY(uuids) OR originid = ANY(uuids)`
2. `DELETE FROM sde.gdb_items WHERE uuid = ANY(uuids)`
3. `DELETE FROM sde.sde_column_registry WHERE table_name LIKE '%filtro%'`
4. `DELETE FROM sde.sde_table_registry WHERE table_name LIKE '%filtro%'`

Depois: recriar projeto no ArcGIS Pro e re-registrar as tabelas. Ele le os tipos atuais do banco.

**CUIDADO:** gdb_itemrelationships usa UUID (varchar), nao integer. Cast errado da erro.

## Arcade — formatacao de data no Dashboard

```
Text($datapoint.campo_data, 'DD/MM/Y')    // 31/03/2026
```

Null-safe:
```
IIF(IsEmpty($datapoint.campo), '', Text($datapoint.campo, 'DD/MM/Y'))
```

Wrap de texto: toggle "Pairar Texto" nas configuracoes da tabela.
Truncamento: `Left($datapoint.campo, 200) + '...'`
