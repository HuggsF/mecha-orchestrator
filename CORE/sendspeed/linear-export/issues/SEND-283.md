# SEND-283 — Condições de regra baseadas na primeira, última e URL atual do usuário

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | Urgent |
| Responsável | pedro.iegler@sendspeed.com |
| Time | Sendspeed |
| Projeto | — |
| Labels | Implementação, Regras, User Story, UserIn |
| Parent | — |
| Criada | 2026-01-16T12:44:39.975Z por Vinicius Carneiro |
| Iniciada | 2026-01-19T12:34:07.967Z |
| Concluída | 2026-01-27T14:43:48.473Z |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-283-condicoes-de-regra-baseadas-na-primeira-ultima-e-url-atual |
| URL | https://linear.app/sendspeed/issue/SEND-283/condicoes-de-regra-baseadas-na-primeira-ultima-e-url-atual-do-usuario |

## Descrição

> **Como** PO
>
> **Quero** desenvolver uma nova regra.
>
> **Para** expandir as possibilidades de trigger na plataforma.

---

>>> ## Critérios de aceite:

* Deve ser possível criar uma condição de regra baseada na current URL do usuário.
* Deve ser possível criar uma condição de regra baseada na visited URL na sessão.
* Deve ser possível criar uma condição de regra baseada na last URL visitada.
* As opções de URL devem estar disponíveis de forma clara no seletor de condições, seguindo o mesmo padrão das regras existentes.
* As condições devem permitir comparação simples (ex: é igual, contém, não contém)
* A configuração deve ser compreensível para usuários não técnicos.
* A regra deve funcionar de forma consistente, respeitando o comportamento real de navegação do usuário.
* O uso dessas condições deve permitir maior controle sobre quando uma campanha ou ação é exibida.
> **[Imagem 1 — transcrição]:** Screenshot de UI da plataforma, painel "Defina as Condições da Regra". Contém um seletor lógico "AND" (dropdown) com o texto "das seguintes condições" e um badge "1 condição total". A linha de condição número 1 mostra três dropdowns em sequência: "Visualização da página", "É igual à URL" e um campo de texto com placeholder "Valor". Há um ícone de lixeira à direita para remover a condição. Abaixo, dois botões: "+ Adicionar Condição" e "+ Adicionar Grupo". Demonstra como a nova condição de URL aparece no seletor de condições da regra.

  Vai entrar entre visualização de página e É igual à URL.

>>> ### State:

* Devemos criar um State para ajudar a rastrear os eventos de maneira quase que instantânea.
* O state deve representar de forma clara o **status atual de uma interação ou contexto.**
* As regras baseadas em state devem ser **fáceis de entender.**
* O uso de state deve ajudar a **evitar repetições indevidas ou conflitos de exibição.**
* O state deve apoiar a **orquestração e rastreamento da jornada do usuário.**
* O state deve permitir **evolução futura**, suportando novos cenários e regras mais robusto.

> **[Imagem 2 — transcrição]:** Diagrama (fluxograma/esquema de estrutura de dados) com o título "Local Storage". Contém duas caixas do tipo tabela. A primeira caixa, "Buffer Events", lista um item: "events". A segunda caixa, "State", lista cinco itens: "sum_amount", "visited_url", "last_url", "current_url", "current_utm". Uma seta parte da caixa Buffer Events e aponta para a caixa State, com o rótulo "page view atualiza state". Demonstra a estrutura proposta de armazenamento no localStorage: um buffer de eventos e um objeto de estado (state) que é atualizado a cada visualização de página, contendo os campos de URL (visited, last, current), utm atual e soma de valores.

>>>

>>>

## Histórico de status
- Backlog (backlog): 2026-01-16T12:44:39.975Z → 2026-01-16T15:26:55.115Z
- To-do (unstarted): 2026-01-16T15:26:55.115Z → 2026-01-19T12:34:07.974Z
- In Progress (started): 2026-01-19T12:34:07.974Z → 2026-01-21T19:36:12.619Z
- Pull Request (started): 2026-01-21T19:36:12.619Z → 2026-01-22T12:33:33.706Z
- Product Review (started): 2026-01-22T12:33:33.706Z → 2026-01-27T14:43:48.485Z
- Released (completed): 2026-01-27T14:43:48.485Z → atual

## Relações
—

## Anexos
—
