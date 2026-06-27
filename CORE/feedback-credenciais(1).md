---
name: Nunca exibir credenciais ou conteudo sensivel
description: Regra absoluta — nunca exibir senhas, tokens, API keys, connection strings ou qualquer dado sensivel no output. Mascarar sempre.
type: feedback
---

NUNCA exibir credenciais, senhas, tokens, API keys, connection strings ou qualquer conteudo sensivel no output da conversa.

Ao ler arquivos como `.env`, `.env.docker`, `credentials.*`, configs com senhas:
- Mostrar apenas a **estrutura** (nomes das variaveis), nunca os valores
- Mascarar valores sensiveis com `***` ou `[REDACTED]`
- Se precisar validar que um valor existe, dizer apenas "presente" ou "ausente"

**Why:** Vanessa trabalha com bancos de producao da Prefeitura e do time Omega. Credenciais expostas no output da conversa sao um risco de seguranca. Erro cometido em 24/03/2026 ao exibir o .env completo com senhas de banco.

**How to apply:** Toda vez que um arquivo potencialmente sensivel for lido, filtrar o output antes de mostrar. Isso vale para qualquer ambiente — trabalho, pessoal, Omega. Sem excecoes.
