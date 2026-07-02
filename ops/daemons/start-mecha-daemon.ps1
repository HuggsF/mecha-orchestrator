# start-mecha-daemon.ps1 — inicia o daemon de custo do MechaShell em background (Windows)
# Uso:  powershell -ExecutionPolicy Bypass -File .\start-mecha-daemon.ps1
# Para registrar no logon (roda sozinho a cada boot):
#   schtasks /Create /TN "MechaCostDaemon" /SC ONLOGON /RL LIMITED /F `
#     /TR "powershell -WindowStyle Hidden -ExecutionPolicy Bypass -File `"$PSScriptRoot\start-mecha-daemon.ps1`""

$ErrorActionPreference = "Stop"
$daemon = Join-Path $PSScriptRoot "mecha_daemon.py"
$job    = Join-Path $PSScriptRoot "cost_monitor.py"

Start-Process -WindowStyle Hidden -FilePath "python" -ArgumentList @(
    "`"$daemon`"", "--name", "cost-optimize", "--interval", "6h", "--cmd", "python `"$job`""
)

$state = Join-Path $PSScriptRoot ".state\cost-optimize.status.json"
Write-Host "[MECHA] daemon cost-optimize iniciado (intervalo 6h)."
Write-Host "[MECHA] heartbeat/status: $state"
Write-Host "[MECHA] parar: encerre o processo python do daemon (ou Stop-Process), ou remova o lock em .state\cost-optimize.lock"
