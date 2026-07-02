# SEND-24 — Behavior Agent: decisão de agir e notificação em tempo-real

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | Urgent |
| Responsável | — |
| Time | Sendspeed |
| Projeto | — |
| Labels | Behavior |
| Parent | — |
| Criada | 2025-06-10T18:20:47.243Z por pedro.antunes@sendspeed.com |
| Iniciada | — |
| Concluída | 2025-07-10T12:18:31.163Z |
| Arquivada | 2026-06-03T22:53:18.586Z |
| Vencimento | — |
| Branch | hugofernandes/send-24-behavior-agent-decisao-de-agir-e-notificacao-em-tempo-real |
| URL | https://linear.app/sendspeed/issue/SEND-24/behavior-agent-decisao-de-agir-e-notificacao-em-tempo-real |

## Descrição

**Como** Behavior Agent
**Quero** analisar o lote de eventos recebido do Buffer Manager e:

* **se** `intent == true`(confirmar!??)  **emitir** o evento Socket.IO `behavior_shouldact_<localStorageID>` com o resultado da análise;
* **se** `intent == false` **persistir** a análise no banco de dados **e** registrar mensagem de debug;
  **Para** acionar componentes downstream quando necessário **e** manter histórico completo de decisões (positivas **e** negativas) por usuário.

## Critérios de Aceitação (Gherkin)

| \# | Cenário | Dado | Quando | Então |
| -- | -- | -- | -- | -- |
| 1 | **Recepção de lote** | que o Behavior Agent esteja online | lote chega via `socket.on('intent_candidate:<localStorageID>')` | ele executa `analyzeIntent(lote)` |
| 2 | **Decisão positiva** | que `analyzeIntent` retorne `intent: true` | após processamento | emite em ≤ 50 ms o evento `behavior_shouldact_<localStorageID>` com payload completo |
| 3 | **Decisão negativa** | que `intent == false` | após processamento | **não** emite evento; **insere** documento na coleção/tabla `behavior_analyses` e grava log nível DEBUG `"Intent FALSE – análise salva"` |
| 4 | **Persistência** | — | análise (true **ou** false) concluída | persiste registro com campos:&#10;`json { "localStorageID": "...", "intent": true/false, "score": 0.82, "reason": "...", "eventsAnalyzed": 6, "timestamp": "..." }` |

## Histórico de status

- Backlog (backlog): 2025-06-10T18:20:47.243Z → 2025-06-10T18:50:10.877Z
- To-do (unstarted): 2025-06-10T18:50:10.877Z → 2025-07-10T12:18:31.151Z
- Released (completed): 2025-07-10T12:18:31.151Z → atual

## Relações

—

## Anexos

—
