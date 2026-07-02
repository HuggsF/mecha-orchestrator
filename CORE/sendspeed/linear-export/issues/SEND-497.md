# SEND-497 — [callback-sms] Centralizar parsing do crm_postback em utilitário único

| Campo | Valor |
| -- | -- |
| Status | To-do (unstarted) |
| Prioridade | High |
| Responsável | andrei.garcia@externo.sendspeed.com |
| Time | Sendspeed |
| Projeto | — |
| Labels | Tech Story |
| Parent | SEND-488 |
| Criada | 2026-06-15T18:43:55.269Z por andrei.garcia@externo.sendspeed.com |
| Iniciada | — |
| Concluída | — |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-497-callback-sms-centralizar-parsing-do-crm_postback-em |
| URL | https://linear.app/sendspeed/issue/SEND-497/callback-sms-centralizar-parsing-do-crm-postback-em-utilitario-unico |

## Descrição

## Contexto

A lógica de `JSON.parse(crm_postback)` + extração de `crm_callback_url` está **triplicada** no projeto `v01-webhook-api`:

* `src/workers/smartico/SmsSentLookupService.ts` → `rowToInfo()` (linhas 79–89)
* `src/lib/cache/RedisSmsSentCache.ts` → `rowToInfo()` (linhas 92–103)
* `src/workers/analysis/SonaMessageProcessor.ts` → `extractCrmUrl()` (linhas 173–183)

Toda vez que o contrato do `crm_postback` mudar (como agora com o campo `crm` do FastTrack), precisamos alterar nos três lugares.

## O que fazer

Criar `src/lib/parseCrmPostback.ts` — função pura que centraliza o parse:

```ts
import type { CrmPostback } from '../types/domain';

export function parseCrmPostback(raw: string | null): CrmPostback | null {
  if (!raw) return null;
  try {
    return typeof raw === 'string'
      ? (JSON.parse(raw) as CrmPostback)
      : raw;
  } catch {
    return null;
  }
}
```

Substituir as 3 implementações inline por chamadas a `parseCrmPostback()`.

## Critério de aceite

* Arquivo `src/lib/parseCrmPostback.ts` criado com função exportada
* `SmsSentLookupService`, `RedisSmsSentCache` e `SonaMessageProcessor` usando a função
* Testes unitários em `src/__tests__/lib/parseCrmPostback.test.ts` cobrindo: JSON válido, JSON inválido, null
* Comportamento idêntico ao atual (sem regressão no Smartico)

## Observação

Esta task é **prerequisito** para as demais tasks de roteamento multi-CRM — deve ser mergeada primeiro.

## Histórico de status
- Backlog (backlog): 2026-06-15T18:43:55.269Z → 2026-06-17T12:23:19.079Z
- To-do (unstarted): 2026-06-17T12:23:19.079Z → atual

## Relações
- Blocks: SEND-501 — [callback-sms] Estender SonaMessageProcessor para roteamento FastTrack no fallback por phone
- Blocks: SEND-500 — [callback-sms] Atualizar CallbackGrouper e BatchProcessor para roteamento por CRM
- Blocks: SEND-499 — [callback-sms] Implementar FastTrackClient — cliente HTTP para callbacks FastTrack
- Blocks: SEND-498 — [callback-sms] Atualizar tipos CrmPostback e SmsSentInfo para contrato multi-CRM

## Anexos
—
