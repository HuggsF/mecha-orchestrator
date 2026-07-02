---
project_name: sendspeed-absorption
conversation_id: debate-o6-s2-2026-07-02
date: "2026-07-02"
emoji_rail: 📡 ➔ 🧬 ➔ 📓
domain: sendspeed
module: sendspeed_catalog
source: linear-export
status: confirmed
---

# ➔ Contratos e Decisões Abertas SendSpeed

## Contratos confirmados

### crm_postback (multi-CRM)

```typescript
interface CrmPostback {
  crm: "smartico" | "fasttrack";  // ausência = "smartico"
  crm_message_id: string;
  callback_url: string;           // ver nota SEND-498
  api_key: string;                // [REDACTED em produção]
}
```

### SmsSentInfo (SEND-498)

```typescript
interface SmsSentInfo {
  messageId: string;
  phone: string;
  crm: CrmType;
  sentAt: Date;
  journeyId?: string;
  executionId?: string;
  nodeId?: string;
}
```

### Redis key parametrizada (SEND-491)

```
crm_callback:client:{userId}:{crm}:{product}
```

## Decisões em aberto (gaps confirmados)

| Gap                          | Bloqueado por  | Status         |
|------------------------------|----------------|----------------|
| Auth + payload FastTrack     | SEND-504       | `blocked`      |
| BSP WhatsApp (Infobip/Meta)  | SEND-508       | `pending`      |
| `callback_url` vs `crm_callback_url` | SEND-498 | `contradictory` |
| FastTrack discovery          | SEND-511       | `blocked`      |
| NGX eventos UI (spike)       | SEND-517       | `started`      |
| Worker compartilhado vs dedicado | SEND-502   | `decided` (Opção A) |

## Nomenclatura (SEND-498)

Discrepância documentada: alguns services usam `callback_url`, outros `crm_callback_url`. Padrão canônico = `callback_url` até resolução formal.

## FastTrack — status `pending_fasttrack_doc`

Toda tool/contrato que depende da documentação FastTrack carrega `pending_fasttrack_doc: true`.
Nunca servir como fato — sempre como `status: blocked, blocked_by: ["SEND-504"]`.
