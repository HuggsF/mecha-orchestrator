# SEND-433 — Bug: Remover Objetivo da Jornada

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | Urgent |
| Responsável | Hugo Fernandes |
| Time | Sendspeed |
| Projeto | — |
| Labels | UserIn |
| Parent | — |
| Criada | 2026-03-30T18:01:08.924Z por paulo.ribeiro@sendspeed.com |
| Iniciada | 2026-03-31T18:30:48.817Z |
| Concluída | 2026-06-22T17:15:57.236Z |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-433-bug-remover-objetivo-da-jornada |
| URL | https://linear.app/sendspeed/issue/SEND-433/bug-remover-objetivo-da-jornada |

## Descrição

## **Descrição**

Ao selecionar **"Sem objetivo definido"** no modal de objetivo de uma jornada e salvar, o objetivo não é de fato removido. Ao recarregar a página, o objetivo anterior reaparece.

## **Passos para Reproduzir**

1. Abrir uma jornada que já tenha um objetivo vinculado (ex: "Registrar Usuário")
2. Clicar no badge do objetivo no header da jornada
3. No modal, selecionar **"Sem objetivo definido"** (🚫)
4. Salvar a jornada
5. Recarregar a página

**Resultado atual:** O objetivo anterior ("Registrar Usuário") volta a aparecer.

**Resultado esperado:** A jornada deveria ficar sem objetivo vinculado.

## **Critérios de Aceitação**

- [ ] Selecionar "Sem objetivo definido" e salvar persiste a remoção do objetivo
- [ ] Após recarregar, a jornada continua sem objetivo vinculado
- [ ] Vincular um novo objetivo após remover funciona normalmente

---

## 🎯 Priorização RICE — Score: 16.0 (#8 no To-do)

| Reach | Impact | Confidence | Effort | Score |
| -- | -- | -- | -- | -- |
| 8 | 0.5 (low) | 100% | 0.25 meses | **16.0** |

**Justificativa:** Reach 8: qualquer usuário editando objetivos de jornada. Impacto low (0.5): não impede o uso da jornada, mas a remoção de objetivo simplesmente não funciona. Confidence 100%: bug reprodutível e trivial — o save provavelmente não envia `null` ou string vazia para o campo `objective`. Esforço mínimo (0.25 meses): fix no payload de save ou na API de update da jornada.

## Histórico de status
- Refining (backlog): 2026-03-30T18:01:08.924Z → 2026-03-31T14:49:10.928Z
- To-do (unstarted): 2026-03-31T14:49:10.928Z → 2026-03-31T18:30:48.922Z
- In Progress (started): 2026-03-31T18:30:48.922Z → 2026-06-22T17:15:57.246Z
- Released (completed): 2026-06-22T17:15:57.246Z → atual

## Relações
—

## Anexos
—
