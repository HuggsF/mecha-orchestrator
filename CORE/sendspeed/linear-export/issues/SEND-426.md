# SEND-426 — 📨 Implementar validação de regras de envio de RCS

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | High |
| Responsável | — |
| Time | Sendspeed |
| Projeto | — |
| Labels | — |
| Parent | — |
| Criada | 2026-03-24T18:25:13.030Z por Vinicius Carneiro |
| Iniciada | — |
| Concluída | 2026-06-22T17:16:29.858Z |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-426-implementar-validacao-de-regras-de-envio-de-rcs |
| URL | https://linear.app/sendspeed/issue/SEND-426/implementar-validacao-de-regras-de-envio-de-rcs |

## Descrição

## 📋 Descrição

Implementar validações no sistema de disparos para garantir que todas as mensagens RCS sigam os padrões estabelecidos.

## 🎯 Objetivo

Garantir que campanhas RCS (TEXT e CAROUSEL) estejam em conformidade antes do envio.

---

## ✅ Critérios de Aceite

### Validação de Telefone

- [ ] Aceitar somente dígitos (remover espaços, traços, parênteses)
- [ ] Brasil: aceitar 11 a 13 dígitos
- [ ] Colômbia: aceitar 10 a 12 dígitos
- [ ] Adicionar DDI automaticamente (55 para Brasil, 57 para Colômbia)
- [ ] Descartar números inválidos (poucos dígitos ou com letras/símbolos)

---

### Campanha TEXT

- [ ] Tamanho máximo da mensagem: **3.072 caracteres**
- [ ] Emojis: **permitidos**
- [ ] Quebras de linha: **permitidas**

#### Ações Sugeridas (opcionais)

- [ ] Máximo de **11 ações**
- [ ] Texto de cada ação: máximo **25 caracteres**
- [ ] Tipos de ação:
  * **Responder**: texto do botão
  * **Abrir URL**: texto + URL (http:// ou https://)
  * **Discar telefone**: texto + número
  * **Mostrar localização**: texto + latitude/longitude

---

### Campanha CAROUSEL

#### Cartões

- [ ] Mínimo: **1 cartão**
- [ ] Máximo: **10 cartões**
- [ ] Largura: **Pequeno** ou **Médio** (aplica a todos)

#### Mídia de cada cartão (opcional)

- [ ] Tipo: Imagem ou Vídeo
- [ ] Altura: Curto, Médio ou Alto
- [ ] URL deve começar com `http://` ou `https://`

#### Textos de cada cartão (opcionais)

- [ ] Título: máximo **200 caracteres** (emojis permitidos)
- [ ] Descrição: máximo **2.000 caracteres** (emojis permitidos)

#### Botões de cada cartão (opcionais)

- [ ] Máximo: **4 botões** por cartão
- [ ] Texto de cada botão: máximo **25 caracteres**
- [ ] Tipos: Abrir URL, Responder, Discar telefone, Mostrar localização

---

## 📍 Onde aplicar

- [ ] Endpoint de disparo de RCS
- [ ] Validação no frontend (editor de campanha RCS)
- [ ] Mostrar contadores de caracteres
- [ ] Validar URLs (http/https)
- [ ] Preview de como ficará no dispositivo

## 📎 Referência

Documento: `# Regras de Envio de RCS.md`

---

## 🎯 Priorização RICE — Score: 8.53

| Reach | Impact | Confidence | Effort | Score |
| -- | -- | -- | -- | -- |
| 8 | 2 (high) | 80% | 1.5 meses | **8.53** |

**Justificativa:** Reach 8: todas as empresas usando RCS. Impacto high (2): sem validação, mensagens inválidas geram falhas e custos. Confidence 80%: specs Google RCS bem documentadas. Esforço 1.5 meses: múltiplos formatos, frontend + backend + contadores.

## Histórico de status
- Backlog (backlog): 2026-03-24T18:25:13.030Z → 2026-03-24T18:26:05.889Z
- To-do (unstarted): 2026-03-24T18:26:05.889Z → 2026-03-24T18:29:28.138Z
- Backlog (backlog): 2026-03-24T18:29:28.138Z → 2026-03-25T13:29:21.336Z
- Refining (backlog): 2026-03-25T13:29:21.336Z → 2026-03-31T12:33:53.591Z
- To-do (unstarted): 2026-03-31T12:33:53.591Z → 2026-06-22T17:16:29.868Z
- Released (completed): 2026-06-22T17:16:29.868Z → atual

## Relações
- related: SEND-428 — Especificações RCS — Validações, Alertas e Orientações por Formato

## Anexos
—
