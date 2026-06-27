# Playbook: DevSquad - Pydantic Input Contracts for Claw

Este playbook orienta o DevSquad na implementação de esquemas de tipagem estrita com Pydantic para validar todas as coordenadas de clique e dados de entrada do robô Claw, mitigando falhas físicas pré-execução.

## Definição da Meta
- **Meta**: "Criar um arquivo `claw_contracts.py` no diretório de esquemas que defina modelos Pydantic `ClickInput` (com atributos inteiros x e y validados no intervalo da resolução da tela, ex: 0 <= x <= 1920 e 0 <= y <= 1080) e `TypeInput` (com string de texto não vazia). O módulo deve lançar erros preventivos legíveis (`ValueError`) se os dados de entrada violarem as restrições físicas."

## Passos de Execução
1. **Especificação**: Uncle Bob gera a `specification` definindo os limites físicos da tela (ex: Full HD 1920x1080) e as restrições de validação de campo do Pydantic.
2. **Implementação**: Linus implementa os modelos `ClickInput` e `TypeInput` em `claw_contracts.py`, integrando validadores personalizados.
3. **Testes**: Kent Beck desenvolve testes unitários passando coordenadas válidas e forçando falhas deliberadas com coordenadas fora dos limites (ex: x=-50 ou y=2000).
4. **Auditoria**: Mitnick aprova as defesas preventivas contra estouro de limites ou injeção de parâmetros maliciosos.
