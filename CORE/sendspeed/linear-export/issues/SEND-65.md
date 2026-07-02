# SEND-65 — [LEGADO] LOST LIST

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | Urgent |
| Responsável | andrei.garcia@externo.sendspeed.com |
| Time | Sendspeed |
| Projeto | — |
| Labels | — |
| Parent | — |
| Criada | 2025-08-22T13:59:22.755Z por bruno.heidrich@sendspeed.com |
| Iniciada | 2025-08-27T15:05:04.327Z |
| Concluída | 2025-09-03T23:10:04.941Z |
| Arquivada | 2026-03-05T02:15:24.095Z |
| Vencimento | — |
| Branch | hugofernandes/send-65-legado-lost-list |
| URL | https://linear.app/sendspeed/issue/SEND-65/legado-lost-list |

## Descrição

**Como** responsável pelas campanhas de SMS, 
**Quero** que o sistema mantenha automaticamente uma "Lost List" de números que não funcionam (inválidos, inexistentes ou bloqueados) e ignore esses números nos envios 
**Para** evitar gasto desnecessário e melhorar a taxa de entrega.

**Critérios de aceite (testáveis)**

* Antes de cada envio, números presentes na Lost List **não recebem** SMS e o resumo mostra **quantos foram ignorados** e o motivo "Lost List".
* Um número entra na Lost List quando tiver **2 falhas seguidas e definitivas** de entrega dentro de **7 dias** (ex.: número inexistente/bloqueado).
* **Falhas temporárias** (ex.: caixa cheia/ocupado) **não** colocam o número na Lost List.
* É possível **desbloquear manualmente** um número (remover da Lost List) com registro simples de **quem** e **por quê**.
* É possível **buscar e exportar** a Lost List em **CSV**.
* Existe um **resumo** com total de números na Lost List e **economia estimada** de envios evitados.

> **[Imagem 1 — transcrição]:** Diagrama de arquitetura/fluxo (quadro branco estilo draw.io) descrevendo o funcionamento da Lost List. Elementos e rótulos legíveis: uma caixa "Envio CSV" à esquerda; um banco de dados verde "Redis / Cache ? is_lostlist" com nota "cache lostlist:<numero>"; uma caixa de decisão central "Está na lost list?" com ramo rotulado "Não" que segue para um elemento vertical "Queue"; da Queue saem setas para três caixas "Envio Msg" (à direita). Da decisão, ramo "Sim" segue (linha curva) até um banco de dados verde grande à direita com texto "Guardado na campanha os números que não foram enviados por está na Lost List". Há também uma seta da decisão para uma caixa "Não envia e marca status como <Não_entregue>", e um cilindro verde central "Lost List". No canto inferior esquerdo, uma caixa "Script Query Colocar Todos números que deram rejeitado 2x" apontando para o cilindro "Lost List". Ilustra a lógica de verificação, cache, enfileiramento e persistência dos números da Lost List.

## Histórico de status
- To-do (unstarted): 2025-08-22T13:59:22.755Z → 2025-08-27T15:05:04.306Z
- In Progress (started): 2025-08-27T15:05:04.306Z → 2025-08-29T12:52:23.533Z
- Product Review (started): 2025-08-29T12:52:23.533Z → 2025-09-03T23:10:04.926Z
- Released (completed): 2025-09-03T23:10:04.926Z → atual

## Relações
—

## Anexos
—
