# Arquitetura — Micro-frontends da MECHA IDE

O grid da IDE foi quebrado em **micro-frontends**: cada painel é um Design Component
próprio, editável de forma independente, composto pelo **shell** (`MECHA IDE.dc.html`).

## Shell × micro-frontends

```
MECHA IDE.dc.html  (shell)
├─ estado global + lógica (runs, modos, modelos, RAG, firewall…)
├─ title bar · activity bar · sidebar · status bar · overlays (⌘K, Mission Control…)
└─ monta os micro-frontends da região de conteúdo via <dc-import>, passando 1 view-model:
   ├─ MechaGraph.dc.html      vm = graphVM     (grafo: nós, arestas, drag, seleção)
   ├─ MechaChamados.dc.html   vm = chamadosVM  (kanban FreeScout)
   ├─ MechaClaw.dc.html       vm = clawVM      (loop See-Think-Act + telemetria)
   ├─ MechaInfra.dc.html      vm = infraVM     (topologia Local/VPS)
   └─ MechaTerminal.dc.html   vm = terminalVM  (Terminal/Log/Problems)
```

## Contrato (padrão "container/presentational")

- **O shell calcula** todos os dados e callbacks em `renderVals()` e os empacota num
  único objeto `vm` por painel (`graphVM`, `chamadosVM`, …).
- **O micro-frontend é presentational**: template-only (sem classe de lógica), lê de
  `{{ vm.* }}` e dispara os callbacks recebidos. Não guarda estado próprio.
- A montagem usa `style="position:absolute;inset:0"` (ou `height:100%` no terminal) +
  `hint-size="100%,100%"`, dentro do `<sc-if value="{{ isX }}">` do shell — só monta
  o painel ativo.

## Por que assim

- **Editável isoladamente**: dá pra abrir `MechaGraph.dc.html` e iterar só no grafo.
- **Baixo risco**: o estado continua centralizado no shell (fonte única de verdade);
  os filhos não duplicam lógica nem disputam estado.
- **Escala**: novos painéis entram como novos arquivos + 1 `vm` + 1 `<dc-import>`.

## Próximos candidatos a extrair
- **MechaAgents** (dock LEGION: runs, composer, timeline, diff) — maior e mais
  acoplado; extrair quando estabilizar o protocolo de props do composer.
- **MechaExplorer** (árvore + editor com realce) — depende de `tree`, `hlLines`,
  `tabs`; viável como `editorVM`.
