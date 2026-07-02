# SEND-353 — 🐞 - Erro ao deletar a relação.

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | Urgent |
| Responsável | pedro.iegler@sendspeed.com |
| Time | Sendspeed |
| Projeto | — |
| Labels | UserIn, User Story, Bug |
| Parent | — |
| Criada | 2026-02-24T17:21:31.347Z por Vinicius Carneiro |
| Iniciada | 2026-02-24T17:58:53.510Z |
| Concluída | 2026-02-26T12:20:59.319Z |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-353--erro-ao-deletar-a-relacao |
| URL | https://linear.app/sendspeed/issue/SEND-353/erro-ao-deletar-a-relacao |

## Descrição

## 📍 Onde ocorre

> **[Referência de anexo/embed]:** UserIn - Marketing Engagement Platform (embed de página) — https://platform-stg-userin-ai.fly.dev/objects/graph

## 🔁 Passo a Passo

1. Entrar na plataforma.
2. Objetos -> Grafo & Relações.
3. Selecionar a relação.

> **[Imagem 1 — transcrição]:** Screenshot de UI do grafo de objetos mostrando o nó **UserProfile** (Perfil do utilizador, chips "1 campos", "8 relacoes", tags Financeiro, Comportamento, Intencao, Preferencias, botão "+ Adicionar campo") conectado por uma linha/edge rotulada **"Contacto CRM (0..1)"** ao card cinza escuro **"Contact — System"** (Catalogo vazio, 1 relacoes, campos Abc Nome, Abc Apelido, Abc Email, "+2 mais..."). Uma **seta vermelha** (marcação manual) aponta para o rótulo da relação "Contacto CRM (0..1)", indicando a relação que se tenta selecionar/apagar.

4. Apagar.

## ❌ Resultado Atual

Ele apresenta um erro ao apagar.

> **[Imagem 2 — transcrição]:** Screenshot de UI do grafo (visão mais ampla) com o nó **UserProfile** conectado a **Contact — System** (via "Contacto CRM (0..1)") e ao nó roxo **Feature — System** (Catalogo vazio, 0 relacoes, campos Nome, Modulo, Plano) via edge rotulada **"Jogos Favoritos (0..N)"**. No canto inferior direito, um **toast de erro vermelho**: **"Erro ao deletar — Campo "contact" não encontrado"**. Demonstra a falha ao tentar apagar a relação.

## ✅ Resultado Esperado

Quando for uma relação com um objeto Core e System ele deve apresentar uma mensagem avisando que não é possível apagar, quando for Custom deve ser permitido.

Semelhante ao card SEND-346

## Histórico de status
- To-do (unstarted): 2026-02-24T17:21:31.347Z → 2026-02-24T17:58:53.522Z
- In Progress (started): 2026-02-24T17:58:53.522Z → 2026-02-24T18:38:50.046Z
- Product Review (started): 2026-02-24T18:38:50.046Z → 2026-02-25T15:15:08.698Z
- Pull Request (started): 2026-02-25T15:15:08.698Z → 2026-02-25T16:15:52.512Z
- Product Review (started): 2026-02-25T16:15:52.512Z → 2026-02-26T12:20:59.338Z
- Released (completed): 2026-02-26T12:20:59.338Z → atual

## Relações
- Related: SEND-346 — 🐞 - Possibilidade de deletar objetos core e system.
- Related: SEND-343 — 🚀 - Aviso ao clicar no botão provisionar iGaming

## Anexos
—
