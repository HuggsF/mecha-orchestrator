# SEND-493 — [sms-api] Consumer SMS — implementar forwardCrmPostback equivalente ao fluxo RCS

| Campo | Valor |
| -- | -- |
| Status | To-do (unstarted) |
| Prioridade | Medium |
| Responsável | andrei.garcia@externo.sendspeed.com |
| Time | Sendspeed |
| Projeto | — |
| Labels | — |
| Parent | SEND-488 |
| Criada | 2026-06-15T17:59:49.802Z por andrei.garcia@externo.sendspeed.com |
| Iniciada | — |
| Concluída | — |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-493-sms-api-consumer-sms-implementar-forwardcrmpostback |
| URL | https://linear.app/sendspeed/issue/SEND-493/sms-api-consumer-sms-implementar-forwardcrmpostback-equivalente-ao |

## Descrição

## Objetivo

Criar o mecanismo de postback de CRM para o fluxo SMS puro, análogo ao que existe hoje apenas no fluxo RCS (`RcsCallbackService.forwardCrmPostback`).

## Contexto

Atualmente o campo `crm_postback` é salvo na tabela `sms` também para mensagens SMS (via `sms-dispatch.service.ts` e `sms.repository.ts`), mas **nenhum consumer lê esse campo e dispara o POST de retorno ao CRM** no fluxo SMS.

No fluxo RCS, o ciclo está completo:

```
Infobip → Kafka → rcs-consumer.service.ts → rcs-callback.service.ts → forwardCrmPostback → POST CRM
```

No fluxo SMS, o delivery receipt não passa por esse serviço — o PHP cron é responsável pelo `sms.status`. Precisamos investigar e definir onde encaixar o postback.

## Investigação necessária

1. **Verificar** se os delivery receipts de SMS da Infobip chegam via webhook HTTP a este serviço ou somente pelo PHP
2. **Identificar** se existe (ou precisa ser criado) um endpoint/consumer de webhook SMS neste serviço
3. **Mapear** qual evento dispara o `sms_sent` update no fluxo SMS

## Implementação esperada

Após a investigação, criar (no local adequado):

```ts
private async forwardCrmPostback(traceId: string, status: string): Promise<void> {
  // Mesmo padrão do RcsCallbackService:
  // 1. SELECT crm_postback, user_id FROM sms WHERE trace_id = ?
  // 2. parse crm_postback
  // 3. leitura do campo crm → dispatch Smartico ou Fasttrack
  // 4. resolveForMessage(userId, status, 'SMS', crm)
  // 5. POST para callback_url
}
```

## Dependências

* Task `CrmCallbackConfigService — parametrizar CRM` (para suporte ao `product = 'SMS'`)
* Task `RcsCallbackService — roteamento Smartico/Fasttrack` (reaproveitar ou extrair helpers de HTTP POST e resolução)

## Nota

Se o delivery receipt SMS não passar por este serviço, esta task deve levantar a proposta de arquitetura para que passe — ou documentar por que o postback SMS não é viável sem alteração de infra.

## Histórico de status
- Backlog (backlog): 2026-06-15T17:59:49.802Z → 2026-06-17T12:22:43.853Z
- To-do (unstarted): 2026-06-17T12:22:43.853Z → atual

## Relações
—

## Anexos
—
