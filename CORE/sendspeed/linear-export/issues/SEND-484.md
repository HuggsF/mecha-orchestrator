# SEND-484 — 4. Observabilidade de callback e padronização para o modelo SevenX como default

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | No priority |
| Responsável | — |
| Time | Sendspeed |
| Projeto | — |
| Labels | — |
| Parent | — |
| Criada | 2026-06-02T17:54:51.427Z por Vinicius Carneiro |
| Iniciada | — |
| Concluída | 2026-06-22T17:18:38.420Z |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-484-4-observabilidade-de-callback-e-padronizacao-para-o-modelo |
| URL | https://linear.app/sendspeed/issue/SEND-484/4-observabilidade-de-callback-e-padronizacao-para-o-modelo-sevenx-como |

## Descrição

> **Como** time de operações/suporte da plataforma
> **Quero** detectar e diagnosticar falhas no envio de callbacks proativamente, com o modelo SevenX como formato padrão de callback
> **Para** resolver problemas de callback antes que o cliente perceba, em vez de depender de ele nos avisar

# 📈 Use Case:

O modelo SevenX passa a ser o formato default de callback. Em paralelo, a plataforma monitora o envio de callbacks e dispara alerta interno quando uma falha ocorre (ex: callback não entregue, erro de formato), permitindo que o time aja antes do cliente reportar.

## ✅ Critérios de aceite:

* O modelo SevenX é aplicado como formato default para callbacks.
* Toda falha no envio/processamento de callback é registrada com contexto suficiente para diagnóstico (cliente, fornecedor, payload, motivo)

sms_2026-05-11_part0001

* Um alerta interno é disparado quando a taxa de falha de callback cruza um limiar \[decidir: qual limiar e qual canal de alerta?\]j
* O time consegue identificar a causa de uma falha de callback sem solicitar informação ao cliente
* Métrica de sucesso: % de problemas de callback detectados internamente antes de o cliente abrir chamado (definir baseline)

## 🧩 Cenários de teste:

- [ ] Configurar cliente novo e verificar que o callback sai no formato SevenX por default
- [ ]  Forçar falha de entrega de callback e verificar log com contexto completo
- [ ]  Elevar a taxa de falha acima do limiar e verificar disparo do alerta interno
- [ ]  Reproduzir um caso real de falha apenas com os dados do log, sem consultar o cliente

## Histórico de status
- To-do (unstarted): 2026-06-02T17:54:51.427Z → 2026-06-03T19:19:25.262Z
- Backlog (backlog): 2026-06-03T19:19:25.262Z → 2026-06-22T17:18:38.426Z
- Released (completed): 2026-06-22T17:18:38.426Z → atual

## Relações
—

## Anexos
—
