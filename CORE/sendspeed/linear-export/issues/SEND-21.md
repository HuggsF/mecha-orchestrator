# SEND-21 — Configurador de Widgets Inteligentes (Buyer Agent)

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | Urgent |
| Responsável | Hugo Fernandes |
| Time | Sendspeed |
| Projeto | — |
| Labels | Buyer |
| Parent | — |
| Criada | 2025-06-09T15:44:56.690Z por Hugo Fernandes |
| Iniciada | 2025-07-08T11:59:05.820Z |
| Concluída | 2025-07-21T12:45:15.792Z |
| Arquivada | 2026-01-25T01:58:20.394Z |
| Vencimento | — |
| Branch | hugofernandes/send-21-configurador-de-widgets-inteligentes-buyer-agent |
| URL | https://linear.app/sendspeed/issue/SEND-21/configurador-de-widgets-inteligentes-buyer-agent |

## Descrição

### 🧑‍💼 Como um(a) **gestor(a) de marketing de uma empresa usuária da plataforma Buyer Agent**

Quero **configurar visualmente meus próprios cards (mini e completos) com base em templates pré-definidos**

Para que eu possa **personalizar ofertas de acordo com o comportamento do usuário e contexto da minha loja sem precisar de desenvolvedores**.

---

### 🎯 Critérios de Aceitação

- [ ] O painel do configurador exibe uma lista de templates disponíveis por categoria (`flash_sale`, `abandoned_cart`, `discount_offer`, etc).
- [ ] É possível selecionar um template e ver uma prévia (em tempo real) dos modos **mini** e **completo**.
- [ ] Os campos configuráveis devem ser editáveis no painel lateral (ex: título, descrição, imagem, botão).
- [ ] O sistema valida campos obrigatórios e atualiza a prévia ao digitar.
- [ ] É possível configurar estilos visuais (cor de fundo, cor do texto, fonte, espaçamento, etc).
- [ ] O usuário pode definir as condições de exibição (página, horário, dias da semana, geolocalização, dispositivo).
- [ ] A configuração final deve gerar um JSON pronto para uso pela engine Buyer Agent.
- [ ] O widget pode ser copiado em 1 linha de HTML para ser integrado ao site do cliente.
- [ ] As alterações salvas são versionadas por empresa e armazenadas com controle de autoria e data.

---

### 🧠 Notas Técnicas

* Os widgets são renderizados dinamicamente via `<script data-card="ID_DO_CARD" />`.
* Deve haver suporte a múltiplos ambientes por empresa (ex: staging e produção).
* Todos os campos configuráveis devem estar definidos no esquema de `editableFields` do JSON.
* Usar `localStorage` ou backend temporário para persistência em modo sandbox/editor ao vivo.
* Suporte a fallback para valores padrão.

---

### 🛠 Tecnologias sugeridas

* Frontend: React ou Vue (preferência para Vue 3 + Tailwind)
* Backend (opcional): Node.js / Firebase / Supabase
* Armazenamento: JSON por empresa, versionado
* Renderização dos widgets: iframe ou Shadow DOM para isolamento

---

### 🧪 Testes

* Testes unitários para validação de campos e geração de JSON
* Testes E2E com simulação de visualização em diferentes tamanhos de tela
* Testes de performance no carregamento dos widgets

---

### Estrutura Atual do Card no banco

