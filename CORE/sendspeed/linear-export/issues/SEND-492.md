# SEND-492 — [sms-api] RcsCallbackService — roteamento Smartico/Fasttrack no forwardCrmPostback

| Campo | Valor |
| -- | -- |
| Status | To-do (unstarted) |
| Prioridade | High |
| Responsável | andrei.garcia@externo.sendspeed.com |
| Time | Sendspeed |
| Projeto | — |
| Labels | — |
| Parent | SEND-488 |
| Criada | 2026-06-15T17:59:20.928Z por andrei.garcia@externo.sendspeed.com |
| Iniciada | — |
| Concluída | — |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-492-sms-api-rcscallbackservice-roteamento-smarticofasttrack-no |
| URL | https://linear.app/sendspeed/issue/SEND-492/sms-api-rcscallbackservice-roteamento-smarticofasttrack-no |

## Descrição

## Objetivo

Adaptar `RcsCallbackService.forwardCrmPostback()` para ler o campo `crm` do JSON e rotear o postback para o método correto (Smartico ou Fasttrack).

## Arquivo principal

`src/rcs/rcs-callback.service.ts`

## ⚠️ PONTO EM ABERTO — formato do POST para a Fasttrack

**Não temos a documentação da API de callback da Fasttrack.** Não sabemos ainda:

* Qual o endpoint exato
* Qual o formato do body esperado por eles
* Se há headers de autenticação adicionais além do `api_key`
* Se o payload difere do padrão Smartico

**A implementação de** `forwardFasttrackPostback()` **ficará bloqueada até recebermos essa documentação.**

O padrão Smartico atual seguirá inalterado para a Smartico. A Fasttrack terá seu próprio método quando a doc estiver disponível.

## Fluxo atual (apenas Smartico)

```
forwardCrmPostback(traceId, status, messageId)
  → SELECT crm_postback FROM sms WHERE trace_id = ?
  → parse JSON  →  crm = crmPostback.crm ?? 'smartico'
  → resolveForMessage(userId, status, 'RCS', 'smartico')
  → POST callback_url?api_key=... body: [{ messageId, status }]
```

## Fluxo esperado (multi-CRM, após receber doc Fasttrack)

```
forwardCrmPostback(traceId, status, messageId)
  → SELECT crm_postback FROM sms WHERE trace_id = ?
  → parse JSON  →  crm = crmPostback.crm ?? 'smartico'
  → if crm === 'fasttrack' → forwardFasttrackPostback(...)  ← TBD
  → else                   → forwardSmarticoPostback(...)   (extração do código atual)
```

## O que implementar agora

1. **Extrair** a lógica atual de POST do Smartico para `forwardSmarticoPostback(crmPostback, traceId, userId, status)` — sem mudança de comportamento
2. **Ler** o campo `crm` do JSON e fazer dispatch
3. **Criar** `forwardFasttrackPostback()` com `TODO` explícito, logando e suprimindo o POST até a doc chegar:

```ts
private async forwardFasttrackPostback(...): Promise<void> {
  // TODO: implementar após receber documentação da API de callback da Fasttrack.
  // Por enquanto suprime o POST e apenas loga.
  this.logger.warn('[RcsCallback][Fasttrack] postback suppressed — API doc pending', { traceId });
}
```

4. **Passar** `crm` para `resolveForMessage` (depende de SEND-491)

## Dependências

* SEND-491 `CrmCallbackConfigService` — parametrizar CRM
* Documentação da API de callback da Fasttrack (para completar `forwardFasttrackPostback`)

_(Referências a SEND-491 acima eram embeds `<issue>` de cross-reference no Linear.)_

## Histórico de status
- Backlog (backlog): 2026-06-15T17:59:20.928Z → 2026-06-17T12:23:58.889Z
- To-do (unstarted): 2026-06-17T12:23:58.889Z → atual

## Relações
—

## Anexos
—
