# SEND-26 — BuyerAgent JS (Front-end): exibir Card minimizado e isolado de CSS

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | Urgent |
| Responsável | — |
| Time | Sendspeed |
| Projeto | — |
| Labels | Buyer |
| Parent | — |
| Criada | 2025-06-10T18:27:12.457Z por pedro.antunes@sendspeed.com |
| Iniciada | — |
| Concluída | 2025-06-24T18:04:47.232Z |
| Arquivada | 2025-12-27T01:54:03.697Z |
| Vencimento | — |
| Branch | hugofernandes/send-26-buyeragent-js-front-end-exibir-card-minimizado-e-isolado-de |
| URL | https://linear.app/sendspeed/issue/SEND-26/buyeragent-js-front-end-exibir-card-minimizado-e-isolado-de-css |

## Descrição

> **Como** *BuyerAgent JS (no browser)*
> **Quero** escutar o evento `buyeragent_doact_<localStorageID>` vindo do servidor, **inserir** o Card HTML recebido em formato "minimizado" em um canto da página, **sem** quebrar o CSS/JS existente
> **Para** que o usuário veja a oferta/intervenção sem que o site fique desconfigurado.

### 🎯 Critérios de Aceitação (Gherkin)

| \# | Cenário | Dado | Quando | Então |
| -- | -- | -- | -- | -- |
| 1 | **Conexão ao socket** | que o script seja carregado | `DOMContentLoaded` | BuyerAgent JS conecta-se ao namespace `/buyer` e ingressa na room `buyer_<localStorageID>` |
| 2 | **Recepção de Card** | que chegue o evento `buyeragent_doact_<localStorageID>` com payload válido (`card.html`, `meta`) | evento recebido | cria contêiner invisível `<buyer-card-container>` e insere o HTML fornecido **dentro de Shadow DOM** |
| 3 | **Estado inicial minimizado** | — | card injetado | mostra ícone/badge (≤ 36 px) fixo em `bottom-right` (z-index ≥ 9999) e mantém o card oculto |
| 4 | **Expandir** | que o usuário clique no badge | — | card expande com animação (`max-height`), permanecendo dentro do Shadow DOM |
| 5 | **Fechar** | que o usuário clique em "×" no card | — | card volta ao estado minimizado |
| 6 | **Isolamento de CSS** | — | card inserido | estilos externos da página **não** afetam o conteúdo do card; teste com classe `.btn { background:red }` na página não altera botão interno |

### Detalhes de Implementação

| Tema | Recomendação |
| -- | -- |
| **Shadow DOM** | `js const host=document.createElement('buyer-card-container'); document.body.appendChild(host); const shadow=host.attachShadow({mode:'open'}); shadow.innerHTML=cardHtml; `garante isolamento total de CSS e evita colisões de classes. |
| **Badge minimizado** | Elemento `<button id="buyer-badge">` dentro do Shadow; CSS inline: `position:fixed; bottom:16px; right:16px; width:36px; height:36px; border-radius:50%;` |
| **Expansão** | `shadow.querySelector('#buyer-badge').addEventListener('click', ()=>{ card.classList.toggle('open'); });` com transição CSS (`max-height`, `opacity`). |
| **Sanitização** | Usar DOMPurify ou função custom: strip `<script>`, `javascript:` URLs, atributos `on*`. |
| **Carregamento assíncrono** | Script principal inserido via `<script async src="buyer-agent.js"></script>` para não bloquear render. |
| **Fallback** | Se Shadow DOM não suportado (IE11), renderizar em `<iframe sandbox>` de 0 × 0 → expandir. |
| **Observabilidade** | Emitir `buyer_front_card_rendered` via `window.dispatchEvent` para analytics. |

## Histórico de status

- Backlog (backlog): 2025-06-10T18:27:12.457Z → 2025-06-10T18:50:09.188Z
- To-do (unstarted): 2025-06-10T18:50:09.188Z → 2025-06-24T18:04:47.209Z
- Released (completed): 2025-06-24T18:04:47.209Z → atual

## Relações

—

## Anexos

—
