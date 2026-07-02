# SEND-328 — 🐞 - Menu de configuração da box no fluxo.

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | Urgent |
| Responsável | pedro.iegler@sendspeed.com |
| Time | Sendspeed |
| Projeto | — |
| Labels | User Story, UserIn, Jornadas, Bug |
| Parent | — |
| Criada | 2026-02-13T17:58:54.237Z por Vinicius Carneiro |
| Iniciada | 2026-02-19T15:41:24.459Z |
| Concluída | 2026-02-20T16:35:32.710Z |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-328--menu-de-configuracao-da-box-no-fluxo |
| URL | https://linear.app/sendspeed/issue/SEND-328/menu-de-configuracao-da-box-no-fluxo |

## Descrição

## 📍 Onde ocorre

Durante a configuração do fluxo de uma jornada

## 🔁 Passo a Passo

1. Criar uma jornada nova.
2. Adicionar uma box no fluxo e começar a configurar.
3. Durante a configurar deletar a box.

## ❌ Resultado Atual

Quando a box é deletada, via atalho do teclado o menu de configuração permanece aberto na esquerda.

## ✅ Resultado Esperado

Quando a box for deletada, via atalho do teclado, o menu deve fechar automaticamente.

**OBS**: Esse comportamento ja é feito quando a box é deletada via X

> **[Imagem 1 — transcrição]:** Screenshot de UI do builder de jornadas (canvas). Mostra dois nós verdes **"Trigger Manual" / trigger** com o texto "Clique para configurar", ligados por uma linha tracejada a um nó azul-ciano **"Executar JavaScript" / action** exibindo o código `alert('teste2');`. O nó ativo aparece com borda azul destacada e um botão vermelho de fechar (X) no canto superior direito. Painel lateral esquerdo "Componentes — Clique para adicionar ao canvas" com a seção "Ações Insite": Exibir Modal (Exibe um Smart Modal para o usuário), Personalizar Site (Injeta um SmartBlock personalizado no site do usuário), Exibir Minigame (roleta, scratch, quiz), Injetar HTML (Injeta conteúdo HTML customizado), Executar JavaScript (Executa código JavaScript customizado), Enviar Evento (SmartTrack, Meta Pixel, GA, etc.). Topo com título da jornada "Teste trigger manual dual flux", badge verde "Ativo" e botões: InSite, Organizar, Importar, Exportar, Simular, Pausar, toggle "Auto" e botão azul "Salvar". Cabeçalho de conta "Admin YAD STORE / YAD STORE" e idioma "Português (Brasil)".

## 🧪 Evidências

Resultado atual:

> **[Imagem 2 — transcrição]:** Screenshot de UI (mesmo builder) — resultado atual. É um recorte ampliado (zoom) do nó azul-ciano **"Executar JavaScript" / action** com o texto "Clique para configurar". No canto superior direito há o botão vermelho de fechar (X) destacado/circulado em laranja (marcação manual), indicando que o menu/box permanece indevidamente aberto após deletar via atalho de teclado.

> **[Imagem 3 — transcrição]:** Screenshot de UI mostrando o painel lateral direito aberto de **"Executar JavaScript" (action) — Executa código JavaScript customizado**. Faixa informativa: "Executa JavaScript no navegador do usuário — O código será executado quando esta ação for acionada". Aviso amarelo **"Atenção — Use com cuidado. Erros no código podem afetar a experiência do usuário."** Campo **"Código JavaScript"** com `alert('teste1');`. Nota "Variáveis disponíveis: window.__SmartTrack, window.__JourneyInsiteEngine". Bloco escuro "Preview: alert('teste1');". Rodapé com botões "Clonar", "Cancelar" e "Salvar Configuração". Ao fundo, o canvas com nós "Trigger Manual" e "Executar JavaScript" (alert('teste2')). Painel esquerdo mostra gatilhos: Evento (Em breve), Webhook (Em breve), Regra da Plataforma, Trigger Manual e condições "Tem Tag?", "Atributo do Usuário".

Resultado esperado:

> **[Imagem 4 — transcrição]:** Screenshot de UI muito semelhante à Imagem 3 — resultado esperado. Painel lateral direito de **"Executar JavaScript" (action)** com campo "Código JavaScript" contendo `alert('teste1');` (campo com foco/borda azul), aviso amarelo de "Atenção", nota de variáveis disponíveis (window.__SmartTrack, window.__JourneyInsiteEngine) e bloco "Preview: alert('teste1');". Rodapé com "Clonar", "Cancelar" e "Salvar Configuração". No canvas à esquerda, dois nós verdes "Trigger Manual" e dois nós azul-ciano "Executar JavaScript" (alert('teste1') selecionado com borda azul e botão X; alert('teste2') ao lado). Painel esquerdo com GATILHOS (Evento — Em breve, Webhook — Em breve, Regra da Plataforma, Trigger Manual) e CONDIÇÕES (Tem Tag?, Atributo do Usuário).

## Histórico de status
- Backlog (backlog): 2026-02-13T17:58:54.237Z → 2026-02-13T19:43:36.172Z
- To-do (unstarted): 2026-02-13T19:43:36.172Z → 2026-02-19T15:41:24.467Z
- In Progress (started): 2026-02-19T15:41:24.467Z → 2026-02-19T15:42:02.719Z
- Pull Request (started): 2026-02-19T15:42:02.719Z → 2026-02-19T17:01:09.522Z
- Product Review (started): 2026-02-19T17:01:09.522Z → 2026-02-19T17:04:20.779Z
- Pull Request (started): 2026-02-19T17:04:20.779Z → 2026-02-19T17:04:34.433Z
- Product Review (started): 2026-02-19T17:04:34.433Z → 2026-02-20T16:35:32.721Z
- Released (completed): 2026-02-20T16:35:32.721Z → atual

## Relações
—

## Anexos
—
