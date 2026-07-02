# -*- coding: utf-8 -*-
"""
rag_client — interface UNICA de busca hibrida do MECHA (System Design, decisao 1).
====================================================================================
Facade sobre:
  - Qdrant (vetorial)  -> QdrantRAGClient (qdrant_client_helper.py)
  - Neo4j  (grafo)     -> driver oficial, lazy e fail-safe (mesmo padrao do bridge)

Materializado no Phase 1 do debate O6 (item 8 da matriz, finding E2).
Consumidores-alvo: squad runners, probes do ORCHESTRATOR_CORE, amanda_teams_bot.

Uso:
    from rag_client import RagClient
    rag = RagClient()
    hits = rag.vector_search("reator kafka ghost workers", limit=5)
    rows = rag.graph_query("MATCH (p:SystemPillar) RETURN p.name AS name LIMIT 5")
    ctx  = rag.hybrid_search("como o CDC alimenta o grafo?", limit=5)

Config por env (mesmas convencoes dos modulos existentes):
    QDRANT_URL  (default http://localhost:6333)
    NEO4J_URI   (default bolt://localhost:7687)
    NEO4J_USER  (default neo4j)
    NEO4J_PASS  (default rootroot)
"""

from __future__ import annotations

import logging
import os
from typing import Any, Dict, List, Optional

logger = logging.getLogger("rag_client")

NEO4J_URI = os.environ.get("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.environ.get("NEO4J_USER", "neo4j")
NEO4J_PASS = os.environ.get("NEO4J_PASS", "rootroot")

try:
    from neo4j import GraphDatabase
except ImportError:  # fail-safe: grafo vira no-op
    GraphDatabase = None


class RagClient:
    """Busca hibrida Qdrant + Neo4j atras de uma unica interface."""

    def __init__(
        self,
        vector_client: Optional[Any] = None,
        neo4j_uri: Optional[str] = None,
        neo4j_user: Optional[str] = None,
        neo4j_pass: Optional[str] = None,
    ) -> None:
        self._vector = vector_client        # lazy: so instancia no primeiro uso
        self._driver = None
        self._graph_failed = False
        self._uri = neo4j_uri or NEO4J_URI
        self._auth = (neo4j_user or NEO4J_USER, neo4j_pass or NEO4J_PASS)

    # ---- vetorial (Qdrant) ----------------------------------------------

    @property
    def vector(self) -> Any:
        if self._vector is None:
            from qdrant_client_helper import QdrantRAGClient
            self._vector = QdrantRAGClient()
        return self._vector

    def vector_search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Busca semantica. Retorna [{id, score, text, metadata}]."""
        return self.vector.search(query, limit=limit)

    def upsert(self, text: str, metadata: Optional[Dict[str, Any]] = None) -> str:
        """Indexa um chunk; retorna o point_id."""
        return self.vector.upsert(text, metadata or {})

    # ---- grafo (Neo4j) ---------------------------------------------------

    def _drv(self):
        """Driver lazy e fail-safe (mesmo padrao do Neo4jOrchestrationBridge)."""
        if self._graph_failed or GraphDatabase is None:
            return None
        if self._driver is None:
            try:
                self._driver = GraphDatabase.driver(self._uri, auth=self._auth)
                self._driver.verify_connectivity()
            except Exception as exc:
                self._graph_failed = True
                logger.warning("[RagClient] Neo4j indisponivel (%s) -> grafo em no-op.", exc)
                return None
        return self._driver

    def graph_query(self, cypher: str, **params: Any) -> List[Dict[str, Any]]:
        """Cypher arbitrario. Retorna [] se o grafo estiver offline (no-op)."""
        drv = self._drv()
        if drv is None:
            return []
        try:
            with drv.session() as session:
                return [dict(record) for record in session.run(cypher, **params)]
        except Exception as exc:
            logger.warning("[RagClient] graph_query falhou: %s", exc)
            return []

    def graph_neighbors(self, file_path: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Vizinhos de um chunk no grafo (ContextChunk -[BELONGS_TO]-> SystemPillar)."""
        cypher = (
            "MATCH (c {file_path: $file_path})-[r]-(n) "
            "RETURN type(r) AS rel, labels(n) AS labels, "
            "coalesce(n.name, n.title, n.file_path) AS name LIMIT $limit"
        )
        return self.graph_query(cypher, file_path=file_path, limit=limit)

    # ---- hibrido ---------------------------------------------------------

    def hybrid_search(
        self,
        query: str,
        limit: int = 5,
        with_graph: bool = True,
        neighbors_per_hit: int = 5,
    ) -> List[Dict[str, Any]]:
        """
        Busca vetorial enriquecida com contexto do grafo.
        Cada hit ganha 'graph_context' com os vizinhos do chunk no Neo4j
        (quando o metadata traz file_path e o grafo esta online).
        """
        hits = self.vector_search(query, limit=limit)
        if not with_graph:
            return hits
        for hit in hits:
            file_path = (hit.get("metadata") or {}).get("file_path")
            hit["graph_context"] = (
                self.graph_neighbors(file_path, limit=neighbors_per_hit)
                if file_path else []
            )
        return hits

    def close(self) -> None:
        if self._driver is not None:
            try:
                self._driver.close()
            except Exception:
                pass
            self._driver = None


if __name__ == "__main__":  # pragma: no cover
    logging.basicConfig(level=logging.INFO)
    rag = RagClient()
    print("[rag_client] graph RETURN 1 ->", rag.graph_query("RETURN 1 AS ok"))
    print("[rag_client] vector_search('kafka ghost workers', 2):")
    for h in rag.vector_search("kafka ghost workers", limit=2):
        print(f"  score={h['score']:.4f} text={h['text'][:70]!r}")
    rag.close()
