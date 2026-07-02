# SEND-15 — Endpoint de Recuperação de Eventos com Identidade Unificada (por Session ID, User ID, localId ou externalId)

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | No priority |
| Responsável | — |
| Time | Sendspeed |
| Projeto | SendSpeed 2.0 |
| Labels | — |
| Parent | — |
| Criada | 2025-05-26T21:28:03.637Z por pedro.antunes@sendspeed.com |
| Iniciada | — |
| Concluída | 2025-07-10T12:20:02.306Z |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-15-endpoint-de-recuperacao-de-eventos-com-identidade-unificada |
| URL | https://linear.app/sendspeed/issue/SEND-15/endpoint-de-recuperacao-de-eventos-com-identidade-unificada-por |

## Descrição

**Como** desenvolvedor front-end ou analista de dados,
**Quero** consultar um endpoint para recuperar os eventos de um usuário (identificado ou não), com base em diferentes identificadores (`externalId`, `userId`, `localId`, `sessionId`),
**Para que** eu possa visualizar a jornada completa e unificada daquele usuário dentro de um contexto específico da empresa.

### 📌 Fluxo e Comportamento Esperado

* O sistema deve receber sempre o `companyId` para garantir o escopo dos dados.
  * A forma de envio (header, token ou query param) pode ser definida pela engenharia.
* Deve ser possível realizar a consulta por:
  * `externalId` → O sistema resolve o `userId` e recupera os dados unificados daquele usuário.
  * `userId` → Retorna todos os eventos com `userId`, além dos `localId` e `sessionId` vinculados a ele.
  * `localId` → Retorna todos os eventos daquele dispositivo.
  * `sessionId` → Retorna apenas os eventos daquela sessão específica.
* Caso o usuário nunca tenha se identificado (`userId` desconhecido):
  * Os eventos devem ser retornados **com o rótulo de "usuário anônimo"** e agrupados por `localId`.
* Caso o `userId` já tenha sido vinculado:
  * Todos os eventos devem ser retornados, **inclusive os anônimos anteriores** ao login.
* A resposta deve conter:
  * Timeline de eventos ordenada por timestamp.
  * Identidade lógica do usuário (`userId` se houver, ou `anon_localId_xyz`).
  * Dados brutos e enriquecidos dos eventos: tipo, URL, timestamp, agente, metadata, embedding text etc.

---

### ✅ Critérios de Aceite (Atualizados)

1. **Autorização e Escopo:**
   * Toda requisição ao endpoint deve conter o `companyId` obrigatoriamente.
   * A API só deve retornar eventos pertencentes àquela empresa.
2. **Parâmetros aceitos:**
   * `externalId`, `userId`, `localId`, `sessionId` (pelo menos um é obrigatório).
   * `dateStart`, `dateEnd` (opcional).
   * A API deve ser inteligente o suficiente para resolver o `userId` a partir do `externalId`.
3. **Identificação Automática do Usuário:**
   * Se qualquer dos identificadores estiver associado a um `userId`, a resposta deve consolidar **todos os eventos** associados àquele `userId`, mesmo que tenham sido registrados como anônimos anteriormente.
   * Caso contrário, os eventos devem ser agrupados logicamente como `anon_{localId}`.
4. **Formato da Resposta:**

   ```
   json
   ```

   `{ "identity": { "type": "identified", "userId": "user_abc123", "externalId": "crm_001" }, "events": [ { "eventId": "evt_001", "timestamp": "2025-05-26T13:55:00Z", "eventType": "pageview", "sessionId": "sess_xyz", "localId": "device_001", "userId": "user_abc123", "url": "/produto/123", "embeddingText": "..." }, ... ] }`

   Ou, no caso de usuário não identificado:

   ```
   json
   ```

   `{ "identity": { "type": "anonymous", "localId": "device_002" }, "events": [ ... ] }`
5. **Fallback e Tratamento:**
   * Se `externalId` for passado mas não existir, a resposta deve indicar que nenhum `userId` foi encontrado, mas pode retornar eventos anônimos vinculados a `localId` se também estiver presente.

@pedro.antunes - se external_id não existe, não vejo como encontrar algum dado relevante através do localstorage_id uma vez que provavelmente serão dados diferentes. O que acha?

---

### 🛠 Recomendação Técnica para Eng:

* Implementar **resolução de identidade** via serviço ou coleção auxiliar (`identity_links`) que contenha o mapeamento:

  ```
  json
  ```

  CopiarEditar

  `{ "companyId": "company_xyz", "userId": "user_abc", "externalId": "crm_001", "localIds": ["device_001", "device_002"], "sessionIds": ["sess_1", "sess_2"] }`
* Na leitura:
  * Usar `$or` com base nos identificadores.
  * Agregar eventos por identidade, usando `userId` quando existir, e `localId` quando não.

## Doc adicional clickup

> **[Embed — ClickUp]:** Documento do ClickUp — título "ClickUp" ("ClickUp is the highest-rated and fastest growing Productivity Platform."). Link: https://app.clickup.com/9013936724/v/dc/8cmbgjm-44613/8cmbgjm-60813

## Histórico de status

- Backlog (backlog): 2025-05-26T21:28:03.637Z → 2025-05-27T04:35:46.798Z
- To-do (unstarted): 2025-05-27T04:35:46.798Z → 2025-05-28T10:19:46.666Z
- Backlog (backlog): 2025-05-28T10:19:46.666Z → 2025-05-28T13:57:23.003Z
- To-do (unstarted): 2025-05-28T13:57:23.003Z → 2025-07-10T12:20:02.289Z
- Released (completed): 2025-07-10T12:20:02.289Z → atual

## Relações

—

## Anexos

—
