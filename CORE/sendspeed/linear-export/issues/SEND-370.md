# SEND-370 — [SPRINT] US-01 — Webhook Externo por Jornada (com campo meta)

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | Urgent |
| Responsável | pedro.antunes@sendspeed.com |
| Time | Sendspeed |
| Projeto | — |
| Labels | Jornadas, Implementação, Tech Story |
| Parent | — |
| Criada | 2026-03-09T12:18:49.926Z por pedro.antunes@sendspeed.com |
| Iniciada | 2026-03-09T16:45:05.103Z |
| Concluída | 2026-04-15T22:14:54.773Z |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-370-sprint-us-01-webhook-externo-por-jornada-com-campo-meta |
| URL | https://linear.app/sendspeed/issue/SEND-370/sprint-us-01-webhook-externo-por-jornada-com-campo-meta |

## Descrição

## Objetivo

Cada jornada ativa gera uma **URL de webhook única**. Sistemas externos (CRM, iGaming, ad servers) chamam essa URL para triggar a jornada, passando um campo `meta` livre com qualquer dado.

## Critérios de Aceite

- [ ] Rota: `POST /api/journeys/webhook/{journeyId}/trigger`
- [ ] Aceita payload com `userId`, `phone` e campo `meta` livre (qualquer JSON)
- [ ] O `meta` é gravado em `JourneyExecution.context.webhookMeta`
- [ ] Não executa síncrono — publica na fila Kafka (**US-02**)
- [ ] Suporta batch: `recipients: [{ userId, phone, meta }]`
- [ ] Autenticação via `x-api-secret` ou JWT
- [ ] ~~Rate limit: 1000 req/min por jornada (Redis sliding window)~~
- [ ] URL do webhook aparece no Journey Builder (Header) para copiar
- [ ] Ao ativar jornada, gera URL e salva em `campaignConfig.webhookUrl`
- [ ] Ao pausar/arquivar, retorna 410 Gone
- [ ] Só a empresa pode chamar a jornada dela
- [ ] Toda chamada deve ter no minimo o externalId

## Payload Exemplo

```json
{
  "externalId": "user_123",
  "phone": "5521999999999",
  "meta": {
    "campaignName": "Promo Aviator",
    "source": "crm_hubspot",
    "depositAmount": 500,
    "tags": ["vip", "high_roller"],
    "qualquer_campo": "qualquer_valor"
  }
}
```

## Dependências

* US-02 (Fila Kafka)

## Sprint

**Semana 1**

# **Para ajudar:**

No modelo JourneyExecution em src/journey-builder/models/JourneyExecution.js. Cada vez que um usuário passa por uma jornada, é criado um documento com:

```
const journeyExecutionSchema = new mongoose.Schema({
  journeyId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Journey',
    required: true,
    index: true,
  },
  userId: { type: String, index: true },
  visitorId: { type: String, index: true },
  sessionId: String,
  externalId: { type: String, index: true },
  companyId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Company',
    required: true,
    index: true,
  },
  source: {
    type: String,
    enum: ['insite', 'offsite'],  // ← precisa expandir para 'campaign', 'external', 'webhook'
    default: 'offsite',
    index: true,
  },
  status: {
    type: String,
    enum: ['active', 'completed', 'failed', 'exited', 'paused', 'waiting_event', 'condition_exit'],
    default: 'active',
  },
  triggerId: String,
  triggerType: String,
  journeyVersion: String,
  lastNodeId: String,
  currentNodeId: String,
  steps: [stepExecutionSchema],  // cada nó executado com status, result, durationMs
  context: {
    type: mongoose.Schema.Types.Mixed,  // ← aqui entra o webhookMeta
    default: {},
  },
  metadata: {
    pageUrl: String,
    referrer: String,
    userAgent: String,
    device: String,
    browser: String,
    os: String,
  },
  startedAt: { type: Date, default: Date.now },
  completedAt: Date,
  durationMs: Number,
  exitReason: String,
  // ...
});
```

Cada **step** (nó executado) grava:

```
const stepExecutionSchema = new mongoose.Schema({
  nodeId: { type: String, required: true },
  nodeType: { type: String, required: true },
  status: {
    type: String,
    enum: ['pending', 'executing', 'completed', 'failed', 'skipped', 'condition_exit'],
    default: 'pending',
  },
  startedAt: Date,
  completedAt: Date,
  durationMs: Number,
  result: mongoose.Schema.Types.Mixed,
  error: String,
  nextNodeId: String,
}, { _id: false });
```

**Quem grava hoje:** Apenas o CampaignJourneyProcessor grava consistentemente (com source: 'campaign'). O journeyOffsiteProcessor grava em alguns caminhos mas não em todos. Na sprint (US-02/US-06), o JourneyExecutionWorker vai ser o ponto único de gravação para tudo que não é insite.

## Histórico de status
- To-do (unstarted): 2026-03-09T12:18:49.926Z → 2026-03-09T16:45:05.117Z
- In Progress (started): 2026-03-09T16:45:05.117Z → 2026-03-12T16:03:05.533Z
- Pull Request (started): 2026-03-12T16:03:05.533Z → 2026-03-13T18:52:48.520Z
- Product Review (started): 2026-03-13T18:52:48.520Z → 2026-03-25T13:33:15.367Z
- Done (started): 2026-03-25T13:33:15.367Z → 2026-04-15T22:14:54.785Z
- Released (completed): 2026-04-15T22:14:54.785Z → atual

## Relações
—

## Anexos
—
