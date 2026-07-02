# SEND-501 — [callback-sms] Estender SonaMessageProcessor para roteamento FastTrack no fallback por phone

| Campo | Valor |
| -- | -- |
| Status | To-do (unstarted) |
| Prioridade | High |
| Responsável | andrei.garcia@externo.sendspeed.com |
| Time | Sendspeed |
| Projeto | — |
| Labels | Tech Story |
| Parent | SEND-488 |
| Criada | 2026-06-15T18:44:56.947Z por andrei.garcia@externo.sendspeed.com |
| Iniciada | — |
| Concluída | — |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-501-callback-sms-estender-sonamessageprocessor-para-roteamento |
| URL | https://linear.app/sendspeed/issue/SEND-501/callback-sms-estender-sonamessageprocessor-para-roteamento-fasttrack |

## Descrição

## Contexto

O `SonaMessageProcessor` (`src/workers/analysis/SonaMessageProcessor.ts`) é o fallback do **worker-analysis** para mensagens Sona não encontradas em `sms_sent` pelo `sms_id`. Ele faz lookup por `phone` e, se encontrar, envia o callback diretamente.

Hoje ele chama `sendCallback()` sempre com lógica Smartico hardcoded (payload `[{ messageId, status }]`, client axios direto). Com multi-CRM, se o registro encontrado por phone for de um cliente FastTrack, o callback deve ir para o `FastTrackClient`.

## Arquivos impactados

* `src/workers/analysis/SonaMessageProcessor.ts`
* `src/workers/analysis/WorkerAnalysis.ts` (composição de dependências)

## O que fazer

### Substituir `extractCrmUrl()` pelo `parseCrmPostback()` centralizado

A função `extractCrmUrl()` (linha 173) deve ser removida e substituída pela chamada ao utilitário `parseCrmPostback()` que retorna o `CrmPostback` completo (incluindo `crm_type` e `api_key`).

### Injetar `ICrmCallbackClient` dispatcher

O `SonaMessageProcessor` deve receber um dispatcher (ou mapa de clientes) via construtor, assim como o `BatchProcessor`:

```ts
constructor(
  // ...dependências atuais...
  private readonly crmClients: Record<CrmType, ICrmCallbackClient>,
) {}
```

### `sendCallback()` — atualizar assinatura

```ts
private async sendCallback(
  postback: CrmPostback,
  found: SmsSentRow,
  record: AnalysisRecord,
  userId: string | null,
): Promise<void>
```

Usar `postback.crm ?? 'smartico'` para selecionar o cliente correto.

## Critério de aceite

* `SonaMessageProcessor` não usa mais axios diretamente para o callback — delega ao cliente correto via `ICrmCallbackClient`
* `extractCrmUrl()` removido — substituído por `parseCrmPostback()`
* Testes em `SonaMessageProcessor.test.ts` com cenários: callback Smartico, callback FastTrack, `crm` ausente defaultando para Smartico
* Audit log (`logCallbackAudit`) atualizado para logar o `crm_type` usado

## Histórico de status
- Backlog (backlog): 2026-06-15T18:44:56.947Z → 2026-06-17T12:23:48.670Z
- To-do (unstarted): 2026-06-17T12:23:48.670Z → atual

## Relações
- Blocked by: SEND-499 — [callback-sms] Implementar FastTrackClient — cliente HTTP para callbacks FastTrack
- Blocked by: SEND-497 — [callback-sms] Centralizar parsing do crm_postback em utilitário único

## Anexos
—