```json
{
    "_id" : ObjectId("686711742716f7e1c5666723"),
    "id" : "card_conversion_risk_mco0kgci_47f13hp1z",
    "name" : "🎯 Impulso de Conversão",
    "description" : "Card criado para Purchase Intent - Visualização de produtos",
    "category" : "conversion_risk",
    "priority" : "critical",
    "status" : "active",
    "trigger" : {
        "event" : "page_view",
        "delay" : NumberInt(2),
        "conditions" : {
            "device" : "desktop",
            "page_url" : "sendspeed-frontend-dev.fly.dev",
            "session_duration" : NumberInt(30)
        }
    },
    "content" : {
        "title" : "🎯 Momento perfeito para garantir!",
        "subtitle" : "Oferta limitada",
        "message" : "Aproveite esta oportunidade única!",
        "tone" : "friendly"
    },
    "actions" : [
        {
            "id" : "action_1751585140402",
            "type" : "button",
            "label" : "GARANTIR AGORA",
            "action" : "navigate",
            "value" : "/garantir-agora",
            "style" : "primary",
            "_id" : ObjectId("686711742716f7e1c5666724")
        }
    ],
    "design" : {
        "position" : "center",
        "size" : "medium",
        "theme" : "light",
        "animation" : "fade",
        "colors" : {
            "background" : "linear-gradient(135deg, #a8edea, #fed6e3)",
            "text" : "#ffffff",
            "accent" : "#fbbf24"
        }
    },
    "generated_html" : {
        "full_html" : "<!DOCTYPE html>\n<html lang=\"pt-BR\">\n<head>\n  <meta charset=\"UTF-8\">\n  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n  <title>🎯 Impulso de Conversão</title>\n  <style>\n    * {\n      margin: 0;\n      padding: 0;\n      box-sizing: border-box;\n    }\n    \n    body {\n      font-family: Inter, sans-serif;\n      background-color: #f5f5f5;\n      display: flex;\n      justify-content: center;\n      align-items: center;\n      min-height: 100vh;\n      padding: 20px;\n    }\n    \n    .buyer-card {\n      background: linear-gradient(135deg, #a8edea, #fed6e3);\n      color: #ffffff;\n      padding: 24px;\n      border-radius: 12px;\n      font-family: Inter, sans-serif;\n      font-size: 16px;\n      font-weight: normal;\n      font-style: normal;\n      text-align: center;\n      max-width: 400px;\n      width: 100%;\n      margin: 0 auto;\n      box-shadow: 0 10px 25px rgba(0,0,0,0.15);\n      border: 0px solid #e5e7eb;\n      position: relative;\n      overflow: hidden;\n      display: flex;\n      flex-direction: column;\n      align-items: center;\n      justify-content: center;\n    }\n    \n    .buyer-card .emoji {\n      font-size: 32px;\n      margin-bottom: 16px;\n      text-align: center;\n    }\n    \n    .buyer-card h2 {\n      text-align: center;\n      font-weight: bold;\n      margin: 0 0 16px 0;\n      font-size: 24px;\n      width: 100%;\n      line-height: 1.2;\n    }\n    \n    .buyer-card h3 {\n      text-align: center;\n      font-weight: 600;\n      margin: 0 0 16px 0;\n      opacity: 0.9;\n      font-size: 18px;\n      width: 100%;\n      line-height: 1.3;\n    }\n    \n    .buyer-card p {\n      text-align: center;\n      margin: 0 0 24px 0;\n      opacity: 0.8;\n      width: 100%;\n      line-height: 1.6;\n      font-size: 16px;\n    }\n    \n    .buyer-card .actions {\n      display: flex;\n      flex-wrap: wrap;\n      justify-content: center;\n      align-items: center;\n      gap: 8px;\n      width: 100%;\n    }\n    \n    .buyer-card button:hover {\n      transform: translateY(-2px);\n      box-shadow: 0 4px 12px rgba(0,0,0,0.2);\n    }\n    \n    /* Responsividade */\n    @media (max-width: 768px) {\n      .buyer-card {\n        max-width: 90vw;\n        padding: 20px;\n      }\n      \n      .buyer-card h2 {\n        font-size: 20px;\n      }\n      \n      .buyer-card h3 {\n        font-size: 16px;\n      }\n      \n      .buyer-card p {\n        font-size: 14px;\n      }\n      \n      .buyer-card button {\n        font-size: 14px !important;\n        padding: 10px 20px !important;\n      }\n    }\n    \n    \n    .buyer-card {\n      animation: fade 0.5s ease-out;\n    }\n    \n    @keyframes fade {\n      from { opacity: 0; transform: translateY(20px); }\n      to { opacity: 1; transform: translateY(0); }\n    }\n    \n    @keyframes slide {\n      from { transform: translateX(100%); }\n      to { transform: translateX(0); }\n    }\n    \n    @keyframes bounce {\n      0%, 20%, 53%, 80%, 100% { transform: translate3d(0,0,0); }\n      40%, 43% { transform: translate3d(0, -30px, 0); }\n      70% { transform: translate3d(0, -15px, 0); }\n      90% { transform: translate3d(0, -4px, 0); }\n    }\n  \n  </style>\n</head>\n<body>\n  <div class=\"buyer-card\">\n    \n    <h2>🎯 Momento perfeito para garantir!</h2>\n    <h3>Oferta limitada</h3>\n    <p>Aproveite esta oportunidade única!</p>\n    <div class=\"actions\">\n      <button style=\"background-color:#fbbf24;color:white;border:none;font-weight:600;padding:12px 24px;border-radius:12px;cursor:pointer;font-family:Inter, sans-serif;font-size:16px;margin:8px 4px;text-align:center;transition:all 0.3s ease;\" onclick=\"window.open('/garantir-agora', '_blank')\" onmouseover=\"this.style.opacity='0.9';this.style.transform='translateY(-2px)'\" onmouseout=\"this.style.opacity='1';this.style.transform='translateY(0)'\">GARANTIR AGORA</button>\n    </div>\n  </div>\n</body>\n</html>",
        "preview_html" : "<div style=\"\n    background: linear-gradient(135deg, #a8edea, #fed6e3);\n    color: #ffffff;\n    padding: 12px;\n    border-radius: 8px;\n    width: 100%;\n    max-width: 100%;\n    height: 100px;\n    max-height: 100px;\n    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;\n    text-align: center;\n    margin: 0 auto;\n    box-shadow: 0 4px 12px rgba(0,0,0,0.15);\n    position: relative;\n    overflow: hidden;\n    cursor: pointer;\n    line-height: 1.3;\n    transition: all 0.3s ease;\n    display: flex;\n    flex-direction: column;\n    justify-content: center;\n    align-items: center;\n    gap: 8px;\n  \" \n  data-sendspeed-card-id=\"card_conversion_risk_mco0kgci_47f13hp1z\"\n  data-sendspeed-company-id=\"6838710e6d63d23e3271d7c1\"\n  data-sendspeed-card-category=\"conversion_risk\"\n  data-sendspeed-card-status=\"active\"\n  onclick=\"window.open('/garantir-agora', '_blank')\"\n  onmouseover=\"this.style.transform='scale(1.05)'; this.style.boxShadow='0 6px 18px rgba(0,0,0,0.2)';\"\n  onmouseout=\"this.style.transform='scale(1)'; this.style.boxShadow='0 4px 12px rgba(0,0,0,0.15)';\"\n  >\n    <h4 style=\"\n      margin: 0;\n      font-size: 14px;\n      font-weight: 700;\n      line-height: 1.2;\n      text-align: center;\n      color: #ffffff;\n      text-shadow: 0 1px 2px rgba(0,0,0,0.1);\n      word-break: break-word;\n      hyphens: auto;\n      overflow: hidden;\n      display: -webkit-box;\n      -webkit-line-clamp: 2;\n      -webkit-box-orient: vertical;\n      flex-shrink: 0;\n    \" \n    data-sendspeed-element=\"title\"\n    >🎯 Momento perfeito para garantir!</h4>\n    \n    <button style=\"\n      background: #fbbf24;\n      color: white;\n      border: none;\n      padding: 8px 12px;\n      border-radius: 4px;\n      font-size: 11px;\n      font-weight: 600;\n      cursor: pointer;\n      max-width: 100%;\n      text-align: center;\n      margin: 0;\n      transition: all 0.2s ease;\n      box-shadow: 0 2px 6px rgba(0,0,0,0.1);\n      font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;\n      line-height: 1.2;\n      word-break: break-word;\n      hyphens: auto;\n      text-transform: uppercase;\n      letter-spacing: 0.5px;\n      min-height: 24px;\n      flex-shrink: 0;\n      white-space: nowrap;\n      overflow: hidden;\n      text-overflow: ellipsis;\n    \" \n    data-sendspeed-element=\"cta\"\n    data-sendspeed-action=\"navigate\"\n    data-sendspeed-action-value=\"/garantir-agora\"\n    data-buyer-agent-is-cta\n    onclick=\"event.stopPropagation(); window.open('/garantir-agora', '_blank')\"\n    onmouseover=\"this.style.opacity='0.9'; this.style.transform='translateY(-1px)';\"\n    onmouseout=\"this.style.opacity='1'; this.style.transform='translateY(0)';\"\n    >GARANTIR AGORA</button>\n    \n    <!-- Metadata oculta para tracking -->\n    <div style=\"display: none;\" \n         data-sendspeed-metadata='{&quot;cardId&quot;:&quot;card_conversion_risk_mco0kgci_47f13hp1z&quot;,&quot;companyId&quot;:&quot;6838710e6d63d23e3271d7c1&quot;,&quot;category&quot;:&quot;conversion_risk&quot;,&quot;status&quot;:&quot;active&quot;,&quot;priority&quot;:&quot;critical&quot;,&quot;createdAt&quot;:&quot;2025-07-03T23:25:40.689Z&quot;,&quot;version&quot;:1}'></div>\n  </div>\n  \n  <!-- CSS Responsivo para proporções 200x100px -->\n  <style>\n    @media (max-width: 768px) {\n      [data-sendspeed-card-id=\"card_conversion_risk_mco0kgci_47f13hp1z\"] {\n        width: 100% !important;\n        max-width: 180px !important;\n        height: 90px !important;\n        max-height: 90px !important;\n      }\n    }\n    \n    @media (max-width: 480px) {\n      [data-sendspeed-card-id=\"card_conversion_risk_mco0kgci_47f13hp1z\"] {\n        width: 100% !important;\n        max-width: 160px !important;\n        height: 80px !important;\n        max-height: 80px !important;\n        padding: 8px !important;\n      }\n    }\n  </style>",
        "preview_large_html" : "\n    <div style=\"\n      background: linear-gradient(135deg, #a8edea, #fed6e3);\n      color: #ffffff;\n      padding: clamp(12px, 2.5vw, 20px);\n      border-radius: clamp(6px, 1.5vw, 10px);\n      width: 100%;\n      max-width: 100%;\n      min-height: 100px;\n      height: auto;\n      font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;\n      text-align: center;\n      margin: 0 auto;\n      box-shadow: 0 6px 24px rgba(0,0,0,0.15);\n      position: relative;\n      overflow: hidden;\n      cursor: pointer;\n      line-height: 1.4;\n      transition: all 0.3s ease;\n      display: flex;\n      flex-direction: column;\n      justify-content: space-between;\n      gap: clamp(6px, 1.5vw, 12px);\n    \" \n    data-sendspeed-card-id=\"card_conversion_risk_mco0kgci_47f13hp1z\"\n    data-sendspeed-company-id=\"6838710e6d63d23e3271d7c1\"\n    data-sendspeed-card-category=\"conversion_risk\"\n    data-sendspeed-card-status=\"active\"\n    onclick=\"window.open('/garantir-agora', '_blank')\"\n    onmouseover=\"this.style.transform='scale(1.02)'; this.style.boxShadow='0 8px 32px rgba(0,0,0,0.2)';\"\n    onmouseout=\"this.style.transform='scale(1)'; this.style.boxShadow='0 6px 24px rgba(0,0,0,0.15)';\"\n    >\n      <h2 style=\"\n        margin: 0;\n        font-size: clamp(14px, 3vw, 18px);\n        font-weight: 700;\n        line-height: 1.3;\n        text-align: center;\n        color: #ffffff;\n        text-shadow: 0 1px 3px rgba(0,0,0,0.1);\n        flex-shrink: 0;\n      \" \n      data-sendspeed-element=\"title\"\n      >🎯 Momento perfeito para garantir!</h2>\n      \n      \n        <p style=\"\n          margin: 0;\n          font-size: clamp(11px, 2.2vw, 14px);\n          opacity: 0.9;\n          line-height: 1.3;\n          text-align: center;\n          color: #ffffff;\n          flex-shrink: 0;\n        \" \n        data-sendspeed-element=\"subtitle\"\n        >Oferta limitada</p>\n      \n      \n      <p style=\"\n        margin: 0;\n        font-size: clamp(9px, 1.8vw, 12px);\n        opacity: 0.85;\n        line-height: 1.4;\n        text-align: center;\n        color: #ffffff;\n        flex: 1;\n        display: flex;\n        align-items: center;\n        justify-content: center;\n      \" \n      data-sendspeed-element=\"message\"\n      >Aproveite esta oportunidade única!</p>\n      \n      <button style=\"\n        background: #fbbf24;\n        color: white;\n        border: none;\n        padding: clamp(8px, 2vw, 12px) clamp(12px, 3vw, 20px);\n        border-radius: clamp(4px, 1vw, 6px);\n        font-size: clamp(10px, 2.5vw, 14px);\n        font-weight: 600;\n        cursor: pointer;\n        max-width: 100%;\n        text-align: center;\n        margin: 0;\n        transition: all 0.3s ease;\n        box-shadow: 0 3px 12px rgba(0,0,0,0.15);\n        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;\n        line-height: 1.2;\n        min-height: clamp(24px, 5vw, 36px);\n        display: flex;\n        align-items: center;\n        justify-content: center;\n        flex-shrink: 0;\n      \" \n      data-sendspeed-element=\"cta\"\n      data-sendspeed-action=\"navigate\"\n      data-sendspeed-action-value=\"/garantir-agora\"\n      data-buyer-agent-is-cta onclick=\"event.stopPropagation(); window.open('/garantir-agora', '_blank')\"\n      onmouseover=\"this.style.opacity='0.9'; this.style.transform='translateY(-1px)'; this.style.boxShadow='0 4px 16px rgba(0,0,0,0.2)';\"\n      onmouseout=\"this.style.opacity='1'; this.style.transform='translateY(0)'; this.style.boxShadow='0 3px 12px rgba(0,0,0,0.15)';\"\n      >GARANTIR AGORA</button>\n      \n      <!-- Metadata oculta para tracking -->\n      <div style=\"display: none;\" \n           data-sendspeed-metadata='{&quot;cardId&quot;:&quot;card_conversion_risk_mco0kgci_47f13hp1z&quot;,&quot;companyId&quot;:&quot;6838710e6d63d23e3271d7c1&quot;,&quot;category&quot;:&quot;conversion_risk&quot;,&quot;status&quot;:&quot;active&quot;,&quot;priority&quot;:&quot;critical&quot;,&quot;createdAt&quot;:&quot;2025-07-03T23:25:40.689Z&quot;,&quot;version&quot;:1}'></div>\n    </div>\n\n    <!-- CSS Responsivo Embutido -->\n    <style>\n      @media (max-width: 768px) {\n        [data-sendspeed-card-id=\"card_conversion_risk_mco0kgci_47f13hp1z\"] {\n          margin: 0 auto;\n          width: 95% !important;\n          min-height: 100px !important;\n          height: auto !important;\n        }\n      }\n      \n      @media (max-width: 480px) {\n        [data-sendspeed-card-id=\"card_conversion_risk_mco0kgci_47f13hp1z\"] {\n          width: 100% !important;\n          min-height: 100px !important;\n          height: auto !important;\n          padding: 10px !important;\n        }\n      }\n      \n      @media (prefers-reduced-motion: reduce) {\n        [data-sendspeed-card-id=\"card_conversion_risk_mco0kgci_47f13hp1z\"],\n        [data-sendspeed-card-id=\"card_conversion_risk_mco0kgci_47f13hp1z\"] * {\n          transition: none !important;\n          animation: none !important;\n        }\n      }\n    </style>\n  ",
        "inline_css" : "\n      .buyer-card-mini {\n        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;\n        box-sizing: border-box;\n        transition: all 0.2s ease;\n      }\n      .buyer-card-mini:hover {\n        transform: scale(1.02);\n        box-shadow: 0 4px 12px rgba(0,0,0,0.2);\n      }\n      .buyer-card-mini button:hover {\n        opacity: 0.9 !important;\n      }\n    ",
        "external_css" : "\n      /* Buyer Card Miniatura - Socket Ready */\n      .buyer-card-mini {\n        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;\n        box-sizing: border-box;\n        transition: all 0.2s ease;\n        user-select: none;\n      }\n      \n      .buyer-card-mini:hover {\n        transform: scale(1.02);\n        box-shadow: 0 4px 12px rgba(0,0,0,0.2);\n      }\n      \n      .buyer-card-mini button {\n        transition: all 0.2s ease;\n        user-select: none;\n      }\n      \n      .buyer-card-mini button:hover {\n        opacity: 0.9 !important;\n        transform: scale(1.05);\n      }\n      \n      /* Buyer Card Full - Página Completa */\n      .buyer-card {\n        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;\n        box-sizing: border-box;\n      }\n      \n      .buyer-card button {\n        transition: all 0.3s ease;\n        cursor: pointer;\n        user-select: none;\n      }\n      \n      /* Animações suaves */\n      @keyframes fadeIn {\n        from { opacity: 0; transform: translateY(10px); }\n        to { opacity: 1; transform: translateY(0); }\n      }\n      \n      /* Dark mode support */\n      @media (prefers-color-scheme: dark) {\n        .buyer-card-mini {\n          box-shadow: 0 2px 8px rgba(255,255,255,0.1);\n        }\n      }\n    ",
        "generated_at" : ISODate("2025-07-03T23:25:40.846+0000")
    },
    "frequency" : {
        "max_displays_per_session" : NumberInt(1),
        "max_displays_per_user" : NumberInt(3),
        "cooldown_hours" : NumberInt(24)
    },
    "targeting" : {
        "include_segments" : [

        ],
        "exclude_segments" : [

        ],
        "include_pages" : [

        ],
        "exclude_pages" : [

        ],
        "devices" : [
            "desktop",
            "mobile",
            "tablet"
        ],
        "countries" : [

        ]
    },
    "analytics" : {
        "track_impressions" : true,
        "track_clicks" : true,
        "track_conversions" : false,
        "conversion_goal" : "purchase",
        "custom_events" : [

        ]
    },
    "performance" : {
        "clicks" : NumberInt(0),
        "conversions" : NumberInt(0),
        "conversion_rate" : NumberInt(0),
        "impressions" : NumberInt(0),
        "revenue_generated" : NumberInt(0)
    },
    "companyId" : "6838710e6d63d23e3271d7c1",
    "tenantId" : "tenant_6838710e6d63d23e3271d7c1",
    "created_by" : "684196b0390709bb6c89bd0d",
    "version" : NumberInt(1),
    "createdAt" : ISODate("2025-07-03T23:25:40.689+0000"),
    "updatedAt" : ISODate("2025-07-03T23:25:40.848+0000"),
    "__v" : NumberInt(0)
}
```

