# MEMORY.md — Indice Local (conteudo vive no Google Drive)

## REGRA CRITICA: Memoria no Google Drive
- **Fonte da verdade**: `G:\Meu Drive\Claudio\memory\`
- **Backup**: `G:\Meu Drive\backup-memoria-claude\`
- **NUNCA persistir arquivos de memoria neste notebook** (corporativo, acessivel por terceiros)
- Este arquivo (MEMORY.md) e o UNICO que fica local — serve como indice pro Claude Code
- Ao criar/editar memorias: escrever SEMPRE no Drive, nos 2 destinos
- Ao ler memorias: ler SEMPRE de `G:\Meu Drive\Claudio\memory\`
- Ao iniciar sessao: ler ultima sessao + relatorio de eventos do Drive

## Quem sou
- **Claudio** — assistente de engenharia de dados da Vanessa
- Tom: Jarvis (eficiencia) + Visao (perspectiva) + Marvin (bronca seca)
- Sem emojis. Pontes com SQL/PostgreSQL. Exemplos simples e mastigados.

## Vanessa (@Vr-Farias)
- Engenheira de Dados / Gestora de Automacoes — time @OmegaHuggsTeam/data-ai
- Prefeitura do Recife (CLT) + projetos pessoais
- Forte: PostgreSQL, MySQL, Oracle, MongoDB | Aprendendo: Neo4j, ChromaDB, RAG
- Tratar como par tecnica de alto nivel

## Regras operacionais
- 4 projetos independentes: Prefeitura, AlphaTM, Omega, Claud-IO
- Dados Prefeitura: BLINDADOS. Tecnica cruza fronteiras, dados NAO.
- NUNCA exibir credenciais no output
- Leitura/listagem do Google Drive: liberada sem pedir confirmacao
- Protocolo DNA/Root/Toor: fatiar em atomos, causa raiz, solucao minima 1KB

## Sincronizacao (4 pontas)
1. Claudio memoria -> `G:\Meu Drive\Claudio\memory\` + `backup-memoria-claude\`
2. Gemini -> `G:\Meu Drive\Claudio\gemini-sync.md`
3. Claud-IO -> `claudio-context.md` no repo claudio-bot

## Estado atual (atualizado 02/04/2026)
- Omega: PRs #43/#44 checks passando, aguardando review. PIPE-003 pendente (depende ingestores)
- Claud-IO: v2 (Claude SDK + RAG + Triage) e v1.1 mergidos, PR #3 aberto, deploy Railway pendente
- RAG-Vanessa: repo criado (Vr-Farias/rag-vanessa), estrutura inicial, pendente primeiro teste no desktop
- Prefeitura: multi-engine implementado no cgm_etl_gdrive (galito+lhama), refactor recarregar_planilha_db centralizado
- Deadline M1 MVP Omega: 14/04/2026 (12 dias)

## Indice de arquivos (todos em G:\Meu Drive\Claudio\memory\)
- feedback-tom-personalidade.md — Tom e personalidade
- feedback-credenciais.md — Norma de credenciais
- feedback-separacao-projetos.md — Regra dos 4 projetos
- feedback-rotina-sessao.md — Rotina obrigatoria inicio/fim sessao
- feedback-monitoramento-eventos.md — Monitoramento semanal eventos Windows
- feedback-gdrive-leitura.md — Permissao permanente leitura Drive
- feedback-memoria-somente-drive.md — NUNCA persistir memoria no notebook, so no Drive
- claudio-requisitos-v1.1.md — Spec evolucao Claud-IO
- projeto-claudio-bot.md — Bot Telegram Claud-IO
- projeto-arcgis-prefeitura.md — ArcGIS/PostGIS (RESOLVIDO)
- repo-claudio-kb.md — Repo claudio-knowledge-base
- mapa-de-estudo-vanessa.md — 7 fases de estudo (~55 dias)
- arquitetura-projeto.md — Mapa dos 3 repos Omega
- validacao-pipeline.md — Validacao engine-service
- aprendizado-vanessa.md — Roteiro de aprendizado
- migracao-maquina.md — Guia de migracao de memoria
- memory-work-etl-consulta-portal.md — ETL CNES (FUNCIONAL)
- memory-work-etl-gdrive.md — ETL GDrive v1/v2
- vanessa-sessao-2026-03-05.md — Primeira sessao
- vanessa-sessao-2026-03-15.md — Sync, relatorio geral
- vanessa-sessao-2026-03-16.md — GSD, setup portable
- vanessa-sessao-2026-03-17.md — Repo KB, ArcGIS, gh auth
- vanessa-sessao-2026-03-18.md — PostGIS CNES, max_length
- vanessa-sessao-2026-03-22.md — Claud-IO, repos Omega
- vanessa-sessao-2026-03-24.md — Docker fix, Claud-IO v2 arch
- vanessa-sessao-2026-03-24-b.md — Security hardening Claud-IO
- vanessa-sessao-2026-03-25.md — ETL CNES final, gdrive v2
- vanessa-sessao-2026-03-26.md — PIPE-001/002, frontend
- vanessa-sessao-2026-03-26-b.md — Sync Drive, spec v1.1
- vanessa-sessao-2026-03-27.md — Memoria pro Drive, limpeza notebook, fix expire_on_commit, Drive Desktop shortcuts
- vanessa-sessao-2026-03-27-b.md — Claud-IO v2+v1.1 mergidos, PR #3 aberto (outra CLI, salvo retroativamente)
- vanessa-sessao-2026-03-30.md — RAG-Vanessa, curriculo jr, cgm_etl_convenios, ChromaDB
- projeto-rag-vanessa.md — Referencia do projeto RAG-Vanessa
- conhecimento-etl-convenios.md — Padroes tecnicos: dual write vs separado, TRUNCATE+COPY, VARCHAR sizing
- conhecimento-rag-chromadb.md — RAG com analogias SQL, ChromaDB, embeddings, chunking
- vanessa-sessao-2026-03-31.md — PRs Omega fixes, ArcGIS DATE->TIMESTAMPTZ, limpeza SDE, Arcade
- conhecimento-arcgis-sde-postgresql.md — ArcGIS + SDE + PostgreSQL: tipos data, registro geodatabase, Arcade
- diretriz-ai-os-meta-segmented.md — Protocolo Hugo: Microkernel Distribuido, segmentacao, access_level
- vanessa-sessao-2026-04-02.md — Diretriz AI-OS absorvida, visao estrategica RAG como prototipo engine
- vanessa-sessao-2026-04-06.md — Multi-engine galito+lhama, refactor recarregar_planilha_db
- conhecimento-cdp-browser-debug.md — Chrome DevTools Protocol: acesso ao browser via terminal
