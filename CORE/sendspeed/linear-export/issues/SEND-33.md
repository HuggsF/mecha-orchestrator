# SEND-33 — [1] Registrar Interações com Tracking Específico

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | Urgent |
| Responsável | andrei.garcia@externo.sendspeed.com |
| Time | Sendspeed |
| Projeto | — |
| Labels | Tracker |
| Parent | — |
| Criada | 2025-06-25T13:41:23.668Z por bruno.heidrich@sendspeed.com |
| Iniciada | 2025-07-10T12:12:36.212Z |
| Concluída | 2025-08-11T13:53:46.347Z |
| Arquivada | 2026-02-15T02:17:35.100Z |
| Vencimento | — |
| Branch | hugofernandes/send-33-1-registrar-interacoes-com-tracking-especifico |
| URL | https://linear.app/sendspeed/issue/SEND-33/1-registrar-interacoes-com-tracking-especifico |

## Descrição

**Como gestor de tráfego**

**Eu quero** registrar eventos específicos usando o tracker
**Para que** eu consiga analisar o resultado de ações

> Os eventos gerados aqui serão utilizados futuramente nas telas de analytics dos cards, que deverão fazer queries puxando esses dados do banco seguindo o nome do evento e os meta_dados.

> **[Imagem 1 — transcrição]:** Diagrama de fluxo (whiteboard) intitulado por dois bullets: "Perdemos 98% do trafego pago em menos de 90s" e "Onde cada usuário parou no funil". Fluxo horizontal da esquerda para a direita com 4 caixas conectadas por setas: (1) caixa roxa "Aquisição / Entrou na página"; (2) caixa verde "Buyer Agent / Entendeu e sugeriu (Preview)" — anotações acima: "Quantas sugestões / Pra quem sugeriu?" — legenda abaixo: `trackerEvent('eventName', data)` e `trackerEvent('track_card_showpreview', data)`; (3) caixa verde "Buyer Agent / Usuário clickou no Preview" — anotações: "Quantos clicks em preview / Quem clickou" — legenda: `trackerEvent('track_card_clickpreview', data)`; (4) caixa verde "Buyer Agent / Usuário clickou CTA do card" — anotações: "Quantos clicks em cta / Quem clickou" — legenda: `trackerEvent('track_card_clickcardcard', data)`. Demonstra o mapeamento de cada etapa do funil do Buyer Agent aos respectivos eventos de tracker.

**Critérios de Aceitação:**

