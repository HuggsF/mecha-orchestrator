# SEND-36 — Separação de Ambientes de Desenvolvimento

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | Urgent |
| Responsável | andrei.garcia@externo.sendspeed.com |
| Time | Sendspeed |
| Projeto | — |
| Labels | — |
| Parent | — |
| Criada | 2025-07-03T11:49:47.959Z por bruno.heidrich@sendspeed.com |
| Iniciada | 2025-07-10T12:12:29.059Z |
| Concluída | 2025-07-21T12:44:35.937Z |
| Arquivada | 2026-01-25T01:58:20.246Z |
| Vencimento | — |
| Branch | hugofernandes/send-36-separacao-de-ambientes-de-desenvolvimento |
| URL | https://linear.app/sendspeed/issue/SEND-36/separacao-de-ambientes-de-desenvolvimento |

## Descrição

**Como** Tech Lead

**Eu quero** implementar separação clara entre ambientes de desenvolvimento

**Para que** a equipe possa trabalhar de forma organizada e evitar conflitos entre diferentes estágios do projeto

### Critérios de Aceitação

#### Cenário 1: Definição de Ambientes

* **Dado** que estou configurando o projeto
* **Quando** eu defino os ambientes de desenvolvimento
* **Então** devo ter pelo menos os ambientes: local, staging, produção, desenvolvimento
* **E** cada ambiente deve ter configurações isoladas

#### Cenário 2: Separação de Bancos de Dados

* **Dado** que tenho múltiplos ambientes configurados
* **Quando** eu acesso cada ambiente
* **Então** cada um deve usar seu próprio banco de dados MongoDB
* **E** não deve haver interferência entre os dados dos ambientes

#### Cenário 3: Configuração por Ambiente

* **Dado** que estou trabalhando em um ambiente específico
* **Quando** eu faço alterações de configuração
* **Então** as alterações devem afetar apenas o ambiente atual
* **E** outros ambientes devem permanecer inalterados

#### Cenário 4: Fluxo de Deployment

* **Dado** que tenho código pronto em um ambiente
* **Quando** eu promovo para o próximo ambiente
* **Então** deve seguir a sequência: local → staging → produção
* **E** deve haver validação antes de cada promoção

#### Cenário 5: Identificação Visual do Ambiente

* **Dado** que estou acessando a aplicação
* **Quando** eu visualizo a interface
* **Então** deve haver indicação clara de qual ambiente estou usando
* **E** ambientes não-produção devem ter indicadores visuais distintos

#### Cenário 6: Sincronização SendSpeed

* **Dado** que tenho ambientes configurados
* **Quando** eu configuro a integração SendSpeed
* **Então** cada ambiente deve ter sua própria configuração
* **E** deve mapear corretamente: staging → sendspeed-staging, local → sendspeed-localhost, etc.

## Histórico de status

- Backlog (backlog): 2025-07-03T11:49:47.959Z → 2025-07-10T12:12:29.044Z
- In Progress (started): 2025-07-10T12:12:29.044Z → 2025-07-21T12:44:35.988Z
- Released (completed): 2025-07-21T12:44:35.988Z → atual

## Relações

—

## Anexos

—
