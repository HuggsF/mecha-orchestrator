---
project_name: sendspeed-absorption
conversation_id: debate-o6-s2-2026-07-02
date: "2026-07-02"
emoji_rail: 📡 ➔ 🚀 ➔ 🗺️
domain: sendspeed
module: sendspeed_journeys
source: linear-export
status: confirmed
---

# ➔ Journey Engine SendSpeed

## SendSmsExecutor — integração real (SEND-391)

O Journey Backend executa envios via `SendSmsExecutor` com chamada à API real. Cada execução carrega `journeyId / executionId / nodeId / batchId / trace_id` para rastreabilidade ponta-a-ponta.

## Acionamento com array de entrada (SEND-477)

```
POST /journey/trigger
{
  "journey_id": "...",
  "entries": [{ "phone": "+55...", "attrs": {...} }]
}
```

Acionamento em lote — cada item do array vira uma execução independente com `batchId` compartilhado.

## Envio de lista fria via API com arquivo (SEND-478)

Upload de arquivo CSV/JSON com lista de contatos → trigger em background. Progresso consultável via `batchId`.

## Objetivos e atribuição (SEND-450)

- Meta definida por jornada: taxa de conversão, cliques, resgates
- Janela de atribuição: **24h last touch**
- `ShortLink/ClickEvent` ganham `journeyId / executionId / nodeId / channel / userId`

## Encurtador de links (SEND-446 ⊃ SEND-449)

> SEND-449 é sobreposição quase total do escopo RCS de SEND-446 — consolidar antes de implementar.

- `shortenUrlsInMessage()` no momento do envio (URL original preservada no editor)
- Não re-encurtar link já curto da plataforma
- `shortenRcsButtonUrls()` para botões de carrossel RCS

## Status "Pendente" em Mensageria (SEND-479)

Novo status intermediário `pending` entre disparo e entrega confirmada. Alimenta o invariante de analytics: `Enviado = Falha + Rejeitado + Pendente`.

## Journeys multi-agent MECHA

| Pipeline                              | Agentes                                                 |
|---------------------------------------|---------------------------------------------------------|
| `journey_recuperacao_cadastro_userin` | CatalogBot → IntegrationBot → JourneyBot → SmartFlowBot |
| `journey_callback_multicrm_fasttrack` | CatalogBot → CallbackBot → IntegrationBot → CallbackBot → SmartFlowBot |
| `journey_rcs_encurtador`              | CatalogBot → ChannelBot → JourneyBot → SmartFlowBot     |
| `journey_otp_whatsapp`                | CatalogBot → ChannelBot → IntegrationBot → SmartFlowBot |
