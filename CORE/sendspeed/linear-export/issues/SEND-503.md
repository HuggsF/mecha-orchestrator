# SEND-503 — [callback-sms] Atualizar SmarticoPayloadBuilder ou criar CrmPayloadBuilder por CRM

| Campo | Valor |
| -- | -- |
| Status | To-do (unstarted) |
| Prioridade | Medium |
| Responsável | andrei.garcia@externo.sendspeed.com |
| Time | Sendspeed |
| Projeto | — |
| Labels | Tech Story |
| Parent | SEND-488 |
| Criada | 2026-06-15T18:45:27.521Z por andrei.garcia@externo.sendspeed.com |
| Iniciada | — |
| Concluída | — |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-503-callback-sms-atualizar-smarticopayloadbuilder-ou-criar |
| URL | https://linear.app/sendspeed/issue/SEND-503/callback-sms-atualizar-smarticopayloadbuilder-ou-criar |

## Descrição

## Contexto

O `SmarticoPayloadBuilder` (`src/workers/smartico/SmarticoPayloadBuilder.ts`) constrói o array `SmarticoItem[]` com `{ messageId, status, user_phone? }`.

Hoje ambos os CRMs (Smartico e FastTrack) usam o mesmo formato de payload conforme SEND-488 (ref: https://linear.app/sendspeed/issue/SEND-488/integracao-com-crm-fasttrack). Mas o FastTrack pode vir a ter campos adicionais quando a documentação oficial chegar (ex: `crm_message_id`, campos de autenticação no body, formato diferente).

## O que fazer

### Se payload idêntico (confirmado pela doc FastTrack)

Renomear `SmarticoItem` para `CrmCallbackItem` e `SmarticoPayloadBuilder` para `CrmPayloadBuilder` — ambos os clientes usam o mesmo builder.

```ts
// src/types/queue-messages.ts
export interface CrmCallbackItem {
  messageId: string;
  status: string;
  user_phone?: string;
  crm_message_id?: string; // opcional — FastTrack pode usar
}
```

### Se payload diferente (pendente doc FastTrack)

Extrair interface `ICrmPayloadBuilder<T>` e criar `FastTrackPayloadBuilder` dedicado.

## Pendente (doc FastTrack)

- [ ] Confirmar se o payload FastTrack é idêntico ao Smartico
- [ ] Confirmar se `crm_message_id` deve aparecer no body do POST
- [ ] Confirmar se há campos obrigatórios adicionais

## Critério de aceite

* Decisão tomada após receber a doc FastTrack
* `SmarticoItem` / `SmarticoPayloadBuilder` renomeados ou mantidos, com a escolha documentada no PR
* Nenhuma regressão no payload enviado ao Smartico
* Testes unitários atualizados

## Histórico de status
- Backlog (backlog): 2026-06-15T18:45:27.521Z → 2026-06-17T12:22:30.746Z
- To-do (unstarted): 2026-06-17T12:22:30.746Z → atual

## Relações
- Blocked by: SEND-504 — [callback-sms] ⏳ Aguardar documentação FastTrack — ajustar payload, auth e campos

## Anexos
—
