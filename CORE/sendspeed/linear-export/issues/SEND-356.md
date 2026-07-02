# SEND-356 — Atualização de Nomenclatura — Ajustes visuais de nomes em toda a plataforma

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | High |
| Responsável | paulo.ribeiro@sendspeed.com |
| Time | Sendspeed |
| Projeto | — |
| Labels | — |
| Parent | — |
| Criada | 2026-02-27T13:39:32.427Z por paulo.ribeiro@sendspeed.com |
| Iniciada | 2026-04-09T09:51:24.332Z |
| Concluída | 2026-05-08T18:07:58.952Z |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-356-atualizacao-de-nomenclatura-ajustes-visuais-de-nomes-em-toda |
| URL | https://linear.app/sendspeed/issue/SEND-356/atualizacao-de-nomenclatura-ajustes-visuais-de-nomes-em-toda-a |

## Descrição

## Descrição

Atualizar os textos exibidos na interface para nomes mais claros e alinhados com o vocabulário do usuário final. As alterações são exclusivamente visuais no front-end e não geram nenhum impacto em código, rotas ou estrutura técnica.

> ⚠️ As mudanças de nomenclatura devem ser aplicadas em **toda a plataforma** — sidebar, títulos de página, abas, breadcrumbs, botões e qualquer outro lugar onde o nome antigo apareça. O objetivo é garantir coerência total entre todos os pontos da interface.

---

## Itens a atualizar

### Menu lateral — itens pai

| Nome atual (front) | Novo nome (front) | Observação |
| -- | -- | -- |
| Visão Geral (segmentos) | Início | Atualmente dentro de Segmentos, passa a ser o menu inicial |
| — | Como Começar | Conteúdo da tela Início atual |
| Segmentos | Audiência | Renomear seção pai |
| Companion | Componentes | Renomear seção pai |
| Objetos | Modelagem de Dados | Renomear seção pai |
| — | Análise de Dados | Novo item — não clicável por enquanto (em breve) |
| Segurança | Validador de Premiação | Antes: Segurança > Validador de Usuários; não terá submenus |
| Setup Empresa | Setup da Empresa | Ajuste de nome |

### Subitens — Jornadas

| Nome atual (front) | Novo nome (front) | Observação |
| -- | -- | -- |
| Builder | Construtor de Fluxos |  |
| — | Regras | Entra como novo subitem de Jornadas |

### Subitens — Audiência

| Nome atual (front) | Novo nome (front) | Observação |
| -- | -- | -- |
| Tags | Segmentos |  |
| Usuários | Relatório de Usuários |  |
| Configurações | Parametrização de Audiência | Mover para Setup da Empresa |

### Subitens — Componentes

| Nome atual (front) | Novo nome (front) | Observação |
| -- | -- | -- |
| — | Cards | Ocultar por enquanto |
| — | Modais |  |
| — | Smart Blocks |  |
| — | Mini Games |  |
| — | Biblioteca |  |

### Subitens — Modelagem de Dados

| Nome atual (front) | Novo nome (front) | Observação |
| -- | -- | -- |
| Visão Geral | Painel de Ontologia |  |
| Grafo & Relações | Grafo & Relações | Manter nome atual |

### Subitens — Setup da Empresa

| Nome atual (front) | Novo nome (front) | Observação |
| -- | -- | -- |
| — | Setup Geral | Aqui, por enquanto vai tudo que está dentro de Setup da Empresa |
| Políticas | Regras Gerais | Movido de Regras > Políticas. Acesso restrito a admins |
| Configurações | Parametrização de Audiência | Movido de Audiência > Configurações |

### Configurações de usuário — fora da sidebar

| Nome atual (front) | Novo nome (front) | Observação |
| -- | -- | -- |
| Configurações (menu lateral que só está em DEV) | Config Usuário | Mover para dentro do avatar do usuário (barra top) por enquanto |

---

## Ordem final da sidebar

```
Início
Como Começar
Jornadas
  Construtor de Fluxos
  Analytics
  Templates
  Objetivos
  Métricas de Sucesso
  Regras
Campanhas
Disparos
  Analytics
  Alertas
Audiência
  Segmentos
  Relatório de Usuários
  Listas
  Contatos
Componentes
  Cards (oculto por enquanto)
  Modais
  Smart Blocks
  Mini Games
  Biblioteca
Modelagem de Dados
  Painel de Ontologia
  Grafo & Relações
Análise de Dados (em breve, não clicável)
Insights
Integrações
Validador de Premiação
Setup da Empresa
  Setup Geral
  Regras Gerais
  Parametrização de Audiência
```

---

## Referências visuais

### Sidebar atualizada (Figma)

