# Coverage Report: Claw Vision & Claw Control

## 1. Topologia e Consciência Estrutural
- **Módulos Alvo**: `ops/patterns/claw_vision.py` e `ops/patterns/claw_control.py`
- **Domínio**: Core (Operações de mouse, teclado e visão computacional)
- **Status Inicial**: 0% de cobertura.
- **Vulnerabilidades Identificadas**: Interação não segura com APIs do Win32 (WinDLL) e dependências físicas rígidas sem fail-safes explícitos, podendo causar "Fail-Open" se as coordenadas forem mal calculadas.

## 2. Decisões de TDD ("Let it Fail")
- **Fail-Fast**: Adicionados testes explícitos que injetam valores inválidos nas chamadas Win32 (ex: via `GetWindowRect` e resoluções do Desktop Virtual) para garantir que `ValueError` ou `PermissionError` sejam propagados para a raiz do loop, interrompendo comportamentos inseguros.
- **Firewall Cognitivo**: Cobertura do mecanismo que checa termos proibidos em tela via OCR e interrompe o clique físico usando `PermissionError("FIREWALL_BLOCK")`.
- **Botão de Pânico**: Verificação ativa (via `check_panic_button`) garante que qualquer movimentação anômala ou concorrência física cause falha na automação e pare a rotina.

## 3. Handoff para o DevOps Squad (Pendências)
Apesar da abstração garantida pelos Mocks, algumas verificações de fundo demandam infraestrutura:
- [ ] **Integração CI/CD Windows**: Configurar Runners do Windows no GitHub Actions para testar chamadas reais de `ctypes.windll` de forma segura.
- [ ] **Mocks Deep Win32**: Refinar abstrações em C para que a pilha física não dependa de telas ligadas para validar resoluções DPI, prevenindo falhas de compilação/teste intermitentes.

**Status Final**: Scripts de teste em Pytest criados e gravados em `ops/patterns/tests/`. Dados inseridos no RAG Dojo para determinismo.
