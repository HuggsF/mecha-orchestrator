# SEND-495 — [api-legada] Adicionar campo `crm` ao crm_postback — HandleApi, ValidationService e SmsService

| Campo | Valor |
| -- | -- |
| Status | To-do (unstarted) |
| Prioridade | High |
| Responsável | andrei.garcia@externo.sendspeed.com |
| Time | Sendspeed |
| Projeto | — |
| Labels | — |
| Parent | SEND-488 |
| Criada | 2026-06-15T18:30:22.838Z por andrei.garcia@externo.sendspeed.com |
| Iniciada | — |
| Concluída | — |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-495-api-legada-adicionar-campo-crm-ao-crm_postback-handleapi |
| URL | https://linear.app/sendspeed/issue/SEND-495/api-legada-adicionar-campo-crm-ao-crm-postback-handleapi |

## Descrição

## Objetivo

Adicionar o campo `crm` ao JSON `crm_postback` em todos os pontos de montagem da api-legada, garantindo retrocompatibilidade total com o fluxo Smartico existente e preparando a estrutura para receber requisições da Fasttrack.

## Contexto

A api-legada (`nodejs-api-v02`) monta e salva o `crm_postback` em vários pontos, mas **nenhum deles inclui o campo** `crm` — identificador de roteamento introduzido no contrato multi-CRM definido em SEND-488.

Sem esse campo, o futuro consumer de postback (SEND-???) não conseguirá distinguir se deve fazer o POST para Smartico ou Fasttrack.

---

## Padrão interno a seguir (imutável — definido em SEND-488)

```json
{
  "crm": "smartico" | "fasttrack",
  "callback_url": "https://...",
  "crm_message_id": "abc-123",
  "api_key": "optional"
}
```

> ⚠️ **Nota de nomenclatura:** a api-legada usa nomes de campos internos ligeiramente diferentes do padrão sms-api (`crm_callback_url` em vez de `callback_url`, `crm_api_key` em vez de `api_key`). Esta task **não renomeia** esses campos internos — apenas **adiciona** o campo `crm`. A unificação de nomes pode ser feita numa task separada se necessário.

---

## Regra de retrocompatibilidade

* `crm_postback` sem campo `crm` → assume `"smartico"` em todo o pipeline
* Todos os registros existentes no banco sem `crm` → consumer lê como Smartico por fallback

---

## Arquivos a alterar

### 1. `src/handlers/HandleApi.js` — linhas 103–107

**Problema:** o objeto `crm_postback` montado na entrada da requisição não inclui `crm`.

**Antes:**

```js
crm_postback: {
    crm_message_id:   req.body.ext_id ? req.body.ext_id : "",
    crm_callback_url: crmCallbackUrl,
    crm_api_key:      crmApiKey,
}
```

**Depois:**

```js
crm_postback: {
    crm:              req.body.crm ?? req.body.crm_postback?.crm ?? 'smartico',
    crm_message_id:   req.body.ext_id ? req.body.ext_id : "",
    crm_callback_url: crmCallbackUrl,
    crm_api_key:      crmApiKey,
}
```

> O campo `crm` deve aceitar valor vindo direto no body (`req.body.crm`) ou aninhado dentro de `crm_postback` (`req.body.crm_postback?.crm`), com default `'smartico'`.

---

### 2. `src/services/ValidationSerice.js` — linha 111

**Problema:** o schema Zod de `validateApiPayload` não declara o campo `crm` dentro do objeto `crm_postback`.

**Antes:**

```js
crm_postback: z.object({
    crm_message_id:   z.string().max(36).optional(),
    crm_callback_url: z.string().max(255).optional(),
    crm_api_key:      z.string().max(255).optional(),
}).optional()
```

**Depois:**

```js
crm_postback: z.object({
    crm:              z.enum(['smartico', 'fasttrack']).optional(),
    crm_message_id:   z.string().max(36).optional(),
    crm_callback_url: z.string().max(255).optional(),
    crm_api_key:      z.string().max(255).optional(),
}).optional()
```

