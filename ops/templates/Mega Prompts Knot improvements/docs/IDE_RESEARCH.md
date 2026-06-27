# Deep Research — IDEs líderes & 100 ciclos de melhoria

> Benchmark: **Cursor 3 ("Glass" / Agents Window)**, **Zed** (agentic, parallel agents,
> tool-call transparency, multibuffer), **VS Code** (extensões, command palette, diff).
> Objetivo: adaptar os padrões 2026 ao **MECHA IDE** sem copiar 1:1 — manter identidade
> LEGION/MECHA (Squads nomeados, See-Think-Act, RAG Qdrant+Neo4j).

## Padrões extraídos (o que os líderes fazem)
1. **Agents Window** — agentes são objetos de 1ª classe; rodam **em paralelo**; troca rápida como abas de terminal.
2. **Mission Control** — grid (estilo Exposé) com todos os runs e seus status.
3. **Plan first / autonomia graduada** — Ask → Plan → Agent → Auto.
4. **Transparência de tool-calls** — o run mostra cada passo (read/search/edit/run) ao vivo.
5. **Diff review editável** — aceitar/rejeitar tudo antes de aplicar.
6. **Model-as-infra** — escolher o modelo por run.
7. **Contexto explícito** — `@` arquivos/símbolos, `/` skills, regras por glob.
8. **Background agents** — notificação ao terminar.
9. **Review como gargalo** — passe de auditoria (BugBot) com contagem de issues.

---

## 100 ciclos (checklist de execução)

### Wave 1 · Agents Window (runs paralelos) — 1–14
1. Modelo de dados `runs[]` (id, título, modo, modelo, status, mensagens)
2. `activeRun` + criação de run (+)
3. Run-switcher (pills) no header do dock
4. Status por run: idle / running / review / done
5. Cor/ícone por status
6. Renomear run a partir do 1º prompt
7. Fechar run
8. Persistir runs na sessão
9. Contador de runs no ícone 🦾 da activity bar
10. Run vazio mostra empty-state próprio
11. Histórico por run (mensagens isoladas)
12. Indicador "N rodando" no header
13. Atalho novo run (⌘⇧.)
14. Scroll independente por run

### Wave 2 · Mission Control — 15–24
15. Overlay grid de todos os runs (⌃G)
16. Card por run: título, modo, modelo, status, última msg
17. Clique foca o run (fecha overlay)
18. Realce do run ativo
19. Botão novo run no grid
20. Vazio → call-to-action
21. Fechar com Esc / clique fora
22. Badge de status colorido por card
23. Contagem total no cabeçalho do overlay
24. Entrada via ⌘K e via header

### Wave 3 · Model picker — 25–34
25. Catálogo de modelos (OpenRouter): Sonnet, Opus, GPT-4o, Gemini, Kimi, Llama local
26. Seletor no composer
27. Modelo por run (persistente)
28. Tag do modelo no card do Mission Control
29. Custo relativo (¢) por modelo
30. Badge "local" p/ Ollama
31. Default por modo (Plan→Opus, Ask→Sonnet…)
32. Trocar modelo no meio do run
33. Modelo no rodapé da mensagem do assistant
34. Aviso se modelo exige chave ausente

### Wave 4 · Tool-call timeline — 35–48
35. Sequência de passos ao enviar (read/grep/edit/run)
36. Ícone + label por tipo de passo
37. Estado por passo: pending → running → done
38. Alvo do passo (arquivo/comando)
39. Animação de progresso
40. Colapsar/expandir a timeline
41. Duração simulada por passo
42. Passo de RAG ("rag_client.search → k=3")
43. Passo de firewall (aprovação)
44. Resumo "N tools · Xs"
45. Timeline some quando termina (vira resumo clicável)
46. Erro simulado ocasional + retry
47. Passo grava status atômico
48. Timeline por run isolada

### Wave 5 · Diff review — 49–60
49. Card de diff unificado no modo Agent
50. Linhas +/− coloridas (monocromático)
51. Cabeçalho com arquivo
52. Accept / Reject (tudo)
53. Estado aplicado/descartado
54. Contagem +N −M
55. Múltiplos arquivos no mesmo diff
56. Colapsar diff
57. Copiar diff
58. "Revisar no editor" abre o arquivo
59. Reviewer (Mitnick/Warlock) com issues
60. Selo [APROVADO]/[REJEITADO]

### Wave 6 · Contexto & comandos — 61–72
61. `@` abre picker de arquivos/símbolos
62. Pills de contexto anexado
63. Remover pill
64. `/` skills (já há hint) → executa skill
65. Regras `.mecha/rules/` na árvore
66. Indicador de regras ativas
67. Pin de skill
68. Histórico de prompts (↑)
69. Anexar arquivo atual com 1 clique
70. Contexto do nó do grafo → run
71. Contexto de chamado → run
72. Slash `/rag` busca conhecimento

### Wave 7 · Polish multi-tela — 73–100
73. Densidade consistente (8px grid)
74. Hover states em todos os clicáveis
75. Focus ring acessível
76. Empty-states ilustrados por tela
77. Skeleton/placeholder de carregamento
78. Tooltips nos ícones
79. aria-label nos botões-ícone
80. Contraste AA no texto secundário
81. Scrollbars finas consistentes
82. Breadcrumb clicável navega
83. Atalhos visíveis no overlay (?)
84. Toast com fila
85. Estado vazio do grafo
86. Kanban: contador por coluna
87. Infra: legenda Local/VPS fixa
88. Status bar: modelo ativo + run ativo
89. Title bar: nome do run ativo
90. Persistir largura do dock (feito) + min/max
91. Animações de transição suaves
92. Reduzir motion se prefers-reduced-motion
93. Estados de erro honestos (demo/real)
94. Microcopy revisada PT-BR
95. Ícones consistentes (sem emoji solto onde não cabe)
96. Consistência de raios (8–12px)
97. Sombh/elevação por camada
98. Teclado: Tab order lógico
99. Mobile/narrow: dock vira overlay
100. Auditoria final de todas as telas + screenshot

> Execução: waves 1–5 = features novas; wave 6 = contexto; wave 7 = qualidade transversal.
> Cada item marcado conforme implementado no `MECHA IDE.dc.html`.
