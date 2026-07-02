# GEMINI.md — Regras globais MECHA ⊕ Omega (Antigravity / Gemini)

> Cole o conteúdo deste arquivo em `~/.gemini/GEMINI.md` (rules global do Antigravity e do Gemini CLI). Vale para TODA sessão, em todo projeto.

## 0. Identidade & modelo
Você opera sob a governança **MECHA**. Use **Gemini 3.1 em `thinking_level=LOW`** para o trabalho de rotina; escale para Claude apenas em tarefas robustas. Mantenha o bloco de tools enxuto e **prompt-cacheado** (prefixo estável).

## 1. Lei 2 — RAG-first (inviolável)
O conhecimento vive no **Gêmeo Digital (Neo4j)** e nas notas — nunca escondido em config. Ao concluir qualquer trabalho relevante (tool, skill, doc, decisão, descoberta), **INGIRA no Neo4j**:
`python .mecha/ops/daemons/ingest_session.py`
(additivo e idempotente). Conhecimento que não está no grafo não existe.

## 2. Gêmeo Digital — saúde antes de agir
Antes de alterar código que dependa da arquitetura, **consulte o grafo**. Cheque `.mecha/ops/daemons/.state/digital_twin.status.json`: se `verdict.status = ALERT` (grafo zerado), **pare e corrija** antes de prosseguir. Causa provável: o twin real `mecha_ontology_graph` está **parado** com volume nomeado → `docker start mecha_ontology_graph` (**NÃO re-ingerir**; os dados estão intactos no volume).

## 3. Ferramentas — enxuto por padrão
Prefira o **MechaShell** (6 primitivas: `run/read/write/edit/ls/find`) a servidores pesados como o Desktop Commander. Faça admin de processo/arquivo **no shell via `run`** (`ps`/`kill`/`mv`/`mkdir`). **Bound toda leitura** (`head`/`tail`); use `edit` (diff) em vez de reescrever o arquivo inteiro.

## 4. Skills (quando usar)
- **host-bridge-diagnostics** — inspecionar infra do host (Docker/Neo4j/Qdrant) inalcançável do sandbox; **enumere TODOS os candidatos** antes de cravar um; grafo vazio tem 3 causas (sem volume / dados em container parado / ingestão nunca rodou); read-only.
- **daemonize** — transformar um agendamento em daemon resiliente (lockfile single-instance, fail-closed, backoff, heartbeat).
- **mecha-shell** — terminal + arquivos enxuto.

## 5. Contratos & validação
Tipagem estrita (**Pydantic**) em toda entrada/saída. Planos e docs com hierarquia **H1→H2→H3** (sem saltos) e frontmatter **`emoji_rail`**. Valide antes de mergear.

## 6. Clean-room (inviolável)
O `rag-dojo` é **clean-room**: somente dados públicos open-source. **Nunca** ingira dado privado/da org nele. Dado real vive no twin canônico. A fronteira é de sentido único: o dojo exporta contrato/componente, não importa dado.

## 7. Segurança & resiliência
Read-only por padrão em infra. **Nada destrutivo** (`rm`, `DROP`, `DELETE`, `docker rm/down/stop`) sem confirmação explícita do usuário no mesmo turno. **Secure Default State (Fail-closed)**, **Ephemeral Asset Pruning (kill-lixo)** (sem temporários órfãos).

## 8. GitOps
Cada squad em branch própria (`squad/<dominio>/<feature>`); commits atômicos em Conventional Commits; identifique-se antes de commitar; consulta determinística ao RAG **antes** de alterar código (não adivinhe — recupere a verdade do grafo).
