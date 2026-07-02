# SEND-12 — Associação de Histórico Anônimo a Usuário Identificado com Persistência de localId e Gerenciamento de sessionId

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | No priority |
| Responsável | — |
| Time | Sendspeed |
| Projeto | SendSpeed 2.0 |
| Labels | Tracker, Tech Story |
| Parent | — |
| Criada | 2025-05-26T20:57:40.345Z por pedro.antunes@sendspeed.com |
| Iniciada | — |
| Concluída | 2025-07-10T12:19:58.272Z |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-12-associacao-de-historico-anonimo-a-usuario-identificado-com |
| URL | https://linear.app/sendspeed/issue/SEND-12/associacao-de-historico-anonimo-a-usuario-identificado-com |

## Descrição

**Como** um analista de dados ou produto,
**Quero** que o sistema associe automaticamente os eventos de um usuário anônimo (identificado por `localId` e múltiplos `sessionId`) ao seu `userId` quando ele fizer login,
**Para que** eu possa ter uma visão consolidada e contínua da jornada do usuário, desde suas ações anônimas até suas ações autenticadas, mesmo em diferentes sessões e dispositivos.

### Detalhamento Técnico e Fluxo Esperado

* **SessionID**: gerado a cada nova entrada no site (nova aba ou refresh), salvo em `sessionStorage`.
* **LocalID** (DeviceID): gerado apenas na primeira visita e salvo em `localStorage`. Reutilizado em sessões futuras naquele dispositivo.
* **UserID**: atribuído após login, persistente no sistema.
* Um `UserID` pode ter múltiplos `localId` associados (ex: celular e desktop).
* Um `localId` pode ter múltiplos `sessionId`.
* Cada evento tem `sessionId`, `localId`, e, se autenticado, também `userId`.

Verificar id gerado pelo FingerPrintJS (sem IP). 

---

### ✅ Critérios de Aceite (refinados)

1. **Criação e Persistência de localId:**
   * Se `localId` não existir no `localStorage`, o tracker deve gerar um novo UUID e salvá-lo.
   * Se já existir, deve ser reutilizado em sessões futuras no mesmo dispositivo.
2. **Geração de sessionId por visita:**
   * A cada carregamento do site (inclusive hard refresh ou nova aba), o tracker deve gerar um novo `sessionId` e salvá-lo em `sessionStorage`.
3. **Associação de eventos anônimos após login:**
   * Quando um usuário fizer login:
     * Todos os eventos anteriores (com aquele `localId`) devem ser associados ao novo `userId` no banco (marcação retroativa e contínua).
     * A sessão atual deve atualizar seus eventos já enviados com o `userId`.
     * Eventos futuros devem registrar `userId`, mantendo `localId` e `sessionId`.
     * **Conceito de Event-sourcing**
4. **Consolidação de histórico por dispositivo:**
   * Para cada `userId`, o sistema deve ser capaz de consolidar eventos de múltiplos `localId` (diferentes dispositivos) e múltiplos `sessionId`.
5. **Registro da transição (login):**
   * A transição de anônimo para logado (login) deve ser registrada como um evento especial, com o timestamp da associação e os identificadores envolvidos (`localId`, `sessionId`, `userId`, `externalId` se houver).
     * Como entender diferentes fontes de acesso do mesmo usuário e consolidar tudo isso trazendo seu histórico de visitação
6. **Query de análise completa:**
   * Deve ser possível recuperar toda a timeline do usuário usando o `userId`, contendo eventos anteriores e posteriores ao login, inclusive de diferentes dispositivos (`localId` distintos).

---

### 📊 Exemplo Visual com os Identificadores:

> **[Imagem 1 — transcrição]:** Diagrama de fluxo (fluxograma/whiteboard) que ilustra a unificação de identidade de um usuário ao fazer login, a partir de múltiplos dispositivos. Estrutura da esquerda para a direita:
>
> - **Bloco amarelo (esquerda superior) rotulado "Celular"** contém duas caixas: "SessionID 1 / localId 1" e "SessionID 2 / localId 1". (Fase anônima no celular.)
> - **Bloco laranja (esquerda inferior) rotulado "Desktop"** contém duas caixas: "SessionID 3 / localId 2" e "SessionID 4 / localId 2". (Fase anônima no desktop.)
> - Setas partindo tanto do bloco Celular quanto do bloco Desktop convergem para uma **caixa azul central rotulada "Login"**.
> - À direita do "Login", uma seta aponta para um **grande bloco laranja rotulado "UserID X Logado"** (representa o estado autenticado consolidado), que contém dois sub-blocos:
>   - **Sub-bloco amarelo "Celular"** com as caixas: "SessionID 5 / localId 1 / userId X / externalID" e "SessionID 6 / localId 1 / userId X / externalID".
>   - **Sub-bloco laranja "Desktop"** com as caixas: "SessionID 8 / localId 2 / userId X" e "SessionID 9 / localId 2 / userId X / externalID" (a última caixa aparece parcialmente sobreposta ao rótulo "Desktop").
>
> **O que a imagem demonstra:** após o login, os identificadores de dispositivo (`localId 1` = Celular, `localId 2` = Desktop) e suas respectivas sessões passam a ser associados a um mesmo `userId X` (e a um `externalID`), consolidando o histórico anônimo de múltiplos dispositivos em uma única identidade de usuário logado. O `localId` continua identificando cada dispositivo, enquanto o `userId` passa a ser a referência primária.

Os IDs devem ser gerados automaticamente pelo mongo uuid v4.

---

### 🧠 Observações para o Time Técnico:

* **Importante não reatribuir** `localId` após login — ele continua sendo o identificador do dispositivo.
* O `userId` deve **se sobrepor como referência primária** em relatórios e análises pós-login.
* O `externalId` pode ser usado como um ID do sistema externo (ex: CRM, banco de dados da empresa).

## Histórico de status

- Backlog (backlog): 2025-05-26T20:57:40.345Z → 2025-05-27T04:35:54.212Z
- To-do (unstarted): 2025-05-27T04:35:54.212Z → 2025-05-28T10:19:35.383Z
- Backlog (backlog): 2025-05-28T10:19:35.383Z → 2025-05-28T13:57:20.734Z
- To-do (unstarted): 2025-05-28T13:57:20.734Z → 2025-07-10T12:19:57.957Z
- Released (completed): 2025-07-10T12:19:57.957Z → atual

## Relações

—

## Anexos

—
