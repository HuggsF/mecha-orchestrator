# SEND-380 — 🚀 - Disparo de RCS automatizado via nó de ação no Journey Builder

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | Medium |
| Responsável | thiago.melin@sendspeed.com |
| Time | Sendspeed |
| Projeto | — |
| Labels | User Story, Jornadas, UserIn |
| Parent | — |
| Criada | 2026-03-13T12:33:32.126Z por Vinicius Carneiro |
| Iniciada | 2026-03-31T18:33:14.333Z |
| Concluída | 2026-06-22T17:15:52.947Z |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-380--disparo-de-rcs-automatizado-via-no-de-acao-no-journey |
| URL | https://linear.app/sendspeed/issue/SEND-380/disparo-de-rcs-automatizado-via-no-de-acao-no-journey-builder |

## Descrição

> **Como** gestor de CRM de uma operadora de iGaming
> **Quero** configurar um nó "Enviar RCS" dentro de uma jornada automatizada no Journey Builder
> **Para** que jogadores recebam mensagens ricas e interativas automaticamente com base em comportamento, com maior taxa de engajamento que SMS

---

# 📈 Use Case: Jornada de reativação de churn com RCS e fallback SMS

A operadora configura uma jornada de reativação de churn no Journey Builder:

1. **Trigger**: RuleMatch:inactive_7d (jogador não acessa há 7 dias)
2. **Condição**: UserAttribute:phone (verifica se tem telefone)
3. **Ação**: Nó "Enviar RCS" dispara:

> "{{contact.firstName}}, temos odds especiais esperando por você! Volte agora."

O SendRcsExecutor busca a credencial RCS da empresa (scope: send_rcs), resolve variáveis Liquid, envia via /api/rcs/:companyId/send e registra o **Touchpoint com atribuição Last Touch** (janela de 72h). Se o jogador voltar e depositar, a conversão é atribuída a este RCS como último ponto de contato. Se o envio falhar, o exit reason RCS_SEND_FAILED permite fallback via SMS.

**Modelo de atribuição**: Last Touch (default) — 100% do crédito da conversão vai para o último touchpoint antes do evento de conversão. Configurável por jornada para first_touch, linear, time_decay ou position_based.

---

# ✅ Critérios de aceite:

* Novo SendRcsExecutor criado seguindo o padrão do SendSmsExecutor
* Nó action.sendRcs registrado no NodeEngine e disponível no Journey Builder
* Configuração do nó permite: mensagem livre, template de RCS ou credencial específica
* Mensagem suporta variáveis Liquid ({{contact.firstName}}, {{name:Amigo}})
* Busca telefone em múltiplas fontes (mesmo fluxo do SendSmsExecutor)
* Valida credencial RCS da empresa (scope: send_rcs) antes do envio
* Envia via INTEGRATIONS_API_URL/api/rcs/:companyId/send
* Registra Touchpoint com channel: rcs, journeyId, nodeId e janela de atribuição configurável
* Atribuição Last Touch: conversão creditada ao último RCS dentro da janela
* Confidence score calculado com base no tempo entre envio e conversão
* Retorna exit reasons específicos para cada cenário de falha
* Nó exportado no actions/index.js e registrado no registry do Journey Builder
* Fluxo continua para o próximo nó após execução (permite fallback para SMS)

---

# 🧩 Cenários de teste:

- [ ] Arrastar nó "Enviar RCS" no Journey Builder e configurar mensagem com variáveis
- [ ] Simular jornada com perfil que tem telefone — RCS enviado com sucesso
- [ ] Verificar que Touchpoint é criado com channel: rcs, journeyId e expiresAt
- [ ] Simular conversão dentro da janela — Touchpoint marcado como converted com last_touch
- [ ] Simular conversão fora da janela de 72h — não atribuída
- [ ] Simular RCS + SMS para o mesmo usuário — Last Touch atribui ao mais recente
- [ ] Simular jornada sem credencial RCS — exit reason NO_RCS_INTEGRATION
- [ ] Simular falha no envio RCS e verificar fallback para nó SMS
- [ ] Simular API offline — exit reason INTEGRATION_OFFLINE
- [ ] Validar que SendRcsExecutor está exportado no actions/index.js

---

## 🎯 Priorização RICE — Score: 4.5

| Reach | Impact | Confidence | Effort | Score |
| -- | -- | -- | -- | -- |
| 6 | 3 (massive) | 50% | 2 meses | **4.5** |

**Justificativa:** Reach 6: empresas que adotarem RCS. Impacto massive (3): habilita canal rico nas jornadas. Confidence 50%: depende de SEND-391 e SEND-378. Esforço 2 meses: executor + nó + touchpoint + fallback.

## Histórico de status
- Backlog (backlog): 2026-03-13T12:33:32.126Z → 2026-03-13T15:01:05.222Z
- To-do (unstarted): 2026-03-13T15:01:05.222Z → 2026-03-31T18:33:14.345Z
- In Progress (started): 2026-03-31T18:33:14.345Z → 2026-06-22T17:15:52.957Z
- Released (completed): 2026-06-22T17:15:52.957Z → atual

## Relações
- related: SEND-391 — [Tech] SendSmsExecutor integracao API real no journey backend
- related: SEND-378 — 🚀 - Disparo de SMS automatizado via nó de ação no Journey Builder

## Anexos
—
