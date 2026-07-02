# SEND-371 — [SPRINT] US-03 — Disparos Externos Criam Jornadas (externalCampaignId -> journeyId )

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | Urgent |
| Responsável | pedro.antunes@sendspeed.com |
| Time | Sendspeed |
| Projeto | — |
| Labels | Jornadas, Implementação, Tech Story |
| Parent | — |
| Criada | 2026-03-09T12:18:50.227Z por pedro.antunes@sendspeed.com |
| Iniciada | 2026-03-11T16:41:16.181Z |
| Concluída | 2026-04-15T22:14:48.308Z |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-371-sprint-us-03-disparos-externos-criam-jornadas |
| URL | https://linear.app/sendspeed/issue/SEND-371/sprint-us-03-disparos-externos-criam-jornadas-externalcampaignid |

## Descrição

## Objetivo

A primeira mensagem de um `externalCampaignId` cria automaticamente uma jornada tipo `external`. Mensagens subsequentes usam cache Redis para agrupar na mesma jornada — unificando analytics e KPIs.

## Contexto

Assim como `campaign` + lista fria já cria jornadas via `CampaignJourneyBridge`, disparos externos devem fazer o mesmo automaticamente.

## Critérios de Aceite

- [ ] Novo campo: `campaignConfig.externalCampaignId` (indexed, unique sparse)
- [ ] `ExternalCampaignResolver.resolveOrCreate()`:
  - Redis hit → retorna journeyId (rápido)
  - Mongo hit → retorna journeyId (popula Redis)
  - Não existe → cria via CampaignJourneyBridge com `journeyType: 'external'`
- [ ] Cache Redis: `ext_campaign:{companyId}:{externalCampaignId}` → journeyId, **TTL: 7 dias**
- [ ] Endpoint: `POST /api/journeys/external/dispatch`
- [ ] Cada recipient enfileirado no Kafka com `source: 'external'`
- [ ] Jornada aparece no Builder com badge "Externa" (já implementado no frontend)
- [ ] Campo `meta` de cada disparo gravado em `JourneyExecution.context.webhookMeta`

## Fluxo

```
Disparo Externo → POST /external/dispatch
  → ExternalCampaignResolver (Redis 7d → Mongo → Create)
  → JourneyExecutionProducer.enqueue(journeyId, recipient)
  → Kafka → Worker → Executor → SendSpeed API
```

## Dependências

* US-02 (Fila Kafka)

## Sprint

**Semana 2**

## Histórico de status
- To-do (unstarted): 2026-03-09T12:18:50.227Z → 2026-03-11T16:41:16.204Z
- In Progress (started): 2026-03-11T16:41:16.204Z → 2026-03-13T16:43:57.730Z
- Pull Request (started): 2026-03-13T16:43:57.730Z → 2026-03-13T18:52:51.449Z
- Product Review (started): 2026-03-13T18:52:51.449Z → 2026-03-25T13:33:27.607Z
- Done (started): 2026-03-25T13:33:27.607Z → 2026-04-15T22:14:48.320Z
- Released (completed): 2026-04-15T22:14:48.320Z → atual

## Relações
—

## Anexos
—
