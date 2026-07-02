# SEND-473 — Qualidade de Lista + Segmentos de Lista

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | Urgent |
| Responsável | Vinicius Carneiro |
| Time | Sendspeed |
| Projeto | — |
| Labels | Implementação |
| Parent | — |
| Criada | 2026-05-07T19:03:30.347Z por paulo.ribeiro@sendspeed.com |
| Iniciada | 2026-05-11T12:48:09.685Z |
| Concluída | 2026-06-22T17:15:33.188Z |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-473-qualidade-de-lista-segmentos-de-lista |
| URL | https://linear.app/sendspeed/issue/SEND-473/qualidade-de-lista-segmentos-de-lista |

## Descrição

**Área:** Audiência / Listas
**Status Frontend:** ✅ Implementado
**Status Backend:** ⏳ Pendente (sugestões ao final deste documento)
**Ambiente:** Branch `fix/send-473-qualidade-de-lista`

---

## **Resumo Executivo**

Foram implementadas duas novas funcionalidades no módulo de Listas da plataforma:

1. **Qualidade de Lista** — validação automática dos campos de contato (telefone, email, CPF, nome) com score de saúde por lista e relatório de erros no fluxo de upload de CSV.
2. **Segmentos de Lista** — novo recurso que permite combinar múltiplas listas por lógica de **União (OU)** ou **Exclusão (MENOS)**, criando audiências compostas para uso em campanhas.

Ambas as funcionalidades estão completamente implementadas no frontend com dados simulados onde o backend ainda não tem suporte. O comportamento é idêntico ao que será entregue com integração real.

---

## **Casos de Uso**

### **UC-01 — Upload de CSV com sanitização automática**

**Ator:** Operador de marketing
**Fluxo:**

1. Operador acessa uma lista estática em `/audience/lists/:id`
2. Clica em "Adicionar Contatos → Importar arquivo"
3. Arrasta ou seleciona um arquivo CSV (com telefones no formato `+5511987654321`, `(11) 9.8765-4321`, etc.)
4. Mapeia as colunas para os campos da plataforma
5. Clica em "Ver Qualidade" — o sistema exibe um relatório de validação com percentual de válidos/inválidos por campo
6. Clica em "Importar assim mesmo"
7. **O sistema sanitiza o CSV automaticamente antes de enviar ao backend:** remove `+` do telefone, normaliza email para lowercase, aplica trim nos demais campos
8. Os contatos são importados já com os dados normalizados

**Resultado esperado:** telefone salvo como `5511987654321` independente do formato original no CSV.

---

### **UC-02 — Visualização de saúde da lista**

**Ator:** Operador de marketing
**Fluxo:**

1. Operador acessa `/audience/lists`
2. Visualiza cards das listas — listas estáticas com membros exibem um badge de saúde colorido (verde/amarelo/vermelho) com percentual
3. Entra em uma lista específica
4. Acessa a aba "Qualidade"
5. Visualiza score geral + breakdown por campo (Telefone, Email, CPF, Nome) com barras de progresso, contagem de válidos/inválidos/vazios/duplicados e exemplos de valores inválidos

**Resultado esperado:** operador consegue identificar a qualidade dos dados da lista sem precisar exportar e analisar manualmente.

---

### **UC-03 — Criação de Segmento de Lista por União**

**Ator:** Operador de marketing
**Fluxo:**

1. Operador acessa "Audiência → Segmentos de Lista" na sidebar
2. Clica em "Novo Segmento"
3. Define nome e descrição
4. Escolhe a lógica: **União (OU)**
5. Seleciona 2 ou mais listas existentes
6. O preview calcula em tempo real o total estimado de contatos com deduplicação e o breakdown de contribuição por lista
7. Clica em "Criar Segmento"
8. O segmento aparece na listagem e pode ser usado na criação de campanhas

**Resultado esperado:** operador consegue juntar múltiplas bases de leads sem duplicatas, ampliando o alcance da campanha.

---

### **UC-03b — Criação de Segmento de Lista por Exclusão (Supressão)**

**Ator:** Operador de marketing
**Fluxo:**

1. Operador acessa "Audiência → Segmentos de Lista" na sidebar
2. Clica em "Novo Segmento"
3. Define nome e descrição
4. Escolhe a lógica: **Exclusão (MENOS)**
5. Adiciona a **lista base** primeiro (exibe badge azul "Base")
6. Adiciona uma ou mais **listas de exclusão** (exibem badge vermelho "Excluir")
7. O preview mostra o total estimado após remoção, com seção "Composição" separando base e excluídos
8. Clica em "Criar Segmento"

**Resultado esperado:** operador consegue criar uma audiência que exclui automaticamente optouts, clientes já atendidos ou números com bounce, sem precisar manipular os arquivos manualmente.

