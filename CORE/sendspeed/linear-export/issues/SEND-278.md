# SEND-278 — Local de adição de valores na plataforma

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | Urgent |
| Responsável | andrei.garcia@externo.sendspeed.com |
| Time | Sendspeed |
| Projeto | — |
| Labels | Sendspeed, User Story, Implementação |
| Parent | — |
| Criada | 2026-01-08T18:11:12.164Z por Vinicius Carneiro |
| Iniciada | 2026-01-13T18:29:47.975Z |
| Concluída | 2026-01-19T18:24:19.679Z |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-278-local-de-adicao-de-valores-na-plataforma |
| URL | https://linear.app/sendspeed/issue/SEND-278/local-de-adicao-de-valores-na-plataforma |

## Descrição

> **Como** Customer Success
>
> **Quero** conseguir adicionar os valores de cobrança de cada cliente
>
> **Para** facilitar a visualizações dos valores disparados por cada cliente.

---

## Critérios de aceite:

* Dentro da plataforma do Backoffice, precisamos de um local onde a Leticia (Customer Success) consiga adicionar e editar os valores cobrados dos canais (SMS, RCS, VOIP, etc…) de cada cliente.
* Os valores cobrados devem ser identificados e puxados no momento da criação da campanha e inseridos automaticamente na linha da campanha no banco.
* Precisa ser algo simples, apenas para controle de valor.
* Quando o valor for atualizado na plataforma, ele deve contar a partir do momento da atualização para frente, sem afetar/alterar os valores antigos.
* Deve ter a opção de editar valores antigos também, mas separado (se por algum motivo o valor não tenha sido atualizado na data correta, devemos conseguir editar/alterar manualmente apenas os valores das campanhas disparadas que estão divergentes sem afetar os outros valores.)

## Cenário de teste:

- [ ] Entrar no backoffice da Sendspeed.
- [ ] Adicionar o valor á um canal de uma empresa.
- [ ] Efetuar um disparo de teste.
- [ ] Consultar no banco de dados se os valores foram impressos corretamente.

## Histórico de status
- Backlog (backlog): 2026-01-08T18:11:12.164Z → 2026-01-09T16:27:40.794Z
- To-do (unstarted): 2026-01-09T16:27:40.794Z → 2026-01-13T18:29:47.994Z
- In Progress (started): 2026-01-13T18:29:47.994Z → 2026-01-14T12:19:57.591Z
- Pull Request (started): 2026-01-14T12:19:57.591Z → 2026-01-19T12:33:04.746Z
- Product Review (started): 2026-01-19T12:33:04.746Z → 2026-01-19T18:24:19.707Z
- Released (completed): 2026-01-19T18:24:19.707Z → atual

## Relações
—

## Anexos
—
