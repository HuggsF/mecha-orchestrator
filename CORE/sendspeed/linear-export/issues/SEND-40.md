# SEND-40 — Interface de Auditoria do Behavior

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | Urgent |
| Responsável | andrei.garcia@externo.sendspeed.com |
| Time | Sendspeed |
| Projeto | — |
| Labels | — |
| Parent | — |
| Criada | 2025-07-09T12:36:55.605Z por bruno.heidrich@sendspeed.com |
| Iniciada | 2025-07-10T12:12:45.735Z |
| Concluída | 2025-08-11T13:53:36.677Z |
| Arquivada | 2026-02-15T02:17:35.630Z |
| Vencimento | — |
| Branch | hugofernandes/send-40-interface-de-auditoria-do-behavior |
| URL | https://linear.app/sendspeed/issue/SEND-40/interface-de-auditoria-do-behavior |

## Descrição

**Como** PM (Product Manager),
**Quero** visualizar em uma interface os eventos analisados pelo Behavior, a decisão tomada e o tipo de risco ou oportunidade identificada,
**Para que** eu possa auditar, validar e evoluir as interpretações do sistema de comportamento.

**Critérios de Aceitação:**

* A tela deve listar sessões analisadas com os seguintes dados:
  * `session_id`
  * eventos relevantes (scroll, tempo em seções, cliques)
  * tipo de intenção detectada (ex: dúvida, alta chance de conversão, evasão)
  * decisão tomada
  * `behavior_explanation`
* Deve ser possível filtrar por:
  * tipo de intenção (ex: dúvida, risco, oportunidade)
  * tipo de card disparado - *Se tiver.*
  * seletor de período de tempo - personalizado, 7, 15, 30, 60, 90 dias.
* Deve haver um campo visual destacando o risco ou oportunidade (ex: "82% chance de evasão") - *ou o mais proximo possível dessa análise*.
* A interface deve ser responsiva e acessível para leitura rápida.

### Todos os dados devem ser carregados dinamicamente via API com paginação.

# **Ex de Tela:**

**AUDITORIA DO BEHAVIOR - Organizar por ordem SEMPRE do mais recente.**

#### Filtros no topo (linha horizontal com espaçamento)

* **Tipo de Intenção:** `[ dropdown ]`
  (ex: Dúvida, Oportunidade, Risco de Evasão)
* **Tipo de Card:** `[ dropdown ]`
  (ex: Pop-up, Modal, Flutuante)
* **Período:** `[ calendário / range selector ]`
  (ex: Últimos 7 dias, 01/07 a 07/07)
* *SE FOR FÁCIL*: Filtro pelo localstorageId ou userId

---

### 📋 Tabela com resultados

| SESSION_ID | EVENTOS | INTENÇÃO DETECTADA | EXPLICAÇÃO |
| -- | -- | -- | -- |
| abc123 | Scroll, tempo na seção, clique | **Dúvida** | Usuário pausou no preço por 8s após scroll acelerado → sinal de dúvida |
| xyz789 | Scroll rápido, sem clique, abandono | **Risco de Evasão (82%)** | Navegação curta e sem interação após carregar produto |
| def456 | Clique em botão, tempo em seção | **Oportunidade (74%)** | Engajamento alto com CTA e tempo acima da média → potencial conversão |

---

### Ações adicionais (abaixo ou flutuante no canto)

* Botão "Exportar CSV"
* Botão "Ver detalhes da sessão"
* Ícones ou cores para destacar tipo de risco (ex: ⚠️ para risco alto)

## Histórico de status

- Backlog (backlog): 2025-07-09T12:36:55.605Z → 2025-07-10T12:12:45.720Z
- In Progress (started): 2025-07-10T12:12:45.720Z → 2025-07-22T14:20:16.946Z
- Pull Request (started): 2025-07-22T14:20:16.946Z → 2025-07-31T14:39:31.333Z
- Product Review (started): 2025-07-31T14:39:31.333Z → 2025-08-11T13:53:36.622Z
- Released (completed): 2025-08-11T13:53:36.622Z → atual

## Relações

—

## Anexos

—
