# SEND-170 — Cálculo de Tempo Médio por Conversão

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | Urgent |
| Responsável | Hugo Fernandes |
| Time | Sendspeed |
| Projeto | — |
| Labels | Tech Story |
| Parent | — |
| Criada | 2025-09-24T16:19:51.824Z por bruno.heidrich@sendspeed.com |
| Iniciada | 2025-10-10T15:11:14.399Z |
| Concluída | 2025-12-03T18:51:57.579Z |
| Arquivada | 2026-06-04T22:49:19.833Z |
| Vencimento | — |
| Branch | hugofernandes/send-170-calculo-de-tempo-medio-por-conversao |
| URL | https://linear.app/sendspeed/issue/SEND-170/calculo-de-tempo-medio-por-conversao |

## Descrição

**Como** Head de Produto
**Quero** que o sistema calcule e atualize a média de tempo entre o início da sessão e cada conversão (X, Y e Z),
**Para** entender quanto tempo os usuários levam, em média, para realizar cada tipo de conversão.

### Critérios de Aceite

* O cálculo deve ser feito separadamente para cada conversão (X, Y e Z).
* O tempo médio deve considerar apenas sessões em que a conversão de fato ocorreu.
* O cálculo deve ser atualizado de forma contínua (não apenas em batch manual).
* O resultado deve estar disponível para consultas analíticas em até **N segundos/minutos** após o evento (definir SLA).

---

> **[Imagem 1 — transcrição]:** Slide de apresentação intitulado **"Hardening Sprint 15 dias - Término 20/10/2025"**. É um diagrama de fluxo horizontal ilustrando o caso de uso da LiderBet. Da esquerda para a direita:
> - Bloco 1: dois KPIs riscados/anotados — "KPI: Qtd de previws do card na tela" e "KPI: Qtd de clicks no preview do card". Abaixo, um mockup de card promocional escuro com tema de tigre ("SURPRESA NO TIGRE SORTUDO / SÓ PRA VOCÊ", com botão e imagem de mascote tigre). Legenda abaixo: **"Event: Click no card xyz"**. Uma seta aponta para a direita.
> - Bloco 2: "KPI: Qtd de clicks no card". Mockup de tela cheia escura com card de boas-vindas "OFERTA DE BOAS-VINDAS!" e o mesmo tema de tigre. Seta para a direita.
> - Bloco 3: Mockup de página de cadastro/promoção com banner "15% ATÉ CASHBACK DIRETO NO SEU SALDO" (marca Lider), formulário de registro à direita com botão "CONCLUIR REGISTRO". Legenda abaixo: **"Event: Click no cta signup"**. Seta para a direita.
> - Bloco 4 (estrela amarela grande rotulada "NSM"): texto "Query: qtd sessões que clickaram primeiro no card xyz e depois signup" e "KPI: Qtd signup/First visit".
> - Painel lateral direito (caixa amarela) rotulado **"NSM:"** com texto em negrito "Qtd sessões que clickaram primeiro no card xyz e depois no signup". Abaixo, lista de KPIs: "Qtd clicks preview do card", "Qtd clicks no card", "Qtd signup/first_visit".

CASO DE USO ATUAL - LiderBet ✅

KPI's necessários:

* QTD DE CLICKS NO PREVIEWS DO CARD NA TELA
  * 
    ```json
    {event:click no card xyz}
    ```
* QTD DE CLICKS NO CARD
  * 
    ```json
    {event:click no cta signup?}
    ```
* QTD DE SESSÕES QUE CLICKARAM PRIMEIRO NO CARD XYZ E DEPOIS NO SIGNUP (signup/first_visit)
  * 
    ```json
    {event: signup + first_visit}
    ```

---

# Agregações usadas e resultados:

**Premissas e parâmetros**

