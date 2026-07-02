# SEND-270 — Criação do Template de Componentes

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | Urgent |
| Responsável | andrei.garcia@externo.sendspeed.com |
| Time | Sendspeed |
| Projeto | — |
| Labels | UserIn, Templates, User Story, Melhoria |
| Parent | — |
| Criada | 2025-12-01T20:41:55.057Z por Vinicius Carneiro |
| Iniciada | 2025-12-09T18:09:25.939Z |
| Concluída | 2026-01-19T18:24:42.635Z |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-270-criacao-do-template-de-componentes |
| URL | https://linear.app/sendspeed/issue/SEND-270/criacao-do-template-de-componentes |

## Descrição

> **Como** funcionario da UserIn,
>
> **Quero** conseguir selecionar cards criados nos meus cards como template,
>
> **Para** disponibiliza-los para os clientes como templates.

---

Imagem de exemplo da tela do cliente:

> **[Imagem 1 — transcrição]:** Screenshot de UI — card de "Preview do Template" (fundo branco). No topo esquerdo o rótulo "Preview do Template"; no topo direito um checkbox verde marcado com o texto "Ativar como template". No centro, uma área de card retangular com o texto "🚀 JOGUE E GANHE!" (emoji de foguete). Abaixo, o título em negrito "Finalizar Registro" e duas badges: "Modal" (cinza) e "Template" (amarela). No canto inferior direito há um botão "Editar" (com ícone de lápis) e um menu de três pontos verticais. Rodapé com "Criado: 03/10/2025" e "Atualizado: 22/10/2025". Demonstra a tela do card com o checkbox "Ativar como template" marcado e a badge "Template" aplicada ao componente.

---

Imagem de exemplo da tela UserIn:

> **[Imagem 2 — transcrição]:** Screenshot de UI — comparação de dois cards lado a lado. **Card esquerdo "Preview do Template":** área de card com "🚀 JOGUE E GANHE!"; título "Finalizar Registro"; badges "Modal" (cinza) e "Template" (amarela); botão "Utilizar o template" (com ícone de lápis) e menu de três pontos; rodapé "Criado: 03/10/2025 / Atualizado: 22/10/2025". Representa a visão do cliente (botão "Utilizar o template"). **Card direito "Preview do Componente":** área de card com "🚀 JOGUE E GANHE!"; título "Esclarecimento de Produto"; badges "Card" (cinza), "Pausado" (amarela) e "Jornada de conversão" (azul/lilás); uma faixa preta com texto "⚡ Gatilho ativado"; botão verde "◎ Gatilho", botão "Editar" (com ícone de lápis) e menu de três pontos; rodapé "Criado: 03/10/2025 / Atualizado: 22/10/2025". Representa a visão UserIn do componente com gatilho ativado. Demonstra a diferença entre o card exibido como template (cliente) e como componente (UserIn).

---

## Critérios de aceite:

### UserIn:

* O componente precisa ter o checkbox para transforma-lo em Template.
* Os templates criados devem ser disponibilizados imediatamente para os clientes que possuem aquela biblioteca
* Ao selecionar o checkbox ele deve perguntar para quais bibliotecas eu quero adicionar aquele Template.
* Usuários que não são UserIn não devem ver o checkbox para transformar o componente em Template.

### Cliente:

* O Template utilizado deve ser clonado e abrir automaticamente a aba de personalização.
* O Template deve ser salvo e exibido para o cliente apenas se finalizado, caso contrario ele não deve salvar
* Quando finalizado, o Template deve agora se tornar um card criado pelo cliente, contendo todas as alterações feitas por ele.
* As alterações feitas no Template pelo cliente não podem refletir no template original.

## Cenário de teste:

### Cenário 01:

- [ ] Entrar na plataforma pelas credenciais UserIn
- [ ] Acessar a aba de "meus cards".
- [ ] Criar um novo componente (card).
- [ ] Selecionar o card criado e atribui-lo como Template.

### Cenário 02:

- [ ] Entrar na plataforma pelas credenciais do cliente.
- [ ] Acessar a aba de meus cards.
- [ ] Selecionar "Utilizar o template"
- [ ] Alterar as configurações do componente.
- [ ] Finalizar

## Histórico de status
- Refining (backlog): 2025-12-01T20:41:55.057Z → 2025-12-05T13:59:19.626Z
- To-do (unstarted): 2025-12-05T13:59:19.626Z → 2025-12-09T18:09:25.947Z
- In Progress (started): 2025-12-09T18:09:25.947Z → 2025-12-15T12:52:03.174Z
- Pull Request (started): 2025-12-15T12:52:03.174Z → 2026-01-19T18:04:57.201Z
- Product Review (started): 2026-01-19T18:04:57.201Z → 2026-01-19T18:24:42.644Z
- Released (completed): 2026-01-19T18:24:42.644Z → atual

## Relações
—

## Anexos
—
