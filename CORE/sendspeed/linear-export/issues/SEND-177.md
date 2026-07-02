# SEND-177 — TriggerLogin (desativação do behavior)

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | Urgent |
| Responsável | andrei.garcia@externo.sendspeed.com |
| Time | Sendspeed |
| Projeto | — |
| Labels | — |
| Parent | — |
| Criada | 2025-09-26T12:18:50.766Z por bruno.heidrich@sendspeed.com |
| Iniciada | 2025-09-26T15:09:24.528Z |
| Concluída | 2025-11-14T13:59:20.045Z |
| Arquivada | 2026-05-20T22:16:09.187Z |
| Vencimento | — |
| Branch | hugofernandes/send-177-triggerlogin-desativacao-do-behavior |
| URL | https://linear.app/sendspeed/issue/SEND-177/triggerlogin-desativacao-do-behavior |

## Descrição

**Como** Head de Produto
**Quero** que, ao receber um events de usuário logado, o sistema desative automaticamente o behavior,
**Para** evitar que o usuário que não queremos atuar nesse momento seja impactado por cards e acabe prejudicando nossos testes bem como a própria experiencia do usuário.

### Critérios de Aceite

* Se o usuário recebeu um TriggerLogin, **nenhum outro card deve ser exibido** durante aquela sessão.
* O behavior deve ser desativado de forma imediata após o TriggerLogin.
* O estado de desativação deve ser registrado para auditoria e métricas.
* Deve ser possível medir quantos usuários tiveram o behavior desativado por TriggerLogin.

Event = tg_user_login

## Histórico de status
- To-do (unstarted): 2025-09-26T12:18:50.766Z → 2025-09-26T15:09:24.540Z
- In Progress (started): 2025-09-26T15:09:24.540Z → 2025-10-10T15:01:49.390Z
- Product Review (started): 2025-10-10T15:01:49.390Z → 2025-10-30T18:21:55.936Z
- In Progress (started): 2025-10-30T18:21:55.936Z → 2025-11-10T13:16:30.411Z
- Product Review (started): 2025-11-10T13:16:30.411Z → 2025-11-14T13:59:20.061Z
- Released (completed): 2025-11-14T13:59:20.061Z → atual

## Relações
—

## Anexos
—
