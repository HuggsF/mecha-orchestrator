# SEND-412 — 🐞 - AJUSTAR E REFINAR LISTA DE OBJETIVOS COM OS OBJETIVOS DA EMPRES (BET)

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | No priority |
| Responsável | — |
| Time | Sendspeed |
| Projeto | — |
| Labels | Bug, Jornadas, UserIn |
| Parent | — |
| Criada | 2026-03-19T19:13:32.854Z por Vinicius Carneiro |
| Iniciada | — |
| Concluída | 2026-06-22T17:18:50.074Z |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-412--ajustar-e-refinar-lista-de-objetivos-com-os-objetivos-da |
| URL | https://linear.app/sendspeed/issue/SEND-412/ajustar-e-refinar-lista-de-objetivos-com-os-objetivos-da-empres-bet |

## Descrição

## 📍 Onde ocorre

**Backend:** `journeyService.js` (create, update, duplicate) e `objectiveService.js` (update).
**Frontend:** `useJourneyBuilder.ts` (loadJourney, save) e `ObjectivesPage.tsx` (handleSaveMetrics).
**Schema:** `Journey.js` (campo `successMetrics`) e `Objective.js` (campo `successMetricIds`).

---

## 🔁 Passo a Passo

1. Acessar a plataforma Userin > Jornadas.
2. Criar ou editar uma jornada e associar um Objetivo com métricas de sucesso.
3. Salvar a jornada.
4. Editar novamente a mesma jornada e salvar (ou duplicar a jornada).
5. Verificar no banco de dados (ou na UI de objetivos) que as métricas de sucesso possuem **entradas duplicadas**.

---

## ❌ Resultado Atual

**Problema 1 — Sem deduplicação no backend:**
Os métodos `create`, `update` e `duplicate` do `journeyService.js` passam o array `successMetrics` direto sem validar unicidade por `metricId`:

**Problema 2 —** `objectiveService.update` também não deduplica:

**Problema 3 — Schema sem constraint de unicidade:**
Nem `Journey.successMetrics[].metricId` nem `Objective.successMetricIds` possuem validação de unicidade no schema Mongoose.

**Problema 4 — Duplicação de jornada copia duplicatas:**
`journeyService.duplicate` copia todos os campos do original incluindo `successMetrics`, perpetuando duplicatas existentes.

---

## ✅ Resultado Esperado

* Ao salvar uma jornada, o array `successMetrics` deve conter apenas **uma entrada por** `metricId`.
* Ao atualizar um objetivo, o array `successMetricIds` deve conter apenas **valores únicos**.
* Ao duplicar uma jornada, as `successMetrics` devem ser deduplicadas.
* A UI não deve exibir métricas duplicadas na seção de objetivos da jornada.

## Histórico de status
- Backlog (backlog): 2026-03-19T19:13:32.854Z → 2026-03-19T19:44:52.127Z
- Refining (backlog): 2026-03-19T19:44:52.127Z → 2026-03-20T13:24:13.856Z
- Backlog (backlog): 2026-03-20T13:24:13.856Z → 2026-06-22T17:18:50.079Z
- Released (completed): 2026-06-22T17:18:50.079Z → atual

## Relações
—

## Anexos
—
