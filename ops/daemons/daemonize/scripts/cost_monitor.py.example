#!/usr/bin/env python3
"""
cost_monitor.py — tick determinístico do daemon de custo do MechaShell.

Mede o custo de tokens do schema enxuto (gemini/function_declarations.json),
acrescenta ao cost_log.csv, compara com o run anterior e sinaliza platô
("o valor despencou e estabilizou"). Read-only no projeto, exceto o log.
"""
import os, csv, math, datetime, argparse

def est_tokens(text: str) -> int:
    return math.ceil(len(text) / 4)  # heurística char/4 (sem rede p/ tiktoken)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", default=r"C:\Users\huggs\OneDrive\Documentos\workspace\dc-lean")
    a = ap.parse_args()
    decl = os.path.join(a.project, "gemini", "function_declarations.json")
    log = os.path.join(a.project, "analysis", "cost_log.csv")
    os.makedirs(os.path.dirname(log), exist_ok=True)

    tokens = est_tokens(open(decl, encoding="utf-8").read())
    baseline = 5920
    drop = round((baseline - tokens) / baseline * 100, 1)

    last = None
    if os.path.exists(log):
        rows = list(csv.DictReader(open(log, encoding="utf-8")))
        if rows:
            last = int(rows[-1]["lean_tokens"])
    delta = (tokens - last) if last is not None else 0

    new = not os.path.exists(log)
    with open(log, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["timestamp", "lean_tokens", "delta_vs_last", "drop_vs_baseline_pct", "note"])
        w.writerow([datetime.datetime.now(datetime.timezone.utc).isoformat(),
                    tokens, f"{delta:+d}", drop, "monitor tick"])

    plateau = last is not None and abs(delta) < max(1, 0.02 * last)
    print(f"lean_tokens={tokens} delta={delta:+d} drop_vs_baseline={drop}%")
    if plateau:
        print("PLATEAU: <2% de variação vs run anterior — o custo estabilizou. "
              "Recomendo desligar o daemon (convergiu).")

if __name__ == "__main__":
    main()
