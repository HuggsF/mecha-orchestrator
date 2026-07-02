# SEND-37 — Behavior Analise Comportamental

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | Urgent |
| Responsável | andrei.garcia@externo.sendspeed.com |
| Time | Sendspeed |
| Projeto | — |
| Labels | Behavior |
| Parent | — |
| Criada | 2025-07-08T18:04:26.224Z por bruno.heidrich@sendspeed.com |
| Iniciada | 2025-07-10T12:13:08.215Z |
| Concluída | 2025-08-11T13:53:49.436Z |
| Arquivada | 2026-02-15T02:17:35.746Z |
| Vencimento | — |
| Branch | hugofernandes/send-37-behavior-analise-comportamental |
| URL | https://linear.app/sendspeed/issue/SEND-37/behavior-analise-comportamental |

## Descrição

**Como** analista de dados,
**Quero** que o sistema de análise comportamental (behavior) registre qual dado de navegação foi analisado para justificar uma decisão,
**Para que** eu possa entender, auditar e melhorar as regras de interpretação de intenção.

**Critérios de Aceitação:**

*  A decisão (ex: risco eminente de X) deve conter o racional baseado em comportamento real (ex: "usuário pausou no preço por 8s após scroll acelerado — sinal de dúvida em preço").
*  Deve existir o campo `behavior_explanation` no JSON, com linguagem legível e interpretável.
*  A explicação deve sempre citar pelo menos um evento concreto (scroll, tempo de permanência, clique, etc.).
*  A explicação precisa estar vinculada ao log da ação tomada.

## Histórico de status

- Backlog (backlog): 2025-07-08T18:04:26.224Z → 2025-07-10T12:13:08.175Z
- Product Review (started): 2025-07-10T12:13:08.175Z → 2025-08-11T13:53:49.425Z
- Released (completed): 2025-08-11T13:53:49.425Z → atual

## Relações

—

## Anexos

—
