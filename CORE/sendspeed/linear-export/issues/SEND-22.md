# SEND-22 — Tracker Agent: emissão de eventos via Socket + persistência MongoDB

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | Urgent |
| Responsável | — |
| Time | Sendspeed |
| Projeto | — |
| Labels | Tracker |
| Parent | — |
| Criada | 2025-06-10T18:03:36.404Z por pedro.antunes@sendspeed.com |
| Iniciada | — |
| Concluída | 2025-07-10T12:19:09.873Z |
| Arquivada | 2026-01-18T02:05:01.838Z |
| Vencimento | — |
| Branch | hugofernandes/send-22-tracker-agent-emissao-de-eventos-via-socket-persistencia |
| URL | https://linear.app/sendspeed/issue/SEND-22/tracker-agent-emissao-de-eventos-via-socket-persistencia-mongodb |

## Descrição

**Como** *Tracker Agent*
**Quero** emitir **todos** os eventos de tracking para um canal Socket IO com o padrão `tracker_<localStorageID>` **e** gravá-los no MongoDB
**Para** que outros agentes (Buffer/Behavior, Buyer, dashboards, etc.) recebam esses eventos em tempo real e possamos manter um histórico confiável para análises posteriores.

### 🎯 Critérios de Aceitação 

| \# | Cenário | Dado | Quando | Então |
| -- | -- | -- | -- | -- |
| 1 | **Identificação do usuário** | que o visitante acessa o site sem `localStorageID` | o Tracker é inicializado | é gerado um UUID, salvo em `localStorage` e usado como `<localStorageID>` |
| 2 | **Re-uso do ID** | que o visitante já possua `localStorageID` | o Tracker é inicializado | o ID existente é reutilizado |
| 3 | **Conexão ao Socket.IO** | que o Tracker tenha `<localStorageID>` | o usuário carrega a primeira página da sessão | o Tracker conecta-se ao Socket.IO e ingressa no canal/room `tracker_<localStorageID>` |
| 4 | **Emissão de eventos** | que um evento de tracking (`page_view`, `click`, etc.) ocorra | o evento é capturado pelo Tracker | o Tracker **publica** a mensagem JSON completa no canal `tracker_<localStorageID>` **em ≤ 50 ms** |
| 5 | **Persistência** | que o evento seja publicado no socket | — | o mesmo payload é inserido na coleção `tracker_events` no MongoDB com carimbo de data/hora |

## Histórico de status

- Backlog (backlog): 2025-06-10T18:03:36.404Z → 2025-06-10T18:50:17.142Z
- To-do (unstarted): 2025-06-10T18:50:17.142Z → 2025-07-10T12:19:09.859Z
- Released (completed): 2025-07-10T12:19:09.859Z → atual

## Relações

—

## Anexos

—
