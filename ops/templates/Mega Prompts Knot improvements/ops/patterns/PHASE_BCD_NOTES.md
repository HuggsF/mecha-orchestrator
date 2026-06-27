# Fases B, C e D — MECHA × FreeScout (copiar por cima)

Arquivos em `.mecha\ops\patterns\`:
- **NOVO:** `claw_freescout.py`  (cliente FreeScout + lógica de incidente, stdlib)
- **Atualizado:** `claw_loop.py`   (reporta incidentes ao FreeScout + telemetria do incidente)

Front em `.mecha\ops\`:
- **Atualizado:** `mecha.html`     (mostra o chamado vinculado no alerta + linha de incidente)

`claw_brain.py`, `claw_control.py` e `telegram_bot.py` **não mudam**.

---

## Fase B — MECHA → FreeScout
Quando o **firewall bloqueia** uma ação OU a **auto-recuperação** dispara (janela ausente 3 ciclos), o `claw_loop` chama `report_incident(...)` e abre um **chamado no FreeScout** (`claw_freescout.open_or_update_incident`).
- **Dedup por sessão:** o 1º evento de cada tipo (`firewall`, `recovery`) cria a conversation; os próximos viram **notas** na mesma — sem spam.
- Cliente sintético do robô: `mecha-claw@telegram.local`. Tags: `mecha-claw`, `firewall`/`recovery`.
- Best-effort: se o FreeScout estiver fora, o loop segue normal (só não registra).

## Fase C — Unificação (Telegram + Dashboard)
- A notificação do Telegram do bloqueio agora inclui **`📋 Chamado FreeScout: #N`**.
- O `claw_status.json` ganha o campo **`incident {number, url, kind}`** e o `block` ganha **`ticket` / `ticket_url`**.
- O `mecha.html` mostra **"Chamado FreeScout #N aberto"** no alerta do firewall e uma **linha "Incidente vinculado → #N · abrir"** no rail (com link pro FreeScout).

## Fase D — Consolidação
- **Mesma config do FreeScout** dos dois sistemas (HuggsBot e MECHA): `FREESCOUT_URL`, `FREESCOUT_API_KEY`, `FREESCOUT_MAILBOX_ID`. O MECHA lê do `.env` em `.mecha/`.
- Tudo é **best-effort + degradável**: sem FreeScout, nada quebra; sem campos novos, o dashboard só não mostra o incidente.
- Fluxo unificado final:
  ```
  HuggsBot (Telegram) ─┐
                       ├─→  FreeScout (chamados)  ──(webhook)──→  Telegram
  MECHA Claw ──────────┘            ▲
     firewall / auto-recuperação ───┘   e aparece no mecha.html (incidente vinculado)
  ```

---

## Pré-requisitos / teste
1. `.env` em `.mecha/` com `FREESCOUT_URL` + `FREESCOUT_API_KEY` (+ mailbox). Módulo *API & Webhooks* ativo.
2. Suba o daemon + dashboard (porta 8000 livre do nginx) e o `claw_loop.py`.
3. **Testar firewall:** mire um botão perto de "Excluir/Apagar" → bloqueia, abre chamado, e o nº aparece no alerta do dashboard e na notificação do Telegram.
4. **Testar recuperação:** feche a janela alvo → após 3 ciclos, relança e abre/atualiza o chamado de `recovery`.
5. Confira o chamado criado na UI do FreeScout (porta 8080) com as tags `mecha-claw` + tipo.
