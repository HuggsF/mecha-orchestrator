# SEND-373 — [SPRINT] US-05 — Envio de RCS na Jornada (Adapter + API + Editor)

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | Urgent |
| Responsável | pedro.antunes@sendspeed.com |
| Time | Sendspeed |
| Projeto | — |
| Labels | Jornadas, Sendspeed, Tech Story |
| Parent | — |
| Criada | 2026-03-09T12:18:50.852Z por pedro.antunes@sendspeed.com |
| Iniciada | 2026-03-16T15:38:00.423Z |
| Concluída | 2026-04-15T22:14:49.516Z |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-373-sprint-us-05-envio-de-rcs-na-jornada-adapter-api-editor |
| URL | https://linear.app/sendspeed/issue/SEND-373/sprint-us-05-envio-de-rcs-na-jornada-adapter-api-editor |

## Descrição

## Objetivo

Implementar envio de RCS (Rich Communication Services) de ponta a ponta: adapter no integrations service, executor no backend, editor visual no frontend.

## O que falta (não existe hoje)

* **Integrations service**: não tem rota `/api/rcs` nem adapter RCS
* **journeyOffsiteProcessor**: não suporta `action.sendRcs`
* **SendRcsExecutor**: existe mas é stub (não chama API real)

## Critérios de Aceite

- [ ] Novo endpoint: `POST /api/rcs/:companyId/send` no integrations service
- [ ] Adapter `sendspeed-rcs.adapter.ts` implementado
- [ ] Suporte a conteúdo RCS: texto, imagem, carrossel (até 10 cards), botões
- [ ] `SendRcsExecutor` chama a API real
- [ ] `journeyOffsiteProcessor` suporta `action.sendRcs`
- [ ] Scope `send_rcs` habilitado (`isEnabled: true`)
- [ ] Frontend: editor visual de mensagem RCS (carrossel, imagens, botões)
- [ ] Preview do RCS no builder

## Estrutura RCS Content

```json
{
  "type": "carousel",
  "cards": [
    {
      "title": "Bônus 100%",
      "description": "Deposite e ganhe",
      "imageUrl": "https://cdn.example.com/promo.jpg",
      "buttons": [
        { "type": "url", "label": "Depositar", "value": "https://jogao.com/deposito" }
      ]
    }
  ]
}
```

## Dependências

* US-04 (padrão de envio via executor)
* API RCS da SendSpeed (confirmar endpoints)

## Sprint

**Semana 2**

## Histórico de status
- To-do (unstarted): 2026-03-09T12:18:50.852Z → 2026-03-16T15:37:58.375Z
- Pull Request (started): 2026-03-16T15:37:58.375Z → 2026-03-16T15:38:00.423Z
- In Progress (started): 2026-03-16T15:38:00.423Z → 2026-03-18T14:43:14.961Z
- Backlog (backlog): 2026-03-18T14:43:14.961Z → 2026-03-18T14:43:21.433Z
- In Progress (started): 2026-03-18T14:43:21.433Z → 2026-03-23T17:44:01.651Z
- Pull Request (started): 2026-03-23T17:44:01.651Z → 2026-03-24T17:29:12.852Z
- Product Review (started): 2026-03-24T17:29:12.852Z → 2026-03-25T13:33:24.897Z
- Done (started): 2026-03-25T13:33:24.897Z → 2026-04-15T22:14:49.527Z
- Released (completed): 2026-04-15T22:14:49.527Z → atual

## Relações
—

## Anexos
—
