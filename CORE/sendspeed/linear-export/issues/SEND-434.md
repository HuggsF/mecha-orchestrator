# SEND-434 — 🐞 - Condição de Atributo de Perfil não funciona na Jornada

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | Urgent |
| Responsável | Vinicius Carneiro |
| Time | Sendspeed |
| Projeto | — |
| Labels | Jornadas, UserIn, Bug, User Story |
| Parent | — |
| Criada | 2026-03-31T12:37:44.972Z por Vinicius Carneiro |
| Iniciada | 2026-04-02T11:46:45.935Z |
| Concluída | 2026-05-08T18:07:07.864Z |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-434--condicao-de-atributo-de-perfil-nao-funciona-na-jornada |
| URL | https://linear.app/sendspeed/issue/SEND-434/condicao-de-atributo-de-perfil-nao-funciona-na-jornada |

## Descrição

## Bug

A condição de **atributo de perfil** configurada nos nós de gatilho e condição da jornada não está sendo avaliada corretamente. Quando uma jornada possui um nó de condição baseado em atributos do perfil do usuário (ex: `profile.tags`, `profile.phone`, `profile.segment`), a avaliação falha ou retorna resultado incorreto, fazendo com que o fluxo não siga o caminho esperado.

## Comportamento esperado

* O nó de condição deve avaliar os atributos do perfil do usuário (vindos do Segment Engine) e direcionar o fluxo corretamente com base na regra configurada

## Comportamento atual

* A condição de atributo de perfil não é avaliada corretamente, fazendo com que o fluxo da jornada não siga o caminho esperado

## Impacto

* Jornadas que dependem de segmentação por atributo de perfil não funcionam
* Disparos condicionais (ex: só enviar SMS se tem telefone, só enviar se tag = VIP) não são filtrados
* Afeta diretamente a personalização e eficácia das jornadas em produção

## Áreas de investigação

* `JourneyOffsiteProcessor.evaluateConditionNode()` — lógica de avaliação de condições
* `buildEvaluationContext()` — como o profile é mapeado para o contexto de avaliação
* Resolução de variáveis do profile (Segment Engine) no contexto da jornada
* Mapeamento entre campos configurados no editor visual e campos reais do profile

## Critérios de aceite

- [ ] Condição com atributo de perfil `phone exists` direciona corretamente
- [ ] Condição com atributo de perfil `tag = X` avalia corretamente
- [ ] Condição com atributo numérico (ex: `depositCount > 0`) funciona
- [ ] Fluxo segue caminho "true" quando condição é satisfeita
- [ ] Fluxo segue caminho "false" quando condição não é satisfeita
- [ ] Logs de debug mostram claramente o valor avaliado e o resultado da condição

---

## 🎯 Priorização RICE — Score: 19.2 (#2 no To-do)

| Reach | Impact | Confidence | Effort | Score |
| -- | -- | -- | -- | -- |
| 8 | 3 (massive) | 80% | 1 mês | **19.2** |

**Justificativa:** Bug crítico com impacto massivo. Afeta todas as empresas que usam jornadas com condições de perfil (Reach 8). O impacto é o maior possível (3 = massive) porque sem condições funcionando, toda a lógica de personalização e segmentação dentro das jornadas está quebrada — SMS vai para quem não deveria, fluxos ignoram regras de negócio. Confidence 80% porque o bug é claro mas a causa raiz precisa de investigação. Esforço estimado em 1 mês considerando debug + fix + testes.

## Histórico de status
- Backlog (backlog): 2026-03-31T12:37:44.972Z → 2026-03-31T12:41:05.202Z
- To-do (unstarted): 2026-03-31T12:41:05.202Z → 2026-04-02T11:46:45.944Z
- Pull Request (started): 2026-04-02T11:46:45.944Z → 2026-04-14T15:15:03.305Z
- Product Review (started): 2026-04-14T15:15:03.305Z → 2026-05-08T18:07:07.893Z
- Released (completed): 2026-05-08T18:07:07.893Z → atual

## Relações
—

## Anexos
- fix(journey): SEND-434 resolve profile attributes from multiple sources — https://github.com/sendspeed0/platform-backend/pull/29
