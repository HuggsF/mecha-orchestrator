# SEND-500 — [callback-sms] Atualizar CallbackGrouper e BatchProcessor para roteamento por CRM

| Campo | Valor |
| -- | -- |
| Status | To-do (unstarted) |
| Prioridade | High |
| Responsável | andrei.garcia@externo.sendspeed.com |
| Time | Sendspeed |
| Projeto | — |
| Labels | Tech Story |
| Parent | SEND-488 |
| Criada | 2026-06-15T18:44:40.685Z por andrei.garcia@externo.sendspeed.com |
| Iniciada | — |
| Concluída | — |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-500-callback-sms-atualizar-callbackgrouper-e-batchprocessor-para |
| URL | https://linear.app/sendspeed/issue/SEND-500/callback-sms-atualizar-callbackgrouper-e-batchprocessor-para |

## Descrição

## Contexto

O fluxo principal de despacho de callbacks passa por:

1. `SmsSentLookupService` → popula `SmsSentInfo` com `crm_callback_url`
2. `CallbackGrouper` → agrupa mensagens por `crm_callback_url`
3. `BatchProcessor.handleCallbackGroup()` → faz POST para cada URL via `SmarticoClient`

Com multi-CRM, o `BatchProcessor` precisa saber **qual cliente usar** para cada grupo, e o `CallbackGrouper` precisa propagar o `crm_type`.

## Arquivos impactados

* `src/workers/smartico/CallbackGrouper.ts`
* `src/workers/smartico/BatchProcessor.ts`
* `src/workers/smartico/WorkerSmartico.ts` (composição de dependências)

## O que fazer

### `CallbackGrouper`

A chave de agrupamento precisa incluir o `crm_type`, ou os grupos precisam carregar o `crm_type` junto:

```ts
export interface GroupKey {
  url: string;
  crm_type: CrmType;
  api_key: string | null;
}

export interface GroupedCallbacks {
  groups: Map<string, { key: GroupKey; records: EnrichedRecord[] }>;
  // ...
}
```

### `EnrichedRecord`

Adicionar `crm_type`, `api_key` e `crm_message_id` ao `EnrichedRecord` em `CallbackGrouper.ts`.

### `BatchProcessor.handleCallbackGroup()`

Recebe `GroupKey` e despacha para o cliente correto:

```ts
private getClient(crmType: CrmType): ICrmCallbackClient {
  if (crmType === 'fasttrack') return this.fasttrackClient;
  return this.smarticoClient; // default + retrocompatível
}
```

### Retrocompatibilidade

`crm_type` ausente ou `undefined` no `SmsSentInfo` → trata como `'smartico'`. Nenhum registro Smartico existente deve ser afetado.

## Critério de aceite

* `CallbackGrouper` propaga `crm_type` e `api_key` nos grupos
* `BatchProcessor` usa `ICrmCallbackClient` via dispatcher, não `SmarticoClient` diretamente
* Testes em `BatchProcessor.test.ts` cobrindo: roteamento para Smartico, roteamento para FastTrack, ausência de `crm` defaultando para Smartico
* Zero regressão no fluxo Smartico existente

## Histórico de status
- Backlog (backlog): 2026-06-15T18:44:40.685Z → 2026-06-17T12:23:54.399Z
- To-do (unstarted): 2026-06-17T12:23:54.399Z → atual

## Relações
- Blocked by: SEND-499 — [callback-sms] Implementar FastTrackClient — cliente HTTP para callbacks FastTrack
- Blocked by: SEND-497 — [callback-sms] Centralizar parsing do crm_postback em utilitário único
- Blocked by: SEND-498 — [callback-sms] Atualizar tipos CrmPostback e SmsSentInfo para contrato multi-CRM

## Anexos
—
