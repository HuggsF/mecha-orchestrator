# SEND-50 — Exportação Estrutural do Card para Embeds Externos

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | Urgent |
| Responsável | — |
| Time | Sendspeed |
| Projeto | — |
| Labels | — |
| Parent | — |
| Criada | 2025-07-28T19:02:16.815Z por bruno.heidrich@sendspeed.com |
| Iniciada | — |
| Concluída | 2025-08-11T13:52:59.703Z |
| Arquivada | 2026-02-15T02:17:35.885Z |
| Vencimento | — |
| Branch | hugofernandes/send-50-exportacao-estrutural-do-card-para-embeds-externos |
| URL | https://linear.app/sendspeed/issue/SEND-50/exportacao-estrutural-do-card-para-embeds-externos |

## Descrição

**Como** PM responsável pela entrega dos cards para múltiplos canais
**Eu quero** exportar o card com todas as informações necessárias (HTML + JSON de configuração)
**Para que** o card e seu preview possam ser renderizados com alta fidelidade em qualquer ambiente externo, sem perda de qualidade ou funcionalidade

#### **🎯 Critérios de Aceitação:**

* ✅ **AC01**: O HTML exportado deve ser **idêntico visualmente** ao que é exibido no preview da plataforma
* ✅ **AC02**: O JSON deve conter todas as informações dinâmicas necessárias para reidratar o card (ex: ações dos botões, parâmetros de tracking, fontes, variantes de layout)
* ✅ **AC03**: Deve ser possível plotar apenas a versão preview do card (miniatura reduzida) a partir do mesmo bundle
* ✅ **AC04**: Componentes com JS (ex: countdown, tracking de clique) devem funcionar normalmente após exportação
* ✅ **AC05**: Fontes externas como Google Fonts devem ser carregadas corretamente sem depender de recursos da plataforma

## Histórico de status
- Backlog (backlog): 2025-07-28T19:02:16.815Z → 2025-07-30T16:57:20.927Z
- To-do (unstarted): 2025-07-30T16:57:20.927Z → 2025-08-11T13:52:59.691Z
- Released (completed): 2025-08-11T13:52:59.691Z → atual

## Relações
—

## Anexos
—
