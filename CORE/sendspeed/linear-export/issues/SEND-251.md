# SEND-251 — [MELHORIA] Criar tela de visualização de jornadas no Analytics com campos obrigatórios

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | Urgent |
| Responsável | Vinicius Carneiro |
| Time | Sendspeed |
| Projeto | — |
| Labels | — |
| Parent | — |
| Criada | 2025-11-25T18:32:59.608Z por Vinicius Carneiro |
| Iniciada | 2025-11-26T12:01:41.951Z |
| Concluída | 2025-12-03T18:48:21.607Z |
| Arquivada | 2026-06-04T22:49:16.955Z |
| Vencimento | — |
| Branch | hugofernandes/send-251-melhoria-criar-tela-de-visualizacao-de-jornadas-no-analytics |
| URL | https://linear.app/sendspeed/issue/SEND-251/melhoria-criar-tela-de-visualizacao-de-jornadas-no-analytics-com |

## Descrição

**Como analista de produto**
**Quero** uma tela no Analytics que permita selecionar ou criar uma Jornada no momento de criação do card/modal
**Para** garantir que todas as análises sejam vinculadas a um fluxo rastreável e padronizado, evitando inconsistências de dados

**Critérios de Aceite:**

* A tela deve exibir lista de Jornadas existentes para seleção.
* Deve ser possível criar uma nova Jornada diretamente nesse processo, caso não exista.
* É obrigatório que o usuário selecione ou crie a Jornada antes de finalizar a criação.
* A criação da jornada deve exigir obrigatoriamente os campos:
  * **Título** (texto)
  * **Descrição** (texto longo)
  * **Conversão Personalizada** (objeto estruturado com: nome do evento, parâmetros, regras)
* Validação deve impedir avanço sem os três campos preenchidos corretamente.
* A nova tela deve exibir:
  * Jornada selecionada
  * Nome do card/modal
  * Conversão personalizada vinculada
* O objeto de Conversão Personalizada deve ser armazenado no banco exatamente com as regras definidas pelo usuário.
* A UI deve seguir padrão atual do painel de Analytics (spacing, tipografia, componentes).
* A ação de "Criar Jornada" deve abrir modal dedicado para nome, descrição e eventos envolvidos.
* Toda interação deve ser registrada como evento:
  * `CREATE_CUSTOM_JOURNEY`
  * `SELECT_JOURNEY_FROM_CARD_CREATION`
  * `CREATE_ANALYTICS_CARD_WITH_JOURNEY`
* Deve existir feedback visual claro (sucesso/erro) em todas as operações.

## Histórico de status
- To-do (unstarted): 2025-11-25T18:32:59.608Z → 2025-11-26T12:01:41.960Z
- In Progress (started): 2025-11-26T12:01:41.960Z → 2025-12-01T18:03:00.075Z
- Pull Request (started): 2025-12-01T18:03:00.075Z → 2025-12-03T17:25:12.608Z
- Product Review (started): 2025-12-03T17:25:12.608Z → 2025-12-03T18:48:21.623Z
- Released (completed): 2025-12-03T18:48:21.623Z → atual

## Relações
—

## Anexos
—
