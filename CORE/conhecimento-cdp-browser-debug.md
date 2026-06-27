---
name: Conhecimento Chrome DevTools Protocol (CDP)
description: Acesso ao navegador via terminal — funciona com Chrome, Edge, OperaGX (qualquer Chromium). Testado no notebook 02/04/2026.
type: reference
---

# Chrome DevTools Protocol (CDP) — Acesso ao navegador via terminal

## O que e

Protocolo que permite conectar ao navegador via WebSocket e controlar/inspecionar programaticamente. Funciona com qualquer browser baseado em Chromium (Chrome, Edge, OperaGX, Brave).

## Como usar

1. Abrir o browser com a flag de debug:
```
"C:/Program Files/Google/Chrome/Application/chrome.exe" --remote-debugging-port=9222
```

2. Testar conexao:
```
curl -s http://localhost:9222/json/version
```

3. Listar abas:
```
curl -s http://localhost:9222/json
```

## O que da pra fazer

- Listar abas abertas (titulo, URL)
- Capturar console logs e erros JS
- Inspecionar DOM (elementos da pagina)
- Monitorar network requests
- Tirar screenshots
- Executar JavaScript na pagina

## Caminhos dos browsers

- Chrome: `C:/Program Files/Google/Chrome/Application/chrome.exe`
- OperaGX: `C:/Users/vanessa.rsilva/AppData/Local/Programs/Opera GX/opera.exe` (verificar)
- Edge: `C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe`

## Cuidados

- Se usar `taskkill //F //IM chrome.exe` fecha TODOS os processos do Chrome, nao so o de debug
- O perfil temporario (`--user-data-dir=temp`) abre limpo (sem contas logadas)
- Sem `--user-data-dir`, abre com perfil real do usuario (contas, extensoes, tudo)
- Porta 9222 e padrao, pode ser qualquer porta livre

## Testado em

- Notebook trabalho (vanessa.rsilva), Chrome 146.0.7680.153, 02/04/2026 -- funciona
