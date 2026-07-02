# SEND-469 — Módulo de Disparo de Lista Fria (SMS + RCS)

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | Urgent |
| Responsável | Vinicius Carneiro |
| Time | Sendspeed |
| Projeto | — |
| Labels | Melhoria, UserIn |
| Parent | — |
| Criada | 2026-04-29T10:56:41.168Z por paulo.ribeiro@sendspeed.com |
| Iniciada | 2026-05-07T18:47:42.993Z |
| Concluída | 2026-06-22T17:15:35.118Z |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-469-modulo-de-disparo-de-lista-fria-sms-rcs |
| URL | https://linear.app/sendspeed/issue/SEND-469/modulo-de-disparo-de-lista-fria-sms-rcs |

## Descrição

## **Branch**

`fix/send-469-disparo-lista-fria`

## **User Story**

**Como** operador de marketing, **quero** criar e gerenciar disparos em massa via SMS ou RCS para listas de contatos, **para que** eu possa executar campanhas de cold outreach diretamente na plataforma, sem depender de ferramentas externas, e acompanhar os resultados em analytics.

---

## **Contexto**

A plataforma já possui o construtor de jornadas (`/journey-analytics`) e os editores de template SMS e RCS. Este card unifica esses componentes em um fluxo dedicado de **Disparos**, acessível via `Campanhas > Disparos` na sidebar.

Todo disparo de lista fria é internamente criado como uma **Jornada do tipo** `campaign`, aproveitando a infraestrutura já existente de execução e analytics de jornadas.

---

## **Fluxo do usuário (implementado no frontend)**

```
Campanhas > Disparos
  → Novo Disparo
    1. Nome e Audiência (nome do disparo + múltiplas listas)
    2. Canal de envio (SMS ou RCS)
    3. Template da mensagem (selecionar, criar ou duplicar)
       └── RCS: preencher fallback SMS obrigatório
    4. Quando enviar (imediatamente ou agendar data/hora futura — mín. 10 min)
    5. Monitoramento (opcional — lista ou números manuais)
  → Salvar Rascunho ou Disparar
  → Volta para lista de Disparos
  → Ver Analytics em /journey-analytics/:journeyId
```

---

## **Arquivos modificados no frontend**

| Arquivo | Descrição |
| -- | -- |
| `client/src/pages/CampaignsPage.tsx` | Listagem de disparos com filtros, cards de status, ações contextuais |
| `client/src/pages/CreateCampaignPage.tsx` | Formulário de criação/edição em layout 2 colunas |
| `client/src/components/campaigns/TemplateDrawer.tsx` | Drawer lateral para criar/duplicar templates sem sair do fluxo |
| `client/src/components/campaigns/EditWarningDialog.tsx` | Dialog de aviso ao editar template existente |
| `client/src/components/sms/SmsPhonePreview.tsx` | Componente compartilhado de preview SMS |
| `client/src/components/ui/DateTimePicker.tsx` | Picker customizado com filtro de horas/min baseado em mínimo configurável |
| `client/src/lib/campaignsApi.ts` | `getCampaignJourneys`, `createCampaignAsJourney`, `executeCampaignJourney`, `updateCampaignJourney` |
| `client/src/lib/draftStorage.ts` | Persistência local (localStorage) de campos não suportados pelo backend |
| `client/src/components/Sidebar.tsx` | Ícone Megaphone + label "Disparos" no submenu |
| `client/src/components/Layout.tsx` | Prop `contentClassName` para fundo customizado por página |

---

## **O que funciona de ponta a ponta hoje**

* Criar disparo via `POST /api/campaigns/as-journey` (cria JourneyWorkflow tipo `campaign`)
* Executar via `POST /api/journeys/:id/execute-campaign` (CampaignJourneyProcessor processa fila)
* Listar via `GET /api/journeys` (sem filtro por `journeyType` ainda — ver pendências)
* Preview de template SMS e RCS no formulário
* Seleção e criação de template sem sair do fluxo (TemplateDrawer)
* Validações UX: troca de canal, sair com formulário sujo, agendamento < 10 min

---

## **Workarounds temporários no frontend (localStorage)**

O backend não persiste todos os campos enviados pelo frontend. Os campos abaixo são salvos no `localStorage` via `draftStorage.ts` e lidos de volta ao editar o rascunho. **Isso funciona apenas no navegador/dispositivo onde foi criado.** Se outro usuário abrir o rascunho ou o cache for limpo, os dados são perdidos.

