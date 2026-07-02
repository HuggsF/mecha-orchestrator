# SEND-508 — 2. Integração de OTP via WhatsApp

| Campo | Valor |
| -- | -- |
| Status | To-do (unstarted) |
| Prioridade | No priority |
| Responsável | — |
| Time | Sendspeed |
| Projeto | — |
| Labels | Sendspeed |
| Parent | — |
| Criada | 2026-06-16T12:33:21.911Z por Vinicius Carneiro |
| Iniciada | — |
| Concluída | — |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-508-2-integracao-de-otp-via-whatsapp |
| URL | https://linear.app/sendspeed/issue/SEND-508/2-integracao-de-otp-via-whatsapp |

## Descrição

> **Como** cliente integrador da SendSpeed **Quero** enviar códigos OTP aos meus usuários via WhatsApp através da plataforma **Para** autenticar usuários por um canal de alta entregabilidade e leitura, reduzindo falhas de autenticação que ocorrem hoje via SMS

### 📈 Use Case:

A SendSpeed oferece hoje OTP via SMS?]. O WhatsApp tem maior taxa de leitura e oferece a categoria de template *authentication* da Meta, dedicada a OTP. A integração permite que clientes disparem OTP via WhatsApp pela plataforma. Depende de mapeamento prévio da documentação do provedor Infobip.

### ✅ Critérios de aceite — Fase 1 (Mapeamento):

* Documentação do provedor de WhatsApp mapeada [decidir: Meta Cloud API / Infobip / outro BSP]
* Requisitos do template *authentication* documentados (aprovação Meta, formato, variáveis, validade do código)
* Restrições identificadas: rate limits, janela de sessão, política da categoria *authentication*
* Entregável: decisão go/no-go + estimativa de esforço da Fase 2

### ✅ Critérios de aceite — Fase 2 (Integração):

* Cliente solicita envio de OTP via WhatsApp por API existente / novo endpoint.
* Template de autenticação registrado e aprovado na Meta
* Status reportado ao cliente (enviado, entregue, lido) via callback.
* Fallback definido quando WhatsApp falha: cai para SMS e retorna erro.
* OTP respeita validade/expiração.

### 🧩 Cenários de teste:

* OTP entregue via WhatsApp dentro da validade → autenticação concluída
* Usuário sem WhatsApp → fallback acionado se optado pelo cliente e erro retornado
* Template não aprovado pela Meta → envio bloqueado com erro claro
* Código expirado → rejeição na validação

## Histórico de status
- To-do (unstarted): 2026-06-16T12:33:21.911Z → atual

## Relações
—

## Anexos
—
