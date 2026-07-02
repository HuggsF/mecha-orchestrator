# SEND-514 — 3. Aumentar o filtro de período do relatório para até 30 dias

| Campo | Valor |
| -- | -- |
| Status | To-do (unstarted) |
| Prioridade | No priority |
| Responsável | — |
| Time | Sendspeed |
| Projeto | — |
| Labels | Sendspeed |
| Parent | — |
| Criada | 2026-06-22T17:39:29.909Z por Vinicius Carneiro |
| Iniciada | — |
| Concluída | — |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-514-3-aumentar-o-filtro-de-periodo-do-relatorio-para-ate-30-dias |
| URL | https://linear.app/sendspeed/issue/SEND-514/3-aumentar-o-filtro-de-periodo-do-relatorio-para-ate-30-dias |

## Descrição

**Como** usuário do relatório de disparos (iTeams / SS Control)

**Quero** filtrar por um intervalo de até 30 dias

**Para** analisar um ciclo mensal completo de disparo/cobrança em uma consulta só

### 📈 Use Case

O teto do filtro de período é baixo demais para um ciclo mensal fechado. Subir para 30 dias cobre o ciclo. A mudança parece trivial, mas o risco real é performance: 30 dias com o total cobrado ligado (US2) é o cenário que estoura — por isso o SLA é critério, não detalhe.

### ✅ Critérios de aceite

* O filtro aceita intervalo de até 30 dias [confirmar: máximo atual], no front de iTeams e SS Control
* Intervalos acima de 30 dias são bloqueados com mensagem clara (não erro genérico)
* Consulta de 30 dias responde dentro de um limite aceitável [decidir: SLA/timeout], inclusive com o total cobrado ativado
* Comportamento consistente entre os dois consumidores

### 🧩 Cenários de teste

* Selecionar exatamente 30 dias → relatório retorna
* Selecionar 31 dias → bloqueado com mensagem clara
* 30 dias com total cobrado ligado → responde dentro do SLA, sem timeout
* Cliente de alto volume em 30 dias → sem degradação inaceitável (definir baseline)

## Histórico de status
- To-do (unstarted): 2026-06-22T17:39:29.909Z → atual

## Relações
—

## Anexos
—
