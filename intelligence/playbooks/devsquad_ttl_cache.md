# Playbook: DevSquad - TTL Cache Manager

Este playbook instrui o DevSquad a criar um componente gerenciador de cache persistente com suporte a tempo de expiração (TTL) utilizando o SQLite local.

## Definição da Meta
- **Meta**: "Criar um módulo Python `ttl_cache.py` contendo uma classe `TTLCacheManager` baseada em SQLite local que permita definir chaves, valores e tempos de expiração (TTL em segundos), com métodos `set(key, value, ttl_sec)`, `get(key)` que retorna None se expirado, e limpeza automática periódica."

## Passos de Execução
1. **Especificação**: Uncle Bob gera `specification` definindo a tabela SQLite, tipos e assinaturas.
2. **Implementação**: Linus gera `implementation` escrevendo o código SQLite e manipulação de datas.
3. **Testes**: Kent Beck gera `tests` testando `get()` após expiração simulada (ex: `time.sleep`).
4. **Auditoria**: Mitnick valida que não há vazamentos de conexões SQLite e aprova a entrega.