## **📊 Campos Principais de Consulta**

### **Campos Obrigatórios de Filtro**

* **companyId** - ID da empresa (obrigatório)


* **category** - Categoria do card (obrigatório)


* **status** - Status do card (sempre filtrado para "active")

---

```typescript
export type CardCategory = "exit_risk" | "doubt_risk" | "conversion_risk";
```

* **exit_risk** - Cards para risco de saída (usuário saindo da página)


* **doubt_risk** - Cards para dúvidas (usuário hesitante)


* **conversion_risk** - Cards para conversão (usuário no funil)

### **Consulta Principal no Repositório**

```
async findByCompanyIdAndCategory(companyId: string, category: CardCategory): Promise<BuyerCardDocument[]> {
  return await this.model.find({ 
    companyId: companyId,
    category: category,
    status: 'active'
  }).sort({ createdAt: -1 }).limit(1);
}
```

### **Campos de Ordenação e Seleção**

* **createdAt** - Ordenação por data de criação (mais recente primeiro)


* **priority** - Prioridade do card ("low", "medium", "high", "critical")


* **version** - Versão do card

### **Campos de Trigger (Condições)**

* **trigger.event** - Tipo de evento:


* exit_intent


* time_on_page


* scroll_depth


* inactivity


* page_view


* click_element


