---
name: Sessao 2026-03-27-b (outra CLI)
description: Claud-IO evoluiu massivamente — v2 (Claude SDK + RAG + Triage) e v1.1 (memoria, privacidade, comandos) mergidos, PR #3 aberto com handlers refactor
type: project
---

# Sessao 2026-03-27-b — Claud-IO (feito em outra sessao CLI, salvo retroativamente)

## PR #1 — MERGED — feat: Claud-IO v2
- **Groq substituido por Claude Agent SDK** (CLAUDE_CODE_OAUTH_TOKEN)
- **RAG semantico com ChromaDB** — rag/store.py com RAGStore, ingere memoria coletiva + /share, recupera contexto por similaridade
- **Domain Router portado do PR #44 do Omega** — triage/domain_router.py + rules.yml (7 dominios, threshold 0.7)
- **Schema validator** — valida rules.yml no load, fail-fast (sugestao do Henrique)
- **Pipeline v2**: Whitelist -> RateLimit -> InjectionDefense -> Triage -> RAG -> Claude SDK
- **Deploy Railway** — Procfile + railway.toml (substituiu Oracle Cloud como opcao)
- 17 arquivos novos/modificados, 45 testes (triage, schema, RAG)
- Commit: 6db1ce2

## PR #2 — MERGED — feat: Claud-IO v1.1
- **Memoria expandida**: 50 -> 500 msgs/usuario, ficha com telegram/github/email/funcao/estilo
- **Privacidade no RAG**: user_id + visibility (public/private), mensagens privadas por usuario, /share publico
- **Comandos novos**: /email, /relatorio (gera e envia por SMTP), /estilo (detailed/pragmatic/summary), /perfil
- **System prompt atualizado**: tom Jarvis+Visao+Marvin, anti-alucinacao, confidencialidade Prefeitura, linguagem adaptativa
- **Email sender**: modulo SMTP com TLS (email_sender/sender.py)
- Auto-migracao de usuarios antigos sem campos novos
- Merge: 0c1e725

## PR #3 — ABERTO — feat: v1.1 improvements
- **fix**: rules.yml alinhado com schema_validator (confidence_per_match -> confidence_weight)
- **feat**: retry com backoff no Claude client (3 tentativas, 1s/2s/4s)
- **refactor**: handlers extraidos do main.py -> handlers/core.py, handlers/profile.py, handlers/team.py
- **feat**: /config (config unificada de perfil), /buscar (busca semantica explicita no RAG)
- **feat**: /help atualizado com 12 comandos
- main.py agora e so orquestrador (~48 linhas vs ~418 antes)

## Mudancas arquiteturais importantes
- Groq -> Claude Agent SDK (GRANDE mudanca, elimina terceiro no pipeline)
- ChromaDB integrado como RAG store (era planejado pra v2, ja esta no bot)
- Domain Router do engine-service portado pro bot
- Deploy migrou de Oracle Cloud pra Railway
- Estrutura modularizada: handlers/, llm/, rag/, triage/, email_sender/

## Commits do dia no repo
- 89e24a6 — docs: update .env.example for v1.1
- 3745b7b — feat: add dynamic signature to /relatorio
- 0c1e725 — merge: v1.1 features into master
- 6db1ce2 — feat: v2 Claude Agent SDK + RAG + Domain Router
- 36a5327 — feat: implement v1.1 commands and privacy pipeline
