# Playbook: RPA Obsidian Logger Automation

Este playbook é executado pelo Claw para registrar notas de auditoria diretamente no Obsidian local. Ele simula o foco na janela do Obsidian, o atalho de criação de nota e digitação.

- set_goal "Focar na janela do Obsidian Graph"
- wait 2
- click 100 100
- wait 1
- set_goal "Enviar comando Ctrl+N para criar nova nota"
- preempt_command "shortcut" {"keys": ["ctrl", "n"]}
- wait 2
- set_goal "Digitar o título e o corpo do log da auditoria"
- type "Log de Auditoria - Tribunal Hermes"
- wait 1
- preempt_command "press" {"key": "enter"}
- wait 1
- type "Jornada automatizada concluída com sucesso. Purity Score: 9.8"
- wait 1
- set_goal "Salvar e fechar o editor"
- preempt_command "shortcut" {"keys": ["ctrl", "s"]}
- wait 2
- set_goal "Confirmar que a nota foi persistida no grafo"
