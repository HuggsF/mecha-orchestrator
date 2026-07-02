# SEND-446 — Feature: Integrar encurtador de links na criação de SMS e RCS (botões de carrossel) para metrificação de cliques

| Campo | Valor |
| -- | -- |
| Status | To-do (unstarted) |
| Prioridade | High |
| Responsável | andrei.garcia@externo.sendspeed.com |
| Time | Sendspeed |
| Projeto | — |
| Labels | User Story, UserIn, Implementação, Analytics |
| Parent | — |
| Criada | 2026-04-02T14:44:48.907Z por Vinicius Carneiro |
| Iniciada | — |
| Concluída | — |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-446-feature-integrar-encurtador-de-links-na-criacao-de-sms-e-rcs |
| URL | https://linear.app/sendspeed/issue/SEND-446/feature-integrar-encurtador-de-links-na-criacao-de-sms-e-rcs-botoes-de |

## Descrição

## Contexto

Já temos um encurtador de links funcional na plataforma (`ShortLink` + `ClickEvent`) que é usado nas **campanhas SMS** via `CampaignWorker.processUrls`. Porém, ele **não está integrado** em todos os pontos de criação de mensagens, especificamente:

1. **SMS nas Jornadas** (`SendSmsExecutor`) — envia a URL crua, sem encurtar nem rastrear
2. **RCS** — não existe editor de conteúdo rico (carousel, rich card, botões) neste repo; RCS é tratado como texto simples idêntico ao SMS
3. **Templates RCS** — não há como configurar botões de carrossel com URLs encurtadas

---

## Encurtador existente (o que já temos)

### Infraestrutura

| Componente | Arquivo | Função |
| -- | -- | -- |
| Model | `domain/models/ShortLink.js` | `code`, `destinationUrl`, `injectParams`, `stats`, `campaignId` |
| Clicks | `domain/models/ClickEvent.js` | `shortLinkId`, `visitorHash`, `clickCount`, `device`, `queryParams`, `campaignId` |
| Service | `application/services/shortLinkService.js` | `createLink()`, `processRedirect()`, `buildFinalUrl()` |
| Redirect | `index.js` | `GET /r/:code` e `GET /l/:code` → `handleRedirect` |
| CRUD API | `routes/shortLinkRoutes.js` | `POST /api/short-links`, etc. |

### Onde já funciona

* **Campanhas SMS** (`CampaignWorker.processUrls`): substitui `{{url_destino}}` por link encurtado com UTM + `campaignId`
* **Campanhas sync** (`campaignService.sendToRecipient`): mesmo fluxo via `shortLinkService.createLink`

### Onde NÃO funciona (escopo deste card)

* **Pipeline de disparo SMS** (jornadas e triggers): mensagem chega com URL do parceiro e é enviada crua
* **Botões de URL no RCS** (carrossel e rich card): não existe encurtamento
* **Analytics de cliques por jornada**: `ClickEvent` não tem `journeyId`

---

## Objetivo

Integrar o encurtador de links existente em dois pontos específicos:

1. **SMS — Na pipeline de disparo:** Quando a mensagem é recebida para envio, **identificar URLs no corpo da mensagem** e substituí-las automaticamente pelo nosso link encurtado antes de despachar para o provedor
2. **RCS — No momento da configuração do botão:** Quando o usuário coloca a URL no botão do carrossel/rich card, **substituir pela URL encurtada** no salvamento/envio, de forma que quando o destinatário clicar no botão da mensagem RCS, utilizará o nosso link

---

## Especificação técnica

### 1\. SMS — Encurtamento na pipeline de disparo

**Onde:** No momento em que a mensagem entra na pipeline de envio, **antes** de chamar a API de integrações.

**Pontos de interceptação (3 paths de envio de SMS):**

| Path | Arquivo | Onde interceptar |
| -- | -- | -- |
| Jornada offsite | `SendSmsExecutor.js` | Após resolver variáveis Liquid, antes do `POST /api/sms/:companyId/send` |
| Campanha Kafka | `CampaignWorker.js` | Já tem `processUrls` — **manter e padronizar** |
| Campanha sync | `campaignService.js` | Já tem encurtamento — **manter e padronizar** |

