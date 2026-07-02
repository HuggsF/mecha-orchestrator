# SEND-372 — [SPRINT] US-04 — SMS Real na Jornada (SendSpeed API)

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | Urgent |
| Responsável | pedro.antunes@sendspeed.com |
| Time | Sendspeed |
| Projeto | — |
| Labels | User Story, Jornadas, Sendspeed |
| Parent | — |
| Criada | 2026-03-09T12:18:50.563Z por pedro.antunes@sendspeed.com |
| Iniciada | 2026-03-13T19:44:58.965Z |
| Concluída | 2026-04-15T22:15:02.075Z |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-372-sprint-us-04-sms-real-na-jornada-sendspeed-api |
| URL | https://linear.app/sendspeed/issue/SEND-372/sprint-us-04-sms-real-na-jornada-sendspeed-api |

## Descrição

# US-4: SMS Real em Todas as Jornadas (via Kafka)

## Objetivo

Remover a simulação de SMS e chamar a API real da SendSpeed em qualquer tipo de jornada (campaign, offsite, external, insite, webhook), passando obrigatoriamente pelo Kafka.

## Contexto

O `SendSmsExecutor` funciona no `CampaignJourneyProcessor`, mas o `journeyOffsiteProcessor` apenas simulava (tinha um `// TODO` no código). Precisamos que funcione em todos os contextos, com envio assíncrono via Kafka.

## Arquitetura

```
┌─────────────────────────────────────────────────────────────────┐
│ platform-backend │
│ │
│ ┌──────────────┐ ┌──────────────┐ ┌──────────────────────┐ │
│ │ Campaign │ │ OffSite │ │ InSite / Webhook │ │
│ │ Processor │ │ Processor │ │ External Trigger │ │
│ └──────┬───────┘ └──────┬───────┘ └──────────┬───────────┘ │
│ │ │ │ │
│ ▼ ▼ ▼ │
│ SendSmsExecutor executeSendSms() /journeys/offsite-action
│ │ │ │ │
│ └─────────────────┴──────────────────────┘ │
│ │ │
│ ▼ │
│ POST /api/sms/:companyId/send │
└───────────────────────────┬─────────────────────────────────────┘
 │
 ▼
┌───────────────────────────────────────────────────────────────────┐
│ userin-integrations │
│ │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ sms.routes.ts (PRODUCER) │ │
│ │ - Valida payload (phone, message) │ │
│ │ - Resolve credencial │ │
│ │ - Enfileira no Kafka (obrigatório, sem fallback) │ │
│ └─────────────────────────┬───────────────────────────────────┘ │
│ │ │
│ ▼ │
│ Kafka Topic: userin_send_sms │
│ │
└───────────────────────────────────────────────────────────────────┘
 │
 ▼
┌───────────────────────────────────────────────────────────────────┐
│ SendSpeed (CONSUMER) │
│ │
│ - Consome mensagens do tópico userin_send_sms │
│ - Processa e envia SMS via API real │
│ - Implementação é responsabilidade da equipe SendSpeed │
│ │
└───────────────────────────────────────────────────────────────────┘
```

## Critérios de Aceite

### Executores (platform-backend)

| Critério | Status | Implementação |
| -- | -- | -- |
| `SendSmsExecutor` chama API real | ✅ | `POST /api/sms/:companyId/send` |
| `journeyOffsiteProcessor.executeSendSms()` sem simulação | ✅ | Removido `// TODO`, chama API real |
| Funciona em todos os contextos | ✅ | Campaign, OffSite, InSite, Webhook, External |

### Kafka (userin-integrations → Producer)

| Critério | Status | Implementação |
| -- | -- | -- |
| SMS enfileirado no Kafka | ✅ | Tópico `userin_send_sms` |
| Kafka obrigatório (sem fallback HTTP) | ✅ | Retorna HTTP 503 se Kafka indisponível |
| Apenas Producer | ✅ | `sms-producer.service.ts` enfileira mensagens |

### Kafka (SendSpeed → Consumer)

| Critério | Status | Implementação |
| -- | -- | -- |
| Consumer do tópico | ⏳ | Responsabilidade da equipe SendSpeed |
| Envio real do SMS | ⏳ | SendSpeed consome e processa |

### Resolução de Dados