* Collection: `events`
* Campos relevantes: `companyId`, `createdAt`, `sessionId`, `originalEventType`, `type`
* Chave de evento usada nas consultas: `eventKey = UPPER(COALESCE(originalEventType, type))`
* Filtro do dia (inline, sem variáveis shell):
  * `createdAt >= new Date(new Date().toISOString().slice(0,10) + 'T00:00:00.000-03:00')`
  * `createdAt <= new Date(new Date().toISOString().slice(0,10) + 'T23:59:59.999-03:00')`

Substitua `68c04d36acefcf067dff2148` pelo `companyId` desejado.

---

**Consulta A — Sessões únicas por tipo de evento (1 por sessão)**

Objetivo: quantas sessões de hoje tiveram ao menos 1 ocorrência de cada tipo de evento.

```
db.getCollection("events").aggregate([
  // 1) Eventos de hoje da empresa
  {
    $match: {
      companyId: "68c04d36acefcf067dff2148",
      createdAt: {
        $gte: new Date(
          new Date().toISOString().slice(0, 10) + "T00:00:00.000-03:00"
        ),
        $lte: new Date(
          new Date().toISOString().slice(0, 10) + "T23:59:59.999-03:00"
        ),
      },
      sessionId: { $ne: null },
    },
  },
  // 2) Normalizar a chave do evento
  {
    $project: {
      sessionId: 1,
      eventKey: { $toUpper: { $ifNull: ["$originalEventType", "$type"] } },
    },
  },
  // 3) Pairs distintos (evento, sessão): garante 1 por sessão
  { $group: { _id: { eventKey: "$eventKey", sessionId: "$sessionId" } } },
  // 4) Agrupar por tipo e somar sessões
  { $group: { _id: "$_id.eventKey", sessions: { $sum: 1 } } },
  // 5) Ordenar e projetar
  { $sort: { sessions: -1 } },
  { $project: { _id: 0, event: "$_id", sessions: 1 } },
]);
```

Passo a passo:

1. Filtramos apenas eventos do dia e da empresa.
2. Construímos `eventKey` com `originalEventType` (fallback `type`) em UPPER.
3. Agrupamos por `{eventKey, sessionId}` para remover duplicatas por sessão.
4. Reagrupamos por `eventKey` para obter o total de sessões.

Quando usar: KPI de alcance por evento (ex.: “quantas sessões tiveram BUYER_AGENT_NEW_CARD”).

## Formato de retorno

> **[Imagem 2 — transcrição]:** Screenshot de UI (resultado de query em ferramenta de banco, tema escuro) com duas colunas: **sessions** (numérica) e **event**. Linhas (sessions → event), a primeira destacada em azul:
> - 6903.0 → PAGE_VIEW
> - 5306.0 → CLICK
> - 4076.0 → VISIBILITY_CHANGE
> - 2237.0 → FORM_SUBMISSION
> - 1229.0 → SCROLL_DENSITY
> - 1032.0 → FORM_LEAVE
> - 311.0 → BUYER_AGENT_NEW_CARD
> - 291.0 → OFF_SCREEN_MOUSE
> - 157.0 → TRACK_CONVERSION_FR4F3
> - 117.0 → BUYER_AGENT_OPEN_CHAT_BOX
> - 117.0 → BUYER_AGENT_CHAT_BOX
> - 99.0 → TRACK_CONVERSION_1YGNV
> - 95.0 → BUYER_AGENT_CLOSE_CHAT_BOX
> - 51.0 → PAGE_EXIT
> - 45.0 → BUYER_AGENT_CARD_CLICK
> - 45.0 → BUYER_AGENT_CARD_CTA_CLICK
> - 6.0 → TRIGGER_CARD_MGB6YSZM_XA3D7R
> - 4.0 → TRACK_CONVERSION_L3J8Z
> - 1.0 → TRIGGER_CARD_MGGYXYMJ_0MEFUM
> - 1.0 → TRIGGER_CARD_MFZEP4N5_7LI52R

---

