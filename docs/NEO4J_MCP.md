# Neo4j — ingestão da ontologia + MCP de conexão limpa

> Camada `index` do MECHA. Consolida todo acesso Neo4j numa superfície MCP única.
> Data: 2026-07-02.

## O que existe no grafo (bolt://localhost:7687, neo4j/rootroot)

| Origem | Labels | Nós |
|---|---|---|
| second_brain (Obsidian) | Folder, Document | 7.612 (2 + 7.610) |
| Ontologia MECHA v2.1.0 | Layer, Domain, Subdomain, Component | 136 (10 + 9 + 16 + 101) |

Relações da ontologia (131): `(Layer)-[:GROUPS]->(Domain)`,
`(Domain)-[:CONTAINS]->(Subdomain)`, `(Domain|Subdomain)-[:HAS_COMPONENT]->(Component)`.
Chave de componente: `<domain|subdomain>::<nome>` (nomes não são globais — ex.: `__init__.py`).

## Ingestão — `ops/neo4j_ontology_ingest.py`

```powershell
python ops\neo4j_ontology_ingest.py            # MERGE incremental (idempotente)
python ops\neo4j_ontology_ingest.py --reset    # limpa SÓ a ontologia e reingere
python ops\neo4j_ontology_ingest.py --dry-run  # conta, não escreve
```

MERGE em tudo → re-rodável sem duplicar. `--reset` faz DETACH DELETE apenas nos labels
`Layer/Domain/Subdomain/Component` — nunca toca Folder/Document. Verificação pós-ingest
imprime contagens e confirma os 7.612 preservados.

## MCP — `ops/patterns/neo4j_mcp_server.py` (FastMCP, stdio)

Fonte **única** de conexão: um driver lazy, notificações silenciadas (saída limpa),
guard read-only (recusa CREATE/MERGE/DELETE/SET/REMOVE — escrita passa pelos ingestores).

Tools: `neo4j_status`, `cypher_read(query, params)`, `ontology_domains`,
`ontology_layers`, `find_component(name)`, `neighbors(node_key)`.

Por que "conexões mais limpas": antes, verify_ingestion, graphrag_ingester, rag_client e
neo4j_orchestration_bridge cada um abria seu próprio `GraphDatabase.driver` com bolt+rootroot
hardcoded. Agora há um ponto de entrada consultável, com guard e retornos estruturados.

## Wiring no IDE (ação humana)

O registro versionado está em `.mecha/mcp_config.json` (entrada `neo4j-mecha`). Para ativar
no Antigravity/Claude: Settings → MCP → apontar para este arquivo (ou copiar a entrada para
o config global do app) e reiniciar. Não dá para religar o registry de um IDE em execução
por fora — é a única etapa que fica com você.

## Pendências

- `rag_client`, `neo4j_mcp_server`, `neo4j_ontology_ingest` são novos e ainda não estão na
  `mecha_ontology.json` (a ingestão reflete o que o JSON declara). Rodar `generate_ontology.py`
  com validação e reingerir fecha o loop.
- Fase 2 opcional: `Component -[:DOCUMENTED_BY]-> Document` ligando ontologia ao second_brain.
