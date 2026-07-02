# SEND-472 — Alterações roleta pós feedback do cliente

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | Urgent |
| Responsável | paulo.ribeiro@sendspeed.com |
| Time | Sendspeed |
| Projeto | — |
| Labels | Roleta, UserIn, User Story, Componente, Melhoria |
| Parent | — |
| Criada | 2026-05-06T17:55:13.824Z por Vinicius Carneiro |
| Iniciada | 2026-05-06T18:13:45.365Z |
| Concluída | 2026-05-08T18:07:09.956Z |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-472-alteracoes-roleta-pos-feedback-do-cliente |
| URL | https://linear.app/sendspeed/issue/SEND-472/alteracoes-roleta-pos-feedback-do-cliente |

## Descrição

Precisamos fazer algumas alterações na criação/edição dos minigames, o cliente deu o feedback que o botão da roleta não combina com o design system da plataforma.

> **[Imagem 1 — transcrição]:** Screenshot de UI mostrando um mini-game de roleta ("Wheel of Fortune") em um modal sobreposto à plataforma. A roleta tem borda dourada com luzes brancas ao redor. Fundo temático de floresta com tigres cartoon (mascote estilo jogo "Fortune Tiger"). As fatias da roleta são azuis e exibem prêmios em amarelo: "DOBRE O SEU SALDO" (fatia de topo com ícones de moedas $), "500 GIROS", "20 GIROS", "05 GIROS", "10 GIROS", "10 GIROS", "100 GIROS", "100 GIROS". No centro há um botão circular azul escrito "GIRAR". No topo da roleta há um ponteiro triangular azul. Na parte inferior há um botão azul retangular grande escrito "RESGATAR AGORA". No canto superior direito há um "x" de fechar. Esta é a versão ATUAL (antes das alterações) que o cliente reclamou não combinar com o design system.

> **[Imagem 2 — transcrição]:** Screenshot de UI da tela de configuração/edição da roleta na plataforma. Título de seção: "Botão Central (GIRAR)". Abaixo há um campo de input de texto contendo uma URL parcialmente visível: "https://ai-sendspeed.nyc3.digitaloceanspaces.com/" ao lado de um botão de upload (ícone de seta para cima). Abaixo, um preview em caixa cinza mostra a imagem do botão "GIRAR" (botão circular azul brilhante com texto "GIRAR" em branco), com um botão vermelho de "x" (remover) no canto superior direito. No rodapé aparece parcialmente o início de outra seção: "Estilo dos Textos nas Fatias". Demonstra o padrão de input de imagem já existente para outros componentes da roleta.

> **[Imagem 3 — transcrição]:** Imagem isolada de um botão retangular azul com cantos arredondados e gradiente (azul mais claro no topo, mais escuro embaixo), com o texto "RESGATAR AGORA" em branco e negrito, centralizado. É o botão de resgate atual.

> **[Imagem 4 — transcrição]:** Screenshot de UI mostrando a mesma roleta da Imagem 1 (modal com tigres, roleta dourada, fatias azuis com prêmios "DOBRE O SEU SALDO", "500 GIROS", "20 GIROS", "05 GIROS", "10 GIROS", "100 GIROS", botão central azul "GIRAR", ponteiro azul no topo). A diferença é o botão inferior: aqui está escrito "RESGATAR PRÊMIO" com estilo diferente — borda azul e fundo verde (botão outline/verde), em vez do botão azul sólido "RESGATAR AGORA". Demonstra o novo botão de resgate que aparece após a entrega do prêmio, substituindo o botão de resgate atual. Atrás do modal, à direita, veem-se partes da interface da plataforma (textos parcialmente visíveis como "nçado", "Usa", "com/").

### Critérios de aceite

* O mini game só deve ser fechado após clicar no botão de resgatar o prémio, sem tempo limite para sair da tela.
* Precisamos criar outro input de imagem para ser utilizado como botão de resgate, como temos para todos os outros componentes da roleta.

  > **[Imagem 2 — transcrição]:** (ver acima — seção "Botão Central (GIRAR)" com input de URL, botão de upload e preview do botão)
* O botão de resgate só aparecerá após a entrega do prémio e ele substituirá o botão de resgate que temos atualmente.

> **[Imagem 3 — transcrição]:** (ver acima — botão azul "RESGATAR AGORA")

> **[Imagem 4 — transcrição]:** (ver acima — roleta com botão verde "RESGATAR PRÊMIO")

## Histórico de status
- To-do (unstarted): 2026-05-06T17:55:13.824Z → 2026-05-06T18:13:45.397Z
- In Progress (started): 2026-05-06T18:13:45.397Z → 2026-05-06T19:23:48.413Z
- Product Review (started): 2026-05-06T19:23:48.413Z → 2026-05-08T18:07:09.970Z
- Released (completed): 2026-05-08T18:07:09.970Z → atual

## Relações
—

## Anexos
—
