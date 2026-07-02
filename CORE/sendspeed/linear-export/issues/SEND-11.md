# SEND-11 — Implementação Simplificada do Tracker com Coleta Automática de Dados Estruturados e de Interação

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | No priority |
| Responsável | marcelo.motta@sendspeed.com |
| Time | Sendspeed |
| Projeto | SendSpeed 2.0 |
| Labels | Tracker, Tech Story |
| Parent | — |
| Criada | 2025-05-26T20:46:22.214Z por pedro.antunes@sendspeed.com |
| Iniciada | 2025-06-03T12:33:37.187Z |
| Concluída | 2025-06-10T18:33:01.211Z |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-11-implementacao-simplificada-do-tracker-com-coleta-automatica |
| URL | https://linear.app/sendspeed/issue/SEND-11/implementacao-simplificada-do-tracker-com-coleta-automatica-de-dados |

## Descrição

[https://tracker.userinsight.me/demo](<https://tracker.userinsight.me/demo>)

* **Como** um Desenvolvedor da Empresa Cliente,
* **Quero** poder integrar um tracker no website da minha empresa com apenas uma linha de código,
* **Para que** o sistema capture automaticamente uma ampla gama de interações do usuário e dados contextuais da página (incluindo metadados OG, Schema, SEO, e propriedades de objetos relevantes) com o mínimo esforço de implementação, permitindo análises de comportamento ricas e detalhadas.

**Critérios de Aceite:**

1. **Implementação com Linha Única:** O tracker deve ser inicializado no site do cliente colando um único snippet de código JavaScript (ex: `<script async src="https://tracker.sendspeed.com/tracker.js?apiKey=SUA_API_KEY"></script>`).
2. **Captura Automática de Eventos Padrão:**
   * **Pageviews:** Registrados automaticamente em cada carregamento de página e em transições de rota em SPAs (Single Page Applications).
   * **Cliques:** Captura de cliques em elementos interativos (links, botões, etc.), incluindo informações sobre o elemento clicado (ID, classes, texto, seletor CSS).
   * **Mudanças de Visibilidade da Página:** Eventos para quando a aba se torna ativa ou inativa.
   * **Profundidade de Rolagem (Scroll Depth):** Percentuais de rolagem da página (ex: 25%, 50%, 75%, 100%).
3. **Captura de Dados Estruturados da Página (em** `pageview` ou eventos contextuais):
   * **Metadados SEO:** `title` da página, `meta description`, `meta keywords`.
   * **Open Graph (OG):** Extração automática de `og:title`, `og:type`, `og:image`, `og:url`, `og:description`, `og:site_name`, etc.
   * **Google Schema (JSON-LD):** Parseamento e coleta de dados de scripts `<script type="application/ld+json">`.
   * **Google Merchant (via Schema):** Se os dados do produto estiverem em conformidade com o Schema.org para `Product`, eles devem ser capturados (ex: nome, preço, SKU, marca).
   * **Propriedades de Objetos Globais/Relevantes:** Capacidade de configurar (ou detectar heuristicamente) e coletar dados de objetos JavaScript específicos (ex: `dataLayer` do Google Tag Manager, informações de usuário logado expostas em um objeto global).
4. **Compatibilidade com SPA:** O tracker deve detectar e registrar corretamente as visualizações de página virtuais em SPAs (Angular, React, Vue, etc.) sem necessidade de configuração manual adicional para as transições de rota mais comuns.
5. **Estrutura de Dados Consistente:** Todos os dados coletados devem ser enviados para o endpoint `POST /collect` seguindo uma estrutura JSON bem definida, incluindo `apiKey`, `userId` (ou `localId` para anônimos), `sessionId`, `clientInfo` e um array de `events`.
6. **Informações do Cliente:** Coleta automática de `userAgent`, idioma do navegador, tamanho da tela, tamanho da viewport.
7. **Timestamps Precisos:** Todos os eventos devem ter um timestamp UTC preciso.
8. **Performance:** O tracker deve ter impacto mínimo na performance do site cliente, utilizando carregamento assíncrono e otimizações para não bloquear a renderização da página.
   1. Async: perder o evento não é big deal.
   2. Como monitorar eventos perdidos: pode escalar rapidamente e sem monitoramento será impossível entender o bug.

---

### Exemplo de Estrutura de Dados Enviada ao Endpoint `POST /collect`

Este exemplo mostra um payload que o tracker enviaria, contendo múltiplos eventos, incluindo `pageview` com metadados ricos e um evento de `add_to_cart`.

JSON

```
{
  "apiKey": "CLIENT_API_KEY_XYZ",
  "userId": "user_12345", // Ou null se anônimo
  "localId": "device_abc123xyz", // ID persistente no dispositivo para anônimos
  "sessionId": "session_uuid_qwerty",
  "clientInfo": {
    "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "language": "pt-BR",
    "screenSize": "1920x1080",
    "viewportSize": "1366x657",
    "timezone": "America/Sao_Paulo"
  },
  "events": [
    {
      "eventId": "evt_0e28b7a1-f821-4b7d-a0e9-3f0c9a71c2d8",
      "type": "pageview",
      "timestamp": "2025-05-26T14:30:05.123Z",
      "url": "https://www.lojadojoao.com/produto/notebook-ultra-x",
      "referrer": "https://www.google.com/",
      "pageTitle": "Notebook Ultra X | Loja do João",
      "metadata": {
        "seo": {
          "description": "Compre o Notebook Ultra X com o melhor preço e condições. Processador rápido, tela incrível e design leve.",
          "keywords": "notebook, ultra x, comprar notebook, laptop"
        },
        "og": {
          "title": "Notebook Ultra X | Loja do João",
          "type": "product",
          "image": "https://www.lojadojoao.com/images/notebook-ultra-x.jpg",
          "url": "https://www.lojadojoao.com/produto/notebook-ultra-x",
          "description": "Compre o Notebook Ultra X com o melhor preço e condições.",
          "site_name": "Loja do João"
        },
        "schema": [ // Pode haver múltiplos schemas na página
          {
            "@context": "https://schema.org",
            "@type": "Product",
            "name": "Notebook Ultra X",
            "image": "https://www.lojadojoao.com/images/notebook-ultra-x.jpg",
            "description": "O Notebook Ultra X oferece performance e portabilidade.",
            "sku": "NB-ULTRAX-123",
            "mpn": "789012345",
            "brand": {
              "@type": "Brand",
              "name": "UltraTech"
            },
            "offers": {
              "@type": "Offer",
              "url": "https://www.lojadojoao.com/produto/notebook-ultra-x",
              "priceCurrency": "BRL",
              "price": "4799.90",
              "availability": "https://schema.org/InStock",
              "itemCondition": "https://schema.org/NewCondition"
            }
          },
          {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
              {
                "@type": "ListItem",
                "position": 1,
                "name": "Eletrônicos",
                "item": "https://www.lojadojoao.com/eletronicos"
              },
              {
                "@type": "ListItem",
                "position": 2,
                "name": "Notebooks",
                "item": "https://www.lojadojoao.com/eletronicos/notebooks"
              }
            ]
          }
        ]
      }
    },
    {
      "eventId": "evt_c8a3d1f9-0e4b-4b6f-8e7a-6f1d0a9b3e5c",
      "type": "click",
      "timestamp": "2025-05-26T14:31:15.456Z",
      "url": "https://www.lojadojoao.com/produto/notebook-ultra-x",
      "pageTitle": "Notebook Ultra X | Loja do João",
      "metadata": {
        "elementSelector": "button#add-to-cart-btn.btn.btn-primary",
        "elementText": "Adicionar ao Carrinho",
        "elementId": "add-to-cart-btn",
        "elementClasses": "btn btn-primary"
      }
    },
    {
      "eventId": "evt_b2f8e9c4-1d5a-4c8e-9a7b-0f3e1a8d7c6b",
      "type": "add_to_cart",
      "timestamp": "2025-05-26T14:31:15.987Z",
      "url": "https://www.lojadojoao.com/produto/notebook-ultra-x",
      "pageTitle": "Notebook Ultra X | Loja do João",
      "metadata": {
        "productId": "NB-ULTRAX-123",
        "productName": "Notebook Ultra X",
        "quantity": 1,
        "price": 4799.90,
        "currency": "BRL",
        "cartTotalItems": 1,
        "cartTotalValue": 4799.90
      }
    },
    {
      "eventId": "evt_d4e9f0a8-2c6b-4a9d-8b1e-7g4f2b9e8d7c",
      "type": "scroll_depth",
      "timestamp": "2025-05-26T14:32:05.000Z",
      "url": "https://www.lojadojoao.com/produto/notebook-ultra-x",
      "pageTitle": "Notebook Ultra X | Loja do João",
      "metadata": {
        "percentage": 75
      }
    }
  ]
}
```

---

### Entendido! A premissa é que a "mágica" aconteça com a inserção de apenas uma linha de código, e o tracker se encarregue de "ouvir" e "interpretar" os eventos DOM e `Workspace`/`XHR` automaticamente, sem que o desenvolvedor precise adicionar instrumentação específica em cada botão ou elemento.

Isso significa que o tracker precisa ser inteligente em como ele observa a página e infere o significado das interações.

Aqui está a seção de eventos revisada, com essa filosofia em mente:

---

### Exemplos de Eventos que o Tracker Deve Ser Capaz de Capturar Automaticamente (com uma única linha de código):

O tracker, uma vez inserido, atuará como um observador inteligente da atividade do usuário, utilizando listeners globais para eventos DOM, monitoramento de chamadas de rede (`Workspace`/`XHR` quando relevante e possível de forma genérica), e heurísticas para interpretar essas interações.

**1. Eventos de Navegação e Engajamento Essenciais (Captura Automática Direta):**

* `page_view` (ou `page_enter`):
  * **Como**: Disparado automaticamente no carregamento inicial da página e em cada mudança de URL detectada em SPAs (via History API, `popstate`, `hashchange`).
  * **Finalidade**: Marco de entrada e visualização de uma nova página/tela. Base para a jornada do usuário e cálculo de tempo.
* `page_exit` (ou `page_leave`):
  * **Como**: Disparado quando o tracker detecta uma tentativa de sair da página (ex: `beforeunload`, `pagehide`, `visibilitychange` para `hidden` interpretado como saída). Usa `navigator.sendBeacon` para maior confiabilidade na entrega do evento.
  * **Finalidade**: Marco de saída de uma página, crucial para entender o fluxo e calcular tempo na última página da sessão.
* `visibility_change`:
  * **Como**: Listener para o evento `visibilitychange` do browser.
  * **Finalidade**: Identifica se a página está em foco (visível) ou em segundo plano, permitindo diferenciar tempo ativo de tempo passivo na página.
* `scroll_depth`:
  * **Como**: Monitorando o evento `scroll` globalmente e calculando a profundidade atingida (com debounce/throttle para performance).
  * **Finalidade**: Mede o engajamento com o conteúdo da página.
* `page_ping` (ou `heartbeat`):
  * **Como**: Lógica interna do tracker que envia um evento em intervalos regulares (ex: a cada 10-30 segundos) apenas se a página estiver ativa e em foco.
  * **Finalidade**: Ajuda a calcular com mais precisão o tempo de engajamento ativo e a identificar sessões longas ou abandonadas.

**2. Eventos de Interação do Usuário (Captura Automática com Heurísticas e Observação DOM):**

* `click`:
  * **Como**: Listener global de cliques. O tracker captura o evento e coleta informações sobre o elemento clicado (tag, ID, classes, texto, atributos `data-*`).
  * **Finalidade**: Interação genérica. A *interpretação semântica* do clique (ex: "clique em navegação", "clique em CTA") é feita a posteriori ou por heurísticas baseadas no contexto do elemento.
* `form_submission`:
  * **Como**: Listener global para o evento `submit` em formulários.
  * **Finalidade**: Indica que o usuário tentou enviar um formulário.
  * **Heurísticas para contexto**: O tracker pode tentar inferir o tipo de formulário (login, busca, contato) baseado em atributos do formulário (`name`, `id`, `action`) ou nomes de campos comuns. A captura dos dados dos campos em si deve ser opcional e consciente da privacidade.
* `element_view` (ou `impression`):
  * **Como**: Utilizando `IntersectionObserver` para detectar quando elementos específicos (que podem ser definidos por seletores CSS genéricos ou padrões comuns, ex: `[data-track-impression]`, banners com `role="banner"`) entram na viewport.
  * **Finalidade**: Rastrear a visualização de componentes chave da interface.

### **Eventos DOM Nativos para Rastrear Comportamento do Usuário**

| Evento DOM | Como capturar | O que revela |
| -- | -- | -- |
| `DOMContentLoaded` | `document.addEventListener('DOMContentLoaded', ...)` | Carregamento da página (marca início real de interação). |
| `load` | `window.addEventListener('load', ...)` | Página e recursos carregados (imagens, scripts). |
| `beforeunload` | `window.addEventListener('beforeunload', ...)` | Tentativa de fechar ou atualizar aba (usa `sendBeacon`). |
| `unload` | `window.addEventListener('unload', ...)` | Similar ao acima, mas menos confiável. |
| `visibilitychange` | `document.addEventListener('visibilitychange', ...)` | Detecta quando a aba perde ou ganha foco. |
| `focus` / `blur` | `window.addEventListener('focus'/'blur', ...)` | Detecta troca de aba ou minimização. |
| `mousemove` | `document.addEventListener('mousemove', ...)` | Detecta movimentação do mouse (usado para detectar idle). |
| `mousedown` / `mouseup` | `document.addEventListener('mousedown', ...)` | Interação com mouse. Útil para detectar foco/ação. |
| `click` | `document.addEventListener('click', ...)` | Captura cliques em qualquer elemento. Use `event.target` para contexto. |
| `dblclick` | `document.addEventListener('dblclick', ...)` | Captura cliques duplos. Pode indicar frustração. |
| `touchstart` / `touchend` | `document.addEventListener('touchstart', ...)` | Para dispositivos mobile/touch. Alternativa ao click. |
| `scroll` | `window.addEventListener('scroll', ...)` | Detecta rolagem. Combine com `window.scrollY` para medir profundidade. |
| `resize` | `window.addEventListener('resize', ...)` | Pode indicar troca de orientação/dispositivo. |
| `keydown` / `keyup` | `document.addEventListener('keydown', ...)` | Captura digitação (útil para detectar busca, preenchimento de forms). |
| `input` | `document.addEventListener('input', ...)` | Detecta entrada em campos `<input>`, `<textarea>`. Heurística para formulário ativo. |
| `submit` | `document.addEventListener('submit', ...)` | Submissão de formulários. Pode inferir ações como login, busca, contato. |
| `hashchange` | `window.addEventListener('hashchange', ...)` | Para SPAs que usam # na URL. Detecta troca de "rotas". |
| `popstate` | `window.addEventListener('popstate', ...)` | Navegação para trás/avanço em SPAs. Detecta mudança de rota. |
| `wheel` | `document.addEventListener('wheel', ...)` | Detecta movimento do scroll, inclusive com mouse/trackpad. |
| `contextmenu` | `document.addEventListener('contextmenu', ...)` | Clique com botão direito. Pode ser usado para detectar curiosidade ou tentativa de copiar. |
| `dragstart` / `drop` | `document.addEventListener('dragstart', ...)` | Para ações de arrastar (drag & drop). |
| `copy` / `paste` / `cut` | `document.addEventListener('copy', ...)` | Quando o usuário copia ou cola conteúdo. Pode ser usado para detectar interesse em um texto. |

---

### 🧠 Combinando para detectar heurísticas:

* **Idle** = Sem `mousemove`/`keydown`/`scroll`/`click` por X segundos.
* **Rage Click** = Muitos `click` em curto intervalo (mesmo `clientX`, `clientY`).
* **Scroll Profundo** = Detectar `scroll` com `window.innerHeight + window.scrollY >= document.body.offsetHeight`.
* **Mouse fora da tela** = `mouseout` com `event.relatedTarget === null` no topo da página → intenção de saída.
* **Form abandonado** = Evento `input` + `beforeunload` sem `submit`.

**3. Eventos Semânticos de Alto Nível (Captura Automática via Heurísticas Avançadas, Padrões de URL, e/ou Detecção de Data Layer Existente):**

A captura 100% automática desses eventos sem *nenhuma* convenção no site cliente é desafiadora, mas o tracker se esforçará ao máximo usando: \* **Análise de URL**: Certos padrões de URL após interações podem indicar eventos (ex: `/checkout/success` => `purchase`). \* **Inspeção de** `Workspace`/`XHR`: Monitorar chamadas de rede (ex: para `/api/cart/add`) pode, em alguns casos, inferir eventos. (Isso requer cuidado para não capturar dados sensíveis e respeitar políticas de segurança). \* **Detecção de Padrões de DOM/Texto**: Clicar em um botão com texto "Adicionar ao Carrinho" ou a aparição de um texto "Produto adicionado com sucesso!" pode ser uma heurística. \* **Escuta de Data Layers (se presentes)**: Se o tracker detectar um `dataLayer` (como o do GTM), ele pode automaticamente se inscrever para ouvir eventos padronizados (ex: e-commerce events do GA4) que já estejam sendo enviados para lá. Isso ainda se encaixa na "uma linha de código" para o tracker, pois ele se adapta ao que já existe.

* `internal_search_executed`:
  * **Como**: Heurística baseada na submissão de um formulário identificado como de busca, ou uma mudança de URL para um padrão de resultados de busca (ex: `/search?q=termo`).
  * **Finalidade**: Entender o que o usuário procura.
* `product_view`:
  * **Como**: Heurística baseada em URLs que seguem padrões de produto (ex: `/produto/...`, `/item/...`) E/OU presença de dados estruturados (Schema.org `Product`) na página.
  * **Finalidade**: Interesse explícito em um produto.
* `add_to_cart_attempt`:
  * **Como**: Heurística por clique em botões com texto/ícones comuns de "adicionar ao carrinho" OU detecção de uma chamada `Workspace`/`XHR` para um endpoint de carrinho OU observação de mudança em um mini-cart no DOM.
  * **Finalidade**: Tentativa de adicionar ao carrinho.
* `checkout_start`:
  * **Como**: Heurística por clique em botões "Finalizar Compra" OU navegação para URL de início de checkout (ex: `/checkout`, `/carrinho/finalizar`).
  * **Finalidade**: Início do funil de conversão.
* `purchase_completed`:
  * **Como**: Heurística por navegação para URL de sucesso/obrigado (ex: `/checkout/order-received`, `/pedido/confirmado`) OU detecção de evento de compra em um `dataLayer` existente.
  * **Finalidade**: Conversão realizada.
* Tentar rastrear fetchs, requisições. 

**Importante sobre Eventos Semânticos:** Para os eventos da categoria 3, a precisão da captura automática sem qualquer codificação adicional pelo cliente dependerá da conformidade do site com padrões web comuns, da clareza de sua estrutura DOM e URLs, ou da existência de um `dataLayer`. O tracker deve ser transparente sobre quais heurísticas utiliza e, idealmente, permitir configurações (ainda dentro do script principal ou via interface da plataforma) para refinar essa detecção em sites específicos, se necessário, sem alterar o código fonte do cliente.

Essa abordagem mantém o princípio da "uma linha de código" para a instalação, focando em captura automática e inteligente, ao mesmo tempo que reconhece os limites e as estratégias para inferir eventos mais complexos.

Esta funcionalidade de tracker seria a base para coletar os dados ricos necessários para o User Behavior Agent e outras análises.

## Histórico de status

- Backlog (backlog): 2025-05-26T20:46:22.214Z → 2025-05-27T04:35:55.405Z
- To-do (unstarted): 2025-05-27T04:35:55.405Z → 2025-05-28T10:23:36.698Z
- Backlog (backlog): 2025-05-28T10:23:36.698Z → 2025-05-28T13:56:37.127Z
- To-do (unstarted): 2025-05-28T13:56:37.127Z → 2025-06-03T12:33:37.098Z
- In Progress (started): 2025-06-03T12:33:37.098Z → 2025-06-10T18:33:01.136Z
- Released (completed): 2025-06-10T18:33:01.136Z → atual

## Relações

—

## Anexos

—
