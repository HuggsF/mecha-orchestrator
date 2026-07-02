# SEND-414 — 🚀 - Operadores numéricos para regras de Atributo de Perfil

| Campo | Valor |
| -- | -- |
| Status | Backlog (backlog) |
| Prioridade | High |
| Responsável | — |
| Time | Sendspeed |
| Projeto | — |
| Labels | Implementação, Regras, UserIn, User Story |
| Parent | — |
| Criada | 2026-03-19T19:34:47.402Z por Vinicius Carneiro |
| Iniciada | — |
| Concluída | — |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-414--operadores-numericos-para-regras-de-atributo-de-perfil |
| URL | https://linear.app/sendspeed/issue/SEND-414/operadores-numericos-para-regras-de-atributo-de-perfil |

## Descrição

> **Como** operador da plataforma Userin configurando regras de segmentação
> **Quero** que as condições de Atributo de Perfil numérico disponibilizem os operadores: É igual a, É maior que, É igual ou maior e É igual ou menor
> **Para** criar regras precisas baseadas em métricas numéricas do perfil do usuário (ex: Qtd Wins, Sequência de Perdas, Score) e acionar componentes/jornadas com maior granularidade.

---

# 📈 Use Case: Segmentação por métricas numéricas de jogadores

Um operador de uma plataforma de jogos quer criar regras para exibir ofertas personalizadas com base no comportamento do jogador:

* **"Sequência de Perdas" é igual ou maior que 5** → Mostrar modal com bônus de recuperação.
* **"Qtd Wins" é igual ou menor que 2** → Exibir block incentivando participação em torneios.
* **"Score" é maior que 1000** → Habilitar jornada VIP.
* **"Qtd Wins" é igual a 10** → Exibir conquista especial.

Atualmente, os operadores **"É igual ou maior" (>=)** e **"É igual ou menor" (<=)** não estão disponíveis no dropdown. Apenas "Maior que" e "Menor que" existem, impedindo segmentações que incluam o valor limite.

---

# ✅ Critérios de aceite:

* O dropdown de operadores para atributos numéricos (`profile_attribute` / `user_attribute`) deve exibir **exatamente**: É igual a, É maior que, É igual ou maior, É igual ou menor.
* O operador `maior_ou_igual` deve avaliar `>=` corretamente no engine client-side.
* O operador `menor_ou_igual` deve avaliar `<=` corretamente no engine client-side.
* O campo de valor deve aceitar apenas entrada numérica quando o atributo é do tipo `number`.
* Regras existentes com operadores antigos devem continuar funcionando sem regressão.

---

# 🧩 Cenários de teste:

- [ ] Dropdown exibe apenas: É igual a, É maior que, É igual ou maior, É igual ou menor.
- [ ] Regra "Sequência de Perdas" **É igual ou maior que** 5 → valor 5 = match ✔️
- [ ] Regra "Sequência de Perdas" **É igual ou maior que** 5 → valor 4 = NÃO match ✔️
- [ ] Regra "Qtd Wins" **É igual ou menor que** 2 → valor 2 = match ✔️
- [ ] Regra "Qtd Wins" **É igual ou menor que** 2 → valor 3 = NÃO match ✔️
- [ ] Regra "Score" **É maior que** 5 → valor 5 = NÃO match (apenas >5) ✔️
- [ ] Regra "Score" **É maior que** 5 → valor 6 = match ✔️
- [ ] Regra "Score" **É igual a** 10 → valor 10 = match ✔️
- [ ] Regra "Score" **É igual a** 10 → valor 11 = NÃO match ✔️
- [ ] Operadores funcionam em **Jornada InSite** (condition.ruleMatch).
- [ ] Operadores funcionam no **polling** do engine (condições de estado).
- [ ] Regras existentes com operadores antigos não sofrem regressão.

---

## 🎯 Priorização RICE — Score: 12.8

| Reach | Impact | Confidence | Effort | Score |
| -- | -- | -- | -- | -- |
| 8 | 2 (high) | 80% | 1 mês | **12.8** |

**Justificativa:** Reach 8: empresas de iGaming precisam segmentar por métricas numéricas. Impacto high (2): habilita regras que hoje não são possíveis (>= e <=). Confidence 80%: lógica clara. Esforço 1 mês: frontend + engine + testes.

## Histórico de status
- Backlog (backlog): 2026-03-19T19:34:47.402Z → 2026-03-19T19:45:55.088Z
- Refining (backlog): 2026-03-19T19:45:55.088Z → 2026-03-31T12:33:41.008Z
- To-do (unstarted): 2026-03-31T12:33:41.008Z → 2026-03-31T18:37:05.999Z
- Refining (backlog): 2026-03-31T18:37:05.999Z → 2026-04-16T20:33:15.136Z
- Backlog (backlog): 2026-04-16T20:33:15.136Z → 2026-04-16T20:33:26.548Z
- To-do (unstarted): 2026-04-16T20:33:26.548Z → 2026-04-16T20:33:29.084Z
- Backlog (backlog): 2026-04-16T20:33:29.084Z → 2026-04-16T20:33:35.303Z
- Refining (backlog): 2026-04-16T20:33:35.303Z → 2026-04-24T13:59:03.011Z
- Backlog (backlog): 2026-04-24T13:59:03.011Z → atual

## Relações
—

## Anexos
—
