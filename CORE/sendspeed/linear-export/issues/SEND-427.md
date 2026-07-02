# SEND-427 — 🚀 - E2E: Smartico Inbound Webhook → Gatilho Externo → Disparo de Jornada (sem registro)

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | Urgent |
| Responsável | Vinicius Carneiro |
| Time | Sendspeed |
| Projeto | — |
| Labels | User Story, Jornadas, UserIn |
| Parent | — |
| Criada | 2026-03-25T18:40:07.254Z por Vinicius Carneiro |
| Iniciada | 2026-03-26T12:44:27.249Z |
| Concluída | 2026-04-01T12:10:31.129Z |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-427--e2e-smartico-inbound-webhook-gatilho-externo-disparo-de |
| URL | https://linear.app/sendspeed/issue/SEND-427/e2e-smartico-inbound-webhook-gatilho-externo-disparo-de-jornada-sem |

## Descrição

> **Como** gestor de CRM de uma operadora de iGaming
> **Quero** que quando a Smartico enviar um payload via webhook inbound externo contendo nome, número e CID do jogador, a jornada vinculada a esse gatilho seja disparada automaticamente
> **Para** que a comunicação com o jogador seja acionada diretamente pela Smartico, sem necessidade de cadastro prévio no Userin, permitindo disparos de SMS/mensagens em tempo real baseados em eventos do CRM externo

---

# 📈 Use Case: Smartico envia webhook → Jornada dispara SMS 

A operadora integra seu CRM Smartico ao Userin via gatilho inbound externo. O fluxo:

1. **Smartico envia webhook**: POST no endpoint inbound do Userin com payload contendo `nome`, `numero` (telefone).
2. **Autenticação**: ApiKey validada pelo middleware de autenticação de webhooks
3. **Extração de dados**: Sistema extrai `nome`, `numero` do payload.
4. **Disparo da jornada**: `JourneyOffsiteProcessor.processUser()` é chamado com `companyId` e `event` correspondente ao gatilho configurado na jornada
5. **Match do gatilho**: Journey Engine identifica jornadas ativas cujo trigger corresponde ao evento do webhook Smartico
6. **Execução da ação**: SMS/mensagem enviado usando os dados do profile (nome, telefone do payload)
7. **Touchpoint registrado**: Canal, journeyId e janela de atribuição registrados para Last Touch

**Resultado**: Jogador recebe SMS segundos após a Smartico disparar o webhook. Nenhum registro prévio no Userin é necessário — o payload do webhook é suficiente.

---

# 🔑 Payload esperado da Smartico

```json
{
  "nome": "Carlos Silva",
  "numero": "+5511987654321"
}
```

| Campo | Tipo | Obrigatório | Descrição |
| -- | -- | -- | -- |
| `nome` | string | Sim | Nome do jogador (usado em templates Liquid como `{{contact.nome}}`) |
| `numero` | string | Sim | Telefone do jogador no formato E.164 (destino do SMS) |
|  |  |  |  |

---

# 🛠️ Fluxo técnico detalhado

### 1\. Recebimento do webhook

* Endpoint: `POST /api/webhooks/cactus` (com `source: smartico`) **ou** novo endpoint dedicado `POST /api/webhooks/smartico`
* Middleware: `webhookAuthMiddleware` valida ApiKey da Smartico
* Middleware: `idempotencyMiddleware` previne duplicatas

### 2\. Processamento do payload

* Extrair `nome`, `numero` do body
* Mapear: `nome` → `metadata.name`, `numero` → `metadata.phone`
* Persistir hook via `userInHookService.upsertRegister()` com `source: 'smartico'` e `type` baseado no evento

### 3\. Disparo da jornada (conexão que hoje não existe)

* **Após** persistir o hook, chamar `journeyOffsiteProcessor.processUser(companyId, null, eventType)`
* Isso conecta o webhook recebido diretamente ao Journey Engine OffSite
* Hoje o controller Cactus **não** chama `processUser` — essa é a implementação principal deste card

### 4\. Profile no Segment Engine

