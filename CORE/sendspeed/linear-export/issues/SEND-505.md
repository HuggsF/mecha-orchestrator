# SEND-505 — Implementar OTP Whatsapp Infobip

| Campo | Valor |
| -- | -- |
| Status | To-do (unstarted) |
| Prioridade | High |
| Responsável | andrei.garcia@externo.sendspeed.com |
| Time | Sendspeed |
| Projeto | — |
| Labels | — |
| Parent | — |
| Criada | 2026-06-15T21:37:43.258Z por andrei.garcia@externo.sendspeed.com |
| Iniciada | — |
| Concluída | — |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-505-implementar-otp-whatsapp-infobip |
| URL | https://linear.app/sendspeed/issue/SEND-505/implementar-otp-whatsapp-infobip |

## Descrição

## Objetivo

Criar um canal de envio OTP via WhatsApp usando a API de template da Infobip. Fluxo **dedicado e desacoplado**: endpoint próprio, gate de habilitação por cliente, supplier próprio resolvido dinamicamente, campanha própria — **sem tocar no fluxo SMS OTP existente** (`/otp`).

O design é preparado para **múltiplos suppliers de WhatsApp no futuro** (ex.: Infobip=64 hoje, Sona=65 amanhã). O sistema seleciona de qual supplier disparar com base no que está configurado no cliente.

