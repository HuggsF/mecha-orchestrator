# SEND-19 — Criar tabelas 'users' e 'companies'

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | No priority |
| Responsável | marcelo.motta@sendspeed.com |
| Time | Sendspeed |
| Projeto | SendSpeed 2.0 |
| Labels | Tech Story |
| Parent | — |
| Criada | 2025-05-27T18:21:27.369Z por Luiz Otávio |
| Iniciada | 2025-06-03T12:33:08.327Z |
| Concluída | 2025-06-10T18:32:59.204Z |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-19-criar-tabelas-users-e-companies |
| URL | https://linear.app/sendspeed/issue/SEND-19/criar-tabelas-users-e-companies |

## Descrição

> **Como** engenheiro de backend,
> **Quero** implementar as tabelas users e companies na base de dados,
> **Para que** possamos identificar corretamente os usuários da plataforma e as empresas-clientes.
>
> Associação N:N , um usuário pode estar em várias empresas, e uma empresa pode ter vários usuarios (por linha)

---

### 👉 Escopo

* Especificações da Tabela `users`
  * Objetivo: Representar os usuários que acessam a plataforma.
  * Campos obrigatórios:
    * `UUID`, chave única
    * `email`, string e único
    * `name`, string
    * `has_access` (utilizar uma tabela especifica: cada linha um vinculo de acesso entre company e usuario da empresa)
      * `company_id`, chave da tabela *companies*, campo *company_id*
      * `role`, enum =  owner (para o MVP, vamos seguir somente com uma possibilidade
* Especificações da tabela `companies`
  * **Objetivo:** Representar empresas-clientes da SendSpeed.
  * **Campos obrigatórios:**
    * `company_id`, chave única
    * `cnpj`, string única e com validação de formato
    * `company_name`, string
    * `company_official_name`, string (razão social. Abertos a nomes melhoreS)
    * `plan`, enum = standard (para o MVP, vamos seguir somente com uma possibilidade)is_active: boolean
    * `active`, boolean
    * `user_owner`, chave da tabela *users*, campo *UUID*

---

### **👉 Critérios de Aceite**

* As tabelas `users` e `companies` devem ser criadas com os campos definidos acima
* Cada usuário pode estar vinculado a uma ou mais empresas via `company_id`
* Cada empresa deve possuir um `user_owner`
* Deve ser possível inserir e consultar dados nas duas tabelas
* Campos obrigatórios devem ser validados (ex: email único, cnpj com formato válido)

## Histórico de status

- Backlog (backlog): 2025-05-27T18:21:27.369Z → 2025-05-28T13:57:08.085Z
- To-do (unstarted): 2025-05-28T13:57:08.085Z → 2025-06-03T12:33:07.185Z
- In Progress (started): 2025-06-03T12:33:07.185Z → 2025-06-10T18:32:59.188Z
- Released (completed): 2025-06-10T18:32:59.188Z → atual

## Relações

—

## Anexos

—