**Lógica unificada (novo método em** `shortLinkService`):

```javascript
/**
 * Detecta URLs na mensagem e substitui por links encurtados.
 * Chamado pela pipeline de disparo antes de enviar ao provedor.
 */
async shortenUrlsInMessage(message, context) {
  const urlRegex = /https?:\/\/[^\s]+/g;
  const urls = message.match(urlRegex);
  if (!urls?.length) return { message, shortLinks: [] };

  const shortLinks = [];
  let processedMessage = message;

  for (const url of urls) {
    const shortLink = await this.createLink({
      destinationUrl: url,
      companyId: context.companyId,
      journeyId: context.journeyId || null,
      campaignId: context.campaignId || null,
      executionId: context.executionId || null,
      nodeId: context.nodeId || null,
      userId: context.externalId || null,
      channel: 'sms',
      injectParams: {
        utm_source: 'userin',
        utm_medium: 'sms',
        utm_campaign: context.journeyId || context.campaignId || '',
        utm_content: context.nodeId || '',
      },
    });
    processedMessage = processedMessage.replace(url, `${SHORT_LINK_BASE_URL}/r/${shortLink.code}`);
    shortLinks.push(shortLink);
  }

  return { message: processedMessage, shortLinks };
}
```

**Integração no** `SendSmsExecutor.js`:

```javascript
// Após resolver Liquid e ANTES de enviar
const { message: finalMessage, shortLinks } = await shortLinkService.shortenUrlsInMessage(
  resolvedMessage,
  {
    companyId,
    journeyId: context.journeyId,
    executionId: context.executionId,
    nodeId: this.nodeId,
    externalId,
  }
);

// Enviar com mensagem processada
const response = await axios.post(`${INTEGRATIONS_API_URL}/api/sms/${companyId}/send`, {
  credentialId,
  userPhone: phone,
  message: finalMessage,  // << URLs já substituídas
});
```

**Resultado:** A mensagem que o parceiro configurou com `https://bet.exemplo.com/promo?id=123` chega no celular do usuário como `https://userin.ai/r/xK9mP` — mais curta (economiza GSM-7) e rastreará cada clique.

### 2\. RCS — Encurtamento no botão do carrossel

**Onde:** No momento em que o usuário configura a URL do botão no editor de RCS. A substituição acontece no **salvamento/envio** do template ou da campanha, **não** no frontend (para manter a URL original visível no editor).

**Fluxo:**

```
1. Usuário configura carrossel no editor RCS:
   Botão: "Apostar Agora" → URL: https://bet.exemplo.com/promo
   ↓
2. Frontend salva o template/campanha com a URL original
   ↓
3. No momento do ENVIO (executor ou worker), antes de chamar a API:
   a. Percorre cada card do carrossel
   b. Para cada suggestion do tipo 'open_url':
      - Cria ShortLink com a URL original
      - Substitui a URL pela encurtada
   ↓
4. API de integrações recebe o carrossel com URLs encurtadas nos botões
   ↓
5. Destinatário recebe RCS, clica no botão "Apostar Agora"
   ↓
6. GET /r/xK9mP → ClickEvent gravado → redirect para URL original
```

**Novo método em** `shortLinkService`:

```javascript
/**
 * Encurta URLs nos botões (suggestions) de cada card do carrossel/rich card RCS.
 * Chamado no momento do envio, após carregar o template.
 */
async shortenRcsButtonUrls(rcsContent, context) {
  if (!rcsContent?.cards?.length) return rcsContent;

  const processedContent = JSON.parse(JSON.stringify(rcsContent));

  for (let cardIdx = 0; cardIdx < processedContent.cards.length; cardIdx++) {
    const card = processedContent.cards[cardIdx];
    for (const suggestion of card.suggestions || []) {
      if (suggestion.type === 'open_url' && suggestion.url) {
        const shortLink = await this.createLink({
          destinationUrl: suggestion.url,
          companyId: context.companyId,
          journeyId: context.journeyId || null,
          campaignId: context.campaignId || null,
          executionId: context.executionId || null,
          nodeId: context.nodeId || null,
          userId: context.externalId || null,
          channel: 'rcs',
          metadata: {
            cardIndex: cardIdx,
            buttonText: suggestion.text,
            contentType: rcsContent.type,  // 'carousel' | 'rich_card'
          },
          injectParams: {
            utm_source: 'userin',
            utm_medium: 'rcs',
            utm_campaign: context.journeyId || context.campaignId || '',
            utm_content: `card${cardIdx}_${suggestion.text}`,
          },
        });
        suggestion.url = `${SHORT_LINK_BASE_URL}/r/${shortLink.code}`;
      }
    }
  }

  return processedContent;
}
```

**Integração no** `CampaignWorker.js` (canal RCS):

```javascript
if (channel === 'rcs' && campaign.rcsContent) {
  const processedRcsContent = await shortLinkService.shortenRcsButtonUrls(
    campaign.rcsContent,
    { companyId, campaignId: campaign._id, externalId: recipient.externalId }
  );

  endpoint = `${INTEGRATIONS_API_URL}/api/rcs/${companyId}/send`;
  body = {
    credentialId,
    userPhone: phone,
    contentType: campaign.rcsContent.type,
    message: textFallback,
    rcsContent: processedRcsContent,
  };
}
```

**Integração no** `SendRcsExecutor.js` (jornada):

```javascript
// Antes de enviar, encurtar URLs nos botões
const processedContent = await shortLinkService.shortenRcsButtonUrls(
  rcsContent,
  {
    companyId,
    journeyId: context.journeyId,
    executionId: context.executionId,
    nodeId: this.nodeId,
    externalId,
  }
);

// Enviar com botões já encurtados
await axios.post(`${INTEGRATIONS_API_URL}/api/rcs/${companyId}/send`, {
  credentialId,
  userPhone: phone,
  contentType: processedContent.type,
  message: fallbackSms,
  rcsContent: processedContent,
});
```

### 3\. Alterações nos Models

`ShortLink.js` — novos campos:

```javascript
journeyId: { type: mongoose.Schema.Types.ObjectId, ref: 'JourneyWorkflow', default: null },
executionId: { type: mongoose.Schema.Types.ObjectId, ref: 'JourneyExecution', default: null },
nodeId: { type: String, default: null },
channel: { type: String, enum: ['sms', 'rcs', 'email', 'whatsapp'], default: null },
userId: { type: String, default: null },
metadata: { type: mongoose.Schema.Types.Mixed, default: {} },
```

Índices:

```javascript
shortLinkSchema.index({ journeyId: 1, createdAt: -1 });
shortLinkSchema.index({ campaignId: 1, createdAt: -1 });
```

`ClickEvent.js` — novos campos herdados do ShortLink:

```javascript
journeyId: { type: mongoose.Schema.Types.ObjectId, default: null },
executionId: { type: mongoose.Schema.Types.ObjectId, default: null },
nodeId: { type: String, default: null },
channel: { type: String, default: null },
```

`processRedirect`: Propagar `journeyId`, `executionId`, `nodeId`, `channel` do `ShortLink` para o `ClickEvent` no momento do redirect.

### 4\. Analytics de cliques

**Jornadas —** `GET /api/journeys/:id/analytics`:

```javascript
const clickStats = await ClickEvent.aggregate([
  { $match: { journeyId: ObjectId(journeyId) } },
  { $group: {
    _id: '$nodeId',
    totalClicks: { $sum: '$clickCount' },
    uniqueClicks: { $sum: 1 },
  }},
]);
```

**Campanhas RCS —** Cliques por botão do carrossel:

```javascript
const buttonClickStats = await ClickEvent.aggregate([
  { $match: { campaignId: ObjectId(campaignId), channel: 'rcs' } },
  { $lookup: { from: 'shortlinks', localField: 'shortLinkId', foreignField: '_id', as: 'link' } },
  { $unwind: '$link' },
  { $group: {
    _id: { cardIndex: '$link.metadata.cardIndex', buttonText: '$link.metadata.buttonText' },
    totalClicks: { $sum: '$clickCount' },
    uniqueClicks: { $sum: 1 },
  }},
]);
```

### 5\. Frontend

**Editor de nó SMS na jornada:**

* Toggle "Encurtar links automaticamente" (default: ativado)
* Helper text: "URLs detectadas na mensagem serão substituídas por links curtos rastreados"

**Editor de RCS (botões):**

* Input de URL no botão mostra badge informativo: "🔗 Link será encurtado automaticamente"
* No preview do celular, exibir a URL encurtada no botão
* A URL original permanece no input do editor (a substituição é no envio)

**Analytics:**

* Jornada: exibir cliques por nó de envio (SMS e RCS)
* Campanha RCS: exibir cliques por botão do carrossel (Card 1: N cliques, Card 2: N cliques)

---

## Fluxo visual

### SMS — Pipeline de disparo

```
Mensagem chega na pipeline
"Promo especial! Acesse https://bet.exemplo.com/promo?id=123"
                          │
                          ▼
       shortenUrlsInMessage() detecta a URL
                          │
                          ▼
       ShortLink criado: code=xK9mP, destinationUrl=bet.exemplo.com/promo?id=123
                          │
                          ▼
Mensagem processada:
"Promo especial! Acesse https://userin.ai/r/xK9mP"
                          │
                          ▼
       POST /api/sms/:companyId/send
                          │
                          ▼
       Usuário recebe SMS e clica no link
                          │
                          ▼
       GET /r/xK9mP → ClickEvent gravado → redirect 302
```

### RCS — Botão do carrossel

```
Editor: usuário coloca URL no botão
Botão "Apostar" → https://bet.exemplo.com/promo
                          │
                          ▼
       Template/campanha salvo com URL original
                          │
                          ▼
       No momento do ENVIO:
       shortenRcsButtonUrls() percorre cada card
                          │
                          ▼
       ShortLink criado: code=yL3nQ, metadata={ cardIndex: 0, buttonText: 'Apostar' }
                          │
                          ▼
       Botão enviado com: url=https://userin.ai/r/yL3nQ
                          │
                          ▼
       Destinatário recebe RCS, clica em "Apostar"
                          │
                          ▼
       GET /r/yL3nQ → ClickEvent { channel: 'rcs', metadata.cardIndex: 0 }
       → redirect 302 para https://bet.exemplo.com/promo
```

---

## Critérios de aceite

### SMS (pipeline de disparo)

- [ ] `shortLinkService.shortenUrlsInMessage()` implementado
- [ ] `SendSmsExecutor` chama `shortenUrlsInMessage` antes de enviar ao provedor
- [ ] `CampaignWorker` (SMS path) padronizado para usar mesmo método
- [ ] `campaignService` (sync path) padronizado para usar mesmo método
- [ ] URLs no corpo da mensagem são substituídas por links encurtados
- [ ] `ShortLink` criado com `journeyId`/`campaignId`, `channel: 'sms'`, `userId`, UTMs
- [ ] Toggle de encurtamento no painel do nó SMS da jornada

### RCS (botão do carrossel)

- [ ] `shortLinkService.shortenRcsButtonUrls()` implementado
- [ ] Encurtamento acontece no momento do **envio**, não no salvamento do template
- [ ] URL original permanece no editor; substituição é transparente
- [ ] Cada botão `open_url` gera `ShortLink` individual com `metadata.cardIndex` e `metadata.buttonText`
- [ ] `CampaignWorker` (RCS path) chama `shortenRcsButtonUrls` antes de enviar
- [ ] `SendRcsExecutor` (jornada) chama `shortenRcsButtonUrls` antes de enviar
- [ ] Fallback SMS do RCS também tem URLs encurtadas

### Models e Analytics

