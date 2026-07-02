# SEND-18 — Análise de Comportamento via IA com Importação de Padrões

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | No priority |
| Responsável | andrei.garcia@externo.sendspeed.com |
| Time | Sendspeed |
| Projeto | SendSpeed 2.0 |
| Labels | Tech Story, Behavior |
| Parent | — |
| Criada | 2025-05-26T22:04:43.623Z por pedro.antunes@sendspeed.com |
| Iniciada | 2025-06-03T12:31:38.211Z |
| Concluída | 2025-06-06T13:58:41.099Z |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-18-analise-de-comportamento-via-ia-com-importacao-de-padroes |
| URL | https://linear.app/sendspeed/issue/SEND-18/analise-de-comportamento-via-ia-com-importacao-de-padroes |

## Descrição

**Como** um analista de produto,
**Quero** poder importar padrões de eventos e acionar uma análise automatizada com IA (GPT-4o-mini),
**Para que** o sistema identifique e classifique comportamentos dos usuários com base nos seus eventos e retorne insights estruturados.

### 📌 Descrição Funcional

* O Behavior Agent será responsável por interpretar os eventos brutos de um usuário, utilizando **IA generativa**.
* O analista pode **clicar no botão "Analisar com Behavior Agent"** em qualquer usuário para acionar a análise.
* A IA processa os **últimos 50 eventos** da sessão por padrão (parâmetro `limit` personalizável).
* A análise utiliza um **prompt estruturado** (já definido) e retorna um JSON com insights detalhados.
* A análise será **salva por usuário, data/hora e sessão** e deverá ser exibida novamente ao acessar o usuário.

---

### ✅ Critérios de Aceite

#### 🧩 1. Interface e Ação

* Deve existir um botão "Analisar com Behavior Agent" acessível na interface de logs do usuário.
* Ao clicar, deve ser exibido um loading com feedback da análise em andamento.
* Após a execução, o resultado deve ser salvo e apresentado em tela.

#### 🔄 2. Input de Análise para a IA (GPT-4o-mini)

* A IA deve receber como `input` os últimos 50 eventos do usuário (ou `limit` definido via parâmetro).
* O formato do input segue um JSON no formato:

```json
{"events": [ ... ] }

Os eventos incluem: eventType, timestamp, url, metadata, searchTerm, timeOnPage, etc.
```

#### 🧠 3. Prompt Utilizado na Análise

* A IA deve utilizar o prompt completo intitulado:

> **Prompt para AI Generativa - Análise de Comportamento do Usuário**

O prompt orienta a IA a gerar um JSON com os seguintes blocos:

* `currentState`
* `intent`
* `patterns`
* `frictionPoints`
* `preferences`
* `journey`
* `predictions`

(⚠️ Todos os campos são obrigatórios e seguem um enum padronizado.)

#### 🧾 4. Armazenamento dos Resultados

* O JSON de resposta deve ser salvo no banco de dados com:
  * `userId` (ou localId se anônimo)
  * `sessionId`
  * `timestamp da análise`
  * `output` (JSON retornado)
* Deve ser possível acessar **sempre a última análise realizada** ao clicar no usuário.

#### 🧪 5. Histórico de Padrões Importados (via JSON)

* Ainda é possível importar manualmente padrões comportamentais personalizados para fins de teste.
* Esses padrões devem ser armazenados para uso posterior ou visualização comparativa.

#### 🔍 6. Exibição dos Resultados

* Os resultados devem ser exibidos em cards visuais separados:
  * Usuário analisado
  * Padrões identificados (ex: "Usuário converteu", "Explorador confuso")
  * Recomendação (ex: "Oferecer produtos similares")
* O JSON original da análise também pode ser exibido via modal ou aba "Detalhado".

---

### 💡 Exemplo de Comportamento Esperado

Ao clicar em **"Analisar com Behavior Agent"** para `Maria Silva`:

* O sistema coleta os **últimos 50 eventos** da sessão atual de Maria.
* Esses eventos são enviados para a IA com o prompt padrão.
* A IA retorna o JSON com insights como:
  * `intent.primary = purchase_research`
  * `frictionPoints.detected = [quick_exits, repeated_search]`
  * `purchaseProbability = 0.82`
* Esse resultado é salvo com a marcação da data e sessão, e apresentado em tempo real.

---

### 📁 Parâmetros Customizáveis

