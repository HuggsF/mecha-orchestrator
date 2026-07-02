# SEND-417 — 🐞 - AutoSave do Journey Builder desativado por padrão e modal de salvar aparece incorretamente

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | Urgent |
| Responsável | — |
| Time | Sendspeed |
| Projeto | — |
| Labels | Bug, Jornadas, UserIn, User Story |
| Parent | — |
| Criada | 2026-03-20T13:17:43.033Z por Vinicius Carneiro |
| Iniciada | 2026-03-31T18:31:44.316Z |
| Concluída | 2026-04-14T15:14:46.136Z |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-417--autosave-do-journey-builder-desativado-por-padrao-e-modal |
| URL | https://linear.app/sendspeed/issue/SEND-417/autosave-do-journey-builder-desativado-por-padrao-e-modal-de-salvar |

## Descrição

## 📍 Onde ocorre

**Frontend** — Journey Builder, cabeçalho com toggle "Auto" e modal "Alterações não salvas" (`sendspeed-engage-ai-flow-08`).

---

## 🔁 Passo a Passo

1. Acessar a plataforma Userin > Jornadas.
2. Abrir uma jornada existente ou criar uma nova.
3. Observar que o toggle **"Auto"** (AutoSave) vem **desativado** por padrão.
4. Fazer alterações na jornada (mover nó, editar configuração, etc.).
5. Tentar sair da jornada (voltar para lista).
6. Modal **"Alterações não salvas"** aparece, mesmo quando o AutoSave está ativado e já salvou as alterações.

---

## ❌ Resultado Atual

**Problema 1 — AutoSave desativado por padrão:**
O toggle "Auto" inicia sempre como desativado. O usuário precisa ativar manualmente a cada vez que abre o editor.

**Problema 2 — Modal de "Alterações não salvas" aparece mesmo com AutoSave ativo:**
Quando o AutoSave está ativado e salvando automaticamente cada mudança, o modal "Alterações não salvas" ainda aparece ao sair da jornada. Se o AutoSave está funcionando corretamente, não existem alterações não salvas e o modal não deveria ser exibido.

---

## ✅ Resultado Esperado

* O toggle **"Auto" deve vir ativado por padrão** ao abrir o Journey Builder.
* Quando o AutoSave está **ativado** e a jornada já foi salva automaticamente, o modal "Alterações não salvas" **NÃO deve aparecer** ao sair.
* O modal só deve aparecer quando o AutoSave está **desativado** e existem alterações pendentes.

---

## 🧪 Evidências

* Toggle "Auto" vem desativado por padrão no cabeçalho do Journey Builder.
* Modal "Alterações não salvas" aparece ao sair mesmo com AutoSave ativo.
* Prints anexados mostram o comportamento na interface.

---

## 🎯 Priorização RICE — Score: 16.0 (#3 no To-do)

| Reach | Impact | Confidence | Effort | Score |
| -- | -- | -- | -- | -- |
| 10 | 1 (medium) | 80% | 0.5 meses | **16.0** |

**Justificativa:** Afeta todos os usuários do Journey Builder (Reach 10) em toda sessão de edição. Impacto médio: não bloqueia o trabalho, mas gera fricção constante (ativar toggle manualmente, fechar modal desnecessário) e risco de perda de trabalho quando o usuário esquece de ativar o AutoSave. Confidence 80% porque o problema é visível e o fix envolve estado do toggle + lógica do modal. Esforço de \~2 semanas entre frontend e testes.

## Histórico de status
- Backlog (backlog): 2026-03-20T13:17:43.033Z → 2026-03-20T13:19:25.573Z
- Refining (backlog): 2026-03-20T13:19:25.573Z → 2026-03-31T12:33:20.020Z
- To-do (unstarted): 2026-03-31T12:33:20.020Z → 2026-03-31T18:31:44.333Z
- In Progress (started): 2026-03-31T18:31:44.333Z → 2026-03-31T18:55:18.391Z
- Product Review (started): 2026-03-31T18:55:18.391Z → 2026-04-14T15:14:46.158Z
- Released (completed): 2026-04-14T15:14:46.158Z → atual

## Relações
—

## Anexos
—
