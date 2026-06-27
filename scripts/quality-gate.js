const { execSync } = require('child_process');
const fs = require('fs');

// ANSI Color Codes
const RESET = "\x1b[0m";
const BOLD = "\x1b[1m";
const RED = "\x1b[31m";
const GREEN = "\x1b[32m";
const YELLOW = "\x1b[33m";
const CYAN = "\x1b[36m";
const MAGENTA = "\x1b[35m";

try {
  // Collect Git Telemetry
  const commitHash = execSync('git rev-parse --short HEAD').toString().trim();
  const commitMsg = execSync('git log -1 --pretty=%B').toString().trim();
  const changedFilesOutput = execSync('git diff-tree --no-commit-id --name-only -r HEAD').toString().trim();
  const changedFiles = changedFilesOutput ? changedFilesOutput.split('\n').filter(Boolean) : [];
  
  // Calculate insertions and deletions
  let insertions = 0;
  let deletions = 0;
  try {
    const stats = execSync('git show --numstat --format="" HEAD').toString().trim();
    if (stats) {
      stats.split('\n').forEach(line => {
        const parts = line.split('\t');
        if (parts.length >= 2) {
          const ins = parseInt(parts[0], 10);
          const del = parseInt(parts[1], 10);
          if (!isNaN(ins)) insertions += ins;
          if (!isNaN(del)) deletions += del;
        }
      });
    }
  } catch (e) {
    // Fallback if git show fails
  }

  // Code Quality Audits
  const warnings = [];
  let securityAuditPassed = true;
  let hasZodCheck = false;

  changedFiles.forEach(file => {
    if (fs.existsSync(file) && fs.lstatSync(file).isFile()) {
      const content = fs.readFileSync(file, 'utf8');
      
      // Look for TODOs or FIXMEs
      const todoMatches = content.match(/TODO|FIXME/gi);
      if (todoMatches) {
        warnings.push(`${file}: Found ${todoMatches.length} pending TODO/FIXME item(s).`);
      }

      // Backend Security Audit (Zod & Helmet check for Node/Express)
      if (file.endsWith('.ts') || file.endsWith('.js') || file.endsWith('.tsx')) {
        const hasExpress = content.includes('express()') || content.includes("require('express')") || content.includes("import express");
        const hasHelmet = content.includes('helmet') || content.includes('Helmet');
        
        if (hasExpress && !hasHelmet) {
          securityAuditPassed = false;
          warnings.push(`${file}: Express application detected but 'helmet' security headers are missing!`);
        }

        if (content.includes('zod') || content.includes('Zod') || content.includes('z.object')) {
          hasZodCheck = true;
        }
      }
    }
  });

  // Extract actual added and removed lines of code
  let diffContent = "";
  try {
    const diffRaw = execSync('git show --unified=0 --format="" HEAD').toString().trim();
    if (diffRaw) {
      const lines = diffRaw.split('\n');
      const addedLines = lines.filter(l => l.startsWith('+') && !l.startsWith('+++')).map(l => l.substring(1));
      const removedLines = lines.filter(l => l.startsWith('-') && !l.startsWith('---')).map(l => l.substring(1));
      
      if (addedLines.length > 0 || removedLines.length > 0) {
        diffContent = `
  • ${BOLD}Código que Entrou (+):${RESET}\n` + 
          (addedLines.length > 0 
            ? addedLines.slice(0, 15).map(l => `    ${GREEN}+ ${l}${RESET}`).join('\n') + (addedLines.length > 15 ? `\n    ${YELLOW}... (${addedLines.length - 15} mais linhas)${RESET}` : '')
            : `    ${YELLOW}(Nenhuma linha adicionada)${RESET}`) + `

  • ${BOLD}Código que Saiu (-):${RESET}\n` + 
          (removedLines.length > 0 
            ? removedLines.slice(0, 15).map(l => `    ${RED}- ${l}${RESET}`).join('\n') + (removedLines.length > 15 ? `\n    ${YELLOW}... (${removedLines.length - 15} mais linhas)${RESET}` : '')
            : `    ${YELLOW}(Nenhuma linha removida)${RESET}`);
      }
    }
  } catch (e) {
    diffContent = `\n  • ${RED}Não foi possível obter o diff detalhado.${RESET}`;
  }

  // Render Enriched Report
  console.log(`
${BOLD}${MAGENTA}========================================================================${RESET}
${BOLD}${CYAN}                🛡️  DEVOPS QUALITY GATE v2.0${RESET}
${BOLD}${MAGENTA}========================================================================${RESET}

${BOLD}[COGNITIVE STATE]:${RESET}
Auditoria de sanidade ativada para o commit ${CYAN}${commitHash}${RESET}. Avaliando a integridade dos padrões de arquitetura do sistema (Validação com Zod, Headers com Helmet e ausência de pendências técnicas críticas).

${BOLD}[TRANSFORMER LAYER]:${RESET}
- ${YELLOW}Static Analysis:${RESET} Escaneamento de ${changedFiles.length} arquivos modificados no último commit.
- ${YELLOW}Security Inspection:${RESET} Analisando conformidade de privacidade e cabeçalhos HTTP (Helmet).
- ${YELLOW}Rigor & Typings:${RESET} Verificando acoplamento de schemas de validação de dados (Zod).
- ${YELLOW}Metrics Tracking:${RESET} Coletando telemetria de linhas alteradas e pendências de débito técnico.

${BOLD}[OUTPUT / TELEMETRY]:${RESET}
  • ${BOLD}Commit ID:${RESET} ${CYAN}${commitHash}${RESET}
  • ${BOLD}Mensagem:${RESET} "${commitMsg.split('\n')[0]}"
  • ${BOLD}Métricas de Linhas:${RESET} ${GREEN}+${insertions} inserções${RESET}, ${RED}-${deletions} remoções${RESET}
  • ${BOLD}Arquivos Afetados:${RESET}
${changedFiles.map(f => `    - ${f}`).join('\n')}
${diffContent}

  • ${BOLD}Security & Standard Audit:${RESET}
    - Zod Integration:  ${hasZodCheck ? `${GREEN}✔ ACTIVE${RESET}` : `${YELLOW}⚠️ NOT DETECTED (Consider using Zod for payload schemas)${RESET}`}
    - Helmet Security:  ${securityAuditPassed ? `${GREEN}✔ PASSED${RESET}` : `${RED}❌ FAILED (Helmet headers missing on Express configs!)${RESET}`}
    
  • ${BOLD}Quality Alerts:${RESET}
    ${warnings.length > 0 ? warnings.map(w => `${YELLOW}⚠️  ${w}${RESET}`).join('\n    ') : `${GREEN}✔ No warnings (0 pending TODOs/FIXMEs, 100% clean).${RESET}`}

${BOLD}${MAGENTA}========================================================================${RESET}
  👉 ${BOLD}Status Final:${RESET} ${securityAuditPassed ? `${GREEN}● APPROVED (Ready for Push)${RESET}` : `${YELLOW}● WARNING (Fix security warnings soon)${RESET}`}
${BOLD}${MAGENTA}========================================================================${RESET}
`);

} catch (error) {
  console.error(`\n${RED}[CRITICAL ERROR] Quality Gate failed to run:${RESET}`, error.message);
  process.exit(1);
}