---

### 3. `src/services/SmsService.js` — linha 24

**Problema:** `insertSmsPayload()` monta o objeto `crmPostbackJson` sem o campo `crm`.

**Antes:**

```js
const crmPostbackJson = {
    crm_message_id:   crmMessageId,
    crm_callback_url: crmCallbackUrl,
    crm_api_key:      crmApiKey
};
```

**Depois:**

```js
const crmPostbackJson = {
    crm:              payload.crm_postback?.crm ?? 'smartico',
    crm_message_id:   crmMessageId,
    crm_callback_url: crmCallbackUrl,
    crm_api_key:      crmApiKey
};
```

---

### 4. `src/services/SmsService.js` — linha 78

**Problema:** `insertSmsv2Payload()` monta o fallback de `crmPostbackJson` sem o campo `crm`.

**Antes:**

```js
crmPostbackJson = JSON.stringify({
    crm_message_id:   payload.ext_id || null,
    crm_callback_url: payload.crm_postback_url || null,
    crm_api_key:      payload.crm_api_key || null,
});
```

**Depois:**

```js
crmPostbackJson = JSON.stringify({
    crm:              'smartico',
    crm_message_id:   payload.ext_id || null,
    crm_callback_url: payload.crm_postback_url || null,
    crm_api_key:      payload.crm_api_key || null,
});
```

> Neste fluxo (v2/CSV), o CRM é sempre Smartico — a Fasttrack não usa o endpoint v2.

---

### 5. `src/consumers/SmsConsumer.js` — linha 76

**Problema:** `saveSms()` normaliza o `crm_postback` do payload da fila mas não garante a presença do campo `crm` no JSON final persistido.

**Ajuste:** após a normalização existente, garantir que o objeto parseado inclui `crm` antes de re-serializar:

```js
// Após o bloco de normalização existente (linha ~91)
const parsed = JSON.parse(crmPostbackJson);
if (!parsed.crm) parsed.crm = 'smartico';
crmPostbackJson = JSON.stringify(parsed);
```

---

## ⚠️ Ponto em aberto — campos da Fasttrack

Não temos a documentação da Fasttrack. Os campos que eles enviarão na requisição de disparo (equivalentes a `crm_callback_url`, `crm_api_key`, `crm_message_id`) ainda não são conhecidos.

Quando a doc chegar, será necessário:

* Mapear os campos recebidos da Fasttrack para os internos da api-legada
* Adicionar normalização análoga à que existe no sms-api (SEND-490)

Por ora, esta task assume que a Fasttrack enviará o `crm_postback` já estruturado no formato interno (com `crm: "fasttrack"`), o que poderá ser ajustado após a documentação.

_(Referências a SEND-488 e SEND-490 acima eram embeds `<issue>` de cross-reference no Linear.)_

---

## Critérios de aceite

- [ ] Requisição Smartico existente: `crm_postback` salvo no banco contém `crm: "smartico"` — comportamento inalterado
- [ ] Requisição com `crm: "fasttrack"` no body: campo `crm` propagado e salvo corretamente
- [ ] Registros sem `crm` no banco: fallback para `"smartico"` aplicado nos consumers
- [ ] Schema Zod rejeita valores de `crm` fora do enum `['smartico', 'fasttrack']`

## Histórico de status
- Backlog (backlog): 2026-06-15T18:30:22.838Z → 2026-06-17T12:22:58.248Z
- To-do (unstarted): 2026-06-17T12:22:58.248Z → atual

## Relações
- Blocks: SEND-496 — [api-legada] SmsConsumer — implementar forwardCrmPostback com roteamento Smartico/Fasttrack
- Related to: SEND-490 — [sms-api] Adicionar campo `crm` ao crm_postback nos DTOs e builders

## Anexos
—
