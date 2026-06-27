# Guia de Migracao de Memoria do Claude Code para Nova Maquina

## Contexto

A memoria do Claude Code fica em `~/.claude/projects/<slug-do-projeto>/memory/`.
O `<slug-do-projeto>` e gerado automaticamente a partir do caminho absoluto do projeto,
substituindo separadores por hifens. Exemplo:

- Caminho: `C:\Users\vanes\OneDrive\Documentos\claude`
- Slug: `C--Users-vanes-OneDrive-Documentos-claude`
- Memoria: `C:\Users\vanes\.claude\projects\C--Users-vanes-OneDrive-Documentos-claude\memory\`

## Passo a passo

### 1. Na maquina atual — exportar os arquivos

Copiar a pasta de memoria para um local acessivel (pendrive, OneDrive, etc.):

```bash
cp -r ~/.claude/projects/C--Users-vanes-OneDrive-Documentos-claude/memory/ /caminho/destino/backup-memoria-claude/
```

Arquivos a copiar:
- MEMORY.md
- vanessa-sessao-2026-03-05.md
- aprendizado-vanessa.md
- validacao-pipeline.md
- arquitetura-projeto.md
- migracao-maquina.md (este arquivo)

### 2. Na nova maquina — instalar e abrir o Claude Code

```bash
# Instalar Claude Code (se ainda nao tiver)
npm install -g @anthropic-ai/claude-code

# Criar/clonar o projeto no caminho desejado
# (idealmente o mesmo caminho para manter o slug igual)

# Abrir o Claude Code no diretorio do projeto
cd /caminho/do/projeto
claude
```

### 3. Descobrir o slug da nova maquina

Ao abrir o Claude Code pela primeira vez no projeto, ele cria a pasta automaticamente.
Para encontrar onde ficou:

```bash
# Listar as pastas de projeto do Claude Code
ls ~/.claude/projects/
```

Procurar a pasta que corresponde ao caminho do projeto na nova maquina.

### 4. Copiar os arquivos de memoria

```bash
# Substituir <slug-novo> pelo nome da pasta encontrada no passo 3
cp /caminho/destino/backup-memoria-claude/*.md ~/.claude/projects/<slug-novo>/memory/
```

### 5. Verificar

Abrir o Claude Code no projeto e perguntar algo que eu deveria saber
(ex: "como me chamo?" — resposta esperada: Claudio).

## Cenario ideal (sem copia manual)

Se na nova maquina o caminho do projeto for **identico** ao atual:

```
C:\Users\vanes\OneDrive\Documentos\claude
```

E a pasta `C:\Users\vanes\.claude\` for sincronizada pelo OneDrive ou copiada junto,
a memoria vai funcionar automaticamente sem nenhum passo extra.

## Dica

O arquivo `CLAUDE.md` na raiz do projeto (`C:\Users\vanes\OneDrive\Documentos\claude\CLAUDE.md`)
tambem e carregado automaticamente. Se o projeto estiver no OneDrive e sincronizar,
este arquivo ja estara disponivel na nova maquina.
