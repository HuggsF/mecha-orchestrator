# SEND-411 — 🐞 - Regra de "não click" não funciona corretamente

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | Urgent |
| Responsável | Hugo Fernandes |
| Time | Sendspeed |
| Projeto | — |
| Labels | Bug, Regras, UserIn, User Story |
| Parent | — |
| Criada | 2026-03-19T19:12:57.934Z por Vinicius Carneiro |
| Iniciada | 2026-04-02T11:45:08.954Z |
| Concluída | 2026-06-22T17:15:41.768Z |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-411--regra-de-nao-click-nao-funciona-corretamente |
| URL | https://linear.app/sendspeed/issue/SEND-411/regra-de-nao-click-nao-funciona-corretamente |

## Descrição

## 📍 Onde ocorre

**Engine client-side** — Arquivo `engineRoutes.js` (função `evaluateCondition`, linhas \~4025–4067) e **RuleMatchExecutor.js** (linhas \~103–158).

Afeta qualquer regra/jornada que use a condição de click com operador **"Não" (não_existe/nao_existe)**.

---

## 🔁 Passo a Passo

1. Acessar a plataforma Userin e criar/editar uma **Regra**.
2. Adicionar condição de **Click** com toggle **"Não"** (Sim/Não) — ex: "Não clicou em btn-deposito".
3. Associar a regra a um componente (Modal, Block, etc.) ou usar como trigger em uma Jornada InSite.
4. Acessar o site do cliente com o SmartTracker ativo.
5. Navegar pelo site **sem clicar** no elemento especificado.
6. Observar que a regra **não dispara** corretamente ou **dispara incorretamente** em eventos não-CLICK.

---

## ❌ Resultado Atual

**Problema 1 — Trigger evaluation (**`evaluateCondition`):
Quando o evento atual NÃO é CLICK (ex: PAGE_VIEW, SCROLL), o engine retorna `true` para operadores negativos **sem consultar o SessionHistory**. Isso significa que a condição "não clicou em X" é avaliada como verdadeira em TODOS os eventos não-CLICK, independente do usuário já ter clicado anteriormente.

**Problema 2 — RuleMatchExecutor:**
O operador `não_existe` não é tratado e cai no fallback positivo (`clickTarget.includes(expectedClick)`), retornando resultado **invertido** do esperado.

---

## ✅ Resultado Esperado

* Quando o operador é **"não_existe"** (Não clicou) e o evento atual NÃO é CLICK, o engine deve **consultar o** `SessionHistory.hasEventMatching("CLICK", criteria)` e retornar `!hasEventInHistory`.
* Se o usuário já clicou no elemento X durante a sessão, a condição "não clicou em X" deve retornar **false**.
* Se o usuário **nunca clicou** no elemento X durante a sessão, a condição "não clicou em X" deve retornar **true**.
* O `RuleMatchExecutor.js` deve tratar explicitamente o operador `não_existe`.

---

## 🧪 Evidências

**Arquivos afetados:**

* `backend-plataforma/backend/src/interfaces/http/routes/engineRoutes.js` (linhas \~4025–4067)
* `backend-plataforma/backend/src/journey-builder/engine/nodes/conditions/RuleMatchExecutor.js` (linhas \~103–158)

**Comportamento observado via console do DevTools:**

* Regra de "não click" dispara em qualquer PAGE_VIEW sem respeitar histórico de clicks.
* Logs do engine mostram: `"click: evento atual não é CLICK..."` e retorna `true` sem verificar `SessionHistory`.

---

## 🎯 Priorização RICE — Score: 38.4

| Reach | Impact | Confidence | Effort | Score |
| -- | -- | -- | -- | -- |
| 8 | 3 (massive) | 80% | 0.5 meses | **38.4** |

**Justificativa:** Bug grave no engine de regras. Reach 8: qualquer empresa usando condições de "não click". Impacto massive (3): regras disparam incorretamente. Confidence 80%: causa raiz identificada nos dois arquivos. Esforço 0.5 meses: fix em 2 arquivos + testes.

## Histórico de status
- Backlog (backlog): 2026-03-19T19:12:57.934Z → 2026-03-19T19:45:21.438Z
- Refining (backlog): 2026-03-19T19:45:21.438Z → 2026-03-31T12:33:10.961Z
- To-do (unstarted): 2026-03-31T12:33:10.961Z → 2026-04-02T11:45:08.982Z
- Pull Request (started): 2026-04-02T11:45:08.982Z → 2026-06-22T17:15:41.779Z
- Released (completed): 2026-06-22T17:15:41.779Z → atual

## Relações
—

## Anexos
- fix(engine): SEND-413 + SEND-411 state polling access + SessionHistory click — https://github.com/sendspeed0/platform-backend/pull/28
- fix(engine): SEND-413 + SEND-411 — state polling access + SessionHistory click check — https://github.com/sendspeed0/platform-backend/pull/27
