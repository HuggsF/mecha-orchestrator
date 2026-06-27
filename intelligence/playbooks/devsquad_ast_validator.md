# Playbook: DevSquad - AST Markdown Hierarchy Validator

Este playbook orienta o DevSquad na criação de um script utilitário de validação estrutural de arquivos Markdown para garantir conformidade estrita com a hierarquia AST (H1 -> H2 -> H3).

## Definição da Meta
- **Meta**: "Criar um script Python `ast_validator.py` que leia um arquivo Markdown, extraia os cabeçalhos (`#`, `##`, `###`) e valide se a hierarquia está correta, lançando erros caso haja saltos inválidos (ex: transição direta de H1 para H3 sem um H2 intermediário), em conformidade com as regras de governança do debate Henrique vs. Hiansen."

## Passos de Execução
1. **Especificação**: Uncle Bob gera a `specification` descrevendo o parser de cabeçalhos e a árvore abstrata.
2. **Implementação**: Linus escreve o módulo `ast_validator.py` utilizando expressões regulares ou um parser de markdown nativo do Python (como `mistune` ou `markdown`).
3. **Testes**: Kent Beck implementa testes unitários que passam arquivos de teste válidos (H1->H2->H3) e falham deliberadamente com arquivos inválidos (H1->H3).
4. **Auditoria**: Mitnick verifica tratamento de exceções robusto e conformidade com as diretrizes do workspace.
