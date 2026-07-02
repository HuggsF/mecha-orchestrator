# SEND-504 — [callback-sms] ⏳ Aguardar documentação FastTrack — ajustar payload, auth e campos

| Campo | Valor |
| -- | -- |
| Status | To-do (unstarted) |
| Prioridade | High |
| Responsável | andrei.garcia@externo.sendspeed.com |
| Time | Sendspeed |
| Projeto | — |
| Labels | Tech Story |
| Parent | SEND-488 |
| Criada | 2026-06-15T18:45:45.923Z por andrei.garcia@externo.sendspeed.com |
| Iniciada | — |
| Concluída | — |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-504-callback-sms-aguardar-documentacao-fasttrack-ajustar-payload |
| URL | https://linear.app/sendspeed/issue/SEND-504/callback-sms-aguardar-documentacao-fasttrack-ajustar-payload-auth-e |

## Descrição

## Contexto

A documentação oficial da API de webhook/callback do FastTrack ainda não foi disponibilizada. Diversas decisões técnicas estão bloqueadas até o recebimento desta documentação.

## O que esta task cobre

Esta task serve como **ponto de coleta** de todas as incógnitas que dependem da doc FastTrack. Quando a doc chegar, revisar cada item abaixo e criar tasks de ajuste conforme necessário.

## Incógnitas abertas

### Autenticação

- [ ] Como o FastTrack autentica o POST de callback recebido? (Bearer token? Signature header? IP allowlist?)
- [ ] O `api_key` é enviado como query param (`?api_key=`) ou no header? Ou ambos?
- [ ] Há algum segredo compartilhado para validação de assinatura?

### Payload do POST

- [ ] O formato `[{ "messageId": "...", "status": "..." }]` é aceito pelo FastTrack?
- [ ] O campo `crm_message_id` deve aparecer no payload?
- [ ] Há campos obrigatórios adicionais (ex: `timestamp`, `event_type`)?
- [ ] O array deve ter exatamente 1 item ou pode ser batch?

### Resposta esperada

- [ ] Qual HTTP status code indica sucesso? (200? 204?)
- [ ] Quais status codes devem acionar retry? (429? 5xx?)
- [ ] Há resposta no body que precise ser interpretada?

### Status/De-para

- [ ] O FastTrack aceita os mesmos valores de status que o Smartico (`delivered`, `failed`, `undelivered`)?
- [ ] Precisa de tabela `crm_callback_status_mappings` com mapeamento específico FastTrack?

### Ambiente

- [ ] URL de sandbox para testes?
- [ ] URL de produção?

## Ação

Quando a doc for recebida:

1. Anexar no issue SEND-488 (ref: https://linear.app/sendspeed/issue/SEND-488/integracao-com-crm-fasttrack)
2. Revisar e atualizar as tasks:
   * `[callback-sms] Implementar FastTrackClient`
   * `[callback-sms] Atualizar SmarticoPayloadBuilder ou criar CrmPayloadBuilder por CRM`
3. Criar tasks adicionais se necessário (ex: nova tabela de de/para, validação de assinatura)

## Histórico de status
- Backlog (backlog): 2026-06-15T18:45:45.923Z → 2026-06-17T12:23:43.690Z
- To-do (unstarted): 2026-06-17T12:23:43.690Z → atual

## Relações
- Blocks: SEND-503 — [callback-sms] Atualizar SmarticoPayloadBuilder ou criar CrmPayloadBuilder por CRM
- Blocks: SEND-499 — [callback-sms] Implementar FastTrackClient — cliente HTTP para callbacks FastTrack

## Anexos
—
