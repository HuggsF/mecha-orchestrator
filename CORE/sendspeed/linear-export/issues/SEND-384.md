# SEND-384 — 🚀 - Métricas de atribuição Last Touch de SMS/RCS no Journey Analytics

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | Medium |
| Responsável | — |
| Time | Sendspeed |
| Projeto | — |
| Labels | User Story, Analytics, UserIn, Melhoria |
| Parent | — |
| Criada | 2026-03-13T13:19:56.639Z por Vinicius Carneiro |
| Iniciada | — |
| Concluída | 2026-06-22T17:16:42.598Z |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-384--metricas-de-atribuicao-last-touch-de-smsrcs-no-journey |
| URL | https://linear.app/sendspeed/issue/SEND-384/metricas-de-atribuicao-last-touch-de-smsrcs-no-journey-analytics |

## Descrição

> **Como** gestor de performance de uma operadora de iGaming
> **Quero** visualizar as métricas de atribuição Last Touch das jornadas de SMS e RCS dentro do analytics de jornadas já existente na plataforma
> **Para** saber quais jornadas e canais estão convertendo mais, com qual confidence score, e otimizar o investimento em engajamento com dados reais

---

# 📈 Use Case: Acompanhamento de conversões SMS/RCS no Journey Analytics existente

O gestor de performance da ApostaTudo acessa o Journey Analytics existente (rota `/journey-analytics/:id`) para acompanhar a jornada "Boas-vindas FTD" que envia SMS:

1. **Summary cards (já existentes)**: Vê total de execuções, completadas, taxa de conversão, visitantes únicos — agora incluindo execuções que dispararam SMS/RCS.
2. **Conversions (já existente via ClickHouse)**: A seção de conversões mostra registers, FTDs, depositantes e valor total. Com Last Touch, o gestor agora sabe que dos 312 FTDs, **280 foram atribuídos ao SMS da jornada** (último touchpoint antes do depósito), com confidence score médio de 0.72.
3. **Funnel (já existente)**: O funil por nó mostra que o nó `action.sendSms` recebeu 2.400 entradas, 2.350 enviaram com sucesso (98%), 50 falharam (sem telefone). O passRate de cada etapa permite identificar gargalos.
4. **KPI Values (já existente)**: Os KPIs configurados na jornada (ex: taxa FTD, custo por conversão) são recalculados automaticamente pelo AttributionService quando conversões são atribuídas via Last Touch. O dashboard mostra status on_target/warning/critical.
5. **Novo: Métricas de canal SMS/RCS no funnel**: No detalhe do nó sendSms/sendRcs no funil, o gestor vê: total enviados, entregues, falhas por exit reason (NO_PHONE, NO_INTEGRATION, SEND_FAILED), e touchpoints ativos vs convertidos.

**Infraestrutura existente utilizada:**

* Frontend: `useJourneyAnalytics` hook, `JourneyListPage`, rota `/journey-analytics/:id`
* Backend: `GET /api/journeys/:id/analytics` (ClickHouse), `/analytics/funnel`, `/analytics/triggers`, `/analytics/exit-points`, `/analytics/users`
* Atribuição: `AttributionService.processConversion()`, model `Touchpoint`, `metricCounters` e `kpiValues` no model Journey

---

# ✅ Critérios de aceite:

* Analytics de jornada exibe métricas de execuções que incluem nós sendSms e sendRcs
* Seção de conversões (ClickHouse) mostra FTDs, registers e depósitos atribuídos via Last Touch
* Funnel por nó mostra métricas específicas dos nós sendSms/sendRcs: enviados, falhas e exit reasons
* KPI Values recalculados automaticamente quando conversões são atribuídas ao touchpoint da jornada
* Tabela de users (`/analytics/users`) mostra se o usuário recebeu SMS/RCS e se converteu
* Timeline (já existente) reflete execuções com envio de SMS/RCS por dia
* Dados de atribuição (model, confidence, weight) visíveis no detalhe da execução
* Triggers breakdown mostra quantas execuções por trigger resultaram em envio de SMS/RCS
* Exit points mostra os exit reasons do SendSmsExecutor/SendRcsExecutor (NO_PHONE, NO_INTEGRATION, etc.)

---

# 🧩 Cenários de teste:

- [ ] Acessar /journey-analytics/:id de uma jornada com nó sendSms — summary cards mostram execuções corretas
- [ ] Verificar que a seção de conversões mostra FTDs atribuídos via Last Touch à jornada
- [ ] Verificar que o funil mostra o nó sendSms com passRate (enviados vs falhas)
- [ ] Verificar que exit points listam exit reasons do SMS (NO_PHONE, SEND_FAILED, INTEGRATION_OFFLINE)
- [ ] Verificar que KPI Values atualizam quando AttributionService processa uma conversão
- [ ] Verificar que a tabela de users mostra status do SMS (enviado/falhou) por usuário
- [ ] Repetir cenários acima para jornada com nó sendRcs
- [ ] Verificar timeline com execuções de SMS/RCS por dia no gráfico existente
- [ ] Jornada sem execuções de SMS/RCS — funnel mostra nó com zero entradas (não quebra UI)
- [ ] Filtrar por período e source (offsite) e verificar que dados filtram corretamente

---

## 🎯 Priorização RICE — Score: 3.0

| Reach | Impact | Confidence | Effort | Score |
| -- | -- | -- | -- | -- |
| 6 | 2 (high) | 50% | 2 meses | **3.0** |

**Justificativa:** Reach 6: gestores de performance usando jornadas SMS/RCS. Impacto high (2): sem métricas de atribuição, ROI das jornadas é invisível. Confidence 50%: depende de SEND-378/380. Esforço 2 meses: integração ClickHouse + funnel + touchpoints + UI.

## Histórico de status
- Backlog (backlog): 2026-03-13T13:19:56.639Z → 2026-03-13T14:59:56.918Z
- To-do (unstarted): 2026-03-13T14:59:56.918Z → 2026-06-22T17:16:42.608Z
- Released (completed): 2026-06-22T17:16:42.608Z → atual

## Relações
—

## Anexos
—
