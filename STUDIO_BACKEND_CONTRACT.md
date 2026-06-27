# 🔌 Contrato de Integração — Mecha Huggs Workforce Studio (HWorkforceStudio)

**Objetivo:** especificar o back-end real (sem mocks) que o frontend do **Studio** deve consumir.
**Back-end escolhido:** servidor do dashboard em `telegram_bot.py` (classe `MechaHTTPHandler`).
**Status:** back-end revisado, endurecido e renomeado nesta sessão. **Aguardando o design do frontend** para fazer a ligação final.

---

## 1. Identidade do produto

| Campo | Valor |
|-------|-------|
| Nome de exibição (UI) | **Mecha Huggs Workforce Studio** |
| Identificador técnico | **HWorkforceStudio** |
| Exposto em | `GET /api/health` → `{ "product", "slug" }` e no log de inicialização do servidor |

Use o nome completo em títulos/cabeçalhos visíveis e `HWorkforceStudio` em identificadores técnicos (título de janela, classes, nome de pacote, chaves de config).

---

## 2. Base URL e portas

- Padrão: `http://localhost:8585`
- Fallback automático (se 8585 ocupada): `8282` → `8181` → `9999` → porta dinâmica (ver log de inicialização).
- **CORS já habilitado** (`Access-Control-Allow-Origin: *`, métodos `GET, POST, OPTIONS`, header `Content-Type`) — o Studio pode ser servido de outra origem (arquivo local, Vite/React em outra porta, etc.). Preflight `OPTIONS` responde 200.

> Se o Studio for servido **pelo próprio** `telegram_bot.py` (arquivos estáticos a partir de `.mecha/ops/`), use caminhos **relativos/absolutos de raiz** (ex.: `/api/status`). Se for hospedado **à parte**, aponte os `fetch` para `http://localhost:8585` (configurável via uma constante `BACKEND_URL`).

---

## 3. Endpoints (dados reais, não mockados)

### `GET /api/health`  *(novo nesta sessão)*
Confirma que o back-end está no ar e reporta a identidade do produto + frescor do loop do Claw.
```json
{ "product": "Mecha Huggs Workforce Studio", "slug": "HWorkforceStudio",
  "status": "online", "claw_loop": "online" }
```
`claw_loop` = `"online"` se `claw_status.json` foi atualizado nos últimos 45s, senão `"offline"`.

### `GET /api/status`
Retorna o conteúdo **real** de `claw_status.json` (escrito pelo `claw_loop.py` e pelos bots). Schema esperado pela UI:
```json
{
  "loop_state": "running | paused | offline",
  "step": 12, "max_steps": 100,
  "last_seen_title": "Obsidian — Vault",
  "current_goal": "…",
  "last_thumbnail": "C:\\…\\ops\\logs\\thumbs\\frame.png",
  "events": [ { "time": "14:25:10", "level": "ok|info|warn|danger|vision", "msg": "…", "id": "…" } ]
}
```
Sem arquivo → `{ "error": "No status found", "loop_state": "offline" }`. Recomendação de polling: **1500 ms** (como o dashboard atual).

### `POST /api/preempt`
Envia comando de controle ao Claw (grava `claw_preempt.json`, consumido pelo loop). Corpo:
```json
{ "action": "<ação>", "params": { … } }
```
Ações suportadas (via `send_preempt_command` / playbooks): `pause`, `resume`, `stop`, `set_goal` `{ "goal": "…" }`, `click` `{ "x": int, "y": int }`, `type` `{ "text": "…" }`.
Resposta: `200 { "ok": true }` · faltando `action` → `400 { "error": "Missing action" }`.

### `GET /maps/navigation_graph.json`
Grafo de navegação **real** (arquivo em `.mecha/ops/maps/navigation_graph.json`). O `demoGraph` do `mecha.html` é **apenas fallback** caso o fetch falhe — no Studio, trate o fallback como estado de erro visível, não como dado normal.

### Estáticos
Servidos a partir de `.mecha/ops/` (o servidor faz `chdir` para lá). Ex.: dashboard atual em `http://localhost:8585/mecha.html`.

---

## 4. Checklist de "não mockado" para o frontend do Studio

1. Todo dado de tela vem de `GET /api/status` (não de constantes locais).
2. Ações de botão chamam `POST /api/preempt` (não `console.log`/stubs).
3. Grafo vem de `GET /maps/navigation_graph.json`; `demo*` só como estado de erro.
4. Exibir nome/efetividade do back-end via `GET /api/health` (badge "online/offline").
5. `BACKEND_URL` configurável; sem URLs/respostas hardcoded.

---

## 5. Endurecimento aplicado ao back-end nesta sessão

- Escrita **atômica** (`tmp`+`os.replace`) + lock em `claw_status.json`/`claw_preempt.json` → o Studio nunca lê JSON parcial.
- `GET /api/health` adicionado (identidade + saúde).
- Renomeação para **Mecha Huggs Workforce Studio / HWorkforceStudio** (health, banner, help do Telegram).
- **Token do Telegram deixou de ser logado** (mascarado via `_scrub_token`).

---

## 6. ⚠️ Pendências de segurança (ação do operador)

1. **Rotacionar o token do Telegram**: havia um token real em `.mecha/ops/.env` e ele aparecia em logs de erro. Gere um novo no **BotFather** e substitua no `.env`. *(Adicionei `.mecha/.gitignore` para impedir commits futuros de `.env`.)*
2. **Amanda (8686):** defina `TEAMS_SHARED_SECRET` em produção (agora é *fail-closed*; sem o segredo o webhook responde 503, salvo `MECHA_ALLOW_INSECURE=1` em dev).
3. **OneDrive:** o workspace está sob OneDrive; durante sync o arquivo pode ser lido truncado por outro processo. Rode a stack a partir de um caminho fora do OneDrive (ou pause o sync ao executar) para evitar imports parciais.

---

## 7. O que preciso de você para concluir a ligação (frontend)

- O **design do Studio** (HTML único, ou projeto React/JSX — me diga qual).
- Como ele será hospedado: servido pelo `telegram_bot.py` (estático) **ou** app separado (Vite/Next em outra porta)?

Com isso eu: integro ao repo, troco mocks por `fetch` real nos endpoints acima, aplico o nome **Mecha Huggs Workforce Studio / HWorkforceStudio** e valido a ligação ponta a ponta.
