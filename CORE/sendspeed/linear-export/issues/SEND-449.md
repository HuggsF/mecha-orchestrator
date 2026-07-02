# SEND-449 — Feature: Encurtamento automático de links nos botões de RCS

| Campo | Valor |
| -- | -- |
| Status | Backlog (backlog) |
| Prioridade | No priority |
| Responsável | — |
| Time | Sendspeed |
| Projeto | — |
| Labels | — |
| Parent | — |
| Criada | 2026-04-14T11:38:51.718Z por Vinicius Carneiro |
| Iniciada | — |
| Concluída | — |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-449-feature-encurtamento-automatico-de-links-nos-botoes-de-rcs |
| URL | https://linear.app/sendspeed/issue/SEND-449/feature-encurtamento-automatico-de-links-nos-botoes-de-rcs |

## Descrição

## História

Como gestor de marketing, quero que ao criar uma mensagem RCS com botão de link, o sistema encurte automaticamente a URL no momento do envio — sem que eu precise fazer nada — para que eu consiga ver quantas pessoas clicaram no botão da minha mensagem.

---

## O problema hoje

Quando crio um RCS com um botão (ex: "Apostar Agora" → https://meusite.com/promo), a mensagem é enviada com esse link direto. Não consigo saber quantas pessoas clicaram no botão porque não há rastreamento. O único jeito seria encurtar o link manualmente antes de configurar o botão — o que é trabalhoso e propenso a erro.

---

## O que precisa acontecer

1. Configuro o botão do RCS normalmente, com a URL original (ex: https://meusite.com/promo)
2. A URL original fica visível pra mim no editor — nada muda na tela de criação
3. No momento que clico em **Enviar**, o sistema substitui automaticamente a URL do botão por um link curto rastreado
4. O destinatário recebe o RCS com o botão funcionando normalmente
5. Quando ele clica, o sistema registra o clique e redireciona para a URL original
6. No relatório da campanha ou jornada, vejo quantos cliques cada botão recebeu

---

## O que o gestor vê

**Na criação:**

* Configura o botão com a URL que quiser
* Um aviso discreto abaixo do campo de URL: *"Link será encurtado automaticamente no envio para rastreamento de cliques"*

**No relatório:**

* Cliques por botão (se houver carrossel com vários cards, cada botão aparece separado)
* Total de cliques e cliques únicos

---

## Critérios de aceite

- [ ] Ao enviar um RCS com botão de link, a URL é substituída automaticamente por um link rastreado
- [ ] A URL original continua visível no editor — a substituição acontece só no envio
- [ ] O destinatário clica no botão e é redirecionado para a URL original normalmente
- [ ] Cada clique é registrado
- [ ] No relatório, aparece o número de cliques por botão
- [ ] Se o RCS tiver carrossel com múltiplos cards, cada botão é rastreado individualmente
- [ ] Se a URL já for um link encurtado da plataforma, não encurta de novo

---

## Cenários

- [ ] Envio RCS com 1 botão → clique registrado corretamente
- [ ] Envio RCS em carrossel com 3 cards, 1 botão cada → 3 links distintos gerados, cliques contados separadamente
- [ ] Usuário clica 3x no mesmo botão → contador incrementa, cliques únicos = 1
- [ ] Envio RCS sem botão de link → nenhum encurtamento, comportamento normal
- [ ] Relatório exibe: Card 1 = 45 cliques, Card 2 = 78, Card 3 = 23

---

## Priorização RICE — Score: 19.2

| Reach | Impact | Confidence | Effort | Score |
| -- | -- | -- | -- | -- |
| 10 | 3 (massive) | 80% | 1.25 meses | **19.2** |

**Justificativa:** Toda empresa que usa RCS hoje envia os botões sem saber se alguém clicou. Sem esse dado, é impossível medir o retorno das campanhas. A infraestrutura de encurtamento já existe — é extensão de algo que funciona.

## Histórico de status
- Backlog (backlog): 2026-04-14T11:38:51.718Z → atual

## Relações
—

## Anexos
—
