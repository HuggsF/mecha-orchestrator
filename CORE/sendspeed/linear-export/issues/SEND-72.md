# SEND-72 — [COMPANION][VETOR] - Ensino vetorial v1.1: Selecionar dados da diário

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | No priority |
| Responsável | Hugo Fernandes |
| Time | Sendspeed |
| Projeto | — |
| Labels | — |
| Parent | — |
| Criada | 2025-08-29T14:18:02.995Z por bruno.heidrich@sendspeed.com |
| Iniciada | 2025-09-04T19:37:20.077Z |
| Concluída | 2025-09-25T12:56:26.336Z |
| Arquivada | 2026-04-03T01:20:18.825Z |
| Vencimento | — |
| Branch | hugofernandes/send-72-companionvetor-ensino-vetorial-v11-selecionar-dados-da |
| URL | https://linear.app/sendspeed/issue/SEND-72/companionvetor-ensino-vetorial-v11-selecionar-dados-da-diario |

## Descrição

**Como** Head de Produto, 
**quero** gerar um imput de **"vetor diário"** a partir dos dados reais (páginas, eventos e conversões) 
**para** que o Companion aprenda com o que mais funcionou.

**Pronto quando**

* Criamos uma rotina de transmissão dos imputs diários para o vetor.
* Vejo um **resumo** (volume, principais páginas/eventos, conversões ligadas, %conversao, % nao converteu, etc).
* Consigo salvar o conjunto **com versão** (ex.: "2025-S35").
* Se um dado já foi vetorizado, ele não vai revetorizar esse dado
* Sempre no mesmo estilo de vetorização

---

* [OK] Criamos uma rotina de transmissão dos inputs diários para o vetor
  * Scheduler diário + execução manual (CLI/endpoint) orquestrando vetorização e resumo.
* [OK] Vejo um resumo (volume, principais páginas/eventos, conversões ligadas, % conversão, % não converteu)
  * Endpoint de daily summary com KPIs e listas topo; snapshot JSON/HTML.
* [OK] Consigo salvar o conjunto com versão (ex.: "2025-S35")
  * Versão diária vectors_daily:YYYY-MM-DD com alias semanal vectors_week:YYYY-SWW.
* [OK] Se um dado já foi vetorizado, ele não vai revetorizar esse dado
  * Idempotência por vetor (consulta no índice e conta skipped).
* [OK] Sempre no mesmo estilo de vetorização
  * Pipeline única (sanitize → journey text → embed → upsert) com limites centralizados em env.

### **Vetor diário (input real → versão diária)**

* Inputs
  * Mongo `events`: { companyId, sessionId, type, url, title, createdAt, ... }
  * Mongo `visitors_contacts`: { sessionId, companyId, visitorId, localstorageId, name, email, createdAt }
  * Query params: `companyId`, `dateFrom`, `dateTo`
  * Coleções: events (base), visitors_contacts (para marcar conversões).
* Processamento
  * Seleciona sessões do período (America/Sao_Paulo), separa convertidas vs não-convertidas.
  * Para cada sessão (até N): buscar últimos 60 eventos, `sanitizeEvent`, gerar `toJourneyText`, `embedText` (OpenAI), upsert Pinecone `id="sess:{sessionId}"` com metadados planos.
  * **Pipeline (Mongo)**
    * 1) events → $match por companyId e createdAt no período.
    * 2) events → contagens rápidas:
      * Top URLs: $group por url, $count, $sort, $limit.
      * Top tipos de evento: $group por type, $count, $sort, $limit.
    * 3) sessions no período:
      * $group por sessionId para obter eventCount, firstUrl, lastUrl, firstEventAt, lastEventAt.
    * 4) lookup em visitors_contacts por sessionId para marcar converted=true/false.
    * 5) Agregações finais:
      * totalSessions, convertedSessions, nonConvertedSessions, conversionRate = converted/total.
      * Estatísticas: eventCount média/mediana, duração média (last-first).
      * "Conversões ligadas": total e por conversionCode (se aplicável).
    * Agrega KPIs do dia.
      * **volume**: totalSessions, eventsInPeriod.
      * **% conversão** e **% não converteu**: conversionRate, 1 - conversionRate.
      * **principais páginas**: topPages (por url, contagem).
      * **principais eventos**: topEventTypes (por type, contagem).
      * **conversões ligadas**: conversionsByType (opcional por conversionCode), convertedSessions.
      * Extras: medianEventCountPerSession, avgSessionDurationMs, topEntryPages (firstUrl), topExitPages (lastUrl).
  * Persiste versão: `vector_versions` { companyId, versionId: `vectors_daily:{YYYY-MM-DD}`, type: 'daily', dateRange, createdAt, stats }.
* 
  * Em vector_versions: stats armazena o snapshot do dia (facilita histórico/semana 2025-S35).
* Outputs
  * Pinecone upserts (convertidas: converted=true; não: converted=false).
  * Mongo `vector_versions` documento para o dia e alias semanal opcional `vectors_week:{YYYY}-S{WW}`.
  * Endpoint/relatório resumo diário: { totalSessions, %converted, %nonConverted, topPages, topEvents, precisionAtK? }.

---

## **Endpoint sugerido**

GET /api/vectors/daily-summary?companyId=...&dateFrom=YYYY-MM-DD&dateTo=YYYY-MM-DD

* Calcula a partir do events e visitors_contacts e também persiste em vector_versions.stats.

Resposta sugerida:

