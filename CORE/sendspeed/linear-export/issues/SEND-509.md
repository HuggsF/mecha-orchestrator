# SEND-509 — 1. Fazendinha Automatizada de Qualidade de Rota

| Campo | Valor |
| -- | -- |
| Status | To-do (unstarted) |
| Prioridade | No priority |
| Responsável | — |
| Time | Sendspeed |
| Projeto | — |
| Labels | — |
| Parent | — |
| Criada | 2026-06-16T12:42:32.568Z por Vinicius Carneiro |
| Iniciada | — |
| Concluída | — |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-509-1-fazendinha-automatizada-de-qualidade-de-rota |
| URL | https://linear.app/sendspeed/issue/SEND-509/1-fazendinha-automatizada-de-qualidade-de-rota |

## Descrição

> **Como** analista de operações da SendSpeed 
> **Quero** que a fazendinha de chips execute envios de sonda de forma automatizada nas rotas ativas de RCS e SMS 
> **Para** detectar degradação de qualidade de rota antes que ela afete os envios reais dos clientes

### 📈 Use Case:

A SendSpeed roteia mensagens RCS e SMS por múltiplas rotas/fornecedores cuja qualidade oscila no tempo (bloqueio de carrier, marcação como spam, queda de entregabilidade). Hoje como a degradação é detectada via reclamação de cliente. Integrando o sistema de fazendinha do Bruno Heidreich, a SendSpeed passa a disparar mensagens-sonda para números controlados internamente, medindo a entregabilidade real de cada rota de forma proativa, gerando sinal acionável de roteamento antes do cliente perceber.

### ✅ Critérios de aceite:

* A integração consome o sistema de fazendinha do Bruno.
* O disparo de sondas é automatizado segundo gatilho de agendamento a cada X min / pré-campanha / ambos]
* Para cada rota testada, registra no mínimo: taxa de entrega confirmada, latência de entrega e confirmação de recebimento real no chip.
* O resultado dispara uma ação de alerta e despriorização automática no roteamento.
* Cobre RCS e SMS com thresholds separados por canal
* Volume e frequência de sondas respeitam limite de custo/reputação havendo um ambiente de configuração de para definir quais são os limites de envio diario.

### 🧩 Cenários de teste:

* Rota saudável: sondas entregues acima do threshold → rota segue ativa, sem alerta
* Rota degradada: taxa cai abaixo do threshold na janela → ação configurada é disparada
* Sistema do Bruno indisponível → não pode marcar falsa degradação nem bloquear roteamento por falha própria.
* Sonda RCS para número sem suporte RCS → não conta como rota degradada.

## Histórico de status
- To-do (unstarted): 2026-06-16T12:42:32.568Z → 2026-06-22T17:16:54.941Z
- Released (completed): 2026-06-22T17:16:54.941Z → 2026-06-22T17:16:57.544Z
- To-do (unstarted): 2026-06-22T17:16:57.544Z → atual

## Relações
—

## Anexos
—
