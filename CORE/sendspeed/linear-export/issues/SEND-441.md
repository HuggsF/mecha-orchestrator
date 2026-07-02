# SEND-441 — [QA] SEND-435: Validar fix do no Aguardar em jornadas offsite

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | High |
| Responsável | — |
| Time | Sendspeed |
| Projeto | — |
| Labels | QA-Validated, Jornadas |
| Parent | SEND-435 |
| Criada | 2026-03-31T23:26:00.058Z por Hugo Fernandes |
| Iniciada | 2026-03-31T23:41:48.522Z |
| Concluída | 2026-04-15T22:15:03.200Z |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-441-qa-send-435-validar-fix-do-no-aguardar-em-jornadas-offsite |
| URL | https://linear.app/sendspeed/issue/SEND-441/qa-send-435-validar-fix-do-no-aguardar-em-jornadas-offsite |

## Descrição

## Objetivo

Validar que o fix resolve o bug SEND-435 usando o pipeline QA automatizado.

## Test Plan

1. Criar jornada offsite com webhook trigger no staging
2. Fluxo: Webhook -> SMS -> Aguardar 1min -> SMS -> Aguardar 5min -> SMS
3. Disparar webhook com 3 usuarios de teste
4. Verificar timing dos SMS (deve respeitar delays)
5. Capturar screenshots como evidencia

## Acceptance Criteria

- [ ] Playbook `SEND-435.browser.md` criado
- [ ] Todos os 3 usuarios completam a jornada
- [ ] Delays respeitados (+-10% tolerancia)
- [ ] Screenshots capturados e anexados
- [ ] Resultado postado como comentario

## Histórico de status
- Refining (backlog): 2026-03-31T23:26:00.058Z → 2026-03-31T23:41:48.546Z
- In Progress (started): 2026-03-31T23:41:48.546Z → 2026-04-01T00:50:41.825Z
- Done (started): 2026-04-01T00:50:41.825Z → 2026-04-15T22:15:03.218Z
- Released (completed): 2026-04-15T22:15:03.218Z → atual

## Relações
—

## Anexos
—
