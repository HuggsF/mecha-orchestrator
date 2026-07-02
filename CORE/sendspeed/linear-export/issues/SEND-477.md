# SEND-477 — MAI - 05.1 - User Story — Acionar Journey com Array de Entrada

| Campo | Valor |
| -- | -- |
| Status | To-do (unstarted) |
| Prioridade | No priority |
| Responsável | — |
| Time | Sendspeed |
| Projeto | — |
| Labels | — |
| Parent | — |
| Criada | 2026-05-18T11:13:40.062Z por pedro.antunes@sendspeed.com |
| Iniciada | — |
| Concluída | — |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-477-mai-051-user-story-acionar-journey-com-array-de-entrada |
| URL | https://linear.app/sendspeed/issue/SEND-477/mai-051-user-story-acionar-journey-com-array-de-entrada |

## Descrição

**Como** sistema externo/integrador,
**quero** acionar uma Journey da Userin enviando um **array de entradas** em uma única requisição,
**para** processar múltiplos usuários/eventos de uma vez, reduzindo chamadas unitárias, latência e custo operacional.

### Contexto

Hoje a chamada de Journey tende a ser individual. Para cenários de alto volume, como inbound de SMS/RCS, callbacks de entrega, respostas de campanha, atualizações de status ou eventos vindos de parceiros, isso gera excesso de requisições.

A evolução necessária é permitir que a Journey receba um **batch de entradas**, onde cada item do array representa um usuário, evento ou interação a ser processada.

### Exemplo de payload

```
{
  "journeyId": "journey_123",
  "source": "sendspeed",
  "entries": [
    {
      "externalId": "user_001",
      "phone": "+5521999999999",
      "channel": "SMS",
      "event": "DELIVERED",
      "messageId": "msg_001",
      "timestamp": "2026-05-18T10:30:00-03:00",
      "attributes": {
        "campaignId": "camp_123",
        "provider": "route_a"
      }
    },
    {
      "externalId": "user_002",
      "phone": "+5521988888888",
      "channel": "RCS",
      "event": "FAILED",
      "messageId": "msg_002",
      "timestamp": "2026-05-18T10:31:00-03:00",
      "attributes": {
        "error": "UNDELIVERABLE"
      }
    }
  ]
}
```

Exemplo Smartico 

```
[
  {
    "eid": "uuid-unico",
    "event_date": 1680106470149,
    "ext_brand_id": "brand-id",
    "user_ext_id": "user-id",
    "event_type": "core_personal_message",
    "payload": {
      "title": "Título",
      "short_message": "Mensagem curta",
      "channel": "sms-api"
    }
  }
]
```

### Requisitos

* A API deve aceitar **array de entradas**, não apenas uma entrada única.
* Cada item do array deve ser processado como uma execução individual da Journey.
* O endpoint deve aceitar campos flexíveis como:
  * `externalId`
  * `phone`
  * `email`
  * `channel`
  * `event`
  * `messageId`
  * `timestamp`
  * `attributes`
* O processamento deve ser assíncrono via fila.
* Deve haver validação por item, sem rejeitar o batch inteiro quando apenas um item estiver inválido.
* Deve retornar um `batchId` para rastreabilidade.
* Deve estudar e definir o tamanho seguro aceito por REST:
  * tamanho máximo do payload;
  * quantidade máxima de itens por array;
  * estratégia de chunking;
  * resposta para payload grande demais.

### Critérios de aceite

* Dado um payload com múltiplas entradas, a Userin deve criar uma execução individual para cada item válido.
* Dado um item inválido dentro do array, ele deve ser marcado como erro sem bloquear os demais.
* Dado um payload acima do limite definido, a API deve retornar erro claro, como `413 Payload Too Large`.
* Dado um batch aceito, a resposta deve conter `batchId`, quantidade recebida, quantidade aceita e quantidade rejeitada.
* Deve existir log/rastreabilidade por `batchId`, `journeyId` e item processado.

### Observação importante

Inbound SMS/RCS é apenas um **caso de uso exemplo**. A solução deve ser genérica para qualquer origem que precise disparar Journeys em lote.

## Histórico de status
- To-do (unstarted): 2026-05-18T11:13:40.062Z → 2026-06-22T17:16:53.762Z
- Released (completed): 2026-06-22T17:16:53.762Z → 2026-06-22T17:17:10.227Z
- To-do (unstarted): 2026-06-22T17:17:10.227Z → atual

## Relações
—

## Anexos
—