* Se profile já existe para : enriquece com dados do payload
* Se não existe: cria on-the-fly com `{ name: nome, phone: numero }`
* Profile disponibilizado para resolução de variáveis Liquid na jornada

### 5\. Execução do SMS

* `SendSmsExecutor` (não o stub `executeSendSms`) resolve variáveis, busca credencial e envia
* Touchpoint registrado com `channel: sms`, `journeyId`, `nodeId`

---

# ✅ Critérios de aceite:

### Webhook Smartico (Entrada)

- [ ] Endpoint recebe POST com payload `{ nome, numero}` e `source: smartico`
- [ ] ApiKey da Smartico validada pelo middleware
- [ ] Idempotência previne processamento duplicado do mesmo evento
- [ ] Hook persistido com `source: 'smartico'` e metadata contendo nome/numero/cid

### Journey Engine (Processamento)

- [ ] `journeyOffsiteProcessor.processUser()` chamado automaticamente após recebimento do webhook (sem necessidade de chamada manual ao `/offsite/trigger`)
- [ ] Profile buscado ou criado on-the-fly no Segment Engine usando `cid` como `externalId`
- [ ] Jornadas ativas com gatilho correspondente ao evento Smartico são identificadas e executadas
- [ ] **Nenhuma dependência de evento de registro prévio** — o webhook é o gatilho direto

### Disparo (Saída)

- [ ] SMS enviado via `SendSmsExecutor` real (não o stub simulado)
- [ ] Variáveis Liquid resolvidas com dados do payload (`{{contact.nome}}`, `{{contact.numero}}`)
- [ ] Touchpoint registrado com canal correto e janela de atribuição

---

# 🧩 Cenários de teste:

- [ ] POST webhook com payload `{ nome, numero}` e source smartico → jornada dispara e SMS é enviado
- [ ] Webhook Smartico com jogador já existente no Segment Engine → profile enriquecido, jornada dispara
- [ ] Webhook Smartico com jogador novo → profile criado on-the-fly, SMS enviado com dados do payload
- [ ] Mesmo payload enviado duas vezes → segundo rejeitado por idempotência
- [ ] Webhook com ApiKey inválida → retorna 401
- [ ] Webhook sem campo `numero` → jornada executa, SMS falha com NO_PHONE
- [ ] Segment Engine offline → erro logado, webhook retorna 200 (não bloqueia)
- [ ] API integrações SMS offline → SMS falha mas hook é persistido
- [ ] Verificar Touchpoint criado com `channel: sms` e `source: smartico`

---

# ⚠️ Gaps técnicos identificados (implementação necessária)

1. **Conexão webhook → Journey Engine**: Hoje o controller Cactus persiste o hook mas **não** chama `processUser()`. Esse é o principal trabalho deste card.
2. **Profile on-the-fly**: Garantir que o Segment Engine aceita criação de profile com dados mínimos (nome + telefone)
3. **SendSmsExecutor real**: O executor OffSite de SMS (`executeSendSms`) é um stub. Usar o `SendSmsExecutor` real ou integrar com o serviço de SMS.
4. **Mapeamento de campos**: `nome` → `contact.name`/`contact.firstName`, `numero` → `contact.phone`

## Histórico de status
- Backlog (backlog): 2026-03-25T18:40:07.254Z → 2026-03-25T19:26:43.182Z
- To-do (unstarted): 2026-03-25T19:26:43.182Z → 2026-03-26T12:44:27.257Z
- In Progress (started): 2026-03-26T12:44:27.257Z → 2026-03-26T17:35:59.189Z
- Product Review (started): 2026-03-26T17:35:59.189Z → 2026-03-30T14:46:41.604Z
- Done (started): 2026-03-30T14:46:41.604Z → 2026-03-31T18:25:02.729Z
- Release (started): 2026-03-31T18:25:02.729Z → 2026-04-01T12:10:31.155Z
- Released (completed): 2026-04-01T12:10:31.155Z → atual

## Relações
—

## Anexos
—
