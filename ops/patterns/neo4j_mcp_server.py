# -*- coding: utf-8 -*-
# ==============================================================================
# NEO4J MCP SERVER - fonte unica de conexao com o Digital Twin (grafo MECHA)
# ==============================================================================
# Consolida todo acesso Neo4j numa unica superficie MCP (FastMCP / stdio).
# Antes: cada script (verify_ingestion, graphrag_ingester, rag_client,
# neo4j_orchestration_bridge) abria seu proprio driver com bolt+rootroot
# hardcoded. Agora: um driver, um guard read-only, retornos estruturados.
#
# Grafo: 7.612 Folder/Document (second_brain) + ontologia MECHA v2.1.0
#        (Layer/Domain/Subdomain/Component via neo4j_ontology_ingest.py).
# ==============================================================================

from __future__ import annotations

import os
import re
from typing import Any, Dict, List, Optional

from mcp.server.fastmcp import FastMCP
from neo4j import GraphDatabase

mcp = FastMCP("MECHA Neo4j Graph")

NEO4J_URI = os.environ.get("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.environ.get("NEO4J_USER", "neo4j")
NEO4J_PASS = os.environ.get("NEO4J_PASS", "rootroot")

# Guard read-only: recusa qualquer clausula de escrita. O MCP é para
# consulta/navegacao; escrita no grafo passa pelos ingestores dedicados.
_WRITE = re.compile(
    r"\b(CREATE|MERGE|DELETE|DETACH|SET|REMOVE|DROP|CALL\s+apoc\.\w+\.(create|delete)|"
    r"LOAD\s+CSV|FOREACH)\b",
    re.IGNORECASE,
)

_driver = None


def _drv():
    """Driver unico, lazy e fail-safe. Notificacoes silenciadas (saida limpa)."""
    global _driver
    if _driver is None:
        try:
            # Neo4j 5.7+: suprime notificacoes benignas (ex.: property key
            # inexistente em coalesce multi-propriedade) — mantem a saida do MCP limpa.
            _driver = GraphDatabase.driver(
                NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASS),
                notifications_min_severity="OFF",
            )
        except (TypeError, ValueError):
            _driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASS))
        _driver.verify_connectivity()
    return _driver


def _read(cypher: str, **params: Any) -> List[Dict[str, Any]]:
    with _drv().session() as session:
        return [dict(r) for r in session.run(cypher, **params)]


@mcp.tool()
def neo4j_status() -> Dict[str, Any]:
    """Status do grafo Neo4j: online, labels, tipos de relacao e contagens por label.
    Use para saber o que existe no Digital Twin antes de consultar."""
    try:
        labels = [r["label"] for r in _read("CALL db.labels() YIELD label RETURN label")]
        rels = [r["relationshipType"] for r in
                _read("CALL db.relationshipTypes() YIELD relationshipType RETURN relationshipType")]
        counts = {}
        for lb in labels:
            counts[lb] = _read(f"MATCH (n:`{lb}`) RETURN count(n) AS c")[0]["c"]
        total_rels = _read("MATCH ()-[r]->() RETURN count(r) AS c")[0]["c"]
        return {"status": "ONLINE", "uri": NEO4J_URI, "labels": labels,
                "relationship_types": rels, "node_counts": counts, "total_relationships": total_rels}
    except Exception as exc:  # noqa: BLE001
        return {"status": "OFFLINE", "error": str(exc)}


@mcp.tool()
def cypher_read(query: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Executa uma consulta Cypher READ-ONLY e retorna as linhas.
    Clausulas de escrita (CREATE/MERGE/DELETE/SET/REMOVE/...) sao recusadas —
    escrita no grafo passa pelos ingestores dedicados, nao pelo MCP.

    Args:
        query: consulta Cypher (apenas leitura).
        params: parametros nomeados opcionais.
    """
    if _WRITE.search(query):
        return {"error": "Consulta recusada: contem clausula de escrita. Este MCP e read-only."}
    try:
        rows = _read(query, **(params or {}))
        return {"count": len(rows), "rows": rows[:200]}
    except Exception as exc:  # noqa: BLE001
        return {"error": str(exc)}


@mcp.tool()
def ontology_domains() -> List[Dict[str, Any]]:
    """Lista os dominios da ontologia MECHA com sua camada (layer) e nº de componentes/subdominios."""
    return _read(
        "MATCH (d:Domain) "
        "OPTIONAL MATCH (l:Layer)-[:GROUPS]->(d) "
        "OPTIONAL MATCH (d)-[:HAS_COMPONENT]->(c:Component) "
        "OPTIONAL MATCH (d)-[:CONTAINS]->(s:Subdomain) "
        "RETURN d.id AS domain, d.kind AS kind, d.path AS path, "
        "collect(DISTINCT l.name) AS layers, count(DISTINCT c) AS components, "
        "count(DISTINCT s) AS subdomains ORDER BY domain"
    )


@mcp.tool()
def ontology_layers() -> List[Dict[str, Any]]:
    """Mapa camada -> dominios (as 10 camadas canonicas do bloco layers v2.1.0)."""
    return _read(
        "MATCH (l:Layer) OPTIONAL MATCH (l)-[:GROUPS]->(d:Domain) "
        "RETURN l.name AS layer, l.description AS description, "
        "collect(d.id) AS domains ORDER BY layer"
    )


@mcp.tool()
def find_component(name: str) -> List[Dict[str, Any]]:
    """Localiza componente(s) da ontologia por nome (match parcial, case-insensitive)
    e mostra o dominio/subdominio pai. Ex.: 'rag_client', 'neo4j', 'dna_passport'."""
    return _read(
        "MATCH (c:Component) WHERE toLower(c.name) CONTAINS toLower($q) "
        "OPTIONAL MATCH (parent)-[:HAS_COMPONENT]->(c) "
        "RETURN c.name AS component, c.type AS type, c.key AS key, "
        "labels(parent)[0] AS parent_type, coalesce(parent.id, '') AS parent "
        "ORDER BY component LIMIT 50",
        q=name,
    )


@mcp.tool()
def neighbors(node_key: str, limit: int = 25) -> Dict[str, Any]:
    """Vizinhos 1-hop de um no, aceitando Domain.id, Subdomain.id, Component.key,
    ou Document/Folder por file_path. Retorna as arestas (tipo, direcao, alvo)."""
    rows = _read(
        "MATCH (n) WHERE n.id = $k OR n.key = $k OR n.file_path = $k OR n.name = $k "
        "WITH n LIMIT 1 "
        "MATCH (n)-[r]-(m) "
        "RETURN labels(n)[0] AS node_type, "
        "coalesce(n.id, n.key, n.file_path, n.name) AS node, "
        "type(r) AS rel, "
        "CASE WHEN startNode(r) = n THEN 'out' ELSE 'in' END AS direction, "
        "labels(m)[0] AS target_type, "
        "coalesce(m.id, m.key, m.file_path, m.name) AS target "
        "LIMIT $limit",
        k=node_key, limit=limit,
    )
    return {"node": node_key, "count": len(rows), "edges": rows}


if __name__ == "__main__":
    # Transport stdio (padrao FastMCP) — plugavel em Antigravity/Claude via mcp_config.
    mcp.run()
