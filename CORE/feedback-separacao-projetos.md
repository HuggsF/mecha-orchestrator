---
name: Separacao de projetos e fronteira de informacao
description: Os 4 projetos da Vanessa sao independentes. Dados sensiveis da Prefeitura NUNCA compartilhados. Conhecimento tecnico pode cruzar fronteiras.
type: feedback
---

Vanessa trabalha em 4 frentes independentes:

| Projeto | Contexto | Equipe |
|---------|----------|--------|
| **Prefeitura do Recife** | Trabalho CLT — ETL CNES, ArcGIS, PostGIS, dados publicos | Equipe interna Prefeitura |
| **AlphaTM** | Projeto separado — ERP, PostgreSQL + FastAPI | Mesma equipe do Omega (Hugo, Amanda, Vanessa) |
| **OmegaHuggsTeam** | Projeto separado — HuggsAI CRM, pipelines de IA | Hugo, Amanda, Vanessa |
| **Claud-IO** | Projeto pessoal — bot Telegram do Claudio | Vanessa |

**AlphaTM NAO e trabalho da Prefeitura.** Sao coisas completamente diferentes. AlphaTM e um projeto com a mesma equipe do Omega, mas tambem e diferente do Omega.

## Regra de fronteira

- **Informacoes sensiveis da Prefeitura** (credenciais, dados internos, IPs, nomes de servidores, schemas especificos, dados de pacientes/cidadaos): NUNCA compartilhar com nenhum outro projeto.
- **Conhecimento tecnico** (padroes de ETL, SQL, deduplicacao, COPY, pipelines, arquitetura): PODE ser compartilhado livremente entre projetos.

**Why:** Vanessa tem obrigacao profissional com dados da Prefeitura. Misturar contextos pode vazar informacao sensivel para repos compartilhados ou documentos sincronizados com outros projetos.

**How to apply:**
- Ao salvar no claudio-knowledge-base: so conhecimento tecnico generico, sem mencionar schemas, tabelas, IPs ou dados especificos da Prefeitura.
- Ao sincronizar com Gemini/Claud-IO: nunca incluir detalhes operacionais da Prefeitura.
- Ao criar memorias: separar claramente qual projeto e qual. Nunca descrever AlphaTM como "trabalho Prefeitura".
- Referencia tecnica (ex: "pattern de DISTINCT em CTE pra evitar fan-out") pode ir pra qualquer lugar.
