# SEND-239 — [MELHORIA] Garantir Escalabilidade do Tracker (Nova Socket)

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | Urgent |
| Responsável | Vinicius Carneiro |
| Time | Sendspeed |
| Projeto | — |
| Labels | — |
| Parent | — |
| Criada | 2025-11-10T13:12:19.021Z por bruno.heidrich@sendspeed.com |
| Iniciada | 2025-11-14T13:57:23.463Z |
| Concluída | 2025-12-03T18:54:20.116Z |
| Arquivada | 2026-06-04T22:49:20.441Z |
| Vencimento | — |
| Branch | hugofernandes/send-239-melhoria-garantir-escalabilidade-do-tracker-nova-socket |
| URL | https://linear.app/sendspeed/issue/SEND-239/melhoria-garantir-escalabilidade-do-tracker-nova-socket |

## Descrição

**Como** Head de Produto
**Quero** garantir que o tracker rode de forma estável em sites com **até 10–20x mais volume** do que temos hoje,
**Para** assegurar que o produto suporte novos clientes de alto tráfego sem gargalos ou quedas de performance.

### Critérios de Aceite

* Deve ser realizado um **teste de estresse controlado**, simulando cenários de 5x, 10x e 20x o volume atual.
* O socket deve ser **migrado do Fly.io para uma máquina de alta performance** (DigitalOcean ou equivalente).
* O sistema deve se manter estável (sem travar, cair ou atrasar mensagens).
* Logs e métricas de performance precisam ser registrados para acompanhamento.
* Deve haver um relatório com os resultados e limites de escala identificados.

## Histórico de status
- To-do (unstarted): 2025-11-10T13:12:19.021Z → 2025-11-14T13:57:23.471Z
- In Progress (started): 2025-11-14T13:57:23.471Z → 2025-11-26T12:02:50.441Z
- Pull Request (started): 2025-11-26T12:02:50.441Z → 2025-12-03T17:25:11.203Z
- Product Review (started): 2025-12-03T17:25:11.203Z → 2025-12-03T18:54:19.293Z
- Canceled (canceled): 2025-12-03T18:54:19.293Z → 2025-12-03T18:54:20.164Z
- Released (completed): 2025-12-03T18:54:20.164Z → atual

## Relações
—

## Anexos
—
