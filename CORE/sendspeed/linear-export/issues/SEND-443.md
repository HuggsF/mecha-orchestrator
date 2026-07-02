# SEND-443 — 🐞 - Endpoint /api/auth/login retorna "Endpoint não encontrado" no ambiente DEV

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | Urgent |
| Responsável | Hugo Fernandes |
| Time | Sendspeed |
| Projeto | — |
| Labels | Bug, User Story, UserIn |
| Parent | — |
| Criada | 2026-04-01T12:24:47.079Z por Vinicius Carneiro |
| Iniciada | 2026-04-02T11:41:30.421Z |
| Concluída | 2026-06-22T17:15:39.504Z |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-443--endpoint-apiauthlogin-retorna-endpoint-nao-encontrado-no |
| URL | https://linear.app/sendspeed/issue/SEND-443/endpoint-apiauthlogin-retorna-endpoint-nao-encontrado-no-ambiente-dev |

## Descrição

## 📍 Onde ocorre

**Ambiente:** DEV — `platform-api-dev-userin-ai.fly.dev`
**Frontend:** `platform-dev-userin-ai.fly.dev/login`
**Endpoint afetado:** `POST /api/auth/login`

---

## 🔁 Passo a Passo

1. Acessar `https://platform-dev-userin-ai.fly.dev/login` (frontend)
2. Tentar realizar login com credenciais válidas
3. Ou acessar diretamente `https://platform-api-dev-userin-ai.fly.dev/api/auth/login` no browser

---

## ❌ Resultado Atual

A API retorna:

```json
{"success":false,"error":"Endpoint não encontrado"}
```

Essa resposta é gerada pelo middleware catch-all 404 em `backend/src/index.js` (linha \~340):

```javascript
app.use((req, res, next) => {
  res.status(404).json({
    success: false,
    error: 'Endpoint não encontrado'
  });
});
```

---

## 🔍 Investigação

### O que funciona:

| Teste | Resultado |
| -- | -- |
| `GET /health` | ✅ 200 OK — app está rodando |
| `POST /api/auth/login` (via curl) | ✅ Funciona — retorna "Credenciais inválidas" para dados de teste |
| Rota registrada em `authRoutes.js` | ✅ `router.post('/login', ...)` existe |
| Rota montada em `index.js` | ✅ `app.use('/api/auth', require('./interfaces/http/routes/authRoutes'))` |

### O que falha:

| Teste | Resultado |
| -- | -- |
| `GET /api/auth/login` (browser) | ❌ 404 — rota só aceita POST, GET cai no catch-all |
| Login via frontend (intermitente) | ❌ Reportado como não funcional |

### Possíveis causas:

1. **Falha intermitente no deploy DEV** — A máquina Fly.io pode ter reiniciado ou falhado temporariamente. O `auto_stop_machines = false` está configurado, mas a instância `shared-cpu-2x` com 2GB pode sofrer pressão de memória.
2. **Timeout de conexão MongoDB** — Se o MongoDB não responde, o app sobe mas as rotas que dependem de DB falham silenciosamente. O health check (`/health`) retorna 200 independente do estado do DB.
3. **CORS bloqueando o frontend** — O frontend em `platform-dev-userin-ai.fly.dev` faz POST para `platform-api-dev-userin-ai.fly.dev/api/auth/login`. Se o CORS não permite a origin do frontend DEV, o preflight (OPTIONS) falha e o browser reporta como erro de rede.
4. **Variáveis de ambiente ausentes no DEV** — Se `MONGODB_URI` ou `JWT_SECRET` não estão configurados no ambiente DEV (Fly.io secrets), o app pode falhar na inicialização das rotas.

---

## ✅ Resultado Esperado

* `POST /api/auth/login` deve **sempre** retornar resposta válida (sucesso ou erro de credenciais) no ambiente DEV
* O frontend em `platform-dev-userin-ai.fly.dev/login` deve conseguir autenticar normalmente
* Health check deve refletir o estado real da aplicação (incluindo conexão DB)

---

## 🔧 Ações sugeridas

1. Verificar logs do app DEV no Fly.io: `fly logs -a platform-api-dev-userin-ai`
2. Verificar se MongoDB está acessível: `fly ssh console -a platform-api-dev-userin-ai`
3. Verificar secrets configurados: `fly secrets list -a platform-api-dev-userin-ai`
4. Melhorar health check para incluir status do MongoDB (retornar 503 se DB desconectado)
5. Adicionar CORS origin explícito para `platform-dev-userin-ai.fly.dev`

---

## 📁 Arquivos relevantes

* `backend-plataforma/backend/src/index.js` — middleware 404 (linha \~340), registro de rotas (linha \~279), CORS config
* `backend-plataforma/backend/src/interfaces/http/routes/authRoutes.js` — rota `POST /login`
* `backend-plataforma/backend/src/interfaces/http/controllers/authController.js` — handler do login
* `backend-plataforma/deploy/fly.development.toml` — config Fly.io DEV
* `sendspeed-engage-ai-flow-08/client/src/config/env.ts` — URL do backend DEV
* `sendspeed-engage-ai-flow-08/client/src/lib/api.ts` — `loginInstance.post('/auth/login', ...)`

---

## 🎯 Priorização RICE — Score: 48.0

| Reach | Impact | Confidence | Effort | Score |
| -- | -- | -- | -- | -- |
| 10 | 3 (massive) | 80% | 0.5 meses | **48.0** |

**Justificativa:** Reach 10: login é a porta de entrada — afeta todos os usuários e devs que acessam o ambiente DEV. Impacto massive (3): sem login funcional, o ambiente DEV inteiro fica inacessível para testes e desenvolvimento. Confidence 80%: o endpoint existe e funciona via curl, indicando problema de infraestrutura/deploy e não de código. Esforço 0.5 meses: diagnóstico de infra (logs, secrets, CORS) + melhoria do health check para refletir estado real da aplicação.

## Histórico de status
- Backlog (backlog): 2026-04-01T12:24:47.079Z → 2026-04-01T12:27:58.796Z
- Refining (backlog): 2026-04-01T12:27:58.796Z → 2026-04-01T12:28:52.227Z
- To-do (unstarted): 2026-04-01T12:28:52.227Z → 2026-04-02T11:41:30.437Z
- Pull Request (started): 2026-04-02T11:41:30.437Z → 2026-06-22T17:15:39.525Z
- Released (completed): 2026-06-22T17:15:39.525Z → atual

## Relações
—

## Anexos
- fix(infra): CORS origins for DEV/STG + MongoDB health check [SEND-443] — https://github.com/sendspeed0/platform-backend/pull/26
