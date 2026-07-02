# SEND-378 — 🚀 - Disparo de SMS automatizado via nó de ação no Journey Builder

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | High |
| Responsável | thiago.melin@sendspeed.com |
| Time | Sendspeed |
| Projeto | — |
| Labels | User Story, Jornadas, UserIn, Melhoria |
| Parent | — |
| Criada | 2026-03-13T12:33:06.497Z por Vinicius Carneiro |
| Iniciada | 2026-03-31T18:32:30.248Z |
| Concluída | 2026-06-22T17:15:53.814Z |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-378--disparo-de-sms-automatizado-via-no-de-acao-no-journey |
| URL | https://linear.app/sendspeed/issue/SEND-378/disparo-de-sms-automatizado-via-no-de-acao-no-journey-builder |

## Descrição

> **Como** gestor de retenção de uma plataforma de iGaming
> **Quero** configurar um nó "Enviar SMS" dentro de uma jornada automatizada no Journey Builder
> **Para** que jogadores recebam uma mensagem SMS automaticamente ao atingir uma condição comportamental, sem intervenção manual

---

# 📈 Use Case: Jornada de boas-vindas com SMS de incentivo ao primeiro depósito

A Apostatudo configura uma jornada de boas-vindas no Journey Builder:

1. **Trigger**: Evento register (quando usuário se cadastra)
2. **Delay**: Espera 2 horas
3. **Condição**: Verifica se fez depósito (HasTag:first_deposit)
4. **Ação (se NÃO fez depósito)**: Nó "Enviar SMS" dispara:

> "{{contact.firstName}}, seu bônus de R$50 expira em 24h! Deposite agora."

O sistema busca o telefone do perfil unificado (profile → CRM → segment-engine), valida a credencial SMS da empresa, envia via API de integrações e registra o **Touchpoint com atribuição Last Touch** (janela de 72h). Se o jogador depositar dentro dessa janela, a conversão (FTD) é atribuída a este SMS como último ponto de contato, com confidence score calculado proporcionalmente ao tempo decorrido.

**Modelo de atribuição**: Last Touch (default) — 100% do crédito da conversão vai para o último touchpoint antes do evento de conversão. Configurável por jornada para first_touch, linear, time_decay ou position_based.

---

# ✅ Critérios de aceite:

* Nó action.sendSms disponível no Journey Builder para drag-and-drop
* Configuração do nó permite: mensagem livre, template de SMS ou credencial específica
* Mensagem suporta variáveis Liquid ({{contact.firstName}}, {{name:Amigo}})
* Busca telefone em múltiplas fontes: contexto → profile → CRM Contact → segment-engine
* Valida credencial SMS da empresa antes do envio (específica ou default ativa)
* Envia via INTEGRATIONS_API_URL/api/sms/:companyId/send
* Registra Touchpoint com canal sms, journeyId, nodeId e janela de atribuição configurável
* Atribuição Last Touch: conversão é creditada ao último SMS enviado dentro da janela
* Confidence score calculado com base no tempo entre envio e conversão (<1h = 0.85, <6h = 0.75, <24h = 0.65, <48h = 0.55, >48h = 0.50)
* Retorna exit reasons claros para cada cenário de falha
* Fluxo continua para o próximo nó após execução (success ou fail)

---

# 🧩 Cenários de teste:

- [ ] Arrastar nó "Enviar SMS" no Journey Builder e configurar mensagem com variáveis Liquid
- [ ] Simular jornada com perfil que tem telefone — SMS enviado com sucesso
- [ ] Verificar que Touchpoint é criado com channel: sms, journeyId e expiresAt (72h default)
- [ ] Simular conversão (hook first_deposit) dentro da janela — Touchpoint marcado como converted com attributionModel: last_touch
- [ ] Simular conversão fora da janela de 72h — Touchpoint expirado, conversão não atribuída
- [ ] Verificar confidence score: conversão em <1h retorna 0.85, em >48h retorna 0.50
- [ ] Simular dois SMSs para o mesmo usuário — Last Touch atribui 100% ao mais recente
- [ ] Simular jornada com perfil sem telefone — exit reason NO_PHONE_REGISTERED_USER
- [ ] Simular jornada sem credencial SMS — exit reason NO_SMS_INTEGRATION
- [ ] Simular API offline — exit reason INTEGRATION_OFFLINE

---

## 🎯 Priorização RICE — Score: 12.8

| Reach | Impact | Confidence | Effort | Score |
| -- | -- | -- | -- | -- |
| 8 | 3 (massive) | 80% | 1.5 meses | **12.8** |

**Justificativa:** Feature core — SMS automatizado nas jornadas. Reach 8: todas as empresas com jornadas de SMS. Impacto massive (3): habilita envio real de SMS via nó de ação (hoje é stub). Confidence 80%: depende do SEND-391. Esforço 1.5 meses.

## Histórico de status
- Backlog (backlog): 2026-03-13T12:33:06.497Z → 2026-03-13T15:01:09.035Z
- To-do (unstarted): 2026-03-13T15:01:09.035Z → 2026-03-31T18:32:30.260Z
- In Progress (started): 2026-03-31T18:32:30.260Z → 2026-06-22T17:15:53.823Z
- Released (completed): 2026-06-22T17:15:53.823Z → atual

## Relações
- related: SEND-380 — 🚀 - Disparo de RCS automatizado via nó de ação no Journey Builder

## Anexos
—
