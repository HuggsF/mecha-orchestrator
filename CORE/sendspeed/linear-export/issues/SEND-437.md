# SEND-437 — 🚀 — Preview do payload no gatilho Inbound Externo

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | Urgent |
| Responsável | Vinicius Carneiro |
| Time | Sendspeed |
| Projeto | — |
| Labels | Melhoria, User Story, UserIn |
| Parent | — |
| Criada | 2026-03-31T18:10:10.038Z por Vinicius Carneiro |
| Iniciada | 2026-04-01T14:50:01.640Z |
| Concluída | 2026-04-14T15:15:50.189Z |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-437--preview-do-payload-no-gatilho-inbound-externo |
| URL | https://linear.app/sendspeed/issue/SEND-437/preview-do-payload-no-gatilho-inbound-externo |

## Descrição

## 📍 Onde ocorre

**Componente:** Painel lateral do nó **Inbound** (trigger) no Journey Builder

**Seção:** "FORMATO ESPERADO DO PAYLOAD"

---

## ❌ Resultado Atual

O preview do payload exibe campos genéricos fixos que não refletem o contexto real do gatilho Inbound. Os campos `ext_id`, `user_phone` e `txt` são exemplos estáticos que não ajudam o integrador a entender quais variáveis estão disponíveis:

```json
{
  "cid": "69c6c04f780bb9d2c9ae11d9",
  "ext_id": "user_123",
  "user_phone": "5511999999999",
  "txt": "valor qualquer",
  "campo_livre": "vira variável Liquid"
}
```

---

## ✅ Resultado Esperado

O preview deve exibir os campos reais que o sistema utiliza, com notação Liquid (`{{...}}`) nos campos dinâmicos para que o integrador saiba exatamente quais variáveis pode enviar e como referenciá-las nos nós da jornada:

```json
{
  "cid": "69c6c04f780bb9d2c9ae11d9",
  "campaign_id": "{{campaign_id}}",
  "campaign_name": "{{campaign_name}}",
  "campo_livre": "vira variável Liquid"
}
```

**Mudanças:**

| Campo atual | Novo campo | Motivo |
| -- | -- | -- |
| `ext_id: "user_123"` | `campaign_id: "{{campaign_id}}"` | Reflete o campo real usado nas jornadas, com notação Liquid |
| `user_phone: "5511999999999"` | `campaign_name: "{{campaign_name}}"` | Campo mais relevante para o contexto de campanhas externas |
| `txt: "valor qualquer"` | *(removido)* | Campo genérico sem utilidade no exemplo |
| `campo_livre` | `campo_livre` | Mantém para ilustrar que campos extras viram variáveis Liquid |

---

## 🎯 Objetivo

Tornar o preview do payload uma **documentação inline útil** para integradores (Smartico, CRMs, ad servers), mostrando os campos reais que o sistema espera e como eles se transformam em variáveis Liquid dentro da jornada.

---

## Critérios de Aceitação

- [ ] Preview do payload no painel do Inbound mostra `campaign_id` e `campaign_name` com notação `{{...}}`
- [ ] Campo `cid` permanece com valor de exemplo (company ID)
- [ ] Campo `campo_livre` permanece para ilustrar variáveis Liquid customizadas
- [ ] Campos genéricos antigos (`ext_id`, `user_phone`, `txt`) removidos do exemplo
- [ ] Preview é read-only e atualiza automaticamente se o CID da empresa mudar

---

## 🎯 Priorização RICE — Score: 8.0

| Reach | Impact | Confidence | Effort | Score |
| -- | -- | -- | -- | -- |
| 8 | 0.5 (low) | 100% | 0.5 meses | **8.0** |

**Justificativa:** Reach 8: todos os integradores configurando gatilhos Inbound veem esse preview. Impacto low (0.5): melhoria de DX/documentação, não resolve bug funcional. Confidence 100%: alteração estática no componente do painel lateral, sem risco. Esforço 0.5 meses: localizar o componente do painel Inbound e atualizar o JSON de exemplo.

## Histórico de status
- Backlog (backlog): 2026-03-31T18:10:10.038Z → 2026-04-01T12:08:13.029Z
- To-do (unstarted): 2026-04-01T12:08:13.029Z → 2026-04-01T14:50:01.661Z
- In Progress (started): 2026-04-01T14:50:01.661Z → 2026-04-01T15:38:14.333Z
- Product Review (started): 2026-04-01T15:38:14.333Z → 2026-04-14T15:15:50.202Z
- Released (completed): 2026-04-14T15:15:50.202Z → atual

## Relações
—

## Anexos
—
