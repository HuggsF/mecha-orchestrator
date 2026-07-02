# SEND-265 — Criação de Template de Jornada

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | Urgent |
| Responsável | peterson.marques@sendspeed.com |
| Time | Sendspeed |
| Projeto | — |
| Labels | UserIn, User Story, Templates, Melhoria |
| Parent | — |
| Criada | 2025-12-01T16:15:28.181Z por Vinicius Carneiro |
| Iniciada | 2025-12-16T03:22:51.665Z |
| Concluída | 2026-01-19T18:24:46.245Z |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-265-criacao-de-template-de-jornada |
| URL | https://linear.app/sendspeed/issue/SEND-265/criacao-de-template-de-jornada |

## Descrição

> **Como** funcionário da UserIn,
>
> **Quero** criar uma jornada e marcar como template,
>
> **Para** facilitar a implementação em outras empresas.

---

## Critérios de aceite:

### Userin:

* A jornada precisa ter o checkbox para transforma-lo em Template.
* Os templates criados devem ser disponibilizados imediatamente para os clientes que possuem aquela biblioteca
* Ao selecionar o checkbox ele deve perguntar para quais bibliotecas eu quero adicionar aquele Template.
* Usuários que não são UserIn não devem ver o checkbox para transformar a jornada em Template.
* Todos os componentes e regras dos componentes, ID de conversão personalizada devem ser copiados exatamente iguais.

### Cliente

* O Template utilizado deve ser clonado e abrir automaticamente a aba de personalização.
* O Template deve ser salvo e exibido para o cliente apenas se finalizado, caso contrario ele não deve salvar/mostrar.
* Quando finalizado, o Template deve agora se tornar uma jornada criada pelo cliente, contendo todas as alterações feitas por ele.
* As alterações feitas no Template pelo cliente não podem refletir no template original.

## Cenário de teste:

### Cenário 01:

- [ ] Entrar na plataforma pelas credenciais UserIn
- [ ] Acessar a aba de "Jornadas".
- [ ] Criar uma nova jornada.
- [ ] Selecionar a jornada criada e atribui-la como Template.

### Cenário 02:

- [ ] Entrar na plataforma pelas credenciais do cliente.
- [ ] Acessar a aba de "Jornadas".
- [ ] Selecionar "Utilizar o template".
- [ ] Finalizar sem alterar nada.

### Cenário 02.1:

- [ ] Entrar na plataforma pelas credenciais do cliente.
- [ ] Acessar a aba de "Jornadas".
- [ ] Selecionar "Utilizar o template".
- [ ] Alterar as configurações da jornada.
- [ ] Finalizar.

## Histórico de status
- Backlog (backlog): 2025-12-01T16:15:28.181Z → 2025-12-01T16:16:49.243Z
- Refining (backlog): 2025-12-01T16:16:49.243Z → 2025-12-01T16:16:58.802Z
- Backlog (backlog): 2025-12-01T16:16:58.802Z → 2025-12-01T17:01:49.004Z
- Refining (backlog): 2025-12-01T17:01:49.004Z → 2025-12-01T21:06:57.122Z
- Backlog (backlog): 2025-12-01T21:06:57.122Z → 2025-12-02T11:37:40.688Z
- Refining (backlog): 2025-12-02T11:37:40.688Z → 2025-12-05T13:58:54.568Z
- Canceled (canceled): 2025-12-05T13:58:54.568Z → 2025-12-05T13:58:55.903Z
- Released (completed): 2025-12-05T13:58:55.903Z → 2025-12-05T13:59:01.572Z
- Backlog (backlog): 2025-12-05T13:59:01.572Z → 2025-12-05T13:59:07.886Z
- To-do (unstarted): 2025-12-05T13:59:07.886Z → 2025-12-16T03:22:51.674Z
- In Progress (started): 2025-12-16T03:22:51.674Z → 2025-12-17T00:09:59.734Z
- Pull Request (started): 2025-12-17T00:09:59.734Z → 2026-01-19T18:04:50.053Z
- Product Review (started): 2026-01-19T18:04:50.053Z → 2026-01-19T18:24:46.254Z
- Released (completed): 2026-01-19T18:24:46.254Z → atual

## Relações
—

## Anexos
—
