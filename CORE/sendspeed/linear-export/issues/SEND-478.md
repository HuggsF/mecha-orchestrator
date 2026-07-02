# SEND-478 — MAI -[BACKLOG] - User Story - Envio de Lista Fria via API com Arquivo

| Campo | Valor |
| -- | -- |
| Status | Backlog (backlog) |
| Prioridade | No priority |
| Responsável | — |
| Time | Sendspeed |
| Projeto | — |
| Labels | — |
| Parent | — |
| Criada | 2026-05-18T11:21:22.868Z por pedro.antunes@sendspeed.com |
| Iniciada | — |
| Concluída | — |
| Arquivada | 2026-06-22T17:18:01.876Z |
| Vencimento | — |
| Branch | hugofernandes/send-478-mai-backlog-user-story-envio-de-lista-fria-via-api-com |
| URL | https://linear.app/sendspeed/issue/SEND-478/mai-backlog-user-story-envio-de-lista-fria-via-api-com-arquivo |

## Descrição

**Título:**
Criar disparo via API a partir de arquivo de lista fria

**Como** sistema externo/integrador,
**quero** enviar uma lista fria por API, escolhendo um template e parâmetros de disparo,
**para** que a Userin receba o arquivo, crie a audiência e gere o disparo automaticamente, igual ao fluxo feito pela plataforma.

---

## Contexto

Hoje o disparo de lista fria é feito pela plataforma, com upload de lista, seleção de template, criação de audiência e configuração do disparo.

A necessidade é permitir o mesmo fluxo via API, para que sistemas externos consigam automatizar esse processo sem precisar operar pela interface.

O endpoint deve receber um **arquivo**, não apenas JSON com contatos.

---

## Fluxo esperado

 1. Sistema externo chama endpoint da Userin via API.
 2. Envia arquivo da lista fria, por exemplo CSV ou XLSX.
 3. Informa o template a ser usado.
 4. Informa os mesmos parâmetros disponíveis no disparo pela plataforma.
 5. Userin recebe o arquivo completo.
 6. Userin sobe o arquivo para o bucket.
 7. Userin processa/valida a lista.
 8. Userin cria uma audiência com base nessa lista.
 9. Userin cria o disparo vinculado à audiência criada.
10. Disparo pode ser:

* imediato;
* agendado;
* salvo como rascunho, se existir esse comportamento na plataforma.

---

## Endpoint sugerido

```
POST /api/campaigns/cold-list/import-and-send
Content-Type: multipart/form-data
```

---

## Exemplo de campos da requisição

```
file: lista_fria.csv
templateId: tpl_123
campaignName: Campanha Lista Fria Maio
channel: SMS
sendMode: now
scheduledAt: null
audienceName: Lista Fria Maio 2026
deduplicateBy: phone
ignoreInvalidContacts: true
metadata: {
  "source": "external_api",
  "clientCampaignId": "campanha_cliente_001"
}
```

Para envio agendado:

```
file: lista_fria.csv
templateId: tpl_123
campaignName: Campanha Lista Fria Agendada
channel: RCS
sendMode: scheduled
scheduledAt: 2026-05-20T10:00:00-03:00
audienceName: Lista Fria Agendada Maio 2026
deduplicateBy: phone
ignoreInvalidContacts: true
```

---

## Requisitos funcionais

* Criar endpoint para envio de lista fria via API.
* Endpoint deve aceitar arquivo via `multipart/form-data`.
* Arquivo deve suportar pelo menos:
  * CSV;
  * XLSX, se já for suportado na plataforma.
* Deve receber `templateId`.
* Deve receber os mesmos parâmetros existentes no disparo pela plataforma.
* Deve permitir disparo imediato.
* Deve permitir disparo agendado.
* Deve subir o arquivo original para o bucket.
* Deve criar audiência automaticamente a partir do arquivo.
* Deve vincular a audiência criada ao disparo.
* Deve criar o disparo já com status correto:
  * `scheduled`, se agendado;
  * `queued` ou `processing`, se disparo imediato;
  * `draft`, se esse modo existir.
* Deve retornar identificadores criados:
  * `uploadId`;
  * `audienceId`;
  * `campaignId`;
  * `jobId`.

---

## Requisitos de validação

* Validar se o arquivo foi enviado.
* Validar formato permitido.
* Validar tamanho máximo do arquivo.
* Validar colunas obrigatórias, como:
  * `phone`;
  * `name`, se o template usar variável de nome;
  * demais variáveis obrigatórias do template.
* Validar se `templateId` existe e pertence à empresa.
* Validar se o canal do template é compatível com o canal do disparo.
* Validar data futura quando `sendMode = scheduled`.
* Validar duplicidade por telefone, e-mail ou outro identificador configurado.
* Validar contatos inválidos sem quebrar todo o processamento, se `ignoreInvalidContacts = true`.

---

## Critérios de aceite

* Dado um arquivo válido e um `templateId`, a Userin deve subir o arquivo para o bucket.
* Dado o arquivo processado, a Userin deve criar uma audiência automaticamente.
* Dado uma audiência criada, a Userin deve criar um disparo vinculado a ela.
* Dado `sendMode = now`, o disparo deve entrar na fila de envio imediatamente.
* Dado `sendMode = scheduled`, o disparo deve ficar agendado para a data informada.
* Dado um arquivo inválido, a API deve retornar erro claro informando o motivo.
* Dado um template com variáveis obrigatórias, o arquivo deve ser validado contra essas variáveis.
* Dado sucesso na criação, a API deve retornar IDs de rastreabilidade.

## Histórico de status
- To-do (unstarted): 2026-05-18T11:21:22.868Z → 2026-05-18T12:22:49.859Z
- Backlog (backlog): 2026-05-18T12:22:49.859Z → 2026-05-18T12:28:59.741Z
- To-do (unstarted): 2026-05-18T12:28:59.741Z → 2026-05-18T12:29:11.591Z
- Backlog (backlog): 2026-05-18T12:29:11.591Z → 2026-05-18T12:32:45.529Z
- To-do (unstarted): 2026-05-18T12:32:45.529Z → 2026-05-18T12:33:12.944Z
- Backlog (backlog): 2026-05-18T12:33:12.944Z → atual

## Relações
—

## Anexos
—
