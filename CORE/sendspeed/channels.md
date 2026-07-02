---
project_name: sendspeed-absorption
conversation_id: debate-o6-s2-2026-07-02
date: "2026-07-02"
emoji_rail: 📡 ➔ 📓 ➔ 🚀
domain: sendspeed
module: sendspeed_channels
source: linear-export
status: confirmed
---

# ➔ Canais de Envio SendSpeed

## SMS

- Envio padrão via `SmsService` / `SmsConsumer`
- Encurtamento de URLs em `shortenUrlsInMessage()` no momento do envio
- Lista fria via API (SEND-478): upload CSV/JSON → trigger em background

## RCS (SEND-429, SEND-452)

- Nó "Enviar RCS" no Journey Builder: seleção de template com busca + filtros + navegação para edição
- Template obrigatório para salvar o nó
- Preview fiel no editor com suporte a emojis (SEND-452)
- `shortenRcsButtonUrls()` para botões de carrossel (SEND-449 ⊂ SEND-446)

## WhatsApp — OTP via Infobip (SEND-505, SEND-508)

### Endpoint

```
POST /api/otp/whatsapp
```

Desacoplado de `/otp` SMS. Mesma auth (`AuthGuard`, `sms_otp`).

### Gate por cliente

```
otp_whatsapp=1 AND whatsapp_otp_supplier_id → OK
caso contrário → 403 / 422
```

### Fluxo

1. Gate de cliente
2. Extração do código OTP para o placeholder do template authentication Meta
3. Redis lock/dedupe por `userId + supplier`
4. 200 imediato com `trace_id` + dispatch background (3x retry)
5. `smsFailover` opcional por cliente

### Suppliers OTP

| ID | Supplier  | Status     |
|----|-----------|------------|
| 64 | Infobip   | Fase 1     |
| 65 | Sona      | Futuro     |

### Decisão de BSP (em aberto — SEND-508)

Meta Cloud API vs Infobip vs outro — define Fase 1 vs Fase 2.

### Zero regressão

`/otp` SMS existente não é alterado. Reutiliza tópicos Kafka `otp_sms_sent / otp_sms_failed`.
