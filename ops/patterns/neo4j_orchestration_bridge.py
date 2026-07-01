# ==============================================================================
# NEO4J ORCHESTRATION BRIDGE (Item 5, grounded - SEM Kafka)
# ==============================================================================
# Transmite eventos do Shura (AgentBus pipeline.events) AO VIVO para o Digital
# Twin Neo4j, sob o contrato Memory Mesh (source='shura', MERGE idempotente,
# MATCH-then-MERGE, NUNCA destrutivo). Une-se ao CDC pelo MESMO Neo4j: o deploy
# do devops liga na Campaign via (:Artifact)-[:DEPLOYS]->(:Campaign), habilitando
# a rota de linhagem outcome->proveniencia.
#
# Fail-safe: se o Neo4j estiver indisponivel, o bridge vira no-op (a orquestracao
# nunca quebra por causa do espelhamento). Idempotente no bus singleton.
# Por que sem Kafka: o AgentBus JA e o stream de eventos in-process; broker seria
# over-engineering. Promova para Kafka (topico mecha.orchestration + consumer
# espelho do ml_kafka_connector) so quando precisar de replay/multi-sink.
# ==============================================================================

import os
import time
import logging
from typing import Any, Dict, List, Optional

try:
    from neo4j import GraphDatabase
except Exception:  # pragma: no cover
    GraphDatabase = None

logger = logging.getLogger("MECHA_Neo4jBridge")

