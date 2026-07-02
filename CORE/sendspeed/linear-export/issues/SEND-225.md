# SEND-225 — [MELHORIA] ROLETA

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | Urgent |
| Responsável | peterson.marques@sendspeed.com |
| Time | Sendspeed |
| Projeto | — |
| Labels | — |
| Parent | — |
| Criada | 2025-10-17T14:28:52.423Z por bruno.heidrich@sendspeed.com |
| Iniciada | 2025-10-22T18:16:59.343Z |
| Concluída | 2025-10-31T13:12:18.554Z |
| Arquivada | 2026-05-06T22:26:33.083Z |
| Vencimento | — |
| Branch | hugofernandes/send-225-melhoria-roleta |
| URL | https://linear.app/sendspeed/issue/SEND-225/melhoria-roleta |

## Descrição

**Como** head de produto

**Quero** uma roleta interativa de prêmios gamificada

**Para** sentir engajamento imediato e incentivar a conversão ou cadastro

---

Critérios de aceite:

* Modal surge com delay configurável ou por evento customizado (window.\__SmartTrack.customEvent('trigger_card_roleta')).
* Roleta gira com animação fluida e feedback visual de “ganhou/perdeu”.
* Regras, prêmios e textos são dinâmicos via JSON (ex: roleta_config.json).
* Registro do evento no GA4 e SmartTrack com categorias:
  * gamification_spin_start
  * gamification_spin_result
  * gamification_reward_claimed
* Exibição de popup de recompensa (CTA: “Resgatar bônus”).
* Comportamento responsivo (desktop e mobile).
* Não conflita com outros modais ativos (e.g. e-book, cashback).

> **[Imagem 1 — transcrição]:** Screenshot de UI de um card modal de gamificação intitulado **"Gire e Ganhe"** (título em amarelo, canto superior esquerdo), com botão **"x"** de fechar no canto superior direito. Fundo do modal escuro/preto com borda roxa. No centro há uma **roleta circular de prêmios** parcialmente visível (mostra a metade superior), com aro amarelo e um ponteiro/botão circular vermelho no topo. Os setores visíveis da roleta: um setor roxo à esquerda (com ícone de dado/dice branco e texto parcial "...ROS", provavelmente "GIROS") e um setor vermelho à direita (com ícone de presente/gift e texto "100 G..." — provavelmente "100 GIROS" ou "100 GEMAS"). É a roleta gamificada descrita na issue.

## Histórico de status
- To-do (unstarted): 2025-10-17T14:28:52.423Z → 2025-10-22T18:16:58.012Z
- Paused (unstarted): 2025-10-22T18:16:58.012Z → 2025-10-22T18:16:59.352Z
- In Progress (started): 2025-10-22T18:16:59.352Z → 2025-10-27T15:06:06.158Z
- Pull Request (started): 2025-10-27T15:06:06.158Z → 2025-10-27T15:06:09.774Z
- Product Review (started): 2025-10-27T15:06:09.774Z → 2025-10-31T13:12:18.565Z
- Released (completed): 2025-10-31T13:12:18.565Z → atual

## Relações
—

## Anexos
—
