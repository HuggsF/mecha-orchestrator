# SEND-38 — Análise de desempenho individual {Card}

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | High |
| Responsável | andrei.garcia@externo.sendspeed.com |
| Time | Sendspeed |
| Projeto | — |
| Labels | — |
| Parent | — |
| Criada | 2025-07-08T18:07:09.178Z por bruno.heidrich@sendspeed.com |
| Iniciada | 2025-07-21T12:26:16.363Z |
| Concluída | 2025-08-11T13:53:42.875Z |
| Arquivada | 2026-02-15T02:17:35.423Z |
| Vencimento | — |
| Branch | hugofernandes/send-38-analise-de-desempenho-individual-card |
| URL | https://linear.app/sendspeed/issue/SEND-38/analise-de-desempenho-individual-card |

## Descrição

**Como** desenvolvedor,
**Quero** que cada card disparado tenha um identificador único e um campo de tracking no JSON,
**Para que** eu possa medir individualmente o desempenho de cada card em termos de visualização, clique e conversão.

**Critérios de Aceitação:**

*  Cada card deve conter um `card_id` único no JSON enviado.
*  O JSON de evento deve incluir os campos: `card_id`, `action_type` (view, click, convert), `timestamp`, `session_id`, `user_id`.
*  Os dados devem ser enviados para a fila de eventos ou armazenados em banco com consistência.
*  Deve ser possível, via logs ou dashboard, filtrar performance por `card_id`

## Histórico de status

- Backlog (backlog): 2025-07-08T18:07:09.178Z → 2025-07-10T12:13:28.690Z
- To-do (unstarted): 2025-07-10T12:13:28.690Z → 2025-07-21T12:26:16.346Z
- Pull Request (started): 2025-07-21T12:26:16.346Z → 2025-07-31T14:40:00.467Z
- Product Review (started): 2025-07-31T14:40:00.467Z → 2025-08-11T13:53:42.756Z
- Released (completed): 2025-08-11T13:53:42.756Z → atual

## Relações

—

## Anexos

—
