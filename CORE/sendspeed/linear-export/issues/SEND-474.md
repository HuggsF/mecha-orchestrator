# SEND-474 — Gestão de Tokens por Rota na SendSpeed

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | No priority |
| Responsável | — |
| Time | Sendspeed |
| Projeto | — |
| Labels | — |
| Parent | — |
| Criada | 2026-05-08T18:51:22.039Z por pedro.antunes@sendspeed.com |
| Iniciada | — |
| Concluída | 2026-05-18T12:23:07.603Z |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-474-gestao-de-tokens-por-rota-na-sendspeed |
| URL | https://linear.app/sendspeed/issue/SEND-474/gestao-de-tokens-por-rota-na-sendspeed |

## Descrição

### 

**Como** empresa cliente da SendSpeed,
**quero** gerenciar tokens de autenticação por rota diretamente no dashboard,
**para** criar, visualizar e revogar acessos em tempo real para diferentes canais como SMS, RCS e OTP.

---

## Contexto

A SendSpeed possui múltiplas rotas de envio, como:

* SMS
* RCS
* OTP
* WhatsApp, se aplicável futuramente
* Rotas específicas por fornecedor ou operação

Cada rota pode possuir um **alias amigável**, facilitando a identificação no dashboard.

Exemplo:

| Rota técnica | Alias |
| -- | -- |
| `sms_route_01` | SMS Transacional |
| `sms_otp_vivo` | OTP Vivo |
| `rcs_main` | RCS Principal |

Cada empresa poderá ter **um ou mais tokens ativos por rota**, podendo criar ou revogar tokens sem necessidade de suporte técnico.

---

## Funcionalidades

### 1\. Listar rotas disponíveis da empresa

O dashboard deve exibir todas as rotas liberadas para a empresa.

Cada rota deve mostrar:

* Alias da rota
* Tipo da rota: SMS, RCS, OTP etc.
* Status da rota: ativa/inativa
* Quantidade de tokens ativos
* Data da última criação de token
* Data da última revogação

---

### 2\. Criar novo token por rota

A empresa poderá clicar em **"Criar token"** dentro de uma rota.

Ao criar, o sistema deve gerar um token seguro e exibir:

* Nome do token
* Token gerado
* Rota vinculada
* Data de criação
* Usuário que criou
* Status ativo

O token deve ser exibido integralmente **apenas uma vez**, no momento da criação.

Depois disso, o dashboard deve exibir somente uma versão mascarada tendo que clickar em um icone de view pra ve-lo.

Exemplo:

`sk_live_************8f3a`

---

### 3\. Nomear tokens

Ao criar um token, o usuário deve poder informar um nome descritivo.

Exemplos:

* Produção ERP
* Integração Smartico
* Ambiente Homologação
* API Interna Cliente
* Backup Gateway

Isso ajuda a empresa a saber onde cada token está sendo usado.

---

### 4\. Revogar token em tempo real

A empresa poderá revogar qualquer token ativo.

Ao revogar:

* O token deve deixar de autenticar imediatamente
* O status deve mudar para revogado
* Deve registrar data/hora da revogação
* Deve registrar o usuário que revogou
* O token não deve poder ser reativado

Antes da revogação, o sistema deve pedir confirmação.

Mensagem sugerida:

> Tem certeza que deseja revogar este token?
> Essa ação é irreversível e pode interromper integrações que usam esse token.

---

### 5\. Múltiplos tokens por rota

Cada rota pode ter vários tokens ativos simultaneamente.

Isso permite cenários como:

* Um token por sistema integrado
* Um token para produção e outro para homologação
* Troca segura de tokens sem downtime
* Rotação periódica de credenciais

### *6. Testar token (Ver complexidade)*

*Deverá ser possível "validar" que o token ta funcionando, recebendo primeiro disparo*

*O usuário enviará uma mensagem por fora, token recebe primeira mensagem -> Token validado*

---

## Regras de negócio

 1. Cada token pertence obrigatoriamente a uma empresa.
 2. Cada token pertence obrigatoriamente a uma rota.
 3. Uma rota pode ter múltiplos tokens ativos.
 4. Um token só pode acessar a rota para a qual foi criado.
 5. Tokens revogados não podem ser reutilizados.
 6. Tokens devem ser validados em tempo real nas APIs da SendSpeed.
 7. O token completo só pode ser exibido no momento da criação.
 8. Deve existir auditoria de criação e revogação.
 9. Apenas usuários autorizados da empresa podem criar ou revogar tokens.
10. Tokens não devem ser apagados fisicamente, apenas marcados como revogados.

## Tela sugerida

### Gestão de Tokens

**Empresa:** Cliente XPTO

| Rota | Tipo | Tokens ativos | Status | Ações |
| -- | -- | -- | -- | -- |
| SMS Transacional | SMS | 3 | Ativa | Ver tokens |
| OTP Principal | OTP | 2 | Ativa | Ver tokens |
| RCS Marketing | RCS | 1 | Ativa | Ver tokens |

Dentro da rota:

| Nome do token | Prefixo | Status | Criado por | Criado em | Ações |
| -- | -- | -- | -- | -- | -- |
| Produção ERP | `sk_****a91f` | Ativo | Pedro | 08/05/2026 | Revogar |
| Smartico | `sk_****89cc` | Ativo | Bruno | 08/05/2026 | Revogar |
| Homologação | `sk_****77ab` | Revogado | Pedro | 07/05/2026 | — |

## Histórico de status
- To-do (unstarted): 2026-05-08T18:51:22.039Z → 2026-05-18T12:23:07.615Z
- Released (completed): 2026-05-18T12:23:07.615Z → atual

## Relações
—

## Anexos
—
