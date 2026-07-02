# SEND-55 — Gerenciar usuários e permissões na conta

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | Urgent |
| Responsável | peterson.marques@sendspeed.com |
| Time | Sendspeed |
| Projeto | — |
| Labels | — |
| Parent | — |
| Criada | 2025-08-13T22:10:13.868Z por bruno.heidrich@sendspeed.com |
| Iniciada | 2025-08-20T12:13:19.120Z |
| Concluída | 2025-09-25T19:09:00.824Z |
| Arquivada | 2026-06-11T22:48:57.789Z |
| Vencimento | — |
| Branch | hugofernandes/send-55-gerenciar-usuarios-e-permissoes-na-conta |
| URL | https://linear.app/sendspeed/issue/SEND-55/gerenciar-usuarios-e-permissoes-na-conta |

## Descrição

* **Como** cliente com conta principal,
* **Quero** criar sub-usuários e atribuir permissões específicas,
* **Para** que minha equipe possa acessar apenas as áreas necessárias para seu trabalho.

**Critérios de Aceite:**

1. O cliente deve poder criar, editar e excluir sub-usuários.
2. Deve ser possível atribuir diferentes níveis de acesso.
3. Sub-usuários devem entrar na plataforma com login próprio.
4. O cliente principal deve poder alterar permissões a qualquer momento.

Tech Story

Etapa 01: Criar membro e adm, no banco…
Etapa 02: Adm tem tais funcoes e permissoes
Etapa 03: Membro tem tais funcoes e permissoes
Etapa 04: Tela onde o adm pode adicionar outros membro (User story X)

> **[Imagem 1 — transcrição]:** Diagrama/fluxo em quadro branco (estilo Excalidraw) com o título grande "USERIN" no topo. Abaixo, uma sequência de quatro caixas retangulares conectadas horizontalmente por linhas: (1) "[TASK] Atualização da Sidebar da Plataforma POR EMPRESA"; (2) "Página Interna da Plataforma UserIn com todos os clientes e suas configurações"; (3) "Dentro da página, preciso ter controle das opções de sidebar que irão aparecer pra este cliente + Histórico de alteração"; (4) "Vai refletir EM TEMPO REAL na plataforma do CLIENTE." Ligada à terceira caixa por linha tracejada vermelha, há uma caixa inferior tracejada: "PLANOS (PARA DEIXAR A VENDA AUTOMÁTICA)". Observação: este diagrama textualmente pertence ao tema de sidebar/planos (relacionado a SEND-64), mas foi renderizado a partir do conteúdo desta issue.

# 🏗️ Arquitetura Implementada

### Hierarquia de Usuários

* 👑 Proprietário (owner) - Controle total da conta
* 🔧 ADM (admin) - Gerencia membros, acessa relatórios
* 👨‍💼 Membro - Três tipos com níveis diferentes:
  * Manager: Cria campanhas, gerencia contatos
  * Employee: Edita campanhas, visualiza contatos
  * Viewer: Apenas visualização

### **Endpoints Criados (/api/sub-users)**

* GET /my-permissions - Permissões do usuário atual
* GET / - Listar sub-usuários da empresa
* POST / - Criar novo sub-usuário
* PUT /:userId - Editar sub-usuário
* DELETE /:userId - Remover sub-usuário
* PATCH /:userId/grant-access - Conceder acesso
* PATCH /:userId/revoke-access - Revogar acesso
* PATCH /:userId/role - Alterar role

## **🔐 Sistema de Permissões**

**Permissões por Role:**

* **Proprietário**: Todas as 15+ permissões
* **ADM**: 11 permissões (não pode gerenciar empresa)
* **Manager**: 8 permissões (foco em conteúdo)
* **Employee**: 5 permissões (operações básicas)
* **Viewer**: 3 permissões (apenas visualização)

## **🚀 Regras de Negócio Implementadas**

### **Criação de Sub-usuários**

* ADM só pode criar membros (não outros ADMs)
* Email único com associação automática se já existir
* Senhas temporárias geradas automaticamente

### **Controle Hierárquico**

* Proprietário pode gerenciar todos (exceto outro proprietário)
* ADM pode gerenciar apenas membros
* Membros não podem gerenciar ninguém

### **Segurança**

* Soft delete preserva histórico
* Validações em múltiplas camadas
* Rate limiting mantido

## Histórico de status
- To-do (unstarted): 2025-08-13T22:10:13.868Z → 2025-08-20T12:13:19.108Z
- In Progress (started): 2025-08-20T12:13:19.108Z → 2025-09-18T19:09:42.815Z
- Pull Request (started): 2025-09-18T19:09:42.815Z → 2025-09-25T18:36:31.528Z
- Product Review (started): 2025-09-25T18:36:31.528Z → 2025-09-25T19:09:00.811Z
- Released (completed): 2025-09-25T19:09:00.811Z → atual

## Relações
—

## Anexos
—
