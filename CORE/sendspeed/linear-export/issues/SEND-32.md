# SEND-32 — [5] Visualizar Usuários no Funil de Conversão

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | High |
| Responsável | Hugo Fernandes |
| Time | Sendspeed |
| Projeto | — |
| Labels | — |
| Parent | — |
| Criada | 2025-06-25T13:40:47.670Z por bruno.heidrich@sendspeed.com |
| Iniciada | 2025-07-10T12:13:46.682Z |
| Concluída | 2025-09-04T19:36:48.783Z |
| Arquivada | 2026-03-12T01:50:30.666Z |
| Vencimento | — |
| Branch | hugofernandes/send-32-5-visualizar-usuarios-no-funil-de-conversao |
| URL | https://linear.app/sendspeed/issue/SEND-32/5-visualizar-usuarios-no-funil-de-conversao |

## Descrição

**Como** Customer Success Manager

**Eu quero** ver a lista de usuários que passaram pelo funil de um card

**Para que** eu possa entender os padrões de comportamento dos clientes em potencial e identificar oportunidades de re-engajamento

**Critérios de Aceitação:**

- [ ] Devo ver lista paginada de usuários do funil
- [ ] Cada usuário deve mos,strar: etapa alcançada, timestamp dispositivo
- [ ] Devo poder filtrar por etapa específica (impressão, preview, CTA)
- [ ] Devo poder filtrar por dispositivo e localização
- [ ] Devo poder ver apenas convertidos ou não convertidos (CTA ou não CTA)
- [ ] Tempos de permanência em cada etapa devem ser visíveis
- [ ] Distinção clara entre usuários anônimos e identificados

### Query

* através dos usuários que tem um "click-preview-card" com id do evento "x"
* tentar trazer as etapas que o usuário percorreu nesse card: 1 e ultima ação
* Tempo na sessão: do início da exibição do card ao click ou se o usuário não fez nada
  * URL_REFERRER vazia pode indicar a pagina inicial

> **[Imagem 1 — transcrição]:** Screenshot de UI — painel "Jornada dos Usuários (150)". No topo, campo de busca "Buscar por ID do usuário..." e botão "Filtros"; à direita "150 de 150 usuários". Lista de cards de usuários, todos rotulados "Usuário Anônimo" com IDs sequenciais (anon_0, anon_1, anon_2, ...). Cada linha exibe: tags coloridas (verde) indicando as etapas do funil alcançadas (Impressão, Preview, CTA, Conversão), texto "Último passo: <etapa>" com ícone, o tipo de dispositivo à direita (Tablet ou Desktop) e a duração da sessão (ex: "166s sessão"). Exemplos visíveis: anon_0 (Impressão, Preview, CTA, Conversão; último passo: conversões; Tablet; 166s), anon_1 (Impressão; último passo: impressões; Desktop; 198s), anon_2 (todas as 4 etapas; conversões; Tablet; 54s), anon_3 (Impressão, Preview, CTA; último passo: cta; Tablet; 101s), anon_4 (Impressão; impressões; Tablet; 64s), anon_5 (4 etapas; conversões; Tablet; 286s), anon_6 (Impressão, Preview, CTA; cta; Tablet; 157s). Demonstra a lista paginada de usuários no funil com etapa alcançada, dispositivo e tempo de sessão.

## Histórico de status

- Backlog (backlog): 2025-06-25T13:40:47.670Z → 2025-07-10T12:13:46.668Z
- Pull Request (started): 2025-07-10T12:13:46.668Z → 2025-07-21T12:37:03.084Z
- In Progress (started): 2025-07-21T12:37:03.084Z → 2025-07-31T12:28:06.906Z
- Pull Request (started): 2025-07-31T12:28:06.906Z → 2025-08-11T13:53:54.220Z
- Product Review (started): 2025-08-11T13:53:54.220Z → 2025-08-13T22:11:34.359Z
- Pull Request (started): 2025-08-13T22:11:34.359Z → 2025-08-25T12:15:37.996Z
- Product Review (started): 2025-08-25T12:15:37.996Z → 2025-08-27T15:25:04.130Z
- Pull Request (started): 2025-08-27T15:25:04.130Z → 2025-09-04T19:36:48.912Z
- Released (completed): 2025-09-04T19:36:48.912Z → atual

## Relações

—

## Anexos

—
