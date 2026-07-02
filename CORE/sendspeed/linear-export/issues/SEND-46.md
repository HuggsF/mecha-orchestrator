# SEND-46 — Identificação e Ação do Buyer com Evento do Gatilho Imediato

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | No priority |
| Responsável | andrei.garcia@externo.sendspeed.com |
| Time | Sendspeed |
| Projeto | — |
| Labels | — |
| Parent | — |
| Criada | 2025-07-23T12:33:43.571Z por bruno.heidrich@sendspeed.com |
| Iniciada | 2025-07-23T19:22:05.476Z |
| Concluída | 2025-08-11T13:53:17.631Z |
| Arquivada | 2026-02-15T02:17:35.939Z |
| Vencimento | — |
| Branch | hugofernandes/send-46-identificacao-e-acao-do-buyer-com-evento-do-gatilho-imediato |
| URL | https://linear.app/sendspeed/issue/SEND-46/identificacao-e-acao-do-buyer-com-evento-do-gatilho-imediato |

## Descrição

**Como** Módulo de Buyer (tomador de decisão do sistema)
**Eu quero** receber e identificar eventos do Gatilho Imediato vindos do site
**Para que** eu possa executar ações específicas de forma autônoma, como exibir um card promocional

Critérios de Aceitação

**Cenário 1: Identificação de Evento do Gatilho Imediato**

* Dado que um evento com `type: "trigger_event"` é recebido via socket
* Quando o campo `event` for igual ao nome configurado no Gatilho Imediato
* Então o buyer deve reconhecer esse evento como um gatilho autorizado para ação

**Cenário 2: Ação do Buyer baseada no Evento**

* Dado que o evento foi identificado como um Gatilho Imediato válido
* Então o buyer deve executar a ação pré-configurada (ex: exibir card, redirecionar, exibir oferta, etc.)

**Cenário 3: Ignorar Eventos Não Vinculados**

* Dado que o buyer recebe eventos genéricos
* Quando o nome do evento **não corresponder** a nenhum gatilho imediato ativo
* Então o buyer deve **ignorar** o evento

## Histórico de status

- To-do (unstarted): 2025-07-23T12:33:43.571Z → 2025-07-23T19:22:05.461Z
- In Progress (started): 2025-07-23T19:22:05.461Z → 2025-08-11T13:53:17.612Z
- Released (completed): 2025-08-11T13:53:17.612Z → atual

## Relações

—

## Anexos

—
