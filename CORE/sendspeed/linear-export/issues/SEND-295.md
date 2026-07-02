# SEND-295 — Seletor de rotas dentro da Smartico.

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | No priority |
| Responsável | Hugo Fernandes |
| Time | Sendspeed |
| Projeto | — |
| Labels | Melhoria, Sendspeed, User Story |
| Parent | — |
| Criada | 2026-01-30T13:17:24.593Z por Vinicius Carneiro |
| Iniciada | 2026-03-05T18:45:54.868Z |
| Concluída | 2026-06-22T17:15:45.395Z |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-295-seletor-de-rotas-dentro-da-smartico |
| URL | https://linear.app/sendspeed/issue/SEND-295/seletor-de-rotas-dentro-da-smartico |

## Descrição

> **Como Operador de CRM**
> **Quero acessar a Smartico e configurar uma campanha de SMS podendo selecionar a rota Gold ou Platinum**
> **Para que a SendSpeed realize o disparo utilizando exatamente a rota escolhida, sem falhas, inconsistências ou bugs no envio**

---

# Use Case:

O Tulio tem que entrar na Smartico e configurar uma campanha de SMS e poder selecionar entre a rota Gold ou Platinum e a SendSpeed precisa disparar na rota selecionada sem haver falhas ou bugs.

---

**IMPORTANTE:** A partir de FEV/26 nossos clientes poderão entrar em 8 faixas diferente de preço baseado na quantidade de disparo e/ou relacionamento. Cada rota vai ter o seu preço dentro das 8 faixas válido para qualquer produto da SendSpeed. Então, devemos separar as rotas por grupos (Gold, Platinum) podendo ser configuradas na plataforma.

A rota Gold ela vai usar a rota da Pushfy ou Sona bet3 (por enquanto priorizar Pushfy).

A rota Platinum ela vai usar a Sona Bet2.

Esses grupos devem ser capaz de serem personalizaveis diretamente na plataforma.

---

# **Critérios de Aceite:**

* O usuário deve conseguir acessar a Smartico com permissões para criação e edição de campanhas SMS
* Durante a configuração da campanha de SMS, deve existir uma opção clara para seleção da rota de envio:
  * Rota **Gold**
  * Rota **Platinum**
* A rota selecionada na Smartico deve ser enviada corretamente para a SendSpeed no momento do disparo
* A SendSpeed deve realizar o envio do SMS utilizando **exclusivamente a rota selecionada**, sem fallback automático ou troca de rota não autorizada
* Não deve haver falhas, bugs ou perdas de mensagens relacionadas à escolha da rota
* Logs técnicos devem registrar:
  * ID da campanha
  * Rota selecionada (Gold ou Platinum)
  * Status do disparo
* Em caso de erro no disparo, o erro deve ser retornado de forma clara para monitoramento e troubleshooting
* A campanha deve ser disparada com sucesso quando configurada corretamente, garantindo consistência entre Smartico e SendSpeed

## Histórico de status
- Backlog (backlog): 2026-01-30T13:17:24.593Z → 2026-01-30T14:12:29.285Z
- Refining (backlog): 2026-01-30T14:12:29.285Z → 2026-02-04T15:37:11.630Z
- Backlog (backlog): 2026-02-04T15:37:11.630Z → 2026-02-04T15:37:14.474Z
- To-do (unstarted): 2026-02-04T15:37:14.474Z → 2026-03-05T18:45:54.878Z
- Pull Request (started): 2026-03-05T18:45:54.878Z → 2026-06-22T17:15:45.406Z
- Released (completed): 2026-06-22T17:15:45.406Z → atual

## Relações
—

## Anexos
—
