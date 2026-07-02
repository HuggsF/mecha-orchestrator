# Ontology & Topology Reference (pedroCRM)

Este documento descreve a referência de implementação do painel de Ontologia e Topologia extraída da branch/projeto `sendspeed-engage-ai-flow-08-pedro-crm`, para servir de fundação na reconstrução ou integração de dados da orquestração MECHA e do RAG.

## 1. Visão Geral (OntologyOverviewPage)
A página de **Ontology Overview** atua como o painel central de governança de dados da empresa, consolidando as definições através de `objectApi` e `ontologyApi`.

- **Métricas Chave**: 
  - `ATTRIBUTE`: Propriedades puras.
  - `AGG`: Agregações ou totalizadores de dados (e.g. Total Gasto).
  - `SIGNAL`: Eventos comportamentais / Triggers.
  - `OUTPUT`: Campos computados/derivados (Modelos preditivos, Scores de IA).
  - `RELATIONSHIP`: Ligações entre as Entidades e o UserProfile.

## 2. Topologia em Canvas (ObjectGraph)
A visualização de relações e topologias de eventos utiliza a biblioteca `@xyflow/react` (ReactFlow). 
- **Nó Principal (`UserProfileNode`)**: O centro de gravidade (Perfil do Utilizador), destacando a quantidade de campos diretamente vinculados.
- **Entidades Auxiliares (Custom Nodes)**: Diferentes verticais (`bets`, `ecommerce`, `saas`) têm esquemas de cor únicos e se conectam ao UserProfile por *Edges*.
- **Drag & Drop Relationships**: Suporta conexões desenhadas pelo usuário conectando *handles* para instanciar novos `CreateRelationshipDialog`s.

## 3. Estrutura de Metadados e API
O CRM divide o esquema semântico em três domínios principais de busca, que os agentes do MECHA devem seguir ao compor dados ou ingerir no Qdrant:
1. **ObjectTypeManager**: Gerenciamento de classes (Ex: Entidade "Compra", Entidade "Partida").
2. **SchemaDetector**: Ingestão de CSV e Auto-Mapping de tipos de dados.
3. **SignalConfigurator & OutputConfigurator**: Painéis para desenhar fórmulas complexas que atualizam automaticamente os atributos agregados e geram scores via IA.

## 4. Integração com o MECHA (Próximos Passos)
Para o `rag-dojo` e o `amanda_teams_bot` trabalharem em harmonia com este padrão:
- O RAG deve incorporar as definições do `ObjectGraph.tsx` para entender as associações primárias entre o `UserProfile` e eventos de sistema.
- A ingestão de ontologias no MECHA deve ser determinística, onde a IA (Ex: Auditor) recusa alterações no schema que não possuam as propriedades obrigatórias (ex: `dataType`, `kind`).