## **Consulta B — Ocorrências totais vs sessões únicas (repetição)**

Objetivo: identificar se há muitos eventos repetidos na mesma sessão.

```
db.getCollection("events").aggregate([
  {
    $match: {
      companyId: "68c04d36acefcf067dff2148",
      createdAt: {
        $gte: new Date(
          new Date(new Date().setDate(new Date().getDate() - 1))
            .toISOString()
            .slice(0, 10) + "T00:00:00.000-03:00"
        ),
        $lte: new Date(
          new Date(new Date().setDate(new Date().getDate() - 1))
            .toISOString()
            .slice(0, 10) + "T23:59:59.999-03:00"
        ),
      },
      sessionId: { $ne: null },
    },
  },
  {
    $addFields: {
      eventKey: { $toUpper: { $ifNull: ["$originalEventType", "$type"] } },
    },
  },
  {
    $group: {
      _id: "$eventKey",
      events: { $sum: 1 },
      sessionsSet: { $addToSet: "$sessionId" },
    },
  },
  {
    $project: {
      _id: 0,
      event: "$_id",
      events: 1,
      uniqueSessions: { $size: "$sessionsSet" },
      repeated: { $subtract: ["$events", { $size: "$sessionsSet" }] },
      repeatRate: {
        $cond: [
          { $gt: ["$events", 0] },
          {
            $round: [
              {
                $divide: [
                  { $subtract: ["$events", { $size: "$sessionsSet" }] },
                  "$events",
                ],
              },
              4,
            ],
          },
          0,
        ],
      },
    },
  },
  { $sort: { repeated: -1, events: -1 } },
]);
```

Interpretação:

* `events`: total de ocorrências do evento no dia.
* `uniqueSessions`: quantidade de sessões distintas com o evento.
* `repeated = events - uniqueSessions`: quantos eventos são “extras” (repetidos na mesma sessão).
* `repeatRate`: fração de repetição sobre o total.

Quando usar: diagnóstico de spam/ruído ou validação de instrumentação.

## Formato do retorno

> **[Imagem 3 — transcrição]:** Screenshot de UI (resultado de query, tema escuro) com colunas: **events**, **event**, **uniqueSessions**, **repeated**, **repeatRate**. Primeira linha destacada em azul (CLICK). Dados (events / event / uniqueSessions / repeated / repeatRate):
> - 59291.0 / CLICK / 5319 / 53972.0 / 0.9103
> - 36395.0 / PAGE_VIEW / 6918 / 29477.0 / 0.8099
> - 31869.0 / VISIBILITY_CHANGE / 4089 / 27780.0 / 0.8717
> - 5826.0 / SCROLL_DENSITY / 1232 / 4594.0 / 0.7885
> - 2200.0 / OFF_SCREEN_MOUSE / 294 / 1906.0 / 0.8664
> - 2612.0 / FORM_SUBMISSION / 2243 / 369.0 / 0.1413
> - 338.0 / BUYER_AGENT_CARD_CLICK / 45 / 293.0 / 0.8669
> - 543.0 / BUYER_AGENT_NEW_CARD / 313 / 230.0 / 0.4236
> - 1212.0 / FORM_LEAVE / 1034 / 178.0 / 0.1469
> - 182.0 / BUYER_AGENT_CARD_CTA_CLICK / 45 / 137.0 / 0.7527
> - 212.0 / BUYER_AGENT_CHAT_BOX / 117 / 95.0 / 0.4481
> - 225.0 / TRACK_CONVERSION_FR4F3 / 158 / 67.0 / 0.2978
> - 181.0 / BUYER_AGENT_OPEN_CHAT_BOX / 117 / 64.0 / 0.3536
> - 151.0 / BUYER_AGENT_CLOSE_CHAT_BOX / 96 / 55.0 / 0.3642
> - 76.0 / PAGE_EXIT / 51 / 25.0 / 0.3289
> - 114.0 / TRACK_CONVERSION_1YGNV / 99 / 15.0 / 0.1316
> - 9.0 / TRIGGER_CARD_MGB6YSZM_XA3D7R / 6 / 3.0 / 0.3333
> - 4.0 / TRACK_CONVERSION_L3J8Z / 4 / 0.0 / 0.0
> - 1.0 / TRIGGER_CARD_MGGYXYMJ_0MEFUM / 1 / 0.0 / 0.0
> - 1.0 / TRIGGER_CARD_MFZEP4N5_7LI52R / (demais colunas cortadas)

