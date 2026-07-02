# SEND-429 — RCS em Jornadas — Seleção de Template com Busca, Filtros e Navegação para Edição

| Campo | Valor |
| -- | -- |
| Status | To-do (unstarted) |
| Prioridade | High |
| Responsável | — |
| Time | Sendspeed |
| Projeto | — |
| Labels | — |
| Parent | — |
| Criada | 2026-03-26T11:25:52.499Z por paulo.ribeiro@sendspeed.com |
| Iniciada | — |
| Concluída | — |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-429-rcs-em-jornadas-selecao-de-template-com-busca-filtros-e |
| URL | https://linear.app/sendspeed/issue/SEND-429/rcs-em-jornadas-selecao-de-template-com-busca-filtros-e-navegacao-para |

## Descrição

## **Descrição**

Atualmente, o nó "Enviar RCS" no Journey Builder permite selecionar um template RCS de um dropdown simples e, em seguida, editar o conteúdo rico **inline** dentro do painel lateral de 450px. Isso gera dois problemas:

1. **O editor completo de RCS não cabe em 450px** — a experiência é apertada, com muito scroll vertical, e não há espaço para preview + editor lado a lado.
2. **A busca de templates é um dropdown flat sem filtro** — com muitos templates, o usuário precisa rolar a lista inteira para achar o que quer.

## **Proposta**

Transformar o painel do nó RCS em uma **experiência de seleção e visualização**, não de edição. A edição acontece na tela dedicada de templates.

### **O que muda**

| Atual | Proposto |
| -- | -- |
| Dropdown simples com todos os templates | Seletor com input de busca por texto + filtro por formato (Texto, Cartão, Carrossel, Arquivo) |
| Opção "Nenhum (conteúdo inline)" que habilita o RcsContentEditor inline | Opção "Criar novo template" que abre /templates/rcs/new em nova aba |
| RcsContentEditor completo inline no painel de 450px | Apenas RcsPhonePreview (read-only) mostrando o conteúdo do template selecionado |
| Botão X para desvincular template | Botão "Editar template" que abre /templates/rcs/:id/edit em nova aba |
| Preview colapsável (Collapsible) | Preview sempre visível — é o conteúdo principal do painel |

### **Detalhes do seletor de templates**

**Input de busca:**

* Filtro por nome do template em tempo real (debounce)
* Placeholder: "Buscar por nome..."

**Filtros por formato:**

* Chips ou toggles horizontais: Todos | Texto | Cartão | Carrossel | Arquivo
* Mapeiam para rcsContent.type: text, rich_card, carousel, file
* "Todos" é o padrão

**Lista de resultados:**

* Cada item mostra: nome, tipo (badge), quantidade de cards (se carrossel), quantidade de variáveis
* Seleção única — clicar no item seleciona e carrega o preview
* Se nenhum template encontrado: "Nenhum template encontrado. \[Criar novo ↗\]"

### **Comportamento dos botões**

| Botão | Ação |
| -- | -- |
| **Criar novo template** | Abre /templates/rcs/new em nova aba (target="\_blank") |
| **Editar template** | Abre /templates/rcs/:id/edit em nova aba. Visível só quando há template selecionado |
| **Desvincular** | Remove a associação do template, limpa o preview. O nó fica sem conteúdo RCS até selecionar outro |

### **O que sai do painel**

* RcsContentEditor (editor de conteúdo rico) — não aparece mais inline no painel da jornada
* A edição de conteúdo RCS acontece **exclusivamente** na tela de templates (/templates/rcs/:id/edit)

### **O que permanece no painel**

* Seletor de credencial (provedor RCS)
* Seletor de template (com busca e filtros)
* RcsPhonePreview (read-only, mostrando o conteúdo do template selecionado)
* Textarea de fallback SMS
* toggle on/off fallback SMS
* Alerta informativo sobre fallback

## **Critérios de Aceitação**

- [ ] O RcsContentEditor não aparece no painel do nó RCS da jornada
- [ ] Input de busca filtra templates por nome em tempo real
- [ ] Filtros por formato (Todos, Texto, Cartão, Carrossel, Arquivo) funcionam e podem ser combinados com a busca
- [ ] Cada item na lista mostra: nome, badge de tipo, quantidade de variáveis
- [ ] Ao selecionar um template, o RcsPhonePreview exibe o conteúdo completo (text, rich_card, carousel ou file)
- [ ] Botão "Editar template" abre /templates/rcs/:id/edit em nova aba
- [ ] Botão "Criar novo template" abre /templates/rcs/new em nova aba
- [ ] Botão "Desvincular" remove o template selecionado e limpa o preview
- [ ] Template é obrigatório — o nó não pode ser salvo sem template selecionado
- [ ] Ao voltar da aba de edição do template, se o template selecionado foi alterado, o preview reflete as mudanças (re-fetch ao focar a aba ou ao abrir o painel)
- [ ] Texto de fallback SMS permanece editável inline no painel
- [ ] Se nenhum template corresponde à busca/filtro, exibir empty state com link para criar novo

## **Edge Cases**

* **Template deletado enquanto selecionado na jornada:** Ao abrir o nó, se o template não existir mais, exibir alerta: "O template selecionado foi removido. Selecione outro." e limpar a seleção.
* **Template alterado por outro usuário:** O preview carrega o conteúdo atual do template ao abrir o painel (re-fetch). Não usa cache local.
* **Nenhum template RCS publicado:** Empty state: "Nenhum template RCS disponível. Crie um para usar em jornadas." com botão "Criar template".
* **Muitos templates (50+):** A busca por texto e os filtros garantem que o usuário encontre rapidamente.
* **Usuário abre "Editar template" e não salva:** O preview continua mostrando a versão salva. Nenhuma inconsistência.

---

## 🎯 Priorização RICE — Score: 6.4

| Reach | Impact | Confidence | Effort | Score |
| -- | -- | -- | -- | -- |
| 6 | 2 (high) | 80% | 1.5 meses | **6.4** |

**Justificativa:** Reach 6: usuários configurando jornadas com RCS. Impacto high (2): UX atual apertada em 450px e não escala. Confidence 80%: proposta clara. Esforço 1.5 meses: refactor do painel + busca/filtros + preview.

## Histórico de status
- Backlog (backlog): 2026-03-26T11:25:52.499Z → 2026-03-26T12:18:59.804Z
- Refining (backlog): 2026-03-26T12:18:59.804Z → 2026-03-31T12:33:36.667Z
- To-do (unstarted): 2026-03-31T12:33:36.667Z → atual

## Relações
—

## Anexos
—
