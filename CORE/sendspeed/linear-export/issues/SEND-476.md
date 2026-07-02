# SEND-476 — Dashboard Geral SmartFlow - Upgrade

| Campo | Valor |
| -- | -- |
| Status | Backlog (backlog) |
| Prioridade | No priority |
| Responsável | — |
| Time | Sendspeed |
| Projeto | — |
| Labels | Implementação |
| Parent | SEND-471 |
| Criada | 2026-05-15T17:28:04.874Z por paulo.ribeiro@sendspeed.com |
| Iniciada | — |
| Concluída | — |
| Arquivada | 2026-06-22T17:18:07.783Z |
| Vencimento | — |
| Branch | hugofernandes/send-476-dashboard-geral-smartflow-upgrade |
| URL | https://linear.app/sendspeed/issue/SEND-476/dashboard-geral-smartflow-upgrade |

## Descrição

**Área:** Campanhas / Performance **Status Frontend:** ✅ Fase 1 implementada — ⏳ Fase 2 pendente **Status Backend:** ⏳ Pendente (dados ainda mockados no frontend) **Ambiente:** Branch `feat/send-471-dashboard-geral-smartflow` **Linear:** [SEND-471](https://linear.app/sendspeed/issue/SEND-471) _(embed de referência à issue SEND-471)_

---

## **Parte 1 — Card Original (Fase 1 — Implementada)**

### **Contexto**

Hoje não existe uma visão consolidada e confiável de performance de envio de SMS por campanha, fornecedor e empresa. O dashboard permite:

* Entender eficiência de entrega
* Detectar gargalos (latência, falhas)
* Comparar fornecedores/rotas
* Dar visibilidade por cliente (empresa)

### **User Story**

**Como** operador/gestor da Send/UserIn **Quero** visualizar um dashboard consolidado de envios e entregas de SMS **Para** analisar performance por campanha, fornecedor e empresa, e tomar decisões baseadas em dados.

---

### **O que foi implementado (Fase 1)**

#### **Filtros Globais**

- [X] Período — AdvancedDateRangePicker com placeholder "Período" e opção de limpar
- [X] Empresa — seleção multi-tenant (Empresa 1, 2, 3)
- [X] Campanha — combobox com busca por nome e filtro por tipo (SMS / RCS), refletindo as campanhas reais de lista fria do backend
- [X] Rota — combobox com 4 rotas: Premium, Spam, OTP e RCS, cada uma com descrição exibida no dropdown
- [X] Aplicar — confirma e recarrega os dados
- [X] Limpar filtros — aparece condicionalmente e reseta todos os campos

> Filtro de fornecedor removido do escopo após refinamento.

#### **Métricas Principais (topo da tela)**

- [X] Taxa de Entrega — percentual em tons verdes com meta-alvo e variação vs período anterior (delta badge)
- [X] Taxa de Falhas — percentual em vermelho com limite aceitável e contagem absoluta de falhas

> Os 7 KPI cards originais (enviados, entregues, falhas, taxas, lead time, callback) estão definidos nos tipos e na API mock, prontos para integração.

#### **Gráficos**

- [X] Qualidade de Rotas — donut chart com distribuição de volume por rota, taxa média ponderada de entrega no centro, taxa individual na legenda
- [X] Monitor de Latência — gráfico de barras dos últimos 7 dias com Lead Time médio (envio → entrega operadora) e Callback Time médio (envio → DLR), linha de referência na média e variação vs início do período

#### **Tabela de Campanhas de Melhor Desempenho**

- [X] Ordenação por Volume ou Taxa de Sucesso
- [X] Colunas: nome/tipo/categoria, volume total, barra de sucesso com percentual colorido por threshold (≥95% verde, ≥85% âmbar, abaixo vermelho)
- [X] Badge de Status ROI: Alto Desempenho / Estável / Necessita Revisão
- [X] Menu de 3 pontos por campanha:
  * Ver detalhes da campanha
  * Ver analytics completos
  * Exportar relatório (.csv)
  * Ver destinatários com falha

---

## **Parte 2 — Evoluções Pendentes (Fase 2)**

Complemento ao card original. Estas mudanças **não alteram** o que foi entregue na Fase 1 — são adicionadas abaixo para planejamento da próxima sprint.

---

### **2.1 Novos Filtros**

#### **F-01 — Filtro por Operadora**

Visão segmentada por operadora para identificar se a performance (boa ou ruim) está concentrada em uma rota específica, facilitando a cobrança aos fornecedores.

#### **F-02 — Filtro de Empresa por Admin**

Administradores selecionam uma empresa específica ou, sem seleção, visualizam os dados consolidados de todas as empresas.

> Diferente do filtro de empresa da Fase 1: aqui a ausência de seleção significa "todas", e o controle só aparece para perfis Admin.

#### **F-03 — Filtro por Período com Quebra Diária**

Seleção de intervalo de dias exibindo o acumulado e a linha detalhada de indicadores para cada dia (ver V-01).

#### **F-04 — Filtro por Status de Campanha**

Separação por status: finalizadas, em andamento, abertas, etc.

#### **F-05 — Filtro por ID/CID de Campanha**

Rastreio pelo CID enviado pelo SmartFlow, com granularidade além do agrupamento diário padrão.

---

### **2.2 Revisão de Métricas**

#### **M-01 — Lead Time Médio**

**Cálculo correto:**

```
Lead Time = entrada no banco → última atualização definitiva (entregue ou falha)
```

**Regra:** ignorar mensagens em status "pending" — não incluir no cálculo para não distorcer a métrica.

#### **M-02 — Tempo Médio de Callback**

**Cálculo correto:**

```
Callback Time = momento do envio inicial ("sent") → primeiro retorno efetivo/final
                (falha ou entrega)
```

**Regra:** excluir transições para status intermediários de pendenciamento.

#### **M-03 — Taxa de Entrega (revisão do denominador)**

```
Taxa de Entrega = Total Entregue ÷ (Total Disparado − Contatos Rejeitados)
```

Mede a capacidade pretendida. Rejeitados saem do denominador pois nunca entraram no fluxo de entrega.

#### **M-04 — Taxa de Sucesso (nova métrica)**

```
Taxa de Sucesso = Total Entregue ÷ Total Absoluto de Disparos
```

Inclui rejeitados no denominador. Mede a saúde real da operação e a qualidade dos fornecedores.

---

### **2.3 Estrutura de Visualização**

#### **V-01 — Layout Acumulado + Detalhamento Diário**

Ao filtrar um intervalo de datas:

* **Parte superior:** média acumulada do período (KPI cards existentes)
* **Parte inferior:** tabela/linha expandida com os indicadores de cada dia do intervalo selecionado

---

## **Checklist Fase 2**

- [ ] F-01 Filtro por operadora
- [ ] F-02 Filtro de empresa Admin (ausência = todas)
- [ ] F-03 Filtro por período com quebra diária
- [ ] F-04 Filtro por status de campanha
- [ ] F-05 Filtro por ID/CID de campanha
- [ ] M-01 Lead Time recalculado (sem "pending")
- [ ] M-02 Callback Time recalculado (sem status intermediários)
- [ ] M-03 Taxa de Entrega com denominador revisado (sem rejeitados)
- [ ] M-04 Taxa de Sucesso criada (com rejeitados no denominador)
- [ ] V-01 Layout acumulado + detalhamento diário por dia

## Histórico de status
- To-do (unstarted): 2026-05-15T17:28:04.874Z → 2026-05-18T13:04:22.866Z
- Backlog (backlog): 2026-05-18T13:04:22.866Z → atual

## Relações
—

## Anexos
—
