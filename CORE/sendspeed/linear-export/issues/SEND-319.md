# SEND-319 — Bugs e melhorias Journey Builder UserIn - Inputs com seleção cortada (Adicionar Tag e Atributo do Usuário)

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | No priority |
| Responsável | paulo.ribeiro@sendspeed.com |
| Time | Sendspeed |
| Projeto | — |
| Labels | — |
| Parent | — |
| Criada | 2026-02-10T19:33:07.685Z por paulo.ribeiro@sendspeed.com |
| Iniciada | 2026-02-12T15:33:39.006Z |
| Concluída | 2026-02-20T14:07:55.421Z |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-319-bugs-e-melhorias-journey-builder-userin-inputs-com-selecao |
| URL | https://linear.app/sendspeed/issue/SEND-319/bugs-e-melhorias-journey-builder-userin-inputs-com-selecao |

## Descrição

**Descrição:** Os componentes 'Adicionar Tag' e 'Atributo do Usuário' apresentam bug visual no front. A marcação azul (borda de seleção/foco) do input está cortada, não aparecendo completamente ao redor do campo. Isso prejudica a experiência visual

> **[Imagem 1 — transcrição]:** Screenshot de UI do painel de configuração do card "Atributo do Usuário" (badge "condition", ícone laranja de pessoa) com subtítulo "Verifica atributo do usuário" e "X" para fechar. Campos: "Atributo do Perfil" com dropdown "Nível de Intenção" (com borda de foco azul); "Operador" com dropdown "É igual a"; "Valor" com dropdown "Selecione o valor". No rodapé: "Tipo: enum | Caminho: intention.level". Demonstra o input com a borda de seleção azul cortada no componente Atributo do Usuário.

> **[Imagem 2 — transcrição]:** Screenshot de UI do painel de configuração do card "Adicionar Tag" (badge "action", ícone azul de etiqueta) com subtítulo "Adiciona tag ao usuário" e "X" para fechar. Bloco verde "Adicionar Tag" com o texto "Quando a jornada executar este bloco, a tag selecionada será adicionada ao perfil do usuário. A tag pode ser usada para segmentação e campanhas futuras." Campo "Selecionar tag" com input de busca (placeholder "Buscar tags...", com borda de foco azul) e abaixo um indicador de carregamento "Carregando tags...". Demonstra o input com borda de seleção azul cortada no componente Adicionar Tag.

**Sugestão de melhoria:** Ajustar o CSS dos inputs para que a borda de seleção azul apareça completamente ao redor do campo, sem cortes.

## Histórico de status
- Backlog (backlog): 2026-02-10T19:33:07.685Z → 2026-02-12T15:33:39.018Z
- Product Review (started): 2026-02-12T15:33:39.018Z → 2026-02-20T14:07:55.434Z
- Released (completed): 2026-02-20T14:07:55.434Z → atual

## Relações
—

## Anexos
—