| Campo | Onde é salvo | O que o backend precisa fazer |
| -- | -- | -- |
| `scheduledAt` | `draftStorage` + lido em `CampaignsPage` | Adicionar `campaignConfig.schedule` ao schema e persistir |
| `scheduleType` | `draftStorage` | Idem |
| `templateId` / `templateName` | `draftStorage` | Adicionar `campaignConfig.message.templateId` e `templateName` ao schema |
| `rcsContent` | `draftStorage` | Já existe em `campaignConfig.message.rcsContent` — mapear no `PUT` |
| `fallbackSms` | `draftStorage` | Adicionar `campaignConfig.fallbackSms` ao schema |
| `channel` | `draftStorage` | Já existe — mapear no `PUT` |
| `selectedLists` (múltiplas) | `draftStorage` | Backend recebe apenas a 1ª lista — ver item de múltiplas listas |

---

## **Mapeamento de status: frontend ↔ backend**

O schema do backend (`Journey.js`) aceita **apenas** `['draft', 'active', 'paused', 'archived']`. Os demais status são criações do frontend para exibição.

| Status (frontend) | Status (backend) | Situação |
| -- | -- | -- |
| `draft` (Rascunho) | `draft` | Funciona |
| `sending` (Enviando) | `active` | Funciona — frontend renomeia na exibição |
| `paused` (Pausado) | `paused` | Funciona — `PATCH /api/journeys/:id/status` já existe |
| `archived` | `archived` | Funciona — não usado na tela de Disparos |
| `scheduled` (Agendado) | **não existe** | Backend precisa adicionar ao enum |
| `queued` (Na Fila) | **não existe** | Backend precisa adicionar ao enum |
| `completed` (Concluído) | **não existe** | Backend precisa adicionar ao enum |
| `failed` (Falhou) | **não existe** | Backend precisa adicionar ao enum |
| `cancelled` (Cancelado) | **não existe** | Backend precisa adicionar ao enum |

> **Impacto atual:** O frontend sempre usa o fallback `|| j.status` no `JOURNEY_STATUS_MAP`, então se o backend retornar `'completed'` algum dia, o frontend exibiria `completed` literalmente (sem badge). Os status `queued`, `completed`, `failed`, `cancelled`, `scheduled` são exibidos **apenas nos mocks**.

---

## **Features com UI pronta mas sem backend (mocks)**

Todas as ações abaixo têm UI completa, AlertDialogs, Toasts e chamadas HTTP implementadas. Porém os endpoints não existem ainda — as chamadas silenciosamente falham e a UI responde com estado local.

### **Pausar / Retomar / Cancelar disparo em andamento**

**Frontend:** Botão "Pausar" aparece inline para campanhas com status `sending` ou `queued`. Ao confirmar, atualiza o estado local para `paused`. Dois botões aparecem: "Retomar" e "Cancelar".

**Chamadas HTTP (sem resposta):**

```
PATCH /api/journeys/:id/pause    → não existe
PATCH /api/journeys/:id/resume   → não existe
PATCH /api/journeys/:id/cancel   → não existe
```

> Nota: `PATCH /api/journeys/:id/status` JÁ EXISTE. O dev pode usar essa rota e ajustar o frontend para chamá-la em vez das rotas específicas, se preferir. O enum de status precisaria ser expandido.

---

### **Reprocessar falhas**

**Frontend:** Opção no menu ⋮ para campanhas com `status: 'failed'` ou `completed` com `stats.failed > 0`. AlertDialog mostra contagem de falhas. Toast de sucesso sempre aparece (mock).

**Chamadas HTTP (sem resposta):**

```
POST /api/journeys/:id/reprocess   → não existe
```

**O que o backend precisa fazer:**

* Buscar contatos do disparo com `delivery_status: 'failed'`
* Criar novo disparo com os mesmos dados (template, canal, fallback)
* Vincular ao original via `parentJourneyId` para acumular analytics
* Executar imediatamente via `CampaignJourneyProcessor`

---

### **Disparar novamente (nova data, mesma configuração)**

**Frontend:** Abre Sheet lateral com resumo readonly do disparo original + opção de data. Toast de sucesso sempre aparece (mock).

**Chamadas HTTP (sem resposta):**

```
POST /api/journeys/:id/re-fire
Body: { scheduleType: 'now' | 'later', scheduledAt?: string }
→ não existe
```

**O que o backend precisa fazer:**

