# SEND-51 — [Companiom + Journey + Plataforma] – Bugs / Ajustes e Melhorias em aberto – Semana 3 [08/2025]

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | High |
| Responsável | — |
| Time | Sendspeed |
| Projeto | — |
| Labels | Buyer |
| Parent | — |
| Criada | 2025-08-13T21:53:00.422Z por bruno.heidrich@sendspeed.com |
| Iniciada | 2025-08-20T12:13:21.775Z |
| Concluída | 2025-08-27T15:08:12.065Z |
| Arquivada | 2026-03-01T02:17:24.815Z |
| Vencimento | — |
| Branch | hugofernandes/send-51-companiom-journey-plataforma-bugs-ajustes-e-melhorias-em |
| URL | https://linear.app/sendspeed/issue/SEND-51/companiom-journey-plataforma-bugs-ajustes-e-melhorias-em-aberto-semana |

## Descrição

Lista consolidada de bugs para acompanhamento diário.

Cada bug deve ter **Status**: `A fazer` / `Em progresso` / `Concluído`.

Atualizar diariamente com progresso e pendências.

---

## ✅ Checklist de Bugs

### 1. BUG 01 – Chat do Buyer Agent

* **Status:** [PEDRO - FAZENDO]
* **Passos para reproduzir:**
  1. Quando o card pocka na tela e abrimos o chat do buyer o SCROLL DO MOUSE não funciona para subir e descer a barra de rolagem, apenas arrastando a barra lateral
* **Evidências:**
  > **[Imagem 1 — transcrição]:** Screenshot de UI (mockup mobile). Um preview de card de marketing em formato retrato dentro de uma janela de navegador. Faixa superior com degradê de verde-água para azul e um ícone de janela/tela no canto direito. O card tem fundo em degradê rosa→vermelho com título em negrito branco "Direto ao ponto.", subtítulo "Em poucos minutos eu te digo se a call gratuita é pra você." e um botão amarelo com texto preto "CHAMAR NO WHATS". Rodapé cinza claro: "Powered by SendSpeed".
* **Prioridade:** [Alta]

---

### 2. BUG 02 – Chat do Buyer

* **Status:** [PEDRO - `Concluído`]
* **Passos para reproduzir:**
  1. Dentro do chat do Buyer ainda está o nome SENDSPEED, trocar para a Logo + Nome da UserIn
* **Evidências:**
  > **[Imagem 2 — transcrição]:** Screenshot de UI (mockup mobile), essencialmente idêntico à Imagem 1. Preview de card em janela de navegador; faixa superior com degradê verde-água→azul; card com fundo rosa→vermelho, título "Direto ao ponto.", subtítulo "Em poucos minutos eu te digo se a call gratuita é pra você." e botão amarelo "CHAMAR NO WHATS". Rodapé com "Powered by SendSpeed" — evidenciando o nome SendSpeed que deve ser trocado por UserIn.
* **Prioridade:** [Alta]

---

### 3. BUG 03 – Buyer Agent

* **Status:** [PEDRO - `Concluído`]
* **Passos para reproduzir:**
  1. Está com cores aleatórias, tanto o botão quando o chat, precisamos trocar para cores da UserIn e para a logo da userIn
* **Evidências:**
  > **[Imagem 3 — transcrição]:** Screenshot de UI (recorte). Uma barra/cabeçalho horizontal fina com degradê de verde-água (esquerda) para azul (direita), com um pequeno ícone quadrado branco (janela) no canto superior direito. Sem textos legíveis — mostra a paleta de cor "aleatória" atual do topo do widget.
  >
  > **[Imagem 4 — transcrição]:** Screenshot de UI (recorte). Um botão/ícone circular flutuante com degradê verde-água→azul contendo um ícone branco de "brilhos/estrelas" (sparkles), sobre fundo escuro. Representa o botão flutuante do Buyer Agent com cores que precisam ser ajustadas para as cores da UserIn.
* **Prioridade:** [Baixa]

---

### 3. BUG 04 – Plataforma

* **Status:** [ANDREI - `Concluído`]
* **Passos para reproduzir:**
  1. Dentro da plataforma o Companiom ainda se chama Buyer Agent, precisamos trocar para o nome Companiom