| Parâmetro | Descrição | Default |
| -- | -- | -- |
| `limit` | Número máximo de eventos enviados para a IA | `50` |
| `sessionId` | Sessão específica (se não for a atual) | `null` |
| `mode` | `auto` ou `manual` | `manual` |

Prompt : 

```
Você é um sistema especializado em análise comportamental que processa eventos brutos de usuários e gera insights estruturados. Sua tarefa é analisar a sequência de eventos fornecida e retornar um JSON com insights comportamentais detalhados.
Instruções
Analise os eventos fornecidos e identifique:
O estado atual do usuário (última atividade, tempo na página, duração da sessão)
A intenção principal do usuário baseada no comportamento
Padrões de navegação e comportamento
Pontos de fricção ou frustração
Preferências inferidas dos eventos
Estágio da jornada do usuário
Probabilidades e riscos (compra, abandono, próximas ações)
Formato de Entrada
Você receberá eventos no seguinte formato:

json
{  "events": [    {      "id": "string",      "eventType": "pageview|click|search|pageExit|add_to_cart|purchase|etc",      "timestamp": "ISO 8601 format",      "url": "string",      "searchTerm": "string (para eventos de busca)",      "timeOnPage": "number (segundos)",      "metadata": {        "title": "string",        "category": "string",        "price": "number",        ...
      }    }  ]}
Formato de Saída Esperado
Retorne EXATAMENTE neste formato JSON:

json
{  "currentState": {    "isActive": boolean,    "currentPage": "última página visitada ou 'exit' se saiu",    "timeOnCurrentPage": número em segundos,    "sessionDuration": duração total em segundos,    "lastAction": "tipo_da_última_ação",    "lastActionTime": "X seconds/minutes ago"  },  "intent": {    "primary": "purchase_research|browsing|price_comparison|specific_product|support|information_seeking",    "confidence": número entre 0 e 1,    "stage": "awareness|consideration|evaluation|decision",    "urgency": "low|medium|high",    "specificNeeds": ["array de necessidades detectadas"]  },  "patterns": {    "navigationStyle": "random|focused|methodical",    "decisionSpeed": "fast|medium|slow",    "pricesSensitivity": "low|medium|high|unknown",    "researchDepth": "shallow|medium|deep",    "returnVisitor": boolean,    "crossDeviceBehavior": "single_device|started_mobile_continued_desktop|multi_device"  },  "frictionPoints": {    "detected": [      {        "type": "repeated_search|quick_exits|form_abandonment|navigation_confusion|no_results",        "detail": "descrição específica do problema",        "timestamp": "quando ocorreu em formato humano"      }    ],    "frustrationLevel": número entre 0 e 1  },  "preferences": {    "priceRange": { "min": número ou null, "max": número ou null },    "brands": ["array de marcas mencionadas ou clicadas"],    "features": ["características identificadas"],    "categories": ["categorias visitadas"],    "excludes": ["itens evitados"]  },  "journey": {    "stage": "first_visit|returning|frequent",    "touchpoints": número de interações,    "daysInJourney": 0 se primeira visita ou número de dias,    "previousVisits": [      { "date": "X days ago", "action": "ação principal" }    ],    "progressionVelocity": "slow|normal|fast"  },  "predictions": {    "purchaseProbability": número entre 0 e 1,    "churnRisk": número entre 0 e 1,    "cartAbandonmentRisk": número entre 0 e 1,    "nextLikelyAction": "provável próxima ação",    "estimatedTimeToDecision": "immediately|today|this_week|uncertain"  }}
Regras de Análise
Para currentState:
Calcule sessionDuration somando todos os tempos
Se último evento foi pageExit, isActive = false
lastActionTime deve ser relativo ao momento atual
Para intent:
purchase_research: buscas por produtos, visualização de preços
browsing: navegação sem foco claro
support: buscas por "ajuda", "faq", "contato"
information_seeking: visualização de páginas institucionais
Para patterns:
random: mudanças rápidas entre páginas não relacionadas
methodical: progressão lógica, tempo adequado em cada página
focused: navegação direta para objetivo específico
Para frictionPoints:
quick_exits: tempo < 10 segundos em páginas
repeated_search: mesma busca múltiplas vezes
navigation_confusion: padrão errático de navegação
Para frustrationLevel:
0.0-0.3: Baixo (navegação normal)
0.4-0.6: Médio (alguns problemas)
0.7-1.0: Alto (múltiplos indicadores de frustração)
Para predictions:
purchaseProbability alta: visualizou produtos, preços, adicionou ao carrinho
churnRisk alto: exits rápidos, busca por ajuda, padrão errático
Base-se no comportamento observado para prever próximas ações
Exemplo de Análise
Para eventos de um usuário confuso que procura ajuda:
Navegação errática entre páginas → navigationStyle: "random"
Busca por "ajuda" → intent.primary: "support"
Saídas rápidas → frictionPoints com "quick_exits"
frustrationLevel: 0.8 (alto)
churnRisk: 0.9 (muito alto)

Importante
Analise TODOS os eventos em sequência
Para cada campo em "predictions", adicione também
"reason": "explicação concisa (≤ 200 caracteres) dos sinais que levaram a esse valor".
Exemplo:
"purchaseProbability": {
  "score": 0.76,
  "reason": "Adicionou 2 itens ao carrinho e clicou em 'Pagamento'."
}
Identifique padrões temporais (tempo entre ações)
Considere o contexto completo da sessão
Seja específico nos detalhes mas use apenas os valores enum fornecidos
Retorne APENAS o JSON, sem explicações adicionais
Todos os campos são obrigatórios - use valores padrão sensatos quando não houver dados
Agora analise os seguintes eventos e retorne o JSON de insights: {{events}}
```

