# SEND-69 — [LEGADO][SPIKE][MANUTENÇÃO] Remover espelhamento do banco que causa lock e reduzir custo

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | No priority |
| Responsável | peterson.marques@sendspeed.com |
| Time | Sendspeed |
| Projeto | — |
| Labels | — |
| Parent | — |
| Criada | 2025-08-29T14:11:15.398Z por bruno.heidrich@sendspeed.com |
| Iniciada | 2025-09-04T19:37:14.750Z |
| Concluída | 2025-09-25T18:43:49.728Z |
| Arquivada | 2026-04-03T01:20:19.261Z |
| Vencimento | — |
| Branch | hugofernandes/send-69-legadospikemanutencao-remover-espelhamento-do-banco-que |
| URL | https://linear.app/sendspeed/issue/SEND-69/legadospikemanutencao-remover-espelhamento-do-banco-que-causa-lock-e |

## Descrição

**Como** responsável pela infra, 
**quero** retirar o segundo banco de backup na digital que está espelhado os dados 
**para** eliminar os locks e reduzir seu custo.

**Pronto quando**

* O **segundo banco** foi removido/desabilitado com segurança.
* Não ocorrem **locks** de espelhamento por 48h após a mudança.
* Há **antes/depois** simples do custo do banco.
* Armazenar as informações em outro banco, onde conseguimos acesso caso necessário
* Garantir que o banco principal faça seu próprio backup.
* Existe um **passo-a-passo curto** de como voltar (caso necessário).

## Histórico de status
- Backlog (backlog): 2025-08-29T14:11:15.398Z → 2025-08-29T14:27:38.439Z
- To-do (unstarted): 2025-08-29T14:27:38.439Z → 2025-09-04T19:37:14.735Z
- Pull Request (started): 2025-09-04T19:37:14.735Z → 2025-09-25T15:00:57.494Z
- Product Review (started): 2025-09-25T15:00:57.494Z → 2025-09-25T18:43:49.698Z
- Released (completed): 2025-09-25T18:43:49.698Z → atual

## Relações
—

## Anexos
—
