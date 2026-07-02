# SEND-297 — Subir nova feature de Mini Games

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | High |
| Responsável | Vinicius Carneiro |
| Time | Sendspeed |
| Projeto | — |
| Labels | Mini Games, Componente, User Story, UserIn, Implementação |
| Parent | — |
| Criada | 2026-01-30T13:43:28.648Z por Vinicius Carneiro |
| Iniciada | 2026-02-04T17:53:58.613Z |
| Concluída | 2026-03-02T16:06:28.656Z |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-297-subir-nova-feature-de-mini-games |
| URL | https://linear.app/sendspeed/issue/SEND-297/subir-nova-feature-de-mini-games |

## Descrição

> Como PO
>
> Quero integrar o sistema de Smart Block reformulado
>
> Para ter um sistema de configuração mais ampla diretamente na plataforma.

---

# Use Case

* Vini irá criar uma roleta na plataforma com todas as configurações disponíveis e fazer ela ativar juntamente com o sistema de regras, o mini game deve aparecer em tela e a jogatina deve ser possível.

### Informações importantes:

* Doc de funcionamento dos mini games: [https://github.com/sendspeed0/platform-backend/blob/pedro-components/howto-component-works.md](<https://github.com/sendspeed0/platform-backend/blob/pedro-components/howto-component-works.md>)

# Critérios de aceite:

* As regras devem estar funcionais
* Os analytics que acompanham devem estar funcionais.
* A trava por empresa deve estar funcional, deve estar protegido caso puxe por outra empresa.
* Todos os componentes devem estar funcionais tanto para Desktop quanto para Mobile
* A tela de configuração do Mini Games deve estar totalmente funcional e sem bugs que interfiram diretamente na funcionalidade da feature.

> **[Imagem 1 — transcrição]:** Screenshot de UI da tela de edição de Mini Game na aba "Prêmios" (abas no topo: Geral, Visual, Prêmios — selecionada, Config, Avançado). Cabeçalho "Prêmios (3)" com botão "+ Adicionar Prêmio". Lista de prêmios em cartões, cada um com: placeholder de "Imagem" (área tracejada), campo "Nome" = "50 Giros", campo "syncTag" = "userin_new..." (truncado), campo "Probabilidade" (primeiro cartão = "0,5" com setas de incremento; segundo cartão = "0,7"), "Cor da fatia" (swatch azul/roxo e campo hex "#636..." truncado), e um toggle "Vence" ligado (azul), com ícone de lixeira vermelho. Demonstra a configuração de prêmios da roleta com nome, syncTag, probabilidade (em decimal), cor da fatia e flag de vitória.

* Apenas Mini Game da roleta deve estar funcional, 0s outros Mini Games ficarão ocultos.
* Corrigir o botão de copiar no ID do Minigame.

> **[Imagem 2 — transcrição]:** Screenshot de UI de um card "ID do Minigame" (caixa com borda amarela/creme) exibindo o valor `minigame_1769541328612_zeemsoydq` e um botão flutuante "Copiar" (com ícone de clipboard) sobreposto à direita. Demonstra o botão de copiar do ID do Minigame que precisa de correção.

Adicionar o botão de Girar no preview

> **[Imagem 3 — transcrição]:** Screenshot de UI do painel "Preview" (badge "Roleta" no canto superior direito) mostrando a roleta renderizada: uma roda de fortuna com 8 fatias, tema aquático/azul-turquesa com personagens (tigre, cobra/dragão, hamster, etc.) e o texto "50 GIROS" repetido nas fatias, ponteiro/agulha no topo, logo "jogão" no rodapé da imagem. Abaixo, dois botões de alternância de dispositivo: "Desktop" (laranja/selecionado, ícone de monitor) e "Mobile" (ícone de celular). Nesta versão o preview NÃO tem botão "Girar" no centro (contexto do pedido de adicionar o botão de Girar).

> **[Imagem 4 — transcrição]:** Screenshot de UI da tela completa "Editar Mini Game" (subtítulo "Roleta - Configure todos os detalhes"), com botões "Voltar", "Preview" e "Salvar" (laranja) no topo. Painel esquerdo com abas Geral (ativa), Visual, Prêmios, Config, Avançado. Campos: "Nome Interno *" (placeholder "Minha roleta"), "Nome do Jogo *" = "Teste" (nota "Nome visível para usuários"). Um dropdown de tipo de jogo está aberto, com as opções: "Roleta" (selecionada/check, destaque laranja), "Raspadinha", "Caixa Misteriosa", "Slot Machine", "Prize Drop (Plinko)", "Vira a Carta", "Roda da Fortuna". Abaixo, campo de tipo "Roleta" e campo "Status" = "Ativo". Seção "Textos" (Título, Subtítulo). Painel direito "Preview" com a roleta (mesma roda de fortuna com 50 GIROS), botões "Desktop" (laranja) e "Mobile", e o card "ID do Minigame" = `minigame_1769541328612_zeemsoydq` com botão "Copiar". Demonstra a variedade de tipos de mini game disponíveis (apenas Roleta funcional, os demais ocultos conforme critério).

* Alterar o Sincronizar da aba de Config para a aba de Prêmios

> **[Imagem 5 — transcrição]:** Screenshot de UI da seção "Sincronização de Prêmios" (ícone de presente). Card "Sincronizar com Smartico" com a descrição "Ao resgatar, envia a syncTag do prêmio como client_action para a Smartico" e um toggle desligado (cinza) à direita. Demonstra a opção "Sincronizar com Smartico" que deve ser movida da aba Config para a aba Prêmios.

* Alterar probabilidade de decimal para % mantendo a conversão de decimal para o backend.

> **[Imagem 6 — transcrição]:** Screenshot (close-up) da roleta renderizada no site, mostrando o centro da roda com um botão azul-turquesa circular escrito "GIRAR". Ao redor, as 8 fatias com personagens temáticos (tigre, dragão/cobra, hamster) e o texto "50 GIROS" em cada fatia. Demonstra o botão "GIRAR" central que deve ser adicionado ao preview e a aparência final do mini game jogável.

* Dado que eu subo a roleta com apenas 1 imagem no lugar das fatias, vamos considerar o calculo a partir da direita agulha sendo a primeira fatia e a esquerda da agulha a ultima. Padronizar a quantidade de prêmios de acordo com a quantidade total de fatias.
* É importante que na probabilidade seja possível colocarmos números como 0,000001%.
* Verificar a segurança do Mini Game para evitar o hacking para alteração do prêmio.

## Histórico de status
- Backlog (backlog): 2026-01-30T13:43:28.648Z → 2026-01-30T14:12:20.143Z
- Refining (backlog): 2026-01-30T14:12:20.143Z → 2026-02-04T15:36:54.962Z
- To-do (unstarted): 2026-02-04T15:36:54.962Z → 2026-02-04T17:53:58.629Z
- In Progress (started): 2026-02-04T17:53:58.629Z → 2026-03-02T12:54:06.020Z
- Product Review (started): 2026-03-02T12:54:06.020Z → 2026-03-02T16:06:28.676Z
- Released (completed): 2026-03-02T16:06:28.676Z → atual

## Relações
—

## Anexos
—
