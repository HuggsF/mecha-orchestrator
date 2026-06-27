# Playbook: Smartico RPA Demo

Este é um playbook de teste para validar o motor de automação do MECHA SDK via Telegram. Ele simula os passos de um operador realizando login automático no Smartico Backoffice.

- set_goal "Iniciar automação de login no Smartico Backoffice"
- wait 2
- click 150 200
- wait 1
- type "operador_mecha"
- wait 1
- click 150 280
- wait 1
- type "senha_ultra_secreta_777"
- wait 2
- click 300 400
- wait 3
- set_goal "Verificar o carregamento do Dashboard pós-login"