---

### **UC-04 — Uso de Segmento de Lista em campanha**

**Ator:** Operador de marketing
**Fluxo:**

1. Operador acessa criação de campanha em `/campaigns/new`
2. Na Seção 1 (Nome e Audiência), clica no toggle "Segmento de Lista"
3. Seleciona um segmento criado previamente
4. O sistema exibe o total estimado de contatos e a lógica do segmento
5. Continua o fluxo normal de criação de campanha

**Resultado esperado:** campanha criada com audiência baseada em segmento composto.

---

## **O que foi implementado no Frontend**

### `lib/listValidation.ts` — Biblioteca de validação

| Função | Descrição |
| -- | -- |
| `validatePhone(raw)` | Normaliza e valida número brasileiro. Aceita `+55...`, `(11)...`, `55 11 9...`. Rejeita números com dígitos insuficientes ou DDI inválido. |
| `validateCPF(raw)` | Algoritmo Módulo 11 completo. Valida os dois dígitos verificadores. Rejeita sequências iguais (ex: `111.111.111-11`). |
| `validateEmail(raw)` | Presença de `@`, domínio com TLD e ausência de espaços. |
| `validateName(raw)` | Rejeita vazio, único caractere e strings somente numéricas. |
| `detectDuplicates(values)` | Conta duplicatas em um array de strings. |
| `runQualityReport(rows, mapping)` | Roda todas as validações sobre linhas de CSV e retorna breakdown por campo. **Dado real — baseado na amostra retornada pelo preview do backend.** |
| `sanitizeCsvFile(csvText, mapping, hasHeader)` | Sanitiza CSV antes do upload: `normalizePhone()` na coluna de telefone, `trim().toLowerCase()` no email, `trim()` nos demais. Suporta campos com aspas (RFC 4180). |
| `mockQualityReport(listId, count)` | Gera dados simulados determinísticos para a aba Qualidade. **Dado simulado — substituir quando o endpoint de backend existir.** |
| `getHealthColor(score)` | Retorna `'green'`, `'yellow'` ou `'red'` baseado no score. |
| `getHealthLabel(score)` | Retorna `'Excelente'`, `'Regular'` ou `'Crítica'`. |

---

### `ListsPage.tsx` — `/audience/lists`

* Badge de saúde percentual nos cards de listas estáticas com membros
* Fix: modal "Nova Lista" agora reseta corretamente com tipo padrão "Estática"
* Botão de atalho "Segmentos de Lista" no toolbar

---

### `ListDetailPage.tsx` — `/audience/lists/:id`

* **Aba Qualidade:** score geral + breakdown por campo com barras de progresso, contagens e amostras de erros
* **Relatório de Qualidade no upload:** etapa "Ver Qualidade" adicionada entre mapeamento e importação
* **Mapeamento de CPF:** campo CPF adicionado ao mapeamento de colunas no upload, com sanitização automática via `normalizeCPF()` (remove pontos, traços e espaços)
* **Sanitização de CSV:** arquivo normalizado client-side antes de enviar ao backend (phone, email, CPF, nome, externalId)
* **Drag & drop:** área de upload com eventos `onDrop`, `onDragOver`, `onDragEnter`, `onDragLeave` e três estados visuais
* **Fix Configurações:** salva nome e descrição via chamada real à API (`updateList`)
* **Fix Exportar:** gera download CSV dos membros carregados na página atual

---

### `lib/listSegmentsApi.ts` — API de Segmentos (mock)

API mockada com persistência em `sessionStorage` durante a sessão.

Lógicas suportadas: `'union'` e `'exclude'` (tipo `SegmentLogic`).

| Função | Descrição |
| -- | -- |
| `getListSegments()` | Lista todos os segmentos |
| `getListSegmentById(id)` | Busca segmento por ID |
| `createListSegment(payload)` | Cria segmento com estimativa de contatos |
| `deleteListSegment(id)` | Remove segmento |
| `previewListSegment(...)` | Estimativa por lógica: União (95% da soma) ou Exclusão (base − 60% da lista de exclusão) |

**Fórmulas de estimativa (frontend-only):**

* **União:** `totalContatos × 0.95` — assume 5% de overlap entre listas
* **Exclusão:** `base − min(exclusão × 0.6, base)` — assume 60% de overlap da lista de exclusão com a base; resultado nunca negativo

---

### `ListSegmentsPage.tsx` — `/audience/list-segments`

* Listagem de segmentos com cards mostrando nome, lógica (União/Exclusão), listas incluídas, total estimado de contatos e badge de saúde
* Badge azul para União, badge roxo para Exclusão
* Cards explicativos no topo descrevendo cada lógica
* Busca por nome
* Ação de deletar com confirmação

