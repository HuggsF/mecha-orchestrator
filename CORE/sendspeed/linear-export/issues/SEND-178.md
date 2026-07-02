# SEND-178 — Consulta Simplificada de Condicionais

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | Urgent |
| Responsável | Vinicius Carneiro |
| Time | Sendspeed |
| Projeto | — |
| Labels | — |
| Parent | — |
| Criada | 2025-09-26T13:59:25.069Z por bruno.heidrich@sendspeed.com |
| Iniciada | — |
| Concluída | 2025-12-03T18:52:30.555Z |
| Arquivada | 2026-06-04T22:49:18.119Z |
| Vencimento | — |
| Branch | hugofernandes/send-178-consulta-simplificada-de-condicionais |
| URL | https://linear.app/sendspeed/issue/SEND-178/consulta-simplificada-de-condicionais |

## Descrição

**Como** Head de Produto
**Quero** acessar de forma simples (via página ou endpoint) os números relacionados a usuários em diferentes condições,
**Para** ter clareza sobre comportamento e performance sem depender de consultas técnicas diretas no banco.

### Condições que devem estar disponíveis:

1. **Número de first time users VERSUS não first time users, que não se cadastraram.**
2. **Mediana de tempo de usuários que não converteram.**
3. **Mediana de tempo de usuários que converteram.**

### Critérios de Aceite

* A página ou endpoint deve exibir de forma clara os três números/condições listados.
* O cálculo da **mediana de tempo** deve estar correto (considerando sessões válidas).
* O dado deve ser atualizado em tempo real ou com SLA definido (ex.: atualização a cada X minutos).
* A solução deve ser acessível para time de produto/negócio sem necessidade de query manual no banco.
* Deve ser possível exportar ou consumir os dados em relatórios/dashboards.

## Histórico de status
- To-do (unstarted): 2025-09-26T13:59:25.069Z → 2025-10-17T14:28:12.643Z
- In Progress (started): 2025-10-17T14:28:12.643Z → 2025-10-23T18:58:11.701Z
- Pull Request (started): 2025-10-23T18:58:11.701Z → 2025-12-03T17:25:07.043Z
- Product Review (started): 2025-12-03T17:25:07.043Z → 2025-12-03T18:52:29.073Z
- Backlog (backlog): 2025-12-03T18:52:29.073Z → 2025-12-03T18:52:30.562Z
- Released (completed): 2025-12-03T18:52:30.562Z → atual

## Relações
—

## Anexos
—
