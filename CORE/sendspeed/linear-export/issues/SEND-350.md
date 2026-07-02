# SEND-350 — 🐞 - Persistencia no banco de dados ao deletar um objeto no Grafo

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | Urgent |
| Responsável | pedro.iegler@sendspeed.com |
| Time | Sendspeed |
| Projeto | — |
| Labels | User Story, UserIn, Bug |
| Parent | — |
| Criada | 2026-02-24T15:34:18.608Z por Vinicius Carneiro |
| Iniciada | 2026-02-24T16:26:10.488Z |
| Concluída | 2026-02-25T15:12:49.121Z |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-350--persistencia-no-banco-de-dados-ao-deletar-um-objeto-no |
| URL | https://linear.app/sendspeed/issue/SEND-350/persistencia-no-banco-de-dados-ao-deletar-um-objeto-no-grafo |

## Descrição

## 📍 Onde ocorre

[https://platform-stg-userin-ai.fly.dev/objects/graph](https://platform-stg-userin-ai.fly.dev/objects/graph)

## 🔁 Passo a Passo

1. Entrar na plataforma
2. Objetos -> Grafo & Relações.
3. Criar um novo Object Type.
4. Deleta-lo.
5. Tentar criar um novo com o mesmo nome.

## ❌ Resultado Atual

Quando o objeto é deletado no canva/aba de entidades, ele não é deletado no banco de dados.

## ✅ Resultado Esperado

Quando o objeto for deletado no canva/aba de entidades, ele deve ser deletado no banco de dados também.

## 🧪 Evidências

> **[Imagem 1 — transcrição]:** Screenshot de UI de um modal de criação de Object Type sobre a tela "Objetos" (13 entidades). Campos: **Slug (auto-gerado, editável)** = "teste" (nota: "Identificador unico. Sera usado como namespace: teste.campo"); **Descricao** (vazio); **Icone** = "Generic"; **Vertical** = "Generico". Seção **"Auto-detectar Estrutura (Opcional)"** com "Detectar Schema Automaticamente" e botão roxo **"Iniciar Escuta"** + aviso "Crie uma API Key em Visão Geral → Ingestão". Seção "Ontologia do Objeto" com "Nenhum campo definido." e botão "+ Campo". Botões "Cancelar" e "Criar". No canto inferior direito, um **toast de erro vermelho** com a mensagem: **"Erro — E11000 duplicate key error collection: userin-staging.object_types index: companyId_1_slug_1 dup key: { companyId: "689e27eb4ef82776c55036db", slug: "teste" }"**. Demonstra que o objeto "teste" deletado permanece no banco (erro de chave duplicada ao recriar). No topo, conta "Admin YAD STORE" e botões "Provisionar iGaming" / "+ Novo Object Type".

## Histórico de status
- To-do (unstarted): 2026-02-24T15:34:18.608Z → 2026-02-24T16:26:10.511Z
- In Progress (started): 2026-02-24T16:26:10.511Z → 2026-02-24T18:38:52.583Z
- Product Review (started): 2026-02-24T18:38:52.583Z → 2026-02-25T15:12:49.134Z
- Released (completed): 2026-02-25T15:12:49.134Z → atual

## Relações
—

## Anexos
—
