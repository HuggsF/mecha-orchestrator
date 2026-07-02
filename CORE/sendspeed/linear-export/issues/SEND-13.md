# SEND-13 — Associação de Histórico Anônimo a Usuário Identificado (via localId + identify)

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | No priority |
| Responsável | — |
| Time | Sendspeed |
| Projeto | SendSpeed 2.0 |
| Labels | Tracker, Tech Story |
| Parent | — |
| Criada | 2025-05-26T21:17:40.230Z por pedro.antunes@sendspeed.com |
| Iniciada | — |
| Concluída | 2025-07-10T12:19:55.520Z |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-13-associacao-de-historico-anonimo-a-usuario-identificado-via |
| URL | https://linear.app/sendspeed/issue/SEND-13/associacao-de-historico-anonimo-a-usuario-identificado-via-localid |

## Descrição

**Como** analista de dados ou produto,
**Quero** que o sistema associe o histórico de navegação anônimo (baseado em `localId` e `sessionId`) ao `userId` após o login,
**Para que** eu consiga visualizar a jornada completa do usuário — do anonimato à identificação — mesmo sem reescrever os eventos anteriores no banco.

### 📌 Fluxo Funcional:

1. **Fase Anônima (Pré-login)**:
   * Tracker gera `localId` e `sessionId`.
   * Eventos são enviados com `localId` e `sessionId`, sem `userId`.
2. **Identificação via Login (ex: após autenticação)**:

   ```
   js
   ```

   CopiarEditar

   `UserInsight.identify('external_crm_id_abc123', { name: 'João', email: 'joao@exemplo.com', plano: 'premium' });`
   * O sistema:
     * Busca ou gera `userId` vinculado ao `externalId`.
     * Salva o `userId` no `localStorage`.
     * A partir deste ponto, todos os eventos passam a conter `userId`.
3. **Associação Lógica (não retroativa fisicamente)**:
   * Eventos anteriores **não são atualizados no banco**.
   * Mas ao buscar a timeline de um `userId`, a API deve:
     * Buscar todos os eventos que contenham o `userId` explicitamente.
     * Também buscar os eventos por `localId` associados ao `userId`, com base no histórico de identificação.
     * Realizar o "join lógico" em tempo de leitura.

---

### ✅ Critérios de Aceite (Atualizados)

* O método `UserInsight.identify()`:
  * Aceita `externalId` como identificador principal.
  * Se o `externalId` não existir, cria e associa um novo `userId`.
  * Salva o `userId` no `localStorage` para eventos futuros.
  * A partir do login, todos os eventos passam a incluir `userId`.
* **Eventos anteriores ao login não devem ser atualizados** no banco.
* A **API de recuperação** de eventos (`GET /events`) deve aplicar lógica de agregação:
  * Buscar eventos com `userId`.
  * Buscar eventos com `localId` associados àquele `userId`.
  * Mesclar e ordenar por timestamp, retornando uma timeline única e contínua.
* A transição deve ser registrada como evento:

  ```
  json
  ```

  `{ "eventType": "identify", "externalId": "crm_abc123", "userId": "user_xyz", "localId": "device_001", "timestamp": "2025-05-26T14:00:00Z" }`

---

### 🔍 Exemplo de Timeline de Resposta da API (Unificada via Agregação):

```
json
```

`[ { "eventType": "pageview", "sessionId": "sess_001", "localId": "device_001", "userId": null, "timestamp": "2025-05-26T13:55:00Z" }, { "eventType": "identify", "sessionId": "sess_002", "localId": "device_001", "userId": "user_xyz", "timestamp": "2025-05-26T14:00:00Z" }, { "eventType": "click", "sessionId": "sess_002", "localId": "device_001", "userId": "user_xyz", "timestamp": "2025-05-26T14:01:00Z" } ]`

## Histórico de status

- Backlog (backlog): 2025-05-26T21:17:40.230Z → 2025-05-27T04:35:49.895Z
- To-do (unstarted): 2025-05-27T04:35:49.895Z → 2025-05-28T10:19:39.632Z
- Backlog (backlog): 2025-05-28T10:19:39.632Z → 2025-05-28T13:57:18.561Z
- To-do (unstarted): 2025-05-28T13:57:18.561Z → 2025-07-10T12:19:55.502Z
- Released (completed): 2025-07-10T12:19:55.502Z → atual

## Relações

—

## Anexos

—
