# SEND-489 — [Backoffice] Suporte ao CRM Fasttrack nas telas de crm-callback-config

| Campo | Valor |
| -- | -- |
| Status | To-do (unstarted) |
| Prioridade | High |
| Responsável | andrei.garcia@externo.sendspeed.com |
| Time | Sendspeed |
| Projeto | — |
| Labels | — |
| Parent | SEND-488 |
| Criada | 2026-06-15T17:39:17.487Z por andrei.garcia@externo.sendspeed.com |
| Iniciada | — |
| Concluída | — |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-489-backoffice-suporte-ao-crm-fasttrack-nas-telas-de-crm |
| URL | https://linear.app/sendspeed/issue/SEND-489/backoffice-suporte-ao-crm-fasttrack-nas-telas-de-crm-callback-config |

## Descrição

## Contexto

Adicionar suporte ao CRM **Fasttrack** nas telas de configuração de callback do Backoffice, seguindo o mesmo padrão já implementado para o Smartico.

---

## Escopo técnico

### Telas afetadas

* `/crm-callback-config/default`
* `/crm-callback-config/clients`
* `/crm-callback-config/templates`

Em todas elas, o CRM **Fasttrack** deve aparecer como nova opção disponível nos seletores/abas de CRM, ao lado do Smartico.

---

## Tarefas técnicas

### 1. Adicionar Fasttrack como CRM disponível

* Registrar `fasttrack` como valor válido no enum/constante de CRMs suportados (localizar onde `smartico` está definido e espelhar).
* Garantir que os componentes de seleção de CRM nas três telas listem o Fasttrack.

### 2. Seed inicial — config default do Fasttrack

* Criar uma seed que inicialize a configuração default do Fasttrack **copiando** os valores default do Smartico.
* A seed deve rodar no deploy (ou via `php artisan db:seed`) sem reprocessar se o registro já existir (`upsert` / `firstOrCreate`).
* Verificar a migration/tabela usada para configs default e replicar a estrutura.

### 3. Tela `/crm-callback-config/default`

* Exibir e permitir editar a config default do Fasttrack.
* Utilizar o mesmo layout e campos já presentes para o Smartico.

### 4. Tela `/crm-callback-config/clients`

* Suporte a override por cliente para o Fasttrack.
* Listar clientes com config Fasttrack ativa; permitir criar/editar/remover overrides.

### 5. Tela `/crm-callback-config/templates`

* Templates de callback compatíveis com Fasttrack.
* Verificar se os templates são agnósticos ao CRM ou se precisam de variante Fasttrack.

---

## Critérios de aceite

- [ ] Fasttrack aparece como opção nas três telas de crm-callback-config.
- [ ] Seed cria config default do Fasttrack baseada no default do Smartico (idempotente).
- [ ] É possível salvar e recuperar configurações (default, por cliente e templates) para o Fasttrack.
- [ ] Nenhuma regressão nas configurações existentes do Smartico.
- [ ] Sem erros de console/500 ao navegar pelas telas com Fasttrack selecionado.

## Histórico de status
- To-do (unstarted): 2026-06-15T17:39:17.487Z → atual

## Relações
—

## Anexos
—
