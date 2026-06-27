---
name: Memoria exclusivamente no Google Drive
description: NUNCA persistir arquivos de memoria no notebook corporativo — ler e escrever SEMPRE do Drive
type: feedback
---

Toda memoria do Claudio vive exclusivamente no Google Drive. O notebook do trabalho e corporativo e pode ser acessado por terceiros.

**Locais:**
- Fonte da verdade: `G:\Meu Drive\Claudio\memory\`
- Backup: `G:\Meu Drive\backup-memoria-claude\`
- Local (notebook): SOMENTE o `MEMORY.md` como indice fino — zero arquivos de conteudo

**Why:** Notebook corporativo da Prefeitura, acessivel por outros. Memorias contem contexto de projetos pessoais, feedbacks, e informacoes que nao devem ficar expostas em maquina de trabalho.

**How to apply:**
- Ao criar/editar qualquer memoria: escrever nos 2 destinos do Drive
- Ao ler memorias: sempre de `G:\Meu Drive\Claudio\memory\`
- NUNCA criar arquivos .md de memoria no path local (`~/.claude/projects/.../memory/`) exceto MEMORY.md
- Ao iniciar sessao: puxar contexto do Drive
- Se o Drive nao estiver montado: avisar Vanessa e NAO criar arquivos locais como fallback
