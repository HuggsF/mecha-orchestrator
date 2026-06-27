# MECHA PowerShell Profile
# Este arquivo configura aliases e caminhos para o ambiente MECHA

$MECHA_ROOT = Split-Path $PSScriptRoot -Parent

function mecha {
    param(
        [string]$Command,
        [string]$SubCommand,
        [string]$Target
    )
    & "$PSScriptRoot/mecha.ps1" $Command $SubCommand $Target
}

# Feedback visual de inicializacao do Profile
Write-Host "==========================================================" -ForegroundColor Green
Write-Host " [+] MECHA PROFILE LOADED SUCCESSFULLY! " -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Green