---

## **(Opcional) Sessões com repetição por tipo (amostras)**

```
db.getCollection("events").aggregate([
  {
    $match: {
      companyId: "68c04d36acefcf067dff2148",
      createdAt: {
        $gte: new Date(
          new Date().toISOString().slice(0, 10) + "T00:00:00.000-03:00"
        ),
        $lte: new Date(
          new Date().toISOString().slice(0, 10) + "T23:59:59.999-03:00"
        ),
      },
      sessionId: { $ne: null },
    },
  },
  {
    $addFields: {
      eventKey: { $toUpper: { $ifNull: ["$originalEventType", "$type"] } },
    },
  },
  {
    $group: {
      _id: { event: "$eventKey", session: "$sessionId" },
      count: { $sum: 1 },
    },
  },
  { $match: { count: { $gt: 1 } } },
  { $sort: { count: -1 } },
  { $limit: 100 },
  {
    $project: {
      _id: 0,
      event: "$_id.event",
      sessionId: "$_id.session",
      count: 1,
    },
  },
]);
```

## Formato do retorno

> **[Imagem 4 — transcrição]:** Screenshot de UI (resultado de query, tema escuro) com três colunas: **count**, **event**, **sessionId**. Primeira linha destacada em azul. Dados (count / event / sessionId):
> - 410.0 / PAGE_VIEW / sess_ab24896a-caf6-4314-9a19-721905c2a90e
> - 266.0 / PAGE_VIEW / sess_790187fe-a2d6-44bb-b13b-8b81411fb95f
> - 226.0 / PAGE_VIEW / sess_8d2aab07-1960-4aed-a81d-71d0e7e0f8c9
> - 207.0 / SCROLL_DENSITY / sess_32eab155-a030-4c38-a74a-405bb23c95ce
> - 206.0 / VISIBILITY_CHANGE / sess_9350f034-444f-43a4-bf0b-f6371b91a035
> - 203.0 / PAGE_VIEW / sess_49c3d057-23d7-421d-8cb2-6962dc5ee921
> - 188.0 / VISIBILITY_CHANGE / sess_c77becf4-a942-4dcc-9790-3a6a42a04213
> - 179.0 / PAGE_VIEW / sess_2490bcaf-6ca9-47e8-8fd0-4dd436dff7ce
> - 178.0 / VISIBILITY_CHANGE / sess_4592cea2-41cd-4970-bb6c-7cf825de2fd1
> - 177.0 / CLICK / sess_ab24896a-caf6-4314-9a19-721905c2a90e
> - 167.0 / CLICK / sess_3628becf-7965-4c36-8cec-2c789ef860f9
> - 166.0 / VISIBILITY_CHANGE / sess_1a57df66-3363-4456-bc6e-1939c718d8c6
> - 161.0 / VISIBILITY_CHANGE / sess_1b4a330e-ff5d-4926-9471-c3744016487c
> - 161.0 / CLICK / sess_9861c687-2b1e-41bb-a820-51b1420ee688
> - 159.0 / VISIBILITY_CHANGE / sess_62d0e67a-f8d1-411f-8f93-602e4f8bc40a
> - 154.0 / VISIBILITY_CHANGE / sess_970e62bd-0358-4649-9350-def6e8f7881f
> - 154.0 / VISIBILITY_CHANGE / sess_664fe196-a5f0-45f9-893e-62e86cf9289d
> - 152.0 / CLICK / sess_a5c28821-e748-4955-8019-8f48bb7286dc
> - 148.0 / CLICK / sess_41ef01a5-9612-48e1-8767-8ba2880f7598
> - 148.0 / PAGE_VIEW / sess_cea0bdcd-13cd-4bf5-879b-1168b47df6d9
> - 146.0 / VISIBILITY_CHANGE / sess_e02363fc-289b-4d32-8cb6-02fdb938f2e4
> - 142.0 / VISIBILITY_CHANGE / sess_4a611808-32e4-4827-95e0-52b8cfe9bc8d (parcial)

