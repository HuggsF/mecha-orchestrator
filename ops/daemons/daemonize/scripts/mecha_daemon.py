#!/usr/bin/env python3
"""
mecha_daemon.py — transforma um job periódico/agendado em um DAEMON resiliente.

Diferença (cron vs daemon):
- Uma scheduled task (cron) dispara execuções discretas e depende do
  scheduler/app estar de pé.
- Um daemon é um processo persistente e auto-supervisionado: instância única
  (lockfile), fail-closed (um tick que falha NUNCA derruba o loop), backoff em
  falhas repetidas, log estruturado, heartbeat/status (estilo Shura/claw_status)
  e shutdown gracioso.

Uso:
  python mecha_daemon.py --name cost-optimize --interval 6h --cmd "python job.py"
  python mecha_daemon.py --name X --interval 30m --module pacote.modulo:func
  python mecha_daemon.py --name X --interval 6h --cmd "..." --run-once   # 1 tick (teste)

Convenções MECHA: fail-closed, kill-lixo (sem temporários órfãos), status file
atualizado a cada tick em <state-dir>/<name>.status.json.
"""
from __future__ import annotations
import argparse, json, os, re, signal, sys, time, subprocess, importlib, datetime, traceback

UNIT = {"s": 1, "m": 60, "h": 3600, "d": 86400}

def parse_interval(s: str) -> int:
    m = re.fullmatch(r"\s*(\d+)\s*([smhd])\s*", s, re.I)
    if not m:
        raise SystemExit(f"--interval inválido {s!r}; use 30s/15m/6h/1d")
    return int(m.group(1)) * UNIT[m.group(2).lower()]

def now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def _alive(pid: int) -> bool:
    try:
        if os.name == "nt":
            import ctypes
            h = ctypes.windll.kernel32.OpenProcess(0x1000, 0, pid)
            if h:
                ctypes.windll.kernel32.CloseHandle(h)
                return True
            return False
        os.kill(pid, 0)
        return True
    except Exception:
        return False

class Daemon:
    def __init__(self, name, interval, state_dir, run_once=False, max_backoff=8):
        self.name, self.interval, self.run_once = name, interval, run_once
        self.state_dir = state_dir; os.makedirs(state_dir, exist_ok=True)
        self.lock = os.path.join(state_dir, f"{name}.lock")
        self.status = os.path.join(state_dir, f"{name}.status.json")
        self.logf = os.path.join(state_dir, f"{name}.log")
        self.stop = False; self.fails = 0; self.max_backoff = max_backoff

    def _acquire(self):
        if os.path.exists(self.lock):
            try:
                pid = int(open(self.lock).read().strip())
                if _alive(pid):
                    raise SystemExit(f"[{self.name}] já está rodando (pid {pid})")
            except ValueError:
                pass  # lock corrompido -> sobrescreve
        open(self.lock, "w").write(str(os.getpid()))

    def _release(self):
        try: os.remove(self.lock)
        except OSError: pass

    def _status(self, state, last=None, nxt=None):
        try:
            json.dump({"name": self.name, "pid": os.getpid(), "state": state,
                       "updated": now(), "last_status": last,
                       "consecutive_failures": self.fails, "next_run": nxt,
                       "interval_s": self.interval}, open(self.status, "w"), indent=2)
        except OSError:
            pass

    def _log(self, msg):
        line = f"{now()} [{self.name}] {msg}\n"
        try:
            with open(self.logf, "a", encoding="utf-8") as f: f.write(line)
        except OSError:
            pass
        print(line, end="", flush=True)

    def _sleep(self, secs):  # interruptível
        end = time.time() + secs
        while time.time() < end and not self.stop:
            time.sleep(min(1.0, max(0.0, end - time.time())))

    def run(self, tick):
        self._acquire()
        for s in (signal.SIGINT, getattr(signal, "SIGTERM", None), getattr(signal, "SIGBREAK", None)):
            if s is not None:
                try: signal.signal(s, lambda *_: setattr(self, "stop", True))
                except (ValueError, OSError): pass
        self._log(f"daemon UP; interval={self.interval}s; run_once={self.run_once}")
        try:
            while not self.stop:
                self._status("running")
                t0 = time.time()
                try:
                    tick()                                   # <- fail-closed
                    self.fails = 0
                    self._log(f"tick OK em {time.time()-t0:.1f}s")
                    self._status("idle", last="ok")
                except Exception as e:
                    self.fails += 1
                    self._log(f"tick FALHOU ({self.fails}): {e}\n{traceback.format_exc()}")
                    self._status("idle", last=f"error: {e}")
                if self.run_once or self.stop:
                    break
                factor = min(2 ** min(self.fails, 3), self.max_backoff) if self.fails else 1
                wait = self.interval * factor
                nxt = (datetime.datetime.now(datetime.timezone.utc) +
                       datetime.timedelta(seconds=wait)).isoformat()
                self._status("sleeping", nxt=nxt)
                self._log(f"próximo run em {wait}s ({'backoff x%d' % factor if factor > 1 else 'normal'})")
                self._sleep(wait)
        finally:
            self._status("stopped")
            self._log("daemon DOWN")
            self._release()

def make_tick(args):
    if args.cmd:
        def tick():
            p = subprocess.run(args.cmd, shell=True, capture_output=True, text=True, timeout=args.timeout)
            if p.returncode != 0:
                raise RuntimeError(f"cmd exit {p.returncode}: {(p.stderr or '')[-300:]}")
            return p.stdout
        return tick
    if args.module:
        mod, _, fn = args.module.partition(":")
        return getattr(importlib.import_module(mod), fn or "main")
    raise SystemExit("forneça --cmd ou --module pacote.modulo:func")

def main():
    ap = argparse.ArgumentParser(description="Roda um job periódico como daemon resiliente")
    ap.add_argument("--name", required=True)
    ap.add_argument("--interval", default="6h")
    ap.add_argument("--cmd")
    ap.add_argument("--module")
    ap.add_argument("--state-dir", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), ".state"))
    ap.add_argument("--timeout", type=int, default=3600)
    ap.add_argument("--run-once", action="store_true")
    a = ap.parse_args()
    Daemon(a.name, parse_interval(a.interval), a.state_dir, run_once=a.run_once).run(make_tick(a))

if __name__ == "__main__":
    main()
