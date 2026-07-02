# SEND-271 — Criação de regra na parte de jornada

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | Urgent |
| Responsável | peterson.marques@sendspeed.com |
| Time | Sendspeed |
| Projeto | — |
| Labels | User Story, UserIn, Jornadas, Melhoria |
| Parent | — |
| Criada | 2025-12-02T12:57:23.911Z por Vinicius Carneiro |
| Iniciada | 2025-12-08T12:26:51.838Z |
| Concluída | 2026-01-19T18:24:40.214Z |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-271-criacao-de-regra-na-parte-de-jornada |
| URL | https://linear.app/sendspeed/issue/SEND-271/criacao-de-regra-na-parte-de-jornada |

## Descrição

**Como** analista de produto

**Quero** poder adicionar regras as jornadas

**Para** conseguir rastrear o fluxo de conversão sem a necessidade de um card.

**Associação** N:N (Varias jornadas podem estar em varias regras e vice versa)

---

### **Critérios de aceite:**

* O sistema de regras precisa ser integrado ao sistema de jornadas semelhante ao sistema de integração dos componentes.
* Apenas regras sem componentes deverão ser integradas diretamente á jornada.
* Nas jornadas, deve mostrar quais regras sem componentes estão ligadas à aquela jornada juntamente com os componentes. ex:

> **[Imagem 1 — transcrição]:** Screenshot de UI — card "Jornada 1" (fundo branco, cantos arredondados). No topo esquerdo o título em negrito "Jornada 1"; no topo direito dois ícones de ação: um lápis (editar) e uma lixeira vermelha (excluir). No corpo, dois indicadores lado a lado: um ícone de cartão com o texto "8 componente(s) associado(s)" e um ícone de sliders/ajustes com o texto "3 regra(s) associada(s)". Na parte inferior, dois botões: "Gerenciar componentes" e "Gerenciar regras". Demonstra o card de jornada exibindo a contagem de componentes e de regras associadas, com os respectivos botões de gerenciamento.

* Caso tenha algum componente com regras, quando o componente for adicionado ao sistema de jornadas, ele deve obrigatoriamente puxar todas as regras juntos.

### Cenário de teste:

- [ ] Entrar na plataforma.
- [ ] Criar uma regra individual (sem componente), que dispara um JS
- [ ] Entrar na parte de jornadas já existente.
- [ ] Atrelar a regra individual (sem componente) criada a jornada.
- [ ] Salvar.
- [ ] Testar se a regra esta funcionando normalmente.

## Histórico de status
- Backlog (backlog): 2025-12-02T12:57:23.911Z → 2025-12-02T17:42:29.652Z
- Refining (backlog): 2025-12-02T17:42:29.652Z → 2025-12-02T20:59:35.968Z
- To-do (unstarted): 2025-12-02T20:59:35.968Z → 2025-12-08T12:26:51.849Z
- In Progress (started): 2025-12-08T12:26:51.849Z → 2025-12-12T14:17:07.254Z
- Pull Request (started): 2025-12-12T14:17:07.254Z → 2026-01-19T18:04:52.725Z
- Product Review (started): 2026-01-19T18:04:52.725Z → 2026-01-19T18:24:40.231Z
- Released (completed): 2026-01-19T18:24:40.231Z → atual

## Relações
—

## Anexos
—
