# SEND-220 — SENDSPEED LEGADO - SHORTCODE LINK DEDICADO

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | No priority |
| Responsável | — |
| Time | Sendspeed |
| Projeto | — |
| Labels | — |
| Parent | — |
| Criada | 2025-10-14T20:01:12.035Z por Hugo Fernandes |
| Iniciada | — |
| Concluída | 2025-10-31T13:35:59.795Z |
| Arquivada | 2026-05-06T22:26:32.830Z |
| Vencimento | — |
| Branch | hugofernandes/send-220-sendspeed-legado-shortcode-link-dedicado |
| URL | https://linear.app/sendspeed/issue/SEND-220/sendspeed-legado-shortcode-link-dedicado |

## Descrição

Configurar novo fornecedor de envios de SMS - Infobip link dedicado

[https://api.sendspeed.com/api?i=1136&token=5b70d8ce741a665973d3&dedicated=true](<https://api.sendspeed.com/api?i=1136&token=5b70d8ce741a665973d3&dedicated=true>)  -> quando vier isso na url, cria uma campanha do dia e joga nela todos sms , essa campanha sera criada com supplier_Sms_iD da inforbip (
seria interessante vir nesse ilink tb a identificacao de qual fornecedor usaria  o link dedicado visto q no futuro poderia ter pushfy dedicada ou sona)
ficaria assim [https://api.sendspeed.com/api?i=1136&token=5b70d8ce741a665973d3&dedicated=true&supplier=infobip](<https://api.sendspeed.com/api?i=1136&token=5b70d8ce741a665973d3&dedicated=true&supplier=infobip>)
quando isso estiver funcional deixa o cliente setado na rota normal dele os sms que vao entrando caem na campanha do dia que pega o supplier_sms_id do padrao do cliente se vier para link dedicado joga na outra campanha
enquanto isso nao estiver 100% mudaremos no cliente o supplier padrao dele para a nova rota dedicada e a donald ja passaria a enviar por la

## Histórico de status
- Backlog (backlog): 2025-10-14T20:01:12.035Z → 2025-10-31T13:35:59.807Z
- Released (completed): 2025-10-31T13:35:59.807Z → atual

## Relações
—

## Anexos
—
