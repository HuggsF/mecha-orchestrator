# Playbook: DevSquad - Qdrant RAG Ingester & Searcher

Este playbook orienta o DevSquad no desenvolvimento de uma classe utilitária em Python para indexação e busca semântica em coleções do banco vetorial local Qdrant.

## Definição da Meta
- **Meta**: "Criar um componente `qdrant_rag.py` contendo uma classe `QdrantRAGHelper` que encapsule a conexão com o cliente local do Qdrant, ofereça métodos para criar uma coleção se não existente, fazer upsert de documentos com metadados estruturados, e realizar busca de similaridade de cosseno com limitador de quantidade (limit) e score mínimo."

## Passos de Execução
1. **Especificação**: Uncle Bob define a assinatura da classe, tipos Pydantic para os payloads de documento e limites de score.
2. **Implementação**: Linus implementa `QdrantRAGHelper` integrando a biblioteca oficial `qdrant-client` e manipulação de payloads de vetores.
3. **Testes**: Kent Beck desenvolve testes de integração conectando ao container Qdrant local, indexando frases de teste e validando a busca semântica.
4. **Auditoria**: Mitnick verifica segurança contra injeção de prompt e manipulação segura de chaves API ou endpoints de conexão.
