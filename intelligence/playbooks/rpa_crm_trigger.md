# Playbook: RPA CRM Trigger Automation

Este playbook é executado pelo agente Claw para validar a interface web do CRM de forma simulada. Ele abre a tela do CRM, navega até as jornadas e aciona o modal de disparo manual.

- set_goal "Focar na aba do navegador com o CRM aberto"
- wait 2
- click 120 180
- wait 1
- set_goal "Clicar na aba de Jornadas e abrir o modal de disparo"
- click 80 180
- wait 2
- click 850 120
- wait 2
- set_goal "Preencher o formulário com a tarefa de verificação"
- click 450 310
- wait 1
- type "Claw Automated Browser Validation"
- wait 1
- click 450 390
- wait 1
- click 450 430
- wait 1
- click 600 520
- wait 2
- set_goal "Submeter o formulário de disparo manual"
- click 550 520
- wait 3
- set_goal "Confirmar que a tarefa Claw Automated Browser Validation foi adicionada à tabela"