* **Evidências:**
  > **[Imagem 5 — transcrição]:** Screenshot de UI (menu lateral). Item de menu expandido "Buyer Agent" (com chevron para baixo) e subitens com ícones: "Cards", "Cards 2.0", "Criar Card", "Meus Cards" (destacado/selecionado), "Resultados". Evidencia que o menu ainda usa o nome "Buyer Agent" em vez de "Companiom".
* **Prioridade:** [Média]

---

### 3. BUG 05 – Plataforma / Companiom

* **Status:** [ANDREI - `Concluído`]
* **Passos para reproduzir:**
  1. Dentro da aba onde será o Compeniom precisa estar somente:
     1. Cards (Onde esses cards são o atual cards 2.0)
     2. Meus Cards
     3. Resultados
* **Evidências:**
  > **[Imagem 6 — transcrição]:** Screenshot de UI (menu lateral), igual à Imagem 5. Menu "Buyer Agent" expandido com subitens "Cards", "Cards 2.0", "Criar Card", "Meus Cards" (selecionado) e "Resultados". Serve de referência para a reorganização dos itens que devem permanecer sob o Companiom.
* **Prioridade:** [Média]

---

### 3. BUG 06 – Plataforma / Companiom / Meus Cards

* **Status:** [ANDREI-`Concluído`]
* **Passos para reproduzir:**
  1. Dentro da aba de "Meus Cards" precisam aparecer todos os cards criados pelo cliente, para que ele possa editá-los, acessá-los, mudar status e até mesmo ser encaminhado ao analitycs especifico do card.
* **Evidências:**
  > **[Imagem 7 — transcrição]:** Screenshot de UI (página "Meus Cards"). Cabeçalho com link "← Voltar", ícone de usuário, título "Meus Cards" e subtítulo "Cards criados por você • Admin Bugfix Staging"; botão verde "+ Novo Card" à direita. Dois cartões-resumo: "Total de Cards: 0" (ícone de gráfico de barras) e "Cards Ativos: 0" (indicador verde). Barra de filtros: campo de busca "Buscar por nome, descrição...", dropdowns "Todas as categorias", "Todos os status", "Todas as prioridades", "Última..." e um botão de ordenação. Estado vazio central com ícone de usuário e textos "Você ainda não criou nenhum card" e "Comece criando seu primeiro buyer card para engajar seus visitantes." Dica azul: "Cards criados por você aparecerão apenas nesta página, enquanto todos os cards da empresa aparecem na página principal." Botão verde inferior "+ Criar Meu Primeiro Card".
* **Prioridade:** [Média]

---

### 3. BUG 07 – Plataforma / Companiom / Cards 2.0

* **Status:** [A fazer]
* **Passos para reproduzir:**
  1. Quando o cliente criou mais de 1 card e adicionou um fundo, no preview dessa página todos os cards ficaram com o mesmo fundo
  2. Apesar de nao bugar na hora de aparecer e quando clickar em editar ele fica com o fundo correto, precisamos ajustar pois isso confunde e prejudica muito a experiencia do usuário
