---
name: Sessao 2026-03-27
description: Sync memoria para Drive exclusivo, limpeza notebook corporativo, fix expire_on_commit cgm_etl_gdrive, config Google Drive Desktop resolveu shortcuts
type: project
---

# Sessao 2026-03-27 — Historico

## O que aconteceu nesta sessao

### 1. Sincronizacao de memoria (Drive <-> local)
- Puxadas 4 sessoes novas do Drive (24, 24-b, 25, 26, 26-b) + arquivos novos (etl memories, requisitos v1.1, feedback gdrive)
- Copiados 5 arquivos que so existiam no local pro Drive (feedback-credenciais, separacao-projetos, sessoes 16/17/18)
- Corrigido erro no MEMORY.md do backup: AlphaTM estava como "trabalho Prefeitura", corrigido para "projeto separado"
- 3 pontos alinhados: local, Claudio/memory, backup-memoria-claude (29 arquivos cada)

### 2. Migracao memoria para Google Drive exclusivo (CRITICO)
- Vanessa determinou: NUNCA persistir memorias no notebook corporativo
- Todos os 28 arquivos de conteudo removidos do local
- MEMORY.md local reescrito como indice fino (sem conteudo sensivel, so ponteiros)
- Fonte da verdade: `G:\Meu Drive\Claudio\memory\`
- Backup: `G:\Meu Drive\backup-memoria-claude\`
- Feedback gravado: feedback-memoria-somente-drive.md

### 3. Limpeza do notebook corporativo
- 29 arquivos de projetos removidos de ~/Documents/claude/ (temp_*, *_payload.json, *_b64.txt, gateway_*.py, etc.)
- Zero rastro de Claud-IO, Omega ou Alpha no notebook
- Sobrou apenas: CLAUDE.md, claudio-avatar.svg, codex-skills/, reports/, scripts/

### 4. Conta Claude Code verificada
- Logado na conta do Hugo (tsugamebashi@gmail.com), plano Max, via claude.ai
- Tudo certo

### 5. cgm_etl_gdrive — Fix expire_on_commit
- Projeto original em ~/Documents/gitana/cgm_etl_gdrive/
- Erro: `DetachedInstanceError` ao iterar cargas apos commit intermediario
- Causa: `expire_on_commit=True` (padrao do SQLAlchemy) invalidava objetos Carga apos commits de execucao
- Fix: adicionado `expire_on_commit=False` no `SessionLocal` em `database/db.py` (linha 47)
- Analogia SQL: manter resultado de SELECT em variavel local em vez de depender de cursor aberto

### 6. cgm_etl_gdrive — .venv vazia removida
- Projeto original tinha duas venvs: `.venv` (vazia) e `venv` (funcional)
- `.venv` removida, mantida apenas `venv` com todas as dependencias

### 7. cgm_etl_gdrive (ZIP) — Dependencias instaladas
- Projeto em ~/Documents/gitana/cgm_etl_gdrive-20260323T171103Z-1-001/
- `.venv` existia mas sem dependencias (criada sem pip install)
- Instalado requirements.txt completo na .venv

### 8. cgm_etl_gdrive — Problema de caminhos resolvido
- ETL nao encontrava planilhas apos migracao de maquina
- Causa: Google Drive Desktop nesta maquina precisava estar no modo que resolve shortcuts (.shortcut-targets-by-id)
- Vanessa ajustou a configuracao do Drive Desktop
- Projeto ZIP rodou 35 cargas com zero erros apos ajuste
- Projeto original ainda aponta para files/ sem Meu Drive/ (estrutura diferente)

### Pendencias
- [ ] Deploy Claud-IO na Oracle Cloud
- [ ] Implementacao v1.1 Claud-IO
- [ ] PIPE-003/005/006 Omega
- [ ] Clone dos repos Omega + /gsd:new-project
- [ ] Deadline M1 MVP Omega: 14/04/2026 (18 dias)
- [ ] Testar cgm_etl_gdrive v2 com banco
