# MECHA Squad Rules (Local Lore)

## 1. Fail First (Let it Fail)
- Proibição ESTRITA de usar blocos `try/except` que silenciem falhas (`pass`).
- Se houver falha na infraestrutura ou API, levante a exceção (`raise ValueError`, etc) para que o Orquestrador ou testes percebam imediatamente a ruptura.

## 2. Trash Dump
- Arquivos temporários, scripts de teste descartáveis ou código depreciado NUNCA devem poluir a raiz ou pastas de produção.
- Grave-os exclusivamente em diretórios como `_archive/` ou `scratch/`.

## 3. Consulta Determinística Obrigatória (RAG-First)
- Antes de refatorar ou propor arquiteturas complexas neste repositório, o Agente DEVE consumir a ontologia local ou acionar a skill de RAG do projeto pai. Não adivinhe código.
