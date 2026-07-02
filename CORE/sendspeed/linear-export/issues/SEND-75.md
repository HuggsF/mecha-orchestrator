# SEND-75 — [COMPANION][VETOR] — Ensino vetorial v1.4: Usar o vetor nas decisões

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | No priority |
| Responsável | — |
| Time | Sendspeed |
| Projeto | — |
| Labels | — |
| Parent | — |
| Criada | 2025-08-29T14:25:04.118Z por bruno.heidrich@sendspeed.com |
| Iniciada | 2025-09-04T19:47:12.224Z |
| Concluída | 2025-09-24T16:20:29.087Z |
| Arquivada | 2026-03-26T01:33:07.357Z |
| Vencimento | — |
| Branch | hugofernandes/send-75-companionvetor-ensino-vetorial-v14-usar-o-vetor-nas-decisoes |
| URL | https://linear.app/sendspeed/issue/SEND-75/companionvetor-ensino-vetorial-v14-usar-o-vetor-nas-decisoes |

## Descrição

**Como** Head de Produto, 
**quero** que o Companion **use o vetor ativo em cliente de produção** na escolha do card 
**para** compararmos com a performance do companion de IA e do companion de Gatilho.

**Pronto quando**

* Existe **um vetor ativo** por cliente (posso trocar).
* Decisões passam a registrar: **versão usada** e **motivo curto**.
* Se não houver vetor ativo, aplica **regra padrão** (fallback).
* Criar um Event para saber quem disparou: Gatilho Automático, IA ou Vetor
* Criar uma forma de ativar/desativar o vetor (behavior)

---

## Feito ✅ 

* Existe endpoint para comportamento/vetor por cliente: POST /api/vectors/behavior/save com enabled, activeVersionId e fallback.


* Existe endpoint para logar decisões com fonte e versão: POST /api/vectors/decision/log (source: 'trigger'|'ai'|'vector', versionId, reasonShort).


* Decisões do Companion já registram motivo curto e criam evento events.type=companion_decision (auditoria).


* Fallback geral da decisão já existe (regra padrão quando condição não atende).

## Falta fazer ❌ 

* Usar de fato o vetor ativo na escolha do card: ler vector_behavior.activeVersionId e consultar o vetor para ranquear/selecionar card.


* Popular versionId nas decisões com a versão ativa do vetor (hoje estático) e opcionalmente incluir no reason.


* Uniformizar source nas decisões/eventos: hoje o serviço usa conversion-triggered; alinhar para trigger, ai ou vector (e gravar no evento).


* Evento "quem disparou": incluir source no events.type=companion_decision.metadata para diferenciar Gatilho Automático, IA ou Vetor.


* Respeitar behavior.enabled: se desabilitado ou sem vetor ativo, aplicar fallback padrão; quando habilitado e com vetor ativo, priorizar decisão via vetor.


* Substituir mocks de settings por leitura real (companion_settings) quando necessário para coerência com produção.

## Histórico de status
- To-do (unstarted): 2025-08-29T14:25:04.118Z → 2025-09-04T19:47:12.212Z
- In Progress (started): 2025-09-04T19:47:12.212Z → 2025-09-23T18:04:04.124Z
- Pull Request (started): 2025-09-23T18:04:04.124Z → 2025-09-24T11:50:15.769Z
- Product Review (started): 2025-09-24T11:50:15.769Z → 2025-09-24T16:20:29.070Z
- Released (completed): 2025-09-24T16:20:29.070Z → atual

## Relações
—

## Anexos
—
