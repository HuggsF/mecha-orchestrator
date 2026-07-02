# -*- coding: utf-8 -*-
"""
neo4j_sendspeed_ingest — projeta o domínio SendSpeed no grafo Neo4j.
====================================================================
Cria nós :Module, :Service e :Contract para os 5 módulos MCP do sendspeed,
os 3 serviços do pipeline de callbacks e os contratos-chave do domínio.

Idempotente (MERGE). Nunca toca :Folder/:Document (second_brain) nem a
ontologia em geral — escopo isolado ao sendspeed.

Uso:
    python ops/neo4j_sendspeed_ingest.py              # merge incremental
    python ops/neo4j_sendspeed_ingest.py --dry-run    # conta, não escreve
    python ops/neo4j_sendspeed_ingest.py --reset      # limpa sendspeed e reingere

Regra P2: escrita no grafo SEMPRE via ingestores dedicados, nunca pelo MCP.
"""

from __future__ import annotations

import argparse
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

from neo4j import GraphDatabase

NEO4J_URI  = os.environ.get("NEO4J_URI",  "bolt://localhost:7687")
NEO4J_USER = os.environ.get("NEO4J_USER", "neo4j")
NEO4J_PASS = os.environ.get("NEO4J_PASS", "rootroot")

# ---------------------------------------------------------------------------
# Dados do domínio
# ---------------------------------------------------------------------------

MODULES = [
    {
        "key": "sendspeed::sendspeed_catalog",
        "name": "sendspeed_catalog",
        "domain": "sendspeed",
        "description": "Catálogo geral: status, module_map, find_issue, search, gaps.",
        "tools": ["sendspeed_status", "sendspeed_module_map",
                  "sendspeed_find_issue", "sendspeed_search", "sendspeed_gaps"],
        "source_issues": ["SEND-488", "SEND-504", "SEND-511", "SEND-498",
                          "SEND-475", "SEND-471", "SEND-476", "SEND-487"],
    },
    {
        "key": "sendspeed::sendspeed_callbacks",
        "name": "sendspeed_callbacks",
        "domain": "sendspeed",
        "description": "Contrato crm_postback multi-CRM, de-para de status, mapa do pipeline DLR.",
        "tools": ["crm_postback_contract", "crm_status_depara", "callback_pipeline_map"],
        "source_issues": ["SEND-488", "SEND-490", "SEND-491", "SEND-492",
                          "SEND-493", "SEND-495", "SEND-496", "SEND-497",
                          "SEND-498", "SEND-500", "SEND-502", "SEND-483", "SEND-479"],
    },
    {
        "key": "sendspeed::sendspeed_journeys",
        "name": "sendspeed_journeys",
        "domain": "sendspeed",
        "description": "Engine de jornadas: executor, trigger contract, atribuição, catálogo.",
        "tools": ["journey_engine_map", "journey_trigger_contract",
                  "journey_objective_attribution", "journey_catalog"],
        "source_issues": ["SEND-391", "SEND-477", "SEND-478", "SEND-450",
                          "SEND-446", "SEND-449", "SEND-479"],
    },
    {
        "key": "sendspeed::sendspeed_channels",
        "name": "sendspeed_channels",
        "domain": "sendspeed",
        "description": "Canais SMS/RCS/WhatsApp: spec de envio e fluxo OTP Infobip.",
        "tools": ["channel_send_spec", "otp_flow_spec"],
        "source_issues": ["SEND-429", "SEND-446", "SEND-449", "SEND-452",
                          "SEND-478", "SEND-505", "SEND-508"],
    },
    {
        "key": "sendspeed::sendspeed_integrations",
        "name": "sendspeed_integrations",
        "domain": "sendspeed",
        "description": "Webhooks iGaming NGX/UserIn, segurança HMAC, registry de adapters CRM.",
        "tools": ["igaming_webhook_pattern", "webhook_security_spec", "crm_adapter_registry"],
        "source_issues": ["SEND-499", "SEND-501", "SEND-502", "SEND-503",
                          "SEND-506", "SEND-510", "SEND-515", "SEND-516", "SEND-517"],
    },
]

