# SEND-369 — [SPRINT] US-02 — Fila Kafka Unificada para Execução de Jornadas

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | Urgent |
| Responsável | pedro.antunes@sendspeed.com |
| Time | Sendspeed |
| Projeto | — |
| Labels | Jornadas, Implementação, Tech Story |
| Parent | — |
| Criada | 2026-03-09T12:18:49.610Z por pedro.antunes@sendspeed.com |
| Iniciada | 2026-03-10T12:17:29.798Z |
| Concluída | 2026-04-15T22:14:52.333Z |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-369-sprint-us-02-fila-kafka-unificada-para-execucao-de-jornadas |
| URL | https://linear.app/sendspeed/issue/SEND-369/sprint-us-02-fila-kafka-unificada-para-execucao-de-jornadas |

## Descrição

## Objetivo

Processar **todas** as execuções de jornadas server-side (`campaign`, `offsite`, `external`) por uma fila Kafka unificada — é a **fundação** para todas as outras histórias.

## Contexto

Hoje jornadas offsite executam de forma **síncrona via HTTP** — sem fila, sem escala. Campanhas usam Kafka separado (`userin_campaign_send`). Precisamos unificar tudo em `userin_journey_execute`.

**Tipos de jornada e fila:**

| Tipo | journeyType | Entra na fila? |
| -- | -- | -- |
| InSite | insite | Não (executa no browser) |
| OffSite | offsite | **Sim** |
| Campanha | campaign | **Sim** |
| Externa | external | **Sim** |
|  |  |  |

## Critérios de Aceite

- [ ] Novo tópico Kafka: `userin_journey_execute`
- [ ] `JourneyExecutionProducer` publica: `{ journeyId, companyId, userId, phone, event, meta, source }`
- [ ] `JourneyExecutionWorker` consome em batch, concorrência configurável (default: 20)
- [ ] Worker executa nodes via `createExecutor()` e grava `JourneyExecution`
- [ ] Campo `meta` do webhook salvo em `JourneyExecution.context.webhookMeta`
- [ ] DLQ: `userin_journey_execute_dlq` (retry 3x com backoff)
- [ ] Endpoints migrados para usar fila:
  - `POST /offsite/trigger` → enqueue
  - `POST /webhook/:id/trigger` → enqueue
  - `CampaignJourneyProcessor` → enqueue cada recipient
- [ ] Cache Redis para jornadas ativas (TTL: **1h**, invalidação ativa em update/delete)
- [ ] Flag `JOURNEY_EXEC_SYNC=true` para fallback síncrono em dev
- [ ] Expandir `JourneyExecution.source` enum: `['insite','offsite','campaign','external','webhook']`

## Sprint

**Semana 1** — Fundação para todas as outras histórias

## Histórico de status
- To-do (unstarted): 2026-03-09T12:18:49.610Z → 2026-03-10T12:17:29.833Z
- In Progress (started): 2026-03-10T12:17:29.833Z → 2026-03-12T16:03:11.291Z
- Pull Request (started): 2026-03-12T16:03:11.291Z → 2026-03-13T18:52:49.419Z
- Product Review (started): 2026-03-13T18:52:49.419Z → 2026-03-16T12:28:10.711Z
- Pull Request (started): 2026-03-16T12:28:10.711Z → 2026-03-16T18:57:15.357Z
- Product Review (started): 2026-03-16T18:57:15.357Z → 2026-03-25T13:33:18.862Z
- Done (started): 2026-03-25T13:33:18.862Z → 2026-04-15T22:14:52.344Z
- Released (completed): 2026-04-15T22:14:52.344Z → atual

## Relações
—

## Anexos
—
