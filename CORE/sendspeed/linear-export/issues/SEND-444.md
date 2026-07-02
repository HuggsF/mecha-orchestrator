# SEND-444 — Feature: Atribuir conversões às jornadas que impactaram o usuário

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | Urgent |
| Responsável | Vinicius Carneiro |
| Time | Sendspeed |
| Projeto | — |
| Labels | User Story, Analytics, UserIn, Melhoria |
| Parent | — |
| Criada | 2026-04-01T12:59:31.816Z por Vinicius Carneiro |
| Iniciada | 2026-04-06T17:23:18.048Z |
| Concluída | 2026-04-24T13:41:32.796Z |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-444-feature-atribuir-conversoes-as-jornadas-que-impactaram-o |
| URL | https://linear.app/sendspeed/issue/SEND-444/feature-atribuir-conversoes-as-jornadas-que-impactaram-o-usuario |

## Descrição

## O problema hoje

Hoje, quando uma pessoa recebe um SMS ou RCS de uma jornada e depois vai lá e se registra ou faz um depósito, **a gente não sabe que foi aquela jornada que causou a conversão.** A conversão chega, mas não volta pra jornada que disparou a mensagem.

Ou seja: o gestor cria uma jornada, dispara milhares de mensagens, e na tela de analytics vê "Conversões: 0" — porque não existe nenhum processo que cruze as conversões com os envios.

---

## O que precisa acontecer

### O fluxo natural do usuário

1. **A jornada dispara uma mensagem** (SMS, RCS, Email) para o usuário
2. **O usuário recebe e (talvez) clica**
3. **Minutos depois, ele vai ao site** e faz alguma coisa: visita, se registra, faz o primeiro depósito (FTD)
4. **O webhook chega** informando que o cara registrou, depositou, etc.

Hoje o processo para no passo 4 — o webhook chega, a gente grava, mas **não olha pra trás** pra ver se esse cara recebeu alguma mensagem de alguma jornada.

### O que a nova fila precisa fazer

Toda vez que uma pessoa é processada (chega um evento de registro, FTD, depósito, visita), a fila precisa:

1. **Olhar todas as jornadas com janela de atribuição aberta** — ou seja, jornadas que dispararam mensagens recentemente e ainda estão "esperando" pra saber se o envio gerou resultado
2. **Verificar se essa pessoa estava no envio de qualquer uma dessas jornadas** — se ela recebeu SMS, RCS ou email de alguma delas
3. **Se estava, registrar o que ela fez:**
   * Visitou o site?
   * Se registrou?
   * Fez o primeiro depósito (FTD)?
   * Qual o score dela?
   * Qual o MTD?

Assim, cada jornada passa a saber: "dos 16.000 que eu enviei, 4.200 visitaram, 890 se registraram, 210 fizeram FTD".

---

## Janela de atribuição

A janela de atribuição é o tempo que a gente espera pra saber se o envio deu resultado.

* **Padrão: 24 horas** — se a pessoa recebeu a mensagem e converteu dentro de 24h, conta pra jornada
* **Configurável pelo usuário:** na configuração da jornada, o gestor pode mudar (6h, 12h, 24h, 48h, 72h, 7 dias)
* **Depois que a janela fecha:** conversões que acontecem depois não são creditadas àquela jornada

**Exemplo prático:**

* Jornada "Promo Flu x Corinthians" dispara 24.000 RCS às 14h de terça
* Janela de atribuição: 24h (expira quarta às 14h)
* João recebeu o RCS terça às 14h, se registrou terça às 22h → **conta pra jornada** (dentro da janela)
* Maria recebeu o RCS terça às 14h, se registrou quinta às 10h → **não conta** (fora da janela)

---

## Como funciona passo a passo

