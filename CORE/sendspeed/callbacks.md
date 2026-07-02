---
project_name: sendspeed-absorption
conversation_id: debate-o6-s2-2026-07-02
date: "2026-07-02"
emoji_rail: 📡 ➔ 🛡️ ➔ 🚀
domain: sendspeed
module: sendspeed_callbacks
source: linear-export
status: confirmed
---

# ➔ Callbacks Multi-CRM (Smartico + FastTrack)

## Contrato crm_postback

Campo `crm` obrigatório no payload salvo em `sms.crm_postback`. Ausência = `"smartico"` (retrocompatibilidade inegociável). Valores válidos: `"smartico"` | `"fasttrack"`.

```json
{
  "crm": "smartico",
  "crm_message_id": "...",
  "callback_url": "https://...",
  "api_key": "[REDACTED]"
}
```

> ⚠️ `callback_url` vs `crm_callback_url` — discrepância de nomenclatura documentada em SEND-498. Use `callback_url` até resolução.

## De-para de status por CRM (SEND-483)

| Status interno SendSpeed | Smartico        | FastTrack (pending doc) |
|--------------------------|-----------------|-------------------------|
| Enviado                  | `sent`          | `TODO(fasttrack-doc)`   |
| Entregue                 | `delivered`     | `TODO(fasttrack-doc)`   |
| Falha                    | `failed`        | `TODO(fasttrack-doc)`   |
| Rejeitado                | `rejected`      | `TODO(fasttrack-doc)`   |
| Pendente (SEND-479)      | `pending`       | `TODO(fasttrack-doc)`   |

**Invariante de analytics:** `Enviado = Falha + Rejeitado + Pendente`

## Pipeline de callbacks (SEND-502)

Decisão ratificada: **Opção A** — routing interno no `BatchProcessor/RcsCallbackService`, zero consumers novos.

| Serviço        | Responsabilidade                                     | Issues        |
|----------------|------------------------------------------------------|---------------|
| `sms-api`      | Monta `crm_postback` nos DTOs/builders, consumers RCS/SMS fazem `forwardCrmPostback` | SEND-490..493 |
| `api-legada`   | HandleApi + ValidationService + SmsConsumer roteamento Smartico/FastTrack | SEND-495, 496 |
| `callback-sms` | Parsing único do `crm_postback`, CallbackGrouper/BatchProcessor por CRM | SEND-497, 498, 500, 502 |

## Chaves Redis parametrizadas (SEND-491)

```
crm_callback:client:{userId}:{crm}:{product}
```

Default `crm = smartico` quando ausente — zero regressão no fluxo legado.

## Adapter FastTrack (bloqueado)

- `FastTrackClient` via `ICrmCallbackClient` (SEND-499)
- Auth/payload/retry: `TODO(fasttrack-doc)` — aguarda SEND-504
- Rollback = remover `FastTrackClient` do registry
