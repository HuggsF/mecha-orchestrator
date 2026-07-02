# SEND-296 — Subir nova tela do Smart Block

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | High |
| Responsável | Vinicius Carneiro |
| Time | Sendspeed |
| Projeto | — |
| Labels | UserIn, Smart Block, Componente, User Story, Melhoria |
| Parent | — |
| Criada | 2026-01-30T13:24:48.488Z por Vinicius Carneiro |
| Iniciada | 2026-02-04T17:53:54.799Z |
| Concluída | 2026-03-02T16:06:35.740Z |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-296-subir-nova-tela-do-smart-block |
| URL | https://linear.app/sendspeed/issue/SEND-296/subir-nova-tela-do-smart-block |

## Descrição

> Como PO
>
> Quero integrar o sistema de Smar Block reformulado
>
> Para ter um sistema de configuração mais ampla diretamente na plataforma.

---

# Use Case:

* Vini quer entrar na plataforma da Userin e configurar a utilização do Smart Block para substituir a div VdKYK do modal de registro no site da jogão por outra imagem e fazer ele triggar através das regras vindo por uma UTM. Todas as configurações feitas na plataforma devem estar funcionais.

> **[Imagem 1 — transcrição]:** Screenshot de UI da tela "Editar Smart Block" (subtítulo "Imagem"), com badge azul "Ativo" no topo. Painel esquerdo com abas: Conteúdo (ativa), Seletor, Regras, Estilo. Seção "Informações Básicas": campo "Nome do Smart Block *" = "Novo block ts"; campo "Descrição" (placeholder "Descrição opcional..."); seção "Tags" (placeholder "Adicionar tag..." com botão #); slider "Prioridade: 0" com nota "Maior prioridade = exibido primeiro". Abaixo inicia a seção "Tipo de Conteúdo". Botões inferiores: "Salvar Rascunho" e "Salvar e Ativar". Painel direito "Preview" com botão "Atualizar": mostra "Seletor: eK4KH", "Posição: before", e uma área tracejada com uma imagem de um iPhone rosa/pink (frente e verso). Blocos "Configurações" (Tipo: Image, Status: Active, Prioridade: 0) e "Dispositivos" (Desktop, Tablet, Mobile — todos marcados com check). Demonstra a nova tela de edição do Smart Block do tipo Imagem e seu preview injetando a imagem no seletor eK4KH.

# Critérios de aceite:

* As regras devem estar funcionais.
* A tela antiga deve ser removida ou substituída por essa.
* A trava por empresa deve estar funcional, deve estar protegido caso puxe por outra empresa.
* Os analytics que acompanham devem estar funcionais.
* Todos os componentes devem estar funcionais tanto para Desktop quanto para Mobile
* A nova tela deve ser integrada na nossa plataforma e estar funcional junto com tudo que tem nela sem bugs que interfiram diretamente na funcionalidade da feature.
> **[Imagem 2 — transcrição]:** Screenshot de UI da aba "Regras" do Smart Block (abas no topo: Conteúdo, Seletor, Regras — selecionada, Estilo). Seção "Páginas" com campo "Exibir apenas nestas páginas" contendo `/promocao/*  /jogos/*  /casino` e a nota "Uma URL por linha. Use * como wildcard. Deixe vazio para todas as páginas." Campo "Excluir páginas" contendo `/admin/*  /login`. Seção "Dispositivos" com três toggles ativados (azul/ligado): "Desktop", "Tablet", "Mobile". Demonstra a configuração de regras de exibição por página (allowlist/blocklist) e por dispositivo.

* Esconder a aba de Seletor Visual, deixar como EM BREVE e não clicavel no front.

> **[Imagem 3 — transcrição]:** Screenshot de UI da seção "Seletor Visual". Caixa de destaque laranja "Modo Seletor Visual" com o texto "Abra seu site e clique com o botão direito no elemento onde deseja injetar o conteúdo. O seletor será capturado automaticamente!" Campo "URL do Site" (placeholder "https://seusite.com") com botão de abrir link. Botão laranja gradiente "Abrir Seletor Visual". Caixa verde "Seletor Configurado" mostrando o valor "eK4KH". Demonstra a funcionalidade de Seletor Visual (que, conforme o critério, deve passar a ser exibida como "EM BREVE" e não clicável).

* Esconder Tags e Prioridade

> **[Imagem 4 — transcrição]:** Screenshot de UI de um bloco de formulário com dois elementos: seção "Tags" com campo de entrada (placeholder "Adicionar tag...") e um botão com ícone "#"; e abaixo "Prioridade: 0" com um slider (barra azul, controle posicionado próximo ao meio) e a nota "Maior prioridade = exibido primeiro". Demonstra os campos Tags e Prioridade que, conforme o critério, devem ser escondidos.

* A aba de regras deve ser excluida.

> **[Imagem 5 — transcrição]:** Screenshot de UI mostrando a barra de abas do Smart Block: "Conteúdo", "Seletor", "Regras" (destacada/selecionada com borda azul, ícone de engrenagem), "Estilo". Abaixo, a seção "Páginas" (com campo "Exibir apenas nestas páginas" contendo `/promocao/*  /jogos/*  /casino` e nota sobre wildcard) e a seção "Dispositivos" com toggles Desktop, Tablet e Mobile ligados (azul). Demonstra a aba "Regras" que, conforme o critério, deve ser excluída.

  * No tipo de conteúdo, iremos focar apenas na imagem e HTML, o Personalizado implementaremos posteriormente então precisamos deixa-lo como EM BREVE e não clicavel no front.

> **[Imagem 6 — transcrição]:** Screenshot de UI com duas seções. Seção "Tipo de Conteúdo" com três cartões de opção: "HTML" (ícone `</>` roxo), "Imagem" (ícone de imagem azul, selecionado/destacado com borda azul) e "Personalizado" (ícone de estrelas laranja). Seção "Imagem" com campo "URL da Imagem" contendo `https://ai-sendspeed.nyc3.digitaloceanspac...` (truncado) e um botão de upload; abaixo, o preview da imagem carregada (um iPhone rosa/pink, frente e verso) com um botão vermelho "X" para remover. Demonstra o seletor de Tipo de Conteúdo (foco em Imagem e HTML; Personalizado deve ficar como "EM BREVE").

> **[Nota]:** Também foi capturada uma imagem adicional (screenshot de contexto): modal de registro do site "jogão" (formulário "Criar Conta" com campos CPF, E-mail, Telefone +55, Senha, checkbox de confirmação de +18 anos / Termos e Condições e Política de Privacidade, botão "Criar Conta", selos "Ambiente Seguro", "Dados Seguros (LGPD)", "Operador autorizado" e criativo lateral "APROVEITE CASHBACK TODOS OS DIAS! DEPOSITE E RESGATE NA HORA", "Autorizados pela portaria SPA/MF Nº 325"), lado a lado com o DevTools do Chrome (aba Elements) destacando a `<div class="VdKYK">` (a div-alvo mencionada no Use Case), com `<img alt="Jogao.bet" class="w-full" src="https://imagedelivery.net/BgH9d8bzsn4n0yi.../...1200?quality=95&format=auto">` e regras CSS `@media (min-width: 768px)` com height 750px, max-width 50vw, width 400px. Demonstra o alvo da injeção (div VdKYK do modal de registro).

## Histórico de status
- Backlog (backlog): 2026-01-30T13:24:48.488Z → 2026-01-30T14:12:24.707Z
- Refining (backlog): 2026-01-30T14:12:24.707Z → 2026-02-04T15:36:48.585Z
- To-do (unstarted): 2026-02-04T15:36:48.585Z → 2026-02-04T17:53:54.806Z
- In Progress (started): 2026-02-04T17:53:54.806Z → 2026-03-02T12:54:08.148Z
- Product Review (started): 2026-03-02T12:54:08.148Z → 2026-03-02T16:06:35.759Z
- Released (completed): 2026-03-02T16:06:35.759Z → atual

## Relações
—

## Anexos
—
