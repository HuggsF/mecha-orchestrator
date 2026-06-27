# Script de compilação do executável MECHA App via PyInstaller

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "          COMPILANDO MECHA APP VIA PYINSTALLER            " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# Verifica se a pasta assets existe para empacotar
if (-not (Test-Path "assets")) {
    New-Item -ItemType Directory -Path "assets" -Force | Out-Null
}
if (-not (Test-Path "assets/temp_states")) {
    New-Item -ItemType Directory -Path "assets/temp_states" -Force | Out-Null
}

Write-Host "[*] Iniciando compilação do executável single-file..." -ForegroundColor Yellow
python -m PyInstaller --onefile --name="mecha_app" `
  -p patterns `
  --exclude-module="torch" `
  --exclude-module="tensorflow" `
  --exclude-module="numpy" `
  --exclude-module="pandas" `
  --exclude-module="matplotlib" `
  --exclude-module="scipy" `
  --exclude-module="tensorboard" `
  --exclude-module="onnx" `
  --exclude-module="sympy" `
  --exclude-module="jinja2" `
  --add-data "patterns;patterns" `
  --add-data "mecha.html;." `
  --add-data "templates;templates" `
  --add-data "assets;assets" `
  mecha_app.py

if ($LASTEXITCODE -eq 0) {
    Write-Host "[+] COMPILAÇÃO CONCLUÍDA COM SUCESSO!" -ForegroundColor Green
    Write-Host "[+] Executável gerado em: $PSScriptRoot/dist/mecha_app.exe" -ForegroundColor Green
} else {
    Write-Host "[!] FALHA NA COMPILAÇÃO DO EXECUTÁVEL. Código: $LASTEXITCODE" -ForegroundColor Red
    exit 1
}
