# SEND-431 — RCS - Remover seletor de tamanho individual de cada card do carrossel

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | High |
| Responsável | — |
| Time | Sendspeed |
| Projeto | — |
| Labels | — |
| Parent | — |
| Criada | 2026-03-26T12:18:43.057Z por paulo.ribeiro@sendspeed.com |
| Iniciada | — |
| Concluída | 2026-06-22T17:16:38.413Z |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-431-rcs-remover-seletor-de-tamanho-individual-de-cada-card-do |
| URL | https://linear.app/sendspeed/issue/SEND-431/rcs-remover-seletor-de-tamanho-individual-de-cada-card-do-carrossel |

## Descrição

## **Problema**

Dentro de cada card do carrossel existe um select de tamanho ("Pequeno"/"Médio"/"Grande") que permite alterar individualmente. Segundo a spec do Google RCS, a largura é uma propriedade do carrossel inteiro — não existe tamanho por card.

## **O que corrigir**

1. **Remover** o select de tamanho de dentro de cada card individual
2. **Renomear** o select global de "Largura do cartão" para **"Largura dos cartões"**
3. Manter apenas o select global que já existe acima da lista de cards

---

## 🎯 Priorização RICE — Score: 12.0 (#13 no To-do)

| Reach | Impact | Confidence | Effort | Score |
| -- | -- | -- | -- | -- |
| 6 | 0.5 (low) | 100% | 0.25 meses | **12.0** |

**Justificativa:** Quick win de compliance com spec Google RCS. Reach 6: usuários do editor de carrossel RCS. Impacto low (0.5): não quebra funcionalidade, mas gera confusão e pode causar comportamento inesperado no envio. Confidence 100%: fix trivial (remover 1 select, renomear label). Esforço mínimo.

## Histórico de status
- Backlog (backlog): 2026-03-26T12:18:43.057Z → 2026-03-26T12:18:52.906Z
- Refining (backlog): 2026-03-26T12:18:52.906Z → 2026-03-31T12:33:37.895Z
- To-do (unstarted): 2026-03-31T12:33:37.895Z → 2026-06-22T17:16:38.428Z
- Released (completed): 2026-06-22T17:16:38.428Z → atual

## Relações
—

## Anexos
—
