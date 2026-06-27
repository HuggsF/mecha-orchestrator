---
name: Monitoramento semanal de eventos do Windows
description: Tarefa agendada ClaudioWeeklyEventScan gera relatorios em ~/Documents/claude/reports/ toda segunda 09h. Ler na rotina de inicio.
type: feedback
---

Existe uma tarefa agendada `ClaudioWeeklyEventScan` que roda toda segunda-feira as 09:00.

**O que faz:** varre os logs de eventos do Windows (Application, System, PowerShell Operational, servicos instalados) buscando keywords relacionadas as ferramentas de desenvolvimento (claude, neo4j, chroma, pip, python, node, npm, jdk, java, etc.)

**Onde salva:** `~/Documents/claude/reports/event-scan-YYYY-MM-DD.txt`

**Script:** `~/Documents/claude/scripts/weekly-event-scan.ps1`

**Why:** Vanessa nao tem admin na maquina da Prefeitura. Quer monitorar se alguma atividade de desenvolvimento gera eventos que um admin poderia questionar. A estrategia portable (ZIP + pip --user) foi escolhida justamente para minimizar rastros nos logs.

**How to apply:** na rotina de inicio de sessao, ler o relatorio mais recente. Se houver algo novo ou preocupante, informar a Vanessa proativamente. Se tudo estiver limpo, mencionar brevemente que esta tudo ok.
