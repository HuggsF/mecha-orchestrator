# SEND-425 — 📱 Implementar validação de regras de envio de SMS

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | Urgent |
| Responsável | — |
| Time | Sendspeed |
| Projeto | — |
| Labels | — |
| Parent | — |
| Criada | 2026-03-24T18:24:53.472Z por Vinicius Carneiro |
| Iniciada | — |
| Concluída | 2026-06-22T17:16:15.699Z |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-425-implementar-validacao-de-regras-de-envio-de-sms |
| URL | https://linear.app/sendspeed/issue/SEND-425/implementar-validacao-de-regras-de-envio-de-sms |

## Descrição

## 📋 Descrição

Implementar validações no sistema de disparos para garantir que todas as mensagens SMS sigam os padrões estabelecidos.

## 🎯 Objetivo

Garantir que mensagens SMS inválidas sejam tratadas antes do envio, evitando falhas e custos desnecessários.

---

## ✅ Critérios de Aceite

### Validação de Telefone

- [ ] Aceitar somente dígitos (remover espaços, traços, parênteses)
- [ ] Brasil: aceitar 11 a 13 dígitos
- [ ] Colômbia: aceitar 10 a 12 dígitos
- [ ] Adicionar DDI automaticamente (55 para Brasil, 57 para Colômbia) quando não informado
- [ ] Remover zeros iniciais automaticamente
- [ ] Rejeitar números com letras ou símbolos
- [ ] Rejeitar números fora do range de dígitos permitido

### Validação de Texto

- [ ] Tamanho mínimo: 3 caracteres
- [ ] Tamanho máximo: 160 caracteres (rejeitar mensagens maiores)
- [ ] Remover emojis automaticamente (charset GSM-7)
- [ ] Substituir caracteres especiais:
  - `{` e `[` → `(`
  - `}` e `]` → `)`
  - `|` → `-`
  - Remover: `€`, `^`, `~`
- [ ] Converter quebras de linha em espaço
- [ ] Remover acentos não suportados pelo GSM-7 (`ã`, `õ`, `â`, `ê`, `î`, `ô`, `û`)

### Charset GSM-7 Permitido

* Letras: A-Z, a-z
* Números: 0-9
* Pontuação: `. , ; : ! ? ' " ( ) - + * / # % & @ $ _`
* Acentos GSM-7: `Ä Ö Ñ Ü ä ö ñ ü à è é ù ì ò ç Ç Ø ø Å å Æ æ ß É`
* Moedas: `£ ¥`

---

## 📍 Onde aplicar

- [ ] Endpoint de disparo de SMS
- [ ] Validação no frontend (preview/editor de campanha)
- [ ] Mostrar contador de caracteres restantes (máx 160)
- [ ] Alertar usuário sobre caracteres removidos/substituídos

## 📎 Referência

Documento: `# Regras de Envio de SMS.md`

---

## 🎯 Priorização RICE — Score: 16.0

| Reach | Impact | Confidence | Effort | Score |
| -- | -- | -- | -- | -- |
| 10 | 2 (high) | 80% | 1 mês | **16.0** |

**Justificativa:** Reach 10: todas as empresas enviam SMS. Impacto high (2): mensagens inválidas geram custos e falhas silenciosas. Confidence 80%: regras GSM-7 bem documentadas. Esforço 1 mês: backend + frontend + contadores + testes.

## Histórico de status
- Backlog (backlog): 2026-03-24T18:24:53.472Z → 2026-03-24T18:26:09.055Z
- To-do (unstarted): 2026-03-24T18:26:09.055Z → 2026-03-24T18:29:30.679Z
- Backlog (backlog): 2026-03-24T18:29:30.679Z → 2026-03-25T13:29:20.296Z
- Refining (backlog): 2026-03-25T13:29:20.296Z → 2026-03-31T12:33:52.603Z
- To-do (unstarted): 2026-03-31T12:33:52.603Z → 2026-06-22T17:16:15.710Z
- Released (completed): 2026-06-22T17:16:15.710Z → atual

## Relações
- related: SEND-428 — Especificações RCS — Validações, Alertas e Orientações por Formato

## Anexos
—
