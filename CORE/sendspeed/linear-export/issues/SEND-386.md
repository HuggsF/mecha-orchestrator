# SEND-386 — 🚀 - Reprocessamento e análise de dados de Black List na Sendspeed

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | No priority |
| Responsável | thiago.melin@sendspeed.com |
| Time | Sendspeed |
| Projeto | — |
| Labels | User Story, Sendspeed, Implementação |
| Parent | — |
| Criada | 2026-03-13T14:53:45.848Z por Vinicius Carneiro |
| Iniciada | 2026-03-13T15:00:20.127Z |
| Concluída | 2026-06-22T17:15:46.838Z |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-386--reprocessamento-e-analise-de-dados-de-black-list-na |
| URL | https://linear.app/sendspeed/issue/SEND-386/reprocessamento-e-analise-de-dados-de-black-list-na-sendspeed |

## Descrição

> **Como** gestor de operações da Sendspeed
> **Quero** reprocessar e analisar os dados da black list de números bloqueados para envio de mensagens
> **Para** garantir que campanhas de SMS e RCS não disparem para números bloqueados, reduzindo custos com envios inválidos e evitando penalizações das operadoras

---

# 📈 Use Case: Limpeza e validação da base antes de disparo de campanha

A Sendspeed possui uma black list de números que não devem receber mensagens (opt-out, números inválidos, reclamações, números de operadoras bloqueadas). Antes de uma campanha de SMS ser disparada para 50.000 contatos, o sistema precisa:

1. **Importar/atualizar a black list**: Receber arquivo atualizado (CSV/XLSX) ou via API com números bloqueados, motivo do bloqueio (opt-out, inválido, reclamação, operadora) e data de inclusão.
2. **Reprocessar a base**: Cruzar a lista de destinatários da campanha com a black list. Dos 50.000 contatos, identificar que 3.200 estão na black list — 1.800 por opt-out, 900 por número inválido, 500 por reclamação.
3. **Dashboard de análise**: Visualizar métricas da black list — total de números bloqueados, distribuição por motivo, tendência de crescimento (quantos novos por semana), taxa de black list por campanha (ex: campanha X teve 12% de números bloqueados vs média de 6%).
4. **Filtro automático no envio**: CampaignWorker e CampaignService consultam a black list antes de enviar cada mensagem. Números bloqueados são marcados como `skipped_blacklist` no CampaignRecipient, sem consumir crédito de envio.

**Resultado**: A campanha envia para 46.800 números válidos, economizando o custo de 3.200 envios inúteis e mantendo a reputação da Sendspeed com as operadoras.

---

# ✅ Critérios de aceite:

* Importação de black list via CSV/XLSX ou API com número, motivo e data
* Reprocessamento cruza destinatários da campanha com a black list antes do envio
* CampaignWorker e CampaignService filtram números da black list automaticamente
* Destinatários bloqueados marcados como skipped_blacklist (não contam como falha)
* Dashboard com métricas: total bloqueados, distribuição por motivo, tendência semanal
* Taxa de black list por campanha visível no detalhe da campanha
* Opt-out via resposta de SMS (ex: SAIR) adiciona automaticamente à black list
* API de consulta para verificar se um número está na black list

---

# 🧩 Cenários de teste:

- [ ] Importar CSV com 1.000 números bloqueados e verificar que foram adicionados à black list
- [ ] Criar campanha com lista que contém números da black list — verificar que são filtrados antes do envio
- [ ] Verificar que destinatários filtrados são marcados como skipped_blacklist no CampaignRecipient
- [ ] Verificar que stats da campanha não contam skipped_blacklist como falha
- [ ] Acessar dashboard de black list e verificar métricas de distribuição por motivo
- [ ] Adicionar número via API e verificar que próxima campanha não envia para ele
- [ ] Remover número da black list e verificar que volta a receber mensagens
- [ ] Verificar que black list é consultada tanto no CampaignWorker (Kafka) quanto no CampaignService (síncrono)

## Histórico de status
- Backlog (backlog): 2026-03-13T14:53:45.848Z → 2026-03-13T15:00:20.139Z
- In Progress (started): 2026-03-13T15:00:20.139Z → 2026-03-17T15:17:04.854Z
- Pull Request (started): 2026-03-17T15:17:04.854Z → 2026-06-22T17:15:46.849Z
- Released (completed): 2026-06-22T17:15:46.849Z → atual

## Relações
—

## Anexos
—
