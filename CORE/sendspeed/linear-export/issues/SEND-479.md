# SEND-479 — MAI - 05.2 - User Story - Status "Pendente" em Mensageria

| Campo | Valor |
| -- | -- |
| Status | To-do (unstarted) |
| Prioridade | No priority |
| Responsável | — |
| Time | Sendspeed |
| Projeto | — |
| Labels | — |
| Parent | — |
| Criada | 2026-05-18T11:42:30.171Z por pedro.antunes@sendspeed.com |
| Iniciada | — |
| Concluída | — |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-479-mai-052-user-story-status-pendente-em-mensageria |
| URL | https://linear.app/sendspeed/issue/SEND-479/mai-052-user-story-status-pendente-em-mensageria |

## Descrição

**Título:**
Exibir status **Pendente** na tela de **Analytics da Jornada** para disparos de SMS/RCS

---

**Como** usuário da Userin acompanhando uma **Jornada com disparo de SMS/RCS**,
**quero** visualizar o status **Pendente** na tela de Analytics,
**para** entender quais mensagens ainda não receberam callback final e garantir consistência nos números exibidos.

---

## Contexto

Na tela de **Analytics da Jornada**, hoje são exibidos status como:

* Enviado
* Falha
* Rejeitado

Porém, mensagens que ainda não receberam retorno do provedor (callback) não ficam claramente classificadas, gerando inconsistência na leitura dos dados.

---

## Regra de Negócio

* Toda mensagem enviada dentro de uma Jornada (SMS/RCS) deve estar em um dos status:
  * **Falha**
  * **Rejeitado**
  * **Pendente**
* O status **Pendente** representa:
  * mensagens enviadas sem callback final (ex: delivered, failed, rejected)
  * mensagens ainda em processamento pelo provedor

---

## Regra de consistência (Analytics)

Na tela de Analytics da Jornada deve sempre valer:

```
Enviado = Falha + Rejeitado + Pendente
```

---

## Requisitos

* Incluir o status **Pendente** na tela de **Analytics da Jornada**
* Considerar como Pendente toda mensagem:
  * sem callback final recebido
* Atualizar automaticamente o status quando o callback chegar
* Ajustar gráficos, cards e métricas para incluir "Pendente"
* Garantir que nenhuma mensagem enviada fique sem classificação

---

## Critérios de Aceite

* Mensagens sem callback aparecem como **Pendente** na tela de Analytics
* Ao receber callback, o status é atualizado automaticamente
* A soma dos status bate com o total enviado
* O status "Pendente" aparece nos gráficos e indicadores da Jornada
* Não existem mensagens "sem status" na análise

---

## Valor de Negócio

* Clareza na leitura dos dados de disparo SMS/RCS
* Visibilidade de mensagens ainda em processamento
* Base para análise de atraso de entrega (lead time)
* Apoio na detecção de problemas com provedores (ex: FAKEDLR)

## Histórico de status
- To-do (unstarted): 2026-05-18T11:42:30.171Z → 2026-06-22T17:16:52.966Z
- Released (completed): 2026-06-22T17:16:52.966Z → 2026-06-22T17:17:08.786Z
- To-do (unstarted): 2026-06-22T17:17:08.786Z → atual

## Relações
—

## Anexos
—
