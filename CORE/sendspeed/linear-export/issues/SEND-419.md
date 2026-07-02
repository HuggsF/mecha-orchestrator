# SEND-419 — 🚀 - Criação de Template RCS

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | Urgent |
| Responsável | Vinicius Carneiro |
| Time | Sendspeed |
| Projeto | — |
| Labels | Implementação, User Story, UserIn |
| Parent | — |
| Criada | 2026-03-20T14:45:34.069Z por Vinicius Carneiro |
| Iniciada | 2026-03-20T19:02:06.990Z |
| Concluída | 2026-04-01T12:10:33.897Z |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-419--criacao-de-template-rcs |
| URL | https://linear.app/sendspeed/issue/SEND-419/criacao-de-template-rcs |

## Descrição

> **Como** gestor de campanhas da Sendspeed
> **Quero** criar, editar e gerenciar templates de RCS na plataforma
> **Para** ter mensagens padronizadas e aprovadas prontas para uso em jornadas e campanhas, garantindo consistência de marca e conformidade com os provedores.

\*\*Puxar a branch do Paulo para começar a trabalhar em cima\*\*

---

# 📈 Use Case: Template de boas-vindas RCS para cassino online

Uma operadora de jogos quer enviar uma mensagem RCS rica para novos registros, contendo o logo da marca, um texto de boas-vindas personalizado com o nome do jogador e um botão "Jogar Agora" que leva diretamente à página de depósito. O gestor cria o template "Boas-vindas VIP" com variáveis Liquid `{{ name }}` e `{{ deposit_url }}`, salva e o disponibiliza para uso nas jornadas.

# ✅ Critérios de aceite:

* O modelo Template deve aceitar o tipo `rcs` (além de sms, email, push, whatsapp).
* O CRUD de templates deve permitir criar, editar, listar e excluir templates RCS.
* O template RCS deve possuir os campos: nome (identificador no provedor), conteúdo/body, variáveis Liquid detectadas automaticamente.
* Templates RCS devem ser filtráveis na listagem por tipo.
* O preview do template deve exibir as variáveis Liquid destacadas.

# 🧩 Cenários de teste:

- [ ] Criar template RCS com nome "Boas-vindas VIP" e variáveis `{{ name }}` e `{{ deposit_url }}`.
- [ ] Verificar que o template aparece na listagem filtrada por tipo RCS.
- [ ] Editar o conteúdo do template e confirmar que as variáveis são re-extraídas.
- [ ] Excluir um template RCS e confirmar que não aparece mais na listagem.
- [ ] Tentar criar template RCS sem nome — deve retornar erro de validação.
- [ ] Verificar que templates de outros tipos (SMS, Email) não são afetados.

## Histórico de status
- Backlog (backlog): 2026-03-20T14:45:34.069Z → 2026-03-20T15:20:19.437Z
- To-do (unstarted): 2026-03-20T15:20:19.437Z → 2026-03-20T19:02:07.023Z
- In Progress (started): 2026-03-20T19:02:07.023Z → 2026-03-23T17:44:00.003Z
- Pull Request (started): 2026-03-23T17:44:00.003Z → 2026-03-24T17:29:11.963Z
- Product Review (started): 2026-03-24T17:29:11.963Z → 2026-03-31T18:24:43.123Z
- Release (started): 2026-03-31T18:24:43.123Z → 2026-04-01T12:10:34.913Z
- Released (completed): 2026-04-01T12:10:34.913Z → atual

## Relações
—

## Anexos
—
