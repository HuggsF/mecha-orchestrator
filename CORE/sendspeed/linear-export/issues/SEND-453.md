# SEND-453 — Feature: Envio de card avançado no RCS da Userin

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | Urgent |
| Responsável | Vinicius Carneiro |
| Time | Sendspeed |
| Projeto | — |
| Labels | UserIn, User Story, Implementação |
| Parent | — |
| Criada | 2026-04-14T11:43:48.801Z por Vinicius Carneiro |
| Iniciada | 2026-04-14T16:08:10.898Z |
| Concluída | 2026-05-08T18:07:03.589Z |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-453-feature-envio-de-card-avancado-no-rcs-da-userin |
| URL | https://linear.app/sendspeed/issue/SEND-453/feature-envio-de-card-avancado-no-rcs-da-userin |

## Descrição

## História

Como gestor, quero poder enviar mensagens RCS com card avançado (imagem grande, título, descrição e botões) diretamente pelo RCS da Userin, para aproveitar todo o potencial do canal que já está disponível na Send.

---

## Contexto

A infraestrutura de envio já suporta card avançado no lado da Send. O que falta é refletir essa opção na Userin — no envio desses templates de RCS.

---

## O problema hoje

Ao enviar o um RCS na Userin, o gestor só tem a opção de texto simples e carrossel. Não há como enviar um card rico com imagem, título e botões num layout estruturado, nem como anexar um arquivo — mesmo que a Send já saiba enviar esses formatos.

---

## O que precisa acontecer

### Card avançado

O gestor escolhe o tipo de mensagem **"Card avançado"** e preenche:

* **Imagem** — URL da imagem que vai aparecer no card (pode ser banner grande)
* **Título** — linha em destaque (ex: "Oferta exclusiva para você")
* **Descrição** — texto complementar abaixo do título
* **Botões** — até 4 botões de ação (link, ligar, resposta rápida)
* **Orientação da imagem** — retrato ou paisagem
* **Tamanho do card** — pequeno, médio ou grande

---

## O que o gestor vê

**Na criação de template/campanha RCS, seletor de tipo de mensagem:**

| Tipo | Descrição |
| -- | -- |
| Texto simples | Mensagem com texto e botões opcionais (já existe) |
| Card avançado | Imagem grande + título + descrição + botões |
| Carrossel | Múltiplos cards deslizáveis (já mapeado em outro card) |

**Preview do card avançado:**

* Imagem no topo do card (banner)
* Título em negrito
* Descrição em texto menor
* Botões na parte inferior

---

## Critérios de aceite

- [ ] Opção de **Card avançado** disponível na criação de template RCS
- [ ] Formulário do card avançado permite preencher imagem, título, descrição, botões, orientação e tamanho
- [ ] Preview atualiza em tempo real
- [ ] Ao enviar, a mensagem chega no celular do destinatário no formato correto
- [ ] Templates salvos com esses tipos podem ser reutilizados em campanhas e jornadas

---

## Cenários

- [ ] Crio template tipo **card avançado** com imagem, título e 2 botões → preview mostra o card corretamente → envio chega formatado no celular
- [ ] Uso o card avançado num nó de envio RCS numa jornada.
- [ ] Deixo título e descrição vazios no card avançado → sistema alerta que são obrigatórios

---

## Priorização RICE — Score: 21.3

| Reach | Impact | Confidence | Effort | Score |
| -- | -- | -- | -- | -- |
| 8 | 3 (massive) | 100% | 1.5 semanas | **21.3** |

**Justificativa:** A Send já suporta esses formato — confidence 100% porque não há incerteza de viabilidade. O impacto é massive porque card avançado é o formato RCS mais usado em campanhas de alto engajamento. Não expor essa opção na Userin significa que a plataforma entrega menos do que a infraestrutura já permite.

## Histórico de status
- Backlog (backlog): 2026-04-14T11:43:48.801Z → 2026-04-14T12:48:57.778Z
- Refining (backlog): 2026-04-14T12:48:57.778Z → 2026-04-14T13:23:16.626Z
- To-do (unstarted): 2026-04-14T13:23:16.626Z → 2026-04-14T16:08:10.907Z
- In Progress (started): 2026-04-14T16:08:10.907Z → 2026-04-14T18:50:06.575Z
- Pull Request (started): 2026-04-14T18:50:06.575Z → 2026-04-15T12:25:35.692Z
- Product Review (started): 2026-04-15T12:25:35.692Z → 2026-05-08T18:07:03.605Z
- Released (completed): 2026-05-08T18:07:03.605Z → atual

## Relações
- Related to: SEND-454 — Feature: Envio de vídeo e GIF em mensagens RCS

## Anexos
—
