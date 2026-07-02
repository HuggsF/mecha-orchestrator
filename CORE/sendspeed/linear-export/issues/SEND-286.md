# SEND-286 — Subir regras novas relacionadas aos segmentos

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | Urgent |
| Responsável | pedro.iegler@sendspeed.com |
| Time | Sendspeed |
| Projeto | — |
| Labels | Regras, User Story, UserIn, Implementação |
| Parent | — |
| Criada | 2026-01-27T14:12:10.220Z por Vinicius Carneiro |
| Iniciada | 2026-01-27T20:15:35.512Z |
| Concluída | 2026-02-12T14:55:56.991Z |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-286-subir-regras-novas-relacionadas-aos-segmentos |
| URL | https://linear.app/sendspeed/issue/SEND-286/subir-regras-novas-relacionadas-aos-segmentos |

## Descrição

> Como PO
>
> Quero integrar o sistema de segmentação ao sistema de regras
>
> Para ter uma maior diversidade nos gatilhos de engajamento com o usuário.

---

# Critérios de aceite

* Subir o novo sistema de regras para produção de maneira 100% funcional.
* O critério de sucesso é as regras baterem no site.

**Muito importante:**

* Toda vez que um usuário entra no site, vamos precisar pegar as informações na collection profile no banco de dados e baixar para user_profile do localstorage do usuário sem alterar a atualização do balance amount (saldo) da sessão.
> **[Imagem 1 — transcrição]:** Screenshot de UI (com barra de tarefas do Windows visível na parte inferior, data 26/01/2026) mostrando o painel "Defina as..." (Defina as Condições da Regra) com um dropdown aberto de tipos de condição. As opções do dropdown são: "Visualização da página", "Clicou", "Elemento visível", "Acesso", "Atributo de Perfil" (destacado/selecionado em laranja, com ícone de pessoa), "Tem Tag" (com ícone de etiqueta). Abaixo há um seletor "AND", badge "1 condição total", e uma linha de condição 1 com dropdown "Selecione o evento" e ícone de lixeira. Botões "+ Adicionar Condição" e "+ Adicionar Grupo". No canto inferior direito há botões flutuantes de zoom e expandir. Demonstra a nova opção "Atributo de Perfil" no seletor de tipos de condição de regra.
* Vamos fazer a atualização duas vezes: a primeira vez que o usuário entrar, identificando ele pelo localStorageId e quando o usuário logar, que iremos identificar pelo external_userID e baixar as informações para o sessionStorage.
* Utilizar as informações salvas em profile no DB e cruzar com as informações da sessão atual para conseguir identificar o usuário e validar as regras.
> **[Imagem 2 — transcrição]:** Screenshot de UI, painel "Defina as..." (Defina as Condições da Regra) com dropdown de tipos aberto. Opções: "Visualização da página", "Clicou", "Elemento visível", "Acesso", "Atributo de Perfil", "Tem Tag" (esta última selecionada/marcada com check, destacada em laranja com ícone de etiqueta). A linha de condição 1 mostra três dropdowns: "Tem Tag" (ícone etiqueta), "Tem" e um seletor de valor "High Roller" (com ícone de tag amarela). Ícone de lixeira à direita. Botões "+ Adicionar Condição" e "+ Adicionar Grupo". Demonstra a condição do tipo "Tem Tag" configurada para a tag "High Roller".
> **[Imagem 3 — transcrição]:** Screenshot de UI de configuração de regra/ação. No topo há checkboxes de componentes: "Modal Cobra (Modal)" e "Modal Tigre (Modal)", com a nota "Os componentes marcados serão executados quando as condições da regra forem verdadeiras." Há um campo "Tempo (segundos)" com placeholder "Ex.: 2" e a nota "Se informado, a ação será executada após este atraso". Um campo "Tipo *" com valor "Comportamental". Um campo "Descrição *" (obrigatório) com placeholder "Descreva esta regra". Um dropdown de atributos está aberto mostrando: "Score de Intenção" (com check), "Nível de Intenção", "Total de Depósitos (R$)", "Qtd. de Depósitos", "Média por Depósito (R$)", "Dias Desde Último Depósito", "Valor do 1º Depósito (R$)", "Tier de Depósitos" (destacado em laranja), "Tendência de Depósitos", "Tendência (Últ. 5 Semanas)", "Sessões por Semana". Abaixo, painel "Defina as Condições da Regra" com "AND", "das seguintes condições" e a linha de condição 1: dropdowns "Atributo de Perfil", "Score de Intenção", "Maior que" e campo "Valor". Demonstra a variedade de atributos de perfil comportamentais (relacionados a depósitos e intenção) disponíveis para condições de regra.
> **[Imagem 4 — transcrição]:** Screenshot do navegador Chrome com DevTools aberto na aba "Application" > "Local Storage" do site https://jogao.bet.br. Barra de favoritos visível (Facebook Advertisin..., HYROS Pricing, dltHub, Home | Palantir, Streamlit). Banner do DevTools "...is now available in Portuguese" com botões "Don't show again", "Always match Chrome's language", "Switch DevTools to Portuguese". A tabela de Local Storage (colunas Key / Value) lista as chaves: `67dd9fecfa0359a08dbd1b1c.clientId` = `a8db6f2c9ca3427eb9a672be233238da`; `SmartTrack__page_visit_counter` = `1`; `ZD-buid` = `a8db6f2c9ca3427eb9a672be233238da`; `ZD-suid` = `{"id":"1f187ba179444494a6cfbbad70c3f2d7","expiry":1769625566848,"tabs":{"count...`; `amount_variance` = `{"start":0,"last":0,"ts":"2026-01-28T18:24:27.326Z","history":[],"hitZero":false,"alerts":{...`; `smartTracker__session_id` = `sess_726cbb1b-0a33-42ef-8e8d-4932546b1890`; `smarttrack_rule_condition_hashes` = `{"rule_1769606549853_z1hbavh58":93827164,"rule_1767723727611_6mz6fi5fq":-19...`; `smarttrack_rule_executions` = `[{"timestamp":1769624667321,"ruleId":"rule_1767723727611_6mz6fi5fq","ruleName...`; `smarttrack_session_matched_rules` = `["rule_1767723727611_6mz6fi5fq|pv:1","rule_1769606549853_z1hbavh58|pv:1"]`; `smarttrack_state` = `{"version":1,"updatedAt":"2026-01-28T18:24:26.757Z","visited_url":["https://jogao.b...`; `tt_appInfo` = `{"platform":"pc"}`; `tt_pixel_is_enrich_ipv6_triggered_by_enrich_am` = `true`; `tt_pixel_session_index` = `{"index":0,"main":0}`; `tt_sessionId` = `"9352b2ca-fc76-11f0-9cc8-726d280919d3::ZuhieAjpxT8T6avSxyNB"`; `userin_login` = `{"SmartTrack__localstorage_id":"SmartTrack__local_i9lp5xdtylamj1f9ap2","dt":17696...`; `userin_profile` = `{"balanceRealtime":{"current":0,"sessionStart":0,"sessionNetChange":0,"sessionNetC...` (linha destacada). Demonstra os dados reais persistidos no localStorage do site, incluindo `userin_profile`, `userin_login`, `smarttrack_state`, execuções/regras casadas e o `amount_variance` (controle de saldo).

## Histórico de status
- Backlog (backlog): 2026-01-27T14:12:10.220Z → 2026-01-27T14:43:28.186Z
- To-do (unstarted): 2026-01-27T14:43:28.186Z → 2026-01-27T20:15:35.520Z
- In Progress (started): 2026-01-27T20:15:35.520Z → 2026-01-29T12:39:07.734Z
- Pull Request (started): 2026-01-29T12:39:07.734Z → 2026-02-10T19:36:45.764Z
- Product Review (started): 2026-02-10T19:36:45.764Z → 2026-02-12T14:55:57.005Z
- Released (completed): 2026-02-12T14:55:57.005Z → atual

## Relações
—

## Anexos
—
