# SEND-488 — Integração com CRM Fasttrack

| Campo | Valor |
| -- | -- |
| Status | To-do (unstarted) |
| Prioridade | High |
| Responsável | andrei.garcia@externo.sendspeed.com |
| Time | Sendspeed |
| Projeto | — |
| Labels | — |
| Parent | — |
| Criada | 2026-06-15T17:38:53.966Z por andrei.garcia@externo.sendspeed.com |
| Iniciada | — |
| Concluída | — |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-488-integracao-com-crm-fasttrack |
| URL | https://linear.app/sendspeed/issue/SEND-488/integracao-com-crm-fasttrack |

## Descrição

Integrar todo fluxo Sendspeed com CRM Fasttrack.

Esta é a história de usuário macro que agrupa todas as tarefas técnicas necessárias para suportar o CRM Fasttrack na plataforma Sendspeed.

---

## Padrão `crm_postback` — Contrato oficial multi-CRM

### O que é o `crm_postback`

Campo JSON salvo na coluna `sms.crm_postback` no momento do recebimento da requisição. Guarda os dados necessários para que os consumers façam o POST de status de entrega de volta ao CRM após o envio.

### Estrutura atual (Smartico — legado)

```json
{
  "callback_url": "https://gateway.smartico.ai/...",
  "crm_message_id": "abc-123",
  "api_key": "optional-key"
}
```

### Estrutura padronizada (multi-CRM — a partir dessa tarefa)

```json
{
  "crm": "smartico",
  "callback_url": "https://gateway.smartico.ai/...",
  "crm_message_id": "abc-123",
  "api_key": "optional-key"
}
```

O campo `crm` é a **chave de roteamento** que define para qual CRM o postback será direcionado.

* Valores aceitos: `"smartico"` | `"fasttrack"`
* Ausência do campo → comportamento legado: assume `"smartico"` (retrocompatibilidade total)

### Campos obrigatórios / opcionais

| Campo | Tipo | Obrigatoriedade | Descrição |
| -- | -- | -- | -- |
| `crm` | string | **Obrigatório (novo)** | Identificador do CRM: `"smartico"` ou `"fasttrack"` |
| `callback_url` | string (URL) | **Obrigatório** | URL onde faremos o POST de status |
| `crm_message_id` | string | Opcional | ID da mensagem no CRM para correlação |
| `api_key` | string | Opcional | Chave de API — appendada como `?api_key=` na URL |

### O que enviamos ao CRM (payload do POST de callback)

```
POST {callback_url}?api_key={api_key}
Content-Type: application/json

[{ "messageId": "<trace_id>", "status": "<crm_status>" }]
```

* `messageId` = `trace_id` da mensagem na plataforma Sendspeed
* `status` = status traduzido pelo de/para configurado no backoffice (ex: `delivered`, `failed`, `undelivered`)

O de/para é configurado por CRM + produto (RCS/SMS) + cliente (ou default do sistema), via tabela `crm_callback_status_mappings` e cache Redis.

### Como a Fasttrack deve integrar

A Fasttrack deve enviar na requisição de disparo os campos:

```json
{
  "crm_postback": {
    "crm": "fasttrack",
    "callback_url": "https://api.fasttrack.ai/webhook/sendspeed",
    "crm_message_id": "ft-msg-id-opcional",
    "api_key": "chave-opcional"
  }
}
```

Receberá de volta um POST com o mesmo formato acima quando o status de entrega chegar da operadora.

---

## Arquitetura do servidor — multi-CRM

```
┌──────────────────────────────────────────────────────────────────────┐
│  Operadora (Infobip, Sona, etc.)                                     │
│       ↓  status de entrega chega                                     │
│  webhook-api  →  sms_sent  ←── crm_postback inclui campo "crm"       │
│                   ↓                                                  │
│              fila STATUS_SMS  (mesma fila de hoje, sem mudança)      │
│                   ↓                                                  │
│         worker-smartico  ◄── MESMO CONSUMER E PROCESSO DO SERVIDOR  │
│                   ↓                                                  │
│            BatchProcessor                                            │
│               ↓ lookup sms_sent + parseCrmPostback()                 │
│               ↓                                                      │
│       extrai crm_type  (ausente = "smartico" por retrocompatibilidade)│
│                   ↓                                                  │
│       ┌───────────┴────────────┐                                     │
│       │                        │                                     │
│  crm="smartico"          crm="fasttrack"                             │
│  (legado — inalterado)    (novo)                                     │
│       │                        │                                     │
│       ↓                        ↓                                     │
│  SmarticoClient          FastTrackClient                             │
│  (inalterado)            (novo — mesmo interface)                    │
│       │                        │                                     │
│       ↓                        ↓                                     │
│  Smartico CRM  ✓          FastTrack CRM  ✓                          │
└──────────────────────────────────────────────────────────────────────┘
```

**Garantia:** todo registro sem campo `crm` no `crm_postback` segue o caminho Smartico idêntico ao de hoje. Zero impacto em clientes existentes.

---

## Sub-tasks técnicas [callback-sms]

| Issue | Título | Status |
| -- | -- | -- |
| SEND-497 | Centralizar parsing do crm_postback em utilitário único | Backlog |
| SEND-498 | Atualizar tipos CrmPostback e SmsSentInfo para multi-CRM | Backlog |
| SEND-499 | Implementar FastTrackClient | Backlog |
| SEND-500 | Atualizar CallbackGrouper e BatchProcessor para roteamento | Backlog |
| SEND-501 | Estender SonaMessageProcessor para FastTrack | Backlog |
| SEND-502 | Decisão arquitetural (esta task) | Backlog |
| SEND-503 | Atualizar SmarticoPayloadBuilder / criar CrmPayloadBuilder | Backlog |
| SEND-504 | ⏳ Aguardar documentação FastTrack | Backlog |

_(As referências acima eram embeds `<issue>` de cross-reference no Linear; convertidas para os identificadores das issues.)_

## Histórico de status
- To-do (unstarted): 2026-06-15T17:38:53.966Z → atual

## Relações
—

## Anexos
—