* **Evidências:**
  > **[Imagem 8 — transcrição]:** Screenshot de UI (grade de cards "Preview do Card"). Três cards no topo e um na segunda linha, cada um com miniatura de preview (todos com o MESMO fundo roxo/púrpura de imagem de fundo, evidenciando o bug). Card 1: "gas gratuitas disponíveis" / "Termine agora ou fale comigo no Whats para garantir a sua com antecedência." / botão verde "Garantir no WhatsApp"; título "Card para lead que abandonou formulário"; descrição "Card 2.0 - Apenas 7 vagas gratuitas disponíveis"; tags "Risco de Conversão", "Ativo", "Alta"; faixa preta "⚡ Gatilho ativado - Card sendo exibido automaticamente aos usuários"; botões "Gatilho" e "Editar"; "Criado: 13/08/2025", "Atualizado: 13/08/2025". Card 2: "vida antes de dar o pró-ximo passo?" / "Se você viu que faz sentido, mas precisa de mais informações, me chama no Whats" / botão laranja "CHAMAR NO WHATS"; título "Card para lead que chegou até o fim da página"; "Card 2.0 - Alguma dúvida antes de dar o próximo passo?"; tags "Risco de Dúvida", "Ativo", "Média". Card 3: "Direto ao ponto." / "Em poucos minutos eu te digo se a call gratuita é pra você." / botão contornado amarelo "CHAMAR NO WHATS"; título "Exit Intent Clássico"; "Card 2.0 - Direto ao ponto."; tags "Risco de Saída", "Ativo", "Crítica". Card 4 (2ª linha): "Espere! Não vá embora ainda" / "Oferta especial para você" / "adsdasd" / botão verde "VER OFERTA"; título "Exit Intent Clássico".
  >
  > **[Imagem 9 — transcrição]:** Screenshot de UI (editor de card). Painel esquerdo "Configurações" com campo "Nome do Card" = "Card para lead que chegou até o fim da pági..." e lista de seções: "Conteúdo" (3/3, check verde), "Estilo & Cores" (1 font), "Botão & Ações", "Countdown", "Fundo e Cores", "HTML Customizado", "IA" (badge "Em breve"). À direita, "Preview do Card" com botões "← Voltar", "Carregar" (verde), "Finalizar" (azul); faixa "✅ Modo Ativo — Card será salvo como ativo (visível aos usuários)" com toggle. Preview grande com fundo roxo: título "Alguma dúvida antes de dar o próximo passo?", subtítulo "Se você viu que faz sentido, mas precisa de mais informações, me chama no Whats" e botão laranja "CHAMAR NO WHATS". Rótulo "Template Interativo".
  >
  > **[Imagem 10 — transcrição]:** Screenshot de UI (grade de cards "Preview do Card"), variação da Imagem 8 com miniaturas maiores. Mesmos quatro cards ("Card para lead que abandonou formulário" com botão verde "Garantir no WhatsApp"; "Card para lead que chegou até o fim da página" com botão laranja "CHAMAR NO WHATS"; "Exit Intent Clássico" com botão amarelo contornado "CHAMAR NO WHATS"; "Espere! Não vá embora ainda / Oferta especial para você / adsdasd" com botão verde "VER OFERTA"). Todas as miniaturas exibem o mesmo fundo roxo, reforçando o bug de fundo compartilhado; mesmas tags e datas 13/08/2025.
  >
  > **[Imagem 11 — transcrição]:** Screenshot de UI (editor de card). Painel esquerdo "Configurações", "Nome do Card" = "Card para lead que abandonou formulário"; seções "Conteúdo" (3/3 ✔), "Estilo & Cores" (2 fonts), "Botão & Ações", "Countdown", "Fundo e Cores", "HTML Customizado", "IA (Em breve)". À direita "Preview do Card" com "← Voltar", "Carregar", "Finalizar" e faixa "✅ Modo Ativo". Preview com fundo escuro/vermelho: título "Apenas 7 vagas gratuitas disponíveis", subtítulo "Termine agora ou fale comigo no Whats para garantir a sua com antecedência." e botão verde "Garantir no WhatsApp". Rótulo "Template Interativo".
* **Prioridade:** [Alta]

---

### 3. BUG 08 – Plataforma / Companiom / Cards 2.0

* **Status:** [ANDREI - `Concluído`]
* **Passos para reproduzir:**
  1. Precisamos melhorar o preview do card e como eles aparecem aqui, para o usuário ter uma experiencia satisfatoria.
  2. Pode deixar o grid dividido em 2 ou até mesmo unico caso precise para que o preview do card tenha tamanho suficiente para aparecer completo na tela.
* **Evidências:**
  > **[Imagem 12 — transcrição]:** Screenshot de UI (tela inicial da plataforma SendSpeed). Barra superior com logo "SendSpeed", seletor de idioma "Português (Brasil)" (bandeira do Brasil) e avatar/conta "Admin Bugfix Staging — BUGFIX TREINAMENTOS STAGING". Menu lateral esquerdo com itens: Início, Segmentos, Campanhas, Conversões, Fluxos, Análises, Dados e Integrações, Logs de Atividade, Conteúdo, Treinar IA, Audiência (>), Buyer Agent (>), Configurações. Conteúdo: título "Olá Admin Bugfix Staging! Vamos configurar seu sucesso." e "Complete os passos abaixo para começar a usar todos os recursos."; botão "Configurar workspace". Bloco "Progresso da integração" com stepper de 4 etapas: 1 "Conectar dados" (concluído/check verde), 2 "Criar segmento" (atual, verde), 3 "Definir campanhas", 4 "Verificar automações"; botão verde "Continuar configuração". Abas "Audiência / Campanhas / Atividade" (Campanhas ativa). Seção "Campanhas de Marketing" com botão verde "Nova Campanha", subtítulo "Gerencie e acompanhe suas campanhas de marketing." e caixa "Campanhas ativas" com estado vazio: ícone de envelope, "Nenhuma campanha encontrada", "Você ainda não criou nenhuma campanha. Clique no botão acima para criar sua primeira campanha." e botão verde "Criar Primeira Campanha". No rodapé aparece a URL "https://platform-stg-userin-ai.fly.dev".
