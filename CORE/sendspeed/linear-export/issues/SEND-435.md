# SEND-435 — 🐞 - Nó "Aguardar" não funciona em Jornadas Externas (Offsite)

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | Urgent |
| Responsável | — |
| Time | Sendspeed |
| Projeto | — |
| Labels | RCA-Documented |
| Parent | — |
| Criada | 2026-03-31T14:44:27.268Z por Vinicius Carneiro |
| Iniciada | — |
| Concluída | 2026-06-22T17:16:18.093Z |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-435--no-aguardar-nao-funciona-em-jornadas-externas-offsite |
| URL | https://linear.app/sendspeed/issue/SEND-435/no-aguardar-nao-funciona-em-jornadas-externas-offsite |

## Descrição

## 📍 Onde ocorre

**Journey Offsite Processor** — Nó de tipo `flow.delay` em jornadas acionadas por gatilhos externos (webhook, CRM, etc.).

Afeta **apenas jornadas externas (offsite)**. Jornadas InSite funcionam corretamente.

---

## 🔁 Passo a Passo

1. Criar uma jornada com gatilho **Webhook** (externo)
2. Adicionar nó **Enviar SMS**
3. Adicionar nó **Aguardar** (ex: 1 minuto)
4. Adicionar outro nó **Enviar SMS**
5. Adicionar nó **Aguardar** (ex: 30 minutos)
6. Adicionar mais um nó **Enviar SMS**
7. Disparar o webhook com usuários de teste
8. Observar os horários de entrega dos SMS

**Fluxo testado:**

Webhook (3 usuários) → Enviar SMS → Aguardar 1 min → Enviar SMS → Aguardar 30 min → Enviar SMS → Finalizar

---

## ❌ Resultado Atual

O nó de **Aguardar** (`flow.delay`) não pausa a execução corretamente em jornadas offsite. O delay configurado é ignorado ou não respeitado, fazendo com que os nós subsequentes executem fora do timing esperado.

**Evidências:**

* Jornada configurada com Webhook → SMS → Aguardar 1 min → SMS → Aguardar 30 min → SMS
* 3 usuários entraram no webhook, mas apenas 2 continuaram após o primeiro nó de Aguardar (1 usuário perdido no delay)
* O processador offsite (`journeyOffsiteProcessor`) pode não estar tratando o nó delay da mesma forma que o engine InSite

---

## ✅ Resultado Esperado

* O nó **Aguardar** deve pausar a execução pelo tempo configurado, tanto em jornadas InSite quanto Offsite
* Todos os usuários que entraram no delay devem continuar a jornada após o tempo configurado (sem perda de usuários)
* Aguardar 1 minuto → próximo nó executa exatamente \~1 minuto depois
* Aguardar 30 minutos → próximo nó executa exatamente \~30 minutos depois

---

## 📎 Arquivos potencialmente afetados

* `backend-plataforma/backend/src/journey-builder/services/journeyOffsiteProcessor.js` — processamento de nós offsite
* `backend-plataforma/backend/src/journey-builder/engine/nodes/flow/DelayExecutor.js` — executor do nó delay
* Mecanismo de agendamento/retry para nós com timer em jornadas externas

---

## 🎯 Priorização RICE — Score: 19.2 (#5 no To-do)

| Reach | Impact | Confidence | Effort | Score |
| -- | -- | -- | -- | -- |
| 8 | 3 (massive) | 80% | 1 mês | **19.2** |

**Justificativa:** Reach 8: todas as empresas usando jornadas offsite com delays (caso de uso principal: webhooks de CRM/Smartico). Impacto massive (3): sem o delay funcionando, toda a lógica temporal da jornada quebra — SMS, RCS e ações disparam fora de sequência ou todos de uma vez. Confidence 80%: evidência clara via teste com webhook, mas causa raiz precisa de investigação no offsite processor. Esforço 1 mês: investigar e implementar mecanismo de agendamento para delays offsite (possivelmente fila/cron).

## Histórico de status
- Backlog (backlog): 2026-03-31T14:44:27.268Z → 2026-03-31T14:45:45.371Z
- To-do (unstarted): 2026-03-31T14:45:45.371Z → 2026-03-31T23:44:31.249Z
- Product Review (started): 2026-03-31T23:44:31.249Z → 2026-04-24T13:42:28.873Z
- To-do (unstarted): 2026-04-24T13:42:28.873Z → 2026-06-22T17:16:18.106Z
- Released (completed): 2026-06-22T17:16:18.106Z → atual

## Relações
—

## Anexos
- fix(journey-builder): SEND-435 - Implementar delay real em jornadas offsite — https://github.com/sendspeed0/platform-backend/pull/25
- fix(journey-builder): SEND-435 - Implementar delay real em jornadas offsite — https://github.com/sendspeed0/platform-backend/pull/24
