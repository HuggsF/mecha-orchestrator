# SEND-502 — [callback-sms] Definir arquitetura: worker compartilhado com routing vs. worker-fasttrack dedicado

| Campo | Valor |
| -- | -- |
| Status | To-do (unstarted) |
| Prioridade | High |
| Responsável | andrei.garcia@externo.sendspeed.com |
| Time | Sendspeed |
| Projeto | — |
| Labels | Tech Story |
| Parent | SEND-488 |
| Criada | 2026-06-15T18:45:10.273Z por andrei.garcia@externo.sendspeed.com |
| Iniciada | — |
| Concluída | — |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-502-callback-sms-definir-arquitetura-worker-compartilhado-com |
| URL | https://linear.app/sendspeed/issue/SEND-502/callback-sms-definir-arquitetura-worker-compartilhado-com-routing-vs |

## Descrição

## Decisão: Opção A — Roteamento interno no worker-smartico existente

**Decisão tomada: worker compartilhado com routing interno.**

O consumer `worker-smartico` que roda no servidor hoje **permanece inalterado como processo**. Nenhum novo consumer é criado. O roteamento para Smartico ou FastTrack acontece dentro do `BatchProcessor`, com base no campo `crm` do `crm_postback`.

---

## Arquitetura atual (legado — Smartico only)

```
┌──────────────────────────────────────────────────────────────────────┐
│  Operadora (ex: Infobip, Sona)                                       │
│       ↓  status de entrega                                           │
│  webhook-api  →  fila STATUS_SMS                                     │
│                       ↓                                              │
│              worker-smartico (consumer)                              │
│                       ↓                                              │
│              BatchProcessor                                          │
│               ↓ lookup sms_sent                                      │
│               ↓ parse crm_postback  →  crm_callback_url             │
│               ↓ agrupar por URL                                      │
│               ↓                                                      │
│          SmarticoClient  →  POST  →  Smartico CRM                   │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Nova arquitetura (multi-CRM — Smartico + FastTrack)

```
┌──────────────────────────────────────────────────────────────────────┐
│  Operadora (ex: Infobip, Sona)                                       │
│       ↓  status de entrega                                           │
│  webhook-api  →  sms_sent  ←── crm_postback com campo "crm" novo    │
│                   ↓                                                  │
│              fila STATUS_SMS  (mesma fila de hoje)                   │
│                   ↓                                                  │
│         worker-smartico  ◄── MESMO CONSUMER, MESMO PROCESSO         │
│                   ↓                                                  │
│            BatchProcessor                                            │
│               ↓ lookup sms_sent                                      │
│               ↓ parseCrmPostback()  ←── utilitário centralizado      │
│               ↓                                                      │
│         extrai crm_type  (default: "smartico" se campo ausente)      │
│                   ↓                                                  │
│       ┌───────────┴────────────┐                                     │
│       │                        │                                     │
│  crm="smartico"          crm="fasttrack"                             │
│  (ou ausente = legado)                                               │
│       │                        │                                     │
│       ↓                        ↓                                     │
│  SmarticoClient          FastTrackClient  ◄── NOVO                  │
│  (inalterado)            + api_key como query param                  │
│       │                        │                                     │
│       ↓                        ↓                                     │
│  Smartico CRM            FastTrack CRM                               │
│  (inalterado)            (novo)                                      │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Fluxo worker-analysis (fallback Sona por phone) — também multi-CRM

```
┌──────────────────────────────────────────────────────────────────────┐
│  fila STATUS_ANALYSIS  (mensagens não encontradas por sms_id)        │
│         ↓                                                            │
│    worker-analysis  (consumer existente, inalterado como processo)   │
│         ↓                                                            │
│    SonaMessageProcessor                                              │
│         ↓ lookup por phone                                           │
│         ↓ parseCrmPostback()  →  crm_type                           │
│         ↓                                                            │
│    ┌────┴────────────┐                                               │
│    ↓                 ↓                                               │
│ Smartico          FastTrack                                          │
│ (inalterado)      (novo)                                             │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Por que Opção A e não worker dedicado?

| Critério | Opção A (escolhida) | Opção B (descartada) |
| -- | -- | -- |
| Consumers no servidor | **0 novos** | +1 novo processo |
| Impacto no Smartico | **Zero** — path inalterado | Zero, mas infra mais complexa |
| Fila STATUS_SMS | Mesma, sem mudança | Precisaria de split ou roteamento antes |
| Circuit breaker | Por instância de client (já isolado) | Totalmente independente |
| Deploy | Apenas rebuild + redeploy do worker-smartico | Novo processo para orquestrar |
| Rollback FastTrack | Remove FastTrackClient, rebuild | Remove worker inteiro |

**Conclusão:** A fila STATUS_SMS já mistura mensagens de todos os clientes (Smartico e futuros). Criar um segundo consumer para FastTrack exigiria dividir a fila por CRM *antes* do worker, o que seria mais invasivo do que o routing interno. A Opção A é a mudança de menor superfície.

---

## Garantias de retrocompatibilidade

* `crm_postback` sem campo `crm` → `parseCrmPostback()` retorna `crm_type = 'smartico'` (default)
* Todos os registros Smartico existentes continuam funcionando sem nenhuma alteração
* `SmarticoClient` não é modificado — apenas chamado via interface `ICrmCallbackClient`
* O processo `worker-smartico` no servidor não muda de nome, nem de fila, nem de configuração

## Histórico de status
- Backlog (backlog): 2026-06-15T18:45:10.273Z → 2026-06-17T12:23:31.342Z
- To-do (unstarted): 2026-06-17T12:23:31.342Z → atual

## Relações
—

## Anexos
—