```
{
  "success": true,
  "filters": { "companyId": "685ee1...", "dateFrom": "2025-09-01", "dateTo": "2025-09-01" },
  "kpis": {
    "totalSessions": 842,
    "convertedSessions": 123,
    "nonConvertedSessions": 719,
    "conversionRate": 0.146,
    "eventsInPeriod": 18234,
    "medianEventCountPerSession": 9,
    "avgSessionDurationMs": 174000
  },
  "topPages": [
    { "url": "/home", "count": 512 },
    { "url": "/produto/123", "count": 231 },
    { "url": "/checkout", "count": 158 }
  ],
  "topEventTypes": [
    { "type": "page_view", "count": 8421 },
    { "type": "click", "count": 6502 },
    { "type": "scroll", "count": 2893 }
  ],
  "conversions": {
    "byType": [
      { "conversionCode": "track_conversion_CHECKOUT", "count": 88 },
      { "conversionCode": "track_conversion_LEAD", "count": 35 }
    ]
  },
  "entryPages": [
    { "url": "/home", "count": 480 },
    { "url": "/search", "count": 120 }
  ],
  "exitPages": [
    { "url": "/checkout", "count": 96 },
    { "url": "/produto/123", "count": 90 }
  ],
  "generatedAt": "2025-09-01T03:40:00-03:00"
}
```

---

# Collection - vector_versions

### Objeto diário:

```
{
  "_id": "674f3c2a9a1b2c0012abcd34",
  "companyId": "685ee1397c33dcc03812040d",
  "versionId": "vectors_daily:2025-09-01",
  "type": "daily",
  "dateRange": {
    "from": "2025-09-01T00:00:00-03:00",
    "to": "2025-09-01T23:59:59.999-03:00",
    "timezone": "America/Sao_Paulo"
  },
  "status": "success",
  "source": "schedule",
  "createdBy": "system",
  "createdAt": "2025-09-02T03:40:12.123-03:00",
  "counts": {
    "upsertedConverted": 88,
    "upsertedNonConverted": 210,
    "skipped": 5,
    "totalVectors": 298
  },
  "stats": {
    "kpis": {
      "totalSessions": 842,
      "convertedSessions": 123,
      "nonConvertedSessions": 719,
      "conversionRate": 0.146,
      "eventsInPeriod": 18234,
      "medianEventCountPerSession": 9,
      "avgSessionDurationMs": 174000
    },
    "topPages": [
      { "url": "/home", "count": 512 },
      { "url": "/produto/123", "count": 231 },
      { "url": "/checkout", "count": 158 }
    ],
    "topEventTypes": [
      { "type": "page_view", "count": 8421 },
      { "type": "click", "count": 6502 },
      { "type": "scroll", "count": 2893 }
    ],
    "conversions": {
      "byType": [
        { "conversionCode": "track_conversion_CHECKOUT", "count": 88 },
        { "conversionCode": "track_conversion_LEAD", "count": 35 }
      ]
    },
    "entryPages": [
      { "url": "/home", "count": 480 },
      { "url": "/search", "count": 120 }
    ],
    "exitPages": [
      { "url": "/checkout", "count": 96 },
      { "url": "/produto/123", "count": 90 }
    ]
  },
  "aliases": ["vectors_week:2025-S35"],
  "reportUrl": "/reports/vector-stats-2025-09-01.json",
  "pineconeIndex": "analytics-sessions"
}
```

## Objeto semanal:

```
{
  "_id": "674f3c2a9a1b2c0012abcd35",
  "companyId": "685ee1397c33dcc03812040d",
  "versionId": "vectors_week:2025-S35",
  "type": "weekly",
  "dateRange": {
    "from": "2025-08-25T00:00:00-03:00",
    "to": "2025-08-31T23:59:59.999-03:00",
    "timezone": "America/Sao_Paulo"
  },
  "status": "success",
  "createdBy": "system",
  "createdAt": "2025-09-01T03:45:00-03:00",
  "aggregatesOf": [
    "vectors_daily:2025-08-25",
    "vectors_daily:2025-08-26",
    "vectors_daily:2025-08-27",
    "vectors_daily:2025-08-28",
    "vectors_daily:2025-08-29",
    "vectors_daily:2025-08-30",
    "vectors_daily:2025-08-31"
  ],
  "stats": {
    "kpis": {
      "totalSessions": 5312,
      "convertedSessions": 765,
      "nonConvertedSessions": 4547,
      "conversionRate": 0.144
    },
    "topPages": [{ "url": "/home", "count": 3120 }],
    "topEventTypes": [{ "type": "page_view", "count": 54012 }],
    "conversions": { "byType": [{ "conversionCode": "track_conversion_CHECKOUT", "count": 561 }] }
  }
}
```

### **Índices recomendados**

* unique (companyId, versionId)


* (companyId, type, dateRange.from)


* (createdAt)

## Histórico de status
- Backlog (backlog): 2025-08-29T14:18:02.995Z → 2025-08-29T14:27:20.714Z
- To-do (unstarted): 2025-08-29T14:27:20.714Z → 2025-09-04T19:37:20.061Z
- In Progress (started): 2025-09-04T19:37:20.061Z → 2025-09-05T13:55:12.198Z
- Pull Request (started): 2025-09-05T13:55:12.198Z → 2025-09-25T12:30:24.075Z
- Product Review (started): 2025-09-25T12:30:24.075Z → 2025-09-25T12:56:26.316Z
- Released (completed): 2025-09-25T12:56:26.316Z → atual

## Relações
—

## Anexos
—
