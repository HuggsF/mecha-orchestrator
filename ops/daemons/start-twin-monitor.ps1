# start-twin-monitor.ps1 — monitor contínuo do Gêmeo Digital (Neo4j) como daemon (Windows)
# Uso:   powershell -ExecutionPolicy Bypass -File .\start-twin-monitor.ps1
# Boot:  schtasks /Create /TN "MechaTwinMonitor" /SC ONLOGON /RL LIMITED /F `
#          /TR "powershell -WindowStyle Hidden -ExecutionPolicy Bypass -File `"$PSScriptRoot\start-twin-monitor.ps1`""
$ErrorActionPreference = "Stop"
$daemon  = Join-Path $PSScriptRoot "mecha_daemon.py"
$monitor = Join-Path $PSScriptRoot "digital_twin_monitor.py"

Start-Process -WindowStyle Hidden -FilePath "python" -ArgumentList @(
    "`"$daemon`"", "--name", "digital-twin-monitor", "--interval", "15m",
    "--cmd", "python `"$monitor`""
)
Write-Host "[MECHA] monitor do Gemeo Digital iniciado (intervalo 15m)."
Write-Host "[MECHA] saude (p/ o painel Electron): $PSScriptRoot\.state\digital_twin.status.json"
Write-Host "[MECHA] alertas: $PSScriptRoot\.state\alerts.log"
Write-Host "[MECHA] ajuste o intervalo trocando --interval (ex.: 5m, 30m, 1h)."
