# SEND-29 — [2] Visualizar Lista de Cards com Métricas

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | High |
| Responsável | Hugo Fernandes |
| Time | Sendspeed |
| Projeto | — |
| Labels | — |
| Parent | — |
| Criada | 2025-06-25T13:36:25.187Z por bruno.heidrich@sendspeed.com |
| Iniciada | 2025-07-10T12:13:34.160Z |
| Concluída | 2025-09-04T19:36:42.757Z |
| Arquivada | 2026-03-12T01:50:30.237Z |
| Vencimento | — |
| Branch | hugofernandes/send-29-2-visualizar-lista-de-cards-com-metricas |
| URL | https://linear.app/sendspeed/issue/SEND-29/2-visualizar-lista-de-cards-com-metricas |

## Descrição

**Como** Gestor de CRM

**Eu quero** visualizar uma lista de todos os cards do Buyer Agent com suas métricas principais

**Para que** eu possa avaliar rapidamente o desempenho geral das campanhas

**Critérios de Aceitação:**

- [X] Devo ver uma lista paginada com todos os cards ativos
- [X] Cada card deve mostrar: nome, categoria, impressões, taxa de conversão geral
- [X] Devo poder filtrar por categoria (exit_risk, doubt_risk, conversion_risk)
- [X] Devo poder filtrar por status (active, paused, archived)
- [X] Devo poder ordenar por diferentes métricas
- [X] A lista deve incluir dados do período selecionado
- [X] Deve haver um resumo geral das métricas na parte superior

> **[Imagem 1 — transcrição]:** Screenshot de UI — tela "Análise de Resultados" ("Performance detalhada dos cards do Buyer Agent") da plataforma SendSpeed. Cabeçalho superior direito: seletor de idioma "Português (Brasil)" (bandeira do Brasil) e avatar do usuário "Pedro / SendSpeed". Menu lateral esquerdo com itens: Início, Audiência, Segmentos, Campanhas, Fluxos, Análises, Dados e Integrações, Logs de Atividade, Conteúdo, Buyer Agent (expandido, com subitens: Cards, Criar Card, Meus Cards, Resultados), Configurações. Barra de filtros: seletor de intervalo de datas "26/05/2025 - 25/06/2025", dropdown "Todos os Status", dropdown "Todas as Categorias" e dropdown de ordenação "Nome". Quatro cards de métricas-resumo no topo: **Impressões 36.445**, **Cliques Preview 5.946**, **Cliques CTA 1.891**, **Conversões 457**. Seção "Performance por Card (3)". Primeiro card: "Dúvidas - Chat com Especialista" (tags "Dúvidas" e "Ativo") com preview laranja ("Precisa de ajuda? 🤔 / Fale com nosso especialista / Tire suas dúvidas em tempo real!" + botão verde "Ver Oferta") e um Funil de Conversão com: Impressões 8.765 → (14.1%) Preview 1.234 → (37.0%) CTA 456 → (27.0%) Conversões 123; "Conversão Geral: 1.4%". Botão "Ver Análise Detalhada". Segundo card: "Exit Intent - Oferta Especial" (tags "Saída" e "Ativo") com preview vermelho ("Espera! Não vá embora! 🛑 / Oferta especial para você / Que tal 15% de desconto na sua primeira compra?" + botão "Ver Oferta") e funil: Impressões 12.450 → (15.0%) Preview 1.867 → (29.1%) CTA 543 → (16.4%) Conversões 89; "Conversão Geral: 0.7%". Botão "Ver Análise Detalhada". No rodapé começa a aparecer um terceiro card: "Impulso Final - Urgência" (tags "Conversão" e "Ativo").

## ⚠️Melhorias sugeridas:

*  Retornar possibilidade de filtro de hora.
*  Nomear filtros

> **[Imagem 2 — transcrição]:** Screenshot de UI (recorte do topo de "Análise de Resultados" após melhorias) demonstrando as sugestões implementadas. Título "Análise de Resultados" / "Performance detalhada dos cards do Buyer Agent". À direita do título: seletor de datas "29/07/2025 – 28/08/2025" e "Períodos rápidos:" com botões "7 dias", "30 dias", "90 dias", "Este mês". Abaixo, barra de filtros agora **nomeados**: rótulo "Filtros:" seguido de três dropdowns ("Ativo", "Todas", "Todas") e rótulo "Ordenar:" com dropdown "Nome A-Z". Quatro cards de métricas: **Impressões 91** ("Total do período"), **Cliques 106** ("Interações no preview"), **CTA 77** ("Ações no botão"), **Conversões 0** ("Resultados alcançados").

## Histórico de status

- Backlog (backlog): 2025-06-25T13:36:25.187Z → 2025-07-10T12:13:34.147Z
- Pull Request (started): 2025-07-10T12:13:34.147Z → 2025-07-21T12:36:58.484Z
- In Progress (started): 2025-07-21T12:36:58.484Z → 2025-07-31T12:28:09.961Z
- Pull Request (started): 2025-07-31T12:28:09.961Z → 2025-08-11T13:53:55.195Z
- Product Review (started): 2025-08-11T13:53:55.195Z → 2025-08-13T22:11:33.421Z
- Pull Request (started): 2025-08-13T22:11:33.421Z → 2025-08-25T12:15:35.113Z
- Product Review (started): 2025-08-25T12:15:35.113Z → 2025-08-27T15:25:02.941Z
- Pull Request (started): 2025-08-27T15:25:02.941Z → 2025-09-04T19:36:42.791Z
- Released (completed): 2025-09-04T19:36:42.791Z → atual

## Relações

—

## Anexos

—