* **Prioridade:** [Alta]

---

### 3. BUG 09 – Editor de Cards 2.0 -> Bugs na Edição

* **Status:** [A fazer]
* **Passos para reproduzir:**
  1. Foi notado pelo cliente que as fontes do botão, nao se adaptam a negrito e ao peso da fonte
  2. Toda vez que eu clico em um elemento a aba de conteudo abre, prejudicando a experiencia do usuário (quando clickar no elemento, deve abrir o melhor componente que tenha a ver com ele. Ex.: Background abre fundo e cores, button, abre botoes e acoes, textos abrem estilos e cores)
  3. Dentro de button a parte de visual básico, está com funcionalidades de tamanho disfuncionais
  4. Dentro de button a animacao ripple nao muda nada, podendo ser desativada
  5. Dentro de button a animacao scale e bounce tem quase o mesmo efeito, podendo ser centralizada em uma unica acao
* **Evidências:**
* **Prioridade:** [Média]

---

### 3. BUG 10 – Editor de Cards 2.0 -> Bugs no Parser

* **Status:** [A fazer]
* **Passos para reproduzir:**
  1. Quando eu colo um HTML de um card já criado, o parser acaba nao identificando alguns elementos.
  2. Nos ultimos testes que fiz, percebi que varia de card para card e edicao para edicao.
  3. Mas em grande parte se tem um elemento text, ele nao consegue ativar a chave sozinha
  4. O button vem com formatacoes erradas
  5. E alguns elementos de texto, como sombras, edicao de pesos e outro elementos, as vezes vem faltando
* **Evidências:**
* **Prioridade:** [Baixa]

---

### 3. BUG 11 – Plataforma / Audiência

* **Status:** [PEDRO - `Concluído`]
* **Passos para reproduzir:**
  1. O Menu Audiência deveria se chamar: Journey
* **Evidências:**
  > **[Imagem 13 — transcrição]:** Screenshot de UI (submenu lateral). Item "Audiência" expandido (chevron para baixo) com subitens e ícones: "Visão Geral", "Visitantes", "Contatos". Evidencia o menu "Audiência" que deve ser renomeado para "Journey".
* **Prioridade:** [Média]

---

### 3. BUG 12 – Plataforma / ID Visual

* **Status:** [PEDRO - `Concluído`]
* **Passos para reproduzir:**
  1. Precisamos trocar nossa plataforma para o nome UserIn
  2. Precisamos adicionar o logo da UserIn
  3. Precisamos que a plataforma siga o KV da UserIn
  4. Precisamos garantir que em nenhum momento da plataforma seja citado o nome SendSpeed
* **Evidências:**
  > **[Imagem 14 — transcrição]:** Screenshot de UI (submenu "Audiência" expandido), similar à Imagem 13, com subitens "Visão Geral", "Visitantes", "Contatos" (ícones à esquerda). Referência ao branding/menu atual.
  >
  > **[Imagem 15 — transcrição]:** Screenshot de UI (tela de login SendSpeed). Fundo verde-menta suave. Centralizado: logo "SendSpeed" (ícone verde + wordmark preto) e subtítulo "Entre na sua conta para continuar". Cartão branco "Fazer Login" com texto "Entre com suas credenciais para acessar o dashboard"; campo "E-mail" preenchido com "admin-userin@staging.userin.ai" (ícone de envelope); campo "Senha" com pontos ocultos e ícone de olho; botão verde "Entrar". Abaixo: "Não tem uma conta? **Entre em contato**". Evidencia a marca SendSpeed no login que deve migrar para UserIn.
* **Prioridade:** [Média]

---

### 3. BUG 13 – Buyer Agent

