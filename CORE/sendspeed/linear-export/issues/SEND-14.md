# SEND-14 — Unificação do Rastreamento entre Dispositivos

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | No priority |
| Responsável | — |
| Time | Sendspeed |
| Projeto | SendSpeed 2.0 |
| Labels | Tracker, Tech Story |
| Parent | — |
| Criada | 2025-05-26T21:23:12.189Z por pedro.antunes@sendspeed.com |
| Iniciada | — |
| Concluída | 2025-07-10T12:19:49.452Z |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-14-unificacao-do-rastreamento-entre-dispositivos |
| URL | https://linear.app/sendspeed/issue/SEND-14/unificacao-do-rastreamento-entre-dispositivos |

## Descrição

**Como** analista de dados ou produto,
**Quero** que o sistema unifique o histórico completo de um usuário (`userId`) que acessa a plataforma por múltiplos dispositivos e sessões (com diferentes `localId` e `sessionId`),
**Para que** eu possa analisar sua jornada de forma contínua e consistente, mesmo que ele tenha navegado anonimamente em mais de um dispositivo antes de se identificar.

### 📌 **Fluxo Funcional Realista**

1. Em **cada dispositivo** (ou navegador), o tracker gera:
   * Um `localId` persistido via `localStorage`.
   * Um novo `sessionId` a cada visita/sessão, salvo via `sessionStorage`.
   * Eventos são enviados com `localId`, `sessionId` e sem `userId`.
2. Ao fazer login, o front chama:

   ```
   js
   ```

   CopiarEditar

   `UserInsight.identify(externalId, traits)`
3. O sistema:
   * Resolve o `userId` vinculado ao `externalId` (ou cria um novo).
   * Associa o `localId` atual ao `userId`.
   * Marca o `sessionId` atual como pertencente ao `userId`.
   * Salva `userId` no `localStorage`.
4. A partir de então, todos os eventos terão `userId`.
5. No backend, as buscas futuras com base no `userId` devem:
   * Retornar eventos com `userId` direto.
   * Retornar eventos anteriores associados ao `localId` e `sessionId` já vinculados a esse `userId`.

---

### ✅ **Critérios de Aceite Atualizados**

* Quando o usuário logar em um dispositivo:
  * O sistema deve associar:
    * O `localId` daquele dispositivo ao `userId`.
    * O `sessionId` atual ao `userId`.
  * Os eventos futuros devem conter `userId`.
* **Eventos anteriores ao login não serão atualizados fisicamente** no banco de dados.
* A API de leitura deve:
  * Retornar todos os eventos onde `userId = X`.
  * Incluir eventos anônimos anteriores onde:
    * `localId` foi associado ao `userId`.
    * `sessionId` foi associado ao `userId`.
* A associação `userId ↔ localId ↔ sessionId` deve ser persistida (ex: coleção `identity_links`):

  ```
  json
  ```

  CopiarEditar

  `{ "userId": "user_abc123", "localIds": ["device1_xyz", "device2_pqr"], "sessionIds": ["sess_a", "sess_b", "sess_c"] }`

---

### 🔍 Exemplo de Timeline Consolidada (Consulta por `userId`)

```
json
```

`[ { "eventType": "pageview", "sessionId": "sess_a", // antes do login "localId": "device1_xyz", "userId": null }, { "eventType": "identify", "sessionId": "sess_b", "localId": "device1_xyz", "userId": "user_abc123" }, { "eventType": "click", "sessionId": "sess_b", "localId": "device1_xyz", "userId": "user_abc123" }, { "eventType": "pageview", "sessionId": "sess_c", // novo dispositivo "localId": "device2_pqr", "userId": "user_abc123" } ]`

## Histórico de status

- Backlog (backlog): 2025-05-26T21:23:12.189Z → 2025-05-27T04:35:48.640Z
- To-do (unstarted): 2025-05-27T04:35:48.640Z → 2025-05-28T10:19:41.546Z
- Backlog (backlog): 2025-05-28T10:19:41.546Z → 2025-05-28T13:57:15.762Z
- To-do (unstarted): 2025-05-28T13:57:15.762Z → 2025-07-10T12:19:49.422Z
- Released (completed): 2025-07-10T12:19:49.422Z → atual

## Relações

—

## Anexos

—