Referência Infobip (template): [https://www.infobip.com/docs/api/channels/whatsapp/whatsapp-outbound-messages/whatsapp-template-message/send-whatsapp-template-message](<https://www.infobip.com/docs/api/channels/whatsapp/whatsapp-outbound-messages/whatsapp-template-message/send-whatsapp-template-message>)

---

## Endpoint

```
POST /api/otp/whatsapp
```

* Autenticação **idêntica** ao `/otp`: Bearer / `X-API-Key` / `?token=` (depreciado), via `AuthGuard`.
* Mesma checagem de canal: `assertAuthorizedRouteTokenProduct(req.authorized, 'sms_otp')`.
* **Mesmo body do** `/otp` — reusa `SendOtpDto` (`user_phone`, `txt`, `callback_url?`, `ext_id?`). Nenhum campo novo no contrato público.

---

## Gate de habilitação (tabela `users`)

Antes de despachar, consulta o cliente (raw SQL + cache Redis, espelhando `OtpPaymentService`):

| Coluna | Regra |
| -- | -- |
| `otp_whatsapp` | Precisa estar `= 1`. Caso contrário → **403** (não habilitado). |
| `whatsapp_otp_supplier_id` | Precisa estar preenchido (> 0). É o supplier id do WhatsApp do cliente (ex.: 64 = Infobip). Caso contrário → **403** (não configurado). |

Se `whatsapp_otp_supplier_id` estiver preenchido mas **não houver implementação registrada** para esse id (hoje só o 64) → **422** (supplier não implementado).

> Hoje só o id **64 (Infobip)** está implementado. Amanhã, ao implementar Sona (65), basta registrar no registry e setar 65 no cliente — o sistema passa a rotear para ele automaticamente.

---

## Tratamento do `txt`

O cliente envia o texto completo, ex.: `"ola seu cod de autenticar e 455566"`.

* **Código OTP** (`455566`) é extraído do texto → vai no **placeholder do template** padrão da Infobip.
* **Texto completo** vai no `smsFailover.text` (SMS de fallback da Infobip, caso o template WhatsApp não seja entregue).

---

## Supplier id e campanha

* O supplier usado em **todo** o fluxo (campanha + INSERT sms + dispatch) é o `whatsapp_otp_supplier_id` do cliente — **não** o `default_sms_supplier_id` do token.
* Campanha diária criada com `sms_supplier_id = whatsapp_otp_supplier_id`, seguindo a **mesma lógica do OTP** (cache Redis + lock distribuído + dedupe por dia SP), mas **escopada/keyada pelo supplier id do WhatsApp** para não colidir com a campanha SMS regular do dia.
  * Token de rota: reusa `RouteDailySmsCampaignService` com `routeId = whatsappSupplierId`.
  * Token legado: serviço dedicado keyado por `(userId, whatsappSupplierId, dia)`, com `created_at` incremental (estilo rota) para não colidir com a campanha SMS legada das 00:00:00.

---

## Callback

`notifyUrl` montado igual ao `/otp` (`INFOBIP_CALLBACK_API_HOST?trace_id=<traceId>`). O `callback_url` do cliente continua indo para `crm_postback` exatamente como no `/otp` (reusa `buildCrmPostback`).

---

## Payload Infobip (WhatsApp Template + failover)

```json
{
  "messages": [{
    "from": "<INFOBIP_WHATSAPP_FROM>",
    "to": "<user_phone>",
    "content": {
      "templateName": "<INFOBIP_WHATSAPP_OTP_TEMPLATE>",
      "templateData": { "body": { "placeholders": ["<codigo_extraido>"] } },
      "language": "<INFOBIP_WHATSAPP_OTP_LANGUAGE>"
    },
    "callbackData": "{\"sms_id\": <id>, \"trace_id\": \"<traceId>\"}",
    "notifyUrl": "<INFOBIP_CALLBACK_API_HOST>?trace_id=<traceId>",
    "smsFailover": {
      "from": "<INFOBIP_WHATSAPP_FAILOVER_SMS_FROM>",
      "text": "<texto_completo>"
    }
  }]
}
```

Resposta esperada da Infobip: `messages[0].messageId` + `messages[0].status.name` (+ `bulkId`).

---

## Novas variáveis de ambiente

```env
INFOBIP_SUPPLIER_WHATSAPP_ID=64
INFOBIP_API_WHATSAPP_TEMPLATE_HOST=https://<base>.api-us.infobip.com/whatsapp/1/message/template
INFOBIP_WHATSAPP_FROM=<numero_remetente_whatsapp>
INFOBIP_WHATSAPP_OTP_TEMPLATE=<nome_template_padrao>
INFOBIP_WHATSAPP_OTP_LANGUAGE=pt_BR
INFOBIP_WHATSAPP_FAILOVER_SMS_FROM=sendspeed
```

Auth Infobip e tópico de log reusam os do OTP (`INFOBIP_OPT_USER`/`INFOBIP_OPT_PASSWORD`, `KAFKA_TOPIC_OTP_SMS_LOG`). Eventos de status reusam `otp_sms_sent` / `otp_sms_failed`.

---

## Fluxo técnico

```
POST /api/otp/whatsapp
  → AuthGuard + assertAuthorizedRouteTokenProduct('sms_otp')
  → WhatsappOtpController.send()
  → WhatsappOtpDispatchService.dispatch()
      ├─ WhatsappOtpConfigService.resolve(userId)  [cache Redis]
      │     flag otp_whatsapp=1? supplier id preenchido? senão → 403
      ├─ WhatsappOtpSupplierRegistry.resolve(supplierId)  → senão 422
      ├─ ensureCampaign() com sms_supplier_id = whatsappSupplierId (rota | legado)
      ├─ OtpPaymentService.checkPayment()  [reuso]
      ├─ extrai código OTP do txt + sanitiza telefone/texto
      ├─ OtpSmsRepository.insertOtpSms()  → sms PENDING (sms_supplier_id = whatsapp)
      ├─ HTTP 200 imediato { ok, trace_id, sms_id, status: "PROCESSING" }
      └─ [background] supplier.send({ phone, code, fullText, smsId, traceId })
          ├─ monta template + smsFailover, 3x retry backoff
          ├─ sucesso → Kafka otp_sms_sent → consumer UPDATE sms SENT
          └─ falha  → UPDATE sms FAILED + Kafka otp_sms_failed
```

---

## Arquivos a criar

| Arquivo | Descrição |
| -- | -- |
| `src/otp/whatsapp-otp.controller.ts` | Rota `POST otp/whatsapp` (reusa `SendOtpDto`) |
| `src/otp/services/whatsapp-otp-dispatch.service.ts` | Orquestrador do fluxo WhatsApp |
| `src/otp/services/whatsapp-otp-config.service.ts` | Lê `otp_whatsapp` + `whatsapp_otp_supplier_id` (raw SQL + cache) |
| `src/otp/services/otp-code-extractor.service.ts` | Extrai o código numérico do `txt` |
| `src/otp/suppliers/whatsapp-otp-supplier.interface.ts` | Contrato de supplier WhatsApp (params: phone, code, fullText, smsId, traceId) |
| `src/otp/suppliers/whatsapp-otp-supplier.registry.ts` | Registry id → supplier (preparado p/ múltiplos) |
| `src/otp/suppliers/infobip-whatsapp-otp.supplier.ts` | Implementação Infobip (template + smsFailover) |
| `src/campaign/whatsapp-otp-daily-campaign.service.ts` | Campanha diária dedicada (rota + legado) keyada por supplier |

## Arquivos a modificar

| Arquivo | O que muda |
| -- | -- |
| `src/otp/otp.module.ts` | Registrar novos providers + controller |
| `src/campaign/campaign.module.ts` | Provider/export do novo campaign service |
| `src/campaign/campaign.repository.ts` | Find legado SMS escopado por supplier id |
| `src/users/entities/user.entity.ts` | Mapear colunas `otp_whatsapp` + `whatsapp_otp_supplier_id` |
| `.env` / `.env.example` | Novas variáveis |

---

## Critérios de aceite

- [ ] `POST /api/otp/whatsapp` autentica igual ao `/otp` e recebe o mesmo body (`SendOtpDto`)
- [ ] Cliente sem `otp_whatsapp=1` → 403; sem `whatsapp_otp_supplier_id` → 403
- [ ] `whatsapp_otp_supplier_id` sem implementação registrada → 422
- [ ] Código OTP extraído do `txt` vai no placeholder; texto completo vai no `smsFailover.text`
- [ ] Campanha diária criada com `sms_supplier_id = whatsapp_otp_supplier_id`, sem colidir com a campanha SMS regular
- [ ] `callback_url`/`notifyUrl` tratados igual ao `/otp`
- [ ] Kafka `otp_sms_sent` / `otp_sms_failed` reusados; consumer atualiza status corretamente
- [ ] Design permite plugar novo supplier (ex.: Sona=65) sem alterar o fluxo
- [ ] Fluxo SMS OTP existente (`/otp`) sem regressão
- [ ] Novas variáveis documentadas no `.env.example`

## Histórico de status
- To-do (unstarted): 2026-06-15T21:37:43.258Z → atual

## Relações
—

## Anexos
—
