---
name: daemonize
description: Use to transform a scheduled/cron task (or any periodic job) into a resilient long-running DAEMON. Triggers on "transforma o agendamento em daemon", "daemonize this task", "vira um serviço de background", "rodar continuamente / monitor contínuo", "Shura daemon", "make this a background service", or when a recurring job needs to survive independently of the app, react faster than its interval, keep in-process state, or be supervised with restart/backoff. Bundles a ready, dependency-free daemon runner (scripts/mecha_daemon.py) with lockfile single-instance, fail-closed loop, backoff, heartbeat/status file and graceful shutdown, plus Windows launcher + boot-registration guidance. Also use to DECIDE whether a job should stay cron or become a daemon.
---

# Daemonize — transformar agendamento em daemon

Uma scheduled task (cron) dispara execuções discretas e depende do scheduler/app estar de pé. Um **daemon** é um processo persistente e auto-supervisionado. Esta skill converte o primeiro no segundo, com resiliência de produção (estilo Shura/MECHA).

## 1. Cron ou daemon? (decida primeiro)
Mantenha **cron/scheduled** se: as execuções são discretas, tudo bem depender do app estar aberto, não há estado em memória, e a reação no intervalo basta.
**Transforme em daemon** se ao menos um for verdade: precisa **sobreviver independente do app**; precisa **reagir mais rápido** que o intervalo (ex.: vigiar um arquivo/fila); precisa de **estado em processo** ou heartbeat contínuo; precisa de **supervisão** (restart/backoff) e fail-closed. É o padrão "Shura daemon".

## 2. Anatomia que o transformer garante
- **Instância única:** lockfile com PID + detecção de stale (não roda em dobro).
- **Fail-closed:** um tick que lança exceção **nunca** derruba o loop.
- **Backoff:** falhas repetidas espaçam o próximo run (capado), sem busy-loop.
- **Heartbeat/status:** `<state-dir>/<name>.status.json` (state, last_status, consecutive_failures, next_run) + `.log` estruturado — SSOT de saúde.
- **Shutdown gracioso:** SIGINT/SIGTERM/SIGBREAK → marca stop, finaliza o tick, libera o lock.
- **Sleep interruptível** e **tick idempotente**.

## 3. Como transformar (passos)
1. **Isole o trabalho** num *tick* determinístico — um script (`job.py`) ou callable. Separe "medir/agir" do "agendar". Se o job era um prompt de IA, extraia a parte verificável para o tick (medição/log/alerta) e deixe a parte criativa sob supervisão (ou chame `claude -p` como subprocesso, se disponível).
2. **Rode pelo runner bundlado:**
   `python scripts/mecha_daemon.py --name <n> --interval 6h --cmd "python job.py"`
   ou um callable: `--module pacote.modulo:func`. Teste com `--run-once`.
3. **Launcher + boot (Windows):** veja `references/launch_windows.md` (Start-Process oculto + `schtasks /SC ONLOGON`).
4. **Observe:** leia o `.status.json` e o `.log` no `--state-dir`.
5. **Condição de parada:** o tick pode sinalizar platô/convergência (ex.: "o valor estabilizou"); o supervisor desliga o daemon. Não deixe rodar à toa.

## 4. Exemplo (a task de custo do MECHA)
`scripts/cost_monitor.py.example` é um tick real: mede o custo de tokens do schema, acrescenta ao `cost_log.csv`, e avisa quando o valor **platô** (<2% de variação). Daemonizado:
`python scripts/mecha_daemon.py --name cost-optimize --interval 6h --cmd "python cost_monitor.py"`.

## 5. Convenções MECHA
Fail-closed; **kill-lixo** (sem temporários órfãos — o daemon limpa o lock ao sair); status file como verdade de saúde; nada destrutivo no tick sem confirmação. O daemon roda na máquina do usuário **continuamente** — mantenha o tick read-only por padrão e ponha `--timeout` para não travar.

## Bundle
- `scripts/mecha_daemon.py` — o runner pronto (stdlib puro, Windows/POSIX).
- `scripts/cost_monitor.py.example` — exemplo de tick determinístico.
- `references/launch_windows.md` — launcher, registro no boot, e como parar/observar.
