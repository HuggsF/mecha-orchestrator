# -*- coding: utf-8 -*-
"""
neo4j_ontology_ingest — projeta mecha_ontology.json no grafo Neo4j.
====================================================================
Espelha a ontologia curada (v2.1.0) como grafo consultavel, ao lado
dos nos Folder/Document ja existentes (second_brain).

Grafo produzido:
  (:Layer {name, description})
  (:Domain {id, kind, path, description})
  (:Subdomain {id, description})
  (:Component {key, name, type})

  (Layer)-[:GROUPS]->(Domain)
  (Domain)-[:CONTAINS]->(Subdomain)
  (Domain)-[:HAS_COMPONENT]->(Component)
  (Subdomain)-[:HAS_COMPONENT]->(Component)

Idempotente: tudo via MERGE. `--reset` faz DETACH DELETE apenas nos
labels de ontologia antes de reingerir (nunca toca Folder/Document).

Uso:
    python neo4j_ontology_ingest.py                 # merge incremental
    python neo4j_ontology_ingest.py --reset         # limpa ontologia e reingere
    python neo4j_ontology_ingest.py --dry-run       # so conta, nao escreve
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

from neo4j import GraphDatabase

ONTOLOGY_LABELS = ("Layer", "Domain", "Subdomain", "Component")
_HERE = Path(__file__).resolve().parent
DEFAULT_ONTOLOGY = _HERE.parent / "mecha_ontology.json"

NEO4J_URI = os.environ.get("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.environ.get("NEO4J_USER", "neo4j")
NEO4J_PASS = os.environ.get("NEO4J_PASS", "rootroot")


def _norm_path(declared: str) -> str:
    p = (declared or "").replace("\\", "/")
    return p[len(".mecha/"):] if p.startswith(".mecha/") else p


def ingest(session, ontology: dict, stamp: str) -> dict:
    counts = {"layers": 0, "domains": 0, "subdomains": 0, "components": 0, "rels": 0}

    # Domains + subdomains + components
    for dom in ontology.get("domains", []):
        did = dom["id"]
        session.run(
            "MERGE (d:Domain {id:$id}) "
            "SET d.kind=$kind, d.path=$path, d.description=$desc, d.synced_at=$stamp",
            id=did, kind=dom.get("type", ""), path=_norm_path(dom.get("path", did)),
            desc=dom.get("description", ""), stamp=stamp,
        )
        counts["domains"] += 1

        for comp in dom.get("components", []):
            name = comp.get("name", "").rstrip("/")
            if not name:
                continue
            key = f"{did}::{name}"
            session.run(
                "MERGE (c:Component {key:$key}) SET c.name=$name, c.type=$type, c.synced_at=$stamp "
                "WITH c MATCH (d:Domain {id:$did}) MERGE (d)-[:HAS_COMPONENT]->(c)",
                key=key, name=name, type=comp.get("type", ""), stamp=stamp, did=did,
            )
            counts["components"] += 1
            counts["rels"] += 1

        for sub in dom.get("subdomains", []):
            sid = sub["id"]
            session.run(
                "MERGE (s:Subdomain {id:$id}) SET s.description=$desc, s.synced_at=$stamp "
                "WITH s MATCH (d:Domain {id:$did}) MERGE (d)-[:CONTAINS]->(s)",
                id=sid, desc=sub.get("description", ""), stamp=stamp, did=did,
            )
            counts["subdomains"] += 1
            counts["rels"] += 1

            for comp in sub.get("components", []):
                name = comp.get("name", "").rstrip("/")
                if not name:
                    continue
                key = f"{sid}::{name}"
                session.run(
                    "MERGE (c:Component {key:$key}) SET c.name=$name, c.type=$type, c.synced_at=$stamp "
                    "WITH c MATCH (s:Subdomain {id:$sid}) MERGE (s)-[:HAS_COMPONENT]->(c)",
                    key=key, name=name, type=comp.get("type", ""), stamp=stamp, sid=sid,
                )
                counts["components"] += 1
                counts["rels"] += 1

    # Layers -> Domains (bloco layers da v2.1.0)
    for lname, ldata in (ontology.get("layers") or {}).items():
        session.run(
            "MERGE (l:Layer {name:$name}) SET l.description=$desc, l.synced_at=$stamp",
            name=lname, desc=ldata.get("description", ""), stamp=stamp,
        )
        counts["layers"] += 1
        for did in ldata.get("domains", []):
            session.run(
                "MATCH (l:Layer {name:$name}), (d:Domain {id:$did}) MERGE (l)-[:GROUPS]->(d)",
                name=lname, did=did,
            )
            counts["rels"] += 1

    return counts


def reset_ontology(session) -> int:
    """DETACH DELETE apenas nos labels de ontologia (preserva Folder/Document)."""
    total = 0
    for label in ONTOLOGY_LABELS:
        total += session.run(f"MATCH (n:{label}) RETURN count(n) AS c").single()["c"]
        session.run(f"MATCH (n:{label}) DETACH DELETE n")
    return total


def main() -> int:
    ap = argparse.ArgumentParser(description="Ingest mecha_ontology.json into Neo4j")
    ap.add_argument("--ontology", default=str(DEFAULT_ONTOLOGY))
    ap.add_argument("--reset", action="store_true", help="limpa a ontologia antes de reingerir")
    ap.add_argument("--dry-run", action="store_true", help="conta e valida, nao escreve")
    args = ap.parse_args()

    data = json.loads(Path(args.ontology).read_text(encoding="utf-8"))
    n_dom = len(data.get("domains", []))
    n_layers = len(data.get("layers") or {})
    print(f"[ingest] ontologia v{data.get('version')} — {n_dom} dominios, {n_layers} layers")

    if args.dry_run:
        print("[ingest] dry-run: nada escrito.")
        return 0

    stamp = datetime.now(timezone.utc).isoformat()
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASS))
    try:
        driver.verify_connectivity()
        with driver.session() as session:
            if args.reset:
                removed = reset_ontology(session)
                print(f"[ingest] reset: {removed} nos de ontologia removidos")
            counts = ingest(session, data, stamp)
            print(f"[ingest] OK: {counts}")
            # Verificacao pos-ingest
            for label in ONTOLOGY_LABELS:
                c = session.run(f"MATCH (n:{label}) RETURN count(n) AS c").single()["c"]
                print(f"  {label}: {c}")
            rels = session.run(
                "MATCH ()-[r:GROUPS|CONTAINS|HAS_COMPONENT]->() RETURN count(r) AS c"
            ).single()["c"]
            print(f"  rels (ontologia): {rels}")
            preserved = session.run(
                "MATCH (n) WHERE n:Folder OR n:Document RETURN count(n) AS c"
            ).single()["c"]
            print(f"  preservados (Folder/Document): {preserved}")
    except Exception as exc:  # noqa: BLE001
        print(f"[ingest] ERRO: {exc}")
        return 1
    finally:
        driver.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
