# SEND-499 — [callback-sms] Implementar FastTrackClient — cliente HTTP para callbacks FastTrack

| Campo | Valor |
| -- | -- |
| Status | To-do (unstarted) |
| Prioridade | High |
| Responsável | andrei.garcia@externo.sendspeed.com |
| Time | Sendspeed |
| Projeto | — |
| Labels | Tech Story |
| Parent | SEND-488 |
| Criada | 2026-06-15T18:44:26.412Z por andrei.garcia@externo.sendspeed.com |
| Iniciada | — |
| Concluída | — |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-499-callback-sms-implementar-fasttrackclient-cliente-http-para |
| URL | https://linear.app/sendspeed/issue/SEND-499/callback-sms-implementar-fasttrackclient-cliente-http-para-callbacks |

## Descrição

## Contexto

O cliente Smartico (`src/workers/smartico/SmarticoClient.ts`) faz POST para a URL de callback com payload `SmarticoItem[]`. O FastTrack precisa de um cliente equivalente, com suas particularidades de autenticação e payload.

**⚠️ Documentação FastTrack ainda não disponível.** Esta task estará parcialmente em aberto até o recebimento da doc oficial.

## O que já sabemos (SEND-488)

* Endpoint: `POST {callback_url}?api_key={api_key}`
* Payload (provisório — mesmo formato Smartico): `[{ "messageId": "<trace_id>", "status": "<crm_status>" }]`
* `api_key` é opcional — appendado como query param se presente

## O que fazer

### Criar `src/workers/fasttrack/FastTrackClient.ts`

```ts
export class FastTrackClient {
  async post(url: string, body: unknown[], apiKey?: string | null): Promise<unknown> {
    const finalUrl = apiKey ? `${url}?api_key=${encodeURIComponent(apiKey)}` : url;
    // POST com timeout configurável via FASTTRACK_TIMEOUT_MS
    // circuit breaker análogo ao SmarticoClient
  }
}
```

### Interface comum

Extrair interface `ICrmCallbackClient` em `src/interfaces/ICrmCallbackClient.ts` para que `SmarticoClient` e `FastTrackClient` sejam intercambiáveis:

```ts
export interface ICrmCallbackClient {
  post(url: string, body: unknown[], options?: { apiKey?: string | null }): Promise<unknown>;
}
```

### Variáveis de ambiente

Adicionar ao `.env.example`:

```
FASTTRACK_TIMEOUT_MS=60000
```

## Pendente (doc FastTrack)

- [ ] Confirmar formato exato do payload
- [ ] Confirmar campos de autenticação (bearer token? api_key? ambos?)
- [ ] Confirmar quais HTTP status codes indicam retry vs. falha permanente
- [ ] Confirmar estrutura da resposta esperada

## Critério de aceite

* `FastTrackClient` implementado com suporte a `api_key` como query param
* Interface `ICrmCallbackClient` extraída e `SmarticoClient` adaptado para implementá-la
* Testes unitários com mock HTTP para os cenários conhecidos
* Pontos pendentes de doc marcados com `TODO(fasttrack-doc)` no código

## Histórico de status
- Backlog (backlog): 2026-06-15T18:44:26.412Z → 2026-06-17T12:23:05.016Z
- To-do (unstarted): 2026-06-17T12:23:05.016Z → atual

## Relações
- Blocks: SEND-501 — [callback-sms] Estender SonaMessageProcessor para roteamento FastTrack no fallback por phone
- Blocks: SEND-500 — [callback-sms] Atualizar CallbackGrouper e BatchProcessor para roteamento por CRM
- Blocked by: SEND-504 — [callback-sms] ⏳ Aguardar documentação FastTrack — ajustar payload, auth e campos
- Blocked by: SEND-497 — [callback-sms] Centralizar parsing do crm_postback em utilitário único

## Anexos
—