---

## **(Anexo) Converter epoch_time → DateTime America/Sao_Paulo**

```
db.getCollection("events").aggregate([
  { $match: { sessionId: "sess_..." } },
  {
    $addFields: {
      epochMs: {
        $toLong: {
          $cond: [
            { $gte: ["$epoch_time", NumberLong("1000000000000")] },
            "$epoch_time",
            { $multiply: ["$epoch_time", 1000] },
          ],
        },
      },
    },
  },
  {
    $project: {
      _id: 0,
      companyId: 1,
      sessionId: 1,
      originalEventType: 1,
      epoch_time_converted: {
        $dateToString: {
          date: { $toDate: "$epochMs" },
          timezone: "America/Sao_Paulo",
          format: "%Y-%m-%d %H:%M:%S",
        },
      },
    },
  },
]);
```

---

## **Dicas de performance**

* Indexes recomendados em `events`: `{companyId, createdAt}`, `{sessionId, createdAt}`, `{originalEventType, createdAt}`, `{type, createdAt}`.
* Prefira prefixo ancorado em regex (`^EVENT`) quando filtrar por nome de evento.
* Para card analytics, normalize `eventKey` e filtre depois do `$addFields`.

---

## **Leitura rápida dos resultados**

* Consulta A responde “quantas sessões tocaram cada evento hoje”.
* Consulta B responde “quantos eventos são repetidos por sessão e quanto isso representa do total”.
* Use a amostra de sessões repetidas para investigar origens de duplicidade.

---

```
db.getCollection("events").aggregate([
  {
    $match: {
      $or: [
        { companyId: "68c04d36acefcf067dff2148" },
        { company_id: "68c04d36acefcf067dff2148" }
      ],
      createdAt: {
        $gte: new Date(new Date(new Date().getTime() - 48*60*60*1000).toISOString().slice(0,10) + "T00:00:00.000-03:00"),
        $lte: new Date(
          new Date().toISOString().slice(0, 10) + "T23:59:59.999-03:00"
        ),},
      sessionId: { $ne: null }
    }
  },
  { $sort: { sessionId: 1, createdAt: 1 } },
  {
    $group: {
      _id: "$sessionId",
      firstEventTime: { $first: "$createdAt" },
      events: {
        $push: {
          key: { $toUpper: { $ifNull: ["$metadata.originalEventType", "$type"] } },
          createdAt: "$createdAt"
        }
      }
    }
  },
  {
    $project: {
      _id: 0,
      sessionId: "$_id",
      firstEventAt: "$firstEventTime",

      "Fechou Modal": {
        $let: {
          vars: {
            firstCustom: {
              $arrayElemAt: [
                {
                  $filter: {
                    input: "$events",
                    as: "e",
                    cond: { $eq: ["$$e.key", "TRACK_CONVERSION_1YGNV"] }
                  }
                },
                0
              ]
            }
          },
          in: {
            $cond: [
              { $ne: ["$$firstCustom", null] },
              {
                $divide: [
                  { $subtract: ["$$firstCustom.createdAt", "$firstEventTime"] },
                  1000
                ]
              },
              null
            ]
          }
        }
      },

      "Registro Concluído": {
        $let: {
          vars: {
            firstCustom: {
              $arrayElemAt: [
                {
                  $filter: {
                    input: "$events",
                    as: "e",
                    cond: { $eq: ["$$e.key", "TRACK_CONVERSION_FR4F3"] }
                  }
                },
                0
              ]
            }
          },
          in: {
            $cond: [
              { $ne: ["$$firstCustom", null] },
              {
                $divide: [
                  { $subtract: ["$$firstCustom.createdAt", "$firstEventTime"] },
                  1000
                ]
              },
              null
            ]
          }
        }
      }
    }
  },
  {
    $match: {
      "Fechou Modal": { $ne: null },
      "Registro Concluído": { $ne: null }
    }
  },
  { $sort: { sessionId: 1 } }
]);
```

