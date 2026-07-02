# SEND-326 — 🐞 - Elemento visivel não funciona.

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | Urgent |
| Responsável | pedro.iegler@sendspeed.com |
| Time | Sendspeed |
| Projeto | — |
| Labels | User Story, UserIn, Regras, Bug |
| Parent | — |
| Criada | 2026-02-13T15:06:59.683Z por Vinicius Carneiro |
| Iniciada | 2026-02-19T14:16:49.888Z |
| Concluída | 2026-02-20T16:32:32.988Z |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-326--elemento-visivel-nao-funciona |
| URL | https://linear.app/sendspeed/issue/SEND-326/elemento-visivel-nao-funciona |

## Descrição

## 📍 Onde ocorre

Regra de elemento visivel

> **[Imagem 1 — transcrição]:** Screenshot de UI da plataforma (configuração de regra). Cabeçalho de exemplo com placeholder "Ex: Clicou no botão de login". Seção **"Condições"** com o painel "Defina as Condições da Regra". Há um seletor **"AND"** (dropdown) com o texto "Todas as condições abaixo devem ser verdadeiras" e o badge "1 condição total". A condição nº 1 é composta por três campos: dropdown **"Elemento visível"**, dropdown **"É igual a"**, e um campo de texto com valor **"_3lvVF"**. À direita há um ícone de ajuda (?) e um ícone de lixeira (excluir). Abaixo, botões **"+ Adicionar Condição"** e **"+ Adicionar Grupo"**. No rodapé aparece o início de uma seção "Preview:". Demonstra a configuração de uma regra de "Elemento visível" que deveria disparar a ação.

## 🔁 Passo a Passo.

1. Entrar na plataforma.
2. Criar uma jornada.
3. Adicionar ao fluxo o gatilho de regra -> elemento visivel e um gatilho de JS com o código alert('Ola');
4. Testar insite.

## ❌ Resultado Atual

O alert não aparece na tela quando o elemento visivel aparece.

## ✅ Resultado Esperado

Aparecer o alert na tela ao elemento visivel aparecer na tela.

## 🧪 Evidências

* [https://www.loom.com/share/68fea5f12e4d46f98c4605f0bf487a2d](https://www.loom.com/share/68fea5f12e4d46f98c4605f0bf487a2d)

## Histórico de status
- To-do (unstarted): 2026-02-13T15:06:59.683Z → 2026-02-19T14:16:49.897Z
- In Progress (started): 2026-02-19T14:16:49.897Z → 2026-02-19T17:01:03.357Z
- Pull Request (started): 2026-02-19T17:01:03.357Z → 2026-02-19T17:01:07.869Z
- Product Review (started): 2026-02-19T17:01:07.869Z → 2026-02-20T16:32:33.005Z
- Released (completed): 2026-02-20T16:32:33.005Z → atual

## Relações
—

## Anexos
—
