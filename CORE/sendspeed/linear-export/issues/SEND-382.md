# SEND-382 — Implementação da Top Bar

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | High |
| Responsável | — |
| Time | Sendspeed |
| Projeto | — |
| Labels | — |
| Parent | — |
| Criada | 2026-03-13T12:41:13.485Z por paulo.ribeiro@sendspeed.com |
| Iniciada | — |
| Concluída | 2026-06-22T17:16:39.587Z |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-382-implementacao-da-top-bar |
| URL | https://linear.app/sendspeed/issue/SEND-382/implementacao-da-top-bar |

## Descrição

## Descrição

Implementar a Top Bar como nova feature da plataforma. Atualmente não existe barra superior global. A Top Bar centraliza: busca, acesso rápido, notificações, idiomas e configurações de usuário.

> ⚠️ Pré-requisito para mover avatar e idiomas da sidebar para a Top Bar.

## Componentes

1. **Busca global** — encontrar segmentos, jornadas, componentes
2. **Botão de Ajuda** — Documentação, Sugestões, Dúvidas
3. **Botão de Histórico** — Último acesso e páginas recentes
4. **Botão de Notificações** — Alertas (feature em breve)
5. **Seletor de Idiomas** — movido da sidebar
6. **Avatar do usuário** — movido da sidebar, menu com config e logout

## Referências visuais

> **[Imagem 1 — transcrição]:** (header-bar.png) Screenshot de UI da barra superior (Top Bar) da plataforma UserIn. À esquerda, um campo de busca com placeholder "Buscar segmentos, jornadas, componentes..." e ícone de lupa. À direita, uma fileira de ícones/botões arredondados: ícone de ajuda (círculo com "!" / balão de informação), ícone de histórico (relógio com seta), ícone de notificações (sino), ícone de idioma/globo, e por fim um botão azul redondo com ícone de avatar de usuário (silhueta branca) seguido de um chevron/seta para baixo (menu do usuário).

> **[Imagem 2 — transcrição]:** (Property 12=open.png) Screenshot de UI do dropdown do botão de Ajuda, aberto. No topo há um ícone (balão de informação). O menu lista três itens, cada um com ícone à esquerda: (1) "Documentação UserIn" com subtítulo "Documentação UserIn" (ícone de livro/documento); (2) "Sugestões" com subtítulo "Envie ideias e melhorias" (ícone de lâmpada); (3) "Dúvidas" com subtítulo "Fale com nosso suporte" (ícone de balão de conversa).

> **[Imagem 3 — transcrição]:** (Property 1=open.png) Screenshot de UI do dropdown do botão de Histórico, aberto. No topo direito, ícone de relógio com seta (histórico). Seção "ÚLTIMO ACESSO" com um card azul destacado: ícone de jornadas/fluxo, texto "Jornadas - Construtor de fluxos", subtítulo "5 min atrás", com um chevron à direita. Abaixo, seção "PÁGINAS RECENTES" lista, cada item com ícone e o timestamp "5 min atrás" à direita: "Campanhas" (ícone de megafone), "Primeiros Passos" (ícone de foguete), "Segmentos" (ícone de etiqueta), "Componentes" (ícone de cubo/caixa), "Contatos" (ícone de crachá/contato), "Mini Games" (ícone de controle de videogame).

---

## 🎯 Priorização RICE — Score: 5.33 (#22 no To-do)

| Reach | Impact | Confidence | Effort | Score |
| -- | -- | -- | -- | -- |
| 10 | 1 (medium) | 80% | 1.5 meses | **5.33** |

**Justificativa:** Reach 10: todos os usuários da plataforma vão interagir com a Top Bar. Impacto medium (1): melhoria significativa de navegação e UX, mas não resolve nenhum bloqueio funcional. Confidence 80%: designs Figma prontos, escopo bem definido. Esforço 1.5 meses: busca global, histórico, ajuda, notificações, migração de avatar/idiomas.

## Histórico de status
- Backlog (backlog): 2026-03-13T12:41:13.485Z → 2026-03-20T12:47:32.681Z
- Refining (backlog): 2026-03-20T12:47:32.681Z → 2026-03-31T14:49:27.660Z
- To-do (unstarted): 2026-03-31T14:49:27.660Z → 2026-06-22T17:16:39.603Z
- Released (completed): 2026-06-22T17:16:39.603Z → atual

## Relações
—

## Anexos
—
