# SEND-415 — 🐞 - Desativar "Gerar Jornada com IA" do frontend (HTTP 401)

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | Urgent |
| Responsável | Hugo Fernandes |
| Time | Sendspeed |
| Projeto | — |
| Labels | QA-Validated, Jornadas, UserIn, User Story, Bug |
| Parent | — |
| Criada | 2026-03-20T13:16:40.959Z por Vinicius Carneiro |
| Iniciada | 2026-03-31T18:31:21.776Z |
| Concluída | 2026-06-22T17:15:40.815Z |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-415--desativar-gerar-jornada-com-ia-do-frontend-http-401 |
| URL | https://linear.app/sendspeed/issue/SEND-415/desativar-gerar-jornada-com-ia-do-frontend-http-401 |

## Descrição

## 📍 Onde ocorre

**Frontend** — Modal "Gerar Jornada com IA" no Journey Builder (`sendspeed-engage-ai-flow-08`).

---

## 🔁 Passo a Passo para Reproduzir

1. Acessar a plataforma Userin > Jornadas.
2. Clicar em "Gerar Jornada com IA".
3. Descrever uma jornada no campo de texto.
4. Clicar em "Gerar Jornada com IA".
5. Retorna **HTTP 401** — a funcionalidade não está operacional.

**Environment**: STG (`platform-stg-userin-ai.fly.dev`)
**API Endpoint**: `POST /ai/journeys/generate-full`
**Response**: HTTP 401 Unauthorized

---

## ❌ Resultado Atual

A feature de geração de jornada com IA está exposta na interface mas retorna **HTTP 401 (Unauthorized)**, indicando que o endpoint de IA não está configurado ou autenticado corretamente. Isso gera confusão para o usuário que tenta utilizar a funcionalidade.

---

## ✅ Resultado Esperado

Desativar/ocultar o botão e modal "Gerar Jornada com IA" do frontend até que a integração com o serviço de IA esteja funcional e autenticada.

---

## 🔍 Root Cause Analysis

O serviço `userin-platform-2-journey-ai` ([Fly.io](http://Fly.io)) está **morto** (health: 404). A cadeia de falha:

```
Frontend → Platform Backend → journey-ai-service (MORTO) → HTTP 401
```

O frontend faz `POST /ai/journeys/generate-full` ao Platform API, que tenta comunicar com o `journey-ai-service`. Como o serviço está down, a Platform API retorna 401 ao frontend.

---

## 🔧 Fix Aplicado

**Branch**: `fix/SEND-415-disable-journey-ai-button`
**PR**: [#32](https://github.com/sendspeed0/sendspeed-engage-ai-flow-08/pull/32)
**Commit**: `d9835cc`

**Mudanças** (2 arquivos, +9 -2 linhas):

* `client/src/config/env.ts` — Feature flag `VITE_FF_JOURNEY_AI` (default: `false`)
* `client/src/components/journey-builder/components/JourneyHeader.tsx` — Botão e dialog condicionados à flag

**Como Reativar**: Setar `VITE_FF_JOURNEY_AI=true` no `.env` quando o `journey-ai-service` for restaurado.

---

## 🧪 QA Validation — PASSED

**Metodo**: Browser automation (Computer-Use via Cursor MCP)
**Ambiente validado**: STG (`platform-stg-userin-ai.fly.dev`)
**Evidencias**: [GitHub Issue #33 com screenshots](https://github.com/sendspeed0/sendspeed-engage-ai-flow-08/issues/33)

**Screenshots:**

* [Botao "Gerar com IA" visivel (BUG)](https://github.com/sendspeed0/sendspeed-engage-ai-flow-08/releases/download/qa-evidence-send-415/SEND-415-03-botao-gerar-ia-visivel.png)
* [Modal aberto (BUG)](https://github.com/sendspeed0/sendspeed-engage-ai-flow-08/releases/download/qa-evidence-send-415/SEND-415-04-modal-gerar-jornada-ia.png)
* [Journey AI Service morto (causa raiz)](https://github.com/sendspeed0/sendspeed-engage-ai-flow-08/releases/download/qa-evidence-send-415/SEND-415-05-journey-ai-service-morto.png)

**Aprovacao**: Vinicius Carneiro validou em 2026-03-31 ("Validado, por favor prosseguir!")

---

## 🎯 Priorização RICE — Score: 20.0

| Reach | Impact | Confidence | Effort | Score |
| -- | -- | -- | -- | -- |
| 10 | 0.5 (low) | 100% | 0.25 meses | **20.0** |

---

## ⚠️ Blocker Relacionado

SEND-438: MongoDB DEV (`govtech` user) tem permissão somente leitura, impedindo validação no ambiente DEV. Validação feita em STG como workaround.

## Histórico de status
- Backlog (backlog): 2026-03-20T13:16:40.959Z → 2026-03-20T13:19:22.174Z
- Refining (backlog): 2026-03-20T13:19:22.174Z → 2026-03-31T12:33:15.060Z
- To-do (unstarted): 2026-03-31T12:33:15.060Z → 2026-03-31T18:31:21.786Z
- In Progress (started): 2026-03-31T18:31:21.786Z → 2026-03-31T21:25:02.047Z
- Done (started): 2026-03-31T21:25:02.047Z → 2026-04-01T12:16:21.841Z
- Pull Request (started): 2026-04-01T12:16:21.841Z → 2026-06-22T17:15:40.827Z
- Released (completed): 2026-06-22T17:15:40.827Z → atual

## Relações
—

## Anexos
- fix(journey-builder): disable 'Gerar Jornada com IA' button via feature flag (SEND-415) — https://github.com/sendspeed0/sendspeed-engage-ai-flow-08/pull/32