```
1. Jornada dispara SMS/RCS/Email para 24.000 pessoas
         ↓
2. Pra cada envio, abre uma "janela de atribuição" (24h por padrão)
   → Fica registrado: "essa pessoa recebeu mensagem desta jornada, 
      janela aberta até amanhã às 14h"
         ↓
3. Horas depois, começa a chegar atividade dessas pessoas:
   → João visitou o site
   → João se registrou
   → João fez FTD de R$50
         ↓
4. Pra CADA atividade que chega, a fila pergunta:
   "Esse cara tá dentro de alguma jornada com janela aberta?"
         ↓
5a. SIM → Registra a conversão na jornada:
    → Jornada "Promo Flu x Corinthians" +1 registro, +1 FTD
    → Score e MTD do usuário são associados
         ↓
5b. NÃO → Ignora (ou a janela já fechou, ou nunca recebeu mensagem)
         ↓
6. Quando a janela de 24h expira:
   → Fecha todas as janelas abertas daquela jornada
   → Consolida: "16.895 enviados, 4.200 visitaram, 890 registros, 210 FTDs"
   → Essas métricas aparecem no analytics da jornada
```

---

## O que o gestor vai ver no analytics

Depois dessa feature, a tela de analytics da jornada vai mostrar dados reais de conversão:

| Métrica | Antes | Depois |
| -- | -- | -- |
| Enviados | 16.895 | 16.895 |
| Entregues | 15.735 | 15.735 |
| Visitaram o site | 0 (não existia) | 4.200 |
| Registros | 0 (não conectava) | 890 |
| FTD | 0 (não conectava) | 210 |
| Taxa de conversão | 0% | 5.26% (890/16.895) |
| Receita atribuída | R$ 0 | R$ 12.400 |

---

## Configuração na jornada (o que o usuário configura)

Na tela de configuração da jornada, adicionar:

**Janela de atribuição:**

* Presets: 6h, 12h, 24h (padrão), 48h, 72h, 7 dias
* Helper: "Conversões que ocorrerem após esse tempo não serão creditadas a esta jornada"

**Modelo de atribuição:**

* Last Touch (padrão): a última jornada que enviou mensagem leva o crédito
* First Touch: a primeira jornada que enviou leva o crédito
* Linear: divide o crédito entre todas as jornadas que enviaram

---

## Critérios de aceite

- [ ] Toda vez que chega um evento (registro, FTD, depósito, visita), o sistema verifica todas as jornadas com janela de atribuição aberta
- [ ] Se a pessoa estava no envio de alguma dessas jornadas, a conversão é atribuída à jornada
- [ ] A janela de atribuição padrão é 24 horas
- [ ] O gestor pode configurar a janela (6h a 7 dias) na configuração da jornada
- [ ] Quando a janela expira, as métricas são consolidadas
- [ ] O analytics da jornada mostra: visitas, registros, FTDs e receita atribuída
- [ ] Jornadas que não tiveram conversão dentro da janela mostram "0 conversões" corretamente
- [ ] Múltiplas jornadas podem ter janelas abertas ao mesmo tempo — cada uma recebe suas conversões

---

## Cenários de teste

- [ ] Disparar jornada com janela de 1h, simular registro em 30min → conversão atribuída à jornada
- [ ] Disparar jornada com janela de 1h, simular registro em 2h → conversão NÃO atribuída
- [ ] Disparar 2 jornadas diferentes para o mesmo usuário, simular FTD → conversão atribuída à última (last touch)
- [ ] Alterar janela para 48h na configuração → novos envios usam 48h
- [ ] Verificar analytics: jornada com 10.000 enviados, 500 registros, 50 FTDs → métricas corretas
- [ ] Janela expira → métricas consolidadas, não mudam mais

---

## Priorização RICE — Score: 19.2

| Reach | Impact | Confidence | Effort | Score |
| -- | -- | -- | -- | -- |
| 8 | 3 (massive) | 80% | 1 mês | **19.2** |

**Justificativa:** Sem essa feature, todas as jornadas mostram "0 conversões" no analytics. O gestor não tem como saber se os disparos de SMS/RCS estão gerando resultado. Com isso, ele pode comparar jornadas, otimizar mensagens e provar ROI. Afeta todas as empresas que usam jornadas offsite.

## Histórico de status
- Backlog (backlog): 2026-04-01T12:59:31.816Z → 2026-04-06T17:23:18.063Z
- In Progress (started): 2026-04-06T17:23:18.063Z → 2026-04-09T12:12:27.553Z
- Product Review (started): 2026-04-09T12:12:27.553Z → 2026-04-24T13:41:32.809Z
- Released (completed): 2026-04-24T13:41:32.809Z → atual

## Relações
—

## Anexos
—
