# SEND-421 — 🚀 - Nó de Enviar RCS na Jornada com seleção de template

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | Urgent |
| Responsável | Vinicius Carneiro |
| Time | Sendspeed |
| Projeto | — |
| Labels | Implementação, Jornadas, User Story, UserIn |
| Parent | — |
| Criada | 2026-03-20T14:46:43.610Z por Vinicius Carneiro |
| Iniciada | 2026-03-20T21:10:12.246Z |
| Concluída | 2026-04-01T12:10:25.008Z |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-421--no-de-enviar-rcs-na-jornada-com-selecao-de-template |
| URL | https://linear.app/sendspeed/issue/SEND-421/no-de-enviar-rcs-na-jornada-com-selecao-de-template |

## Descrição

> **Como** operador da Userin configurando jornadas no Journey Builder
> **Quero** arrastar um nó "Enviar RCS" para o fluxo e selecionar qual template RCS será enviado
> **Para** incluir o disparo de RCS como ação dentro de jornadas automatizadas, aproveitando templates prontos e variáveis personalizadas, sem precisar usar apenas campanhas batch.

---

# 📈 Use Case: Jornada de retenção pós-churn com RCS

Um jogador da plataforma Jogão não acessa há 7 dias. O webhook de inatividade dispara a jornada. O fluxo é: Webhook → Delay 1h → Condição (tem depósito?) → Sim: Enviar RCS "Volta VIP" com bônus personalizado → Não: Enviar RCS "Primeiro Depósito" com oferta de boas-vindas. O operador seleciona os templates RCS no nó de ação, escolhe a credencial do provedor (Infobip ou Pushfy) e ativa a jornada.

# ✅ Critérios de aceite:

* Deve existir o nó `action.sendRcs` no catálogo do Journey Builder (arrastar para o canvas).
* O painel de configuração do nó deve permitir selecionar um template RCS (dropdown com templates ativos da empresa).
* O painel deve permitir selecionar a credencial de envio (scope `send_rcs`).
* O executor deve buscar o telefone do usuário (perfil, contato, visitorId).
* O executor deve resolver variáveis Liquid no conteúdo do template antes do envio.
* O envio deve chamar `POST /api/rcs/:companyId/send` na Integrations API.
* Um Touchpoint com `channel: 'rcs'` deve ser criado para atribuição.
* Em caso de falha, o nó deve registrar `exitReason` adequado (NO_PHONE, RCS_SEND_FAILED, INTEGRATION_OFFLINE, etc.).

# 🧩 Cenários de teste:

- [ ] Arrastar nó "Enviar RCS" para o canvas e conectar a um trigger.
- [ ] Selecionar template RCS no painel de configuração — lista apenas templates tipo `rcs`.
- [ ] Selecionar credencial com scope `send_rcs`.
- [ ] Executar jornada com usuário que tem telefone → RCS enviado com sucesso.
- [ ] Executar jornada com usuário sem telefone → exit reason `NO_PHONE`.
- [ ] Verificar que Touchpoint é criado com `channel: 'rcs'` após envio bem-sucedido.
- [ ] Verificar resolução de variáveis Liquid no conteúdo do template.
- [ ] Simular falha na Integrations API → exit reason `RCS_SEND_FAILED` registrado no step.
- [ ] Verificar que o nó aparece corretamente no funnel de analytics da jornada.

## Histórico de status
- Backlog (backlog): 2026-03-20T14:46:43.610Z → 2026-03-20T15:21:10.176Z
- To-do (unstarted): 2026-03-20T15:21:10.176Z → 2026-03-20T21:10:12.256Z
- In Progress (started): 2026-03-20T21:10:12.256Z → 2026-03-23T17:43:57.471Z
- Pull Request (started): 2026-03-23T17:43:57.471Z → 2026-03-24T17:29:09.470Z
- Product Review (started): 2026-03-24T17:29:09.470Z → 2026-03-25T13:31:32.840Z
- Done (started): 2026-03-25T13:31:32.840Z → 2026-03-25T13:31:41.048Z
- Product Review (started): 2026-03-25T13:31:41.048Z → 2026-03-31T18:24:33.398Z
- Release (started): 2026-03-31T18:24:33.398Z → 2026-04-01T12:10:25.018Z
- Released (completed): 2026-04-01T12:10:25.018Z → atual

## Relações
—

## Anexos
—
