# SEND-349 — Bugs Ontologia UserIn - Cards de Grupos abrem tela geral em vez de tela específica

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | High |
| Responsável | paulo.ribeiro@sendspeed.com |
| Time | Sendspeed |
| Projeto | — |
| Labels | UserIn, User Story, Melhoria |
| Parent | — |
| Criada | 2026-02-24T14:26:00.650Z por paulo.ribeiro@sendspeed.com |
| Iniciada | 2026-03-02T17:26:08.240Z |
| Concluída | 2026-03-09T14:15:02.980Z |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-349-bugs-ontologia-userin-cards-de-grupos-abrem-tela-geral-em |
| URL | https://linear.app/sendspeed/issue/SEND-349/bugs-ontologia-userin-cards-de-grupos-abrem-tela-geral-em-vez-de-tela |

## Descrição

**Descrição:** Quando o usuário clica nos cards de "Grupos da ontologia" (como Identidade, Ciclo de Vida, Temporal, Financeiro, Comportamento, Preferências, etc.), eles abrem a tela geral de ontologia em vez de abrir a tela específica de cada grupo/ontologia. O usuário espera ver os detalhes e campos específicos daquele grupo quando clica, mas é redirecionado para a página geral, perdendo o contexto e dificultando o acesso direto às informações desejadas.

> **[Imagem 1 — transcrição]:** Screenshot de UI mostrando a grade **"Grupos da ontologia (45)"** com botão "Ver todos os campos →" no canto superior direito. Cards em grade (cada um com ícone, título, descrição e contagem de campos): **Identidade** (Quem é o utilizador, 8 campos); **Ciclo de Vida** (Fase da jornada do utilizador, 6 campos); **Temporal** (Quando o utilizador entra e melhor horário de contacto, 7 campos); **Financeiro** (Quanto o utilizador gasta - depósitos/compras, 31 campos); **Comportamento** (Como o utilizador se comporta - sessões, engagement, 21 campos); **Preferências** (O que o utilizador gosta - jogos, categorias, páginas, 12 campos); **Navegação** (Dados de navegação e páginas visitadas, 7 campos); **Intenção** (Probabilidade de conversão - score e nível, 3 campos); **Saldo Tempo Real** (Monitoramento de saldo na sessão, 9 campos); **Tags** (Rótulos dinâmicos aplicados ao utilizador, 1 campos); **Relacionamentos** (Ligacoes com objetos - Contact, Game, Product, 2 campos); **Contact** (Atributos do contacto CRM linkado, 4 campos); **Game** (Atributos do objeto Game - iGaming, 6 campos); **activity** (4 campos); **ai** (1 campos); **ai_metadata** (3 campos); **churn** (5 campos); **churn_prediction** (2 campos); **conversion** (2 campos); **deposits** (8 campos); **devices** (1 campos); **diversity** (1 campos); **early_warning** (5 campos); **favorites** (3 campos).

> **[Imagem 2 — transcrição]:** Screenshot de UI (recorte) da tela **UserProfile** com o banner roxo/Core e a métrica **86 Campos**. Abas: Explorador (ativa), Relacionamentos, + Campos... Abaixo, um card cinza escuro **"Identidade — 8 campos"** com seta de expandir (↗) no canto, texto "Quem é o utilizador" e chips **7 Atributos**, **1 Output**. Ilustra o card de grupo que ao ser clicado abre a tela geral em vez da específica.

> **[Imagem 3 — transcrição]:** Screenshot de UI da tela UserProfile — barra de abas (Explorador ativa, Relacionamentos, + Campos Custom, Ingestão) e filtros de categoria: Todos, **Identidade** (selecionado, azul), Ciclo de Vida, Temporal, Financeiro, Comportamento, Preferências, Navegação, Intenção, Saldo Tempo Real, Tags. Linha "Tipo:" com chips Atributos, Agregados, Sinais, Outputs, AI Scoring; à direita "8 campos". Lista de campos: **ID da Empresa** (companyId) badge Atributo; **ID Externo** (externalId) badge Atributo; **Risco de Jogo Problemático** (outputs.responsible_gaming_risk) badges Output + Custom.

**Sugestão de melhoria:** Fazer com que cada card de grupo de ontologia redirecione para a tela específica daquele grupo, mostrando seus campos, atributos e configurações relacionadas. Isso melhora a navegação e permite acesso direto às informações desejadas sem precisar navegar manualmente até o grupo específico.

## Histórico de status
- Backlog (backlog): 2026-02-24T14:26:00.650Z → 2026-02-24T15:36:33.510Z
- Refining (backlog): 2026-02-24T15:36:33.510Z → 2026-03-02T12:27:43.096Z
- To-do (unstarted): 2026-03-02T12:27:43.096Z → 2026-03-02T17:26:08.254Z
- In Progress (started): 2026-03-02T17:26:08.254Z → 2026-03-03T12:12:15.436Z
- Pull Request (started): 2026-03-03T12:12:15.436Z → 2026-03-03T12:50:08.731Z
- Product Review (started): 2026-03-03T12:50:08.731Z → 2026-03-09T14:15:02.993Z
- Released (completed): 2026-03-09T14:15:02.993Z → atual

## Relações
—

## Anexos
—
