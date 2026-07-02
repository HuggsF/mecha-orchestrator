# SEND-470 — 🧩Monitoramento de Entrega via "Fazendinha"

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | No priority |
| Responsável | thiago.melin@sendspeed.com |
| Time | Sendspeed |
| Projeto | — |
| Labels | — |
| Parent | — |
| Criada | 2026-05-05T12:04:35.514Z por pedro.antunes@sendspeed.com |
| Iniciada | — |
| Concluída | 2026-06-22T17:18:29.665Z |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-470-monitoramento-de-entrega-via-fazendinha |
| URL | https://linear.app/sendspeed/issue/SEND-470/monitoramento-de-entrega-via-fazendinha |

## Descrição

### 🎯 Contexto

Hoje não temos uma forma confiável e padronizada de medir:

* Taxa real de entrega de SMS
* Falsos positivos (FAKEDLR)
* Performance por fornecedor/rota

A "fazendinha" será um conjunto de números controlados que recebem disparos continuamente para gerar métricas confiáveis.

---

## 👤 User Story

**Como** time de operações/engenharia da Send/UserIn
**Quero** disparar automaticamente SMS para uma base controlada de números (fazendinha), distribuindo entre diferentes fornecedores e rotas
**Para** medir com precisão taxa de entrega, latência e inconsistências (FAKEDLR), permitindo tomada de decisão baseada em dados

---

## ✅ Critérios de Aceite

### 1\. Disparo Controlado

* Deve ser possível configurar:
  * Quantidade de disparos por dia (ex: X por fornecedor)
  * Intervalo entre disparos
  * Distribuição entre fornecedores
* Cada disparo deve registrar:
  * Timestamp
  * Número destino
  * Fornecedor
  * Rota (se aplicável)
  * Mensagem ID (interno e externo)

---

### 2\. Base "Fazendinha"

* Lista de números controlados (100–1000+)
* Cada número deve ter metadata:
  * Operadora (se possível inferir)
  * Localização (DDD/região)
  * Tipo (Android, iOS, modem, etc — opcional)
* Capacidade de expandir/reduzir facilmente

---

### 3\. Coleta de Status (DLR)

* Capturar:
  * Status enviado pelo fornecedor (DELIVERED, FAILED, etc)
  * Timestamp do DLR
* Armazenar:
  * Tempo entre envio e DLR (latência)

---

### 4\. Detecção de FAKEDLR

O sistema deve identificar possíveis falsos positivos com base em:

* Número não recebeu SMS (via validação manual ou automação futura)
* DLR marcado como "DELIVERED"
* Regras iniciais:
  * Entregue em tempo irreal (< X segundos)
  * Padrões inconsistentes por fornecedor
  * Divergência entre operadores/números

---

### 5\. Dashboard

#### 📊 Visão Geral

* Taxa de entrega por fornecedor (%)
* Volume de disparos
* Taxa de erro
* Taxa de FAKEDLR estimada

#### 🔎 Drill Down

* Por fornecedor
* Por rota
* Por operadora
* Por faixa de horário

#### 📈 Métricas principais

* Delivery Rate
* Failure Rate
* FAKEDLR Rate
* Latência média (envio → entrega)

---

### 6\. Logs e Auditoria

* Cada disparo deve ser rastreável
* Possibilidade de buscar por:
  * Número
  * Message ID
  * Fornecedor

## Histórico de status
- To-do (unstarted): 2026-05-05T12:04:35.514Z → 2026-05-18T13:04:15.130Z
- Backlog (backlog): 2026-05-18T13:04:15.130Z → 2026-06-22T17:18:29.670Z
- Released (completed): 2026-06-22T17:18:29.670Z → atual

## Relações
—

## Anexos
—
