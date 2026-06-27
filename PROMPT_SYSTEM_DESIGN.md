# 🎯 Prompt — System Design Inicial (MECHA ⊕ Omega unificados)

> Copie o bloco abaixo para o modelo/arquiteto que fará o System Design. Ele assume que o **alinhamento de backends já foi aprovado** (ver `ALINHAMENTO_MECHA_OMEGA.md`).

---

## PROMPT

**Papel:** Você é um(a) arquiteto(a) de software sênior especializado(a) em sistemas locais-first, agentes de IA e RAG híbrido. Produza o **System Design inicial** da plataforma unificada **MECHA ⊕ Omega** ("Mecha Huggs Workforce Studio" / HWorkforceStudio).

**Contexto (dado, não rediscutir):**
Estamos fundindo dois sistemas existentes:
- **MECHA** — cérebro de execução já funcional: automação de desktop (Claw: RPA + visão + firewall cognitivo + auto-recuperação), squads multi-agente (Tribunal Hermes, CodeSquad, QASquad), bots Telegram/Teams (FastAPI + servidor HTTP de dashboard na porta 8585/8686), RAG em Qdrant, base de conhecimento em Obsidian/`CORE`. Governança forte: contratos Pydantic, validação AST de hierarquia, *emoji rails* semânticos, princípios "Lei 2" (conhecimento no RAG/notas), "kill-lixo", escrita atômica, fail-closed.
- **Omega RAG** — plataforma de dados/produto (hoje só esqueleto): data lake `OmegaData/*`, observabilidade Grafana+Prometheus, frontend Next.js (`omega-frontend`), `omega_sdk`, knowledge graph (`graphify`), honeypots, canal Signal, pipeline de handover/ingestão.

**Decisões de arquitetura já tomadas (trate como requisitos):**
1. Busca **híbrida = Qdrant (vetorial) + Neo4j (grafo)**; ChromaDB descartado. Tudo atrás de uma interface única `rag_client`.
2. **Conhecimento único:** vault Obsidian/`CORE` é a fonte de verdade; `OmegaData/KnowledgeBase` é derivado/índice.
3. **Governança do MECHA** (emoji rails + Pydantic + validação AST + frontmatter) vale para todas as camadas.
4. **Migração incremental** (sem big-bang), camada por camada, com o MECHA em produção.

**Estrutura-alvo (camadas):** kernel (contratos/governança/validadores) → execution (claw/squads/agents) → knowledge (vault + rag) → index (vector Qdrant / graph Neo4j) → data (data lake) → ingestion (handover/graphify/connectors) → observability (prometheus/grafana/telemetry) → interface (studio/sdk/channels) → security (honeypots/decoys/segredos) → ops (build/deploy/runbooks).

**Restrições não-funcionais:**
- Local-first / Windows; empacotável via PyInstaller (cuidado com caminhos `__file__` vs `sys.executable`, hidden-imports).
- Resiliência: degradação graciosa (sem Docker/Qdrant cai para modo local), escrita atômica, fail-closed em webhooks, sem segredos no código (`.env` + .gitignore; rotação de tokens).
- O workspace fica em OneDrive: evitar leituras parciais durante sync.
- Persona/UX: Amanda (Shadow Processor), tom técnico e limpo.

**Entregáveis do System Design (produza todos):**
1. **Visão C4** (Contexto + Containers + Componentes principais) descrita textualmente e em **Mermaid**.
2. **Fluxo de dados ponta a ponta:** ingestão → conhecimento → indexação (Qdrant+Neo4j) → consulta (rag_client) → execução/agents → interface/canais. Diagrama Mermaid.
3. **Contratos de API por camada** (REST/WebSocket): endpoints, métodos, payloads (com modelos Pydantic), códigos de erro. Incluir o contrato do dashboard/Studio (`/api/health`, `/api/status`, `/api/preempt`) e do webhook do Teams.
4. **Modelo de dados:** coleções/índices Qdrant (dimensões, metadados), esquema de grafo Neo4j (nós/arestas: Lead, Flow, Interaction, Document, Chunk…), e taxonomia do data lake.
5. **Stack tecnológica** por camada + justificativa (Python/FastAPI, Next.js, Qdrant, Neo4j, Prometheus/Grafana, etc.).
6. **Topologia de deploy:** processos/portas, contêineres, modo local vs VPS (huggs.tech), fallback sem Docker.
7. **Plano de migração incremental** (ordem das camadas, critérios de pronto, rollback) — alinhado ao `ALINHAMENTO_MECHA_OMEGA.md`.
8. **Observabilidade:** o que vira métrica (telemetria do Claw → Prometheus → Grafana), logs, eventos do dashboard.
9. **Modelo de segurança:** segredos, honeypots/decoys, firewall cognitivo, autenticação dos canais e do Studio, fail-closed.
10. **Estratégia de testes:** unitários (Pydantic/contratos), integração (RAG, IPC do Claw), E2E (Studio↔backend), smoke por camada.
11. **Riscos e decisões em aberto** (com recomendação).
12. **Governança:** como aplicar emoji rails + validação AST + frontmatter aos novos módulos; ownership por camada (ex.: Amanda vs Vanessa).

**Formato de saída:** documento estruturado em Markdown, com diagramas Mermaid, tabelas para contratos/modelos e uma seção final de "decisões e próximos passos". Seja específico e implementável; não repita o contexto — vá direto ao design. Onde houver trade-off, escolha e justifique em 1–2 linhas.

---
*Fim do prompt.*
