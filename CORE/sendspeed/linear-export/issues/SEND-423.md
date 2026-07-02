# SEND-423 — 🚀 - Analytics de acesso e registro atribuídos à Jornada RCS

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | Urgent |
| Responsável | Vinicius Carneiro |
| Time | Sendspeed |
| Projeto | — |
| Labels | Implementação, Jornadas, User Story |
| Parent | — |
| Criada | 2026-03-20T14:48:00.662Z por Vinicius Carneiro |
| Iniciada | 2026-03-25T18:33:01.608Z |
| Concluída | 2026-04-14T15:16:08.823Z |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-423--analytics-de-acesso-e-registro-atribuidos-a-jornada-rcs |
| URL | https://linear.app/sendspeed/issue/SEND-423/analytics-de-acesso-e-registro-atribuidos-a-jornada-rcs |

## Descrição

> **Como** analista de dados da operação
> **Quero** ver no analytics da jornada quantos acessos (logins) e registros foram gerados a partir dos RCS enviados
> **Para** medir o ROI real do canal RCS, entendendo o funil completo: Enviado → Entregue → Acessou o site → Registrou → Fez primeiro depósito (FTD), e justificar investimento no canal com dados concretos.

---

# 📈 Use Case: Relatório de ROI da jornada de reativação

A operadora rodou uma jornada de reativação para 10.000 jogadores inativos usando RCS. Após 7 dias, o analista precisa reportar: dos 10.000 RCS enviados, 9.200 foram entregues (92%), 3.100 acessaram o site (34% dos entregues), 450 fizeram novo depósito (14% dos que acessaram), gerando R$ 67.500 em depósitos atribuídos à jornada. O funil completo é visualizado no painel de analytics com breakdown por canal.

# ✅ Critérios de aceite:

* Touchpoints com `channel: 'rcs'` devem ser processados pelo `attributionService` para atribuição de conversões (registro, FTD, depósito).
* O analytics da jornada deve exibir breakdown por canal de origem da conversão (qual mensagem RCS/SMS levou ao registro).
* Deve ser possível visualizar o funil: Enviado → Entregue → Acessou → Registrou → FTD por canal.
* Acessos (logins) pós-envio devem ser rastreados e vinculados ao Touchpoint ativo.
* Valor total de depósitos atribuídos deve ser exibido por canal.
* A janela de atribuição (default 72h, max 30 dias) deve ser respeitada.

# 🧩 Cenários de teste:

- [ ] Enviar RCS → usuário acessa site → Touchpoint RCS é atribuído ao acesso.
- [ ] Enviar RCS → usuário registra → conversão atribuída ao canal RCS no analytics.
- [ ] Enviar RCS e SMS na mesma jornada → atribuição distingue qual canal gerou a conversão (last touch).
- [ ] Usuário acessa após janela de atribuição (ex: 4 dias com janela de 72h) → NÃO atribuído.
- [ ] Funil exibe corretamente: Enviados, Entregues, Acessos, Registros, FTDs por canal.
- [ ] Valor total de depósitos atribuídos é calculado e exibido no painel.
- [ ] Analytics de jornada sem envio de RCS não é afetado (sem regressão).

## Histórico de status
- Backlog (backlog): 2026-03-20T14:48:00.662Z → 2026-03-20T15:22:08.857Z
- To-do (unstarted): 2026-03-20T15:22:08.857Z → 2026-03-25T18:33:01.622Z
- In Progress (started): 2026-03-25T18:33:01.622Z → 2026-03-26T12:44:25.075Z
- Pull Request (started): 2026-03-26T12:44:25.075Z → 2026-03-26T14:34:58.123Z
- Product Review (started): 2026-03-26T14:34:58.123Z → 2026-04-14T15:16:08.843Z
- Released (completed): 2026-04-14T15:16:08.843Z → atual

## Relações
—

## Anexos
—