---

### `ListSegmentBuilderPage.tsx` — `/audience/list-segments/new` e `/:id`

* Seleção de 2+ listas com busca
* Toggle de lógica: **União (OU)** vs **Exclusão (MENOS)** com explicação visual
* No modo **Exclusão**: primeira lista recebe badge azul "Base", demais recebem badge vermelho "Excluir"; subtítulo da seção explica a assimetria
* Preview em tempo real adaptado por lógica:
  * **União:** "Contribuição por lista" com barras e percentuais de alcance
  * **Exclusão:** "Composição" com barra azul (base) e barra vermelha (excluídos estimados); label "removidos por exclusão (est.)" em vez de "duplicados removidos"
* Badge de saúde por lista selecionada
* Modo visualização para segmentos existentes (campos somente leitura)

---

### `CreateCampaignPage.tsx` — Seção 1

* Toggle **Listas / Segmento de Lista** na seleção de audiência
* Ao selecionar "Segmento de Lista": dropdown com segmentos disponíveis, total estimado e lógica exibidos

---

### **Rotas e Navegação**

`App.tsx` — Novas rotas adicionadas:

* `/audience/list-segments`
* `/audience/list-segments/new`
* `/audience/list-segments/:id`

`Sidebar.tsx` — Item "Segmentos de Lista" adicionado no submenu de Audiência (entre Listas e Contatos)

---

## **O que é Mock (dados simulados)**

| Onde | O que é simulado | Quando deixa de ser |
| -- | -- | -- |
| Aba "Qualidade" na `ListDetailPage` | Score e breakdown por campo — gerados por `mockQualityReport()` com seed no ID da lista | Quando `GET /api/lists/:id/quality` existir |
| Listagem de Segmentos de Lista | Dois segmentos de exemplo pré-criados e todos os dados de preview | Quando os endpoints de `/api/list-segments` existirem |
| Preview no builder de segmento | Total estimado calculado por heurística: União = 95% da soma; Exclusão = base − 60% da lista de exclusão | Quando `GET /api/list-segments/:id/preview` existir |
| Campanha com Segmento de Lista | Payload enviado ao criar jornada ainda não inclui `listSegmentId` — só funciona visualmente | Quando o campo `audience.type = 'list_segment'` for suportado pela API de jornadas |

> O relatório de qualidade na **etapa de upload** (botão "Ver Qualidade") **não é mock** — roda validação real nas linhas da amostra retornada pelo backend no preview.

> A **sanitização de CSV** antes do upload **não é mock** — o arquivo é efetivamente transformado antes de ser enviado.

---

## **Sugestões de Backend**

> **Atenção:** as sugestões abaixo foram geradas com base no que foi implementado no frontend. São propostas para discussão — o desenvolvedor responsável decide o que implementar, como implementar e em qual ordem. Nenhum item é obrigatório para o funcionamento atual da plataforma.

---

### **Sugestão 1 — Endpoint de qualidade de lista**

**Motivação:** substituir o `mockQualityReport()` da aba Qualidade por dados reais dos membros já importados.

```
GET /api/lists/:id/quality
```

**Response sugerido:**

```
{
  "success": true,
  "data": {
    "totalRows": 10500,
    "healthScore": 94,
    "phone":  { "valid": 9800, "invalid": 450, "empty": 250, "duplicates": 120 },
    "email":  { "valid": 8900, "invalid": 300, "empty": 1300, "duplicates": 45 },
    "cpf":    { "valid": 7200, "invalid": 800, "empty": 2500, "duplicates": 30 },
    "name":   { "valid": 10200, "invalid": 150, "empty": 150, "duplicates": 0 }
  }
}
```

**Impacto no frontend:** trocar `mockQualityReport()` pela chamada real em `ListDetailPage.tsx` e `ListsPage.tsx`. Zero mudança visual.

---

### **Sugestão 2 — Métricas de qualidade no preview de upload**

**Motivação:** o relatório "Ver Qualidade" no fluxo de upload atualmente valida apenas as linhas da amostra (geralmente 5–10 linhas). Retornar métricas calculadas sobre o arquivo completo tornaria o relatório muito mais preciso.

**Endpoint existente a estender:**

```
POST /api/lists/:id/upload/preview
```

**Adição sugerida na response:**

```
{
  "success": true,
  "data": {
    "fileName": "lista.csv",
    "columns": ["..."],
    "sampleRows": [["..."]],
    "quality": {
      "totalRows": 25000,
      "phone":  { "valid": 22000, "invalid": 2000, "empty": 1000, "duplicates": 500 },
      "email":  { "valid": 20000, "invalid": 1500, "empty": 3500, "duplicates": 200 }
    }
  }
}
```

