import os
from neo4j import GraphDatabase
import logging

logging.basicConfig(level=logging.INFO)

# Tentativas de senha
PASSWORDS = ["test", "rootroot", "neo4j", "password"]
URI = os.environ.get("NEO4J_URI", "bolt://localhost:7687")
USER = os.environ.get("NEO4J_USER", "neo4j")

def inject_standards():
    driver = None
    for pw in PASSWORDS:
        try:
            d = GraphDatabase.driver(URI, auth=(USER, pw))
            d.verify_connectivity()
            driver = d
            logging.info(f"Conectado com sucesso com a senha '{pw}'")
            break
        except Exception:
            pass

    if not driver:
        logging.error("Falha ao conectar no Neo4j com todas as senhas tentadas.")
        return

    with driver.session() as session:
        # 1. Injetar Metodologia (Destilador)
        session.run("""
            MERGE (m:CommunicationProtocol {name: 'Destilador'})
            SET m.description = 'Formato padronizado de relatórios de 7 tópicos (Categoria, Resumo, Contexto, Causa Raiz, Validação, Ação, Trilha). Usado para destilar comunicações.'
        """)
        
        # 2. Injetar Golden Patterns
        patterns = [
            ("python_gold_pattern", "FastAPI Clean Architecture, OpenTelemetry, Pydantic"),
            ("observability_gold_pattern", "OpenTelemetry, Prometheus, Grafana, Logs JSON"),
            ("anytype_gold_pattern", "Clean Architecture, Qdrant ontology, Epsilon loops")
        ]
        
        for name, desc in patterns:
            session.run("""
                MERGE (p:ArchitectureStandard {name: $name})
                SET p.description = $desc
            """, name=name, desc=desc)

        # 3. Relacionar os padrões ao Squad de Agentes Genérico para imposição global
        session.run("""
            MERGE (squad:AgentSquad {name: 'MECHA_GLOBAL_SQUAD'})
            WITH squad
            MATCH (m:CommunicationProtocol {name: 'Destilador'})
            MERGE (m)-[:GOVERNS]->(squad)
            WITH squad
            MATCH (p:ArchitectureStandard)
            MERGE (p)-[:GOVERNS]->(squad)
        """)
        
    driver.close()
    logging.info("Injeção da metodologia e Golden Patterns no Neo4j concluída com sucesso.")

if __name__ == "__main__":
    inject_standards()
