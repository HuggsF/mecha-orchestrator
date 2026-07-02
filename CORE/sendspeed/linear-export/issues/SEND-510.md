# SEND-510 — 🧩 Integração com API de Eventos NGX (Event Webhook) — receber e processar 16 eventos de iGaming

| Campo | Valor |
| -- | -- |
| Status | Backlog (backlog) |
| Prioridade | High |
| Responsável | — |
| Time | Sendspeed |
| Projeto | — |
| Labels | — |
| Parent | — |
| Criada | 2026-06-18T22:28:25.309Z por pedro.antunes@sendspeed.com |
| Iniciada | — |
| Concluída | — |
| Arquivada | 2026-06-22T17:17:54.153Z |
| Vencimento | — |
| Branch | hugofernandes/send-510-integracao-com-api-de-eventos-ngx-event-webhook-receber-e |
| URL | https://linear.app/sendspeed/issue/SEND-510/integracao-com-api-de-eventos-ngx-event-webhook-receber-e-processar-16 |

## Descrição

## 🧩 Épico: Integração com API de Eventos NGX (Event Webhook)

**Como** operador da plataforma SmartFlow,
**Quero** receber, validar e processar os **16 tipos de eventos** enviados pela NGX Events API via webhook,
**Para** que o journey builder e os disparos de SMS/RCS da SendSpeed sejam acionados em tempo real com base nas ações dos jogadores (cadastro, depósito, saque, aposta esportiva, cassino, premiação, bonificação, exclusão).

---

## 📄 Documentação de Referência

Especificação completa: **NGX Events API v1.0.3** — 55 páginas, 16 endpoints