* **trigger.conditions**:


* device - Tipo de dispositivo


* session_duration - Duração da sessão


* page_url - URL da página


* user_segment - Segmento do usuário

### **Campos de Targeting**

* **targeting.devices** - Dispositivos permitidos


* **targeting.include_pages** - Páginas incluídas


* **targeting.exclude_pages** - Páginas excluídas


* **targeting.countries** - Países permitidos

### **Campos de Performance**

* **performance.impressions** - Número de visualizações


* **performance.clicks** - Número de cliques


* **performance.conversion_rate** - Taxa de conversão

## **🔍 Fluxo de Consulta Atual**

1. **Busca por companyId + category + status: 'active'**


1. **Ordenação por createdAt (mais recente primeiro)**


1. **Limite de 1 resultado** (.limit(1))


1. **Retorna o card mais recente da categoria**

## **💡 Campos que Poderiam Influenciar (mas não estão sendo usados)**

* **priority** - Poderia priorizar cards críticos


* **trigger.conditions** - Poderia filtrar por device/página


* **targeting** - Poderia filtrar por segmentação


* **frequency** - Poderia controlar frequência de exibição


* **performance** - Poderia priorizar cards com melhor performance

## Histórico de status

- Refining (backlog): 2025-06-09T15:44:56.690Z → 2025-07-08T11:59:05.795Z
- Product Review (started): 2025-07-08T11:59:05.795Z → 2025-07-21T12:45:15.763Z
- Released (completed): 2025-07-21T12:45:15.763Z → atual

## Relações

—

## Anexos

—
