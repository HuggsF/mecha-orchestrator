# SEND-248 — [MELHORIA] Persistir registro padronizado no banco userin_hooks através da AntiCorruptionLayer (UserIn Endpoint)

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | Urgent |
| Responsável | Vinicius Carneiro |
| Time | Sendspeed |
| Projeto | — |
| Labels | — |
| Parent | — |
| Criada | 2025-11-18T14:40:49.144Z por Vinicius Carneiro |
| Iniciada | 2025-11-18T19:02:38.755Z |
| Concluída | 2025-12-01T21:04:10.526Z |
| Arquivada | 2026-06-04T22:49:16.062Z |
| Vencimento | — |
| Branch | hugofernandes/send-248-melhoria-persistir-registro-padronizado-no-banco |
| URL | https://linear.app/sendspeed/issue/SEND-248/melhoria-persistir-registro-padronizado-no-banco-userin-hooks-atraves |

## Descrição

**Como analista de produto**
**Quero** que a AntiCorruptionLayer receba os dados transformados do endpoint UserIn e insira de forma padronizada um registro na tabela **userin_hooks**
**Para** garantir consistência dos dados de registro, rastreabilidade do usuário e integração confiável com SmartX, CRM e outros módulos dependentes.

**Critérios de Aceite:**

* A AntiCorruptionLayer deve receber um payload contendo no mínimo:
  * `type` (valor fixo "register")
  * `externalId` (email ou ID unificado da casa)
  * `companyId`
  * Qualquer outro metadado obrigatório definido pelo schema.
* A camada deve normalizar o payload (campos, formato, casing, validações).
* O registro deve ser salvo em **userin_hooks** exatamente no formato:

  ```
  {
    "type": "register",
    "externalId": "...",
    "companyId": "..."
  }

  ```
* A escrita no banco deve ser **idempotente**: múltiplas chamadas com o mesmo externalId não podem gerar duplicações.
* A AntiCorruptionLayer deve validar a apiKey antes de aceitar a operação.
* Em caso de dados inválidos, o endpoint deve retornar erro padronizado sem interromper outros fluxos do sistema.
* A operação deve registrar logs contendo:
  * payload recebido
  * payload transformado
  * status da operação no banco
* A inserção deve funcionar tanto para registros novos quanto para atualizações (upsert).
* Os dados devem ficar imediatamente disponíveis para outros serviços que dependem de userin_hooks.

## Histórico de status
- To-do (unstarted): 2025-11-18T14:40:49.144Z → 2025-11-18T19:02:38.766Z
- In Progress (started): 2025-11-18T19:02:38.766Z → 2025-11-25T16:38:00.937Z
- Pull Request (started): 2025-11-25T16:38:00.937Z → 2025-11-26T19:55:15.408Z
- Product Review (started): 2025-11-26T19:55:15.408Z → 2025-12-01T21:04:10.543Z
- Released (completed): 2025-12-01T21:04:10.543Z → atual

## Relações
—

## Anexos
—
