---
project_name: sendspeed-absorption
conversation_id: debate-o6-s2-2026-07-02
date: "2026-07-02"
emoji_rail: 📡 ➔ 🕸️ ➔ 🛡️
domain: sendspeed
module: sendspeed_integrations
source: linear-export
status: confirmed
---

# ➔ Integrações Externas SendSpeed

## iGaming NGX → UserIn (SEND-510, SEND-516, SEND-506)

### 16 eventos suportados

Categoria: registro, depósito, KYC, jogo, bônus, retirada, exclusão, etc.

### Endpoints de ingestão

```
POST /user-registration
POST /deposit-confirmation
```

### Segurança (SEND-510 / webhook_security_spec)

```
X-Auth-Signature: Base64(HMAC-SHA256(payload, secret_por_cliente))
```

- Secret diferente por cliente e ambiente (nunca hardcoded)
- 401 sem persistência em falha de assinatura
- Idempotência via `external_id` — reentrega não duplica
- DLQ com retry: 1 / 5 / 15 min

### Gatekeepers obrigatórios em todo design

| Gatekeeper          | Regra                                      |
|---------------------|--------------------------------------------|
| Consentimento       | `user_accepted_notifications = true`       |
| KYC                 | Verificação antes de qualquer jornada      |
| Blocklist           | Bloquear pós `USER_DELETE`                 |
| Teste               | `is_test = true` fora de produção          |

## Recuperação de cadastro — cliente Apostou (SEND-515)

Use case: usuário fecha modal de registro NGX → modal de recuperação UserIn com Smart Block.

- Regra: máx 1x por sessão
- Flag liga/desliga sem deploy
- Medição antes/depois (taxa de conclusão de cadastro)

Spike SEND-517: gatilhos de UI do front NGX (client-side) ainda em investigação.

## Registry de adapters CRM

| Adapter      | Estado          | Observação                              |
|--------------|-----------------|------------------------------------------|
| Smartico     | Produção        | `SmarticoPayloadBuilder`, `callback_url` |
| FastTrack    | Em construção   | `FastTrackClient` via `ICrmCallbackClient`; auth/payload aguarda SEND-504 |
| NGX          | Em construção   | `IGamingWebhookHandler` genérico         |

## Padrão genérico recomendado — adaptador iGaming (SEND-510)

```python
class IGamingWebhookHandler:
    def validate_signature(self, payload: bytes, sig: str, secret: str) -> bool: ...
    def check_idempotency(self, external_id: str) -> bool: ...
    def apply_gatekeepers(self, user_id: str, event: str) -> bool: ...
    def route_to_journey(self, event: str, payload: dict) -> None: ...
    def enqueue_dlq(self, payload: dict, attempt: int) -> None: ...
```
