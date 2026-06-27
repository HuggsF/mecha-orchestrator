---
project_name: "MECHA System Daemon Integration"
conversation_id: "c37b2e6a-7739-4b10-b90e-c3cbb4a32253"
date: "2026-06-20"
emoji_rail: "📓 ➔ 🛡️ ➔ ⚙️ ➔ 🚀"
---

# MECHA Project Initialization

## Goal Description
Este documento registra formalmente a inicialização e o estado das diretrizes de governança do workspace MECHA, em conformidade com as regras do debate Henrique vs. Hiansen. O projeto une o processamento cognitivo do hardware Claw com a orquestração multi-agente do Tribunal Hermes e a automação de conformidade de Amanda no MS Teams.

## User Review Notes
As regras de governança e sincronia exigem que:
1. Todo o conhecimento viva indexado no RAG ou documentado em arquivos de notas markdown legíveis, em vez de oculto em configs.
2. Todo arquivo markdown passe no validador de cabeçalho AST (sem pulo de níveis H1 -> H2 -> H3).
3. Todas as ações do hardware Claw de alta criticidade passem por consulta das squads de IA.

## Proposed Changes Content
* **Tipagem Estrita (Henrique)**: Utilização de contratos robustos Pydantic para intercâmbio de dados e mensageria no barramento `AgentBus`.
* **Segurança RAG-first (Hiansen)**: Atualização contínua de telemetria no dashboard e logs vivos de tarefas em `AMANDA_TASKS.md`.
* **Bypasses Windows**: Mitigação do encoding padrão CP1252 no console forçando UTF-8 na raiz do buffer em todos os daemons e bots.

## Automated Tests Commands
Para validar a conformidade estrutural (Frontmatter e AST) deste plano, execute o seguinte comando:
```bash
python .mecha/ops/patterns/dynamic_typing.py --validate .mecha/project_initialization.md
```

## Manual Verification Steps
1. Validar se o dashboard está rodando em `http://localhost:8585/ops/mecha.html`.
2. Chamar o bot Amanda via Webhook do Teams e confirmar o empilhamento das tarefas em `AMANDA_TASKS.md`.
3. Certificar-se de que os daemons limpam capturas de tela temporárias da raiz do projeto instantaneamente após o uso ("Kill Lixo First").
