# SEND-275 — Capturar e persistir query params da URL em campo estruturado `url_params` nos eventos

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | No priority |
| Responsável | Vinicius Carneiro |
| Time | Sendspeed |
| Projeto | — |
| Labels | — |
| Parent | — |
| Criada | 2026-01-06T11:32:21.584Z por pedro.antunes@sendspeed.com |
| Iniciada | 2026-01-06T12:56:45.734Z |
| Concluída | 2026-01-12T14:58:27.143Z |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-275-capturar-e-persistir-query-params-da-url-em-campo |
| URL | https://linear.app/sendspeed/issue/SEND-275/capturar-e-persistir-query-params-da-url-em-campo-estruturado-url |

## Descrição

**Como** time de Growth
**Quero** que todos os parâmetros de query string presentes na URL sejam capturados e salvos de forma estruturada
**Para** permitir análises eficientes de campanhas, UTMs e origem de tráfego sem uso de regex em URL

### 🎯 Contexto

Atualmente os query params (ex: `utm_*`) ficam apenas embutidos na URL como string.
Isso dificulta:

* performance de queries
* criação de índices eficientes
* análises em MongoDB e BigQuery
* construção de funis e atribuição de campanhas

Cenário atual :

Hoje, os parâmetros vem junto com a URL apenas, dificultando e compromento as buscas por parâmetros.

> **[Imagem 1 — transcrição]:** Screenshot de UI — visualização de um documento/registro de evento (aparência de console MongoDB / visualizador de documento JSON, fundo branco com destaque de sintaxe). Campos e valores exibidos: `_id`: ObjectId('695ceb3ce4a606af1ae870e5'); `apiKey`: "570f1949-8a7b-4fa1-b8b1-ee064044ce2a"; `deviceFingerprint`: "4a4eac8c39edda63b162a57c31c5b8196cc3a260ae85bf774bbfb3a47d2c399d"; `deviceInfo`: Object; `localstorageId`: "SmartTrack__local_i9lp5xdtylamj1f9ap2"; `sessionId`: "sess_77d34fc1-e8d2-414e-9938-9792d6a8e81b"; `visitorId`: "693ababd9f4a357d57358380"; `companyId`: "6927206ff6a052cfcd39dd28"; `externalUserId`: null; `referrer`: null; `url`: "https://jogao.bet.br/?utm_ui=userin_teste" (linha destacada em cinza); `title`: "Jogão Cassino e Apostas Online - Apostas Esportivas e Cassino ao Vivo ..."; `originalEventType`: "PAGE_VIEW"; `type`: "pageshow"; `metadata`: Object; `epoch_time`: 1767697206377; `createdAt`: 2026-01-06T08:00:06.000+00:00; `receivedAt`: 2026-01-06T08:00:12.000+00:00. Demonstra o cenário atual em que os parâmetros de query (ex: utm_ui=userin_teste) ficam embutidos apenas dentro do campo `url` como string, sem um campo estruturado dedicado.

---

## ✅ Critérios de Aceite (Acceptance Criteria)

### 1️⃣ Captura automática

* Dado que um evento contenha uma URL com query params
* Quando o evento for processado
* Então **todos os query params** devem ser extraídos e salvos no campo `url_params`

---

### 2️⃣ Estrutura do campo `url_params`

* `url_params` deve ser um **objeto JSON (key-value)**
* Cada parâmetro da query string vira uma chave
* Valores devem ser **strings**
* Chaves devem ser **case-sensitive conforme a URL original**

📌 Exemplo:

URL:

```
https://site.com/page?utm_ui=userin_teste&utm_campaign=promo_jan&ref=google
```

Evento persistido:

```
{
  "url": "https://site.com/page?utm_ui=userin_teste&utm_campaign=promo_jan&ref=google",
  "url_params": {
    "utm_ui": "userin_teste",
    "utm_campaign": "promo_jan",
    "ref": "google"
  }
}
```

---

### 3️⃣ Ausência de query params

* Se a URL **não** contiver query params:
  * o campo `url_params` **não deve existir**
  * ou deve ser `null` (definir padrão)

---

### 4️⃣ Não duplicar informação

* Os parâmetros **não devem** ser salvos em `metadata`
* `url` original deve ser preservada integralmente

---

### 5️⃣ Compatibilidade com eventos existentes

* A mudança deve valer **apenas para novos eventos**
* Eventos históricos **não precisam de backfill** nesta fase

---

## 🧪 Exemplos de Query (validação)

### Buscar por campanha específica

```
{
  companyId: "6927206ff6a052cfcd39dd28",
  type: "pageshow",
  "url_params.utm_campaign": "promo_jan"
}
```

### Buscar por UTM UI

```
{
  "url_params.utm_ui": "userin_teste"
}
```

---

## 🧠 Considerações Técnicas (Definition Notes)

* A extração deve ocorrer:
  * no **tracker / ingestion layer**
  * antes da persistência no MongoDB
* O parser deve:
  * suportar múltiplos parâmetros
  * tratar encoding (`%20`, `+`, etc.)
* Deve ignorar fragmentos (`#hash`)
* Caso existam parâmetros repetidos:
  * usar o **último valor**

## Histórico de status
- Paused (unstarted): 2026-01-06T11:32:21.584Z → 2026-01-06T12:56:45.743Z
- In Progress (started): 2026-01-06T12:56:45.743Z → 2026-01-06T17:38:58.022Z
- Product Review (started): 2026-01-06T17:38:58.022Z → 2026-01-12T14:58:27.162Z
- Released (completed): 2026-01-12T14:58:27.162Z → atual

## Relações
—

## Anexos
—
