# SEND-498 — [callback-sms] Atualizar tipos CrmPostback e SmsSentInfo para contrato multi-CRM

| Campo | Valor |
| -- | -- |
| Status | To-do (unstarted) |
| Prioridade | High |
| Responsável | andrei.garcia@externo.sendspeed.com |
| Time | Sendspeed |
| Projeto | — |
| Labels | Tech Story |
| Parent | SEND-488 |
| Criada | 2026-06-15T18:44:10.304Z por andrei.garcia@externo.sendspeed.com |
| Iniciada | — |
| Concluída | — |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-498-callback-sms-atualizar-tipos-crmpostback-e-smssentinfo-para |
| URL | https://linear.app/sendspeed/issue/SEND-498/callback-sms-atualizar-tipos-crmpostback-e-smssentinfo-para-contrato |

## Descrição

## Contexto

O contrato oficial multi-CRM definido em SEND-488 introduz novos campos no `crm_postback`:

```json
{
  "crm": "fasttrack",
  "callback_url": "https://api.fasttrack.ai/webhook/...",
  "crm_message_id": "ft-msg-opcional",
  "api_key": "chave-opcional"
}
```

O código atual em `src/types/domain.ts` só conhece `crm_callback_url` (sem o campo `crm`, sem `api_key`, sem `crm_message_id`).

## ⚠️ Discrepância a resolver

O spec de SEND-488 usa `callback_url`, mas o código atual lê `crm_callback_url` (ver `SmsSentLookupService:86`, testes em `BatchProcessor.test.ts:127`). Antes de implementar, alinhar com o time qual é o nome canônico:

* **Opção A**: migrar para `callback_url` (breaking change — requer atualizar todas as integrações existentes)
* **Opção B**: manter `crm_callback_url` no código e mapear no parser

## O que fazer

### `src/types/domain.ts`

```ts
export type CrmType = 'smartico' | 'fasttrack';

export interface CrmPostback {
  crm?: CrmType;             // ausente → retrocompatível com smartico
  callback_url?: string;     // novo nome canônico (alinhar com o time)
  crm_callback_url?: string; // legado — manter parse enquanto houver dados antigos
  crm_message_id?: string;
  api_key?: string;
  [key: string]: unknown;
}
```

### `src/types/domain.ts` — `SmsSentInfo`

Adicionar campos derivados do parse:

```ts
export interface SmsSentInfo {
  trace_id: string | null;
  crm_type: CrmType;           // novo — derivado de crm_postback.crm, default 'smartico'
  crm_callback_url: string | null;
  crm_message_id: string | null; // novo
  api_key: string | null;        // novo
  body: string;
  user_id: string | null;
  supplier_status_lifecicle: string | null;
  supplier_status: string | null;
}
```

### `src/lib/parseCrmPostback.ts` (da task anterior)

Atualizar para extrair e normalizar todos os campos, retornando `SmsSentInfo` completo.

## Critério de aceite

* `CrmPostback` e `SmsSentInfo` atualizados com novos campos
* `parseCrmPostback` retorna `crm_type` defaultando para `'smartico'` quando `crm` está ausente
* Sem quebra em nenhum cenário Smartico existente
* Decisão sobre `callback_url` vs `crm_callback_url` documentada no PR

## Histórico de status
- Backlog (backlog): 2026-06-15T18:44:10.304Z → 2026-06-17T12:23:12.580Z
- To-do (unstarted): 2026-06-17T12:23:12.580Z → atual

## Relações
- Blocks: SEND-500 — [callback-sms] Atualizar CallbackGrouper e BatchProcessor para roteamento por CRM
- Blocked by: SEND-497 — [callback-sms] Centralizar parsing do crm_postback em utilitário único

## Anexos
—
