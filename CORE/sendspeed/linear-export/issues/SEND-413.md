# SEND-413 — 🐞 - Regra de URL (last/current) com gatilho "acesso logado" não dispara

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | Urgent |
| Responsável | Hugo Fernandes |
| Time | Sendspeed |
| Projeto | — |
| Labels | Bug, Regras, UserIn, User Story |
| Parent | — |
| Criada | 2026-03-19T19:14:39.211Z por Vinicius Carneiro |
| Iniciada | 2026-04-02T11:45:04.171Z |
| Concluída | 2026-06-22T17:15:42.657Z |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-413--regra-de-url-lastcurrent-com-gatilho-acesso-logado-nao |
| URL | https://linear.app/sendspeed/issue/SEND-413/regra-de-url-lastcurrent-com-gatilho-acesso-logado-nao-dispara |

## Descrição

## 📍 Onde ocorre

**Engine client-side** — Arquivo `engineRoutes.js` (polling de condições, linhas \~5800–5825).

Afeta regras que combinam condições de **URL** (`page_view_last` e `page_view_current`) com condição de **acesso** (`access: logged_in`).

---

## 🔁 Passo a Passo

1. Criar uma regra na plataforma Userin com as seguintes condições (operador AND):
   * **URL última**: contém `/games` (page_view_last)
   * **URL atual**: contém `home` (page_view_current)
   * **Acesso**: está logado (access = logged_in)
2. Associar a regra como trigger de uma jornada InSite.
3. Acessar o site do cliente.
4. Navegar de `/games` para a `home` (gera PAGE_VIEW).
5. Fazer login no site (modal de login, sem navegação).
6. A regra **NÃO dispara** mesmo com todas as condições satisfeitas.

Mesma situação ocorre com `/sports` → `home`.

---

## ❌ Resultado Atual

**Causa raiz:** `access` não é tratado como condição de estado (state condition).

O engine possui um polling (`setInterval` de 1500ms) que reavalia condições de estado. Porém, `access` não está na lista de `_stateCondTypes`:

```javascript
// engineRoutes.js ~linha 5800
const _stateCondTypes = ["element_visible", "profile_attribute", "user_attribute", "has_tag"];
// "access" NAO ESTA AQUI

const hasStateCond = conds.some(c => {
  const ev = (c.evento || c.event || "").toLowerCase();
  return _stateCondTypes.includes(ev);
});
if (!hasStateCond) return; // Pula polling se nao tem state condition
```

**Fluxo do problema:**

1. Usuário navega de `/games` → `home` → PAGE_VIEW dispara avaliação.
2. URL last = `/games` ✔️, URL current = `home` ✔️, access = not logged ❌ → Regra NÃO match.
3. Usuário faz login (sem navegar) → `sessionStorage.userin_login` é setado.
4. **Nenhum novo PAGE_VIEW** → avaliação não roda novamente.
5. **Polling não roda** porque `access` não está em `_stateCondTypes`.
6. Regra nunca é reavaliada → não dispara.

**Problema secundário — URL "home" vs "/":**
Se a página inicial do site usa path `/` em vez de `/home`, a condição `"/".includes("home")` retorna `false`. Depende de como o site mapeia a rota "home".

---

## ✅ Resultado Esperado

* Ao fazer login sem navegar, a regra deve ser **reavaliada automaticamente** pelo polling.
* Se URL last = `/games`, URL current = `home` e acesso = logado, a regra deve **disparar**.
* Mesma lógica para URL last = `/sports` com URL current = `home`.

**Fix sugerido:** Adicionar `access` ao array `_stateCondTypes`:

```javascript
const _stateCondTypes = ["element_visible", "profile_attribute", "user_attribute", "has_tag", "access"];
```

---

## 🎯 Priorização RICE — Score: 96.0

| Reach | Impact | Confidence | Effort | Score |
| -- | -- | -- | -- | -- |
| 8 | 3 (massive) | 100% | 0.25 meses | **96.0** |

**Justificativa:** Maior score RICE do backlog. Bug com causa raiz já identificada e fix de 1 linha. Reach 8: afeta todas as empresas com regras de URL + acesso logado. Impacto massive (3): regras simplesmente não disparam. Confidence 100%: fix documentado e trivial. Esforço mínimo (0.25 meses).

## Histórico de status
- Backlog (backlog): 2026-03-19T19:14:39.211Z → 2026-03-19T19:45:09.179Z
- Refining (backlog): 2026-03-19T19:45:09.179Z → 2026-03-31T12:33:12.166Z
- To-do (unstarted): 2026-03-31T12:33:12.166Z → 2026-04-02T11:45:04.178Z
- Pull Request (started): 2026-04-02T11:45:04.178Z → 2026-06-22T17:15:42.665Z
- Released (completed): 2026-06-22T17:15:42.665Z → atual

## Relações
—

## Anexos
- fix(engine): SEND-413 + SEND-411 state polling access + SessionHistory click — https://github.com/sendspeed0/platform-backend/pull/28
- fix(engine): SEND-413 + SEND-411 — state polling access + SessionHistory click check — https://github.com/sendspeed0/platform-backend/pull/27
