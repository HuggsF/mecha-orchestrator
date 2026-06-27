# 🌁 Antigravity Bridge Handoff Prompt

> **"Ponte de transmissão: Sincronização e emparelhamento de barramento ponto a ponto entre Micro-Frontends e Daemons Python."**

Este prompt orienta o agente de IA **Antigravity** na implementação do suporte backend necessário para o novo Event Bus unificado do MECHA, tornando os micro-frontends participantes ativos da rede distribuída.

---

## 📑 Handoff Prompt para a IDE

Cumpra as instruções técnicas abaixo para estender o servidor de desenvolvimento do MECHA (`telegram_bot.py` e `amanda_teams_bot.py`) para suportar o barramento de eventos unificado.

---

## 🗂️ Task Board de Execução (T1 — T10)

O agente deve analisar, rastrear e executar a seguinte lista de tarefas de conformidade:

### `[ ]` T1: Mapear Endpoints de WebSocket e REST no Servidor HTTP
* Implementar o suporte a conexões de WebSocket no caminho `/ws/bus` do servidor HTTP em `telegram_bot.py`.
* Criar endpoints REST de fallback `/api/bus/publish` (POST) e `/api/bus/poll` (GET) para clientes sem suporte a conexões persistentes.

### `[ ]` T2: Modelar o Gerenciador Central de Eventos (EventHub)
* Criar uma classe thread-safe `EventHub` que gerencie as inscrições ativas (conexoes WebSocket), despache e filtre mensagens baseando-se no campo `topic`.
* Implementar proteção contra race-conditions sob múltiplos acessos utilizando locks do Python (`threading.Lock`).

### `[ ]` T3: Implementar o Buffer Circular de Telemetria
* Desenvolver uma fila circular (buffer em memória de até 100 mensagens) no `EventHub` para guardar o histórico recente de eventos disparados de forma que chamadas `/api/bus/poll` possam resgatar estados perdidos durante oscilações de rede.

### `[ ]` T4: Acoplar o Loop do Claw ao EventHub
* Alterar o `claw_loop.py` para injetar eventos diretamente no `EventHub` sempre que ocorrer uma transição de estado da janela (`nav.open`), uma ação de firewall (`claw.firewall`) ou eventos de auto-recuperação.

### `[ ]` T5: Integrar Endpoints do MS Teams Webhook (Amanda)
* Ajustar o FastAPI em `amanda_teams_bot.py` para publicar mensagens no `EventHub` local no momento em que um operador envia comandos especiais do Teams (ex: logs de criação de tarefas `/task add` devem disparar o tópico `task.created`).

### `[ ]` T6: Desenvolver Validação Estrita do Envelope Pydantic
* Criar classes de validação baseadas no Pydantic no arquivo `dynamic_typing.py` para validar a assinatura do payload de cada mensagem enviada ao barramento antes de distribuí-la.

### `[ ]` T7: Refatorar o Dashboard mecha.html para Conectar no Bus
* Adicionar a lógica de conexão WebSocket (`new WebSocket(...)`) no javascript principal do `mecha.html`.
* Implementar mecanismos de auto-reconexão robustos com tempo de espera de 3000ms após quedas inesperadas de sinal.

### `[ ]` T8: Adicionar Animação de Realce e Pulso no Grafo
* Atualizar o renderizador de nós em `mecha.html` para aplicar a classe css `.pulse` temporariamente ao nó correspondente quando um evento `node.select` é recebido no barramento.

### `[ ]` T9: Implementar o Log de Eventos Unificado no Terminal
* Fazer com que o `telegram_bot.py` imprima mensagens coloridas em formato estruturado no stdout toda vez que um evento for transmitido pelo barramento (ex: `[BUS:node.select] node_id=login_view`), respeitando a codificação de console UTF-8.

### `[ ]` T10: Executar a Suite E2E de Comunicação
* Criar um script de teste em `ops/patterns/test_e2e_eventbus.py` que conecte via WebSocket e REST, publique um evento simulado, verifique o recebimento e confirme que os dados trafegados são 100% íntegros.
