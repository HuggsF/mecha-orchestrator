param(
    [string]$Command,
    [string]$SubCommand,
    [string]$Target,
    [string]$Goal
)

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

function Show-Help {
    Write-Host "==========================================================" -ForegroundColor Cyan
    Write-Host "                MECHA SYSTEM CLI SDK                      " -ForegroundColor Cyan
    Write-Host "==========================================================" -ForegroundColor Cyan
    Write-Host "Uso:"
    Write-Host "  mecha sdk check-plan <path_to_markdown> : Valida metadados e AST"
    Write-Host "  mecha sdk draw <path_to_json>          : Renderiza imagem vetorial"
    Write-Host "  mecha sdk draw-test                    : Roda o teste do Canvas"
    Write-Host "  mecha sdk scan                         : Executa varredura de janela ativa"
    Write-Host "  mecha sdk graph                        : Exibe grafo de navegacao de janelas"
    Write-Host '  mecha sdk run-claw "<title>" [-goal "<instrucao>"] : Dispara loop do Claw guiado por IA'
    Write-Host "  mecha sdk find-icon <template_name>    : Procura um template na tela ativa"
    Write-Host "  mecha sdk comfy-render <json_path>     : Envia geracao para o ComfyUI"
    Write-Host "  mecha sdk find-text <target_text>      : Localiza e encontra a posicao de um texto"
    Write-Host "  mecha sdk sync-obsidian                : Sincroniza o grafo atual com o Obsidian"
    Write-Host "  mecha sdk run-bot                      : Inicializa o Bot do Telegram de preempção"
    Write-Host "  mecha sdk tribunal-test                : Executa testes E2E integrados do Tribunal"
    Write-Host ""
    Write-Host "Comandos adicionais:"
    Write-Host "  mecha help                             : Mostra este menu de ajuda"
    Write-Host "==========================================================" -ForegroundColor Cyan
}

# Inicializador principal
if ($Command -eq "help" -or -not $Command) {
    Show-Help
    exit 0
}

if ($Command -eq "sdk") {
    if ($SubCommand -eq "check-plan") {
        if (-not $Target) {
            Write-Error "Caminho do arquivo Markdown nao fornecido."
            exit 1
        }
        $absPath = Resolve-Path $Target -ErrorAction SilentlyContinue
        if (-not $absPath) {
            $absPath = $Target
        }
        Write-Host "[*] Executando validador de planos (Pydantic / AST)..." -ForegroundColor Yellow
        python "$PSScriptRoot/patterns/dynamic_typing.py" --validate "$absPath"
        exit $LASTEXITCODE
    }
    elseif ($SubCommand -eq "draw") {
        if (-not $Target) {
            Write-Error "Caminho do arquivo JSON nao fornecido."
            exit 1
        }
        Write-Host "[*] Executando renderizador vetorial do Canvas..." -ForegroundColor Yellow
        python "$PSScriptRoot/patterns/claw_canvas.py" --draw "$Target"
        exit $LASTEXITCODE
    }
    elseif ($SubCommand -eq "draw-test") {
        Write-Host "[*] Executando geracao de teste do Canvas..." -ForegroundColor Yellow
        python "$PSScriptRoot/patterns/claw_canvas.py" --test
        exit $LASTEXITCODE
    }
    elseif ($SubCommand -eq "scan") {
        Write-Host "[*] Executando varredura da janela ativa..." -ForegroundColor Yellow
        python "$PSScriptRoot/patterns/claw_vision.py"
        exit $LASTEXITCODE
    }
    elseif ($SubCommand -eq "graph") {
        Write-Host "[*] Exibindo o grafo de navegacao de janelas..." -ForegroundColor Yellow
        python "$PSScriptRoot/patterns/claw_graph.py"
        exit $LASTEXITCODE
    }
    elseif ($SubCommand -eq "run-claw") {
        if (-not $Target) {
            Write-Error "Titulo da janela alvo nao fornecido."
            exit 1
        }
        Write-Host "[*] Iniciando o loop de acoes físicas do Claw na janela '$Target'..." -ForegroundColor Yellow
        if ($Goal) {
            python "$PSScriptRoot/patterns/claw_loop.py" --target "$Target" --goal "$Goal"
        } else {
            python "$PSScriptRoot/patterns/claw_loop.py" --target "$Target"
        }
        exit $LASTEXITCODE
    }
    elseif ($SubCommand -eq "find-icon") {
        if (-not $Target) {
            Write-Error "Nome do template visual nao fornecido."
            exit 1
        }
        Write-Host "[*] Procurando template visual '$Target' na tela ativa..." -ForegroundColor Yellow
        python "$PSScriptRoot/patterns/claw_cv.py" --find "$Target"
        exit $LASTEXITCODE
    }
    elseif ($SubCommand -eq "comfy-render") {
        if (-not $Target) {
            Write-Error "Caminho do arquivo JSON de request nao fornecido."
            exit 1
        }
        Write-Host "[*] Enviando requisicao de render para o ComfyUI..." -ForegroundColor Yellow
        python "$PSScriptRoot/patterns/claw_comfy.py" --render "$Target"
        exit $LASTEXITCODE
    }
    elseif ($SubCommand -eq "find-text") {
        if (-not $Target) {
            Write-Error "Texto-alvo nao fornecido."
            exit 1
        }
        Write-Host "[*] Procurando texto '$Target' na tela ativa..." -ForegroundColor Yellow
        python "$PSScriptRoot/patterns/claw_ocr.py" --find-text "$Target"
        exit $LASTEXITCODE
    }
    elseif ($SubCommand -eq "sync-obsidian") {
        Write-Host "[*] Sincronizando grafo com o Obsidian..." -ForegroundColor Yellow
        python "$PSScriptRoot/patterns/claw_graph.py" --sync-obsidian
        exit $LASTEXITCODE
    }
    elseif ($SubCommand -eq "run-bot") {
        Write-Host "[*] Inicializando o bot do Telegram..." -ForegroundColor Yellow
        python "$PSScriptRoot/patterns/telegram_bot.py"
        exit $LASTEXITCODE
    }
    elseif ($SubCommand -eq "tribunal-test") {
        Write-Host "[*] Executando testes fim-a-fim do Tribunal..." -ForegroundColor Yellow
        python "$PSScriptRoot/patterns/test_e2e_tribunal.py"
        exit $LASTEXITCODE
    }
    else {
        Write-Error "Subcomando SDK '$SubCommand' desconhecido."
        Show-Help
        exit 1
    }
}
else {
    Write-Error "Comando '$Command' desconhecido."
    Show-Help
    exit 1
}