> **[Imagem 1 — transcrição] (Main Sidebar.png):** Screenshot/Figma da sidebar completa da plataforma UserIn (logo "UserIn" no topo). Itens de menu, na ordem: **Início**; **Como Começar** (com seta ">"); **Jornadas** (expandido, seta "v") com subitens: Construtor de Fluxos, Analytics, Templates, Objetivos, Métricas de Sucesso, Regras; **Campanhas**; **Disparos** (expandido) com subitens Analytics, Alertas; **Audiência** (expandido) com Segmentos, Relatório de Usuários, Listas, Contatos; **Componentes** (expandido) com Cards, Modais, **Smart Blocks** (destacado/selecionado), Mini Games; **Modelagem de Dados** (expandido) com Painel de Ontologia, Grafo & Relações; **Análise de Dados**; **Insights**; **Integrações** (seta ">"); **Setup da Empresa** (expandido) com Setup Geral, Regras Gerais, Parametrização de Audiência. Confirma visualmente a nova nomenclatura e ordem.

### Tela de Configurações de Usuário — mover para o avatar

> **[Imagem 2 — transcrição] (screencapture ...settings...):** Screenshot da tela **"Configurações — Gerencie suas preferências e configurações da conta"**. Abas no topo: **Perfil** (ativa), Empresa, Permissões, API Keys, Notificações, Integrações, Aparência. Seção **"Informações pessoais"** com avatar circular "US", campos Nome = "Usuário", Sobrenome = "UserIn", E-mail = "usuario@userin.com", botões "Salvar alterações" e "Alterar foto". Seção **"Informações de contato"** com campos Endereço, Telefone, Empresa e "Salvar alterações". Início da seção "Configurações Avançadas" com card **"Treinar IA — Responda perguntas sobre sua empresa para personalizar os insights da IA"**. Sidebar à esquerda mostra a nomenclatura ANTIGA/em DEV: Como Começar (Em breve), Análise de Dados (Em breve), Dashboard, Modelagem de Dados, **Companion**, Jornadas, Audiência, Campanhas, Disparos, Integrações, Validador de Premiação, Insights, Setup Empresa; rodapé com conta "SendSpeed Ad... / SendSpeed" e seletor "PT".

### Avatar do usuário na barra top — destino das configurações

> **[Imagem 3 — transcrição] (image.png):** Screenshot/recorte do componente de **avatar do usuário** — um círculo azul com ícone de pessoa (usuário) e uma seta para baixo (chevron) ao lado, indicando um menu dropdown. É o destino proposto para onde as "Configurações de Usuário" devem ser movidas (dentro do avatar na barra superior).

---

## Observação importante

Não renomear rotas, componentes, variáveis ou qualquer estrutura técnica. Apenas os textos exibidos ao usuário devem ser modificados. A nomenclatura técnica permanece intacta em front e back-end.

---

## 🎯 Priorização RICE — Score: 8.0

| Reach | Impact | Confidence | Effort | Score |
| -- | -- | -- | -- | -- |
| 10 | 1 (medium) | 80% | 1 mês | **8.0** |

**Justificativa:** Reach 10: todos os usuários da plataforma vêem a sidebar e navegação. Impacto medium (1): nomenclatura mais clara reduz confusão e melhora onboarding, mas não resolve bugs. Confidence 80%: tabela de de/para completa e Figma pronto. Esforço 1 mês: muitos pontos para alterar (sidebar, títulos, breadcrumbs, botões) com coordenação cuidadosa para não quebrar rotas.

## Histórico de status
- Backlog (backlog): 2026-02-27T13:39:32.427Z → 2026-03-02T12:27:10.843Z
- To-do (unstarted): 2026-03-02T12:27:10.843Z → 2026-03-02T15:25:12.253Z
- Backlog (backlog): 2026-03-02T15:25:12.253Z → 2026-03-03T14:05:26.753Z
- To-do (unstarted): 2026-03-03T14:05:26.753Z → 2026-03-05T18:51:12.837Z
- In Progress (started): 2026-03-05T18:51:12.837Z → 2026-03-13T12:19:16.958Z
- Backlog (backlog): 2026-03-13T12:19:16.958Z → 2026-03-20T12:48:27.049Z
- Refining (backlog): 2026-03-20T12:48:27.049Z → 2026-03-31T14:49:21.498Z
- To-do (unstarted): 2026-03-31T14:49:21.498Z → 2026-04-09T09:51:24.348Z
- Pull Request (started): 2026-04-09T09:51:24.348Z → 2026-04-09T16:44:47.318Z
- Product Review (started): 2026-04-09T16:44:47.318Z → 2026-05-08T18:07:58.966Z
- Released (completed): 2026-05-08T18:07:58.966Z → atual

## Relações
—

## Anexos
- Fix/send 356 nomenclaturas — https://github.com/sendspeed0/sendspeed-engage-ai-flow-08/pull/38
