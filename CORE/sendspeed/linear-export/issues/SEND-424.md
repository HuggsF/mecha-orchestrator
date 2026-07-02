# SEND-424 — 🐞 Autosave pergunta se quer salvar ao sair

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | Urgent |
| Responsável | — |
| Time | Sendspeed |
| Projeto | — |
| Labels | User Story, UserIn, Bug |
| Parent | — |
| Criada | 2026-03-23T13:06:06.119Z por Vinicius Carneiro |
| Iniciada | 2026-03-31T18:31:43.514Z |
| Concluída | 2026-04-14T15:15:43.706Z |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-424-autosave-pergunta-se-quer-salvar-ao-sair |
| URL | https://linear.app/sendspeed/issue/SEND-424/autosave-pergunta-se-quer-salvar-ao-sair |

## Descrição

## 📍 Onde ocorre

Editor de Jornadas (e possivelmente outros editores com autosave)

## 🔁 Passo a Passo

1. Acessar o editor de Jornadas
2. Fazer qualquer alteração
3. Aguardar o autosave salvar automaticamente
4. Tentar sair da página

## ❌ Resultado Atual

Aparece um modal perguntando se o usuário deseja salvar as alterações, mesmo com o autosave já tendo salvado.

## ✅ Resultado Esperado

Não deve aparecer nenhum modal ao sair, pois as alterações já foram salvas automaticamente pelo autosave.

---

## 🎯 Priorização RICE — Score: 16.0 (#7 no To-do)

| Reach | Impact | Confidence | Effort | Score |
| -- | -- | -- | -- | -- |
| 10 | 1 (medium) | 80% | 0.5 meses | **16.0** |

**Justificativa:** Mesmo problema do SEND-417 mas reportado especificamente para Smart Modals. Reach 10: todos os usuários editando conteúdo são afetados. Impacto medium (1): fricção constante ao sair, mas não bloqueia. Confidence 80%: problema de estado entre autosave e dirty flag. Esforço 0.5 meses. Pode ser resolvido junto com SEND-417.

## Histórico de status
- Backlog (backlog): 2026-03-23T13:06:06.119Z → 2026-03-24T18:25:54.282Z
- Refining (backlog): 2026-03-24T18:25:54.282Z → 2026-03-31T12:33:18.723Z
- To-do (unstarted): 2026-03-31T12:33:18.723Z → 2026-03-31T18:31:43.543Z
- In Progress (started): 2026-03-31T18:31:43.543Z → 2026-03-31T18:55:20.664Z
- Product Review (started): 2026-03-31T18:55:20.664Z → 2026-04-14T15:15:43.720Z
- Released (completed): 2026-04-14T15:15:43.720Z → atual

## Relações
—

## Anexos
—
