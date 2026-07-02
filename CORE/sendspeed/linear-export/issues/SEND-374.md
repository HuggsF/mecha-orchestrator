# SEND-374 — [SPRINT] US-06 — Analytics Unificado + JourneyExecution para Todos os Tipos

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | Urgent |
| Responsável | pedro.antunes@sendspeed.com |
| Time | Sendspeed |
| Projeto | — |
| Labels | User Story, Jornadas, Implementação |
| Parent | — |
| Criada | 2026-03-09T12:18:51.145Z por pedro.antunes@sendspeed.com |
| Iniciada | 2026-03-16T15:38:09.644Z |
| Concluída | 2026-04-15T22:14:57.563Z |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-374-sprint-us-06-analytics-unificado-journeyexecution-para-todos |
| URL | https://linear.app/sendspeed/issue/SEND-374/sprint-us-06-analytics-unificado-journeyexecution-para-todos-os-tipos |

## Descrição

## Objetivo

Garantir que **todas** as execuções de jornada (campaign, external, offsite, webhook) gravam `JourneyExecution` com o campo `meta` do webhook, e que o dashboard de analytics funciona unificado.

## O que já existe

O modelo `JourneyExecution` já grava: `journeyId`, `userId`, `steps[]`, `context`, `metadata`, `status`. Porém:

* `source` enum é `['insite', 'offsite']` — falta `campaign`, `external`, `webhook`
* Não grava `meta` do webhook no `context`
* CampaignJourneyProcessor já grava `source: 'campaign'` mas sem estar no enum

## Critérios de Aceite

- [ ] Expandir `JourneyExecution.source` enum: `['insite','offsite','campaign','external','webhook']`
- [ ] Todas as execuções gravam `JourneyExecution` com steps completos
- [ ] `meta` do webhook gravado em `context.webhookMeta`
- [ ] Contadores incrementados em tempo real: sent, delivered, failed, clicked, converted
- [ ] Dashboard exibe métricas unificadas, independente do tipo
- [ ] Filtro por `journeyType`: Insite, Offsite, Campaign, External
- [ ] KPIs de objetivo (`successMetrics`) funcionam para jornadas `external`

## Sprint

**Semana 3**

## Histórico de status
- To-do (unstarted): 2026-03-09T12:18:51.145Z → 2026-03-16T15:38:09.653Z
- In Progress (started): 2026-03-16T15:38:09.653Z → 2026-03-16T21:31:52.599Z
- Pull Request (started): 2026-03-16T21:31:52.599Z → 2026-03-17T19:03:56.075Z
- Product Review (started): 2026-03-17T19:03:56.075Z → 2026-03-25T13:33:06.422Z
- Done (started): 2026-03-25T13:33:06.422Z → 2026-03-25T18:32:32.973Z
- In Progress (started): 2026-03-25T18:32:32.973Z → 2026-03-26T12:44:22.657Z
- Pull Request (started): 2026-03-26T12:44:22.657Z → 2026-03-26T14:34:53.786Z
- Product Review (started): 2026-03-26T14:34:53.786Z → 2026-03-31T18:25:21.148Z
- Done (started): 2026-03-31T18:25:21.148Z → 2026-04-15T22:14:57.588Z
- Released (completed): 2026-04-15T22:14:57.588Z → atual

## Relações
—

## Anexos
—
