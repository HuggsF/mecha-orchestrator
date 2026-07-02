# ADR-001 — Shura como Orquestrador Mestre do Sistema Multi-Agentes Mecha

## Status

Aceita

## Data

2026-06-30

## Contexto

No ecossistema multi-agentes Mecha, o handoff de tarefas entre diferentes domínios (Engenharia, QA, DevOps, Produto) sem uma central de governança levou a regressões e desalinhamentos de domínio (squads executando tarefas alheias ao seu escopo) e falhas não rastreáveis no fluxo de CI/CD.
Precisávamos definir um orquestrador mestre para validar a transição, qualidade, build e domínio antes que qualquer tarefa pudesse avançar na esteira do AgentBus.

## Decisão

Elegeu-se o **Shura 255** (Tribunal Squad) como o Orquestrador Mestre, acompanhado de regras de roteamento (gate) rígidas, materializadas em código nos serviços `cross_squad_router.py` e `shura_daemon.py`.
O sistema impõe as seguintes 14 regras de orquestração:

### Regras de Handoff (ORCH-01..ORCH-04)
- **ORCH-01**: Todo handoff entre times passa por Shura. Shura é o único orquestrador.
- **ORCH-02**: Uma tarefa não passa entre times sem passar pelo gate de validação do Shura recebendo um veredito de aprovação (1).
- **ORCH-03**: Um veredito de reprovação (0) obriga a task a retornar ao time de origem para correção, evitando handoffs defeituosos.
- **ORCH-04**: O domínio do handoff é restrito — nenhum squad recebe uma task fora do seu próprio domínio.

### Regras de Roteamento Inteligente (ORCH-12..ORCH-14)
- **ORCH-12 (Pré-verificação)**: Antes do handoff, o sistema checa se o squad destino já possui uma task em andamento do mesmo domínio. Isso previne tarefas cruzadas acidentais.
- **ORCH-13 (Balanceamento de carga)**: Para rotas declaradas como POOL, o roteamento escolhe dinamicamente o squad PRONTO com menor carga (`in_flight`), utilizando métricas para otimização de failover sem desrespeitar ORCH-01..04.
- **ORCH-14 (Rota SendSpeed)**: A rota dedicada ao domínio sendspeed aplica o roteamento "pool-ready" de forma no-op (pool único), mas emite adequadamente métricas no AgentBus para preservar a governança Shura.

### Governança e Respostas Agregadas (ORCH-05..ORCH-10)
- **ORCH-05**: Shura assina passivamente o AgentBus durante toda a execução.
- **ORCH-06**: Gates de Build e Testes devem estar verdes antes da entrega final (fail fast).
- **ORCH-07**: A resposta final ao usuário é invariavelmente a consolidação entregue pelo Shura (os squads individuais não respondem direto).
- **ORCH-08**: Toda orquestração encerra gerando um relatório formal dos 5 domínios (código, arquitetura, engenharia, testes, produto).
- **ORCH-09**: A orquestração é event-driven e projetada como daemon persistente.
- **ORCH-10**: Todas essas regras estão aplicadas em *código* e não dependem apenas da aderência do LLM ao system prompt.

## Consequências

- **Prós**: Determinismo no fluxo de CI/CD, prevenção de regressões entre domínios, bloqueio de alucinações de squads (já que Shura deve aprovar o debate). O roteamento inteligente permite escalabilidade com pools de agentes por domínio.
- **Contras**: Adiciona latência na entrega (cada transição requer validação de gate/debate) e força o Shura a ser um SPOF (Single Point of Failure) da arquitetura, exigindo que seu daemon seja altamente resiliente.

## Referências

- `intelligence/rules/orchestration_rules.json`
- `ops/patterns/cross_squad_router.py`
- `ops/patterns/shura_daemon.py`
- `ops/patterns/shura_gate.py`
