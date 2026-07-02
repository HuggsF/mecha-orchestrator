# SEND-23 — Buffer Manager (Behavior Agent)

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | Urgent |
| Responsável | — |
| Time | Sendspeed |
| Projeto | — |
| Labels | Behavior |
| Parent | — |
| Criada | 2025-06-10T18:12:21.048Z por pedro.antunes@sendspeed.com |
| Iniciada | — |
| Concluída | 2025-07-10T12:18:39.183Z |
| Arquivada | 2026-01-18T02:05:01.759Z |
| Vencimento | — |
| Branch | hugofernandes/send-23-buffer-manager-behavior-agent |
| URL | https://linear.app/sendspeed/issue/SEND-23/buffer-manager-behavior-agent |

## Descrição

**Como** *Buffer Manager*
**Quero** decidir **sozinho** - com base na configuração obtida via **getConfig** (por *company*) - **se** e **quando** enviar um lote de eventos para o **Behavior Agent analisar****
****Para** otimizar o custo de processamento da IA e respeitar regras específicas de cada cliente.

## Regras-chave ("Janela de Tempo + Mínimo")

| Símbolo | Regra | Default (mock) |
| -- | -- | -- |
| 🕐 | **Janela**: períodos fixos de tempo (ex.: 30 s) | `windowMs = 30000` |
| 📊 | **Mínimo**: só dispara se atingir *N* eventos dentro da janela | `minEvents = 3` |
| 📦 | **Acúmulo**: eventos que não fecharam o mínimo "rolam" para a próxima janela | — |
| ⚡ | **Críticos**: tipos listados em `criticalEvents` ignoram janela e disparam instantaneamente | `["mouse_leave","tab_switch_attempt","page_blur"]` |
| 🛡️ | **Buffer Máx.**: evita overflow; ao atingir, força envio mesmo sem requisitos | `bufferMax = 50` |

> **Exemplo** (`minEvents = 3`, `window = 30 s`)
> • 0-30 s: 2 eventos → ❌ **NÃO** processa; acumula
> • 30-60 s: +4 eventos → ✅ **SIM** processa 6 eventos (2 + 4)

---

### 🎯 Critérios de Aceitação (Gherkin revisado)

| \# | Cenário | Dado | Quando | Então |
| -- | -- | -- | -- | -- |
| 1 | **getConfig por company** | que o Buffer Manager receba `companyId` no 1.º evento | init | chama `GET /config/:companyId` e carrega parâmetros; se falhar, usa *defaults* |
| 2 | **Contagem por janela** | que `windowMs` seja 30 000 | chegam eventos dentro do tempo | apenas **contabiliza** até `minEvents`; não envia ainda |
| 3 | **Disparo por mínimo** | que `eventsInWindow == minEvents` | ainda dentro da janela | **envia** lote completo ao Behavior Agent e zera contagem para nova janela |
| 4 | **Rolagem de eventos** | que a janela expire com `< minEvents` | timer atinge `windowMs` | mantém eventos acumulados e inicia novo relógio |
| 5 | **Evento crítico** | que o tipo do evento ∈ `criticalEvents` | evento recebido | **envia imediatamente** ao Behavior Agent, sem esperar janela |
| 6 | **Buffer máximo** | que `totalBuffered ≥ bufferMax` | antes de inserir novo evento | força envio de **todos** os eventos e zera buffer (regra de segurança) |
| 7 | **Config mutável** | — | Buffer recebe `configUpdated` webhook | atualiza parâmetros em runtime sem reiniciar serviço |
| 8 | **Observabilidade** | — | a cada envio | registra métrica `buffer_send_reason` = `MIN`, `CRITICAL`, `MAX`, `MANUAL` |

---

### 🛠 Detalhes de Implementação

| Área | Descrição |
| -- | -- |
| **getConfig** | Endpoint (mock) devolve JSON<br/>`json { "companyId": "acme", "minEvents": 3, "windowMs": 30000, "bufferMax": 50, "criticalEvents": ["mouse_leave", "tab_switch_attempt", "page_blur"] }` |
| **Timer** | Um `setInterval(windowMs)` ou job de cron interno reinicia janela e verifica rolagem. |
| **Feature Flag** | `CONFIG_FROM_DB=true` ativa busca real; `false` usa defaults codificados (estado atual) |
|  |  |

\*Deve haver um simulador de eventos na demo independente do tracker acoplado tb.

## Histórico de status

- Backlog (backlog): 2025-06-10T18:12:21.048Z → 2025-06-10T18:50:12.899Z
- To-do (unstarted): 2025-06-10T18:50:12.899Z → 2025-07-10T12:18:39.167Z
- Released (completed): 2025-07-10T12:18:39.167Z → atual

## Relações

—

## Anexos

—
