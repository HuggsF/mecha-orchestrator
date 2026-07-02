# SEND-377 — 🚀 - Disparo de SMS em massa via módulo de Campanhas

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | Medium |
| Responsável | — |
| Time | Sendspeed |
| Projeto | — |
| Labels | User Story, UserIn, Implementação |
| Parent | — |
| Criada | 2026-03-13T12:32:50.593Z por Vinicius Carneiro |
| Iniciada | — |
| Concluída | 2026-06-22T17:16:44.528Z |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-377--disparo-de-sms-em-massa-via-modulo-de-campanhas |
| URL | https://linear.app/sendspeed/issue/SEND-377/disparo-de-sms-em-massa-via-modulo-de-campanhas |

## Descrição

> **Como** operador de marketing de uma casa de apostas
> **Quero** criar e disparar uma campanha de SMS para uma lista de contatos
> **Para** reativar jogadores inativos com uma mensagem personalizada e um link rastreável de volta ao site, aumentando a taxa de redeposit

---

# 📈 Use Case: Reativação de jogadores inativos via SMS em massa

A operadora BetMax identificou 12.000 jogadores que não fazem login há 15 dias. O gestor de CRM acessa o módulo de Campanhas, cria uma nova campanha selecionando o canal **SMS**, escolhe a lista "Inativos 15d" como audiência e configura a mensagem:

> "Oi {{nome}}, sentimos sua falta! Volte e ganhe 10 free spins: {{url_destino}}"

Seleciona a credencial SMS (ex: Twilio) já configurada nas integrações, ativa o encurtador de links com UTM tracking e dispara. O sistema processa em batches via Kafka, exibindo progresso em tempo real no dashboard. Ao final: **11.400 enviados**, 580 com telefone inválido, 20 falhas, e **2.300 cliques** no link rastreado.

---

# ✅ Critérios de aceite:

* Usuário consegue criar campanha selecionando canal "SMS"
* Usuário seleciona uma lista estática ou segmento como audiência
* Usuário seleciona credencial de SMS configurada na plataforma de integrações
* Mensagem suporta placeholders dinâmicos ({{nome}}, {{url_destino}})
* URLs são encurtadas automaticamente com tracking (utm_campaign, utm_ui)
* Campanha é processada via Kafka em batches (fallback síncrono se Kafka offline)
* Status de cada destinatário é rastreado (pending → sent → delivered → failed)
* Histórico de mensagens registrado no MessageHistory
* Dashboard exibe stats em tempo real: total, enviados, falhas, cliques

---

# 🧩 Cenários de teste:

- [ ] Criar campanha SMS com lista estática de 100 contatos e disparar com sucesso
- [ ] Verificar que placeholders {{nome}} e {{url_destino}} são substituídos corretamente
- [ ] Verificar que URLs são encurtadas e contém parâmetros utm_campaign
- [ ] Simular Kafka offline e validar que o fallback síncrono processa a campanha
- [ ] Verificar que destinatários sem telefone são marcados como failed
- [ ] Confirmar que o MessageHistory registra cada mensagem enviada com status correto
- [ ] Validar que o dashboard atualiza stats (sent, failed, clicked) durante e após o envio
- [ ] Disparar campanha com credencial inválida e verificar tratamento de erro

---

## 🎯 Priorização RICE — Score: 1.67 (#5 no To-do)

| Reach | Impact | Confidence | Effort | Score |
| -- | -- | -- | -- | -- |
| 5 | 2 (high) | 50% | 3 meses | **1.67** |

**Justificativa:** Feature de alto valor mas com score RICE baixo pelo esforço elevado. Reach 5 porque atinge equipes de marketing das operadoras (não todos os usuários). Impacto high (2): habilita um canal novo de comunicação em massa que hoje não existe. Confidence apenas 50% porque é uma feature grande com múltiplas dependências (Kafka batching, encurtador de links, dashboard real-time, MessageHistory) e escopo pode crescer. Esforço de 3 meses considerando frontend + backend + infra Kafka + testes de carga. Recomenda-se quebrar em sub-tasks menores para aumentar confidence e reduzir risco.

## Histórico de status
- Backlog (backlog): 2026-03-13T12:32:50.593Z → 2026-03-13T14:59:54.043Z
- To-do (unstarted): 2026-03-13T14:59:54.043Z → 2026-06-22T17:16:44.538Z
- Released (completed): 2026-06-22T17:16:44.538Z → atual

## Relações
—

## Anexos
—
