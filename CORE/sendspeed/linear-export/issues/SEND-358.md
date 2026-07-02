# SEND-358 — 🚀 - Atualização imediata de dados do usuário via Webhook

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | No priority |
| Responsável | Vinicius Carneiro |
| Time | Sendspeed |
| Projeto | — |
| Labels | UserIn, Implementação, User Story |
| Parent | — |
| Criada | 2026-03-02T18:43:13.890Z por Vinicius Carneiro |
| Iniciada | 2026-03-03T12:12:18.871Z |
| Concluída | 2026-03-25T13:32:05.398Z |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-358--atualizacao-imediata-de-dados-do-usuario-via-webhook |
| URL | https://linear.app/sendspeed/issue/SEND-358/atualizacao-imediata-de-dados-do-usuario-via-webhook |

## Descrição

> **Como** Product Owner da plataforma,
> **Quero** que eventos recebidos via webhook (depósito e registro) atualizem os dados do usuário imediatamente,
> **Para** que comunicações insite e offsite sejam ativadas em tempo real, sem depender do delay de 1 minuto atual.

---

# 📈 Use Case:

O usuário realiza um depósito ou registro na plataforma do cliente. O sistema externo envia um webhook com os dados do evento (tipo, valor, identificação do usuário). O backend valida a API Key, persiste os dados imediatamente e publica o evento via Redis Pub/Sub. O frontend recebe a atualização via SSE (Server-Sent Events) e, caso a conexão SSE não esteja ativa, continua funcionando via polling existente.

# ✅ Critérios de aceite:

* Endpoint de webhook valida API Key e rejeita requests não autenticados (HTTP 401).
* Dados do usuário são atualizados no banco imediatamente ao receber evento válido.
* Eventos duplicados (mesmo event ID) são ignorados.
* Evento é publicado via Redis Pub/Sub após persistência.
* Frontend conectado via SSE recebe o evento em tempo real.
* Polling HTTP existente continua funcionando como fallback.

# 🧩 Cenários de teste:

- [ ] Enviar webhook com API Key válida → dados persistidos e evento entregue via SSE.
- [ ] Enviar webhook com API Key inválida → retorno 401, nenhum dado alterado.
- [ ] Enviar webhook sem API Key → retorno 401.
- [ ] Enviar mesmo evento duas vezes (mesmo event ID) → segundo é ignorado, dados não duplicados.
- [ ] Enviar webhook com usuário conectado via SSE → frontend recebe atualização em tempo real.
- [ ] Enviar webhook com usuário sem conexão SSE ativa → dados persistidos, disponíveis via polling.
- [ ] Enviar webhook com payload incompleto (campos obrigatórios ausentes) → retorno 400.

---

> **⚠️ Riscos conhecidos (não bloqueantes):**
> **R1 — API Key simples:** vulnerável a replay attacks. Futuro: migrar para HMAC signature.
> **R2 — Múltiplas instâncias:** webhook pode chegar em instância diferente da conexão SSE. Validar comportamento do Redis Pub/Sub em ambiente multi-instância.
> **R3 — Desconexão SSE:** eventos emitidos durante janela de desconexão podem ser perdidos. Futuro: implementar `Last-Event-ID` para replay.
> **R4 — Rajada de webhooks:** pico de eventos pode sobrecarregar o banco com processamento síncrono. Futuro: avaliar Kafka (já existente) como buffer.
> **R5 — Falha sem retry:** se o processamento falhar (ex: banco indisponível), o evento é perdido. Futuro: implementar dead letter queue com retry automático.

## Histórico de status
- Backlog (backlog): 2026-03-02T18:43:13.890Z → 2026-03-02T18:54:41.708Z
- To-do (unstarted): 2026-03-02T18:54:41.708Z → 2026-03-03T12:12:18.885Z
- In Progress (started): 2026-03-03T12:12:18.885Z → 2026-03-05T18:37:02.212Z
- Product Review (started): 2026-03-05T18:37:02.212Z → 2026-03-25T13:32:05.412Z
- Released (completed): 2026-03-25T13:32:05.412Z → atual

## Relações
—

## Anexos
—