* O evento especifico de card deve ter o padrão por ex. trackerMyEvent(<nome_evento>,json_dados)
* Deve ser um metodo do tracker.js 
* Os cards do BuyerAgent devem ter um agente específico atrelado (nome do evento não configuravel) por exemplo :
  * Os cards criados devem ter seu próprio id
  * trackerMyEvent('track_card_preview_print" ,meta_dados_user_card)
  * trackerMyEvent('track_card_preview_click" ,meta_dados_user_card) 
  * trackerMyEvent('track_buyer_agent_click" ,meta_dados_user_card)
  * trackerMyEvent('track_card_cta_click" ,meta_dados_user_card)

### Exemplo baseado no ExternalUserContext

Atualmente para setar o usuário logado (external user id)

```javascript
__SmartTrack.setExternalUserContext(logged_external_id, {
    "email": logged_email,
    "name": logged_user,
    "city": logged_city
});
```

---

## Todo

- [X] Criar função de setar evento customizado
  - [X] Nome dos eventos: padrão DOM (ofeceremos a lista para o cliente)

## CustomEvents

**Como chamar a função**

```javascript
__SmartTrack.customEvent('PURCHASE_COMPLETED', {
    orderId: 'ORD-1234567890',
    total: 299.99,
    currency: 'USD',
    items: [...],
    paymentMethod: 'credit_card'
});
```

## BuyerAgentEvents

Eventos aceitos

```typescript
'BUYER_AGENT_PREVIEW_BOX',
'BUYER_AGENT_OPEN_CHAT_BOX',
'BUYER_AGENT_CLOSE_CHAT_BOX',
'BUYER_AGENT_CHAT_BOX',
'BUYER_AGENT_NEW_CARD',
'BUYER_AGENT_CARD_CLICK',
'BUYER_AGENT_CARD_CTA_CLICK'
```

Eventos mapeados para o DOM nativo

```typescript
// Buyer Agent Events
'BUYER_AGENT_PREVIEW_BOX': 'pageshow',
'BUYER_AGENT_OPEN_CHAT_BOX': 'click',
'BUYER_AGENT_CLOSE_CHAT_BOX': 'click',
'BUYER_AGENT_CHAT_BOX': 'pageshow',
'BUYER_AGENT_NEW_CARD': 'pageshow',
'BUYER_AGENT_CARD_CLICK': 'click',
'BUYER_AGENT_CARD_CTA_CLICK': 'click',
```

Como chamar a função

```javascript
window.__SmartTrack.buyerAgentEvent('BUYER_AGENT_NEW_CARD', {
    cardId: 'card-789',
    cardType: 'product_recommendation',
    position: { x: 300, y: 150 },
    content: {
        title: 'Recommended Product',
        description: 'Based on your browsing history',
        image: 'product-image.jpg'
    },
    timestamp: Date.now()
});
```

- [X] Criar função de setar eventos de card (interação com cards)
  - [X] Id do card vai nos metadados (json)

BUYER_AGENT_OPEN_CHAT_BOX

```
{
    "timestamp": 1751478547842,
    "buyerAgentEventData": {
        "type": "BUYER_AGENT_OPEN_CHAT_BOX",
        "metadata": {
            "nonReadEvents": 0,
            "status": "disabled",
            "previewBox": "invisible",
            "chatBox": "empty",
            "chatBoxContent": "",
            "timestamp": 1751478547842
        },
        "timestamp": 1751478547842
    },
    "buyerAgentEventString": "BUYER_AGENT_OPEN_CHAT_BOX"
}
```

BUYER_AGENT_CLOSE_CHAT_BOX

```
{
    "timestamp": 1751484952589,
    "buyerAgentEventData": {
      "type": "BUYER_AGENT_CLOSE_CHAT_BOX",
      "metadata": {
        "nonReadEvents": 0,
        "status": "disabled",
        "previewBox": "invisible",
        "chatBox": "empty",
        "chatBoxContent": "",
        "timestamp": 1751484952589
      },
      "timestamp": 1751484952589
    },
    "buyerAgentEventString": "BUYER_AGENT_CLOSE_CHAT_BOX"
  },
}
```

BUYER_AGENT_PREVIEW_BOX

```json
{
    "timestamp": 1751491541022,
    "buyerAgentEventData": {
      "type": "BUYER_AGENT_PREVIEW_BOX",
      "metadata": {
        "pugContent": "div\n  h4 editado agora\n  p Estamos aqui para ajudar\n  button FALAR COM ESPECIALISTA\n  div",
        "dataAttributes": {
          "sendspeedCardId": "card_doubt_risk_mckwx2mf_t2klzz7bs",
          "sendspeedCompanyId": "685ee1397c33dcc03812040d",
          "sendspeedCardCategory": "doubt_risk",
          "sendspeedCardStatus": "active",
          "onClick": "event.stopPropagation();window.open('https://wa.me/5511999999999', '_blank')",
          "onMouseOver": "this.style.opacity='0.9';this.style.transform='translateY(-1px)';this.style.boxShadow='0 2px 4px rgba(0,0,0,0.25)'",
          "onMouseOut": "this.style.opacity='1';this.style.transform='translateY(0)';this.style.boxShadow='0 1px 3px rgba(0,0,0,0.2)'",
          "sendspeedElement": "cta",
          "sendspeedAction": "navigate",
          "sendspeedActionValue": "https://wa.me/5511999999999",
          "sendspeedMetadata": "{\"cardId\":\"card_doubt_risk_mckwx2mf_t2klzz7bs\",\"companyId\":\"685ee1397c33dcc03812040d\",\"category\":\"doubt_risk\",\"status\":\"active\",\"priority\":\"medium\",\"createdAt\":\"2025-07-01T19:20:12.435Z\",\"version\":2}"
        },
        "timestamp": 1751491541020
      },
      "timestamp": 1751491541020
    },
    "buyerAgentEventString": "BUYER_AGENT_PREVIEW_BOX"
  },
}
```

BUYER_AGENT_CHAT_BOX

```
{
    "timestamp": 1751492774492,
    "buyerAgentEventData": {
      "type": "BUYER_AGENT_CHAT_BOX",
      "metadata": {
        "pugContent": "div\n  div\n    div\n      div\n        h3 🎯 Test Message for UI Demo\n        p This is a test message to demonstrate the buyer agent UI functionality!\n        button Go to Platform",
        "dataAttributes": {
          "smarttrackBuyerAgentContent": "",
          "smarttrackBuyerAgentCard": "",
          "atributoTeste": "Teste",
          "companyId": "1231231231231231",
          "companyName": "SendSpeed",
          "atributoQualquer": "Qualquer valor",
          "onClick": "window.open('https://platform.sendspeed.com', '_blank')",
          "atributoInterno": "Atributo interno",
          "atributoDaMelisquencia": "Atributo da melisquencia",
          "onMouseOver": "this.style.transform='scale(1.02)'",
          "onMouseOut": "this.style.transform='scale(1)'"
        },
        "timestamp": 1751492774492
      },
      "timestamp": 1751492774492
    },
    "buyerAgentEventString": "BUYER_AGENT_CHAT_BOX"
  },
}
```

BUYER_AGENT_NEW_CARD

```
{
    "timestamp": 1751496675846,
    "buyerAgentEventData": {
      "type": "BUYER_AGENT_NEW_CARD",
      "metadata": {
        "content": "div\n  div\n    div\n      h4 editado agora\n      p Estamos aqui para ajudar\n      button FALAR COM ESPECIALISTA\n      div\n  div\n    div\n      h3 🎯 Test Message for UI Demo\n      p This is a test message to demonstrate the buyer agent UI functionality!\n      button Go to Platform\n      button Buy NOW!",
        "dataAttributes": {
          "smarttrackBuyerAgentContent": "",
          "smarttrackBuyerAgentCta": "",
          "sendspeedCardId": "card_doubt_risk_mckwx2mf_t2klzz7bs",
          "sendspeedCompanyId": "685ee1397c33dcc03812040d",
          "sendspeedCardCategory": "doubt_risk",
          "sendspeedCardStatus": "active",
          "onClick": "window.open('https://platform.sendspeed.com', '_blank')",
          "onMouseOver": "this.style.transform='scale(1.02)'",
          "onMouseOut": "this.style.transform='scale(1)'",
          "sendspeedElement": "cta",
          "sendspeedAction": "navigate",
          "sendspeedActionValue": "https://wa.me/5511999999999",
          "sendspeedMetadata": "{\"cardId\":\"card_doubt_risk_mckwx2mf_t2klzz7bs\",\"companyId\":\"685ee1397c33dcc03812040d\",\"category\":\"doubt_risk\",\"status\":\"active\",\"priority\":\"medium\",\"createdAt\":\"2025-07-01T19:20:12.435Z\",\"version\":2}",
          "smarttrackBuyerAgentCard": "",
          "atributoTeste": "Teste",
          "companyId": "1231231231231231",
          "companyName": "SendSpeed",
          "atributoQualquer": "Qualquer valor",
          "atributoInterno": "Atributo interno",
          "atributoDaMelisquencia": "Atributo da melisquencia",
          "buyerAgentIsCta": ""
        },
        "timestamp": 1751496675846
      },
      "timestamp": 1751496675846
    },
    "buyerAgentEventString": "BUYER_AGENT_NEW_CARD"
  },
}
```

BUYER_AGENT_CARD_CLICK

```json
{
    "timestamp": 1751496138254,
    "buyerAgentEventData": {
      "type": "BUYER_AGENT_CARD_CLICK",
      "metadata": {
        "dataAttributes": {
          "atributoTeste": "Teste",
          "companyId": "1231231231231231",
          "companyName": "SendSpeed",
          "atributoQualquer": "Qualquer valor",
          "onClick": "window.open('https://platform.sendspeed.com', '_blank')",
          "atributoInterno": "Atributo interno",
          "atributoDaMelisquencia": "Atributo da melisquencia",
          "onMouseOver": "this.style.transform='scale(1.02)'",
          "onMouseOut": "this.style.transform='scale(1)'",
          "buyerAgentIsCta": ""
        },
        "card": "div\n  h3 🎯 Test Message for UI Demo\n  p This is a test message to demonstrate the buyer agent UI functionality!\n  button Go to Platform\n  button Buy NOW!",
        "elementClicked": "<button style=\"background: linear-gradient(to right, rgb(14, 218, 156), rgb(7, 99, 246)); color: white; border: none; padding: 10px 20px; border-radius: 6px; cursor: pointer; font-size: 14px; font-weight: 500; width: 100%; transition: transform 0.2s; transform: scale(1.02);\" data-atributo-interno=\"Atributo interno\" data-atributo-da-melisquencia=\"Atributo da melisquencia\" onmouseover=\"this.style.transform='scale(1.02)'\" onmouseout=\"this.style.transform='scale(1)'\" onclick=\"window.open('https://platform.sendspeed.com', '_blank')\">\n        Go to Platform\n      </button>",
        "timestamp": 1751496138254
      },
      "timestamp": 1751496138254
    },
    "buyerAgentEventString": "BUYER_AGENT_CARD_CLICK"
  },
}
```

BUYER_AGENT_CARD_CTA_CLICK

```json
{
    "timestamp": 1751496146358,
    "buyerAgentEventData": {
      "type": "BUYER_AGENT_CARD_CTA_CLICK",
      "metadata": {
        "dataAttributes": {
          "atributoTeste": "Teste",
          "companyId": "1231231231231231",
          "companyName": "SendSpeed",
          "atributoQualquer": "Qualquer valor",
          "onClick": "window.open('https://platform.sendspeed.com', '_blank')",
          "atributoInterno": "Atributo interno",
          "atributoDaMelisquencia": "Atributo da melisquencia",
          "onMouseOver": "this.style.transform='scale(1.02)'",
          "onMouseOut": "this.style.transform='scale(1)'",
          "buyerAgentIsCta": ""
        },
        "card": "div\n  h3 🎯 Test Message for UI Demo\n  p This is a test message to demonstrate the buyer agent UI functionality!\n  button Go to Platform\n  button Buy NOW!",
        "elementClicked": "<button style=\"background: linear-gradient(to right, rgb(14, 218, 156), rgb(7, 99, 246)); color: white; border: none; padding: 10px 20px; border-radius: 6px; cursor: pointer; font-size: 14px; font-weight: 500; width: 100%; transition: transform 0.2s; transform: scale(1.02);\" data-buyer-agent-is-cta=\"\" data-atributo-interno=\"Atributo interno\" data-atributo-da-melisquencia=\"Atributo da melisquencia\" onmouseover=\"this.style.transform='scale(1.02)'\" onmouseout=\"this.style.transform='scale(1)'\" onclick=\"window.open('https://platform.sendspeed.com', '_blank')\">\n        Buy NOW!\n      </button>",
        "timestamp": 1751496146357
      },
      "timestamp": 1751496146357
    },
    "buyerAgentEventString": "BUYER_AGENT_CARD_CTA_CLICK"
  },
}
```

### Eventos adicionados

Precisamos fazer o fix de alguns cards (filtrar eventos que não devem aparecer no chatbox)

- [X] Filtrar melhor os eventos que não devem aparecer no chatbox e que estão quebrando o layout

> **[Imagem 2 — transcrição]:** Diagrama técnico (whiteboard/wireframe) que mapeia os eventos do Buyer Agent aos seus equivalentes no DOM nativo, com anotações de metadata (caixas rosa). Elementos e eventos representados: **Preview Box** → "PREVIEW_BOX event / DOM equivalente: PAGEVIEW / Metadata: preview HTML content". **ICON** → "BUYER_AGENT_CLICK event / DOM equivalente: CLICK / Metadata: nenhum. Talvez o posicionamento da tela no momento do clique?". Ilustração de um "Chat Box" grande → "CHAT_BOX event / DOM equivalente: PAGEVIEW / Metadata: inner HTML completo do chat box". Chat Box com barra de rolagem/minimizar → "BUYER_AGENT_MINIMIZE_CLICK event / DOM equivalente: CLICK / Metadata: inner HTML completo do chat box, posicao da rolagem dentro do inner?". À direita, três representações de Chat Box: (1) com área carregada → "BUYER_AGENT_CARD_LOAD event / DOM equivalente: PAGEVIEW / Metadata: inner HTML do elemento carregado naquele momento dentro do chatbox"; (2) Chat Box com botões e "CTA", seta saindo → "BUYER_AGENT_CARD_CLICK event / DOM equivalente: CLICK / Metadata: inner HTML do elemento que foi clicado, url do clique"; (3) Chat Box com "CTA", seta saindo → "BUYER_AGENT_CARD_CTA_CLICK event / DOM equivalente: CLICK / Metadata: inner HTML do elemento que foi clicado, url do clique".

> **[Imagem 3 — transcrição]:** Screenshot mostrando um bug de layout (o problema a ser corrigido). No canto inferior direito de uma página, aparece o card/preview do Buyer Agent laranja com texto "editado agora / Estamos aqui para ajudar" e botão verde "FALAR COM ESPECIALISTA", com um badge azul/ciano (ícone de sparkle) exibindo o contador "2" (eventos não lidos). À esquerda veem-se recortes de tags coloridas (verde, verde, amarelo, vermelho). Na parte inferior há o console do navegador aberto (DevTools) exibindo avisos ("⚠ 1  🚫 1", "Default levels", "3 Issues: 🚫 1  ⚠ 2"). Ilustra eventos indevidos aparecendo no chatbox e quebrando o layout.

### Possível melhoria

* Quebrar o arquivo WebSocketStatusIndicator.ts em vários pequenos useCases para cada um dos eventos tratados de maneira separada.
* Também rever o código em busca de funções que se repetem e fazem coisas parecidas (aplicar o DRY)

## Histórico de status

- Backlog (backlog): 2025-06-25T13:41:23.668Z → 2025-07-10T12:12:36.195Z
- Product Review (started): 2025-07-10T12:12:36.195Z → 2025-07-21T12:52:19.933Z
- Pull Request (started): 2025-07-21T12:52:19.933Z → 2025-07-31T14:39:50.194Z
- Product Review (started): 2025-07-31T14:39:50.194Z → 2025-08-11T13:53:46.328Z
- Released (completed): 2025-08-11T13:53:46.328Z → atual

## Relações

—

## Anexos

—