- [ ] `ShortLink` com campos: `journeyId`, `executionId`, `nodeId`, `channel`, `userId`, `metadata`
- [ ] `ClickEvent` com campos: `journeyId`, `executionId`, `nodeId`, `channel`
- [ ] `processRedirect` propaga campos do ShortLink para ClickEvent
- [ ] Analytics de jornada retorna `clickStats` por nó
- [ ] Analytics de campanha RCS retorna cliques por botão do carrossel

---

## Cenários de teste

- [ ] SMS com URL `https://bet.com/promo` na mensagem → chega no celular como `https://userin.ai/r/abc` → clique gera `ClickEvent` com `journeyId`
- [ ] SMS sem URL → mensagem enviada sem alteração, nenhum `ShortLink` criado
- [ ] SMS com 2 URLs → ambas substituídas por links encurtados distintos
- [ ] RCS carrossel com 3 cards, botão "Apostar" em cada → 3 `ShortLink`s com `cardIndex` 0, 1, 2
- [ ] Clique no botão do card 2 → `ClickEvent` com `metadata.cardIndex === 2`
- [ ] Editor RCS mostra URL original no input, badge "Link será encurtado"
- [ ] Toggle "Encurtar links" desativado → URL enviada crua
- [ ] Múltiplos cliques do mesmo usuário → `ClickEvent.clickCount` incrementa, `uniqueClicks` não
- [ ] Analytics da jornada: Nó "Enviar SMS" = 150 cliques (89 únicos)
- [ ] Analytics da campanha RCS: Card 1 = 45 cliques, Card 2 = 78, Card 3 = 23
- [ ] Load test: 10.000 links criados em batch → sem colisão de códigos base62

---

## Arquivos afetados

| Arquivo | Alteração |
| -- | -- |
| `backend/src/application/services/shortLinkService.js` | Novos métodos: `shortenUrlsInMessage()`, `shortenRcsButtonUrls()` |
| `backend/src/domain/models/ShortLink.js` | Novos campos + índices |
| `backend/src/domain/models/ClickEvent.js` | Novos campos herdados |
| `backend/src/interfaces/http/controllers/shortLinkController.js` | Propagar campos no redirect |
| `backend/src/journey-builder/engine/nodes/actions/SendSmsExecutor.js` | Chamar `shortenUrlsInMessage` na pipeline |
| `backend/src/journey-builder/engine/nodes/actions/SendRcsExecutor.js` | **Novo** — chamar `shortenRcsButtonUrls` |
| `backend/src/flow/consumers/CampaignWorker.js` | RCS path com `shortenRcsButtonUrls` |
| `backend/src/application/services/campaignService.js` | RCS sync path |
| `backend/src/journey-builder/services/journeyAnalyticsService.js` | `ClickEvent.aggregate` por jornada |
| `client/.../config/SendSmsConfig.tsx` | Toggle de encurtamento |
| `client/.../config/SendRcsConfig.tsx` | Badge "Link será encurtado" nos botões |

---

## 🎯 Priorização RICE — Score: 19.2

| Reach | Impact | Confidence | Effort | Score |
| -- | -- | -- | -- | -- |
| 10 | 3 (massive) | 80% | 1.25 meses | **19.2** |

**Justificativa:** Reach 10: todas as empresas enviam SMS/RCS e precisam metrificar cliques. Impacto massive (3): sem encurtador integrado, não há como medir ROI dos disparos — os dados de cliques das campanhas e jornadas ficam zerados, tornando impossível otimizar engajamento. Confidence 80%: encurtador já existe e funciona em campanhas SMS, a extensão para pipeline de disparo e RCS é incremental. Esforço 1.25 meses: métodos no shortLinkService + integração nos executors e workers + models + analytics frontend.

## Histórico de status
- Backlog (backlog): 2026-04-02T14:44:48.907Z → 2026-04-02T14:58:56.296Z
- To-do (unstarted): 2026-04-02T14:58:56.296Z → atual

## Relações
—

## Anexos
—
