# SEND-320 — Bugs e melhorias Journey Builder UserIn - Regra da Plataforma com dropdown cortado e texto confuso

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | No priority |
| Responsável | paulo.ribeiro@sendspeed.com |
| Time | Sendspeed |
| Projeto | — |
| Labels | — |
| Parent | — |
| Criada | 2026-02-10T19:38:03.116Z por paulo.ribeiro@sendspeed.com |
| Iniciada | 2026-02-12T18:02:40.939Z |
| Concluída | 2026-02-18T16:26:37.719Z |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-320-bugs-e-melhorias-journey-builder-userin-regra-da-plataforma |
| URL | https://linear.app/sendspeed/issue/SEND-320/bugs-e-melhorias-journey-builder-userin-regra-da-plataforma-com |

## Descrição

**Descrição:** O componente 'Regra da Plataforma' apresenta dois problemas:

1. **Bug visual:** A caixa de seleção do dropdown AND/OR está cortada, com a borda azul de seleção não aparecendo completamente.
2. **UX confusa:** O dropdown AND/OR pode confundir o usuário que não entende lógica booleana. O texto atual "das seguintes condições" é vago e não explica a diferença entre as opções AND e OR, deixando o usuário sem clareza sobre o que cada uma faz.

> **[Imagem 1 — transcrição]:** Screenshot de UI do painel de configuração do card "Regra da Plataforma" (badge "condition", ícone laranja de checklist) com subtítulo "Aplica uma regra existente ou cria nova inline" e "X" para fechar. Seção "Tipo de Regra" com dois radios: "Usar regra existente" e "Criar nova regra inline" (selecionado). Texto "Defina as condições da regra. As mesmas opções disponíveis em Regras estão disponíveis aqui." Um dropdown "AND" (aberto, mostrando as opções "AND" — destacada em laranja com check — e "OR") ao lado do texto "das seguintes condições" e badge "0 condições". Área tracejada "Nenhuma condição definida" com botão azul "+ Primeira Condição". Caixa amarela "Saídas: Sim ou Não" com o texto "A regra será avaliada no perfil do usuário. Se as condições forem verdadeiras, segue pelo caminho 'Sim', caso contrário segue pelo 'Não'." Demonstra o dropdown AND/OR (com a borda de seleção cortada) e o texto vago "das seguintes condições".

* Corrigir o bug visual da borda cortada no dropdown
* Substituir o texto vago por descrições mais claras:
  * **\[AND\]** Todas as condições abaixo devem ser verdadeiras
  * **\[OR\]** Pelo menos uma condição abaixo deve ser verdadeira
* **Alternativa (preferencial):** Implementar toggle visual conforme mockup em anexo:

> **[Imagem 2 — transcrição]:** Imagem de mockup/anotação (fundo pontilhado) com o título "Toggle visual (alternativa ao dropdown):" e dois itens com toggles/checkboxes: um checkbox desmarcado (branco) ao lado de "TODAS verdadeiras (AND)" e um checkbox marcado/ligado (verde) ao lado de "PELO MENOS UMA verdadeira (OR)". Demonstra a alternativa preferencial: substituir o dropdown AND/OR por um toggle visual com rótulos explicativos.

## Histórico de status
- Backlog (backlog): 2026-02-10T19:38:03.116Z → 2026-02-12T14:18:52.380Z
- To-do (unstarted): 2026-02-12T14:18:52.380Z → 2026-02-12T18:02:40.955Z
- In Progress (started): 2026-02-12T18:02:40.955Z → 2026-02-12T18:20:31.312Z
- Pull Request (started): 2026-02-12T18:20:31.312Z → 2026-02-12T18:52:19.711Z
- Product Review (started): 2026-02-12T18:52:19.711Z → 2026-02-18T16:26:37.736Z
- Released (completed): 2026-02-18T16:26:37.736Z → atual

## Relações
—

## Anexos
—
