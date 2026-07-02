# SEND-438 — MongoDB DEV read-only — user `govtech` sem permissão de escrita (login falha)

| Campo | Valor |
| -- | -- |
| Status | To-do (unstarted) |
| Prioridade | High |
| Responsável | thiago.melin@sendspeed.com |
| Time | Sendspeed |
| Projeto | — |
| Labels | UserIn, Bug |
| Parent | SEND-415 |
| Criada | 2026-03-31T19:54:40.868Z por Hugo Fernandes |
| Iniciada | — |
| Concluída | — |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-438-mongodb-dev-read-only-user-govtech-sem-permissao-de-escrita |
| URL | https://linear.app/sendspeed/issue/SEND-438/mongodb-dev-read-only-user-govtech-sem-permissao-de-escrita-login |

## Descrição

## Contexto

Durante a validação E2E do fix @SEND-415 (feature flag para ocultar "Gerar Jornada com IA"), descobrimos que o **ambiente DEV está com MongoDB read-only**, impedindo login.

## Diagnóstico

| Ambiente | Fly App | MongoDB URI | DB User | DB Name | Status |
| -- | -- | -- | -- | -- | -- |
| **DEV** | `platform-api-dev-userin-ai` | `teste-ai.s7g5evd.mongodb.net` | `govtech` | `userin-development` | **Read-only** |
| **STG** | `platform-api-stg-userin-ai` | `teste-ai.s7g5evd.mongodb.net` | `aplicacoes` | `userin-staging` | **Read-write** |

Ambos apontam para o **mesmo cluster MongoDB Atlas** (`teste-ai`), porém com users diferentes.

## Evidência técnica

O login com `admin@sendspeed.com` / senha correta:

1. **Autentica com sucesso** (encontra o usuário `SendSpeed Admin` no banco)
2. **Falha ao gravar activity log** — MongoDB retorna: `not authorized on userin-development to execute command { insert: "activities" }`
3. Backend retorna **401** para o frontend (embora a autenticação em si tenha funcionado)

## Impacto

* **Login no DEV completamente quebrado** — nenhum usuário consegue logar
* Impossível validar qualquer fix no ambiente DEV
* Testes E2E no DEV inviáveis

## Fix sugerido

No MongoDB Atlas, conceder permissão **readWrite** ao user `govtech` no database `userin-development`.

OU trocar a MONGODB_URI do DEV para usar o user `aplicacoes` (mesmo do STG) apontando para `userin-development`:

```
mongodb+srv://aplicacoes:<password>@teste-ai.s7g5evd.mongodb.net/userin-development?retryWrites=true&w=majority
```

## Como validar

```bash
flyctl ssh console -a platform-api-dev-userin-ai -C "printenv MONGODB_URI"
curl -X POST https://platform-api-dev-userin-ai.fly.dev/api/auth/login -H 'Content-Type: application/json' -d '{"email":"admin@sendspeed.com","password":"sendspeed@2024"}'
```

Se retornar 200 com token JWT, está corrigido.

## Histórico de status
- Backlog (backlog): 2026-03-31T19:54:40.868Z → 2026-04-01T12:08:25.238Z
- To-do (unstarted): 2026-04-01T12:08:25.238Z → atual

## Relações
—

## Anexos
—
