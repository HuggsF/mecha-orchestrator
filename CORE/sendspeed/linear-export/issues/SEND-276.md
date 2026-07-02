# SEND-276 — Compilação de algumas informações do userin_hooks + events

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | Urgent |
| Responsável | Vinicius Carneiro |
| Time | Sendspeed |
| Projeto | — |
| Labels | User Story, UserIn, Implementação |
| Parent | — |
| Criada | 2026-01-07T14:35:49.406Z por Vinicius Carneiro |
| Iniciada | 2026-01-07T16:52:36.818Z |
| Concluída | 2026-01-15T13:36:37.624Z |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-276-compilacao-de-algumas-informacoes-do-userin_hooks-events |
| URL | https://linear.app/sendspeed/issue/SEND-276/compilacao-de-algumas-informacoes-do-userin-hooks-events |

## Descrição

> Como Product Owner
>
> Quero conseguir juntar todas as informações em um lugar só
>
> Para facilitar a busca e assimilação de alguns dados

---

## Critérios de aceite:

* Os dados do webhook antes de gravar no userin_hooks, quando o não for de registro, ele vai precisar pegar o ultimo evento baseado no createdAt procurando pelo externalUserId.
* Quando encontrado vamos copiar o localStorageId, sessionId e substituir todo o conteúdo do metadata pelo conteúdo do url_params em events antes de gravar.
* Vamos gravar com essas informações junto no userin_hooks - caso não encontre, vamos gravar normalmente sem os dados.

> **[Imagem 1 — transcrição]:** Screenshot de um documento MongoDB (evento do tipo `pageshow`/`PAGE_VIEW`) exibido em visualizador JSON com numeração de linhas. Campos visíveis: `_id: ObjectId('695e61f481709dcc1065e9a0')`; `apiKey: "2485c99d-92fd-47c8-80b3-b2a067ed36f9"`; `deviceFingerprint: "642ab369bba2ae3e723cc0f4c7d879790243bddb67b54e8cb8a696d64ab07039"`; `deviceInfo: Object`; `localstorageId: "SmartTrack__local_nx0nn8xb7omjiif207"` (destacado com retângulo vermelho); `sessionId: "sess_4c1312c9-2976-40f7-9ad3-770ea09df029"` (destacado com retângulo vermelho); `visitorId: "694a7ecba5910814e705f70f"`; `companyId: "69304041c480d72ece530d0f"`; `externalUserId: "34286092"`; `referrer: null`; `url: "https://bullsbet.bet.br/?utm_ui=userin_teste_depoisito&utm_campaign=us"`; `url_params: Object` (destacado com retângulo vermelho); `title: "Bullsbet Cassino e Apostas Online - Apostas Esportivas e Cassino ao Vi"`; `originalEventType: "PAGE_VIEW"`; `type: "pageshow"`; `metadata: Object`; `epoch_time: 1767793132905`; `createdAt: 2026-01-07T10:38:52.000+00:00`; `receivedAt: 2026-01-07T10:39:00.000+00:00`. Demonstra a origem dos campos (localstorageId, sessionId, url_params) que devem ser copiados do evento para o registro em userin_hooks.

> **[Imagem 2 — transcrição]:** Screenshot de um documento MongoDB (registro de webhook do tipo `first_deposit`) em visualizador JSON com numeração de linhas. Campos visíveis: `_id: ObjectId('695e5ea7669ffdee266aca9f')`; `source: "sevenproxy"`; `externalId: "34286092"`; `companyId: "69304041c480d72ece530d0f"`; `type: "first_deposit"`; `__v: 0`; `createdAt: 2026-01-07T13:24:55.365+00:00`; `metadata: Object`; `updatedAt: 2026-01-07T13:24:55.365+00:00`. Na parte inferior, destacados com retângulos vermelhos, aparecem os campos a serem adicionados/gravados: `localstorageId: "SmartTrack__local_nx0nn8xb7omjiif207"`, `sessionId: "sess_4c1312c9-2976-40f7-9ad3-770ea09df029"` e `url_params: Object`. Demonstra o resultado esperado: o registro do webhook (first_deposit) enriquecido com os dados copiados do último evento correspondente ao externalUserId.

## Cenário de teste:

- [ ] Entrar no banco de dados.
- [ ] Consultar no banco de dados os dados.
- [ ] As informações devem bater.

## Histórico de status
- Backlog (backlog): 2026-01-07T14:35:49.406Z → 2026-01-07T14:35:53.058Z
- To-do (unstarted): 2026-01-07T14:35:53.058Z → 2026-01-07T16:52:36.829Z
- In Progress (started): 2026-01-07T16:52:36.829Z → 2026-01-08T16:13:17.518Z
- Product Review (started): 2026-01-08T16:13:17.518Z → 2026-01-15T13:36:37.636Z
- Released (completed): 2026-01-15T13:36:37.636Z → atual

## Relações
—

## Anexos
—