SERVICES = [
    {
        "key": "sendspeed::svc::sms-api",
        "name": "sms-api",
        "domain": "sendspeed",
        "description": "API principal de envio SMS/RCS: DTOs, builders e consumers com forwardCrmPostback.",
        "issues": ["SEND-490", "SEND-491", "SEND-492", "SEND-493"],
    },
    {
        "key": "sendspeed::svc::api-legada",
        "name": "api-legada",
        "domain": "sendspeed",
        "description": "API legada: HandleApi, ValidationService, SmsService e SmsConsumer com roteamento Smartico/FastTrack.",
        "issues": ["SEND-495", "SEND-496"],
    },
    {
        "key": "sendspeed::svc::callback-sms",
        "name": "callback-sms",
        "domain": "sendspeed",
        "description": "Workers de callback: parsing único crm_postback, CallbackGrouper/BatchProcessor por CRM.",
        "issues": ["SEND-497", "SEND-498", "SEND-500", "SEND-502"],
    },
]

CONTRACTS = [
    {
        "key": "sendspeed::contract::crm_postback",
        "name": "crm_postback",
        "domain": "sendspeed",
        "status": "confirmed",
        "description": "Contrato multi-CRM: campo crm (smartico|fasttrack, ausência=smartico), crm_message_id, callback_url, api_key.",
        "blocked_by": [],
    },
    {
        "key": "sendspeed::contract::crm_callback_redis_key",
        "name": "crm_callback_redis_key",
        "domain": "sendspeed",
        "status": "confirmed",
        "description": "Chave Redis parametrizada: crm_callback:client:{userId}:{crm}:{product}.",
        "blocked_by": [],
    },
    {
        "key": "sendspeed::contract::fasttrack_client",
        "name": "fasttrack_client",
        "domain": "sendspeed",
        "status": "blocked",
        "description": "FastTrackClient via ICrmCallbackClient: auth/payload/retry aguardam documentação FastTrack.",
        "blocked_by": ["SEND-504"],
    },
    {
        "key": "sendspeed::contract::igaming_webhook",
        "name": "igaming_webhook",
        "domain": "sendspeed",
        "status": "confirmed",
        "description": "HMAC-SHA256 (X-Auth-Signature), idempotência external_id, DLQ 1/5/15min, gatekeepers KYC/consent/blocklist.",
        "blocked_by": [],
    },
    {
        "key": "sendspeed::contract::otp_whatsapp",
        "name": "otp_whatsapp",
        "domain": "sendspeed",
        "status": "confirmed",
        "description": "OTP WhatsApp via Infobip (supplier_id=64): gate por cliente, template authentication Meta, fallback SMS.",
        "blocked_by": [],
    },
]

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _list_str(items: list) -> str:
    return "|".join(str(i) for i in items)


