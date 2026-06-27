# Antigravity Bridge — prompt + tasks (front ⇄ back)

> **Entregável.** Cole o bloco abaixo no Antigravity como tarefa do agente. Ele analisa
> o frontend (MECHA IDE + micro-frontends) e implementa o **backend que fala o MECHA
> Event Bus** (`docs/EVENT_BUS.md`), substituindo os mocks por dados reais — sem quebrar
> o que já roda. Referências: `docs/EVENT_BUS.md`, `docs/MICROFRONTENDS.md`,
> `.mecha/design/SYSTEM_DESIGN_INICIAL.md`, `docs/FASE_3_RAG.md`.

---

```
# Tarefa: Implementar a Ponte Front⇄Back do MECHA Workbench (Event Bus)
#         Mecha Huggs Workforce Studio — fase de interface (6) + cola das fases 2/3/5

## Contexto
O frontend é a MECHA IDE, composta por um SHELL + micro-frontends (Graph, Chamados,
Claw, Infra, Terminal) que se comunicam por um EVENT BUS pub/sub. O contrato de eventos
(topics, payloads, mapa front⇄back, envelope de rede, handshake) está em docs/EVENT_BUS.md
— é a FONTE DE VERDADE. Hoje o front roda com dados mockados; seu trabalho é implementar
o backend que fala o MESMO protocolo e hidrata/atualiza o front via WebSocket + REST.
O MECHA segue EM PRODUÇÃO; migração incremental, cada fase com rollback.

## Decisões ratificadas (invioláveis)
1. O contrato de eventos de docs/EVENT_BUS.md §2/§3 é imutável sem versionar (`v1`).
2. Front é otimista e observável; BACK é a fonte de verdade (reconciliação por id+ts).
3. Busca híbrida = Qdrant (vetor) + Neo4j (grafo) via rag_client único (Fase 3).
4. Escrita ATÔMICA em todo JSON lido pela UI (claw_status.json, claw_preempt.json).
5. Segurança: WS com token de sessão; ticket.*/agent.* com HMAC fail-closed; segredos só no .env.

## Entregáveis
1. bus/  — barramento de eventos do backend:
   - `bus/protocol.py` : Pydantic dos envelopes e de CADA payload de §2 (validação estrita).
   - `bus/server.py`   : WebSocket `/ws/bus` (handshake hello→sync, broadcast, dedupe, ordenação por ts).
2. interface/control_api (:8585) — REST que muta estado e re-emite no bus:
   - `POST /api/runs` + stream de tool-calls/status  → eventos `agent.run`
   - `POST /api/tickets` / `PATCH /api/tickets/{proto}` (FreeScout) → `ticket.create|advance`
   - `GET /api/health` por serviço → `infra.ping`
   - `POST /api/runs/{id}/model` → `model.change`
3. execution/claw_loop → publica `claw.step` e `claw.firewall` no bus (lendo claw_status.json,
   firewall via Ollama). Incidente de firewall dispara `ticket.create` (idempotente <60s).
4. knowledge/rag_client (Qdrant+Neo4j) consumido por `agent.run` (passo rag_client.search).
5. Hidratação: ao `hello`, responder `sync` com {tickets, services, runs} reais (substitui mocks).
6. Testes: contrato (Pydantic) de todos os payloads; integração WS (hello→sync→broadcast);
   e2e de 1 fluxo cruzado (claw.firewall → ticket.create chega ao canal de Chamados); smoke /health.

## Restrições
- Python 3.11, Pydantic v2, asyncio. Sem credencial em log (scrub). Erros 400/401/403/503/500.
- Não tocar na árvore legada de .mecha/ops/patterns além de publicar no bus.
- Degradação graciosa: sem WS o front mantém o modo demo (não regredir).

## Critério de pronto
- `/ws/bus` faz hello→sync e o front troca mocks por dados reais sem refresh.
- Um firewall block no claw_loop cria chamado real no FreeScout e o card aparece em
  MechaChamados via broadcast (fluxo FE↔BE↔FE observável no event stream).
- Todos os payloads validam contra bus/protocol.py; suíte verde; árvore antiga intacta.

Antes de codar, gere o Implementation Plan (arquivos, ordem, pontos de rollback,
versão do contrato) e aguarde meu OK.
```

---

## Task board (para o Antigravity quebrar e executar)

- [ ] **T1 · Protocolo** — `bus/protocol.py`: envelope + Pydantic de cada topic (§2). Testes de contrato.
- [ ] **T2 · WS server** — `/ws/bus`: handshake hello→sync, broadcast, dedupe (id), ordenação (ts), token de sessão.
- [ ] **T3 · Hidratação** — `sync` devolve {tickets, services, runs} reais; front remove mocks no boot.
- [ ] **T4 · Claw publisher** — `claw_loop` emite `claw.step`/`claw.firewall`; firewall→`ticket.create` idempotente.
- [ ] **T5 · Tickets REST** — `POST/PATCH /api/tickets` (FreeScout) → re-emite `ticket.create|advance`.
- [ ] **T6 · Runs/LLM** — `POST /api/runs` + stream de tool-calls → `agent.run`; `model.change` (OpenRouter).
- [ ] **T7 · Infra health** — `GET /api/health` por serviço (Control :8585) → `infra.ping`.
- [ ] **T8 · RAG no run** — passo `rag_client.search` (Qdrant+Neo4j) dentro de `agent.run`.
- [ ] **T9 · Segurança** — token WS, HMAC fail-closed em ticket.*/agent.*, scrub de segredos.
- [ ] **T10 · E2E + rollback** — fluxo cruzado firewall→ticket observável; smoke; plano de rollback por fase.

## Como validar contra o front
1. Suba `/ws/bus`; abra a MECHA IDE → aba **Log de Eventos** do Terminal.
2. Toda ação real do back deve aparecer lá com o mesmo `topic` do contrato.
3. Dispare um firewall no `claw_loop` → um card novo deve surgir em **Chamados** sem refresh.
