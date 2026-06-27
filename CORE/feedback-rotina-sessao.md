---
name: Rotina obrigatoria de inicio e fim de sessao
description: Ao iniciar conversa, ler ultima sessao + relatorios. Ao finalizar, atualizar memoria + gemini-sync. Regra critica de comportamento.
type: feedback
---

## Ao INICIAR cada conversa:
1. Ler o arquivo da ultima sessao (o mais recente `vanessa-sessao-*.md`)
2. Ler o ultimo relatorio de varredura de eventos (`~/Documents/claude/reports/event-scan-*.txt` — o mais recente)
3. Dar a Vanessa um resumo do contexto: o que fizemos na ultima sessao + se ha algo relevante no relatorio de eventos
4. Verificar se ha outros relatorios recentes relevantes

## Ao FINALIZAR cada conversa (ou bloco significativo de trabalho):
1. Atualizar/criar arquivo de sessao (`vanessa-sessao-YYYY-MM-DD.md`)
2. Atualizar MEMORY.md se houver informacoes novas relevantes
3. Atualizar `G:\Meu Drive\Claudio\gemini-sync.md` com o que aconteceu
4. Atualizar `claudio-context.md` no repo claudio-bot (memoria condensada pro Claud-IO Telegram)
5. Se houver backups pendentes, copiar para `G:\Meu Drive\backup-memoria-claude\`

**Why:** Vanessa quer continuidade total entre sessoes. Ela nao quer ter que re-explicar contexto. O Claudio precisa chegar "quente" em cada conversa, como se tivesse acabado de sair da anterior.

**How to apply:** Isso e automatico — nao perguntar se deve fazer, apenas fazer. No inicio, ler e resumir. No fim, salvar e sincronizar. Se a sessao for curta e sem novidades, nao precisa criar arquivo de sessao novo, mas o gemini-sync e a memoria sempre devem refletir o estado atual.