* Clonar a jornada com todos os `campaignConfig` do original
* Aplicar o novo agendamento
* Criar disparo independente (analytics separados do original)

---

### **Duplicar**

**Frontend:** Chama `POST /api/journeys/:id/duplicate`. **Este endpoint JÁ EXISTE** no backend (linha 24 de `journeyRoutes.js`). O frontend usa um fallback para `/campaigns/new` se a resposta falhar — precisa remover o fallback após confirmar que a rota está mapeando `campaignConfig` corretamente.

**Verificar se o controller** `duplicate`:

* Copia todos os campos de `campaignConfig` (incluindo `message.rcsContent`, `audience`, etc.)
* Define nome como `[Cópia] {nome original}`
* Define status como `draft`

---

### **Múltiplas listas de audiência**

**Frontend:** UI completa com chips removíveis e total estimado. O payload enviado ao backend usa `type: 'list'` com apenas a **primeira lista** selecionada (workaround), porque o backend só aceita `['list', 'segment']` no enum de `audience.type`. As listas adicionais ficam no `draftStorage`.

**O que o backend precisa fazer:**

* Adicionar `'multi-list'` ao enum de `audience.type`
* Adicionar campo `audience.lists[]` ao schema
* Em `CampaignJourneyProcessor`, ao processar `audienceType === 'multi-list'`, fazer union de todos os `listIds` com deduplicação por telefone

---

### **Lista de monitoramento**

**Frontend:** Nova seção opcional no formulário. Suporta seleção de lista existente ou entrada manual de números (somente dígitos). Payload inclui campo `monitoring`. O backend recebe mas ignora o campo (não está no schema).

**O que o backend precisa fazer:**

* Adicionar campo `monitoring` ao schema de `campaignConfig`
* Em `CampaignJourneyProcessor`, ao executar, distribuir os números de monitoramento: início, meio e fim da fila de envio
* Marcar envios de monitoramento com `is_monitoring: true` nos logs

---

## **Pendências de backend — lista completa priorizada**

### **Bloco A — Pré-requisitos (implementar primeiro)**

**A1. Expandir enum de status em** `Journey.js`

```
// platform-backend/backend/src/journey-builder/models/Journey.js — linha 109
status: {
  type: String,
  enum: ['draft', 'active', 'paused', 'archived', 'scheduled', 'queued', 'completed', 'failed', 'cancelled'],
  default: 'draft',
}
```

**A2. Adicionar campos ausentes ao** `campaignConfig` em `Journey.js`

```
campaignConfig: {
  // campos existentes mantidos ...
  message: {
    content: String,
    rcsContent: Mixed,
    preview: String,
    templateId: { type: String, default: null },      // ← ADICIONAR
    templateName: { type: String, default: null },    // ← ADICIONAR
  },
  fallbackSms: { type: String, default: null },       // ← ADICIONAR
  schedule: {                                          // ← ADICIONAR bloco inteiro
    type: { type: String, enum: ['now', 'later'], default: 'now' },
    scheduledAt: { type: Date, default: null },
    timezone: { type: String, default: 'America/Sao_Paulo' },
  },
  // audience.type enum: adicionar 'multi-list'
  audience: {
    type: { type: String, enum: ['list', 'segment', 'multi-list'], default: null },
    listId: ...,
    lists: [{ listId: ObjectId, listName: String, estimatedCount: Number }], // ← ADICIONAR
    // demais campos existentes ...
  },
  monitoring: {                                        // ← ADICIONAR bloco inteiro
    type: { type: String, enum: ['list', 'manual'], default: null },
    listId: { type: ObjectId, ref: 'List', default: null },
    numbers: [String],
    count: { type: Number, default: 0 },
  },
}
```

**A3. Atualizar** `PUT /api/journeys/:id` para persistir `campaignConfig` completo

Hoje o `PUT` só atualiza `name` e `status`. Precisa mapear todos os campos de `campaignConfig` do body para o documento.

**A4. Atualizar** `campaignJourneyBridge.js` para mapear campos ausentes

```
// Campos que hoje não são mapeados em createFromCampaign:
campaignConfig: {
  message: {
    templateId: message?.templateId || null,   // ← ADICIONAR
    templateName: message?.templateName || null, // ← ADICIONAR
    // ...
  },
  fallbackSms: campaignData.fallbackSms || null,  // ← ADICIONAR
  schedule: {                                      // ← ADICIONAR
    type: schedule?.type || 'now',
    scheduledAt: schedule?.scheduledAt ? new Date(schedule.scheduledAt) : null,
    timezone: schedule?.timezone || 'America/Sao_Paulo',
  },
  status: campaignData.status || 'draft',          // ← ADICIONAR (hoje sempre 'draft')
}
```

