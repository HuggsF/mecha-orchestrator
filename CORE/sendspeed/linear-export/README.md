# Exportação Linear — Workspace Sendspeed

Cópia local completa das tasks do Linear (time **Sendspeed**), gerada em **2026-07-01** para uso na IDE. Acesso somente-leitura ao Linear.

## Números

| Métrica | Valor |
| -- | -- |
| Total de issues exportadas | **317** |
| — Em andamento (started) | 3 |
| — A fazer (unstarted) | 33 |
| — Backlog | 11 |
| — Concluídas (completed/Released) | 270 |
| — Trilha/Canceladas | 0 |
| Documentos do workspace | 2 |
| Issues com imagens transcritas | 64 |

## Estrutura de pastas

```
linear-export/
├── README.md            (este arquivo)
├── INDEX.md             (índice legível de todas as issues, agrupado por status)
├── index.json           (índice em JSON, legível por máquina — metadados de todas as 317 issues)
├── issues/              (1 arquivo Markdown por issue: SEND-<n>.md)
│   ├── SEND-10.md
│   ├── SEND-11.md
│   └── ... (317 arquivos)
└── documents/           (documentos do workspace Linear)
    ├── Dicionario.md
    └── Teste.md
```

## O que cada arquivo de issue contém

Cada `issues/SEND-<n>.md` traz:

- Cabeçalho com o título da issue;
- Tabela de metadados: status, prioridade, responsável, time, projeto, labels, parent, datas (criada/iniciada/concluída/arquivada), vencimento, branch git e URL;
- **Descrição integral** (não truncada), preservando a formatação Markdown original (listas, tabelas, blocos de código, diagramas Mermaid/ASCII);
- **Histórico de status** (transições de estado com datas);
- **Relações** (blocking/related/duplicate), quando existentes;
- **Anexos** (links externos, ex.: PRs do GitHub), quando existentes.

## Imagens e anexos — como foram tratados

As imagens embutidas nas issues do Linear usam URLs **assinadas que expiram em poucos minutos** e a API só as devolve renderizadas (não como arquivo). Por isso **não foi possível baixar os arquivos de imagem**. Em vez disso, cada imagem foi **transcrita em texto** dentro da descrição, no ponto onde aparecia, em blocos:

> **[Imagem N — transcrição]:** descrição textual do que a imagem mostra (tipo, textos visíveis, elementos de UI, dados).

Anexos externos (PRs, docs do ClickUp, vídeos do Loom, arquivos `.md`/`.json` embutidos) foram **referenciados por link/título**, não baixados.

## Observações

- A numeração das issues tem lacunas (ex.: pula de SEND-19 para SEND-21) — normal, correspondem a issues excluídas ou de outros times. As 317 aqui são todas do time Sendspeed.
- **Comentários** das issues **não** foram incluídos nesta exportação (apenas descrições). Posso fazer uma passada adicional para incluí-los, se quiser.
- Fonte: workspace Linear da Sendspeed, via API somente-leitura.
