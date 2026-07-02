# SEND-436 — 🐞 - [EXPEDITE] Visão Geral (Segmentos): dados errados em algumas empresas e tela não carrega em outras

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | Urgent |
| Responsável | Vinicius Carneiro |
| Time | Sendspeed |
| Projeto | — |
| Labels | — |
| Parent | — |
| Criada | 2026-03-31T15:20:52.803Z por Vinicius Carneiro |
| Iniciada | 2026-03-31T15:41:17.761Z |
| Concluída | 2026-04-14T15:16:16.694Z |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-436--expedite-visao-geral-segmentos-dados-errados-em-algumas |
| URL | https://linear.app/sendspeed/issue/SEND-436/expedite-visao-geral-segmentos-dados-errados-em-algumas |

## Descrição

## 📍 Onde ocorre

**Página:** `/segments` — "Visão Geral" (Funil de Estágios, Evolução Semanal, Top Tags)

**Ambiente:** Staging

---

## 🔁 Sintomas

### Sintoma 1 — Dados errados/zerados (ex: bet.bet)

* Funil mostra 43.856 ANONYMOUS, mas REGISTERED = 0, FTD = 0, MTD = 0
* Todas as taxas de conversão (Cadastro, FTD, Retorno) aparecem como **0.0%**
* Os dados parecem existir no banco mas não são exibidos corretamente

### Sintoma 2 — Tela não carrega (ex: Jogão em staging)

* A página fica permanentemente em estado de **skeleton/loading**
* Nenhum dado é exibido — funil, evolução semanal e top tags ficam em placeholder

---

## 📸 Evidências

### 

### Print 1 — Donald.bet (dados errados/zerados)

Empresa donald.bet em produção. Funil mostra 43.856 ANONYMOUS porém REGISTERED, FTD e MTD todos zerados. Todas as taxas de conversão (Cadastro, FTD, Retorno) em 0.0%.

> **[Imagem 1 — transcrição]:** Screenshot de UI (dashboard "Visão Geral" da plataforma UserIn/Segmentos) para a empresa "Donald Bet" (usuário logado "Donald Admin", idioma Português (Brasil)). Cabeçalho "Visão Geral — Acompanhe a evolução dos seus segmentos mês a mês · Atualizado em 30/03, 13:31". Controles: toggle "Semana/Mês" (Mês selecionado), navegação de período "1-31", botão de refresh e botão "Configurar Regras". Seção "Funil de Estágios" (Total: 1 usuários) com 4 cards: ANONYMOUS = 1 (100.0% do total); REGISTERED = 0 (0.0% do total); FTD = 0 (0.0% do total); MTD = 0 (0.0% do total). Abaixo, três taxas de conversão: Cadastro = 0.0%, FTD = 0.0%, Retorno = 0.0%. Legenda de cores: Anonymous, Registered, FTD, MTD. Seção "Evolução Mensal" com toggles "Usuários/FTDs/Receita" (Usuários selecionado). Seção "Top Tags" (1 usuários): item "New User" com 1 (100.0%). Observação: apesar do texto do card mencionar 43.856 ANONYMOUS, o screenshot renderizado mostra Total: 1 usuário — evidenciando dados incorretos/inconsistentes na tela.

### Print 2 — Jogão staging (não carrega)

Empresa Jogão em staging (`platform-stg-userin-ai.fly.dev/segments`). Tela permanece em skeleton loading infinito. Nenhum componente renderiza dados.

> **[Imagem 2 — transcrição]:** Screenshot de UI (dashboard "Visão Geral") para a empresa "Jogão" (usuário logado "Jogão Administrador", idioma Português (Brasil)). Cabeçalho "Visão Geral — Acompanhe a evolução dos seus segmentos semana a semana". Controles: toggle "Semana/Mês" (Semana selecionado), período "29 Mar - 4 Abr", refresh e "Configurar Regras". A tela está em estado de skeleton/loading permanente: os 5 cards do topo mostram apenas placeholders cinza (sem números), a seção "Funil de Estágios" exibe 4 grandes blocos cinza vazios, e as seções "Evolução Semanal" e "Top Tags" também mostram apenas placeholders. Nenhum dado real renderizado.

---

## 🔍 Análise de Código — Causas Raíz Identificadas

### Causa 1 — Tela não carrega: `companyId` ausente no contexto

**Arquivo:** `sendspeed-engage-ai-flow-08/client/src/pages/SegmentsOverviewPage.tsx` (linhas \~129-138)

```tsx
if (!companyId) {
  return (
    <Layout>
      <div className="flex flex-col items-center justify-center py-20">
        <RefreshCw className="w-8 h-8 text-slate-400 animate-spin mb-4" />
        <p className="text-slate-500">Carregando...</p>
      </div>
    </Layout>
  );
}
```

