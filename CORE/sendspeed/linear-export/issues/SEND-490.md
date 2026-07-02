# SEND-490 — [sms-api] Adicionar campo `crm` ao crm_postback nos DTOs e builders

| Campo | Valor |
| -- | -- |
| Status | To-do (unstarted) |
| Prioridade | High |
| Responsável | andrei.garcia@externo.sendspeed.com |
| Time | Sendspeed |
| Projeto | — |
| Labels | — |
| Parent | SEND-488 |
| Criada | 2026-06-15T17:59:10.675Z por andrei.garcia@externo.sendspeed.com |
| Iniciada | — |
| Concluída | — |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-490-sms-api-adicionar-campo-crm-ao-crm_postback-nos-dtos-e |
| URL | https://linear.app/sendspeed/issue/SEND-490/sms-api-adicionar-campo-crm-ao-crm-postback-nos-dtos-e-builders |

## Descrição

## Objetivo

Adicionar o campo `crm` ao JSON `crm_postback` em todos os pontos de montagem do serviço, e criar uma **camada de normalização de input** que converta os campos recebidos de cada CRM para o padrão interno da plataforma antes de salvar na coluna `sms.crm_postback`.

## Contexto

A Smartico envia seus campos com nomes específicos. A Fasttrack pode enviar os mesmos dados com nomes diferentes. O sistema deve absorver essas diferenças na borda (DTO/builder) e salvar sempre no mesmo formato interno.

---

## Padrão interno (o que salvar no banco — imutável)

```json
{
  "crm": "smartico" | "fasttrack",
  "callback_url": "https://...",
  "crm_message_id": "abc-123",
  "api_key": "optional"
}
```

---

## Campos que a Smartico envia hoje (formato de entrada)

| Campo recebido | Campo interno | Observação |
| -- | -- | -- |
| `callback_url` | `callback_url` | direto |
| `crm_callback_url` | `callback_url` | alias legado — já tratado |
| `crm_message_id` | `crm_message_id` | direto |
| `api_key` | `api_key` | direto |
| *(ausente)* | `crm` | default `"smartico"` |

---

## Campos que a Fasttrack precisará enviar (formato de entrada — a definir com eles)

⚠️ **Não temos documentação da Fasttrack ainda.** A lista abaixo representa o que precisamos solicitar a eles para fechar a integração. Os nomes dos campos são *propostas* — devem ser confirmados quando recebermos a doc.

| Campo a solicitar | Mapeamento interno | Obrigatório | Descrição |
| -- | -- | -- | -- |
| `crm` | `crm` | **Sim** | Deve vir com valor fixo `"fasttrack"` para identificar o CRM |
| `callback_url` *(ou nome equivalente deles)* | `callback_url` | **Sim** | URL onde faremos o POST de status de entrega |
| `message_id` / `crm_message_id` *(ou nome deles)* | `crm_message_id` | Não | ID da mensagem no CRM para correlação |
| `api_key` / `token` *(ou nome deles)* | `api_key` | Não | Chave de autenticação — será appendada como `?api_key=` na URL |

**Ação necessária:** solicitar à equipe Fasttrack a documentação dos campos que eles enviam na requisição de disparo. Com isso, esta task define o mapeamento e implementa o normalizador.

---

## Normalização — o que implementar

Criar um normalizador por CRM dentro do `buildCrmPostback()`:

```ts
// Pseudo-código
function normalizeCrmPostback(raw, crm): InternalCrmPostback {
  if (crm === 'fasttrack') {
    return {
      crm: 'fasttrack',
      callback_url: raw.callback_url ?? raw.url ?? raw.webhook_url ?? null,  // ajustar com doc deles
      crm_message_id: raw.crm_message_id ?? raw.message_id ?? raw.id ?? null,
      api_key: raw.api_key ?? raw.token ?? null,
    };
  }
  // Smartico (padrão atual)
  return {
    crm: 'smartico',
    callback_url: raw.callback_url ?? raw.crm_callback_url ?? null,
    crm_message_id: raw.crm_message_id ?? null,
    api_key: raw.api_key ?? null,
  };
}
```

Os aliases da Fasttrack (`url`, `webhook_url`, `token`, etc.) serão preenchidos **após recebermos a documentação**.

---

## Arquivos a alterar

### DTOs de entrada da API

* `src/sms/dto/send-sms.dto.ts` — adicionar `crm?: 'smartico' | 'fasttrack'` dentro de `crm_postback`
* `src/rcs/dto/send-rcs.dto.ts` — idem
* `src/sms/sms-simple-validation.service.ts` — adicionar campo `crm` ao schema Zod
* `src/rcs/rcs-validation.service.ts` — idem

### Builders

* `src/sms/services/sms-dispatch.service.ts` — `buildCrmPostback()`: chamar normalizador, incluir `crm`
* `src/sms/sms.service.ts` — mesmo ajuste
* `src/otp/services/otp-dispatch.service.ts` — `buildCrmPostback()`: incluir `crm`

### Consumer RCS ETL

* `src/consumer/rcs-etl.service.ts` — normalização linhas 245–258: preservar campo `crm`

## Regra de retrocompatibilidade

* `crm_postback` sem campo `crm` → assume `"smartico"` em todo o pipeline
* Todos os registros existentes no banco sem `crm` → consumers leem como Smartico por fallback

## Histórico de status
- Backlog (backlog): 2026-06-15T17:59:10.675Z → 2026-06-17T12:23:27.334Z
- To-do (unstarted): 2026-06-17T12:23:27.334Z → atual

## Relações
- Related to: SEND-495 — [api-legada] Adicionar campo `crm` ao crm_postback — HandleApi, ValidationService e SmsService

## Anexos
—
