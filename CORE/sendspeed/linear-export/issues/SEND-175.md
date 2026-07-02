# SEND-175 — Kafka em STG

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | Urgent |
| Responsável | pedro.iegler@sendspeed.com |
| Time | Sendspeed |
| Projeto | — |
| Labels | — |
| Parent | — |
| Criada | 2025-09-26T12:03:45.272Z por bruno.heidrich@sendspeed.com |
| Iniciada | 2025-10-13T14:40:43.328Z |
| Concluída | 2025-11-14T13:59:14.912Z |
| Arquivada | 2026-05-20T22:16:09.554Z |
| Vencimento | — |
| Branch | hugofernandes/send-175-kafka-em-stg |
| URL | https://linear.app/sendspeed/issue/SEND-175/kafka-em-stg |

## Descrição

**Como** Head de Produto
**Quero** que o Kafka esteja ativo e funcional no ambiente STG (produção),
**Para** que todo o processamento de eventos (sessão, conversão, interações) seja registrado e possa ser utilizado nas regras de negócio do produto.

**Critérios de Aceite:**

* Kafka rodando no STG, sem gargalos de ingestão.
* Tópicos e consumidores configurados para receber todos os eventos necessários.
* Logs e métricas acessíveis para monitoramento da operação.
* Eventos fluindo end-to-end (do site até a collection final).

> **[Imagem 1 — transcrição]:** Diagrama de arquitetura (estilo quadro branco / draw.io, fundo claro) mostrando dois cenários de fluxo de dados.
> - À esquerda, um bloco verde ("KAFKA implementado" ou similar, texto pequeno) conecta-se por linhas a três caixas laranjas de anotação empilhadas: "tracker não grava mais direto no mongo /api", "tabela events sendo populada pelo conector /api" e "tabela events sendo populada pelo conector kafka". Abaixo há uma caixa cinza: "Behavior lendo via ksql do kafka".
> - À direita, um segundo diagrama de fluxo: caixa "/api" (laranja) conecta-se a um bloco "mongo" (círculo vermelho com um "X" grande sobreposto, indicando que a gravação direta no mongo está desabilitada/removida). Abaixo, "/api" também conecta a "kafka" (laranja), que via rótulo "Conector" liga-se a outra caixa "mongo" (laranja) à direita. Ou seja, o fluxo passa a ser api → kafka → conector → mongo, em vez de api → mongo direto.

## Histórico de status
- To-do (unstarted): 2025-09-26T12:03:45.272Z → 2025-10-10T15:03:37.278Z
- In Progress (started): 2025-10-10T15:03:37.278Z → 2025-10-10T15:07:25.628Z
- To-do (unstarted): 2025-10-10T15:07:25.628Z → 2025-10-13T14:40:43.336Z
- In Progress (started): 2025-10-13T14:40:43.336Z → 2025-10-21T17:23:03.185Z
- Pull Request (started): 2025-10-21T17:23:03.185Z → 2025-11-10T13:16:36.534Z
- Product Review (started): 2025-11-10T13:16:36.534Z → 2025-11-14T13:59:14.934Z
- Released (completed): 2025-11-14T13:59:14.934Z → atual

## Relações
—

## Anexos
—
