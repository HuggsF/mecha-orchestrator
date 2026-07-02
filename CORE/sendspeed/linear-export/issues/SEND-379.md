# SEND-379 — 🚀 - Disparo de RCS em massa via módulo de Campanhas

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | Medium |
| Responsável | — |
| Time | Sendspeed |
| Projeto | — |
| Labels | User Story, UserIn, Implementação |
| Parent | — |
| Criada | 2026-03-13T12:33:19.924Z por Vinicius Carneiro |
| Iniciada | — |
| Concluída | 2026-06-22T17:16:49.323Z |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-379--disparo-de-rcs-em-massa-via-modulo-de-campanhas |
| URL | https://linear.app/sendspeed/issue/SEND-379/disparo-de-rcs-em-massa-via-modulo-de-campanhas |

## Descrição

> **Como** operador de marketing de uma plataforma de apostas
> **Quero** criar e disparar uma campanha de RCS para minha base de jogadores
> **Para** enviar mensagens ricas com maior taxa de leitura e conversão que SMS puro, aumentando o engajamento e o retorno dos jogadores

---

# 📈 Use Case: Promoção de evento esportivo via RCS com link rastreável

A operadora LuckBet quer promover o clássico do fim de semana. O gestor de marketing acessa o módulo de Campanhas:

1. Seleciona o canal **RCS**
2. Escolhe a credencial do provedor Pontal/Google RBM já configurada
3. Seleciona a lista "Apostadores Ativos Futebol" (8.500 contatos)
4. Configura a mensagem:

> "Flamengo x Palmeiras HOJE às 16h! Aposte com odds turbinadas: {{url_destino}}"

5. Ativa encurtador de links com UTM tracking e dispara

O sistema processa idêntico ao SMS — batches via Kafka, link encurtado, tracking — mas chama o endpoint /api/rcs/:companyId/send. Jogadores que não suportam RCS recebem fallback como SMS (tratado pela API de integrações). Dashboard mostra: **7.800 entregues via RCS**, 500 via fallback SMS, 200 falhas, **3.100 cliques**.

---

# ✅ Critérios de aceite:

* Usuário consegue criar campanha selecionando canal "RCS"
* Usuário seleciona credencial de RCS configurada (scope: send_rcs)
* Mensagem suporta placeholders dinâmicos e URLs encurtadas (mesmo padrão SMS)
* CampaignWorker envia via /api/rcs/:companyId/send quando channel === rcs
* CampaignService (fallback síncrono) envia via mesmo endpoint RCS
* Processamento em batches via Kafka com rate limiting
* Status de cada destinatário rastreado no CampaignRecipient
* Histórico de mensagens registrado com channel: rcs no MessageHistory
* Dashboard de stats funciona identicamente ao SMS

---

# 🧩 Cenários de teste:

- [ ] Criar campanha RCS com lista de 100 contatos e disparar com sucesso
- [ ] Verificar que o CampaignWorker chama /api/rcs/:companyId/send (não /api/sms/)
- [ ] Verificar que placeholders e URLs encurtadas funcionam igual ao SMS
- [ ] Simular Kafka offline e validar fallback síncrono via CampaignService
- [ ] Confirmar que MessageHistory registra channel: rcs corretamente
- [ ] Verificar que stats do dashboard funcionam para RCS
- [ ] Disparar campanha RCS com credencial inválida e verificar tratamento de erro
- [ ] Validar que destinatários sem telefone são marcados como failed

---

## 🎯 Priorização RICE — Score: 1.67

| Reach | Impact | Confidence | Effort | Score |
| -- | -- | -- | -- | -- |
| 5 | 2 (high) | 50% | 3 meses | **1.67** |

**Justificativa:** Reach 5: adoção de RCS limitada. Impacto high (2): habilita canal de alto engajamento. Confidence 50%: depende de toda a stack RCS. Esforço 3 meses: adaptar CampaignWorker + Kafka + dashboard + fallback.

## Histórico de status
- Backlog (backlog): 2026-03-13T12:33:19.924Z → 2026-03-26T12:19:03.559Z
- Refining (backlog): 2026-03-26T12:19:03.559Z → 2026-03-31T12:33:42.251Z
- To-do (unstarted): 2026-03-31T12:33:42.251Z → 2026-06-22T17:16:49.333Z
- Released (completed): 2026-06-22T17:16:49.333Z → atual

## Relações
—

## Anexos
—
