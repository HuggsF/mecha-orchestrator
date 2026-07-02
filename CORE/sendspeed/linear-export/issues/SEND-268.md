# SEND-268 — Criação de Template de Regra

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | Urgent |
| Responsável | Vinicius Carneiro |
| Time | Sendspeed |
| Projeto | — |
| Labels | UserIn, User Story, Templates, Melhoria |
| Parent | — |
| Criada | 2025-12-01T16:57:13.223Z por Vinicius Carneiro |
| Iniciada | 2025-12-08T20:13:22.791Z |
| Concluída | 2025-12-23T19:32:04.447Z |
| Arquivada | 2026-06-25T22:35:06.840Z |
| Vencimento | — |
| Branch | hugofernandes/send-268-criacao-de-template-de-regra |
| URL | https://linear.app/sendspeed/issue/SEND-268/criacao-de-template-de-regra |

## Descrição

> **Como** funcionário da UserIn,
>
> **Quero** que seja possível ao criar uma regra, marca-la como template,
>
> **Para** facilitar a disponibilização do modelo de regras para o cliente.

---

## Critérios de aceite:

### UserIn:

* A regra precisa ter a adição de um checkbox para transforma-lo em Template conforme exemplo:

> **[Imagem 1 — transcrição]:** Screenshot de UI — tabela/listagem de regras da plataforma, exibindo colunas: **Nome**, **Descrição**, **Tipo**, **Template**, **Criado em**, **Atualizado em** (e uma coluna final de ações com menu de três pontos "..."). Linha 1: Nome "SEND-260", Descrição "teste", Tipo = badge "Comportamental", Template = toggle/switch AZUL LIGADO com rótulo "Sim", Criado em "02/12/2025 10:37", Atualizado em "02/12/2025 17:21". Linha 2: Nome 'URL contém "index" E Uma vez por sessão', Descrição 'URL contém "index" E Uma vez por sessão', Tipo = badge "Plano", Template = toggle/switch CINZA DESLIGADO com rótulo "Não", Criado em "27/11/2025 13:34", Atualizado em "02/12/2025 17:15". Demonstra o exemplo do checkbox/toggle "Template" (Sim/Não) que deve ser adicionado à regra para marcá-la como template.

*Obs: Não precisa retirar o checkbox de status, apenas adicionar o de template.*

* Ao selecionar o checkbox ele deve perguntar para quais bibliotecas eu quero adicionar aquele Template.
  * *Ele pode ser gerenciado nos três pontos ao invés de ser no checkbox.*
* Apenas funcionários da UserIn vão ver o checkbox de Template.
* Os templates criados devem ser disponibilizados imediatamente para os clientes que possuem aquela biblioteca
* Caso uma regra atrelada a jornada tenha um ou mais componentes, todos devem ser clonados quando atrelados á uma jornada.

### Cliente:

* A regra precisa ter um botão "Utilizar este template de regra", quando clickado abrirá a tela de edição mas com todos os componentes travados e deverá ser liberada para edição apenas após ele clickar em clonar (Botão que substituirá o Salvar apenas nos templates), abrindo imediatamente a pagina de customização e só salvando caso o cliente aperte em salvar.
  * No template não precisa ter as informações de "Criado em"e "Atualizado em", apenas um botão para "Utilizar um template".
* A regra precisa ter uma identificação mostrando que aquela é um template, ele pode ser adicionado automaticamente na descrição.

## **Cenários de teste:**

### Cenário 01:

- [X] Entrar na plataforma via credenciais UserIn
- [X] Clicar em criar nova regra.
- [X] Criar uma regra: visualização de pagina > após 5s > disparar alert.
- [X] Marcar esta regra como template.
- [X] Salvar.

### Cenário 02:

- [X] Entrar na plataforma via credenciais do Cliente.
- [X] Selecionar as regras.
- [X] Selecionar "Utilizar o Template de regras"
- [X] Salvar

## Histórico de status
- Backlog (backlog): 2025-12-01T16:57:13.223Z → 2025-12-01T17:01:46.634Z
- Refining (backlog): 2025-12-01T17:01:46.634Z → 2025-12-05T13:59:15.883Z
- To-do (unstarted): 2025-12-05T13:59:15.883Z → 2025-12-08T20:13:22.800Z
- In Progress (started): 2025-12-08T20:13:22.800Z → 2025-12-12T14:16:54.960Z
- Pull Request (started): 2025-12-12T14:16:54.960Z → 2025-12-12T14:17:03.232Z
- In Progress (started): 2025-12-12T14:17:03.232Z → 2025-12-12T14:45:24.473Z
- Product Review (started): 2025-12-12T14:45:24.473Z → 2025-12-23T19:32:04.470Z
- Released (completed): 2025-12-23T19:32:04.470Z → atual

## Relações
—

## Anexos
—
