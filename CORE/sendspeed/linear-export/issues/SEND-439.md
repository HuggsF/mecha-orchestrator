# SEND-439 — [INVESTIGATE] SEND-435: Analisar journeyOffsiteProcessor vs InSite delay engine

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | Urgent |
| Responsável | — |
| Time | Sendspeed |
| Projeto | — |
| Labels | Jornadas |
| Parent | SEND-435 |
| Criada | 2026-03-31T23:25:50.837Z por Hugo Fernandes |
| Iniciada | 2026-03-31T23:25:50.904Z |
| Concluída | 2026-04-15T22:14:58.626Z |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-439-investigate-send-435-analisar-journeyoffsiteprocessor-vs |
| URL | https://linear.app/sendspeed/issue/SEND-439/investigate-send-435-analisar-journeyoffsiteprocessor-vs-insite-delay |

## Descrição

## Objetivo

Investigar a causa raiz do bug SEND-435: no `flow.delay` nao pausa em jornadas offsite.

## Contexto

**Pipeline Offsite (RAG, confidence 0.94):**

```
POST /api/external/inbound
  -> JourneyCacheService.getById(cid) Redis(1h) -> MongoDB
  -> journeyExecutionProducer -> Kafka userin_journey_execute
  -> JourneyExecutionWorker (concurrency: 20)
  -> journeyOffsiteProcessor -> execute journey nodes
```

## Acceptance Criteria

- [ ] Identificar como `journeyOffsiteProcessor.js` processa o no `flow.delay`
- [ ] Comparar com o engine InSite (como ele trata delays)
- [ ] Documentar a diferenca entre os dois mecanismos
- [ ] Propor solucao tecnica (Redis sorted set? Bull queue? Kafka delayed?)
- [ ] Postar findings como comentario nesta issue

## Histórico de status
- In Progress (started): 2026-03-31T23:25:50.837Z → 2026-03-31T23:32:10.599Z
- Done (started): 2026-03-31T23:32:10.599Z → 2026-04-15T22:14:58.639Z
- Released (completed): 2026-04-15T22:14:58.639Z → atual

## Relações
—

## Anexos
—
