---
project_name: sendspeed-absorption
conversation_id: debate-o6-s4-2026-07-02
date: "2026-07-02"
emoji_rail: 📡 ➔ 🏢 ➔ 🛡️
domain: sendspeed
module: sendspeed_userin
source: linear-export
status: confirmed
---

# ➔ Plataforma UserIn — RBAC, Dashboards e Billing

## Equipe & Permissões — RBAC (SEND-367)

### Contexto

EPIC macro de controle de acesso na plataforma UserIn. Multi-tenancy com três entidades:
`user` / `company` / `visitor`. Cada empresa é um tenant isolado.

### 10 User Stories (backlog)

| # | História | Critério principal |
|---|----------|--------------------|
| 1 | Criar usuário com perfil e papel | Papel (admin/operator/viewer) definido na criação |
| 2 | Convidar membro para empresa | E-mail + papel; link com TTL |
| 3 | Listar membros da empresa | Paginação + busca por nome/e-mail |
| 4 | Editar papel de membro | Audit log de quem alterou |
| 5 | Remover membro | Remoção sem exclusão de dados históricos |
| 6 | Transferir ownership | Novo dono confirma via e-mail |
| 7 | Permissões granulares por módulo | Bitfield por feature (journey, campaign, template…) |
| 8 | API Key por empresa | Geração, rotação e revogação com audit |
| 9 | SSO / OAuth2 | Provider por empresa (Google, Microsoft) |
| 10 | Logs de auditoria de acesso | Quem fez o quê, quando, em qual IP |

### Operadores numéricos para Atributo de Perfil (SEND-414)

Regras de segmentação hoje suportam apenas operadores string/booleano. A feature adiciona:
`>`, `>=`, `<`, `<=`, `between` para campos numéricos do perfil (saldo, pontos, depósitos).

```
Exemplo: saldo_wallet >= 100 AND num_depositos >= 3
```

Status: `backlog` — sem estimativa de prazo no export.

### Bug: Primeiros Passos (SEND-354)

Criar componentes na tela de Primeiros Passos não marca o passo como concluído.
Status: `backlog`.

---

## Dashboards SmartFlow

### SEND-471 — Dashboard Geral SmartFlow

Painel consolidado de métricas de envio/entrega por canal (SMS, RCS, WhatsApp), jornadas ativas e conversões.

> ⚠️ **Inconsistência de export**: SEND-471 consta como `backlog` no export mas foi descrita pela equipe como arquivada/cancelada em ciclos anteriores. Servir com flag `export_inconsistency: true`.

### SEND-475 — feat/smartflow-profile

Issue vazia no export — sem descrição, sem critérios de aceite.

> ⚠️ **Inconsistência de export**: SEND-475 aparece listada mas está vazia. Ação recomendada: refinar com o produto ou fechar como duplicata.

### SEND-476 — Dashboard SmartFlow Upgrade (Fase 2)

Extensão do SEND-471 com drill-down por campanha, comparativo de períodos e exportação de dados.

> ⚠️ **Inconsistência de export**: mesma situação de SEND-471 — backlog no export, possivelmente arquivada.

### SEND-487 — Alerta adicional de saldo na SS Control

Notificação quando o saldo da conta estiver abaixo de threshold configurável. Status: `unstarted` (To-do). Sem inconsistência.

---

## Billing e Relatórios

### SEND-512 — Propagar valor cobrado por mensagem

Incluir na consulta de dados o campo `valor_cobrado` por mensagem enviada, vinculado ao plano do cliente.

### SEND-513 — Total cobrado no relatório

Campo de totalização `total_cobrado` na query de relatórios (GROUP BY + SUM).

### SEND-514 — Filtro de período até 30 dias

Ampliar o filtro atual (máximo 7 dias) para 30 dias corridos.

### Riscos de performance (SLA a definir)

| Risco | Impacto | Ação recomendada |
|-------|---------|-----------------|
| JOIN pesado (mensagens × planos × clientes) sem índice composto | Timeout em > 30 dias | Materializar view diária ou índice composto `(client_id, sent_at, crm)` |
| SUM total_cobrado em 30 dias com volume alto | Lentidão visível | Pré-agregação em job noturno ou cache Redis com TTL 1h |
| SLA de resposta do relatório | Não definido no export | Acordar com produto — sugestão: < 5s para 7 dias, < 30s para 30 dias |

---

## Multi-tenancy — modelo de dados UserIn

```
Company (tenant)
  └─ User (member)  ← papel: admin | operator | viewer
  └─ Visitor        ← rastreado via JS snippet (não autenticado)
  └─ ApiKey         ← por company, com escopos
```

Isolamento garantido por `company_id` em todas as queries — sem crossleak entre tenants.
