# SEND-84 — [COMPANION][VETOR] — Vetor usa Conversões "Personalizadas" - (continuação do card "[PLATAFORMA] Conversões 'Personalizadas' funcionando 100%")

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | No priority |
| Responsável | — |
| Time | Sendspeed |
| Projeto | — |
| Labels | — |
| Parent | — |
| Criada | 2025-09-05T13:35:23.102Z por bruno.heidrich@sendspeed.com |
| Iniciada | 2025-09-08T14:03:48.516Z |
| Concluída | 2025-09-24T16:20:46.816Z |
| Arquivada | 2026-06-01T22:41:34.155Z |
| Vencimento | — |
| Branch | hugofernandes/send-84-companionvetor-vetor-usa-conversoes-personalizadas |
| URL | https://linear.app/sendspeed/issue/SEND-84/companionvetor-vetor-usa-conversoes-personalizadas-continuacao-do-card |

## Descrição

**Como** Head de Marketing,
**quero** que o Companion **use os eventos das conversões personalizadas** (ex.: "Dúvida") na hora de decidir qual card mostrar,
**para** que cada usuário receba a intervenção certa no momento certo e o vetor aprenda com esses casos.

**Pronto quando**

* Ao ocorrer uma conversão personalizada, o evento **fica disponível para o vetor** do cliente e aparece nos **logs/lista** do módulo.
* As decisões do Companion passam a registrar **card escolhido + conversão que pesou + versão do vetor**, com **motivo curto** (ex.: "tipo=dúvida (FAQ) → Card #24").
* Com o **uso ligado** (por cliente), o sistema **prioriza cards compatíveis** com o tipo da conversão; com o **uso desligado**, volta à **regra padrão**.
* Consigo **ativar/desativar** o uso de conversões personalizadas **por cliente**.
* Teste simples validado: criar a conversão "Dúvida", acionar no site e ver o **card de dúvida** ser escolhido e **registrado com motivo**.

---

## Feito ✅ 

* **Companion decide por conversão personalizada disparada no Tracker e prioriza cards compatíveis por tipo (exit_risk/doubt_risk/conversion_risk).**
* **Logs de decisão gravados em companion_decisions e evento events.type=companion_decision com card, conversionType/conversionCode e motivo curto.**
* **Endpoint de decisão ativo: POST /api/companion/decide-from-conversion.**
* **Endpoints para ativar/desativar por cliente prontos: GET/PUT /api/companion/settings/:companyId.**
* **Integração Tracker → Analytics ativa (detecção de conversão e chamada ao Companion); Analytics → Buyer lê buyer_cards reais.**

## Falta fazer

- [ ] **Ler companion_settings (Mongo) no CompanionDecisionService em vez de mockClientSettings.**
- [ ] **Registrar a versão ativa do vetor em versionId (ex.: ler de vector_behavior.activeVersionId) e opcionalmente incluir no reason.**
- [ ] **Garantir que eventos de conversão personalizados usados para vetorização estejam disponíveis no mesmo datastore do Analytics (ou criar forward/ingest se bancos forem distintos).**
- [ ] **Validar fim a fim o teste "Dúvida" no site real usando as settings do Mongo (não só via script).**

## Histórico de status
- To-do (unstarted): 2025-09-05T13:35:23.102Z → 2025-09-08T14:03:48.532Z
- In Progress (started): 2025-09-08T14:03:48.532Z → 2025-09-23T18:04:06.517Z
- Pull Request (started): 2025-09-23T18:04:06.517Z → 2025-09-24T16:20:46.836Z
- Released (completed): 2025-09-24T16:20:46.836Z → atual

## Relações
—

## Anexos
—