* **Status:** [PEDRO - `Concluído`]
* **Passos para reproduzir:**
  1. Quando o preview pocka ele fica com esse fundo, precisamos remover e ele soltar apenas o card preview
  2. Dentro do card preview precisa vir apenas:
     1. Tittle
     2. *Sub-Tittle*
     3. Button
     4. E futuramente o Countdown
  3. Outros elementos nao podem vir no preview.
* **Evidências:**
  > **[Imagem 16 — transcrição]:** Screenshot de UI (preview flutuante pequeno). Sobre fundo escuro (verde-oliva/preto), um card compacto com borda em degradê (rosa→azul) e fundo interno rosa/vermelho: título em negrito "Direto ao ponto.", subtítulo truncado "Em poucos minutos eu te digo se a call gratuita é pra…" e botão contornado amarelo "CHAMAR NO WHATS". Mostra o "fundo" indesejado ao redor do preview que deve ser removido.
* **Prioridade:** [Alta]

---

### 3. BUG 14 – Buyer Agent / Preview

* **Status:** [PEDRO - `Concluído`]
* **Passos para reproduzir:**
  1. Aumentar tamanho do preview, mantendo responsividade de dispositivos, para que chame mais a atenção do usuário.
* **Evidências:**
  > **[Imagem 17 — transcrição]:** Screenshot de UI. Sobre um fundo amarelo/dourado (parcialmente visível à esquerda, com o texto grande "AP" cortado), abre-se um painel/preview à direita: faixa superior degradê verde-água→azul com ícone de janela; card com fundo rosa→vermelho, título "Direto ao ponto.", subtítulo "Em poucos minutos eu te digo se a call gratuita é pra você." e botão contornado amarelo com texto "CHAMAR NO WHATS" (quebrado em 3 linhas). Rodapé "Powered by SendSpeed". Ilustra o tamanho atual do preview que deve ser aumentado.
* **Prioridade:** [Alta]

---

### 3. BUG 15 – Buyer Agent / Chat

* **Status:** [PEDRO - `Concluído`]
* **Passos para reproduzir:**
  1. Aumentar o tamanho da caixa de chat, mantendo responsividade de dispositivos, para que de para ler de forma correta o card, mantendo suas proporcoes mais "quadradas"
* **Evidências:**
  > **[Imagem 18 — transcrição]:** Screenshot de UI (preview compacto). Card pequeno com borda em degradê (rosa/roxo→azul) e fundo roxo escuro: título em negrito "Alguma dúvida antes de dar o próximo…" (truncado), subtítulo "Se você viu que faz sentido, mas precisa de mais…" (truncado) e botão laranja "CHAMAR NO WHATS". Demonstra as proporções atuais da caixa de chat que devem ser aumentadas/ajustadas.
* **Prioridade:** [Alta]

---

## 📌 Observações de Daily

- [ ] BUG 01 – [pendente - PEDRO]
- [X] MELHORIA 02 – [pendente - PEDRO]
- [X] MELHORIA 03 – [pendente - PEDRO]
- [X] MELHORIA 04 – [pendente - ANDREI]
- [X] MELHORIA 05 – [pendente - ANDREI]
- [X] MELHORIA 06 – [pendente - ANDREI]
- [ ] BUG 07 – [pendente - Andrei]
- [X] MELHORIA 08 – [pendente - ANDREI]
- [ ] MELHORIA 09 – [ANDREI]
- [ ] MELHORIA 10 – [pendente]
- [X] MELHORIA 11 – [pendente - PEDRO]
- [X] MELHORIA 12 – [pendente - PEDRO]
- [X] MELHORIA 13 – [pendente - PEDRO]
- [X] MELHORIA 14 – [pendente - PEDRO]
- [X] MELHORIA 15 – [pendente - PEDRO]

## Histórico de status
- Backlog (backlog): 2025-08-13T21:53:00.422Z → 2025-08-13T21:57:55.882Z
- To-do (unstarted): 2025-08-13T21:57:55.882Z → 2025-08-20T12:13:21.761Z
- In Progress (started): 2025-08-20T12:13:21.761Z → 2025-08-22T12:08:04.899Z
- Product Review (started): 2025-08-22T12:08:04.899Z → 2025-08-27T15:08:12.044Z
- Released (completed): 2025-08-27T15:08:12.044Z → atual

## Relações
—

## Anexos
—
