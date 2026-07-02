# SEND-35 — Configuração de Gatilho Imediato [TELA]

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | High |
| Responsável | andrei.garcia@externo.sendspeed.com |
| Time | Sendspeed |
| Projeto | — |
| Labels | — |
| Parent | — |
| Criada | 2025-07-03T11:47:41.747Z por bruno.heidrich@sendspeed.com |
| Iniciada | 2025-07-22T23:04:24.896Z |
| Concluída | 2025-08-11T13:53:30.976Z |
| Arquivada | 2026-02-15T02:17:35.322Z |
| Vencimento | — |
| Branch | hugofernandes/send-35-configuracao-de-gatilho-imediato-tela |
| URL | https://linear.app/sendspeed/issue/SEND-35/configuracao-de-gatilho-imediato-tela |

## Descrição

**Como** Gerente de CRM

**Eu quero** configurar gatilhos imediatos para cards promocionais

**Para que** eu possa disparar ofertas personalizadas no momento exato que o cliente faz uma ação específica.

### Critérios de Aceitação

**Cenário: O Campo Gatilho Imediato deve sempre estar INATIVO**

#### Cenário 1: Ativação do Gatilho Imediato

* **Dado** que estou na aba "Gatilho" da configuração do card
* **Quando** eu ativo o switch "Ativar Gatilho Imediato"
* **Então** os campos de configuração do gatilho devem ser habilitados
* **E** eu devo poder configurar o nome do evento e os dados JSON

#### Cenário 2: Desativação do Gatilho Imediato

* **Dado** que o gatilho imediato está ativado
* **Quando** eu desativo o switch "Ativar Gatilho Imediato"
* **Então** todos os campos de configuração devem ficar inativos
* **E** os dados previamente inseridos devem ser preservados

#### Cenário 3: Configuração do Nome do Evento

* **Dado** que o gatilho imediato está ativado
* **Quando** eu preencho o campo "Nome do Evento"
* **Então** o sistema deve aceitar apenas caracteres alfanuméricos e underscore
* **E** deve gerar automaticamente um código de tracker personalizado

#### Cenário 4: Exibição dos dados do evento

* **Se passar o dado "X" de um callback de console.log** 

#### Cenário 5: Geração do Código do Tracker

* **Dado** que configurei um nome de evento
* **Quando** o sistema gera o código do tracker
* **Então** deve exibir o código no formato: `tracker.customEvent('nome_evento', {})`
* **E** deve incluir instruções de implementação

> **[Imagem 1 — transcrição]:** Screenshot de UI — bloco informativo azul-claro intitulado "🟦 Como Implementar" com lista numerada: "1. Configure o nome do evento e os dados JSON na sidebar / 2. Copie o código do tracker gerado acima / 3. Cole o código no seu projeto ou GTM no momento exato que deseja disparar o evento / 4. O cliente deverá criar a lógica para o card aparecer quando necessário".

> **[Imagem 2 — transcrição]:** Screenshot de UI — tela do editor de card na aba "Gatilho" (abas no topo: Visual, HTML/CSS, Preview, Gatilho — esta última ativa/verde). Coluna esquerda "Configurações" → "Configuração de Gatilho Imediato" com switch "Desativar Gatilho Imediato" (ligado), campo "Nome do Evento" preenchido com "trigger_card_xyz" (ajuda: "Nome que será usado no tracker personalizado"), campo "Dados do Evento (JSON)" com valor "{}" (ajuda: "Segundo argumento: Dados em formato JSON que serão enviados com o evento para consumo"), seção "Código do Tracker" exibindo `tracker.customEvent('trigger_card_xyz', {})` (com botão de copiar), e um aviso amarelo "⚠️ Importante" começando com "Adicione este código no seu código fonte ou GTM no momento exato que deseja disparar o evento / Certifique-se de que o objeto tracker esteja disponível globalmente...". Coluna direita "Preview Interativo" (badge "Canvas Editável") mostrando um card verde com "100% Seguro e Confiável / Licenciado e regulamentado" e botão "VER LICENÇAS"; abaixo, "Histórico de Alterações" ("Alteração 1 de 0"), a nota "Clique nos elementos para editá-los na sidebar", um bloco escuro "Evento disparado: tracker.customEvent('trigger_card_xyz', {})" e o mesmo bloco azul "Como Implementar" da Imagem 1. Rodapé com botões "Voltar" e "Salvar Card".

> **[Imagem 3 — transcrição]:** Screenshot de UI — caixa de aviso amarela "⚠️ Importante" (detalhe ampliado) com os bullets: "Adicione este código no seu código fonte ou GTM no momento exato que deseja disparar o evento"; "Certifique-se de que o objeto `tracker` esteja disponível globalmente"; "O segundo argumento `{}` deve conter um JSON com os dados que você quer consumir"; "Você é responsável por criar a lógica de quando e como o card deve aparecer".

## Histórico de status

- Backlog (backlog): 2025-07-03T11:47:41.747Z → 2025-07-10T12:13:55.807Z
- To-do (unstarted): 2025-07-10T12:13:55.807Z → 2025-07-22T23:04:24.877Z
- Pull Request (started): 2025-07-22T23:04:24.877Z → 2025-07-31T14:40:03.285Z
- Product Review (started): 2025-07-31T14:40:03.285Z → 2025-08-11T13:53:30.963Z
- Released (completed): 2025-08-11T13:53:30.963Z → atual

## Relações

—

## Anexos

—
