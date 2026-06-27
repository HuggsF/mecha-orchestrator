# MECHA Event Bus — protocolo de intercomunicação (front ⇄ back)

> Como os micro-frontends da MECHA IDE conversam entre si **hoje** (event bus no shell)
> e como o **backend (Antigravity)** deve falar o **mesmo protocolo** para que front e
> back se intercomuniquem. Este é o contrato. Topics e payloads são a fonte de verdade.

## 1. Arquitetura atual (frontend)

```
                 ┌─────────────── MECHA IDE (shell) ───────────────┐
                 │  estado global + EVENT BUS (pub/sub)             │
                 │  emitBus(topic,payload) · onBus(topic,fn)        │
                 └───┬───────┬───────┬────────┬────────┬────────────┘
        vm.bus ↓     │       │       │        │        │   ↑ liveLogs (event stream)
        ┌────────────┴┐ ┌────┴─────┐ ┌┴───────┴┐ ┌────┴─────┐ ┌┴──────────────┐
        │ MechaGraph  │ │MechaCham.│ │MechaClaw│ │MechaInfra│ │ MechaTerminal │
        │ (grafo)     │ │(chamados)│ │ (claw)  │ │ (infra)  │ │ (event stream)│
        └─────────────┘ └──────────┘ └─────────┘ └──────────┘ └───────────────┘
```

- O **shell** é o broker: detém `emitBus`/`onBus` e injeta `vm.bus = { emit, on }` em cada micro-frontend.
- Qualquer FE **publica** (`bus.emit('topic', payload)`) e qualquer FE/serviço **assina** (`bus.on('topic', fn)`).
- Toda emissão também entra no **event stream** (aba *Log de Eventos* do `MechaTerminal`) — a comunicação é observável.
- Exemplo já implementado de FE→FE: `claw.firewall` (MechaClaw) → assinante cria chamado → `ticket.create` aparece em **MechaChamados** e no stream.

## 2. Catálogo de eventos (CONTRATO)

| topic | emissor (FE) | consumidores | payload |
|---|---|---|---|
| `nav.open` | Graph | Explorer, Terminal | `{ fileId, source, node }` |
| `node.select` | Graph | (sidebar detalhe), Terminal | `{ id }` |
| `ticket.advance` | Chamados | Terminal, (backend) | `{ proto, to? }` |
| `ticket.create` | Claw/sistema | Chamados, Terminal | `{ proto, title, source }` |
| `claw.step` | Claw | Terminal, (dashboard) | `{ runId, phase:'see'|'think'|'act', target, cycle }` |
| `claw.firewall` | Claw | Chamados, Terminal | `{ decision:'allow'|'block', reason }` |
| `agent.run` | Agents/LEGION | Terminal, MissionControl | `{ runId, phase:'start'|'review'|'done', mode, model }` |
| `infra.ping` | Infra | Terminal | `{ service, state, port }` |
| `model.change` | Agents | Terminal, status bar | `{ model }` |

> Convenção: `dominio.acao`. Payload é JSON plano e serializável. Toda mensagem ganha
> `ts` (epoch ms) e `id` (uuid) ao cruzar a fronteira de rede (ver §3).

## 3. Mapa front ⇄ back (o que o Antigravity implementa)

O backend deve expor um **WebSocket** (`/ws/bus`) que espelha o mesmo barramento, e
endpoints REST para ações que mutam estado. Regra: **o front é otimista e observável; o
back é a fonte de verdade**. Cada topic do front mapeia para 1 canal/endpoint:

| topic (front) | direção | canal/endpoint backend (Antigravity) |
|---|---|---|
| `claw.step` | back → front | WS push de `execution/claw_loop` (lê `claw_status.json`) |
| `claw.firewall` | back → front | WS push do firewall cognitivo (Ollama) |
| `ticket.create` | front → back → front | `POST /api/tickets` (FreeScout) → WS broadcast |
| `ticket.advance` | front → back → front | `PATCH /api/tickets/{proto}` → WS broadcast |
| `nav.open` | front-only | (sem back; navegação local) |
| `agent.run` | front → back → front | `POST /api/runs` + WS stream de tool-calls/status |
| `infra.ping` | front → back | `GET /api/health` por serviço (Control :8585) |
| `model.change` | front → back | `POST /api/runs/{id}/model` (OpenRouter) |

**Envelope de rede (WS e REST body):**
```json
{ "id": "uuid", "topic": "claw.step", "ts": 1718900000000,
  "actor": "claw_loop", "payload": { "phase": "act", "target": "click", "cycle": 7 } }
```

**Handshake/sessão:** front conecta `/ws/bus`, envia `{topic:"hello",payload:{operator,session}}`;
back responde `{topic:"sync",payload:{tickets,services,runs}}` para hidratar o estado inicial
(substitui os mocks do front).

## 4. Garantias

- **Idempotência:** `ticket.create` com mesma `source+reason` em < 60s não duplica (dedupe por chave).
- **Ordenação:** por `ts`; o front reconcilia por `id`.
- **Degradado:** sem WS, o front cai para o modo demo atual (mocks) — nada quebra.
- **Segurança:** WS exige token de sessão; `agent.run` e `ticket.*` validam HMAC (mesma
  política fail-closed da Amanda API). Segredos nunca trafegam no payload.

## 5. Onde está no código (front)

- `emitBus` / `onBus` / `busApi` / `TOPIC_META` — classe `Component` do shell (`MECHA IDE.dc.html`).
- Emissões: `openNodeFile` (nav.open), `selectNode` (node.select), `advanceTicket`
  (ticket.advance), loop do Claw (claw.step/firewall), assinante firewall→`ticket.create`,
  `send` (agent.run), `pingService` (infra.ping), `setModel` (model.change).
- Consumo visível: `liveLogs` → aba *Log de Eventos* (`MechaTerminal`).
- Cada `vm` recebe `bus` para emitir/assinar direto do micro-frontend.
