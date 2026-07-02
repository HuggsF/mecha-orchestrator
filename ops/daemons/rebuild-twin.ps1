# rebuild-twin.ps1 — recria o mecha_ontology_graph na rede CORRETA, preservando os dados.
# SEGURO: 'docker rm' (sem -v) NÃO apaga volumes NOMEADOS — só o container. Os dados
# vivem em infrastructure_neo4j_data, que permanece. Heap reduzido 1G->512m (host sob
# pressão de memória; o grafo é pequeno, ~349 nós, então sobra).
$ErrorActionPreference = "Stop"

Write-Host "[1/3] Removendo o container morto (volumes nomeados PERMANECEM)..."
docker rm mecha_ontology_graph 2>$null | Out-Null

Write-Host "[2/3] Recriando na infrastructure_mecha_net, apontando pro mesmo disco..."
docker run -d --name mecha_ontology_graph `
  --network infrastructure_mecha_net `
  -p 7474:7474 -p 7687:7687 `
  -v infrastructure_neo4j_data:/data `
  -v infrastructure_neo4j_plugins:/plugins `
  -e NEO4J_AUTH=neo4j/rootroot `
  -e 'NEO4J_PLUGINS=["apoc"]' `
  -e NEO4J_dbms_memory_heap_max__size=512m `
  --restart unless-stopped `
  neo4j:5.18.0 | Out-Null

Write-Host "[3/3] Aguardando boot (~25s) e contando nós (esperado ~349)..."
Start-Sleep -Seconds 25
docker exec mecha_ontology_graph cypher-shell -u neo4j -p rootroot --format plain "MATCH (n) RETURN count(n) AS nodes"
Write-Host "Se contou ~349, o twin voltou com os dados intactos e na rede certa."