**Impacto no frontend:** exibir dados do campo `quality` quando presente, mantendo a validação client-side como fallback quando ausente.

---

### **Sugestão 3 — Segmentos de Lista (novo recurso)**

**Motivação:** persistir segmentos no banco e realizar deduplicação real de contatos entre listas.

**Endpoints sugeridos:**

```
POST   /api/list-segments          → Criar segmento
GET    /api/list-segments          → Listar segmentos da empresa
GET    /api/list-segments/:id      → Buscar segmento por ID
DELETE /api/list-segments/:id      → Remover segmento
GET    /api/list-segments/:id/preview → Preview com deduplicação real
```

**Payload de criação (**`POST`):

```
{
  "name": "Audiência Futebol",
  "description": "Torcedores Flamengo + Fluminense",
  "listIds": ["list-id-1", "list-id-2"],
  "logic": "union"
}
```

Para exclusão, o campo `logic` seria `"exclude"` e o backend trataria `listIds[0]` como base e os demais como listas de supressão:

```
{
  "name": "Leads sem Optouts",
  "description": "Lista de leads removendo os que pediram saída",
  "listIds": ["list-id-base", "list-id-optouts"],
  "logic": "exclude"
}
```

**Response de preview (**`GET /preview`):

```
{
  "success": true,
  "data": {
    "totalCount": 18450,
    "deduplicatedCount": 2050,
    "breakdown": [
      { "listId": "list-id-1", "listName": "Flamengo", "contributingCount": 12500 },
      { "listId": "list-id-2", "listName": "Fluminense", "contributingCount": 5950 }
    ]
  }
}
```

**Ponto de atenção para o backend:** a deduplicação e exclusão reais precisam cruzar membros pelos campos de identificação (`phone`, `email` ou `externalId`). A lógica de **União** inclui todos os contatos únicos das listas selecionadas (sem repetir). A lógica de **Exclusão** remove da lista base todos os contatos cujo identificador também aparece em qualquer lista de exclusão. O campo de identificação primário para cruzamento é decisão do time de backend — sugestão: `phone` como chave principal, `email` como fallback. O CTO já mencionou complexidade no backend de listas — avaliar impacto antes de implementar.

**Impacto no frontend:** trocar chamadas do `listSegmentsApi.ts` (mock) pela chamada real. Zero mudança visual.

---

### **Sugestão 4 — Suporte a Segmento de Lista na criação de campanha**

**Motivação:** o toggle "Segmento de Lista" na Seção 1 do `CreateCampaignPage` funciona visualmente, mas o payload enviado ao criar a jornada ainda usa apenas `listId`. Para que campanhas com segmento funcionem de ponta a ponta, a API de jornadas precisaria aceitar o campo.

**Verificar se o modelo de** `audience` na jornada aceita ou pode aceitar:

```
{
  "audience": {
    "type": "list_segment",
    "listSegmentId": "seg-001",
    "estimatedCount": 18450
  }
}
```

**Impacto no frontend:** adicionar `listSegmentId` ao payload em `handleSubmit` do `CreateCampaignPage.tsx` quando `audienceType === 'segment'`. Mudança pequena e isolada.

---

## **Arquivos modificados / criados**

```
client/src/lib/listValidation.ts             → NOVO
client/src/lib/listSegmentsApi.ts            → NOVO
client/src/pages/ListSegmentsPage.tsx        → NOVO
client/src/pages/ListSegmentBuilderPage.tsx  → NOVO
client/src/pages/ListsPage.tsx               → MODIFICADO
client/src/pages/ListDetailPage.tsx          → MODIFICADO (+ CPF mapping)
client/src/pages/CreateCampaignPage.tsx      → MODIFICADO
client/src/components/Sidebar.tsx            → MODIFICADO
client/src/App.tsx                           → MODIFICADO
docs/LINEAR-CARD-qualidade-lista-segmentos.md → NOVO
client/public/test-lista-qualidade.csv       → NOVO (arquivo de teste)
client/public/test-erros-validacao.csv       → NOVO (arquivo de teste)
client/public/test-lista-base-exclusao.csv   → NOVO (arquivo de teste exclusão)
client/public/test-lista-optouts-exclusao.csv → NOVO (arquivo de teste exclusão)
```

## Histórico de status
- To-do (unstarted): 2026-05-07T19:03:30.347Z → 2026-05-11T12:48:09.709Z
- In Progress (started): 2026-05-11T12:48:09.709Z → 2026-05-12T16:16:28.788Z
- Product Review (started): 2026-05-12T16:16:28.788Z → 2026-06-22T17:15:33.202Z
- Released (completed): 2026-06-22T17:15:33.202Z → atual

## Relações
—

## Anexos
—
