<#
.SYNOPSIS
MECHA SYSTEM CLI SDK - Wrapper
Encaminha as chamadas para o motor Python centralizado em ops/cli/mecha_cli.py
#>

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# SYSTEM PROMPT (MoE / Hiansen Rules)
$env:MECHA_SYSTEM_PROMPT = "Você é o Orquestrador-Mestre MoE do Mecha. Siga as regras do Hiansen de sanitização e debate antes de atuar. Delegue tarefas para o respectivo squad de acordo com a Ontologia."

$CLI_PY = Join-Path $PSScriptRoot "cli\mecha_cli.py"

if ($args.Count -eq 0 -or $args[0] -eq "help") {
    python $CLI_PY -h
    exit $LASTEXITCODE
}

# Repassa todos os argumentos do script para o Python transparente
python $CLI_PY $args
exit $LASTEXITCODE
