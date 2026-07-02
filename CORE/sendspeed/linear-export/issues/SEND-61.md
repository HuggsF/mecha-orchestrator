# SEND-61 — [BUG] [JORNEY] Visão Geral mostrando dados mockados

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | Medium |
| Responsável | peterson.marques@sendspeed.com |
| Time | Sendspeed |
| Projeto | — |
| Labels | — |
| Parent | — |
| Criada | 2025-08-22T12:31:14.496Z por bruno.heidrich@sendspeed.com |
| Iniciada | 2025-08-26T14:45:35.334Z |
| Concluída | 2025-09-04T19:36:36.267Z |
| Arquivada | 2026-03-12T01:50:30.790Z |
| Vencimento | — |
| Branch | hugofernandes/send-61-bug-jorney-visao-geral-mostrando-dados-mockados |
| URL | https://linear.app/sendspeed/issue/SEND-61/bug-jorney-visao-geral-mostrando-dados-mockados |

## Descrição

**Como reproduzir**
Abrir a tela "Visão Geral" do Journey; alguns blocos exibem números que não refletem a realidade (parecem dados de exemplo).

**Esperado**
A tela deve mostrar **apenas dados reais**, atualizar corretamente ao mudar o período e exibir estado vazio quando não houver dados. Em tempo real.

**Pronto quando**

* Todos os blocos exibem **dados reais e consistentes**.
* Trocar o período **atualiza** a tela corretamente.
* **Nenhum** dado de exemplo aparece.

**Para quem for executar essa tarefa, tirar a parte que fala JOURNEY ENTENDA E ACOMPANHE A JORNADA…**

> **[Imagem 1 — transcrição]:** Screenshot de UI (tela "Journey / Visão Geral"). Título "Journey" com subtítulo "Gerencie e analise a jornada do usuário". Seção "Journey" com texto "Entenda e acompanhe a jornada do usuário baseado em comportamentos e dados." Três cartões de métricas: "Novos usuários" = **124** (↑ +12%, "últimos 7 dias"); "Engajamento médio" = **4.2 min** (↑ +0.8 min, "vs. mês passado"); "Eventos capturados" = **52,431** (↑ +18.2%, "últimas 24 horas"). Bloco "Segmentos de jornada" listando: "Novos assinantes — Usuários que se inscreveram nos últimos 30 dias" = **231**; "Usuários ativos — Usuários que fizeram login nos últimos 7 dias" = **1,892**; "Alto valor — Usuários com 5+ compras/mês" = **164**. Os valores são os dados mockados/de exemplo que devem ser substituídos por dados reais.

## Histórico de status
- To-do (unstarted): 2025-08-22T12:31:14.496Z → 2025-08-26T14:45:35.321Z
- In Progress (started): 2025-08-26T14:45:35.321Z → 2025-08-27T15:02:12.632Z
- Pull Request (started): 2025-08-27T15:02:12.632Z → 2025-09-04T19:36:36.302Z
- Released (completed): 2025-09-04T19:36:36.302Z → atual

## Relações
—

## Anexos
—