LINK COM UTM

```
db.getCollection("events").aggregate([
  {
    $match: {
      companyId: "68c04d36acefcf067dff2148",
      createdAt: {
        $gte: new Date(
          new Date(new Date().setDate(new Date().getDate() - 2))
            .toISOString()
            .slice(0, 10) + "T00:00:00.000-03:00"
        ),
        $lte: new Date(
          new Date(new Date().setDate(new Date().getDate() - 2))
            .toISOString()
            .slice(0, 10) + "T23:59:59.999-03:00"
        ),
      },
        sessionId: { $ne: null },
        url: { $regex: /[?&]utm_/i } // apenas URLs com UTM
    },
  },
  {
    $addFields: {
      eventKey: { $toUpper: { $ifNull: ["$originalEventType", "$type"] } },
    },
  },
  {
    $facet: {
      totals: [
        {
          $group: {
            _id: null,
            events: { $sum: 1 },
            sessionsSet: { $addToSet: "$sessionId" },
          },
        },
        {
          $project: {
            _id: 0,
            events: 1,
            uniqueSessions: { $size: "$sessionsSet" },
          },
        },
      ],
      byEvent: [
        {
          $group: {
            _id: "$eventKey",
            events: { $sum: 1 },
            sessionsSet: { $addToSet: "$sessionId" },
          },
        },
        {
          $project: {
            _id: 0,
            event: "$_id",
            events: 1,
            uniqueSessions: { $size: "$sessionsSet" },
            repeated: { $subtract: ["$events", { $size: "$sessionsSet" }] },
            repeatRate: {
              $cond: [
                { $gt: ["$events", 0] },
                {
                  $round: [
                    {
                      $divide: [
                        { $subtract: ["$events", { $size: "$sessionsSet" }] },
                        "$events",
                      ],
                    },
                    4,
                  ],
                },
                0,
              ],
            },
          },
        },
        { $sort: { repeated: -1, events: -1 } },
      ],
    },
  },
]);
```

## Histórico de status
- In Progress (started): 2025-09-24T16:19:51.824Z → 2025-10-09T18:37:20.822Z
- Paused (unstarted): 2025-10-09T18:37:20.822Z → 2025-10-10T14:57:24.072Z
- Pull Request (started): 2025-10-10T14:57:24.072Z → 2025-10-10T15:01:13.317Z
- In Progress (started): 2025-10-10T15:01:13.317Z → 2025-10-10T15:07:30.173Z
- To-do (unstarted): 2025-10-10T15:07:30.173Z → 2025-10-10T15:11:14.431Z
- In Progress (started): 2025-10-10T15:11:14.431Z → 2025-10-23T18:58:29.391Z
- Pull Request (started): 2025-10-23T18:58:29.391Z → 2025-10-30T19:03:20.068Z
- In Progress (started): 2025-10-30T19:03:20.068Z → 2025-10-30T19:03:42.595Z
- Pull Request (started): 2025-10-30T19:03:42.595Z → 2025-12-03T17:25:08.731Z
- Product Review (started): 2025-12-03T17:25:08.731Z → 2025-12-03T18:51:57.619Z
- Released (completed): 2025-12-03T18:51:57.619Z → atual

## Relações
—

## Anexos
—
