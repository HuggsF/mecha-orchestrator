# SEND-512 — 1. Propagar o valor cobrado do cliente por mensagem na consulta de dados

| Campo | Valor |
| -- | -- |
| Status | To-do (unstarted) |
| Prioridade | No priority |
| Responsável | — |
| Time | Sendspeed |
| Projeto | — |
| Labels | Sendspeed |
| Parent | — |
| Criada | 2026-06-22T17:37:44.501Z por Vinicius Carneiro |
| Iniciada | — |
| Concluída | — |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-512-1-propagar-o-valor-cobrado-do-cliente-por-mensagem-na |
| URL | https://linear.app/sendspeed/issue/SEND-512/1-propagar-o-valor-cobrado-do-cliente-por-mensagem-na-consulta-de |

## Descrição

**Como** time/cliente que consulta dados de disparo da SendSpeed

**Quero** que cada mensagem disparada carregue o valor cobrado do cliente, na API e no front

**Para** analisar quanto cada disparo gerou de cobrança, por mensagem

### 📈 Use Case

A consulta de dados não expõe o valor cobrado por mensagem até iTeams/SS Control, base necessária para o total cobrado da US2. O valor vem da tabela de valor praticado por cliente já existente; esta story garante que ele seja atribuído por mensagem e propagado de ponta a ponta até a API e o front dos dois consumidores.

### ✅ Critérios de aceite

* O valor cobrado de cada mensagem é obtido da tabela de valor praticado por cliente
* O valor reflete a granularidade real da tabela (por canal/segmento se houver) [confirmar: a tabela varia por canal e por segmento de SMS, ou é valor único por cliente?]
* Valor propagado de forma consistente: disparo → persistência → API → front (mesmo número nos dois consumidores)
* Mensagens disparadas antes desta US ficam sem valor e são sinalizadas como lacuna (sem backfill), nunca como zero
* Mensagem de cliente sem valor na tabela é sinalizada, não some nem zera

### 🧩 Cenários de teste

* Mensagem de cliente com valor na tabela → valor correto na API e no front
* Mesma mensagem em iTeams e SS Control → valor idêntico
* SMS multi-segmento → valor coerente com a regra da tabela [depende da granularidade confirmada]
* RCS → valor coerente com a regra da tabela [depende da granularidade confirmada]
* Mensagem anterior à US → exibida com lacuna sinalizada
* Cliente sem valor cadastrado na tabela → sinalizado

## Histórico de status
- To-do (unstarted): 2026-06-22T17:37:44.501Z → atual

## Relações
—

## Anexos
—