Se o JWT do usuário não tem o campo `c` (companyId) ou o `/auth/me` não retorna company, a página **nunca sai do loading**. `loadData` nem executa porque começa com `if (!companyId) return`.

### Causa 2 — Tela não carrega: `VITE_BACKEND_SEGMENTS` com default `localhost:3055`

**Arquivo:** `sendspeed-engage-ai-flow-08/client/src/config/env.ts`

Se a env var `VITE_BACKEND_SEGMENTS` não está configurada no build de staging, as requisições vão para `http://localhost:3055` no navegador do usuário — que não existe. Requests ficam **pendurados indefinidamente** e `setIsLoading(false)` nunca roda.

### Causa 3 — Dados errados: fórmula de conversão em `StageFunnel.tsx`

**Arquivo:** `sendspeed-engage-ai-flow-08/client/src/components/segments/dashboard/StageFunnel.tsx`

As taxas são calculadas como:

* Cadastro = `registered / anonymous * 100`
* FTD = `ftd / registered * 100`
* Retorno = `mtd / ftd * 100`

Se os stage counts são **buckets mutuamente exclusivos** (não cumulativos), as divisões estão conceitualmente erradas. Se `registered = 0`, FTD fica `NaN`.

### Causa 4 — Dados errados: response shape de `getUserProfileStats`

**Arquivo:** `sendspeed-engage-ai-flow-08/client/src/utils/segmentsApi.ts`

`getUserProfileStats` retorna `result` direto do JSON. Outros métodos usam `result.data || result`. Se o endpoint retorna `{ success, data: UserProfileStats }`, o objeto `userStats` vai ter a shape errada e `stats?.byStage` fica `undefined` — funil mostra zeros.

### Causa 5 — Sem auth nos requests ao segment-engine

**Arquivo:** `sendspeed-engage-ai-flow-08/client/src/utils/segmentsApi.ts`

`segmentsApi` usa `fetch` plain sem header `Authorization`. Se o segment-engine em staging exige token, as requests são rejeitadas silenciosamente.

### Causa 6 — Stale closure em `loadData`

**Arquivo:** `sendspeed-engage-ai-flow-08/client/src/pages/SegmentsOverviewPage.tsx`

`loadData` é `useCallback` com deps `[companyId, periodType, toast]` mas usa `availablePeriods` e `selectedPeriod` do render anterior.

---

## 📁 Arquivos afetados

| Arquivo | Problema |
| -- | -- |
| `client/src/pages/SegmentsOverviewPage.tsx` | Guard `!companyId` sem timeout/fallback; stale closure |
| `client/src/config/env.ts` | Default `localhost:3055` para segment-engine |
| `client/src/utils/segmentsApi.ts` | Response shape inconsistente; sem auth header |
| `client/src/components/segments/dashboard/StageFunnel.tsx` | Fórmula de conversão assume dados cumulativos |

---

## ✅ Resultado Esperado

* Tela carrega para **todas** as empresas, incluindo Jogão em staging
* Se `companyId` não existe após timeout, exibir mensagem de erro (não skeleton infinito)
* Funil mostra dados corretos: ANONYMOUS, REGISTERED, FTD, MTD com valores reais
* Taxas de conversão calculadas corretamente, tratando divisão por zero
* `VITE_BACKEND_SEGMENTS` configurado corretamente em staging e produção
* Requests ao segment-engine com auth header quando necessário

---

## 🎯 Priorização RICE — Score: 48.0 (#2 no To-do)

| Reach | Impact | Confidence | Effort | Score |
| -- | -- | -- | -- | -- |
| 10 | 3 (massive) | 80% | 0.5 meses | **48.0** |

**Justificativa:** Reach 10: a Visão Geral é a primeira tela que todo usuário vê ao acessar Segmentos — afeta 100% dos usuários da plataforma. Impacto massive (3): para algumas empresas a tela simplesmente não carrega (bloqueio total), e para outras mostra dados zerados/errados (dashboard inútil). Confidence 80%: 6 causas raíz identificadas no código, mas precisa validar quais estão ativas em cada ambiente. Esforço 0.5 meses: maioria dos fixes são pontuais (env var, response shape, guard com timeout, fórmula).

## Histórico de status
- Backlog (backlog): 2026-03-31T15:20:52.803Z → 2026-03-31T15:21:19.765Z
- To-do (unstarted): 2026-03-31T15:21:19.765Z → 2026-03-31T15:41:17.771Z
- In Progress (started): 2026-03-31T15:41:17.771Z → 2026-03-31T18:42:54.769Z
- Product Review (started): 2026-03-31T18:42:54.769Z → 2026-04-14T15:16:16.707Z
- Released (completed): 2026-04-14T15:16:16.707Z → atual

## Relações
—

## Anexos
—
