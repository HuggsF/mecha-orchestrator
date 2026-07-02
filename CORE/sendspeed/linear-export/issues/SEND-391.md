# SEND-391 — [Tech] SendSmsExecutor integracao API real no journey backend

| Campo | Valor |
| -- | -- |
| Status | To-do (unstarted) |
| Prioridade | High |
| Responsável | thiago.melin@sendspeed.com |
| Time | Sendspeed |
| Projeto | — |
| Labels | Jornadas, Sendspeed, Tech Story |
| Parent | SEND-372 |
| Criada | 2026-03-13T15:54:10.634Z por Hugo Fernandes |
| Iniciada | — |
| Concluída | — |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-391-tech-sendsmsexecutor-integracao-api-real-no-journey-backend |
| URL | https://linear.app/sendspeed/issue/SEND-391/tech-sendsmsexecutor-integracao-api-real-no-journey-backend |

## Descrição

## Contexto

O SendSmsExecutor no journey backend precisa chamar a API real do sendspeed-sms-api: POST /api/sms/:companyId/send. Atualmente o journeyOffsiteProcessor apenas simula o envio (tem um TODO no codigo). Precisa funcionar em todos os contextos: fila Kafka, CampaignJourneyProcessor, offsite, external.

## Acceptance Criteria

- [ ] SendSmsExecutor chama POST /api/sms/:companyId/send (API real)
- [ ] journeyOffsiteProcessor.executeSendSms() usa executor real
- [ ] Funciona em todos os contextos: campaign, offsite, external
- [ ] Credencial SMS auto-resolvida by scope send_sms
- [ ] Resultado gravado em JourneyExecution.steps\[\]
- [ ] Publicacao no topico Kafka userin_send_sms com payload correto
- [ ] Usar modelo de user_profiles + contato

## Definition of Done

- [ ] Codigo revisado
- [ ] Testes unitarios passando
- [ ] Testes e2e com journey simulada
- [ ] CI/CD verde
- [ ] Documentacao atualizada

## RAG Context

**module:** journey / executor
**stack:** (stack do journey backend)
**key_files:** SendSmsExecutor, journeyOffsiteProcessor, CampaignJourneyProcessor
**repo:** (repo do journey backend)
**branch:** (criar branch feat a partir de develop)

## Agent Instructions

### Dev Agent

* Remover TODO de simulacao no journeyOffsiteProcessor
* Implementar chamada HTTP real ao sendspeed-sms-api
* Usar credencial resolvida por scope send_sms
* Payload Kafka: trace_id, user_name, user_phone, txt, message_id, companyId
* Conventional Commits: feat(journey): integrate real SMS API via executor

### Reviewer Agent

* Verificar que simulacao foi completamente removida
* Checar que credencial e resolvida corretamente
* Validar payload do Kafka esta completo

### Pm Agent

* Confirmar que todos os contextos estao cobertos

### Qa Agent

* Testar envio real em staging
* Validar que steps\[\] registra resultado
* Testar cenario sem credencial configurada

## Human Validation Checkpoints

- [ ] Code Review: PR aprovado
- [ ] Product Review: PM validou fluxo completo
- [ ] QA Sign-off: Testado em staging

## Branch/PR Convention

Branch: `SEND-{id}/feat/sms-executor-real-api`
PR Title: `feat(journey): integrate real SMS API via SendSmsExecutor [SEND-{id}]`

## Nota

Esta task e independente do sendspeed-sms-api. Pedro Iegler pode trabalhar nela paralelamente.
A API de SMS ja esta pronta: POST /api/sms/:companyId/send

---

## 🎯 Priorização RICE — Score: 12.8 (#4 no To-do)

| Reach | Impact | Confidence | Effort | Score |
| -- | -- | -- | -- | -- |
| 8 | 3 (massive) | 80% | 1.5 meses | **12.8** |

**Justificativa:** Enabler técnico crítico — sem ele, nenhuma jornada envia SMS de verdade (atualmente é um stub/simulação). Reach 8 porque afeta todas as empresas que configuram ações de SMS nas jornadas. Impacto massive (3) já que é pré-requisito para o produto funcionar end-to-end. Confidence 80%: a API de SMS já está pronta, mas a integração precisa cobrir múltiplos contextos (Kafka, campaign, offsite, external). Esforço de 1.5 meses pela complexidade de integração + testes em todos os caminhos.

## Histórico de status
- Backlog (backlog): 2026-03-13T15:54:10.634Z → 2026-03-16T14:03:53.702Z
- To-do (unstarted): 2026-03-16T14:03:53.702Z → atual

## Relações
- related: SEND-380 — 🚀 - Disparo de RCS automatizado via nó de ação no Journey Builder

## Anexos
—
