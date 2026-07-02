# SEND-355 — 🚀 - categória salva no banco de dados como apenas como "game"

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | Urgent |
| Responsável | Vinicius Carneiro |
| Time | Sendspeed |
| Projeto | — |
| Labels | Melhoria, User Story, UserIn |
| Parent | — |
| Criada | 2026-02-24T20:43:32.816Z por Vinicius Carneiro |
| Iniciada | 2026-02-26T19:21:09.564Z |
| Concluída | 2026-03-12T12:32:59.087Z |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-355--categoria-salva-no-banco-de-dados-como-apenas-como-game |
| URL | https://linear.app/sendspeed/issue/SEND-355/categoria-salva-no-banco-de-dados-como-apenas-como-game |

## Descrição

## 📍 Onde ocorre

Banco de dados

## ❌ Resultado Atual

Hoje a categória dos jogos estão sendo salvas como "game" pegando o primeiro componente na URL e utilizando como categoria.

## ✅ Resultado Esperado

Precisamos que ele salve a categória correta

Ex: [https://jogao.bet.br/games/pragmaticplay/sugar-rush-1000](https://jogao.bet.br/games/pragmaticplay/sugar-rush-1000)

A categoria seria: **pragmaticplay**

## 🧪 Evidências

> **[Imagem 1 — transcrição]:** Screenshot (evidência) referente ao salvamento da categoria de jogos no banco de dados. Demonstra que a categoria dos jogos está sendo persistida como o valor genérico "game" (extraído do primeiro segmento da URL) em vez da categoria correta (ex.: "pragmaticplay" a partir da URL `https://jogao.bet.br/games/pragmaticplay/sugar-rush-1000`). [Nota: URL da imagem expirada; conteúdo detalhado não pôde ser re-inspecionado além do contexto descrito na issue.]

## Histórico de status
- Refining (backlog): 2026-02-24T20:43:32.816Z → 2026-02-26T12:22:20.433Z
- To-do (unstarted): 2026-02-26T12:22:20.433Z → 2026-02-26T19:21:09.573Z
- In Progress (started): 2026-02-26T19:21:09.573Z → 2026-02-27T13:26:02.019Z
- Product Review (started): 2026-02-27T13:26:02.019Z → 2026-03-03T15:28:40.495Z
- Pull Request (started): 2026-03-03T15:28:40.495Z → 2026-03-03T17:21:51.942Z
- In Progress (started): 2026-03-03T17:21:51.942Z → 2026-03-04T19:40:25.765Z
- Product Review (started): 2026-03-04T19:40:25.765Z → 2026-03-12T12:32:59.101Z
- Released (completed): 2026-03-12T12:32:59.101Z → atual

## Relações
—

## Anexos
—
