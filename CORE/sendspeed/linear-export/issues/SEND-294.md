# SEND-294 — detalhe tecnico da solucao de melhoria implementada

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | No priority |
| Responsável | andrei.garcia@externo.sendspeed.com |
| Time | Sendspeed |
| Projeto | — |
| Labels | — |
| Parent | SEND-292 |
| Criada | 2026-01-30T13:08:51.476Z por andrei.garcia@externo.sendspeed.com |
| Iniciada | 2026-01-30T13:09:32.825Z |
| Concluída | 2026-03-02T12:29:00.186Z |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-294-detalhe-tecnico-da-solucao-de-melhoria-implementada |
| URL | https://linear.app/sendspeed/issue/SEND-294/detalhe-tecnico-da-solucao-de-melhoria-implementada |

## Descrição

Segue em anexo o doc de melhoria da otp de disparo do sistema, foi implementado nos Supplier da Sona e Pushfy,

fica faltando implementar um nosso Supplier para infobip e adicionar o worker dedicado deles pois o infobip ainda usa um formado antigo que nao tinha classe.

Durante os teste percebi um atraso grande por parte de API em inserir o SMS no banco o que inviabiliza o disparo OTP, temo que conversar com Hugo e adiiconar uma demanda na planing para ele sobre isso.

Para fins de testes criar uma campanha csv na plataforma e testar com a rota da Sona OTP e PushfyOtp sms disponiveis no backoffice.

> **[Anexo (referência de arquivo, não imagem)]:** `<linear-embed node-type="file">` — Nome: **doc-otp.md** (mimetype: text/markdown, tamanho: 19798 bytes, uploadId: upload-1769778393117-v157r6z). href: https://uploads.linear.app/5f8b6dbb-28f3-4684-97e5-bb9afb36f53a/1c329883-56c5-48bc-a312-2ebf4833ddc3/4059dc68-9434-4ac7-8841-f6d71d7f3684 (URL assinada, expira)

## Histórico de status
- Paused (unstarted): 2026-01-30T13:08:51.476Z → 2026-01-30T13:09:32.841Z
- Product Review (started): 2026-01-30T13:09:32.841Z → 2026-03-02T12:29:00.196Z
- Released (completed): 2026-03-02T12:29:00.196Z → atual

## Relações
—

## Anexos
- doc-otp.md (text/markdown, 19798 bytes) — https://uploads.linear.app/5f8b6dbb-28f3-4684-97e5-bb9afb36f53a/1c329883-56c5-48bc-a312-2ebf4833ddc3/4059dc68-9434-4ac7-8841-f6d71d7f3684 (URL assinada, expira)
