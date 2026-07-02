# SEND-491 — [sms-api] CrmCallbackConfigService — parametrizar CRM nas chaves Redis e queries DB

| Campo | Valor |
| -- | -- |
| Status | To-do (unstarted) |
| Prioridade | High |
| Responsável | andrei.garcia@externo.sendspeed.com |
| Time | Sendspeed |
| Projeto | — |
| Labels | — |
| Parent | SEND-488 |
| Criada | 2026-06-15T17:59:14.625Z por andrei.garcia@externo.sendspeed.com |
| Iniciada | — |
| Concluída | — |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-491-sms-api-crmcallbackconfigservice-parametrizar-crm-nas-chaves |
| URL | https://linear.app/sendspeed/issue/SEND-491/sms-api-crmcallbackconfigservice-parametrizar-crm-nas-chaves-redis-e |

## Descrição

## Objetivo

Remover o hardcode `'smartico'` do `CrmCallbackConfigService` e parametrizar o CRM como argumento, para que as chaves Redis e queries DB funcionem tanto para Smartico quanto para Fasttrack.

## Arquivo principal

`src/crm-callback/crm-callback-config.service.ts`

## Problema atual

Todos os métodos usam `'smartico'` hardcoded:

```ts
// Redis key — hardcoded
const key = `crm_callback:client:${userId}:smartico:${product}`;
const key = `crm_callback:default:smartico:${product}`;

// DB query — hardcoded
AND m.crm = 'smartico'
```

Isso impede que o sistema leia configurações de de/para para a Fasttrack.

## Alterações necessárias

### Assinatura dos métodos (adicionar parâmetro `crm`)

```ts
// Antes
resolveForMessage(userId, internalStatus, product)
getClientMap(userId, product)
getDefaultMap(product)

// Depois
resolveForMessage(userId, internalStatus, product, crm = 'smartico')
getClientMap(userId, product, crm = 'smartico')
getDefaultMap(product, crm = 'smartico')
```

### Chaves Redis

```ts
// Antes
`crm_callback:client:${userId}:smartico:${product}`
`crm_callback:default:smartico:${product}`

// Depois
`crm_callback:client:${userId}:${crm}:${product}`
`crm_callback:default:${crm}:${product}`
```

### Queries DB

```sql
-- Antes
AND m.crm = 'smartico'

-- Depois
AND m.crm = ?   -- com crm como parâmetro
```

## Retrocompatibilidade

Todos os parâmetros `crm` com `default = 'smartico'` — callers existentes não precisam ser alterados, mas o `RcsCallbackService` deverá passar o valor lido do `crm_postback.crm`.

## Notas

O backoffice já tem (ou terá) a tarefa técnica de inserir as configurações da Fasttrack na tabela `crm_callback_status_mappings` com `crm = 'fasttrack'`. Este serviço só precisa ler o valor correto.

## Histórico de status
- Backlog (backlog): 2026-06-15T17:59:14.625Z → 2026-06-17T12:23:38.267Z
- To-do (unstarted): 2026-06-17T12:23:38.267Z → atual

## Relações
—

## Anexos
—
