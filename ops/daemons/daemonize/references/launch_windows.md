# Launcher e supervisão no Windows

## Iniciar em background (oculto)
```powershell
Start-Process -WindowStyle Hidden -FilePath "python" -ArgumentList @(
  "`"$PSScriptRoot\mecha_daemon.py`"", "--name", "cost-optimize",
  "--interval", "6h", "--cmd", "python `"$PSScriptRoot\cost_monitor.py`""
)
```
Ou use o `start-mecha-daemon.ps1` pronto em `.mecha/ops/daemons/`.

## Rodar sozinho a cada logon (substitui o cron do app)
```bat
schtasks /Create /TN "MechaCostDaemon" /SC ONLOGON /RL LIMITED /F ^
  /TR "powershell -WindowStyle Hidden -ExecutionPolicy Bypass -File C:\caminho\start-mecha-daemon.ps1"
```
Para um serviço real (roda sem login, com auto-restart), use **NSSM**:
```
nssm install MechaCostDaemon python "C:\caminho\mecha_daemon.py" --name cost-optimize --interval 6h --cmd "python C:\caminho\cost_monitor.py"
nssm set MechaCostDaemon AppExit Default Restart
nssm start MechaCostDaemon
```

## Observar saúde
- Status (heartbeat): `<state-dir>\<name>.status.json` → `state` (running/sleeping/idle/stopped), `last_status`, `consecutive_failures`, `next_run`.
- Log: `<state-dir>\<name>.log`.
PowerShell rápido:
```powershell
Get-Content .\.state\cost-optimize.status.json | ConvertFrom-Json
Get-Content .\.state\cost-optimize.log -Tail 20 -Wait
```

## Parar
- Encerre o processo python do daemon (ele libera o lock no shutdown gracioso):
  `Get-Process python | Where-Object { $_.Path -like '*mecha_daemon*' } | Stop-Process`
- Se ficou um lock órfão após crash: apague `.state\<name>.lock` (o runner detecta PID morto e sobrescreve sozinho no próximo start).
- Se registrou no schtasks/NSSM: `schtasks /Delete /TN MechaCostDaemon /F` ou `nssm remove MechaCostDaemon confirm`.

## Migrar a scheduled task existente
A task `mechashell-cost-optimize-6h` (cron 6h) e este daemon fazem o mesmo trabalho. Rodando o daemon, **desligue a scheduled task** na aba Scheduled para não duplicar (o lockfile evita duas instâncias do daemon, mas não conhece o cron do app).
