# SEND-494 — [sms-api] Testes — atualizar specs e e2e para cobertura multi-CRM (Smartico + Fasttrack)

| Campo | Valor |
| -- | -- |
| Status | To-do (unstarted) |
| Prioridade | Medium |
| Responsável | andrei.garcia@externo.sendspeed.com |
| Time | Sendspeed |
| Projeto | — |
| Labels | — |
| Parent | SEND-488 |
| Criada | 2026-06-15T18:00:12.347Z por andrei.garcia@externo.sendspeed.com |
| Iniciada | — |
| Concluída | — |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-494-sms-api-testes-atualizar-specs-e-e2e-para-cobertura-multi |
| URL | https://linear.app/sendspeed/issue/SEND-494/sms-api-testes-atualizar-specs-e-e2e-para-cobertura-multi-crm-smartico |

## Descrição

## Objetivo

Atualizar os testes existentes e criar novos para garantir cobertura do fluxo multi-CRM após as demais tasks desta épica.

## Arquivos a atualizar / criar

### Unit tests

`src/crm-callback/crm-callback-config.service.spec.ts`

* Adicionar casos com `crm = 'fasttrack'`:
  * Redis key gerada corretamente: `crm_callback:client:{userId}:fasttrack:RCS`
  * DB query usa `crm = 'fasttrack'`
  * `resolveForMessage` com crm Fasttrack retorna config correta
* Verificar que `crm = 'smartico'` (default) não quebra nada

`src/sms/dto/send-sms.dto.spec.ts`

* Testar que `crm_postback: { crm: 'fasttrack', callback_url: '...' }` é aceito
* Testar que `crm_postback` sem campo `crm` ainda é aceito (retrocompatibilidade)

`src/rcs/rcs-validation.service.spec.ts`

* Idem para DTOs RCS

### E2E / integração

`test/rcs-callback.e2e-spec.ts`

* Adicionar cenário: `crm_postback` com `crm: 'fasttrack'` → verifica que o POST vai para Fasttrack
* Adicionar cenário: `crm_postback` sem campo `crm` → assume Smartico (retrocompatibilidade)
* Adicionar cenário: `repass: false` para Fasttrack → postback suprimido

## Critérios de aceite

* Todos os testes existentes passando (sem regressão)
* Cobertura dos cenários Fasttrack nos três níveis (DTO, config service, callback e2e)
* Logs corretos em cada rota (`[Smartico]` vs `[Fasttrack]`)

## Histórico de status
- Backlog (backlog): 2026-06-15T18:00:12.347Z → 2026-06-17T12:22:36.881Z
- To-do (unstarted): 2026-06-17T12:22:36.881Z → atual

## Relações
—

## Anexos
—