NEO4J_URI = os.environ.get("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.environ.get("NEO4J_USER", "neo4j")
NEO4J_PASS = os.environ.get("NEO4J_PASS", "rootroot")


class Neo4jOrchestrationBridge:
    def __init__(self, bus, uri: str = None, user: str = None, password: str = None):
        self.bus = bus
        self._driver = None
        self._uri = uri or NEO4J_URI
        self._auth = (user or NEO4J_USER, password or NEO4J_PASS)
        self._failed = False
        if not getattr(bus, "_neo4j_bridge_attached", False):
            bus.on_channel("pipeline.events", self._on_event)
            setattr(bus, "_neo4j_bridge_attached", True)
            logger.info("[BRIDGE] Espelhamento de orquestracao -> Digital Twin ativo.")

    # ---- conexao fail-safe (lazy) -------------------------------------------
    def _drv(self):
        if self._failed or GraphDatabase is None:
            return None
        if self._driver is None:
            try:
                self._driver = GraphDatabase.driver(self._uri, auth=self._auth)
                self._driver.verify_connectivity()
                logger.info("[BRIDGE] Conectado ao Digital Twin Neo4j em %s", self._uri)
            except Exception as e:
                self._failed = True
                logger.warning("[BRIDGE] Neo4j indisponivel (%s) -> bridge em no-op.", e)
                return None
        return self._driver

    def _run(self, cypher: str, **params) -> Optional[List[Dict[str, Any]]]:
        drv = self._drv()
        if not drv:
            return None
        try:
            with drv.session(database="neo4j") as s:
                return s.run(cypher, **params).data()
        except Exception as e:
            logger.warning("[BRIDGE] Falha ao escrever/ler no Neo4j: %s", e)
            return None

    # ---- handler de eventos --------------------------------------------------
    def _on_event(self, msg):
        try:
            p = msg.payload or {}
            ev = p.get("event")
            tid = p.get("thread_id")
            if not tid:
                return
            if ev == "workflow.completed":
                squad = (p.get("squad") or "").replace("_squad", "")
                self._run(
                    "MERGE (t:Orchestration:Thread {id:$tid}) "
                    "ON CREATE SET t.created_at=datetime() "
                    "SET t.kind='pipeline', t.source='shura', t.updated_at=datetime() "
                    "WITH t MATCH (s:System {name:'Claw'}) MERGE (t)-[:RUN_BY]->(s)",
                    tid=tid)
                outs = p.get("output_vars") or []
                for var in outs:
                    aid = "%s:%s@%s" % (squad, var, tid)   # run-scoped p/ linhagem precisa
                    self._run(
                        "MATCH (t:Thread {id:$tid}) "
                        "MERGE (a:Orchestration:Artifact {id:$aid}) "
                        "SET a.name=$var, a.squad=$squad, a.thread_id=$tid, a.source='shura' "
                        "MERGE (t)-[:PRODUCED]->(a)",
                        tid=tid, aid=aid, var=var, squad=squad)
                # JUNCAO CDC: deploy do devops -> Campaign (lineage de entrega)
                cid = p.get("campaign_id")
                if squad == "devops" and cid is not None and "deploy_manifest" in outs:
                    self.link_deploy_to_campaign("devops:deploy_manifest@%s" % tid, cid)
            elif ev == "handoff.approved":
                self._run("MERGE (t:Orchestration:Thread {id:$tid}) "
                          "SET t.handoffs_approved=coalesce(t.handoffs_approved,0)+1, t.updated_at=datetime()", tid=tid)
            elif ev == "handoff.blocked":
                self._run("MERGE (t:Orchestration:Thread {id:$tid}) "
                          "SET t.handoffs_blocked=coalesce(t.handoffs_blocked,0)+1, t.last_block=$reason, t.updated_at=datetime()",
                          tid=tid, reason=p.get("reason", ""))
            elif ev == "route.rebalanced":
                self._run("MERGE (t:Orchestration:Thread {id:$tid}) "
                          "SET t.rebalanced=coalesce(t.rebalanced,0)+1, t.last_rebalance_to=$chosen, t.updated_at=datetime()",
                          tid=tid, chosen=p.get("chosen", ""))
            elif ev == "rule.recurrence":
                self._run("MERGE (t:Orchestration:Thread {id:$tid}) "
                          "SET t.recurrence_alert=$rule, t.recurrence_streak=$streak, t.updated_at=datetime()",
                          tid=tid, rule=p.get("rule", ""), streak=p.get("streak", 0))
            elif ev == "consolidated":
                self._run("MERGE (t:Orchestration:Thread {id:$tid}) "
                          "SET t.report_path=$rp, t.verdict=$v, t.updated_at=datetime()",
                          tid=tid, rp=p.get("report_path", ""), v=p.get("verdict", ""))
        except Exception as e:
            logger.warning("[BRIDGE] handler error: %s", e)

    # ---- juncao com o CDC ----------------------------------------------------
    def link_deploy_to_campaign(self, deploy_artifact_id: str, campaign_id) -> None:
        """Aresta de juncao: o deploy do devops shippou a Campaign (CDC)."""
        self._run(
            "MERGE (c:Campaign {id:$cid}) "
            "WITH c MATCH (a:Artifact {id:$aid}) MERGE (a)-[:DEPLOYS]->(c)",
            cid=str(campaign_id), aid=deploy_artifact_id)

    # ---- ROTA UTIL: linhagem outcome -> proveniencia -------------------------
    def lineage_for_campaign(self, campaign_id) -> Optional[List[Dict[str, Any]]]:
        """Traca: predicao da campanha (CDC) -> deploy -> run/squad/veredito (Shura)."""
        return self._run(
            "MATCH (c:Campaign {id:$cid}) "
            "OPTIONAL MATCH (c)-[:HAS_PREDICTION]->(p:CampaignPrediction) "
            "OPTIONAL MATCH (c)<-[:DEPLOYS]-(a:Artifact)<-[:PRODUCED]-(t:Thread) "
            "RETURN c.id AS campanha, p.status AS predicao, p.completion_probability AS prob, "
            "a.id AS deploy, t.id AS run, t.verdict AS veredito, t.report_path AS relatorio",
            cid=str(campaign_id))

    def close(self):
        if self._driver:
            try:
                self._driver.close()
            except Exception:
                pass
