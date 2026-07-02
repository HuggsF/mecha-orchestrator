# SEND-242 — [COMPANION][MELHORIA] Roleta Pós-Fechamento de Modal Ser Disparada Pelo Tracker - enableModal()

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | Urgent |
| Responsável | Vinicius Carneiro |
| Time | Sendspeed |
| Projeto | — |
| Labels | — |
| Parent | — |
| Criada | 2025-11-10T13:15:20.927Z por bruno.heidrich@sendspeed.com |
| Iniciada | 2025-11-12T12:08:32.742Z |
| Concluída | 2025-12-01T21:03:50.791Z |
| Arquivada | 2026-06-04T22:49:20.984Z |
| Vencimento | — |
| Branch | hugofernandes/send-242-companionmelhoria-roleta-pos-fechamento-de-modal-ser |
| URL | https://linear.app/sendspeed/issue/SEND-242/companionmelhoria-roleta-pos-fechamento-de-modal-ser-disparada-pelo |

## Descrição

**Como** Head de Produto
**Quero** que a **roleta seja disparada pelo tracker** após o fechamento do modal, e não mais via GTM,
**Para** ter controle total das regras de exibição e melhorar a experiência do usuário.

### Critérios de Aceite

* A segunda roleta deve ser acionada apenas se o usuário:
  * Fechou o modal (clique em X)
  * Nunca viu a roleta (sessionId)
    * A roleta não deve reaparecer para o mesmo usuário.
  * Nunca realizou login (localStorage: UserIn_Login = True)
  * 2 segundos após
* O disparo deve vir diretamente do **tracker**, substituindo o trigger anterior do GTM.
* Deve ser possível monitorar o disparo via logs e eventos.

## Histórico de status
- To-do (unstarted): 2025-11-10T13:15:20.927Z → 2025-11-12T12:08:32.755Z
- In Progress (started): 2025-11-12T12:08:32.755Z → 2025-11-13T18:41:25.137Z
- Pull Request (started): 2025-11-13T18:41:25.137Z → 2025-11-14T20:57:05.624Z
- Product Review (started): 2025-11-14T20:57:05.624Z → 2025-12-01T21:03:50.809Z
- Released (completed): 2025-12-01T21:03:50.809Z → atual

## Relações
—

## Anexos
—
