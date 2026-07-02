#!/usr/bin/env python3
"""
ingest_session.py — ingere os artefatos desta sessão no Gêmeo Digital (Neo4j).

Roda NATIVO no host (docker direto; sem Claude). Additivo e idempotente (MERGE):
cria 1 :Session + N :Artifact, ligados a :SystemPillar (reusa a convenção do grafo).
Seguro de rodar várias vezes.

Uso:
  python ingest_session.py                      # ingere no Neo4j em execução
  python ingest_session.py --container mecha_ontology_graph
  python ingest_session.py --print-cypher       # só mostra o Cypher (não executa)
"""
import os, json, subprocess, argparse, tempfile

def sh(cmd, t=60):
    p = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=t)
    return p.stdout.strip(), p.stderr.strip(), p.returncode

def q(s):  # escapa para string Cypher entre aspas simples
    return str(s).replace("\\", "\\\\").replace("'", "\\'")

def pick_container(explicit=None):
    if explicit:
        return explicit
    out, _, _ = sh('docker ps --format "{{.Names}} {{.Image}}"')
    for line in out.splitlines():
        if "neo4j" in line.lower():
            return line.split()[0]
    return None

def creds(name):
    out, _, _ = sh(f'docker inspect --format "{{{{range .Config.Env}}}}{{{{println .}}}}{{{{end}}}}" {name}')
    for line in out.splitlines():
        if line.startswith("NEO4J_AUTH=") and "/" in line:
            return tuple(line.split("=", 1)[1].split("/", 1))
    return ("neo4j", "neo4j")

def build_cypher(m):
    s = m["session"]
    out = [f"MERGE (s:Session {{id:'{q(s['id'])}'}}) SET s.title='{q(s['title'])}', s.date='{q(s['date'])}';"]
    for p in sorted({a["pillar"] for a in m["artifacts"]}):
        out.append(f"MERGE (:SystemPillar {{name:'{q(p)}'}});")
    for a in m["artifacts"]:
        out.append(f"MERGE (a:Artifact {{id:'{q(a['id'])}'}}) "
                   f"SET a.name='{q(a['name'])}', a.kind='{q(a['kind'])}', "
                   f"a.path='{q(a['path'])}', a.summary='{q(a['summary'])}';")
        out.append(f"MATCH (s:Session {{id:'{q(s['id'])}'}}), (a:Artifact {{id:'{q(a['id'])}'}}), "
                   f"(p:SystemPillar {{name:'{q(a['pillar'])}'}}) "
                   f"MERGE (s)-[:PRODUCED]->(a) MERGE (a)-[:BELONGS_TO]->(p);")
    return "\n".join(out)

def main():
    here = os.path.dirname(os.path.abspath(__file__))
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", default=os.path.join(here, "session_manifest.json"))
    ap.add_argument("--container")
    ap.add_argument("--print-cypher", action="store_true")
    a = ap.parse_args()

    m = json.load(open(a.manifest, encoding="utf-8"))
    script = build_cypher(m)
    if a.print_cypher:
        print(script)
        return

    c = pick_container(a.container)
    if not c:
        raise SystemExit("nenhum container Neo4j em execução — suba o twin: docker start mecha_ontology_graph")
    u, p = creds(c)
    tmp = tempfile.NamedTemporaryFile("w", suffix=".cypher", delete=False, encoding="utf-8")
    tmp.write(script); tmp.close()
    sh(f'docker cp "{tmp.name}" {c}:/tmp/ingest.cypher')
    out, err, rc = sh(f'docker exec {c} cypher-shell -u {u} -p {p} -f /tmp/ingest.cypher')
    os.unlink(tmp.name)
    if rc != 0:
        raise SystemExit(f"ingest falhou em {c}: {(err or out)[:200]}")
    print(f"OK: ingerido em {c} -> 1 Session + {len(m['artifacts'])} Artifacts ligados a SystemPillar")

if __name__ == "__main__":
    main()