Output exemplo: 

```
Output exemplo:
{   "currentState": {     "isActive": false,     "currentPage": "exit",     "timeOnCurrentPage": 5,     "sessionDuration": 18,     "lastAction": "pageExit",     "lastActionTime": "a few seconds ago"   },   "intent": {     "primary": "support",     "confidence": 0.9,     "stage": "consideration",     "urgency": "medium",     "specificNeeds": ["precisa de ajuda", "busca por informações de suporte"]   },   "patterns": {     "navigationStyle": "random",     "decisionSpeed": "fast",     "pricesSensitivity": "unknown",     "researchDepth": "shallow",     "returnVisitor": false,     "crossDeviceBehavior": "single_device"   },   "frictionPoints": {     "detected": [       {         "type": "quick_exits",         "detail": "Usuário saiu rapidamente das páginas 'Produtos', 'Sobre' e 'FAQ'",         "timestamp": "a few seconds ago"       },       {         "type": "navigation_confusion",         "detail": "Sequência desordenada de navegação sem foco claro",         "timestamp": "a few seconds ago"       }     ],     "frustrationLevel": 0.8   },   "preferences": {     "priceRange": { "min": null, "max": null },     "brands": [],     "features": [],     "categories": [],     "excludes": []   },   "journey": {     "stage": "first_visit",     "touchpoints": 8,     "daysInJourney": 0,     "previousVisits": [],     "progressionVelocity": "fast"   },   "predictions": {
  "purchaseProbability": {
    "score": 0.82,
    "reason": "Usuário visualizou 3 produtos, adicionou 1 item ao carrinho e iniciou checkout."
  },
  "cartAbandonmentRisk": {
    "score": 0.35,
    "reason": "Ainda não abandonou o checkout; tempo de inatividade inferior a 2 min."
  },
  "churnRisk": {
    "score": 0.12,
    "reason": "Visitante frequente (5 vezes no mês) e tempo médio de sessão > 4 min."
  },
  "nextLikelyAction": {
    "value": "finalizar_compra",
    "reason": "Checkout step 2 concluído; nenhum sinal de frustração recente."
  },
  "estimatedTimeToDecision": {
    "value": "today",
    "reason": "Historicamente este usuário conclui compra no mesmo dia após add-to-cart."
  }
} }
```

Coloque toda a resposta na anállise do frontend.

## Histórico de status

- Backlog (backlog): 2025-05-26T22:04:43.623Z → 2025-05-27T04:34:49.822Z
- To-do (unstarted): 2025-05-27T04:34:49.822Z → 2025-05-28T10:19:56.645Z
- Backlog (backlog): 2025-05-28T10:19:56.645Z → 2025-05-28T13:56:25.965Z
- To-do (unstarted): 2025-05-28T13:56:25.965Z → 2025-06-03T12:31:30.555Z
- In Progress (started): 2025-06-03T12:31:30.555Z → 2025-06-06T13:58:41.082Z
- Released (completed): 2025-06-06T13:58:41.082Z → atual

## Relações

- relatedTo: SEND-10 — Autenticação Segura de Usuário da Empresa Cliente

## Anexos

—
