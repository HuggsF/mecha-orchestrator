# SEND-45 — Envio de Evento do Card via Tracker - Gatilho Imediato

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | No priority |
| Responsável | andrei.garcia@externo.sendspeed.com |
| Time | Sendspeed |
| Projeto | — |
| Labels | — |
| Parent | — |
| Criada | 2025-07-23T12:33:14.886Z por bruno.heidrich@sendspeed.com |
| Iniciada | 2025-07-23T19:22:11.089Z |
| Concluída | 2025-08-11T13:53:19.900Z |
| Arquivada | 2026-02-15T02:17:35.498Z |
| Vencimento | — |
| Branch | hugofernandes/send-45-envio-de-evento-do-card-via-tracker-gatilho-imediato |
| URL | https://linear.app/sendspeed/issue/SEND-45/envio-de-evento-do-card-via-tracker-gatilho-imediato |

## Descrição

**Como** Desenvolvedor Frontend / Backend
**Eu quero** que os eventos disparados pelo card sejam automaticamente enviados ao socket com um identificador único
**Para que** o backend (ou o sistema de buyer) possa escutar e reagir em tempo real ao comportamento do usuário

Critérios de Aceitação

**Cenário 1: Disparo de Evento Automático ao Interagir com o Card**

* Dado que o card está configurado com um Gatilho Imediato
* Quando o usuário realiza uma ação relevante (ex: clique, envio de formulário, chamada no WhatsApp)
* Então o tracker deve capturar o evento e enviar para o socket com o nome do evento configurado

**Cenário 2: Formato de Payload para o Socket**

* Dado que um evento foi disparado
* Então o sistema deve enviar um payload no seguinte formato:

```
json

{
  "type": "trigger_event",
  "event": "nome_do_evento",
  "cardId": "1234",
  "timestamp": "2025-07-23T10:30:00Z",
  "data": { ...dados_customizados... }
}
```

**Cenário 3: Não envio quando Gatilho Imediato estiver inativo**

* Dado que o gatilho imediato está desativado
* Quando o usuário interagir com o card
* Então **nenhum evento deve ser enviado ao socket**

## Histórico de status

- To-do (unstarted): 2025-07-23T12:33:14.886Z → 2025-07-23T19:22:11.070Z
- In Progress (started): 2025-07-23T19:22:11.070Z → 2025-08-11T13:53:19.885Z
- Released (completed): 2025-08-11T13:53:19.885Z → atual

## Relações

—

## Anexos

—