**A5. Filtro por** `journeyType` no `GET /api/journeys`

```
// journeyService.js — método list()
if (filters.journeyType) query.journeyType = filters.journeyType;
if (filters.channel) query['campaignConfig.channel'] = filters.channel;

// journeyController.js — método list()
const { journeyType, channel } = req.query;
const result = await journeyService.list({ journeyType, channel, ...outrosFilters });
```

**Impacto:** Sem isso, a tela de Disparos mistura jornadas de outros tipos (insite, offsite, etc.).

---

### **Bloco B — Ações (desbloqueadas após Bloco A)**

**B1. Pausar / Retomar disparo**

A rota `PATCH /api/journeys/:id/status` já existe. Bastará que o `changeStatus` no controller aceite os valores `paused` e `active` (retomar) e que o `CampaignJourneyProcessor` respeite a pausa (verificar `journey.status` antes de enfileirar cada batch).

Opcionalmente, adicionar rotas semânticas específicas:

```
PATCH /api/journeys/:id/pause   → muda status para 'paused', interrompe fila
PATCH /api/journeys/:id/resume  → muda status para 'active', retoma fila
```

**B2. Cancelar disparo**

```
PATCH /api/journeys/:id/cancel
→ muda status para 'cancelled', cancela fila pendente
→ salva stats parciais (o que já foi enviado permanece)
```

**B3. Disparar novamente (re-fire)**

```
POST /api/journeys/:id/re-fire
Body: { scheduleType: 'now' | 'later', scheduledAt?: string }
→ Clona campaignConfig do original, cria nova Journey draft, executa ou agenda
→ Response: { success: true, data: { newJourneyId } }
```

**B4. Reprocessar falhas**

```
POST /api/journeys/:id/reprocess
→ Busca contatos com delivery_status 'failed' no MessageHistory
→ Cria nova Journey com mesmos configs, executa apenas para esses contatos
→ Associa via parentJourneyId para acumulação de analytics
→ Response: { success: true, data: { newJourneyId, failedCount } }
```

**B5. Verificar e corrigir** `duplicate`

A rota `POST /api/journeys/:id/duplicate` já existe. Verificar se o controller copia:

* Todos os campos de `campaignConfig` (incluindo `message.rcsContent`, `fallbackSms`, `schedule`, `templateId`)
* Define `status: 'draft'`
* Define `name: '[Cópia] {nome original}'`

O frontend precisa remover o fallback para `/campaigns/new` após confirmação.

**B6. Agendamento real via scheduler**

Quando `schedule.type === 'later'`, o `execute-campaign` não deve executar imediatamente. Opções:

* Cron job que verifica jornadas com `status: 'scheduled'` e `schedule.scheduledAt <= now`
* Bull/BullMQ com delayed job
* Ao salvar com agendamento, o status deve mudar para `scheduled`

---

### **Bloco C — Backlog**

**C1. Múltiplas listas (union + dedup)**

Quando `audience.type === 'multi-list'`, o `CampaignJourneyProcessor` deve:

* Iterar `audience.lists[]` e buscar membros de cada `listId`
* Deduplicar por número de telefone (manter primeiro occurrence)
* O total real (pós-dedup) deve ser salvo em `campaignConfig.stats.totalRecipients`

**C2. Lista de monitoramento**

Quando `campaignConfig.monitoring` estiver configurado:

* Distribuir números de monitoramento: índices 0, meio, fim da fila de envio
* Marcar com `is_monitoring: true` no `MessageHistory`
* Incluir métricas de monitoramento separadas no analytics

**C3. Sanitização automática de listas**

Antes do disparo, validar:

* Formato de telefone (DDI + DDD + número, somente dígitos)
* Remoção de duplicatas na própria lista
* Sinalizar contatos inválidos antes do disparo (`"84 números inválidos detectados"`)

---

## **Contrato de API atual (frontend → backend)**

### **Criar disparo**

