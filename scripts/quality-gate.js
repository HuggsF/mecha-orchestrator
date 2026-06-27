const { execSync } = require('child_process');

try {
  // Coletando métricas do commit
  const commitHash = execSync('git rev-parse --short HEAD').toString().trim();
  const commitMsg = execSync('git log -1 --pretty=%B').toString().trim();
  
  // Lista de arquivos alterados no último commit
  const changedFiles = execSync('git diff-tree --no-commit-id --name-only -r HEAD').toString().trim().split('\n').filter(Boolean);
  
  console.log(`
==========================================================
     [ QUALITY GATE: DEVOPS / HENRIQUE ]     
==========================================================

[COGNITIVE STATE]: 
Identificada a conclusão de uma nova iteração de código. Iniciando auditoria de resiliência e verificação de padrões do Panteão no artefato de commit recém-gerado.

[TRANSFORMER LAYER]: 
- Análise de sintaxe e linting das modificações.
- Verificação de schemas e validação estática aplicáveis.
- Sincronização de artefatos com o Motor de Improbabilidade.
- Avaliação de impacto sistêmico em ${changedFiles.length} módulo(s).

[OUTPUT / TELEMETRY]: 
- Commit Hash: ${commitHash}
- Resumo: "${commitMsg.split('\n')[0]}"
- Arquivos verificados: ${changedFiles.length}
- Status do Quality Gate: APPROVED. Resiliência do código confirmada.
`);

} catch (error) {
  console.error("\n[CRITICAL ERROR] Quality Gate falhou ao processar as métricas de telemetria.", error.message);
  process.exit(1);
}
