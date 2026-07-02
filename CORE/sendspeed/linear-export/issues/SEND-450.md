# SEND-450 — Objetivos funcionais — definir metas que validam o desempenho de uma jornada

| Campo | Valor |
| -- | -- |
| Status | Backlog (backlog) |
| Prioridade | Urgent |
| Responsável | — |
| Time | Sendspeed |
| Projeto | — |
| Labels | UserIn, Melhoria, Jornadas, User Story |
| Parent | — |
| Criada | 2026-04-14T11:41:42.119Z por Vinicius Carneiro |
| Iniciada | — |
| Concluída | — |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-450-objetivos-funcionais-definir-metas-que-validam-o-desempenho |
| URL | https://linear.app/sendspeed/issue/SEND-450/objetivos-funcionais-definir-metas-que-validam-o-desempenho-de-uma |

## Descrição

## História

Como gestor, quero definir um objetivo para cada jornada — com as metas que preciso bater — para que, ao final da jornada, o sistema me diga automaticamente se ela foi bem-sucedida ou não com base nas conversões reais atribuídas àquela jornada.

---

## O problema hoje

A plataforma tem uma seção de **Objetivos** e outra de **Métricas de Sucesso**, mas as duas existem de forma isolada: dá pra criar, mas não há conexão real com as jornadas nem com as conversões que chegam. O resultado é que:

* Crio uma jornada, seleciono um objetivo — mas os KPIs ficam zerados independentemente do que acontece
* Não consigo saber se a jornada "Promo Flu x Corinthians" bateu a meta de FTD que eu defini
* Não há resposta pra pergunta mais básica: **essa jornada funcionou?**

---

## Como deve funcionar

### 1\. Criar objetivos com metas claras

Na seção de **Objetivos**, o gestor define:

* **Nome do objetivo** — ex: "Ativação de novos usuários"
* **Estágio do usuário** — visitante, cadastrado, primeiro depósito, ativo, VIP, inativo
* **Quais métricas precisa bater** — ex: taxa de FTD, número de registros, receita atribuída
* **Metas por métrica** — ex: taxa de FTD acima de 5%, pelo menos 200 registros

### 2\. Vincular o objetivo à jornada

Ao criar ou editar uma jornada, o gestor escolhe **qual objetivo essa jornada persegue**. Isso define:

* Quais métricas serão acompanhadas
* Qual a meta a ser batida
* Qual é a janela de atribuição (tempo que o sistema vai esperar por conversões)

### 3\. As conversões alimentam o objetivo automaticamente

Quando a jornada dispara mensagens e as pessoas convertem (registro, FTD, depósito), o sistema:

1. Identifica que aquela pessoa estava dentro da janela de atribuição da jornada
2. Atribui a conversão à jornada
3. Atualiza os contadores do objetivo vinculado
4. Recalcula os KPIs automaticamente

### 4\. O gestor vê o resultado

No analytics da jornada, uma seção de **Desempenho do Objetivo** mostra:

| Métrica | Meta | Realizado | Status |
| -- | -- | -- | -- |
| Taxa de FTD | 5% | 3.2% | Abaixo da meta |
| Registros | 200 | 347 | Acima da meta |
| Receita atribuída | R$ 10.000 | R$ 14.200 | Acima da meta |

---

## Exemplo prático

1. Gestor cria o objetivo **"Conversão FTD"** com meta: taxa de FTD acima de 5% e pelo menos 100 primeiros depósitos
2. Cria a jornada **"Promo Flu x Corinthians"** e vincula ao objetivo **"Conversão FTD"**, com janela de atribuição de 24h
3. Jornada dispara 16.895 RCS
4. Nas próximas 24h, 210 pessoas fazem FTD — o sistema identifica que essas pessoas receberam o RCS e atribui as conversões à jornada
5. O analytics da jornada mostra: **FTD = 210 (1.24% — abaixo da meta de 5%)** e **Receita = R$ 12.400 — acima da meta**
6. O gestor entende que o volume não foi suficiente para bater a taxa, mas a receita compensou

---

## O que o gestor configura

**Na tela de Objetivos:**

* Nome e descrição do objetivo
* Estágio do público-alvo
* Métricas de sucesso e metas (ex: FTD ≥ 5%, registros ≥ 200, receita ≥ R$ 10.000)

**Na configuração da jornada:**

* Qual objetivo essa jornada persegue
* Janela de atribuição (padrão 24h)
* Modelo de atribuição (last touch por padrão)
* Metas podem ser sobrescritas por jornada (ex: essa jornada específica tem meta de FTD mais agressiva)

**No analytics da jornada:**

* Painel de desempenho do objetivo com métricas, metas e status (acima / abaixo / crítico)

---

## Critérios de aceite

- [ ] Gestor consegue criar um objetivo com nome, estágio e métricas de sucesso com metas
- [ ] Jornada pode ser vinculada a um objetivo
- [ ] Quando uma conversão é atribuída à jornada, os contadores do objetivo são atualizados automaticamente
- [ ] Os KPIs do objetivo são recalculados após cada conversão atribuída
- [ ] O analytics da jornada mostra o painel de desempenho do objetivo com meta x realizado
- [ ] Status de cada métrica é exibido: acima da meta, abaixo da meta, crítico
- [ ] Jornadas sem objetivo vinculado não mostram o painel (ou mostram mensagem orientando a vincular)
- [ ] Metas do objetivo podem ser sobrescritas individualmente por jornada

---

## Cenários

- [ ] Crio objetivo com meta de 5% FTD → vinculo jornada → 100 conversoes FTD chegam → KPI atualiza para valor real e compara com meta
- [ ] Jornada sem objetivo vinculado → painel de objetivo não aparece no analytics
- [ ] Dois objetivos distintos com mesma métrica (ex: FTD) mas metas diferentes → cada jornada calcula contra sua própria meta
- [ ] Janela de atribuição expira → contadores são consolidados e KPIs não mudam mais
- [ ] Gestor sobrescreve meta de FTD da jornada de 5% para 10% → analytics usa a meta da jornada, não do objetivo
- [ ] Status de métrica: valor acima da meta → verde, abaixo → amarelo, abaixo do crítico → vermelho

---

## Priorização RICE — Score: 24.0

| Reach | Impact | Confidence | Effort | Score |
| -- | -- | -- | -- | -- |
| 10 | 3 (massive) | 80% | 1 mês | **24.0** |

**Justificativa:** Toda empresa que usa jornadas precisa saber se elas funcionaram. Sem objetivos funcionais e ligados às atribuições, o analytics da jornada é apenas um dashboard de envio — não de resultado de negócio. Essa é a feature que transforma a plataforma de "ferramenta de disparo" para "ferramenta de crescimento". A estrutura técnica (objetivos, métricas, atribuição, touchpoints) já existe — falta conectar as peças e expor o resultado para o gestor.

## Histórico de status
- Backlog (backlog): 2026-04-14T11:41:42.119Z → atual

## Relações
—

## Anexos
—
