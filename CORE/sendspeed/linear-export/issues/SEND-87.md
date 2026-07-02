# SEND-87 — [COMPANION][ANALYTICS][BUG] — Seleção de data e horário não aplica corretamente

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | No priority |
| Responsável | Hugo Fernandes |
| Time | Sendspeed |
| Projeto | — |
| Labels | — |
| Parent | — |
| Criada | 2025-09-05T13:39:02.897Z por bruno.heidrich@sendspeed.com |
| Iniciada | 2025-09-05T15:23:47.826Z |
| Concluída | 2025-09-25T12:56:18.124Z |
| Arquivada | 2026-04-03T01:20:18.142Z |
| Vencimento | — |
| Branch | hugofernandes/send-87-companionanalyticsbug-selecao-de-data-e-horario-nao-aplica |
| URL | https://linear.app/sendspeed/issue/SEND-87/companionanalyticsbug-selecao-de-data-e-horario-nao-aplica |

## Descrição

**Como** usuário do Analytics, 
**quero** que a seleção de data e **horário** seja aplicada de primeira 
**para** analisar períodos sem confusão.

**Pronto quando**

* Ao escolher data/horário, o filtro **aplica imediatamente** e mostra o período correto.
* Trocas seguidas **não "atrasam"** o valor; não há inversão.

> **[Imagem 1 — transcrição]:** Screenshot da interface de UI "Análise de Resultados" do Analytics/Companion (Buyer Agent). Cabeçalho: título "Análise de Resultados" com subtítulo "Performance detalhada dos cards do Buyer Agent". Ao lado há dois campos de data com ícone de calendário: "23/07/2025 00:00" (data inicial) e "23/08/2025 00:00" (data final). À direita, quatro botões de atalho de período: "7 dias", "30 dias", "90 dias", "Este mês". Abaixo, uma barra de filtros com o rótulo "Filtros:" e três dropdowns: "Status", "Categoria", "Prioridade"; seguido de "Ordenar:" com um dropdown "Nome A-Z" (ícone de setas de ordenação). Em seguida, quatro cards de métricas (KPIs), todos com valor **0**: "Impressões — 0 — Total do período" (ícone de olho), "Cliques — 0 — Interações no preview" (ícone de cursor), "CTA — 0 — Ações no botão" (ícone de alvo), "Conversões — 0 — Resultados alcançados" (ícone de troféu). No rodapé aparece o título de seção "Performance por Card (4 total | 4 nesta página)". A imagem demonstra a tela de filtros de data/horário e os KPIs zerados no período selecionado.

@bruno.heidrich - valida pra mim por gentileza se esse é o comportamento esperado

Também ajustei os filtros para ficar intuitivo

## Histórico de status
- To-do (unstarted): 2025-09-05T13:39:02.897Z → 2025-09-05T15:23:47.841Z
- Pull Request (started): 2025-09-05T15:23:47.841Z → 2025-09-25T12:20:01.123Z
- Product Review (started): 2025-09-25T12:20:01.123Z → 2025-09-25T12:56:18.146Z
- Released (completed): 2025-09-25T12:56:18.146Z → atual

## Relações
—

## Anexos
—
