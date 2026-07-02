# SEND-17 — Geração Textual do EmbeddingText para Cada Evento Rastreado

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | No priority |
| Responsável | — |
| Time | Sendspeed |
| Projeto | SendSpeed 2.0 |
| Labels | Tech Story, Tracker |
| Parent | — |
| Criada | 2025-05-26T21:47:36.283Z por pedro.antunes@sendspeed.com |
| Iniciada | — |
| Concluída | 2025-07-10T12:19:35.755Z |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-17-geracao-textual-do-embeddingtext-para-cada-evento-rastreado |
| URL | https://linear.app/sendspeed/issue/SEND-17/geracao-textual-do-embeddingtext-para-cada-evento-rastreado |

## Descrição

**Como** engenheiro de dados do Tracker,
**Quero** que para cada evento rastreado o sistema gere e armazene um campo `embeddingText` em formato textual,
**Para que** esse texto possa futuramente servir como insumo principal para algoritmos de IA interpretarem o contexto e a intenção por trás das ações do usuário.

### 📌 Descrição Funcional

* O `embeddingText` deve ser uma **descrição em linguagem natural** (string) que combine e resuma as informações relevantes daquele evento.
* Ele deve ser criado **no momento do registro** do evento (real-time, sem etapa assíncrona).
* Esse texto será armazenado junto ao documento do evento no MongoDB, no campo `embeddingText`.
* **Não deve ser vetorizado neste momento** (sem uso de embeddings vetoriais ou IA). Apenas texto plano.

---

### ✅ Exemplo de `embeddingText`

Para o evento:

```
json
```

`{ "eventType": "click", "title": "TechMarket – Marketplace de Tecnologia", "url": "http://localhost:3200/demo", "elementId": "btn-comprar" }`

A string gerada poderia ser:

```
text
```

`"Evento click na página http://localhost:3200/demo com título 'TechMarket – Marketplace de Tecnologia'. Clique no elemento 'btn-comprar'."`

---

### ✅ Critérios de Aceite

* O campo `embeddingText` deve ser gerado e preenchido automaticamente para **todos os tipos de evento**.
* Deve seguir um formato consistente baseado no tipo do evento:
  * Para `pageview`: "Usuário visitou a página \[URL\] com título '\[title\]'."
  * Para `click`: "Clique no elemento '\[elementId\]' na página \[URL\] com título '\[title\]'."
  * Para `search`: "Busca realizada com o termo '\[searchTerm\]' na página \[URL\]."
  * Para `purchase`: "Compra efetuada no valor de R$ \[value\] no pedido \[orderId\]."
* O texto deve ser gerado **com foco na clareza e contexto da ação**, pensando no entendimento humano e futuro uso por IA.
* O campo `embeddingText` deve ser salvo dentro do documento do evento no MongoDB, no mesmo nível de `eventType`, `timestamp`, etc.
* O campo `embeddingGenerated` deve ser setado como `false` por padrão (indicando que ainda não foi vetorizado).

---

### 🧠 Observações

* O foco é gerar o melhor "texto de entendimento" possível para cada evento.
* Esse texto servirá para análise posterior, auditoria manual e insumo para **IA generativa**, como o Behavior Agent.
* No futuro, esse `embeddingText` será vetorizado, mas **isso não faz parte desta US**.

## Histórico de status

- Backlog (backlog): 2025-05-26T21:47:36.283Z → 2025-05-27T04:34:52.290Z
- To-do (unstarted): 2025-05-27T04:34:52.290Z → 2025-05-28T10:19:54.883Z
- Backlog (backlog): 2025-05-28T10:19:54.883Z → 2025-05-28T13:56:28.764Z
- To-do (unstarted): 2025-05-28T13:56:28.764Z → 2025-07-10T12:19:35.738Z
- Released (completed): 2025-07-10T12:19:35.738Z → atual

## Relações

—

## Anexos

—
