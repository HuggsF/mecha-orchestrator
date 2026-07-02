import os
from neo4j import GraphDatabase

URI = 'bolt://localhost:7688'
USER = 'neo4j'
PASSWORD = 'rootroot'

def summarize_neo4j():
    try:
        driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
        driver.verify_connectivity()
    except Exception as e:
        print(f'Erro de conexao: {e}')
        return

    queries = [
        ("Contagem por Label", "MATCH (n) RETURN labels(n)[0] AS label, count(n) AS count ORDER BY count DESC"),
        ("Relacionamentos", "MATCH ()-[r]->() RETURN type(r) AS rel_type, count(r) AS count ORDER BY count DESC")
    ]
    
    with driver.session() as session:
        for title, query in queries:
            print(f"--- {title} ---")
            result = session.run(query)
            for record in result:
                print(dict(record))
            print()

    driver.close()

if __name__ == '__main__':
    summarize_neo4j()
