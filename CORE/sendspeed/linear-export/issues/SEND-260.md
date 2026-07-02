# SEND-260 — Importação de regras da roleta do GTM para plataforma

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | Urgent |
| Responsável | Vinicius Carneiro |
| Time | Sendspeed |
| Projeto | — |
| Labels | User Story, Melhoria, UserIn, Roleta, Regras |
| Parent | — |
| Criada | 2025-12-01T01:05:48.111Z por Vinicius Carneiro |
| Iniciada | 2025-12-01T14:19:26.051Z |
| Concluída | 2026-02-04T12:49:12.988Z |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-260-importacao-de-regras-da-roleta-do-gtm-para-plataforma |
| URL | https://linear.app/sendspeed/issue/SEND-260/importacao-de-regras-da-roleta-do-gtm-para-plataforma |

## Descrição

**Como** analista de produto

**Quero** poder definir as regras dentro da plataforma

**Para** maior autonomia no funcionamento do produto

---

Critérios de aceite:

- [ ]  A roleta precisará aparecer e todas as regras precisam funcionar.
- [X] A roleta não pode aparecer para quem já logou

(REGRA: já logou == false) (localStorage: userin_login==true).

- [X] A roleta irá aparecer após aparecer o modal de registro.

(REGRA: Elemento está visível = seletor dv.ijOkUz, input#cpf)

> **[Imagem 1 — transcrição]:** Screenshot de UI — modal de registro/cadastro do site "LIDER BLACK" (LiderBet / Liderbet). Layout em duas colunas. À esquerda, banner promocional com fundo preto e detalhes vermelhos: logo em neon vermelho "LIDER BLACK", texto grande "CADASTRE-SE E APROVEITE" e chamada "UMA NOVA OFERTA TODO O DIA!". Ilustração de um mascote (tigre/felino antropomórfico) usando óculos escuros e terno, sentado em um trono dourado, cercado por chamas. No rodapé do banner: selo "+18", logo "Lider bet" e texto vertical "JOGUE COM RESPONSABILIDADE / AUTORIZADA PELA PORTARIA SPA/MF N° SUL/2025". À direita, formulário de registro sobre fundo escuro com os campos: **CPF*** (com botão "Validar"), **E-mail*** (com ícone de informação), **Telefone*** (prefixo bandeira do Brasil "+55", com ícone de informação), **Senha*** (com ícone de olho para exibir/ocultar) e dropdown "Brasileiro (a)". Checkbox marcado com o texto "Confirmo que **tenho mais de 18 anos** e aceito os **Termos e Condições** e a **Política de Privacidade**." Botão vermelho de ação "CONCLUIR REGISTRO". No topo direito: "Já tem uma conta? **Faça login aqui**" e um "X" de fechar. No topo à esquerda um botão vermelho "Precisa de **Ajuda?**". Demonstra o modal de registro cujos seletores (div.ijOkUz / dv.ijOkUz, input#cpf) devem ser detectados como visíveis para disparar a roleta, além dos elementos que não devem ser clicados (Ajuda, login, fechar).

- [ ] Ele não pode clickar em alguns elementos.

vQI8R - Click Ajuda
.Ytn0c a - Click Login
button[data-type="register"] - Click fechar

(REGRA: Não click nos elementos acima)

> **[Imagem 2 — transcrição]:** Screenshot de UI — tela de "Configuração do acionador" (aparência de painel do Google Tag Manager / GTM, fundo branco). Campos exibidos: **Tipo de acionador** = "Visibilidade do elemento" (com ícone verde de olho). **Método de seleção** = "Seletor de CSS". **Seletor de elementos** (com ícone de ajuda "?") = `div.jOkUz, input#cpf`. **Quando disparar este acionador** = "Uma vez por página". Demonstra a configuração original do gatilho no GTM (baseado em visibilidade de elemento via seletor CSS) que está sendo importada/replicada dentro da plataforma.

- [ ]  Ele não pode ter iniciado o preenchimento do formulário.
  document.querySelector(".JiKuM")?.addEventListener("click", function(e) {
  alert("Clique detectado dentro do modal!");
  console.log("Elemento clicado:", e.target);
  }, true);

(REGRA: não click no campo de formulário)

* Se fechou o modal registro, não dispara a de roleta.
* Apenas 1x por sessão.
* Se caso todas as regras == true, dispara o modal de roleta.

---

Cenário de teste:

- [ ]  Vini entrará na plataforma e criará uma regra.
- [ ] Os critérios da regra serão: entrou na pagina > identificará o modal aberto > não clickou em nenhum dos itens do critério de aceite > não pode estar preenchendo o formulário > o Usuário tem que nunca ter loggado > caso feche o modal, cancela a ação > aparece 1x por sessão == true, dispara a roleta.
- [ ] A roleta precisará poppar em tela.

## Histórico de status
- Backlog (backlog): 2025-12-01T01:05:48.111Z → 2025-12-01T01:10:10.831Z
- Refining (backlog): 2025-12-01T01:10:10.831Z → 2025-12-01T12:04:52.419Z
- To-do (unstarted): 2025-12-01T12:04:52.419Z → 2025-12-01T14:19:26.062Z
- In Progress (started): 2025-12-01T14:19:26.062Z → 2025-12-03T17:25:38.963Z
- Pull Request (started): 2025-12-03T17:25:38.963Z → 2025-12-08T20:13:26.007Z
- In Progress (started): 2025-12-08T20:13:26.007Z → 2025-12-09T16:06:59.668Z
- Pull Request (started): 2025-12-09T16:06:59.668Z → 2025-12-09T20:36:49.496Z
- Product Review (started): 2025-12-09T20:36:49.496Z → 2026-02-04T12:49:13.001Z
- Released (completed): 2026-02-04T12:49:13.001Z → atual

## Relações
—

## Anexos
—
