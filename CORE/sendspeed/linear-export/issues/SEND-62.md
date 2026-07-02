# SEND-62 — [BUG] [JOURNEY] Página visitantes não funcional

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | No priority |
| Responsável | peterson.marques@sendspeed.com |
| Time | Sendspeed |
| Projeto | — |
| Labels | — |
| Parent | — |
| Criada | 2025-08-22T12:34:13.613Z por bruno.heidrich@sendspeed.com |
| Iniciada | 2025-08-27T00:09:31.693Z |
| Concluída | 2025-09-04T19:36:34.051Z |
| Arquivada | 2026-03-12T01:50:29.905Z |
| Vencimento | — |
| Branch | hugofernandes/send-62-bug-journey-pagina-visitantes-nao-funcional |
| URL | https://linear.app/sendspeed/issue/SEND-62/bug-journey-pagina-visitantes-nao-funcional |

## Descrição

**Como reproduzir**
Abrir "Visitantes" na aba Journey; os usuários anônimos do site não estão ficando armazenados ali, apenas se utiliza o filtro por LocalStorage. 

Porém, nunca saberemos o LocalStorage de um lead anônimo pra conseguir achar ele na busca, logo, ele precisa aparecer ali na tela para conseguirmos entender sua jornada.

**Esperado**
Listar **todos os anônimos** do período, **sem duplicidade**, e **respeitar os filtros** (data, origem, dispositivo).

**Pronto quando**

* A lista traz **100%** dos anônimos do período selecionado.
* **Sem** itens duplicados.
* Filtros **mudam a lista** como esperado.

> **[Imagem 1 — transcrição]:** Screenshot de UI (tela "Análise de Visitantes"). Título "Análise de Visitantes" (ícone de olho) com subtítulo "Análise detalhada de comportamento e navegação de visitantes específicos". Card "Filtros de Visitante" (ícone de lupa) com texto "Informe o LocalStorage ID ou Visitor ID para analisar um visitante específico"; dois campos: "LocalStorage ID" (placeholder "SmartTrack__local_...") e "Visitor ID" (placeholder "68652b60db262ed5ecc5aa4a"); botão roxo "Buscar Visitante". Abaixo, estado vazio com ícone de lupa e textos "Busque um visitante para começar" e "Informe um LocalStorage ID ou Visitor ID para ver a análise detalhada de comportamento". Evidencia que a página depende de busca por ID e não lista os anônimos.

## Histórico de status
- To-do (unstarted): 2025-08-22T12:34:13.613Z → 2025-08-27T00:09:27.212Z
- In Progress (started): 2025-08-27T00:09:27.212Z → 2025-08-27T14:02:15.461Z
- Product Review (started): 2025-08-27T14:02:15.461Z → 2025-08-27T15:03:23.388Z
- Pull Request (started): 2025-08-27T15:03:23.388Z → 2025-09-04T19:36:34.087Z
- Released (completed): 2025-09-04T19:36:34.087Z → atual

## Relações
—

## Anexos
—
