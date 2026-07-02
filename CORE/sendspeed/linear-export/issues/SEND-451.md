# SEND-451 — Feature: Campo de imagem via link na criação de template RCS

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | Urgent |
| Responsável | Vinicius Carneiro |
| Time | Sendspeed |
| Projeto | — |
| Labels | Melhoria, UserIn, User Story |
| Parent | — |
| Criada | 2026-04-14T11:42:19.105Z por Vinicius Carneiro |
| Iniciada | 2026-04-14T18:50:15.637Z |
| Concluída | 2026-04-24T13:41:40.177Z |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-451-feature-campo-de-imagem-via-link-na-criacao-de-template-rcs |
| URL | https://linear.app/sendspeed/issue/SEND-451/feature-campo-de-imagem-via-link-na-criacao-de-template-rcs |

## Descrição

## História

Como gestor, quero poder adicionar uma imagem ao meu template RCS colando um link direto, para que a mensagem chegue com visual rico ao destinatário sem precisar fazer upload de arquivo.

---

## O problema hoje

Na criação de template RCS não há campo para adicionar imagem. A mensagem é enviada apenas como texto, perdendo o principal diferencial do RCS em relação ao SMS.

---

## O que precisa acontecer

1. Na tela de criação de template RCS, aparece um campo **"URL da imagem"**
2. O gestor cola o link da imagem (ex: `https://meusite.com/banner-promo.jpg`)
3. O preview da mensagem atualiza e mostra como a imagem vai aparecer no celular do destinatário
4. Ao enviar, a imagem é exibida no topo da mensagem RCS

---

## O que o gestor vê

**No editor de template RCS:**

* Campo de texto: *"URL da imagem (opcional)"*
* Placeholder: `https://exemplo.com/imagem.jpg`
* Formatos aceitos indicados embaixo do campo: JPG, PNG, GIF — máx. 1MB recomendado
* Preview ao vivo: assim que o link é colado, a imagem aparece no mockup do celular ao lado
* Se o link estiver quebrado ou inválido, aparece um aviso discreto: *"Não foi possível carregar a imagem. Verifique o link."*

**Na mensagem recebida:**

* Imagem aparece no topo do card RCS, seguida do texto e dos botões

---

## Critérios de aceite

- [ ] Campo de URL de imagem disponível na criação e edição de template RCS
- [ ] Preview atualiza em tempo real ao colar o link
- [ ] Se o link for inválido, exibe aviso sem bloquear o salvamento
- [ ] Campo é opcional — templates sem imagem continuam funcionando normalmente
- [ ] A URL é salva no template e enviada corretamente ao provedor RCS no momento do disparo
- [ ] Na listagem de templates, templates com imagem mostram um ícone ou thumbnail indicando que têm imagem

---

## Cenários

- [ ] Colo link válido de JPG → imagem aparece no preview e é enviada com a mensagem
- [ ] Colo link inválido → aviso exibido, consigo salvar o template mesmo assim
- [ ] Deixo campo vazio → template salvo e enviado normalmente sem imagem
- [ ] Edito um template existente e adiciono imagem → próximo envio já inclui a imagem
- [ ] Edito um template com imagem e removo a URL → próximo envio vai sem imagem

---

## Priorização RICE — Score: 16.0

| Reach | Impact | Confidence | Effort | Score |
| -- | -- | -- | -- | -- |
| 8 | 2 (high) | 100% | 1 semana | **16.0** |

**Justificativa:** Toda empresa que usa RCS perde o principal diferencial do canal sem imagem — o RCS é escolhido justamente pelo visual rico. É uma melhoria pequena de implementar (campo + preview + passação do dado ao provedor) com impacto alto na qualidade das mensagens enviadas.

## Histórico de status
- Backlog (backlog): 2026-04-14T11:42:19.105Z → 2026-04-14T12:49:00.033Z
- Refining (backlog): 2026-04-14T12:49:00.033Z → 2026-04-14T13:24:46.249Z
- To-do (unstarted): 2026-04-14T13:24:46.249Z → 2026-04-14T18:50:15.645Z
- In Progress (started): 2026-04-14T18:50:15.645Z → 2026-04-15T20:07:05.941Z
- Pull Request (started): 2026-04-15T20:07:05.941Z → 2026-04-16T18:14:52.973Z
- Product Review (started): 2026-04-16T18:14:52.973Z → 2026-04-24T13:41:40.190Z
- Released (completed): 2026-04-24T13:41:40.190Z → atual

## Relações
—

## Anexos
—
