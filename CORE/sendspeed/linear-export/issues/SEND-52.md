# SEND-52 — Configuração de tempo de exibição do preview no gatilho imediato

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | Medium |
| Responsável | andrei.garcia@externo.sendspeed.com |
| Time | Sendspeed |
| Projeto | — |
| Labels | Buyer |
| Parent | — |
| Criada | 2025-08-13T22:00:31.274Z por bruno.heidrich@sendspeed.com |
| Iniciada | 2025-08-20T12:13:23.224Z |
| Concluída | 2025-08-27T15:24:58.721Z |
| Arquivada | 2026-03-01T02:17:26.046Z |
| Vencimento | — |
| Branch | hugofernandes/send-52-configuracao-de-tempo-de-exibicao-do-preview-no-gatilho |
| URL | https://linear.app/sendspeed/issue/SEND-52/configuracao-de-tempo-de-exibicao-do-preview-no-gatilho-imediato |

## Descrição

* **Como** operador de Marketing configurando um gatilho imediato,
* **Quero** definir o tempo de exibição do preview do card na tela do cliente,
* **Para** controlar quanto tempo o preview será exibido antes de desaparecer, garantindo melhor experiência e adaptação ao contexto.

**Critérios de Aceite:**

1. Dentro da etapa de configuração do **Gatilho Imediato**, deve existir um campo para definir o tempo de exibição do preview (em segundos).
2. O valor padrão (default) deve ser **5 segundos**.
3. O campo deve ser **acionável** (o usuário consegue alterar o valor).
4. Alterações devem ser salvas junto às configurações do gatilho imediato.
5. O comportamento no front-end deve respeitar o tempo configurado, exibindo o preview pelo período definido e depois removendo-o.

**Restrições e Considerações Técnicas:**

* O valor mínimo permitido: 3 segundos.
* O valor máximo permitido: 15 segundos.
* Validar input (apenas números inteiros positivos dentro do range definido).

## Histórico de status
- Backlog (backlog): 2025-08-13T22:00:31.274Z → 2025-08-13T22:10:29.507Z
- To-do (unstarted): 2025-08-13T22:10:29.507Z → 2025-08-20T12:13:23.213Z
- In Progress (started): 2025-08-20T12:13:23.213Z → 2025-08-22T12:08:16.407Z
- Product Review (started): 2025-08-22T12:08:16.407Z → 2025-08-27T15:24:58.704Z
- Released (completed): 2025-08-27T15:24:58.704Z → atual

## Relações
—

## Anexos
—
