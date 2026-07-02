# Extração RPG Cortex — Documentação Privada

> Esta pasta (.private/) está no .gitignore. Conteúdo não versionado.

---

## 1. Estado Atual (pós-extração)

- **KPI Intelligence**: Restaurado em `src/neural_link/telemetry/` (tool_scorecard, model_benchmark, cost_quality_analyzer, metrics_timeseries). Usa `src.neural_link.graph.queries`.
- **RPG Cortex**: Extraído para `src/extracted/rpg_cortex/` (hardware, knowledge, temp, logs).
- **Consumidores**:
  - `jitbit_connector.py` → `from src.extracted.rpg_cortex.hardware.jitbit_wrapper import JitbitWrapper`
  - `computer_use_agent.py` → `TEMP_DIR = PROJECT_ROOT / "src" / "extracted" / "rpg_cortex" / "temp"`
- **Infra**: Dockerfile e docker-compose atualizados para `src/extracted/rpg_cortex/`.

---

## 2. Relações nos Grafos (Neo4j)

KPI e RPG são independentes nos grafos:

| Submódulo | Nós | Relações |
|-----------|-----|----------|
| KPI | ModelMetric, ToolReview, RequestMetric, DailyAggregate | Nenhuma entre si |
| RPG/Telemetry | ExternalSync | (ExternalSync)-[:TRIGGERED]->(Task) |

O JitbitConnector de macros não escreve no grafo. O provider (TelemetryProvider) persiste ExternalSync e não depende de rpg_cortex.

---

## 3. Sem RPG Cortex: Onde Falha

| Componente | Comportamento |
|------------|---------------|
| execute_macro_sync (.mcr/.jmb) | **Falha** — ImportError se JitbitWrapper indisponível |
| run_macro | OK (subprocess ou Virtual Driver) |
| computer_use_agent | OK (TEMP_DIR.mkdir cria pasta) |
| Telemetria | OK |

---

## 4. Plug-and-Play Invisível (checklist)

- [ ] execute_macro_sync: fallback para subprocess quando JitbitWrapper indisponível
- [ ] TEMP_DIR configurável (env COMPUTER_USE_TEMP)
- [ ] rpg_cortex como dependência opcional

---

## 5. Auditoria DI (RPG Cortex)

Padrões: lazy init, parâmetros opcionais, import dinâmico, estado global (_emergency_stop).

Consumidores: jitbit_connector (JitbitWrapper), computer_use_agent (TEMP_DIR).
