# SEND-30 — [3] Filtrar Cards por Período

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | High |
| Responsável | Hugo Fernandes |
| Time | Sendspeed |
| Projeto | — |
| Labels | — |
| Parent | — |
| Criada | 2025-06-25T13:38:59.054Z por bruno.heidrich@sendspeed.com |
| Iniciada | 2025-07-10T12:13:38.638Z |
| Concluída | 2025-09-04T19:36:44.445Z |
| Arquivada | 2026-03-12T01:50:30.474Z |
| Vencimento | — |
| Branch | hugofernandes/send-30-3-filtrar-cards-por-periodo |
| URL | https://linear.app/sendspeed/issue/SEND-30/3-filtrar-cards-por-periodo |

## Descrição

**Como** Analista de Marketing Digital

**Eu quero** selecionar um período específico para visualizar as métricas dos cards

**Para que** eu possa comparar o desempenho das campanhas em diferentes momentos e identificar tendências sazonais

**Critérios de Aceitação:**

- [X] Devo poder selecionar data de início e fim
- [X] Os dados devem ser atualizados automaticamente após seleção
- [X] Períodos pré-definidos devem estar disponíveis (7 dias, 30 dias, 90 dias)
  - [X] Mas pode colocar a data que desejar
- [ ] O período selecionado deve persistir durante a navegação. \~ Após mudança de componente de Filtro o período  não está persistindo.
- [ ] Deve haver validação para períodos inválidos \~ Após mudança de componente de Filtro as validações ainda não estão retornando nenhum alerta no front-end.
  - [ ] mais de 90 dias
  - [ ] datas invalidas
  - [ ] Periodos futuros
  - [ ] final < data inicial

> **[Imagem 1 — transcrição]:** Screenshot de UI — recorte do cabeçalho da tela "Análise de Resultados" ("Performance detalhada dos cards do Buyer Agent"). Mostra a barra de filtros com quatro controles em linha: seletor de intervalo de datas com ícone de calendário exibindo "26/05/2025 - 25/06/2025", dropdown "Todos os Status", dropdown "Todas as Categorias" e um controle de ordenação (ícone de setas up/down) com "Nome". A imagem foca no componente de filtro por período (seleção de datas de início e fim).

## Histórico de status

- Backlog (backlog): 2025-06-25T13:38:59.054Z → 2025-07-10T12:13:38.620Z
- Pull Request (started): 2025-07-10T12:13:38.620Z → 2025-07-21T12:36:59.808Z
- In Progress (started): 2025-07-21T12:36:59.808Z → 2025-07-31T12:28:05.544Z
- Pull Request (started): 2025-07-31T12:28:05.544Z → 2025-08-11T13:53:53.082Z
- Product Review (started): 2025-08-11T13:53:53.082Z → 2025-08-13T22:11:30.926Z
- Pull Request (started): 2025-08-13T22:11:30.926Z → 2025-08-25T12:15:40.007Z
- Product Review (started): 2025-08-25T12:15:40.007Z → 2025-08-27T15:25:05.164Z
- Pull Request (started): 2025-08-27T15:25:05.164Z → 2025-09-04T19:36:44.475Z
- Released (completed): 2025-09-04T19:36:44.475Z → atual

## Relações

—

## Anexos

—