def ingest(session, stamp: str) -> dict:
    counts = {"modules": 0, "services": 0, "contracts": 0, "rels": 0}

    # Nó raiz do domínio
    session.run(
        "MERGE (d:Domain {id: 'sendspeed'}) "
        "SET d.kind='Knowledge Domain', d.path='CORE/sendspeed', "
        "d.description='Domínio SendSpeed absorvido no MECHA (debate O6 #2).', "
        "d.synced_at=$stamp",
        stamp=stamp,
    )

    # Módulos MCP
    for m in MODULES:
        session.run(
            "MERGE (n:Module {key: $key}) "
            "SET n.name=$name, n.domain=$domain, n.description=$desc, "
            "n.tools=$tools, n.source_issues=$issues, n.synced_at=$stamp "
            "WITH n MATCH (d:Domain {id: 'sendspeed'}) "
            "MERGE (d)-[:HAS_MODULE]->(n)",
            key=m["key"], name=m["name"], domain=m["domain"],
            desc=m["description"],
            tools=_list_str(m["tools"]),
            issues=_list_str(m["source_issues"]),
            stamp=stamp,
        )
        counts["modules"] += 1
        counts["rels"] += 1

    # Serviços
    for s in SERVICES:
        session.run(
            "MERGE (n:Service {key: $key}) "
            "SET n.name=$name, n.domain=$domain, n.description=$desc, "
            "n.issues=$issues, n.synced_at=$stamp "
            "WITH n MATCH (d:Domain {id: 'sendspeed'}) "
            "MERGE (d)-[:HAS_SERVICE]->(n)",
            key=s["key"], name=s["name"], domain=s["domain"],
            desc=s["description"], issues=_list_str(s["issues"]),
            stamp=stamp,
        )
        counts["services"] += 1
        counts["rels"] += 1

    # Contratos
    for c in CONTRACTS:
        session.run(
            "MERGE (n:Contract {key: $key}) "
            "SET n.name=$name, n.domain=$domain, n.description=$desc, "
            "n.status=$status, n.blocked_by=$blocked_by, n.synced_at=$stamp "
            "WITH n MATCH (d:Domain {id: 'sendspeed'}) "
            "MERGE (d)-[:HAS_CONTRACT]->(n)",
            key=c["key"], name=c["name"], domain=c["domain"],
            desc=c["description"], status=c["status"],
            blocked_by=_list_str(c["blocked_by"]),
            stamp=stamp,
        )
        counts["contracts"] += 1
        counts["rels"] += 1

    return counts


def reset_sendspeed(session) -> int:
    """Remove apenas nós de domínio sendspeed (Module, Service, Contract com key prefixada)."""
    total = 0
    for label in ("Module", "Service", "Contract"):
        res = session.run(
            f"MATCH (n:{label}) WHERE n.key STARTS WITH 'sendspeed::' "
            "WITH n, count(n) AS c DETACH DELETE n RETURN c"
        )
        total += sum(r["c"] for r in res)
    # Remove Domain sendspeed
    session.run("MATCH (d:Domain {id: 'sendspeed'}) DETACH DELETE d")
    return total


def main() -> int:
    ap = argparse.ArgumentParser(description="Injeta domínio SendSpeed no Neo4j")
    ap.add_argument("--reset",   action="store_true", help="limpa nós sendspeed e reingere")
    ap.add_argument("--dry-run", action="store_true", help="conta e valida, não escreve")
    args = ap.parse_args()

    print(f"[sendspeed-ingest] {len(MODULES)} módulos | {len(SERVICES)} serviços | {len(CONTRACTS)} contratos")

    if args.dry_run:
        print("[sendspeed-ingest] dry-run: nada escrito.")
        return 0

    stamp = datetime.now(timezone.utc).isoformat()
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASS))
    try:
        driver.verify_connectivity()
        print(f"[sendspeed-ingest] Neo4j OK ({NEO4J_URI})")
        with driver.session() as session:
            if args.reset:
                removed = reset_sendspeed(session)
                print(f"[sendspeed-ingest] reset: {removed} nós sendspeed removidos")
            counts = ingest(session, stamp)
            print(f"[sendspeed-ingest] OK: {counts}")
            # Verificação pós-ingest
            for label in ("Module", "Service", "Contract"):
                c = session.run(
                    f"MATCH (n:{label}) WHERE n.key STARTS WITH 'sendspeed::' "
                    "RETURN count(n) AS c"
                ).single()["c"]
                print(f"  {label}: {c}")
            rels = session.run(
                "MATCH (d:Domain {id: 'sendspeed'})-[r:HAS_MODULE|HAS_SERVICE|HAS_CONTRACT]->() "
                "RETURN count(r) AS c"
            ).single()["c"]
            print(f"  rels sendspeed: {rels}")
            preserved = session.run(
                "MATCH (n) WHERE n:Folder OR n:Document RETURN count(n) AS c"
            ).single()["c"]
            print(f"  preservados (Folder/Document): {preserved}")
    except Exception as exc:  # noqa: BLE001
        print(f"[sendspeed-ingest] ERRO: {exc}")
        return 1
    finally:
        driver.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
