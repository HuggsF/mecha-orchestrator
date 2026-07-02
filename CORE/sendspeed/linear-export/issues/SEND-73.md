# SEND-73 — [COMPANION][VETOR] - Ensino vetorial v1.2: Rotina automática diária

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | No priority |
| Responsável | Hugo Fernandes |
| Time | Sendspeed |
| Projeto | — |
| Labels | — |
| Parent | — |
| Criada | 2025-08-29T14:20:38.442Z por bruno.heidrich@sendspeed.com |
| Iniciada | 2025-09-04T19:37:21.512Z |
| Concluída | 2025-09-25T12:56:28.537Z |
| Arquivada | 2026-04-03T01:20:18.572Z |
| Vencimento | — |
| Branch | hugofernandes/send-73-companionvetor-ensino-vetorial-v12-rotina-automatica-diaria |
| URL | https://linear.app/sendspeed/issue/SEND-73/companionvetor-ensino-vetorial-v12-rotina-automatica-diaria |

## Descrição

**Como** Head de Produto, 
**quero** que o sistema **gere automaticamente** o vetor diário em dia/horário definidos 
**para** manter o aprendizado contínuo sem ação manual.

**Pronto quando**

* Consigo **definir o horário** da geração diária.
* A rotina cria a **nova versão** e registra quem/quando.
* Se falhar, aparece **aviso simples** e posso **reprocessar**.
* Tenho um relatório diário (% de converteu, % de nao converteu).
* Se um dado já foi vetorizado, ele não vai revetorizar esse dado
* Sempre no mesmo estilo de vetorização
* Travar no companyId do Felipe Palma por enquanto
* Alerta no slack quando a rotina terminar de rodar

---

* [OK] Consigo definir o horário da geração diária


* 
  * Config via PUT /api/vectors/schedule/config (time/timezone por empresa). Loop in-memory dispara no horário.
* [OK] A rotina cria a nova versão e registra quem/quando
  * Versão diária vectors_daily:YYYY-MM-DD em vector_versions.
  * createdBy capturado de x-user-id (execução manual) ou 'system' (agendada).
* [OK] Se falhar, aparece aviso simples e posso reprocessar
  * Erros notificados no Slack. Reprocesso: scripts/reprocess-day.js YYYY-MM-DD [COMPANY_ID] [--delete-vectors].
* [OK] Tenho um relatório diário (% de converteu, % de não converteu)
  * GET /api/vectors/daily-summary?persist=true gera KPIs; snapshot JSON/HTML salvo e linkado no Slack.
* [OK] Se um dado já foi vetorizado, ele não vai revetorizar esse dado
  * Idempotência por vetor: endpoints fazem fetch no índice e contam como skipped se já existir.
* [OK] Sempre no mesmo estilo de vetorização
  * Mesma pipeline (sanitize → journey text → embed → upsert) com limites em env.
* [OK] Travar no companyId do Felipe Palma por enquanto
  * Habilitar no config.env:

    ```shellscript
    VECTORS_ENFORCE_COMPANY_LOCK=true
    VECTORS_LOCKED_COMPANY_ID=689a2581af373b7c8ef9a707
    ```
* [OK] Alerta no Slack quando a rotina terminar de rodar
  * Sucesso/erro com resumo, contagens e link (Spaces/HTML) usando SLACK_HOOK_* e canais de jobs.

## Histórico de status
- Backlog (backlog): 2025-08-29T14:20:38.442Z → 2025-08-29T14:27:25.604Z
- To-do (unstarted): 2025-08-29T14:27:25.604Z → 2025-09-04T19:37:21.499Z
- In Progress (started): 2025-09-04T19:37:21.499Z → 2025-09-05T13:53:36.561Z
- Pull Request (started): 2025-09-05T13:53:36.561Z → 2025-09-25T12:30:37.110Z
- Product Review (started): 2025-09-25T12:30:37.110Z → 2025-09-25T12:56:28.522Z
- Released (completed): 2025-09-25T12:56:28.522Z → atual

## Relações
—

## Anexos
—
