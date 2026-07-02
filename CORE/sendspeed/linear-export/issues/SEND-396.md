# SEND-396 — Arquitetura Multi-Queue Kafka — 4 filas especializadas por padrão de tráfego

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | Urgent |
| Responsável | pedro.antunes@sendspeed.com |
| Time | Sendspeed |
| Projeto | — |
| Labels | Tech Story |
| Parent | SEND-369 |
| Criada | 2026-03-16T15:12:48.336Z por pedro.iegler@sendspeed.com |
| Iniciada | 2026-03-16T15:13:24.286Z |
| Concluída | 2026-04-15T22:14:57.134Z |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-396-arquitetura-multi-queue-kafka-4-filas-especializadas-por |
| URL | https://linear.app/sendspeed/issue/SEND-396/arquitetura-multi-queue-kafka-4-filas-especializadas-por-padrao-de |

## Descrição

## Resumo

Separa o processamento Kafka em **4 filas independentes** para evitar gargalo cruzado entre fluxos com volumes e prioridades diferentes.

---

## Filas implementadas

| Fila (tópico) | Propósito | Consumer Group |
| -- | -- | -- |
| `userin_journey_execute` | Webhook externo (US-01) + Disparo externo (US-03) | `platform-backend-journey-exec` |
| `userin_offsite_evaluate` | Segment-engine classifica user → avalia quais jornadas offsite se aplicam | `platform-backend-offsite-eval` |
| `userin_offsite_execute` | Executa jornadas offsite qualificadas pelo evaluate | `platform-backend-offsite-exec` |
| `userin_campaign_execute` | Campanhas em massa disparadas pelo dashboard | `platform-backend-campaign-exec` |

Cada fila possui seu respectivo **tópico DLQ** (`_dlq`) com retry 3x e backoff.

---

## Fluxo

### Webhook externo / Disparo externo (US-01 + US-03)

```
POST /offsite/trigger ou /external/dispatch
  → Producer enfileira em userin_journey_execute
  → JourneyExecWorker consome
  → processJourneyExecution() executa a jornada
  → JourneyExecution salvo no MongoDB
```

### Offsite (segment-engine → evaluate → execute)

```
Segment-engine classifica user (compileProfile)
  → offsiteEvaluateProducer enfileira em userin_offsite_evaluate
  → OffsiteEvalWorker consome
  → processUser(evaluateOnly: true) avalia TODAS as jornadas offsite ativas
  → Para cada jornada qualificada:
      → offsiteExecuteProducer enfileira em userin_offsite_execute
      → OffsiteExecWorker consome
      → processJourneyExecution() executa a jornada específica
      → JourneyExecution salvo no MongoDB
```

### Campanha (dashboard)

```
Dashboard dispara campanha com audiência/lista
  → campaignExecuteProducer enfileira em userin_campaign_execute
  → CampaignExecWorker consome
  → processJourneyExecution() executa a jornada
  → JourneyExecution salvo no MongoDB
```

---

## Alterações — platform-backend

### Novos arquivos (6)

| Arquivo | Responsabilidade |
| -- | -- |
| `offsiteEvaluateProducer.js` | API produz para `userin_offsite_evaluate` (rotas `/offsite/trigger` e `/trigger-batch`) |
| `offsiteExecuteProducer.js` | EvaluateWorker produz para `userin_offsite_execute` após qualificar jornadas |
| `offsiteExecuteWorker.js` | Consome `userin_offsite_execute` e executa jornada offsite específica |
| `offsiteEvaluateWorker.js` | Consome `userin_offsite_evaluate` e avalia jornadas offsite para o user |
| `campaignExecuteProducer.js` | Produz para `userin_campaign_execute` (campanhas e audiência) |
| `campaignExecuteWorker.js` | Consome `userin_campaign_execute` e executa jornada de campanha |

### Arquivos modificados (6)

