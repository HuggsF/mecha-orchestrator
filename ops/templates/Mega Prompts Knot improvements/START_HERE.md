# START HERE — Visão geral & como rodar

> Dois sistemas distintos. Não confunda:
> - **MECHA Claw** — robô de automação de desktop + dashboard de telemetria (`mecha.html`).
> - **HuggsBot / Mendas Studio** — sistema de *chamados de comunicação* (Telegram).

---

## ✅ MECHA CLAW — Fase 7 COMPLETA

| Opção | O quê | Status |
|---|---|---|
| 1 | Visão multimodal (Gemini, PNG→Base64 `inlineData`) | ✅ pronto (`claw_brain.py`) |
| 2 | Dashboard reativo (polling 1.5s, log ao vivo, chips) | ✅ pronto (`mecha.html` + status fields) |
| 3 | Auto-recuperação (3 falhas → relança app) | ✅ pronto (`claw_loop.py`) |
| 4 | Firewall cognitivo (lista rápida + Ollama llama3) | ✅ pronto (`claw_control.py`) |

Arquivos já copiados em `.mecha\ops\patterns\`: `claw_control.py`, `claw_loop.py`.
`mecha.html` em `.mecha\ops\mecha.html`. `claw_brain.py` e `telegram_bot.py` não mudaram.

### ▶️ Rodar o MECHA Claw
```powershell
# 1. Porta 8000 livre p/ o servidor Python (o nginx NÃO pode estar nela)
net stop nginx                 # ou troque a porta no telegram_bot.py: ('', 8000) -> ('', 8787)

# 2. Ollama local (firewall cognitivo)
ollama serve                   # e, uma vez:  ollama pull llama3

# 3. (opcional) Visão multimodal
set GEMINI_API_KEY=sua_chave

# 4. Daemon do bot + dashboard (serve ops/ + /api na 8000)
cd .mecha\ops\patterns
python telegram_bot.py
#    abra:  http://localhost:8000/mecha.html   (8787 se trocou a porta)

# 5. Em outro terminal, o loop See-Think-Act
python claw_loop.py --target "Obsidian" --goal "abrir a busca global"
```
Os chips Visão / Firewall / Recuperação saem de "offline" e o log popula a cada 1.5s.

> **Por que dava 404:** o `nginx/1.31.1` estava ocupando a porta 8000 — o servidor Python não conseguia subir nela. Mantenha o nginx fora da 8000 (ou use outra porta no Python).
> **Pré-req extra:** p/ relançar apps que não sejam o Obsidian, defina `CLAW_TARGET_APP_PATH` com o caminho do `.exe`.

---

## ✅ HUGGSBOT — chamados no Telegram  →  `huggsbot/`
Bot conversacional com SLA do PR.COM.001 (categorias 2/3/5/10/15 dias, corte 16h, protocolo, briefing, urgência) + Mini App.
**Persistência:** integra com o **FreeScout** — se configurado, cada `/novo` vira um chamado real lá; senão, cai em memória.

### ▶️ Rodar
```bash
cd huggsbot
python -m venv .venv && source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # Windows: copy .env.example .env
#   cole o TOKEN NOVO em TELEGRAM_TOKEN
#   (opcional) preencha FREESCOUT_URL + FREESCOUT_API_KEY + FREESCOUT_MAILBOX_ID
python huggsbot.py
```
No Telegram: **@Huggies_bbot** → `/start` → `/novo`. No startup o log diz se está em *FreeScout* ou *memória*.

### 🎫 Integração FreeScout (Fase A)
- `/novo` cria uma **conversation** no FreeScout (assunto = `[Nd] título`, cliente = `tg<chat_id>@telegram.local`).
- Categoria/concessão/canal/urgência viram **tags** (com fallback automático se o módulo de Tags não existir) + ficam no corpo; o **prazo (corte 16h)** é calculado pelo bot e gravado no corpo.
- `/status` lê os chamados do cliente direto do FreeScout. A **esteira/visão passa a ser a própria UI do FreeScout** (na porta 8080).
- **Opcional — avisos de volta no Telegram:** rode `python freescout_webhook.py` e no FreeScout (Manage → API & Webhooks → Webhooks) aponte `convo.agent.replied` / `convo.updated` para `http://SEU_HOST:8765/freescout`.
- **Pré-req:** módulo *API & Webhooks* ativo no FreeScout + uma **API Key** (cole só no `.env`).

---

## ⚠️ Avisos importantes
- **Token:** o token que apareceu no chat/print está EXPOSTO. Gere outro no `@BotFather` (/revoke) e cole **só** no `.env` local. Nunca print/cole em lugar nenhum.
- **2 bots, 1 token:** `telegram_bot.py` (MECHA) e `huggsbot.py` (chamados) **não podem** fazer polling no mesmo token ao mesmo tempo (o Telegram derruba com erro de `getUpdates`). Use um bot/token pra cada, ou rode um de cada vez. Nomes de env diferem: MECHA = `TELEGRAM_BOT_TOKEN`, HuggsBot = `TELEGRAM_TOKEN`.

---

## 🎨 Artefatos de design (abrem no navegador)
- `KNOT Studio.dc.html` + `KNOT Studio Playbook.dc.html` — cockpit de megaprompts
- `Mendas Studio Chamados.dc.html` (Teams) · `…Telegram.dc.html` (Telegram) — wireframes do sistema de chamados
- `Mendas Studio Setup.dc.html` + `export/Mendas Studio - Como Configurar.pptx` — deck "Como Configurar"

---

## ✅ MECHA × FreeScout — Fases B/C/D PRONTAS
Os incidentes do MECHA viram chamados no FreeScout e aparecem no Telegram + dashboard.
- **Fase B:** firewall bloqueou OU auto-recuperação → abre/atualiza chamado (`ops/patterns/claw_freescout.py` + `claw_loop.py`). Dedup por sessão (vira nota, sem spam).
- **Fase C:** notificação no Telegram com `#N`, e `mecha.html` mostra "Chamado FreeScout #N" no alerta + linha "Incidente vinculado".
- **Fase D:** mesma config FreeScout dos dois sistemas; tudo best-effort/degradável.
- Detalhes e teste: `ops/patterns/PHASE_BCD_NOTES.md`.
- Copie por cima: `ops/patterns/claw_freescout.py`, `ops/patterns/claw_loop.py`, `ops/mecha.html`.

```
HuggsBot (Telegram) ─┐
                     ├─→  FreeScout (chamados, :8080)  ──webhook──→  Telegram
MECHA Claw ──────────┘     ▲ firewall / auto-recuperação      + incidente no mecha.html
```

---

## ⏳ Falta fazer (opcional / seu lado)
- [ ] **FreeScout:** ativar o módulo *API & Webhooks*, gerar API Key e preencher no `.env` dos dois sistemas (porta 8080 já é o FreeScout).
- [ ] **HuggsBot:** hospedar 24/7 (Railway/Render via Procfile) e setar `MINIAPP_URL` p/ o botão "Abrir painel".
- [ ] **MECHA:** calibrar o prompt de risco do firewall (Ollama) com os falsos-positivos reais da sua operação.
