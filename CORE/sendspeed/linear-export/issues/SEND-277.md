# SEND-277 — Integração de campanhas disparadas via Smartico para Send/Uin

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | Urgent |
| Responsável | Hugo Fernandes |
| Time | Sendspeed |
| Projeto | — |
| Labels | Sendspeed, Melhoria, User Story |
| Parent | — |
| Criada | 2026-01-08T18:08:54.630Z por Vinicius Carneiro |
| Iniciada | 2026-01-21T12:37:55.174Z |
| Concluída | 2026-06-22T17:15:55.576Z |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-277-integracao-de-campanhas-disparadas-via-smartico-para-senduin |
| URL | https://linear.app/sendspeed/issue/SEND-277/integracao-de-campanhas-disparadas-via-smartico-para-senduin |

## Descrição

> **Como** usuario da plataforma da Smartico
>
> **Quero** conseguir integrar a criação e disparo das campanhas
>
> **Para** conseguir enviar diretamente pela Sendspeed/Userin

---

## Critérios de aceite:

* A campanha quando chegar no banco deve ser a identificada através do parametro **userin=1** no link da mensagem, ex:[ https://donald.bet.br/sports?**userin=1**](<https://donald.bet.br/sports?userin=1>)
* Criar uma campanha normalmente.
* Detectar o link URL da mensagem através do regexp
* Substitui o **userin=1** por **utm=campaign=<id_campaign>** no link da mensagem.
* Encurta esse novo link substituido e adiciona o link encurtado na mensagem.
* Dispara a campanha com as informações corretas no padrão que o cliente enviou, ex: copy do cliente + link encurtado.

## Histórico de status
- Backlog (backlog): 2026-01-08T18:08:54.630Z → 2026-01-16T15:27:02.435Z
- To-do (unstarted): 2026-01-16T15:27:02.435Z → 2026-01-21T12:37:55.181Z
- In Progress (started): 2026-01-21T12:37:55.181Z → 2026-06-22T17:15:55.590Z
- Released (completed): 2026-06-22T17:15:55.590Z → atual

## Relações
—

## Anexos
—
