# SEND-454 — Feature: Envio de vídeo e GIF em mensagens RCS

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | No priority |
| Responsável | andrei.garcia@externo.sendspeed.com |
| Time | Sendspeed |
| Projeto | — |
| Labels | — |
| Parent | — |
| Criada | 2026-04-14T11:44:28.300Z por Vinicius Carneiro |
| Iniciada | — |
| Concluída | 2026-06-22T17:49:58.244Z |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-454-feature-envio-de-video-e-gif-em-mensagens-rcs |
| URL | https://linear.app/sendspeed/issue/SEND-454/feature-envio-de-video-e-gif-em-mensagens-rcs |

## Descrição

## História

Como gestor, quero poder enviar vídeos e GIFs nas minhas mensagens RCS para criar campanhas mais dinâmicas e com maior engajamento.

---

## O problema hoje

As mensagens RCS na Userin só suportam texto e imagem estática. Não há como enviar um vídeo curto de promoção ou um GIF animado, mesmo sendo formatos suportados pelo canal RCS.

---

## O que precisa acontecer

1. Na criação de template ou campanha RCS, o gestor pode escolher adicionar um **vídeo** ou **GIF** pela URL
2. O preview mostra uma miniatura do vídeo ou o GIF animado
3. O destinatário recebe a mensagem com o vídeo reproduzível ou o GIF animado direto no app de mensagens

---

## O que o gestor vê

**No editor de template/campanha RCS:**

* Campo **"URL do vídeo"** ou **"URL do GIF"** dependendo do tipo selecionado
* Formatos aceitos indicados: MP4 para vídeo, GIF para animado
* Preview: miniatura do vídeo com ícone de play, ou GIF animado rodando
* Texto de acompanhamento opcional abaixo do vídeo/GIF

**Na mensagem recebida:**

* Vídeo: abre inline com botão de play, sem precisar sair do app de mensagens
* GIF: toca em loop automaticamente

---

## Critérios de aceite

- [ ] Campo de URL de vídeo (MP4) disponível no editor RCS
- [ ] Campo de URL de GIF disponível no editor RCS
- [ ] Preview mostra miniatura do vídeo ou GIF animado em tempo real
- [ ] Texto de acompanhamento opcional funciona para ambos
- [ ] Ao enviar, o destinatário recebe o vídeo reproduzível ou GIF animado
- [ ] Funciona em templates, campanhas e jornadas RCS
- [ ] URL inválida exibe aviso no editor sem bloquear o salvamento

---

## Cenários

- [ ] Colo URL de MP4 → preview mostra miniatura com play → destinatário recebe vídeo reproduzível
- [ ] Colo URL de GIF → preview anima o GIF → destinatário recebe GIF em loop
- [ ] Adiciono texto de acompanhamento junto com o vídeo → ambos chegam na mensagem
- [ ] URL inválida → aviso exibido, consigo salvar mesmo assim
- [ ] Uso vídeo num nó de jornada RCS → funciona igual à campanha

---

## Priorização RICE — Score: 16.0

| Reach | Impact | Confidence | Effort | Score |
| -- | -- | -- | -- | -- |
| 8 | 2 (high) | 100% | 1 semana | **16.0** |

**Justificativa:** Vídeo e GIF são formatos nativos do RCS e muito usados em campanhas de entretenimento, apostas e varejo. A infraestrutura de envio na Send já suporta esses formatos — é expor as opções na Userin, assim como feito para card avançado e arquivo (@SEND-453).

## Histórico de status
- Backlog (backlog): 2026-04-14T11:44:28.300Z → 2026-04-14T12:49:11.312Z
- Refining (backlog): 2026-04-14T12:49:11.312Z → 2026-04-15T20:14:53.130Z
- To-do (unstarted): 2026-04-15T20:14:53.130Z → 2026-06-22T17:49:58.254Z
- Released (completed): 2026-06-22T17:49:58.254Z → atual

## Relações
- Related to: SEND-453 — Feature: Envio de card avançado no RCS da Userin

## Anexos
—
