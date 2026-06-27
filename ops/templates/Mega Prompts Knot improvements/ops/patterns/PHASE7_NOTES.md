# Fase 7 — Patches aplicados (copiar por cima)

Substitua dois arquivos em `.mecha\ops\patterns\`:
- `claw_control.py`  (firewall cognitivo via Ollama)
- `claw_loop.py`     (auto-recuperação + telemetria do dashboard)

`claw_brain.py` (Visão Gemini) **já estava pronto** — não precisa mexer.
`telegram_bot.py` **não muda**: ele já encaminha qualquer ação via `/api/preempt`, então os botões novos do dashboard (`firewall_allow` / `firewall_block_confirm`) já funcionam.

---

## O que mudou

### claw_control.py — Firewall Cognitivo (Opção 4)
`validate_action_safety(x, y)` agora tem 2 camadas:
1. **Rápida (determinística):** lista `PROHIBITED_WORDS` (ampliada). Bloqueia na hora.
2. **Cognitiva (Ollama local):** se houver texto ambíguo sob o clique, consulta o `llama3` (`claw_brain.ask_ollama`) pedindo um JSON `{"risk": safe|dangerous|destructive, "reason": ...}`. Se for `dangerous`/`destructive`, bloqueia.
- Em qualquer bloqueio, grava `claw_control.LAST_BLOCK = {action, risk, reason, context, id}` (lido pelo loop e pelo dashboard).
- Modelo configurável: variável de ambiente `CLAW_FIREWALL_MODEL` (default `llama3`).

### claw_loop.py — Auto-Recuperação (Opção 3) + Telemetria (Opção 2)
- **Contador `window_miss_count`:** quando a janela alvo não está em foco, tenta `focus_window_by_title`; se ausente por **3 ciclos seguidos**, dispara `launch_target_app` (relança a app), avisa no Telegram e zera o contador.
- **`update_claw_status` agora emite** os campos que acendem os chips do dashboard:
  `vision {active, using_image, last_action}`, `firewall {armed, block}`, `recovery {misses, last}`, `events[]`.
- **Visão:** marca `using_image=true` quando o frame é enviado ao Gemini e registra a decisão da IA.
- **Firewall:** ao pegar o `PermissionError("FIREWALL_BLOCK...")`, popula `CLAW_FIREWALL["block"]`, notifica e pausa — o chip fica vermelho e o alerta aparece no painel.
- **Novos comandos de preempção:** `firewall_allow` (libera) e `firewall_block_confirm` (mantém) — os botões "Liberar" / "Manter bloqueio" do `mecha.html`.

---

## Pré-requisitos
- **Ollama** rodando local com o modelo: `ollama pull llama3` e `ollama serve` (porta 11434).
- **Gemini** (opcional p/ visão): `set GEMINI_API_KEY=...` antes de rodar o loop.
- Auto-recuperação de apps fora do Obsidian: defina `CLAW_TARGET_APP_PATH` com o caminho do .exe alvo.

## Como testar (bate com o "Verification Plan" do plano)
1. **Dashboard vivo:** suba o servidor (resolva o 404 do nginx antes) e abra `mecha.html`.
   Rode o loop: `python claw_loop.py --target "Obsidian" --goal "abrir busca"`.
   → os chips Visão/Firewall/Recuperação saem de "offline" e o log de eventos popula.
2. **Visão (Gemini):** com `GEMINI_API_KEY` setada, confira no log "Enviando frame ao Gemini" e a decisão multimodal.
3. **Auto-recuperação:** feche a janela alvo de propósito → após 3 ciclos, o Claw tenta relançar e avisa no Telegram.
4. **Firewall:** aponte o alvo para um botão perto de texto tipo "Excluir/Apagar" → o clique é bloqueado, o alerta aparece no painel; teste os botões **Liberar** / **Manter bloqueio**.

> Os campos novos do status são todos opcionais no front — se algo não emitir, o chip só fica apagado, sem quebrar nada.
