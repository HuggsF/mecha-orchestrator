# SEND-322 — Bugs e melhorias Journey Builder UserIn - Ir para Jornada com conteúdo cortado

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | No priority |
| Responsável | paulo.ribeiro@sendspeed.com |
| Time | Sendspeed |
| Projeto | — |
| Labels | — |
| Parent | — |
| Criada | 2026-02-11T18:18:03.384Z por paulo.ribeiro@sendspeed.com |
| Iniciada | 2026-02-12T16:31:07.893Z |
| Concluída | 2026-02-18T17:20:59.865Z |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-322-bugs-e-melhorias-journey-builder-userin-ir-para-jornada-com |
| URL | https://linear.app/sendspeed/issue/SEND-322/bugs-e-melhorias-journey-builder-userin-ir-para-jornada-com-conteudo |

## Descrição

**Descrição:** O componente 'Ir para Jornada' apresenta bug visual no front. O conteúdo do lado direito está sendo cortado, impedindo que o usuário veja completamente as informações, badges de status (InSite, Ativo, pause) e possivelmente outros elementos da interface.

> **[Imagem 1 — transcrição]:** Screenshot de UI do painel de configuração do card "Ir para Jornada" (badge "flow", ícone roxo de link externo) com subtítulo "Redireciona para outra jornada" e "X" para fechar. Bloco roxo "Ir para Jornada" com o texto "Redireciona o usuário para outra jornada. Este ramo da jornada atual será encerrado, mas outros ramos paralelos continuarão executando." Campo de busca "Buscar jornadas..." com filtros "Todas" (selecionado), "InSite", "OffSite". Lista de jornadas, cada uma com ícone roxo e badges "InSite" e "Ativo" (à direita, parcialmente cortados): "Nova Jornada", "[VC] TESTE DEPÓSITO", "[VC] TESTE UTM", "Smart Block nova Jornada". Caixa de nota: "Nota: Você pode redirecionar entre tipos diferentes: InSite para OffSite: A jornada OffSite será executada via API; OffSite para InSite: O trigger será acionado na próxima visita do usuário." e "Jornadas inativas: Você pode selecionar jornadas em rascunho. Quando ativar esta jornada, as jornadas de destino também serão consideradas." Botões no rodapé: "Clonar", "Cancelar", "Salvar Configuração". Demonstra o conteúdo/badges do lado direito sendo cortados no modal "Ir para Jornada".

**Sugestão de melhoria:** Ajustar a largura do modal implementar responsividade adequada para garantir que todo o conteúdo seja visível.

## Histórico de status
- Backlog (backlog): 2026-02-11T18:18:03.384Z → 2026-02-12T14:13:33.049Z
- To-do (unstarted): 2026-02-12T14:13:33.049Z → 2026-02-12T16:31:07.911Z
- In Progress (started): 2026-02-12T16:31:07.911Z → 2026-02-12T18:20:29.728Z
- Pull Request (started): 2026-02-12T18:20:29.728Z → 2026-02-12T18:52:20.829Z
- Product Review (started): 2026-02-12T18:52:20.829Z → 2026-02-18T17:20:59.876Z
- Released (completed): 2026-02-18T17:20:59.876Z → atual

## Relações
—

## Anexos
—
