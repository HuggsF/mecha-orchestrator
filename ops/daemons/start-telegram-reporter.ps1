<#
.SYNOPSIS
Inicia o Daemon do Reporter do Telegram em background via PowerShell jobs.
Roda a cada 24 horas (86400s) compilando o harness de infraestrutura e enviando via Telegram.
#>

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$DaemonName = "telegram-reporter"
$Interval = "24h"

Write-Host "Iniciando o daemon '$DaemonName' (Intervalo: $Interval)..." -ForegroundColor Cyan

# Executa o mecha_daemon em background usando Start-Job para no travar o terminal
Start-Job -Name "MECHA_$DaemonName" -ScriptBlock {
    param($dir, $name, $inv)
    Set-Location $dir
    # Passa o --name e --interval corretos para a skill daemonize rodar o loop
    python mecha_daemon.py --name $name --interval $inv --cmd "python telegram_reporter_daemon.py"
} -ArgumentList $ScriptDir, $DaemonName, $Interval | Out-Null

Write-Host "Daemon '$DaemonName' rodando em background!" -ForegroundColor Green
Write-Host "Status: $ScriptDir\.state\$DaemonName.status.json"
Write-Host "Para parar: Stop-Process no python.exe ou delete o arquivo de lock em .state\$DaemonName.lock"