| Critério | Status | Implementação |
| -- | -- | -- |
| Credencial auto-resolvida by scope `send_sms` | ✅ | `GET /api/credentials/:companyId/by-scope/send_sms` |
| Telefone resolvido na ordem correta | ✅ | `meta.phone → profile.phone → profile.contact.phone → CRM Contact` |
| Variáveis interpoladas no corpo | ✅ | `replaceVariables()` / `liquidResolver` suporta `{nome}`, `{valor_deposito}`, campos do meta |
| Usar modelo `user_profiles` + contato | ✅ | `profile.contact`, `Contact` model como fallback |

### Tratamento de Erros

| Critério | Status | Implementação |
| -- | -- | -- |
| Resultado gravado em `JourneyExecution.steps[]` | ✅ | `execution.steps.push(step)` com status e resultado |
| Retry automático em falha temporária (timeout, 5xx) | ✅ | `MAX_RETRIES = 2` com backoff exponencial |
| `phone_not_found` sem disparo de API | ✅ | `exitReason: 'phone_not_found'` / `NO_PHONE_REGISTERED_USER` |

### Rastreamento de Origem

| Critério | Status | Implementação |
| -- | -- | -- |
| Source da jornada identificado | ✅ | `source: 'journey'` no payload |
| JourneyId passado | ✅ | `journeyId` no payload |
| ExecutionId passado | ✅ | `executionId` no payload |
| ExternalId do usuário passado | ✅ | `externalId` no payload |

## Arquivos Modificados

### platform-backend

* `backend/src/journey-builder/engine/nodes/actions/SendSmsExecutor.js`
* Chama API real com retry
* Passa contexto de origem (`source`, `journeyId`, `executionId`, `externalId`)
* `backend/src/journey-builder/services/journeyOffsiteProcessor.js`
* `executeSendSms()` chama API real (removida simulação)
* Passa contexto de origem

### userin-integrations

* `src/routes/sms.routes.ts`
* Kafka obrigatório (removido fallback HTTP)
* Retorna HTTP 503 se Kafka indisponível
* `src/services/sms-producer.service.ts`
* Producer para enfileirar SMS no Kafka
* `src/config/kafka.ts`
* Configuração do Kafka (brokers, auth, tópico)

## Payload do Kafka (tópico: userin_send_sms)

```json
{
"user_phone": "5511999999999",
"txt": "Olá João! Seu depósito de R$100 foi confirmado."
}
```

**Campos:**

* `user_phone` - Telefone do destinatário (sem o +, apenas números)
* `txt` - Texto do SMS a ser enviado

**Key:** telefone sem o `+` (ex: `5511999999999`)

## Configuração

### Variáveis de Ambiente (userin-integrations)

```bash
KAFKA_ENABLED=true
KAFKA_BROKERS=pkc-921jm.us-east-2.aws.confluent.cloud:9092
KAFKA_CLIENT_ID=userin-integrations
KAFKA_USERNAME=<api-key>
KAFKA_PASSWORD=<api-secret>
```

### Confluent Cloud

* **Tópico:** `userin_send_sms` (6 partições)
* **ACL Producer:** API Key com permissão WRITE no tópico
* **ACL Consumer:** SendSpeed configura próprio consumer group

## Testes

- [ ] Enviar SMS via jornada Campaign
- [ ] Enviar SMS via jornada OffSite
- [ ] Enviar SMS via jornada InSite
- [ ] Enviar SMS via Webhook externo
- [ ] Enviar SMS via disparo externo (External Trigger)
- [ ] Verificar que SMS sem telefone retorna `phone_not_found`
- [ ] Verificar retry em timeout/5xx
- [ ] Verificar que Kafka indisponível retorna HTTP 503
- [ ] Verificar mensagem no tópico Kafka com payload correto

## Responsabilidades

| Equipe | Responsabilidade |
| -- | -- |
| **UserIn** | Producer - enfileira SMS no Kafka |
| **SendSpeed** | Consumer - consome do Kafka e envia SMS |

## Sprint

**Semana 1** - Implementação do Producer (UserIn)

## Histórico de status
- To-do (unstarted): 2026-03-09T12:18:50.563Z → 2026-03-13T19:44:58.972Z
- In Progress (started): 2026-03-13T19:44:58.972Z → 2026-03-18T18:54:54.906Z
- Pull Request (started): 2026-03-18T18:54:54.906Z → 2026-03-19T20:37:22.715Z
- Product Review (started): 2026-03-19T20:37:22.715Z → 2026-03-25T13:32:55.611Z
- Done (started): 2026-03-25T13:32:55.611Z → 2026-04-15T22:15:02.099Z
- Released (completed): 2026-04-15T22:15:02.099Z → atual

## Relações
—

## Anexos
—
