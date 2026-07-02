# SEND-516 — Ingestão de eventos via webhooks da NGX na UserIn

| Campo | Valor |
| -- | -- |
| Status | In Progress (started) |
| Prioridade | No priority |
| Responsável | pedro.iegler@sendspeed.com |
| Time | Sendspeed |
| Projeto | — |
| Labels | User Story, UserIn |
| Parent | — |
| Criada | 2026-06-22T17:53:31.032Z por Vinicius Carneiro |
| Iniciada | 2026-06-23T15:13:32.229Z |
| Concluída | — |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-516-ingestao-de-eventos-via-webhooks-da-ngx-na-userin |
| URL | https://linear.app/sendspeed/issue/SEND-516/ingestao-de-eventos-via-webhooks-da-ngx-na-userin |

## Descrição

**Como** time de produto/dados da UserIn

**Quero** receber e persistir os eventos de registro de usuário e de depósito confirmado enviados pela NGX

**Para** enriquecer nossa base com dados de cadastro e depósito desses usuários e habilitar segmentações futuras

### 📈 Use Case

Hoje a UserIn não tem visibilidade dos eventos dentro da plataforma NGX usada pela Apostou — cadastros e depósitos ficam só na NGX. Registrando a URL de destino da UserIn no painel NGX e tratando USER_REGISTRATION e DEPOSIT_CONFIRMATION, passamos a manter um espelho atualizado desses dados, vinculado ao contato correto via external_id. A integração nasce genérica para ser reaproveitada por outros clientes NGX.

### ✅ Critérios de aceite

* Endpoints HTTP expostos pela UserIn para receber POST da NGX em /user-registration (USER_REGISTRATION) e /deposit-confirmation (DEPOSIT_CONFIRMATION)
* Toda requisição tem X-Auth-Signature validada via HMAC-SHA256 sobre o corpo cru + secret compartilhado, comparada em Base64; assinatura inválida é rejeitada e nada é persistido
* Sucesso retorna HTTP 200 {"processed": true}; falha retorna HTTP 500 {"processed": false, "error": "..."} (contrato exigido pela NGX)
* Usuário do evento correlacionado a um contato existente via external_id presente em external_params
* Só DEPOSIT_CONFIRMATION com deposit_status = "PAID" é tratado como depósito efetivo
* Persistência idempotente: reentrega do mesmo evento não duplica registro
* Secret e URL de destino parametrizáveis por cliente/integração (não hardcoded para Apostou)

### 🧩 Cenários de teste

* USER_REGISTRATION com assinatura válida e external_id conhecido → contato enriquecido, 200 {"processed": true}
* X-Auth-Signature inválida → rejeitado, nada persistido
* DEPOSIT_CONFIRMATION PAID → depósito persistido e vinculado ao contato
* DEPOSIT_CONFIRMATION PENDING/PROCESSING/REFUSED → não conta como depósito
* Mesmo deposit_id entregue 2x → um único registro
* Evento de usuário sem external_id mapeável → tratado conforme política definida
* Evento de teste da NGX → não polui base de produção (separação por URL/secret de ambiente, já que registro e depósito não têm is_test)

## Histórico de status
- To-do (unstarted): 2026-06-22T17:53:31.032Z → 2026-06-23T15:13:32.240Z
- In Progress (started): 2026-06-23T15:13:32.240Z → atual

## Relações
—

## Anexos
—
