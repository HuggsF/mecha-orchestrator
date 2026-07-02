# SEND-430 — Editor RCS — Permitir Alterar Formato e Nome em Qualquer Momento

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | Urgent |
| Responsável | Vinicius Carneiro |
| Time | Sendspeed |
| Projeto | — |
| Labels | — |
| Parent | — |
| Criada | 2026-03-26T11:52:50.523Z por paulo.ribeiro@sendspeed.com |
| Iniciada | 2026-04-01T14:48:43.409Z |
| Concluída | 2026-04-14T15:16:02.253Z |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-430-editor-rcs-permitir-alterar-formato-e-nome-em-qualquer |
| URL | https://linear.app/sendspeed/issue/SEND-430/editor-rcs-permitir-alterar-formato-e-nome-em-qualquer-momento |

## Descrição

## **Descrição**

A tela de criação/edição de mensagens RCS (RcsPage) tem dois problemas de navegação que travam o usuário:

### **Problema 1 — Não é possível alterar o formato depois de avançar para o editor**

**Fluxo de criação (novo):**

1. Tela "create" — usuário escolhe nome, remetente, formato (Texto/Cartão/Carrossel/Arquivo)
2. Clica "Avançar para editor" → vai para a tela "editor"
3. Na tela "editor", o botão "VOLTAR" executa setContentType(null); setView('create') — ou seja, **limpa o tipo** e volta para a tela de criação **sem conteúdo**

O usuário que quiser mudar de Texto para Cartão depois de já ter começado a editar **perde todo o conteúdo** ao voltar, porque setContentType(null) reseta a seleção.

**Fluxo de edição (existente):**

1. Usuário clica em "Editar" em um template existente na lista
2. openEdit() executa setView('editor') — **pula a tela "create" inteira**
3. Na tela "editor", o botão "VOLTAR" vai para "create" com setContentType(null) — que **não faz sentido** para edição, porque a tela "create" aparece vazia

Resultado: o editor de um template existente **não tem como alterar o formato** sem perder tudo.

### **Problema 2 — Não é possível alterar o nome durante a edição**

Na tela "editor" (onde o conteúdo é editado de fato), **não existe campo de nome**. O campo de nome só aparece na tela "create" (a overview), que é pulada no fluxo de edição.

O nome é definido apenas em messageName no state e é editável exclusivamente na tela "create" com o ícone de lápis. Quem edita um template existente nunca passa por essa tela.

## **Proposta**

### **Formato: trocar com confirmação e migração de conteúdo compatível**

Adicionar um seletor de formato acessível **dentro da tela "editor"**, acima do editor de conteúdo. Ao trocar de formato:

1. Se o conteúdo atual está vazio → troca sem confirmação
2. Se tem conteúdo → exibir dialog de confirmação:

* Título: "Alterar formato para \[novo formato\]?"
* Corpo: "O conteúdo compatível será mantido (título, descrição). Campos exclusivos do formato anterior serão removidos."
* Botões: "Cancelar" / "Alterar formato"

1. Migrar o que for compatível entre formatos:

| De → Para | O que mantém |
| -- | -- |
| Rich Card → Carousel | Título, descrição e botões do card viram o primeiro card do carrossel |
| Carousel → Rich Card | Primeiro card do carrossel vira o rich card (demais cards perdidos — avisar) |
| Rich Card → Text | Título + descrição concatenados no campo mensagem |
| Text → Rich Card | Mensagem vira descrição do card |
| Qualquer → File | Nada migrado (formatos incompatíveis) |
| File → Qualquer | Nada migrado |

### **Nome: sempre editável no editor**

Adicionar o campo de nome (input inline editável) no header da tela "editor", assim como já aparece na tela "create". O nome deve ser editável em qualquer momento do fluxo.

### **Fluxo de edição corrigido**

Quando openEdit() é chamado para um template existente, o "VOLTAR" deve retornar para a **lista** (não para a tela "create" vazia):

| Contexto | "VOLTAR" leva para |
| -- | -- |
| Criando novo (veio de "create") | Tela "create" (overview) — **mantendo** o contentType e conteúdo |
| Editando existente (veio de "list") | Tela "list" |

## **Critérios de Aceitação**

- [ ] O campo de nome é editável na tela "editor", tanto para novo quanto para edição de existente
- [ ] O seletor de formato aparece na tela "editor" (não só na tela "create")
- [ ] Ao trocar formato com conteúdo vazio, troca sem confirmação
- [ ] Ao trocar formato com conteúdo preenchido, exibe dialog de confirmação informando o que será mantido e o que será perdido
- [ ] Conteúdo compatível é migrado entre formatos (título, descrição, mensagem) conforme tabela de migração
- [ ] Ao trocar de Carousel para Rich Card com múltiplos cards, o dialog avisa: "Apenas o primeiro cartão será mantido. Os demais serão removidos."
- [ ] Botão "VOLTAR" no editor de template existente retorna para a lista, não para "create" vazio
- [ ] Botão "VOLTAR" no editor de novo template retorna para "create" preservando o conteúdo e tipo selecionado
- [ ] openEdit() permite acesso ao campo de nome sem precisar navegar para outra tela

## **Edge Cases**

* **Trocar de Carousel (5 cards) para Rich Card:** Aviso explícito de que 4 cards serão perdidos, mostrando a quantidade. Apenas o primeiro card é mantido.
* **Trocar para File:** Aviso de que todo o conteúdo será perdido (formatos incompatíveis). Migração zero.
* **Trocar de formato e cancelar:** Nada muda. O conteúdo permanece exatamente como estava.
* **Nome vazio ao salvar:** Validação já existente — disabled={saving || !name.trim()}. Manter esse comportamento.

---

## 🎯 Priorização RICE — Score: 6.4

| Reach | Impact | Confidence | Effort | Score |
| -- | -- | -- | -- | -- |
| 6 | 2 (high) | 80% | 1.5 meses | **6.4** |

**Justificativa:** Reach 6: usuários do editor RCS. Impacto high (2): fluxo de edição completamente quebrado. Confidence 80%: problemas bem documentados. Esforço 1.5 meses: refactor de navegação + dialog de migração.

## Histórico de status
- Backlog (backlog): 2026-03-26T11:52:50.523Z → 2026-03-26T12:18:56.346Z
- Refining (backlog): 2026-03-26T12:18:56.346Z → 2026-03-31T12:33:51.755Z
- To-do (unstarted): 2026-03-31T12:33:51.755Z → 2026-04-01T14:48:43.441Z
- In Progress (started): 2026-04-01T14:48:43.441Z → 2026-04-01T15:38:17.247Z
- Product Review (started): 2026-04-01T15:38:17.247Z → 2026-04-14T15:16:02.268Z
- Released (completed): 2026-04-14T15:16:02.268Z → atual

## Relações
—

## Anexos
—
