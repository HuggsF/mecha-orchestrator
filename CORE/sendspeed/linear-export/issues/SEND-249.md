# SEND-249 — [MELHORIA] Validação e autenticação do fluxo de registro via módulo webHookCactus usando apiKey

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | Urgent |
| Responsável | Vinicius Carneiro |
| Time | Sendspeed |
| Projeto | — |
| Labels | — |
| Parent | — |
| Criada | 2025-11-18T14:41:24.470Z por Vinicius Carneiro |
| Iniciada | 2025-11-25T16:38:04.496Z |
| Concluída | 2025-12-01T21:04:14.968Z |
| Arquivada | 2026-06-04T22:49:14.986Z |
| Vencimento | — |
| Branch | hugofernandes/send-249-melhoria-validacao-e-autenticacao-do-fluxo-de-registro-via |
| URL | https://linear.app/sendspeed/issue/SEND-249/melhoria-validacao-e-autenticacao-do-fluxo-de-registro-via-modulo |

## Descrição

**Como analista de produto**
**Quero** que o módulo **webHookCactus** autentique e valide todas as requisições recebidas do Webhook User Register através de uma **apiKey dedicada**
**Para** garantir segurança, integridade dos dados e permitir que somente chamadas autorizadas sigam para a AntiCorruptionLayer.

**Critérios de Aceite:**

> * O módulo webHookCactus deve receber o payload enviado pelo Webhook User Register.
> * A requisição deve **obrigatoriamente** incluir uma apiKey válida.
> * A apiKey deve ser verificada antes de qualquer processamento.
> * Requisições sem apiKey ou com apiKey inválida devem ser **bloqueadas imediatamente**, retornando erro padronizado (ex.: `401 – Unauthorized`).
> * Em caso de sucesso, o payload deve ser encaminhado integralmente para a AntiCorruptionLayer.
> * O módulo deve registrar logs contendo:
>   * apiKey recebida (masculada)
>   * origem da requisição
>   * payload recebido
>   * status da validação
> * O módulo não deve alterar o conteúdo do payload; apenas validar e repassar.
> * O sistema deve permitir rotação da apiKey sem impacto no fluxo (ex.: hot swap com chave antiga + nova).
> * Necessário garantir resiliência: falha na validação não pode travar filas ou bloquear outros serviços conectados.
> * O módulo precisa operar de forma idempotente: chamadas duplicadas com mesma apiKey/payload não devem produzir múltiplos encadeamentos posteriores.

## Histórico de status
- To-do (unstarted): 2025-11-18T14:41:24.470Z → 2025-11-25T16:38:04.506Z
- Pull Request (started): 2025-11-25T16:38:04.506Z → 2025-11-26T19:55:17.005Z
- Product Review (started): 2025-11-26T19:55:17.005Z → 2025-12-01T21:04:14.978Z
- Released (completed): 2025-12-01T21:04:14.978Z → atual

## Relações
—

## Anexos
—
