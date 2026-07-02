# SEND-487 — 5. Alerta adicional de saldo na SS Control

| Campo | Valor |
| -- | -- |
| Status | To-do (unstarted) |
| Prioridade | Urgent |
| Responsável | Vinicius Carneiro |
| Time | Sendspeed |
| Projeto | — |
| Labels | Melhoria, User Story |
| Parent | — |
| Criada | 2026-06-02T18:09:36.049Z por Vinicius Carneiro |
| Iniciada | — |
| Concluída | — |
| Arquivada | 2026-06-16T17:45:26.175Z |
| Vencimento | — |
| Branch | hugofernandes/send-487-5-alerta-adicional-de-saldo-na-ss-control |
| URL | https://linear.app/sendspeed/issue/SEND-487/5-alerta-adicional-de-saldo-na-ss-control |

## Descrição

> **Como** time de operações/financeiro responsável pelas recargas
> **Quero** ser avisado mais cedo quando o saldo de um cliente se aproxima do limite crítico
> **Para** reduzir o tempo entre o saldo ficar baixo e a recarga ser feita, evitando interrupção de disparos

### 📈 Use Case:

Hoje os times reagem tarde a saldo baixo, causando interrupções. Adiciona-se um novo alerta na SS Control, disparado em um limiar mais alto que o atual, dando ao time uma janela maior para agir antes do esgotamento.

### ✅ Critérios de aceite:

* Um novo alerta é disparado quando o saldo cruza um limiar \[decidir: qual valor/percentual, e por que esse?\], anterior ao alerta crítico já existente
* O alerta é distinguível visualmente/categoricamente do alerta crítico atual (para não virar ruído)
* \[decidir\] O alerta tem ação/destinatário definido — quem recebe e o que deve fazer? Um alerta sem dono não muda comportamento
* Métrica de sucesso: tempo médio entre cruzar o limiar de saldo baixo e a recarga acontecer diminui (definir baseline atual)

### 🧩 Cenários de teste:

- [ ] Reduzir saldo de um cliente até o novo limiar e verificar disparo do novo alerta
- [ ] Verificar que o novo alerta é visualmente diferente do alerta crítico existente
- [ ] Verificar que o alerta crítico atual continua funcionando normalmente
- [ ] Confirmar que o alerta chega ao destinatário/canal correto
- [ ] Medir o tempo até recarga em um ciclo e comparar com o baseline

## Histórico de status
- To-do (unstarted): 2026-06-02T18:09:36.049Z → atual

## Relações
—

## Anexos
—
