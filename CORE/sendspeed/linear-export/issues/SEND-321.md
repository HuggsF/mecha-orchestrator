# SEND-321 — Bugs e melhorias Journey Builder UserIn - Remover Tag com seleção múltipla bugada

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | No priority |
| Responsável | paulo.ribeiro@sendspeed.com |
| Time | Sendspeed |
| Projeto | — |
| Labels | — |
| Parent | — |
| Criada | 2026-02-10T19:57:44.362Z por paulo.ribeiro@sendspeed.com |
| Iniciada | 2026-02-12T16:47:36.560Z |
| Concluída | 2026-02-18T16:27:40.528Z |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-321-bugs-e-melhorias-journey-builder-userin-remover-tag-com |
| URL | https://linear.app/sendspeed/issue/SEND-321/bugs-e-melhorias-journey-builder-userin-remover-tag-com |

## Descrição

**Descrição:** O componente 'Remover Tag' apresenta um bug crítico de seleção:

1. **Limitação de seleção:** Só é possível selecionar uma tag por vez para remover, mesmo que o usuário precise remover múltiplas tags.
2. **Bug de seleção em massa:** Quando o usuário seleciona uma tag e clica no 'X' para deletá-la, todas as outras tags da lista ficam vermelhas e aparecem como selecionadas simultaneamente, mesmo sem o usuário ter clicado nelas. Isso gera confusão sobre quais tags serão realmente removidas.

> **[Imagem 1 — transcrição]:** Screenshot de UI do painel de configuração do card "Remover Tag" (badge "action", ícone azul) com subtítulo "Remove tag do usuário" e "X" para fechar. Bloco vermelho/rosa "Remover Tag" com o texto "Quando a jornada executar este bloco, a tag selecionada será removida do perfil do usuário. Útil para limpar segmentações ou atualizar o estado do usuário." Seção "Tag a remover" mostrando um chip "Alta Intenção" (texto tachado/riscado, com ícone de lixeira) e um "X" ao lado. Seção "Trocar tag" com input de busca "Buscar tags..." e uma lista de tags (chips coloridos com ícone de engrenagem): "Alta Intenção" (destacada/selecionada em vermelho com check), "Média Intenção", "Baixa Intenção", "Whale", "Hot Lead", "High Roller", "Ready to Convert", "Big FTD". Demonstra o estado normal de seleção de uma única tag para remover.

> **[Imagem 2 — transcrição]:** Screenshot de UI do painel "Remover Tag" (badge "action") mesmo componente, subtítulo "Remove tag do usuário", "X" para fechar. Bloco vermelho "Remover Tag" com o mesmo texto explicativo. Seção "Selecionar tag para remover" com input "Buscar tags..." e a lista de tags TODAS marcadas com check e com borda/estado vermelho de seleção simultaneamente: "Alta Intenção", "Média Intenção", "Baixa Intenção", "Whale", "Hot Lead", "High Roller", "Ready to Convert", "Big FTD". Demonstra o BUG: ao tentar deletar uma tag, todas as tags aparecem selecionadas (vermelhas/com check) ao mesmo tempo.

**Sugestão de melhoria:**

* Corrigir o bug que faz todas as tags ficarem selecionadas ao tentar deletar apenas uma
* Implementar seleção múltipla funcional, permitindo que o usuário selecione várias tags de uma vez para remover
* Adicionar opção "Selecionar todas" para facilitar a remoção em massa quando necessário
* Garantir feedback visual claro de quais tags estão realmente selecionadas

## Histórico de status
- Backlog (backlog): 2026-02-10T19:57:44.362Z → 2026-02-12T14:16:01.066Z
- To-do (unstarted): 2026-02-12T14:16:01.066Z → 2026-02-12T16:47:36.568Z
- In Progress (started): 2026-02-12T16:47:36.568Z → 2026-02-12T18:20:30.668Z
- Pull Request (started): 2026-02-12T18:20:30.668Z → 2026-02-12T18:52:20.321Z
- Product Review (started): 2026-02-12T18:52:20.321Z → 2026-02-18T16:27:40.576Z
- Released (completed): 2026-02-18T16:27:40.576Z → atual

## Relações
—

## Anexos
—
