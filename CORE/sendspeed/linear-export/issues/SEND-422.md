# SEND-422 — 🚀 - Analytics de envio, falha e status do RCS na Jornada

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | Urgent |
| Responsável | Vinicius Carneiro |
| Time | Sendspeed |
| Projeto | — |
| Labels | Implementação, Jornadas, User Story |
| Parent | — |
| Criada | 2026-03-20T14:47:27.547Z por Vinicius Carneiro |
| Iniciada | 2026-03-25T18:33:00.598Z |
| Concluída | 2026-04-14T15:16:13.500Z |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-422--analytics-de-envio-falha-e-status-do-rcs-na-jornada |
| URL | https://linear.app/sendspeed/issue/SEND-422/analytics-de-envio-falha-e-status-do-rcs-na-jornada |

## Descrição

> **Como** gestor de operações da Sendspeed
> **Quero** visualizar no analytics da jornada os dados de envio, entrega, falha e status de cada RCS disparado
> **Para** monitorar a performance do canal RCS em tempo real, identificar problemas de entrega rapidamente e comparar eficiência entre canais (SMS vs RCS) dentro da mesma jornada.

---

# 📈 Use Case: Dashboard de performance RCS da jornada Black Friday

Durante a Black Friday, a operadora dispara uma jornada com 50.000 jogadores. O gestor precisa acompanhar em tempo real: quantos RCS foram enviados, quantos foram entregues, quantos falharam e por qual motivo (número inválido, provedor indisponível, cota excedida). Ele abre o analytics da jornada e vê o breakdown por canal, identifica que 8% das falhas são por número inválido e aciona a equipe de dados para limpeza da base.

# ✅ Critérios de aceite:

* O `SendRcsExecutor` deve registrar status detalhado no `JourneyExecution.steps[]` (sent, failed, reason).
* Deve existir um mecanismo de callback/webhook da Integrations API para receber delivery reports (delivered, failed, expired).
* O analytics da jornada deve exibir métricas de delivery por canal: total enviados, entregues, falhados.
* O analytics deve exibir taxa de entrega por canal (delivery rate).
* O funnel da jornada deve refletir o status real de entrega no nó de RCS (não apenas "step completed").
* Falhas devem ser categorizadas por motivo (número inválido, provedor offline, cota excedida, etc.).

# 🧩 Cenários de teste:

- [ ] Enviar RCS via jornada → step registrado como `sent` no JourneyExecution.
- [ ] Receber callback de delivery → status atualizado para `delivered`.
- [ ] Receber callback de falha → status atualizado para `failed` com motivo.
- [ ] Abrir analytics da jornada → seção "Delivery por Canal" exibe RCS com totais corretos.
- [ ] Comparar taxa de entrega SMS vs RCS na mesma jornada.
- [ ] Verificar que falhas por motivo são listadas (ex: 15% número inválido, 3% provedor offline).
- [ ] Analytics atualiza em near-real-time (delay máximo aceitável do pipeline CDC).

## Histórico de status
- Backlog (backlog): 2026-03-20T14:47:27.547Z → 2026-03-20T15:22:05.865Z
- To-do (unstarted): 2026-03-20T15:22:05.865Z → 2026-03-25T18:33:00.606Z
- In Progress (started): 2026-03-25T18:33:00.606Z → 2026-03-26T12:44:23.530Z
- Pull Request (started): 2026-03-26T12:44:23.530Z → 2026-03-26T14:34:55.321Z
- Product Review (started): 2026-03-26T14:34:55.321Z → 2026-04-14T15:16:13.511Z
- Released (completed): 2026-04-14T15:16:13.511Z → atual

## Relações
—

## Anexos
—
