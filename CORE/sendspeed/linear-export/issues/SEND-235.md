# SEND-235 — [MELHORIA] Aba de Segmentos de Usuários (User Segmentation Tab)

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | Urgent |
| Responsável | Vinicius Carneiro |
| Time | Sendspeed |
| Projeto | — |
| Labels | — |
| Parent | — |
| Criada | 2025-10-31T13:46:40.926Z por Vinicius Carneiro |
| Iniciada | 2025-11-06T21:37:51.183Z |
| Concluída | 2025-12-01T21:02:52.914Z |
| Arquivada | 2026-06-04T22:49:20.592Z |
| Vencimento | — |
| Branch | hugofernandes/send-235-melhoria-aba-de-segmentos-de-usuarios-user-segmentation-tab |
| URL | https://linear.app/sendspeed/issue/SEND-235/melhoria-aba-de-segmentos-de-usuarios-user-segmentation-tab |

## Descrição

**Como** Analista de Produto

**Quero** criar uma aba de **Segmentos** que permita definir e visualizar grupos de usuários com base em atributos e condições personalizadas

**Para** facilitar análises comportamentais e a criação de campanhas direcionadas com base em filtros dinâmicos (ex: país, status logado, eventos, atributos customizados)

---

### **Critérios de Aceite:**

* Deve existir uma nova aba lateral chamada **"Segmentos"** no painel principal.
* O usuário pode **criar um novo segmento** clicando em "+ Novo Segmento".
* O formulário deve conter:
  * Campo **Nome do Segmento** (texto obrigatório)
  * Campo **Descrição** (texto opcional)
* A seção **"Definir Condições do Segmento"** deve permitir:
  * Selecionar o tipo de filtro: User Attribute, URL.
  * Escolher o **atributo** (ex: \__uin_user_islogged).
  * Definir o **valor** correspondente (ex: "true").
  * Escolher o **operador lógico** (Equals, Not Equals, Contains, Not Contains).
  * Agrupar condições com \[**AND / OR\]**.
  * Criar grupos aninhados (Add Condition / Add Group).
* Exibir **contador de condições** (ex: "2 conditions").
* O layout deve seguir o padrão de UI da plataforma (mesma hierarquia visual, espaçamento e componentes de dropdown, input e botão).
* O botão **Salvar Segmento** deve validar campos obrigatórios e salvar no backend.
* O segmento salvo deve ser persistido com:
  * segment_id
  * segment_name
  * segment_conditions (em formato JSON)
  * created_by, created_at, updated_at
* A API deve permitir **listar**, **criar**, **editar** e **excluir** segmentos.
* Cada grupo deve ter opção de **Remover Grupo**.
* Deve permitir visualizar o JSON criado exportar e importar
* Deve permitir a combinação lógica:
  * \[All\] of the following conditions \[AND\]
  * \[Any\] of the following conditions \[OR\]

## Histórico de status
- To-do (unstarted): 2025-10-31T13:46:40.926Z → 2025-11-06T21:37:51.191Z
- In Progress (started): 2025-11-06T21:37:51.191Z → 2025-11-10T18:35:50.944Z
- Pull Request (started): 2025-11-10T18:35:50.944Z → 2025-11-18T17:46:24.171Z
- Product Review (started): 2025-11-18T17:46:24.171Z → 2025-12-01T21:02:52.924Z
- Released (completed): 2025-12-01T21:02:52.924Z → atual

## Relações
—

## Anexos
—
