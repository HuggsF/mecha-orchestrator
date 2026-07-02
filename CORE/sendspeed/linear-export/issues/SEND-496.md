# SEND-496 — [api-legada] SmsConsumer — implementar forwardCrmPostback com roteamento Smartico/Fasttrack

| Campo | Valor |
| -- | -- |
| Status | To-do (unstarted) |
| Prioridade | Medium |
| Responsável | andrei.garcia@externo.sendspeed.com |
| Time | Sendspeed |
| Projeto | — |
| Labels | — |
| Parent | SEND-488 |
| Criada | 2026-06-15T18:31:02.354Z por andrei.garcia@externo.sendspeed.com |
| Iniciada | — |
| Concluída | — |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-496-api-legada-smsconsumer-implementar-forwardcrmpostback-com |
| URL | https://linear.app/sendspeed/issue/SEND-496/api-legada-smsconsumer-implementar-forwardcrmpostback-com-roteamento |

## Descrição

## Objetivo

Criar o mecanismo de postback de CRM na api-legada: após o envio do SMS, ler o `crm_postback` salvo na tabela `sms` e disparar o POST de status de entrega ao CRM correto (Smartico ou Fasttrack).

## Contexto

A api-legada (`nodejs-api-v02`) **salva** o campo `crm_postback` na tabela `sms`, mas **nenhum consumer lê esse campo e dispara o POST de retorno ao CRM**. O ciclo está incompleto.

Confirmado pelo mapeamento do código: `SmsConsumer.js`, `SmsService.js` e `SmsRepository.js` apenas persistem o campo — não existe nenhum método `forwardCrmPostback` ou equivalente neste projeto.

No sms-api, o ciclo está completo apenas no fluxo RCS:

```
Infobip → Kafka → rcs-consumer → RcsCallbackService.forwardCrmPostback → POST CRM
```

No fluxo SMS (tanto sms-api quanto api-legada), o delivery receipt é processado pelo PHP cron — este serviço não recebe o webhook de entrega diretamente.

---

## Investigação necessária (pré-condição)

Antes de implementar, responder:

1. **Os delivery receipts de SMS da Infobip chegam a esta api via webhook HTTP?**
   * Se sim: qual endpoint? Existe já um handler ou precisa ser criado?
   * Se não: o PHP cron é o único receptor — o postback precisaria ser disparado a partir do PHP ou de um novo consumer dedicado
2. **Existe algum evento neste serviço que atualiza** `sms.status`**?**
   * Verificar se algum worker/consumer da api-legada processa atualizações de status de entrega
3. **Se o receipt não passa por aqui:** levantar proposta de arquitetura — criar endpoint de webhook SMS nesta api ou mover a responsabilidade do postback para o PHP.

---

## Implementação esperada (após investigação)

Criar no local adequado (consumer existente ou novo handler de webhook):

```js
async function forwardCrmPostback(traceId, deliveryStatus) {
    // 1. Buscar crm_postback e user_id da tabela sms
    const row = await db.query(
        'SELECT crm_postback, user_id FROM sms WHERE trace_id = ? LIMIT 1',
        [traceId]
    );
    if (!row || !row.crm_postback) return;

    // 2. Parsear — campo pode ser string JSON ou objeto
    const crmPostback = typeof row.crm_postback === 'string'
        ? JSON.parse(row.crm_postback)
        : row.crm_postback;

    // 3. Ler campo crm com fallback para retrocompatibilidade
    const crm = crmPostback.crm ?? 'smartico';

    // 4. Rotear por CRM
    if (crm === 'fasttrack') {
        await forwardFasttrackPostback(crmPostback, traceId, deliveryStatus);
    } else {
        await forwardSmarticoPostback(crmPostback, traceId, deliveryStatus);
    }
}
```

### `forwardSmarticoPostback` — comportamento já conhecido

```js
async function forwardSmarticoPostback(crmPostback, traceId, status) {
    const { crm_callback_url, crm_api_key, crm_message_id } = crmPostback;
    if (!crm_callback_url) return;

    const url = crm_api_key
        ? `${crm_callback_url}?api_key=${crm_api_key}`
        : crm_callback_url;

    await axios.post(url, [{ messageId: traceId, status }]);
}
```

### `forwardFasttrackPostback` — bloqueado até a doc chegar

```js
async function forwardFasttrackPostback(crmPostback, traceId, status) {
    // TODO: implementar após receber documentação da API de callback da Fasttrack.
    // Por enquanto suprime o POST e apenas loga para não perder o evento.
    console.warn('[CrmPostback][Fasttrack] postback suppressed — API doc pending', {
        traceId,
        status,
        crm_callback_url: crmPostback.crm_callback_url
    });
}
```

---

## ⚠️ Ponto em aberto — formato do POST para a Fasttrack

Não temos a documentação da API de callback da Fasttrack. Não sabemos ainda:

* Endpoint exato
* Formato do body esperado por eles
* Headers de autenticação (além do `api_key` em query string)
* Se o payload difere do padrão Smartico

`forwardFasttrackPostback` ficará suprimido (apenas log) até a documentação chegar.

---

## Mapeamento de status

O status enviado no POST (`delivered`, `failed`, etc.) deve seguir o de/para configurado por CRM + produto (SMS) no backoffice — tabela `crm_callback_status_mappings`.

**Verificar** se a api-legada tem acesso a essa tabela ou se o de/para precisa ser resolvido de outra forma (consulta direta ao banco ou via Redis cache como no sms-api).

---

## Dependências

* SEND-495 — campo `crm` precisa estar presente no `crm_postback` salvo no banco
* Documentação da API de callback da Fasttrack (para completar `forwardFasttrackPostback`)
* Definição de onde o delivery receipt SMS é recebido nesta api (investigação acima)

_(Referência a SEND-495 acima era embed `<issue>` de cross-reference no Linear.)_

---

## Critérios de aceite

- [ ] Investigação concluída e documentada: onde o receipt de entrega SMS chega na api-legada
- [ ] `forwardCrmPostback` chamado no evento correto de atualização de status
- [ ] Smartico: POST disparado com `[{ messageId, status }]` para `crm_callback_url?api_key=...`
- [ ] Fasttrack: log emitido, POST suprimido com `TODO` explícito até a doc chegar
- [ ] Registros sem campo `crm` no banco: tratados como Smartico (fallback)

## Histórico de status
- Backlog (backlog): 2026-06-15T18:31:02.354Z → 2026-06-17T12:22:49.772Z
- To-do (unstarted): 2026-06-17T12:22:49.772Z → atual

## Relações
- Blocked by: SEND-495 — [api-legada] Adicionar campo `crm` ao crm_postback — HandleApi, ValidationService e SmsService

## Anexos
—
