# SEND-517 — 1. Mapear e validar os gatilhos de UI do front da NGX para jornadas UserIn (spike)

| Campo | Valor |
| -- | -- |
| Status | In Progress (started) |
| Prioridade | No priority |
| Responsável | — |
| Time | Sendspeed |
| Projeto | — |
| Labels | UserIn, Spike, User Story |
| Parent | — |
| Criada | 2026-06-22T17:58:04.118Z por Vinicius Carneiro |
| Iniciada | 2026-06-25T15:09:36.215Z |
| Concluída | — |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-517-1-mapear-e-validar-os-gatilhos-de-ui-do-front-da-ngx-para |
| URL | https://linear.app/sendspeed/issue/SEND-517/1-mapear-e-validar-os-gatilhos-de-ui-do-front-da-ngx-para-jornadas |

## Descrição

**Como** time de produto da UserIn

**Quero** mapear e validar quais gatilhos de UI do front da NGX existem e disparam de forma confiável

**Para** desenhar jornadas sabendo em quais gatilhos posso confiar, sem descobrir limitação só na implementação

### 📈 Use Case

Hoje as jornadas UserIn no front da NGX são desenhadas sem um mapa claro de quais gatilhos de UI existem e quão confiáveis são — cada jornada redescobre isso na marra. Este spike levanta o inventário de gatilhos de UI (client-side) disponíveis no front da NGX, valida quais disparam de forma confiável e em que condições, e entrega um mapa com veredito por gatilho. É spike: o entregável é conhecimento documentado, não jornada implementada.

### ✅ Critérios de aceite (DoD do spike)

* Existe um inventário documentado dos gatilhos de UI do front da NGX no escopo definido (ex: abrir/fechar modal de registro/login/depósito, exit-intent, page load, cliques-chave)
* Cada gatilho mapeado tem: onde/quando dispara, como a UserIn captura (client-side via script próprio ou se precisa de hook da NGX), confiabilidade observada e condições (device antigo/3G, navegação SPA)
* Cada gatilho tem veredito explícito: utilizável / utilizável com ressalva / não utilizável (com motivo)
* Gatilhos não capturáveis só client-side ficam sinalizados como dependência externa (o que a NGX precisaria expor)
* Validação feita no ambiente de homologação da Apostou
* Time-boxed: ao fim da caixa de tempo, entrega o mapa com o que foi coberto e o que ficou pendente

### 🧩 Cenários de validação (por gatilho)

* Disparar a ação na UI (ex: fechar o modal de registro) e confirmar que a UserIn captura o gatilho
* Repetir em device antigo/3G e em navegação SPA para checar consistência
* Verificar duplicidade/disparo indevido (dispara 2x? dispara quando não deveria?)
* Gatilho não capturável client-side → registrar o que a NGX precisaria expor
* Consolidar tudo no mapa com o veredito por gatilho

## Histórico de status
- To-do (unstarted): 2026-06-22T17:58:04.118Z → 2026-06-25T15:09:36.229Z
- In Progress (started): 2026-06-25T15:09:36.229Z → atual

## Relações
—

## Anexos
—
