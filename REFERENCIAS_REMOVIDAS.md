# Referências Removidas — Arquivos Docker, Infra e Docs

> Arquivos com referências a rpg_cortex / extracted. Guarde no .zip para restauração.

---

## 1. Infra / Docker

### infra/Dockerfile
```dockerfile
COPY automation_hub/ /app/automation_hub/
COPY src/extracted/rpg_cortex/ /app/rpg_cortex/
```

### infra/docker-compose.yml
```yaml
volumes:
  - ../automation_hub:/app/automation_hub
  - ../src/extracted/rpg_cortex:/app/rpg_cortex
```

### infra/claude_workspace.sh
```bash
for log in \
    "automation_hub/logs/brain.log" \
    "automation_hub/logs/operator.log" \
    "rpg_cortex/logs/hardware.log"; do
```

### infra/replicate_agent.sh
```bash
for dir in automation_hub src infra bin; do
```
(Nota: copia src/ (não rpg_cortex). Mantido para replicar o projeto completo.)

---

## 2. Código Python

### src/agents/computer_use_agent.py
```python
TEMP_DIR = PROJECT_ROOT / "src" / "extracted" / "rpg_cortex" / "temp"
```

### src/neural_link/telemetry/jitbit_connector.py
```python
# Caminhos comuns do Jitbit (espelhado de rpg_cortex para evitar dependência)
def _resolve_jitbit_wrapper():
    try:
        from src.extracted.rpg_cortex.hardware.jitbit_wrapper import JitbitWrapper
        return JitbitWrapper
    except ImportError:
        return None
# ...
"JitbitWrapper não disponível. Instale rpg_cortex ou passe jitbit_wrapper."
```

### src/extracted/__init__.py
```python
"""
Extracted packages — módulos extraídos para organização.
- rpg_cortex: Hardware automation, macros, Jitbit (JitbitWrapper, MacroExecutor, MacroKnowledgeBase)
"""
```

---

## 3. Documentação

### docs/specs/usecases/UC-AUDIT-001.md
```
src/, automation_hub/, rpg_cortex/, tools/, scripts/, infra/
```

### docs/guides/GET_STARTED.md
```
rpg_cortex/             # Hardware automation
```

### docs/audit/rpg_cortex.md
Arquivo inteiro — Audit Report sobre rpg_cortex/

### docs/audit/SUMMARY.md
- Linha 15: `| 5 | rpg_cortex/ | 80 | 70 | 65 | **72.5** | 13 | 2 |`
- Linha 42: `rpg_cortex, scripts, tools`
- Linha 66: `Add thread safety to pyautogui calls in rpg_cortex`

### docs/INDEX.md
- Linha 46: `| [rpg_cortex](audit/rpg_cortex.md) | 72.5 | rpg_cortex/ |`

### TODO_CLAUDE.md
```
| rpg_cortex        | Mouse, macros, visão             | logs/hardware.log       |
```

---

## 4. Arquivos da Root (adicionados ao zip e removidos)

### Arquivos removidos inteiramente
- `SETUP_QUICK_START.md` — Setup Rápido RPG-Cortex, jitbit_bridge, .kiro/specs/rpg-cortex
- `README_INFRASTRUCTURE.md` — RPG-Cortex Infrastructure, links .kiro/specs/rpg-cortex
- `NEXT_STEPS.md` — Próximos Passos RPG-Cortex, jitbit_bridge, Missão Zero
- `INFRASTRUCTURE_STATUS.md` — Status Infraestrutura RPG-Cortex, Ponte Jitbit
- `macro-jitbit-sanitization-block.mcr` — Macro binário Jitbit
- `macro-jitbit-test-patched.mcr` — Macro binário Jitbit
- `macro-jitbit-test.mcr` — Macro binário Jitbit

### Referências editadas (conteúdo original no zip)
- `neural_link_orquestrator.md` — "automacao via RPG-Cortex" → removido
- `requirements.txt` — "RPG-Cortex" no comentário → genérico
- `.env.example` — Seção removida:
```
# Jitbit Automation
JITBIT_PATH=C:/Program Files/Jitbit/jitbit.exe
MACROS_DIR=./macros
```

---

## 5. Módulo Removido

```
src/extracted/rpg_cortex/
├── __init__.py
├── hardware/
│   ├── __init__.py
│   ├── cartographer.py
│   ├── emergency.py
│   ├── exceptions.py
│   ├── jitbit_wrapper.py
│   ├── macro_executor.py
│   ├── rpg_controls.py
│   └── smooth_movement.py
├── knowledge/
│   ├── __init__.py
│   ├── macro_knowledge_base.py
│   ├── macros_map.yaml
│   ├── mapa_interface.json
│   └── rpg_skills.txt
├── temp/
└── logs/
```
