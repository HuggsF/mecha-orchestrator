# SEND-416 — Implementação das telas de Componentes UserIn - Cards, Modais, Smart Blocks e Mini Games

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | Medium |
| Responsável | paulo.ribeiro@sendspeed.com |
| Time | Sendspeed |
| Projeto | — |
| Labels | — |
| Parent | — |
| Criada | 2026-03-20T13:17:39.518Z por paulo.ribeiro@sendspeed.com |
| Iniciada | 2026-04-15T21:20:04.018Z |
| Concluída | 2026-05-08T19:28:27.206Z |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-416-implementacao-das-telas-de-componentes-userin-cards-modais |
| URL | https://linear.app/sendspeed/issue/SEND-416/implementacao-das-telas-de-componentes-userin-cards-modais-smart |

## Descrição

**Descrição:** Implementar as telas de listagem e criação para os componentes do sistema: Cards, Modais, Smart Blocks e Mini Games. As telas seguem padrão visual consistente com visualização em grid e lista, filtros, busca e ações rápidas.

**Funcionalidades necessárias:**

**Estrutura geral (aplicável a todas as telas):**

* Header com título e botão de criação
* Barra de busca e filtros (status, prioridades, data)
* Toggle Grid/Lista
* Paginação
* Badges de status
* Menu de ações (Editar, Analytics, Arquivar, Pausar, Deletar)

**Visualização Grid:** Cards visuais com thumbnail, título, badges, botões de ação.

**Visualização Lista:** Tabela com colunas: Nome, Impressões, CTA, CTR, Fechamentos, Tempo Médio, Ações.

**Tela de criação Mini Games:** Modal com seleção de tipos (Roleta, Raspadinha, Caixa Misteriosa, Slot Machine, Prize Drop, Vira a Carta).

---

## 🎯 Priorização RICE — Score: 4.0 (#25 no To-do)

| Reach | Impact | Confidence | Effort | Score |
| -- | -- | -- | -- | -- |
| 10 | 2 (high) | 60% | 3 meses | **4.0** |

**Justificativa:** Reach 10: todos os usuários da plataforma precisarão gerenciar componentes. Impacto high (2): habilita gestão visual de modais, cards, blocks e mini games. Confidence 60%: designs no Figma existem mas escopo é amplo e pode mudar. Esforço 3 meses: 4 telas completas com grid/lista, filtros, ações, paginação e modais de criação.

## Histórico de status
- Backlog (backlog): 2026-03-20T13:17:39.518Z → 2026-03-20T13:17:53.079Z
- Refining (backlog): 2026-03-20T13:17:53.079Z → 2026-03-31T14:49:12.198Z
- To-do (unstarted): 2026-03-31T14:49:12.198Z → 2026-04-15T21:20:04.030Z
- In Progress (started): 2026-04-15T21:20:04.030Z → 2026-04-17T18:03:07.643Z
- Pull Request (started): 2026-04-17T18:03:07.643Z → 2026-04-20T13:54:09.193Z
- Product Review (started): 2026-04-20T13:54:09.193Z → 2026-05-08T19:28:27.218Z
- Released (completed): 2026-05-08T19:28:27.218Z → atual

## Relações
—

## Anexos
- Fix/send 416 telas componentes — https://github.com/sendspeed0/sendspeed-engage-ai-flow-08/pull/45
- Fix/send 416 telas componentes — https://github.com/sendspeed0/sendspeed-engage-ai-flow-08/pull/44