| # | Evento | `type` | Endpoint NGX | Campos-chave |
| -- | -- | -- | -- | -- |
| 1 | Cadastro de usuário | `USER_REGISTRATION` | /user-registration | user_id, user_name, user_cpf, user_email, user_contact, user_credits, user_bonus_credits, user_has_kyc, user_accepted_notifications, external_params |
| 2 | Login | `USER_LOGIN` | /user-login | login_ip_address, login_source, login_agent, login_username, login_user_id |
| 3 | Autoexclusão / Exclusão Admin | `USER_DELETE` | /user-delete | user_id + profile completo + locked flags |
| 4 | Exclusão Permanente (30d após) | `USER_DELETE` | /user-data-delete | Mesmo schema de exclusão |
| 5 | Solicitação de Depósito | `DEPOSIT_REQUEST` | /deposit-request | deposit_id, deposit_value, deposit_qr_code (Pix Copia e Cola), deposit_created_at |
| 6 | **Confirmação de Depósito** | `DEPOSIT_CONFIRMATION` | /deposit-confirmation | deposit_id, deposit_value, deposit_qr_code_image, deposit_status (PENDING |
| 7 | Solicitação de Saque | `WITHDRAWAL_REQUEST` | /withdrawal-request | withdraw_id, withdraw_value, withdraw_pix_key, withdraw_pix_type, withdraw_status |
| 8 | **Confirmação de Saque** | `WITHDRAWAL_CONFIRMATION` | /withdrawal-confirmation | withdraw_id + status |
| 9 | **Aposta Esportiva** | `BET_PLACEMENT` | /bet-placement | bet_id, bet_value, sport_id, sport_name, event_id, event_name, market_id, market_name, selection, odds, bet_events[] |
| 10 | **Distribuição de Prêmio (Esportes)** | `PRIZE_DISTRIBUTION` | /prize-distribution | prize_id, prize_value, game_id, game_name, bet_id |
| 11 | **Aposta Cassino** | `CASINO_BET` | /casino-bet | bet_id, bet_value, game_id, game_name, game_round_id |
| 12 | **Prêmio Cassino** | `CASINO_PRIZE` | /casino-prize | prize_id, prize_value, game_id, game_round_id, bet_id |
| 13 | **Reembolso Cassino** | `CASINO_REFUND` | /casino-refund | refunded_transaction_id, refunded_value, game_id, game_round_id |
| 14 | Bônus → Saldo Real | `BONUS_TO_CREDITS` | /bonus-to-credits | transaction_id, transaction_value |
| 15 | Transferência Admin | `CREDITS_TO_USER` | /credits-to-user | user_from_id, user_to_id, transaction_value |
| 16 | Atualização de Afiliado | `AFFILIATION_UPDATE` | /affiliation-update | affiliate_id, old_affiliate_id, user_to_id |

---

## 🛡️ Autenticação e Segurança

A NGX utiliza **HMAC-SHA256**:

1. Header `X-Auth-Signature` contém a assinatura HMAC do body em Base64
2. Chave secreta **compartilhada** entre NGX e SmartFlow (precisa ser configurada)
3. Validação: gerar HMAC-SHA256 do body com a secret key → codificar em Base64 → comparar com X-Auth-Signature
4. Se divergir → HTTP 401 e descarte do evento

Exemplo real (do documento):

* Body: `{"user_id":"123456","user_name":"name","user_username":"username","user_birth_date":"10/10/1990","user_cpf":"00011122233","user_email":"test@email.com","user_contact":"11988887777"}`
* Secret Key: `66001508-2413-11ee-be56-0242ac120002`
* HMAC gerado: `17wJrEqpFFQF2Arz5+7OklahFKPeO2rbTMKA7juG5Ek=`

---

## 🧠 Mapeamento de Dados (Campos Compartilhados)

Cada evento NGX carrega o perfil completo do jogador (~30 campos):

| Campo NGX | Tipo | Mapeamento SmartFlow | Uso |
| -- | -- | -- | -- |
| user_id | String | player_id (PK) | Identificador único |
| user_name | String | player_name | Personalização |
| user_contact | String | player_phone | **Telefone para disparo SMS/RCS** |
| user_credits | Float | player_balance | Saldo atual |
| user_bonus_credits | Float | player_bonus_balance | Saldo bônus |
| user_cpf | String | player_document | Documento (hash LGPD) |
| user_has_kyc | Boolean | kyc_verified | Gatekeeper para disparos |
| user_accepted_notifications | Boolean | optin_sms | Consentimento LGPD |
| user_locked | Boolean | player_blocked | Conta bloqueada? |
| external_params | JSON | utm_params | Dados de link de cadastro |

---

## 📋 Critérios de Aceitação (BDD)

### Cenário 1: Recebimento e validação de depósito confirmado

**Given** que a NGX envia POST /deposit-confirmation com X-Auth-Signature válido e body { type: "DEPOSIT_CONFIRMATION", user_id: "123", user_contact: "5511998887777", user_has_kyc: true, user_accepted_notifications: true, deposit_id: "dep_789", deposit_value: 150.00, deposit_status: "PAID" }
**When** o sistema processa o evento
**Then** a assinatura HMAC-SHA256 é validada com a secret key
**And** o perfil completo do jogador é parseado e normalizado (30 campos)
**And** deposit_value R$ 150,00 é salvo como transaction_amount
**And** verifica user_has_kyc=true e user_accepted_notifications=true antes de acionar jornada
**And** a jornada SmartFlow para "deposito_confirmado" é acionada
**And** retorna HTTP 200

### Cenário 2: Cadastro com rastreamento de afiliado

**Given** que a NGX envia POST /user-registration com body { type: "USER_REGISTRATION", user_id: "456", user_contact: "5511987654321", user_email: "[novo@email.com](<mailto:novo@email.com>)", user_accepted_notifications: true, user_has_kyc: false, user_affiliated: true, user_affiliation: "aff_123", external_params: { utm_source: "google_ads", utm_campaign: "cpa_bonus_50" } }
**When** o sistema processa
**Then** o jogador "456" é registrado com status "pré-ativo" (KYC pendente)
**And** o telefone é salvo como canal de contato
**And** parâmetros UTM são persistidos para atribuição
**And** jornada de boas-vindas é agendada (condicionada ao KYC)

### Cenário 3: Assinatura HMAC inválida

**Given** que um request chega com X-Auth-Signature alterado
**When** o sistema valida a assinatura
**Then** retorna HTTP 401 Unauthorized
**And** evento descartado com log de segurança (WARN)

### Cenário 4: Self-exclusion com bloqueio total

**Given** que a NGX envia POST /user-delete com body { type: "USER_DELETE", user_id: "123", user_locked: true, user_locked_deposit: true, user_locked_withdraw: true, user_locked_bet: true }
**When** o sistema processa
**Then** o jogador é marcado como "auto-excluído"
**And** todas as jornadas ativas são CANCELADAS
**And** número é mantido em blocklist
**And** nenhum disparo é enviado a partir deste momento

### Cenário 5: Resiliência — evento com falha de processamento

**Given** que o banco de dados está indisponível
**When** o sistema recebe o webhook
**Then** o evento é armazenado em Dead Letter Queue
**And** retorna HTTP 200 para a NGX (evitar reenvio)
**And** job de retry: 1min → 5min → 15min (3 tentativas)
**And** após 3 falhas, evento marcado como "failed" com notificação ao time

---

## 📐 Regras de Negócio

1. **Gatekeeper de consentimento**: Só disparar SMS/RCS se user_accepted_notifications = true (presente em TODOS os eventos)
2. **KYC obrigatório**: Só acionar jornada de depósito se user_has_kyc = true
3. **Autoexclusão prioritária**: USER_DELETE sobrepõe jornadas ativas e bloqueia o player imediatamente
4. **Casino Refund sem disparo**: CASINO_REFUND registra em auditoria mas não aciona jornada
5. **Rejeição silenciosa**: Eventos com is_test=true são logados mas NÃO processados em jornadas reais
6. **Guest Player**: Se deposit_guest_player=true, não disparar comunicação até USER_REGISTRATION

---

## 📊 Matriz de Roteamento por Evento

| Evento | Jornada? | Disparo? | Prioridade |
| -- | -- | -- | -- |
| USER_REGISTRATION | Boas-vindas condicional | ✅ Se opt-in | Alta |
| USER_LOGIN | ❌ auditoria | ❌ | Baixa |
| USER_DELETE | Cancela jornadas | ❌ bloqueio | **Crítica** |
| DEPOSIT_REQUEST | ❌ aguardar | ❌ | Média |
| DEPOSIT_CONFIRMATION | Depósito recebido | ✅ Confirmação | **Crítica** |
| WITHDRAWAL_REQUEST | Saque solicitado | ✅ alto valor | Média |
| WITHDRAWAL_CONFIRMATION | Saque concluído | ✅ Confirmação | Alta |
| BET_PLACEMENT | Aposta registrada | ✅ Confirmação | **Alta** |
| PRIZE_DISTRIBUTION | Premiação | 🎉 Parabéns | **Alta** |
| CASINO_BET | Aposta cassino | ✅ Confirmação | Média |
| CASINO_PRIZE | Ganho cassino | 🎉 Parabéns | **Alta** |
| CASINO_REFUND | ❌ auditoria | ❌ | Baixa |
| BONUS_TO_CREDITS | Bônus convertido | ✅ Notificação | Média |
| CREDITS_TO_USER | Crédito recebido | ✅ Cortesia | Média |
| AFFILIATION_UPDATE | ❌ auditoria | ❌ | Baixa |

---

## ⚙️ Definição de Pronto (DoD)

### Arquitetura

- [ ] Webhook receiver único: POST /api/webhooks/ngx (roteia por "type" no body)
- [ ] Middleware HMAC-SHA256 validation com secret key configurável por ambiente
- [ ] HashMap de 16 parsers de evento (extrai campos específicos + perfil comum)
- [ ] Normalizador de datas: DD/MM/YYYY HH:MM:SS → ISO 8601 UTC
- [ ] Fila assíncrona (RabbitMQ/Kafka) antes de processar jornadas
- [ ] Dead Letter Queue com retry progressivo (1min→5min→15min→falha)
- [ ] Rate limiter: máx 100 req/s por supplier_id

### Qualidade

- [ ] Testes de unidade para cada um dos 16 parsers
- [ ] Testes de integração com payloads reais do sandbox NGX
- [ ] Teste de validação HMAC com o exemplo do doc (secret 66001508-2413-11ee-be56-0242ac120002)
- [ ] Teste de carga simulando pico de partidas ao vivo
- [ ] Logging estruturado (JSON para Dozzle)
- [ ] Métrica Grafana: ngx_events_received_total{type,status}

### Operação

- [ ] Playbook: "O que fazer quando webhook NGX parar de chegar"
- [ ] Documentação interna dos eventos e campos mapeados
- [ ] Configuração da URL do webhook no painel NGX (time de operações)
- [ ] Healthcheck: GET /api/webhooks/ngx/health

---

## 🧩 Tarefas de Desdobramento (estimativa: ~26 SP)

| Tarefa | Descrição | SP | Responsável |
| -- | -- | -- | -- |
| 1. Spike: Descoberta técnica | Obter sandbox NGX, validar conectividade, testar HMAC | 3 | Andrei/Thiago |
| 2. Webhook receiver + validação HMAC | Endpoint POST único, middleware, rate-limit, logging | 5 | Backend |
| 3. Parser + normalização dos eventos | HashMap 16 parsers, conversão datas, validação campos | 8 | Backend |
| 4. Roteamento para filas e jornadas | Conectar parser a filas, mapear eventos → triggers de jornada | 5 | Thiago |
| 5. Testes e2e + monitoramento | Sandbox NGX, métricas, dashboard Grafana, alertas | 5 | Backend+QC |

---

## 📌 Nota Estratégica

⚠️ **Risco identificado**: NGX e FastTrack compartilham o mesmo padrão (provedor iGaming que envia callbacks POST com perfil completo do jogador). **Recomendação**: construir um adaptador genérico (interface IGamingWebhookHandler) para evitar retrabalho com futuros provedores whitelabel.

---

## 🔍 Volume Estimado

* Usuários ativos por operador: milhares
* Eventos por usuário/dia: ~5-15
* Estimativa: **50k a 200k eventos/dia** no pico
* Pico: partidas ao vivo podem gerar 500+ eventos/min
* Payload médio: ~2KB (perfil do jogador incluso)
* Tráfego: ~100-400 MB/dia

## Histórico de status
- Backlog (backlog): 2026-06-18T22:28:25.309Z → atual

## Relações
—

## Anexos
—
