# SEND-513 — 2. Incluir o total cobrado no relatório

| Campo | Valor |
| -- | -- |
| Status | To-do (unstarted) |
| Prioridade | No priority |
| Responsável | — |
| Time | Sendspeed |
| Projeto | — |
| Labels | Sendspeed |
| Parent | — |
| Criada | 2026-06-22T17:38:53.753Z por Vinicius Carneiro |
| Iniciada | — |
| Concluída | — |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-513-2-incluir-o-total-cobrado-no-relatorio |
| URL | https://linear.app/sendspeed/issue/SEND-513/2-incluir-o-total-cobrado-no-relatorio |

## Descrição

**Como** usuário do relatório de disparos (iTeams / SS Control)

**Quero** poder incluir o total cobrado do recorte consultado

**Para** entender a cobrança consolidada de um período/filtro sem somar manualmente

### 📈 Use Case

O relatório não mostra o total cobrado. Usando o valor por mensagem da US1, adiciona-se a opção de exibir o total cobrado do recorte (respeitando os filtros). É opcional porque a informação pode ser sensível e nem todo consumo do relatório precisa dela.

### ✅ Critérios de aceite

* O relatório oferece a opção de incluir o total cobrado = somatório do valor cobrado por mensagem (US1), no front de iTeams e SS Control
* Sem a opção ativada, o relatório se comporta como hoje
* O total respeita todos os filtros aplicados (período, canal, cliente, status)
* Total exibido com precisão/arredondamento definidos
* Recorte com mensagens sem valor (lacuna da US1) → total marcado como parcial, sem somar errado em silêncio

### 🧩 Cenários de teste

* Relatório sem a opção → comportamento atual inalterado
* Ativar a opção → total = soma do valor cobrado das mensagens do recorte
* Trocar filtro → total recalcula coerente
* Período com mensagens sem valor → total marcado como parcial
* Exportação (se existir) reflete o total

## Histórico de status
- To-do (unstarted): 2026-06-22T17:38:53.753Z → atual

## Relações
—

## Anexos
—
