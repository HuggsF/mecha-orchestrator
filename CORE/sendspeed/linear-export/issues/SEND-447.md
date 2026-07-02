# SEND-447 — Barra de filtros e paginação — Journey Builder e Journey Analytics

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | Medium |
| Responsável | paulo.ribeiro@sendspeed.com |
| Time | Sendspeed |
| Projeto | — |
| Labels | — |
| Parent | — |
| Criada | 2026-04-09T10:37:23.950Z por paulo.ribeiro@sendspeed.com |
| Iniciada | 2026-04-10T15:50:54.107Z |
| Concluída | 2026-05-08T18:08:06.195Z |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-447-barra-de-filtros-e-paginacao-journey-builder-e-journey |
| URL | https://linear.app/sendspeed/issue/SEND-447/barra-de-filtros-e-paginacao-journey-builder-e-journey-analytics |

## Descrição

**Descrição:**

Implementação de barra de filtros avançada e paginação nas telas de listagem de jornadas e analytics, melhorando a usabilidade para empresas com muitas jornadas.

**O que foi feito:**

* `/journey-builder` — Substituído o filtro simples de tipo por uma barra completa com: busca por nome (debounce 300ms), filtro de status, tipo, objetivo da jornada e período (data de criação). Paginação de 10 itens por página com reset automático ao mudar filtros.
* `/journey-analytics` — Adicionada paginação de 10 itens por página à lista de jornadas existente, com o mesmo visual.
* **Componente de paginação** (`JourneyPagination`) criado como componente compartilhado, seguindo o design do Figma: botões quadrados arredondados, página ativa em azul sólido `#0020E7`, hover com fundo `#E5E9FD`.
* **Calendário** (`AdvancedDateRangePicker`) utilizado como filtro de período em ambas as páginas.

**Branch:** `fix/send-447-filter-bar-journey-analytics` **Commits:** `1669584`, `b629004`

## Histórico de status
- Backlog (backlog): 2026-04-09T10:37:23.950Z → 2026-04-10T15:50:54.119Z
- Pull Request (started): 2026-04-10T15:50:54.119Z → 2026-04-13T13:01:27.598Z
- Product Review (started): 2026-04-13T13:01:27.598Z → 2026-05-08T18:08:06.212Z
- Released (completed): 2026-05-08T18:08:06.212Z → atual

## Relações
—

## Anexos
- Fix/send 447 filter bar journey analytics — https://github.com/sendspeed0/sendspeed-engage-ai-flow-08/pull/39
