# SEND-381 — 🚀 - Jornada E2E: Webhook → Trigger → Condição → Disparo SMS (via Gatilho Webhook, sem registro)

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | Urgent |
| Responsável | Vinicius Carneiro |
| Time | Sendspeed |
| Projeto | — |
| Labels | User Story, Jornadas, UserIn |
| Parent | — |
| Criada | 2026-03-13T12:35:59.876Z por Vinicius Carneiro |
| Iniciada | 2026-03-25T13:39:39.803Z |
| Concluída | 2026-04-01T12:10:36.646Z |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-381--jornada-e2e-webhook-trigger-condicao-disparo-sms-via |
| URL | https://linear.app/sendspeed/issue/SEND-381/jornada-e2e-webhook-trigger-condicao-disparo-sms-via |

## Descrição

> **Como** gestor de CRM de uma operadora de iGaming
> **Quero** que quando qualquer evento chegar via webhook, uma jornada automatizada seja disparada de ponta a ponta — avaliando condições e enviando um SMS personalizado ao final, sem depender de um fluxo de registro/cadastro
> **Para** que a comunicação com o jogador seja imediata e flexível, acionada por qualquer gatilho externo via webhook (depósito, aposta, inatividade, etc.), sem intervenção manual e sem necessidade de cadastro prévio no sistema

---

# 📈 Use Case: Disparo de SMS via webhook genérico sem necessidade de registro

A operadora ApostaTudo integrou seu sistema ao Userin via webhook. O fluxo end-to-end funciona **sem exigir evento de registro** — o disparo é acionado diretamente pelo gatilho do webhook:

1. **Webhook recebido**: POST /api/webhooks/cactus com evento arbitrário (ex: `first_deposit`, `bet_placed`, `inactive_7d`), contendo dados do jogador (user_id, user_phone, etc.)
2. **Autenticação e idempotência**: Middleware valida ApiKey e previne duplicatas
3. **Processamento OffSite**: JourneyOffsiteProcessor.processUser() busca profile no segment-engine usando o identificador do webhook (externalId/userId)
4. **Avaliação de jornadas**: Encontra jornadas ativas cujo trigger corresponde ao evento recebido no webhook → avalia condições do fluxo
5. **Execução do SendSms**: Resolve variáveis Liquid, busca credencial e envia SMS personalizado
6. **Touchpoint com Last Touch**: Registra Touchpoint com canal SMS, journeyId e janela de atribuição. O modelo **Last Touch** garante que a conversão seja atribuída ao último ponto de contato antes da ação de valor.

**Resultado**: O jogador recebe o SMS segundos após o evento do webhook, sem que tenha sido necessário um fluxo de cadastro/registro no Userin. O gatilho do webhook é suficiente para acionar toda a jornada.

---

# 🔑 Premissa principal

O disparo da jornada **não depende de registro** do usuário na plataforma. O webhook funciona como gatilho direto:

* O payload do webhook traz os dados necessários (telefone, nome, identificador externo)
* Se o perfil já existe no segment-engine, é enriquecido; se não existe, é criado on-the-fly a partir dos dados do webhook
* A jornada é avaliada e executada com base no evento do webhook, não em um evento de cadastro

---

# ✅ Critérios de aceite:

### Webhook (Entrada)

* Webhook recebe evento via POST com dados do jogador (não restrito a `register`)
* ApiKey validada pelo webhookAuthMiddleware
* Idempotência previne processamento duplicado
* Payload do webhook contém dados suficientes para disparo (telefone, identificador)

### Journey Engine (Processamento)

* JourneyOffsiteProcessor.processUser() invocado com companyId e identificador do webhook
* Profile buscado ou criado on-the-fly no segment-engine com dados do webhook
* Jornadas ativas cujo trigger.event corresponde ao evento do webhook são identificadas
* EventTriggerExecutor avalia match e retorna shouldTrigger: true
* Condições do fluxo avaliadas antes da ação
* **Nenhuma dependência de evento de registro prévio**

### SendSms + Atribuição (Saída)

* SendSmsExecutor busca credencial, resolve variáveis e envia SMS
* Touchpoint registrado com channel: sms, journeyId, nodeId e expiresAt
* Modelo Last Touch aplicado: 100% do crédito ao último touchpoint
* Confidence score calculado com base no tempo entre envio e conversão
* AttributionService.processConversion() atribui hook ao touchpoint correto

---

# 🧩 Cenários de teste:

- [ ] POST /api/webhooks/cactus com evento genérico (ex: `first_deposit`) — jornada E2E executa e SMS é enviado **sem registro prévio**
- [ ] Webhook com evento `bet_placed` para jogador já existente — jornada dispara com dados do profile existente
- [ ] Webhook com evento para jogador novo (sem profile) — profile criado on-the-fly e SMS enviado
- [ ] Mesmo payload duas vezes — segundo rejeitado por idempotência
- [ ] Webhook com ApiKey inválida — retorna 401
- [ ] Verificar Touchpoint criado com channel: sms e attributionWindowHours configurável
- [ ] Simular conversão em <1h — atribuída com confidence 0.85 e model: last_touch
- [ ] Simular conversão em >72h — não atribuída (touchpoint expirado)
- [ ] Simular dois touchpoints (SMS + email) — Last Touch atribui 100% ao mais recente
- [ ] Webhook com payload sem telefone — jornada executa, SMS falha com NO_PHONE
- [ ] Segment-engine offline — processamento falha com erro logado
- [ ] API integrações offline — SMS falha mas webhook retorna 200
- [ ] Webhook com evento que não tem jornada associada — processamento ocorre mas nenhuma ação é executada

## Histórico de status
- Backlog (backlog): 2026-03-13T12:35:59.876Z → 2026-03-13T14:59:51.037Z
- To-do (unstarted): 2026-03-13T14:59:51.037Z → 2026-03-25T13:39:39.813Z
- In Progress (started): 2026-03-25T13:39:39.813Z → 2026-03-26T16:42:20.774Z
- Product Review (started): 2026-03-26T16:42:20.774Z → 2026-03-31T18:24:55.547Z
- Release (started): 2026-03-31T18:24:55.547Z → 2026-04-01T12:10:36.662Z
- Released (completed): 2026-04-01T12:10:36.662Z → atual

## Relações
—

## Anexos
—
