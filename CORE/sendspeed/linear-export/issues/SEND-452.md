# SEND-452 — Feature: Preview fiel do RCS no editor de template e suporte a emojis

| Campo | Valor |
| -- | -- |
| Status | To-do (unstarted) |
| Prioridade | No priority |
| Responsável | paulo.ribeiro@sendspeed.com |
| Time | Sendspeed |
| Projeto | — |
| Labels | User Story, UserIn, Melhoria |
| Parent | — |
| Criada | 2026-04-14T11:42:51.050Z por Vinicius Carneiro |
| Iniciada | — |
| Concluída | — |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-452-feature-preview-fiel-do-rcs-no-editor-de-template-e-suporte |
| URL | https://linear.app/sendspeed/issue/SEND-452/feature-preview-fiel-do-rcs-no-editor-de-template-e-suporte-a-emojis |

## Descrição

## História

Como gestor, quero ver exatamente como minha mensagem RCS vai aparecer no celular do destinatário enquanto a crio, e quero poder adicionar emojis para deixar a mensagem mais expressiva.

---

## O problema hoje

O preview atual do template RCS não representa fielmente como a mensagem vai aparecer no celular — o que o gestor vê na tela e o que o destinatário recebe são coisas diferentes. Além disso, não há como inserir emojis diretamente pelo editor, o que limita o tom e o engajamento das mensagens.

---

## O que precisa acontecer

### Preview fiel

1. O mockup do celular no editor mostra a mensagem exatamente como ela vai aparecer no app de mensagens do destinatário
2. Qualquer alteração no texto, imagem ou botões reflete instantaneamente no preview
3. O preview mostra todos os elementos no lugar certo: imagem no topo, texto no meio, botões na parte inferior do card
4. O tamanho da fonte, as quebras de linha e o limite de caracteres são respeitados no preview

### Suporte a emojis

1. Um botão de emoji fica visível no campo de texto da mensagem
2. Ao clicar, abre um seletor de emojis
3. O emoji selecionado é inserido na posição do cursor no texto
4. O emoji aparece no preview em tempo real
5. O emoji é enviado corretamente na mensagem RCS e aparece no celular do destinatário

---

## O que o gestor vê

**No editor:**

* Mockup de celular ao lado do formulário, atualizado em tempo real
* Imagem (se houver), texto e botões posicionados como no RCS real
* Botão 😀 no campo de texto para abrir o seletor de emojis
* Contador de caracteres que conta emojis corretamente

**Exemplo de mensagem com emoji:**

> 🔥 Oferta especial para você! Acesse agora e garanta seu bônus de boas-vindas 🎁

---

## Critérios de aceite

- [ ] Preview reflete fielmente a mensagem final: imagem, texto e botões no lugar certo
- [ ] Qualquer alteração no editor atualiza o preview instantaneamente
- [ ] Botão de emoji disponível no campo de texto
- [ ] Seletor de emojis abre ao clicar no botão
- [ ] Emoji é inserido na posição do cursor
- [ ] Emoji aparece corretamente no preview
- [ ] Emoji é enviado e exibido corretamente no celular do destinatário
- [ ] Contador de caracteres leva emojis em conta

---

## Cenários

- [ ] Digito texto → preview atualiza em tempo real
- [ ] Adiciono imagem via link → imagem aparece no topo do card no preview
- [ ] Adiciono botão → botão aparece na parte inferior do card no preview
- [ ] Clico no botão de emoji → seletor abre
- [ ] Seleciono 🔥 com cursor no meio do texto → emoji inserido naquela posição
- [ ] Preview mostra o emoji → destinatário recebe a mensagem com o emoji
- [ ] Template salvo com emoji → ao reabrir para editar, emoji continua no texto

---

## Priorização RICE — Score: 18.3

| Reach | Impact | Confidence | Effort | Score |
| -- | -- | -- | -- | -- |
| 8 | 2 (high) | 100% | 1.5 semanas | **18.3** |

**Justificativa:** Todo gestor que cria templates RCS é impactado. Preview incorreto gera retrabalho e erros nos disparos — o gestor envia achando que vai ficar de um jeito e o destinatário recebe diferente. Emojis aumentam engajamento em mensagens de marketing e são esperados como funcionalidade básica de qualquer editor de mensagens. Ambos são ajustes de interface com impacto imediato na experiência de criação.

## Histórico de status
- Backlog (backlog): 2026-04-14T11:42:51.050Z → 2026-04-14T12:48:54.383Z
- Refining (backlog): 2026-04-14T12:48:54.383Z → 2026-04-14T13:23:50.923Z
- To-do (unstarted): 2026-04-14T13:23:50.923Z → 2026-04-14T13:23:54.228Z
- Refining (backlog): 2026-04-14T13:23:54.228Z → 2026-04-14T13:23:58.047Z
- To-do (unstarted): 2026-04-14T13:23:58.047Z → atual

## Relações
—

## Anexos
—
