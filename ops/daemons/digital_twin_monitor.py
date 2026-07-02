#!/usr/bin/env python3
"""
digital_twin_monitor.py — tick de MONITOR CONTÍNUO do Gêmeo Digital (Neo4j).

Roda NATIVO no host (acesso direto ao docker — sem ponte de sandbox). Sem
dependência de Claude/IA: docker + cypher puros, pensado pro setup
Antigravity+Gemini+Electron (o painel lê o digital_twin.status.json).

A cada tick:
  - Enumera TODOS os containers Neo4j (lição da skill host-bridge: não cole no 1º).
  - Conta nós nos que estão de pé (descobre credencial via docker inspect).
  - Detecta e ALERTA: grafo ZERADO; twin parado com volume nomeado guardando os
    dados; transição de >0 para 0.
  - Escreve digital_twin.status.json + alerts.log.

Uso (via daemon):
  python mecha_daemon.py --name digital-twin-monitor --interval 15m \
     --cmd "python digital_twin_monitor.py"
Teste de lógica (sem docker):  python digital_twin_monitor.py --selftest
"""
import os, re, json, subprocess, argparse, datetime

def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()

def sh(cmd, timeout=30):
    p = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
    return p.stdout.strip(), p.stderr.strip(), p.returncode

HEXVOL = re.compile(r"^[0-9a-f]{64}$")  # volume anônimo = hash; nomeado = legível

def list_neo4j():
    out, _, _ = sh('docker ps -a --format "{{.Names}}\t{{.Image}}\t{{.State}}"')
    cs = []
    for line in out.splitlines():
        parts = line.split("\t")
        if len(parts) < 3:
            continue
        name, image, state = parts[0], parts[1], parts[2]
        if "neo4j" not in (name + image).lower():
            continue
        cs.append({"name": name, "image": image, "running": state.lower() == "running"})
    return cs

def creds(name):
    out, _, _ = sh(f'docker inspect --format "{{{{range .Config.Env}}}}{{{{println .}}}}{{{{end}}}}" {name}')
    for line in out.splitlines():
        if line.startswith("NEO4J_AUTH=") and "/" in line:
            return tuple(line.split("=", 1)[1].split("/", 1))
    return None

def named_volume(name):
    out, _, _ = sh(f'docker inspect --format "{{{{range .Mounts}}}}{{{{.Type}}}}:{{{{.Name}}}} {{{{end}}}}" {name}')
    for tok in out.split():
        if tok.startswith("volume:"):
            vn = tok.split(":", 1)[1]
            if vn and not HEXVOL.match(vn):
                return vn
    return None

def count_nodes(name):
    base = creds(name) or ("neo4j", "neo4j")
    last_err = "cypher falhou"
    for u, p in [base, ("neo4j", "rootroot"), ("neo4j", "neo4j")]:
        out, err, rc = sh(f'docker exec {name} cypher-shell -u {u} -p {p} --format plain "MATCH (n) RETURN count(n) AS n"')
        if rc == 0:
            m = re.search(r"\d+", out.replace("n", ""))
            if m:
                return int(m.group()), None
        last_err = (err or out)[:120]
        if "authentication" in (err + out).lower():
            continue
    return None, last_err

def gather():
    cs = list_neo4j()
    for c in cs:
        c["named_volume"] = named_volume(c["name"])
        if c["running"]:
            c["nodes"], c["error"] = count_nodes(c["name"])
        else:
            c["nodes"], c["error"] = None, None
    return cs

def decide(cs, prev_max=None):
    running = [c for c in cs if c["running"]]
    with_nodes = [c for c in running if (c.get("nodes") or 0) > 0]
    max_nodes = max([(c.get("nodes") or 0) for c in running], default=0)
    stopped_named = [c for c in cs if not c["running"] and c.get("named_volume")]
    status, reasons = "OK", []
    if not running:
        status = "ALERT"; reasons.append("nenhum container Neo4j em execução")
    elif not with_nodes:
        status = "ALERT"; reasons.append("grafo ZERADO — nenhum Neo4j de pé com nós > 0")
        if stopped_named:
            reasons.append("dados provavelmente em container PARADO c/ volume nomeado: " +
                           ", ".join(f"{c['name']}({c['named_volume']})" for c in stopped_named) +
                           " → 'docker start', NÃO re-ingerir")
    if prev_max is not None and prev_max > 0 and max_nodes == 0:
        status = "ALERT"; reasons.insert(0, f"TRANSIÇÃO para zero: grafo caiu de {prev_max} → 0 nós")
    return {"status": status, "max_nodes_running": max_nodes, "reasons": reasons}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--state-dir", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), ".state"))
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    os.makedirs(a.state_dir, exist_ok=True)
    statusf = os.path.join(a.state_dir, "digital_twin.status.json")
    alertsf = os.path.join(a.state_dir, "alerts.log")

    if a.selftest:
        out = {
            "empty+stopped_real": decide([
                {"name": "cdc_neo4j", "running": True, "nodes": 0, "named_volume": None},
                {"name": "mecha_ontology_graph", "running": False, "nodes": None, "named_volume": "infrastructure_neo4j_data"}]),
            "healthy": decide([{"name": "cdc_neo4j", "running": True, "nodes": 349, "named_volume": None}]),
            "dropped_prev349": decide([{"name": "cdc_neo4j", "running": True, "nodes": 0, "named_volume": None}], prev_max=349),
        }
        print(json.dumps(out, indent=2, ensure_ascii=False))
        return

    prev_max = None
    if os.path.exists(statusf):
        try: prev_max = json.load(open(statusf)).get("verdict", {}).get("max_nodes_running")
        except Exception: pass
    cs = gather()
    verdict = decide(cs, prev_max)
    json.dump({"updated": now(), "verdict": verdict, "containers": cs},
              open(statusf, "w"), indent=2, ensure_ascii=False)
    if verdict["status"] == "ALERT":
        with open(alertsf, "a", encoding="utf-8") as f:
            f.write(f"{now()} ALERT {' | '.join(verdict['reasons'])}\n")
        print("ALERT:", " | ".join(verdict["reasons"]))
    else:
        print(f"OK: {verdict['max_nodes_running']} nós no Gêmeo Digital")

if __name__ == "__main__":
    main()