| Arquivo | Mudança |
| -- | -- |
| `journeyOffsiteProcessor.js` | `processUser()` aceita `{ evaluateOnly: true }` — enfileira em `userin_offsite_execute` em vez de executar inline. `_resolveAndDispatchAudience` roteia: `source === 'campaign'` → `campaignExecuteProducer`, resto → `journeyExecutionProducer` |
| `journeyRoutes.js` | `/offsite/trigger` e `/trigger-batch` usam `offsiteEvaluateProducer`. `/external/dispatch` usa `journeyExecutionProducer` |
| `CampaignJourneyProcessor.js` | Usa `campaignExecuteProducer` para enfileirar campanhas |
| `config.js` | Novos tópicos: `OFFSITE_EVALUATE`, `OFFSITE_EXECUTE`, `CAMPAIGN_EXECUTE` e seus DLQs |
| `workers-entry.js` | Registra todos os novos producers e workers no lifecycle |
| `index.js` | Conecta `offsiteEvaluateProducer` na API + suporte completo `WORKERS_IN_SERVER` |

---

## Alterações — segment-engine

### Novo arquivo (1)

| Arquivo | Responsabilidade |
| -- | -- |
| `offsiteEvaluateProducer.ts` | Producer dedicado com credenciais separadas (`KAFKA_OFFSITE_USERNAME` / `KAFKA_OFFSITE_PASSWORD`) para produzir em `userin_offsite_evaluate` |

### Arquivos modificados (4)

| Arquivo | Mudança |
| -- | -- |
| `consumer.ts` | Após `compileProfile`, produz para `userin_offsite_evaluate` (fire-and-forget) |
| `bootstrap.ts` | Connect/disconnect do `offsiteEvaluateProducer` no lifecycle |
| `config.ts` | Tópico `OFFSITE_EVALUATE` adicionado |
| `index.ts` | Barrel export do novo producer |

---

## Confluent Cloud

* **8 novos tópicos** criados (4 principais + 4 DLQ):
  * `userin_offsite_evaluate` / `userin_offsite_evaluate_dlq`
  * `userin_offsite_execute` / `userin_offsite_execute_dlq`
  * `userin_campaign_execute` / `userin_campaign_execute_dlq`
  * `userin_journey_execute_dlq` (já existia `userin_journey_execute`)
* **ACLs** configuradas para consumer groups `platform-backend-*` (PREFIXED) — READ e DESCRIBE

---

## Testes

**168 testes — 168 passaram (0 falhas)**

| Categoria | Qtd | Descrição |
| -- | -- | -- |
| Producer Connectivity | 27 | Conexão, envio single/batch/stress para os 4 producers |
| Payload Validation | 18 | Serialização válida, payloads inválidos → DLQ, JSON quebrado |
| Processor Logic | 95 | Frequência (always/once/day/week/custom/cooldown), condições (AND/OR/nested, 20+ operadores PT/EN), triggers (webhook/event/ruleMatch/schedule/manual), execução de nós, resolução de campos, variáveis, audiência |
| Worker Integration E2E | 23 | Produce → Kafka real (Confluent Cloud) → Worker consome → MongoDB verifica JourneyExecution. Inclui: single, batch, DLQ, concurrent, cross-queue isolation, stress 50 msgs |
| Producer State | 5 | Disconnect/reconnect dos 4 producers + enqueue em producer desconectado |

## Histórico de status
- To-do (unstarted): 2026-03-16T15:12:48.336Z → 2026-03-16T15:13:24.297Z
- Pull Request (started): 2026-03-16T15:13:24.297Z → 2026-03-16T18:57:18.289Z
- Product Review (started): 2026-03-16T18:57:18.289Z → 2026-03-25T13:33:22.012Z
- Done (started): 2026-03-25T13:33:22.012Z → 2026-04-15T22:14:57.246Z
- Released (completed): 2026-04-15T22:14:57.246Z → atual

## Relações
—

## Anexos
—
