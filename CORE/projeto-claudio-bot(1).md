---
name: Projeto Claud-IO Bot
description: Bot Telegram do Claudio — v2 com Claude Agent SDK, RAG ChromaDB, Domain Router, privacidade por usuario, 12 comandos. PR #3 aberto.
type: project
---

O Claud-IO e um bot Telegram que funciona como **versao portatil do Claudio** (o assistente Claude Code da Vanessa). A ideia e que a Vanessa tenha acesso ao assistente pelo celular/Telegram, com memoria persistente e contexto do time.

**Repositorio:** https://github.com/Vr-Farias/claudio-bot (privado)
**Branch principal:** master
**Status (27/03/2026):** v2 + v1.1 mergidos, PR #3 aberto com melhorias

## Stack atual (pos-v2)
- Python + python-telegram-bot 21.6
- LLM: **Claude Agent SDK** (substituiu Groq/LLaMA) — via CLAUDE_CODE_OAUTH_TOKEN
- RAG: **ChromaDB** (memoria semantica, privacidade por usuario)
- Triage: **Domain Router** (portado do engine-service PR #44, 7 dominios, rules.yml)
- Email: SMTP com TLS (email_sender/sender.py)
- Memoria: JSON local (expandida: 500 msgs/usuario, ficha completa)
- GitHub: consulta atividade dos repos via API
- Deploy planejado: **Railway** (Procfile + railway.toml)

## Pipeline v2
```
Whitelist -> RateLimit -> InjectionDefense -> Triage -> RAG -> Claude SDK
```

## Estrutura modular (apos PR #3)
- handlers/core.py — /start, /help, /clear, seguranca
- handlers/profile.py — /perfil, /email, /estilo, /config
- handlers/team.py — /share, /status, /memory, /relatorio, /buscar
- llm/claude_client.py — call_claude() com retry/backoff
- rag/store.py — RAGStore com privacidade (user_id + visibility)
- triage/domain_router.py + rules.yml + schema_validator.py
- email_sender/sender.py — SMTP sender
- memory/store.py — MemoryStore (500 msgs, ficha expandida, thread-safe)

## 12 comandos
/start, /help, /clear, /perfil, /email, /estilo, /config, /share, /status, /memory, /relatorio, /buscar

## PRs (27/03/2026)
- **PR #1 MERGED** — v2: Claude SDK + RAG ChromaDB + Domain Router + 45 testes
- **PR #2 MERGED** — v1.1: memoria 500, privacidade RAG, /email, /relatorio, /estilo, /perfil
- **PR #3 ABERTO** — fix rules.yml, retry backoff, handlers refactor, /config, /buscar

## Seguranca
- [x] Whitelist de chat IDs (fail-closed)
- [x] Rate limiting (10 msg/min)
- [x] Prompt injection defense (35+ patterns, unicode normalization)
- [x] System prompt sanitizado
- [x] Dados dinamicos fora do git
- [x] Historico git limpo (filter-branch)
- [x] Retry com backoff (3 tentativas, 1s/2s/4s)
- [x] Limite de tamanho de mensagem (2000 chars)
- [x] MemoryStore: sanitizacao, escrita atomica, thread-safe
- [x] Privacidade RAG: mensagens privadas por usuario
- [x] Schema validator no rules.yml

## Pendencias
- [ ] Mergir PR #3 (fix + melhorias)
- [ ] Preencher ALLOWED_CHAT_IDS com chat_ids reais
- [ ] Deploy no Railway
- [ ] Testar pipeline completo E2E
- [ ] v3 futura: Neo4j pra grafos de conhecimento

**Why:** Vanessa quer acesso ao assistente de qualquer lugar, sem depender do PC ligado. Agora e assistente de time (nao mais pessoal).

**How to apply:** priorizar deploy e teste E2E. Neo4j entra na v3. Toda melhoria deve preservar a essencia do Claudio.