```
POST /api/campaigns/as-journey
{
  "name": "Nome do Disparo",
  "channel": "sms" | "rcs",
  "status": "draft" | "active",       // ← backend ignora, sempre cria como draft
  "audience": {
    "type": "list",                    // ← multi-list não suportado ainda
    "listId": "...",
    "listName": "...",
    "estimatedCount": 1200
  },
  "message": {
    "content": "...",
    "rcsContent": { ... },
    "templateId": "...",               // ← backend ignora (não está no schema)
    "templateName": "..."              // ← backend ignora
  },
  "fallbackSms": "...",                // ← backend ignora (não está no schema)
  "schedule": {                        // ← backend ignora (não está no schema)
    "type": "now" | "later",
    "scheduledAt": "2026-05-10T14:00:00.000Z",
    "timezone": "America/Sao_Paulo"
  },
  "monitoring": { ... }               // ← backend ignora (não está no schema)
}
```

### **Executar o disparo**

```
POST /api/journeys/:journeyId/execute-campaign
→ CampaignJourneyProcessor.execute(journeyId)
→ Funciona (processa via Kafka ou síncrono)
```

### **Atualizar rascunho**

```
PUT /api/journeys/:id
Body: { name, status }               // ← só esses dois campos são persistidos hoje
```

### **Listar disparos**

```
GET /api/journeys
→ Retorna TODAS as jornadas da empresa (sem filtro por journeyType)
→ Frontend filtra client-side por journeyType (workaround)
```

### **Duplicar (já existe)**

```
POST /api/journeys/:id/duplicate     // ← EXISTE no backend
→ Verificar se copia campaignConfig completo
```

### **Mudar status (já existe)**

```
PATCH /api/journeys/:id/status       // ← EXISTE no backend
Body: { status: 'paused' | 'active' | 'archived' }
→ Enum atual não inclui 'cancelled', 'completed', 'failed', 'scheduled', 'queued'
```

---

## **Status geral**

| Camada | Status |
| -- | -- |
| UX/Design | Aprovado e implementado |
| Frontend — listagem + ações | Completo |
| Frontend — criação/edição com múltiplas listas | Completo (UI) |
| Frontend — lista de monitoramento | Completo (UI + payload) |
| Frontend — pausar/retomar/cancelar | Completo (mock) |
| Frontend — reprocessar falhas | Completo (mock) |
| Frontend — disparar novamente | Completo (mock) |
| Frontend — duplicar | Completo (chama endpoint existente) |
| Frontend — template drawer/dialog | Completo |
| Frontend — validações UX (10 min, canal, dirty form) | Completo |
| Backend — enum de status incompleto | **Pendente (A1)** |
| Backend — schema com campos ausentes (schedule, templateId, fallbackSms) | **Pendente (A2)** |
| Backend — PUT persiste campaignConfig completo | **Pendente (A3)** |
| Backend — campaignJourneyBridge mapeia campos ausentes | **Pendente (A4)** |
| Backend — filtro journeyType no GET /api/journeys | **Pendente (A5)** |
| Backend — pausar/retomar/cancelar | **Pendente (B1, B2)** |
| Backend — disparar novamente (re-fire) | **Pendente (B3)** |
| Backend — reprocessar falhas | **Pendente (B4)** |
| Backend — verificar duplicate copia campaignConfig | **Pendente (B5)** |
| Backend — agendamento real (scheduler) | **Pendente (B6)** |
| Backend — múltiplas listas (union + dedup) | Backlog (C1) |
| Backend — lista de monitoramento | Backlog (C2) |
| Backend — sanitização de listas | Backlog (C3) |

---

## 

## Histórico de status
- Backlog (backlog): 2026-04-29T10:56:41.168Z → 2026-05-06T19:14:36.221Z
- To-do (unstarted): 2026-05-06T19:14:36.221Z → 2026-05-07T18:47:43.018Z
- In Progress (started): 2026-05-07T18:47:43.018Z → 2026-05-07T20:31:41.911Z
- Pull Request (started): 2026-05-07T20:31:41.911Z → 2026-05-08T12:50:42.057Z
- Product Review (started): 2026-05-08T12:50:42.057Z → 2026-06-22T17:15:35.132Z
- Released (completed): 2026-06-22T17:15:35.132Z → atual

## Relações
—

## Anexos
- feat(SEND-469): Módulo de Disparo de Lista Fria — Frontend completo (SMS + RCS) — https://github.com/sendspeed0/sendspeed-engage-ai-flow-08/pull/46
- feat(SEND-469): Módulo de Disparo de Lista Fria — Backend completo (SMS + RCS) — https://github.com/sendspeed0/platform-backend/pull/34
