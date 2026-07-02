# SEND-448 — Consolidação de Canais - "Crie em um lugar, orquestre no Builder"

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | High |
| Responsável | paulo.ribeiro@sendspeed.com |
| Time | Sendspeed |
| Projeto | — |
| Labels | UserIn |
| Parent | — |
| Criada | 2026-04-10T11:28:44.286Z por paulo.ribeiro@sendspeed.com |
| Iniciada | 2026-04-13T14:31:23.175Z |
| Concluída | 2026-06-22T17:15:36.140Z |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-448-consolidacao-de-canais-crie-em-um-lugar-orquestre-no-builder |
| URL | https://linear.app/sendspeed/issue/SEND-448/consolidacao-de-canais-crie-em-um-lugar-orquestre-no-builder |

## Descrição

## **Descrição do Epic**

Estabelecer um padrão claro e consistente para criação e uso de conteúdo multicanal na plataforma: cada canal (RCS, SMS, Email) tem uma **tela dedicada de criação** dentro de Campanhas, e o **Construtor de Fluxos (Jornadas > Builder)** é o único ponto de orquestração, onde o usuário escolhe os templates já criados, visualiza o preview e configura as opções do envio.

O foco deste epic é garantir que o fluxo entre **criar um template** e **usá-lo numa jornada** seja simples, rápido e sem fricção.

**Fora do escopo deste epic:** disparo por lista fria (Campanhas > Todas as Campanhas). Listas frias poderão ser configuradas em Audiência > Listas, mas o fluxo de disparo direto por campanha não é prioridade agora.

**Princípio:** Cada canal tem UMA tela para criar conteúdo. O Construtor de Fluxos consome esses templates — nunca os recria.

---

## **User Stories**

---

### **US-01: Tela dedicada para RCS — Campanhas > RCS**

**Como** gestor de marketing, **Quero** ter em Campanhas > RCS o único lugar para criar, editar e publicar mensagens RCS, **Para que** eu saiba exatamente onde ir quando precisar montar ou ajustar uma mensagem RCS, sem encontrar editores em outros lugares da plataforma.

**Critérios de aceite:**

- [ ] A tela Campanhas > RCS é o único ponto de criação e edição de conteúdo RCS na plataforma
- [ ] O editor completo (wizard com etapas: configuração > editor side-by-side > revisão) está disponível aqui
- [ ] Suporte a todos os tipos: Texto, Cartão avançado, Carrossel, Arquivo
- [ ] Fluxo de publicação: rascunho → publicado
- [ ] Templates publicados ficam disponíveis para seleção no Construtor de Fluxos
- [ ] Estado vazio educativo para primeiro acesso ("Crie sua primeira mensagem RCS")
- [ ] Busca e filtros por tipo e status na listagem

**Prioridade:** Alta (já existe — refinar e consolidar como único ponto) **Arquivos principais:** `RcsPage.tsx`, `RcsEditorPage.tsx` **Entrega conjunta:** US-03 Fase 1 (remoção da aba RCS de Jornadas > Templates deve ser entregue junto para garantir que Campanhas > RCS seja de fato o único ponto de criação)

---

### **US-02: Nó "Enviar RCS" no Construtor de Fluxos — Seletor + Preview + Navegação**

**Como** gestor de marketing, **Quero** que ao configurar um nó "Enviar RCS" no Construtor de Fluxos eu possa selecionar um template publicado, visualizar o preview fiel e, se precisar ajustar o conteúdo, ir para a tela de edição e voltar facilmente, **Para que** eu monte minha jornada sem sair do contexto de criação e sem perder o trabalho que estava fazendo.

**Critérios de aceite:**

- [ ] O painel do nó "Enviar RCS" exibe: seletor de provedor RCS, seletor de template, preview fiel do celular (somente leitura), configuração de fallback SMS
- [ ] O editor de conteúdo embutido é removido do painel — edição acontece apenas em Campanhas > RCS
- [ ] O seletor de template exibe os templates RCS publicados com filtro por tipo (Todos | Texto | Cartão | Carrossel | Arquivo)
- [ ] O preview do celular reflete o conteúdo real do template selecionado
- [ ] Botão "Editar este template" abre Campanhas > RCS > editor do template selecionado, preservando o contexto da jornada
- [ ] Botão "Criar novo template" abre Campanhas > RCS > novo template, preservando o contexto da jornada
- [ ] Ao retornar da tela de edição/criação, o usuário volta para o Construtor de Fluxos na jornada que estava editando
- [ ] Estado vazio no seletor: se não há templates publicados, exibe CTA "Criar primeira mensagem RCS" com link para Campanhas > RCS
- [ ] O fallback SMS permanece como configuração exclusiva do nó (não do template)
- [ ] O painel lateral é redimensionado adequadamente sem o editor embutido

**Prioridade:** Alta **Arquivo principal:** `SendRcsConfig.tsx`

---

### **US-03: Migrar todas as abas de canal de Jornadas > Templates para suas telas dedicadas em Campanhas**

**Como** gestor de marketing, **Quero** que as abas RCS, SMS e Email sejam removidas de Jornadas > Templates conforme cada canal ganha sua tela dedicada em Campanhas, **Para que** Jornadas > Templates deixe de ser um lugar de criação de conteúdo de canal e se prepare para receber sua nova função: templates de jornadas completas.

**Contexto:** Hoje Jornadas > Templates agrupa abas de canais (RCS, SMS, Email) com permissões inconsistentes. Com cada canal ganhando sua tela dedicada em Campanhas, essas abas se tornam redundantes e devem ser removidas progressivamente. Ao final da migração, a seção "Templates" em Jornadas não é removida — ela é **reproposta** para abrigar templates de jornadas inteiras (fluxos reutilizáveis criados no Builder), que é uma funcionalidade futura planejada.

**Critérios de aceite — Fase 1 (junto com US-01):**

- [ ] A aba "RCS" é removida da tela Jornadas > Templates
- [ ] Acessar a URL antiga de templates RCS redireciona para Campanhas > RCS
- [ ] As rotas /templates/rcs/new e /templates/rcs/:id/edit são removidas
- [ ] A página RcsTemplateEditorPage é removida do projeto

**Critérios de aceite — Fase 2 (junto com US-04):**

- [ ] A aba "SMS" é removida da tela Jornadas > Templates
- [ ] Acessar a URL antiga de templates SMS redireciona para Campanhas > SMS

**Critérios de aceite — Fase 3 (junto com US-07):**

- [ ] A aba "Email" é removida da tela Jornadas > Templates
- [ ] Acessar a URL antiga de templates de email redireciona para Campanhas > Email
- [ ] A tela Jornadas > Templates fica vazia de conteúdo de canal, pronta para receber os Templates de Jornadas (US-11)

**Prioridade:** Média (executada progressivamente a cada fase) **Arquivos principais:** `TemplatesPage.tsx`, `App.tsx`

---

### **US-11: Transformar Jornadas > Templates em "Templates de Jornadas"**

**Como** gestor de marketing, **Quero** poder salvar uma jornada inteira como template reutilizável diretamente do Construtor de Fluxos, **Para que** eu possa criar jornadas recorrentes (ex: fluxo de boas-vindas, fluxo de reengajamento) sem precisar montá-las do zero toda vez.

**Contexto:** Após a migração de todas as abas de canal para Campanhas (US-03), a seção Jornadas > Templates é reproposta com uma nova função: deixa de ser um repositório de mensagens por canal e passa a ser um repositório de **fluxos de jornada completos** — estruturas de automação que podem ser salvas, duplicadas e usadas como ponto de partida para novas jornadas.

**Critérios de aceite:**

- [ ] No Construtor de Fluxos, existe a opção "Salvar como template de jornada"
- [ ] A tela Jornadas > Templates exibe os templates de jornadas salvos (não mais abas de canal)
- [ ] Cada template de jornada exibe: nome, descrição, canais utilizados, data de criação e um preview simplificado do fluxo
- [ ] Ao criar uma nova jornada, o usuário pode escolher "Começar do zero" ou "Usar um template de jornada"
- [ ] Ao usar um template, o fluxo é duplicado e aberto no Builder pronto para edição
- [ ] Templates de jornada podem ser editados, duplicados e excluídos
- [ ] A entrada "Templates" no menu de Jornadas aponta para esta nova tela

**Prioridade:** Baixa (fase futura — após conclusão das fases 1, 2 e 3) **Dependência:** US-03 completa (todas as abas de canal migradas)

---

### **US-04: Tela dedicada para SMS — Campanhas > SMS**

**Como** gestor de marketing, **Quero** ter em Campanhas > SMS o único lugar para criar, editar e publicar mensagens SMS, **Para que** eu tenha um ponto claro e organizado para montar meu conteúdo SMS, seguindo o mesmo padrão de Campanhas > RCS.

**Critérios de aceite:**

- [ ] Nova entrada no menu lateral: Campanhas > SMS
- [ ] Tela de listagem de templates SMS com busca, filtro por status (rascunho/publicado) e filtro por tipo
- [ ] Editor de mensagem SMS: campo de texto livre, inserção de variáveis Liquid, contagem de caracteres e segmentos, preview do celular em tempo real
- [ ] Fluxo de publicação: rascunho → publicado
- [ ] Templates publicados ficam disponíveis para seleção no nó "Enviar SMS" do Construtor de Fluxos
- [ ] Estado vazio educativo para primeiro acesso

**Prioridade:** Média **Referência de padrão:** Seguir a arquitetura estabelecida em Campanhas > RCS

---

### **US-05: Nó "Enviar SMS" no Construtor de Fluxos — Seletor + Preview + Navegação**

**Como** gestor de marketing, **Quero** que ao configurar um nó "Enviar SMS" no Construtor de Fluxos eu possa selecionar um template SMS publicado, visualizar o preview e navegar para edição sem perder o contexto da jornada, **Para que** o fluxo de montar uma jornada multicanal seja consistente independente do canal que estou configurando.

**Critérios de aceite:**

- [ ] O painel do nó "Enviar SMS" exibe: seletor de template, preview do celular com conteúdo real (somente leitura)
- [ ] O seletor lista apenas templates SMS publicados
- [ ] Botão "Editar este template" abre Campanhas > SMS > editor, preservando contexto da jornada
- [ ] Botão "Criar novo template" abre Campanhas > SMS > novo, preservando contexto da jornada
- [ ] Ao retornar, o usuário volta para o Construtor de Fluxos na jornada que estava editando
- [ ] Estado vazio: CTA "Criar primeira mensagem SMS" com link para Campanhas > SMS
- [ ] Editor embutido de SMS existente no painel é removido

**Prioridade:** Média **Dependência:** US-05

---

### **US-06: Tela dedicada para Email — Campanhas > Email**

**Como** gestor de marketing, **Quero** ter em Campanhas > Email o único lugar para criar, editar e publicar templates de email, **Para que** eu tenha um ponto centralizado para montar emails, seguindo o mesmo padrão dos outros canais.

**Critérios de aceite:**

- [ ] Nova entrada no menu lateral: Campanhas > Email
- [ ] Tela de listagem de templates de email com busca e filtros por status
- [ ] Editor de email (reutilizar o editor HTML/visual existente)
- [ ] Fluxo de publicação: rascunho → publicado
- [ ] Templates publicados ficam disponíveis para seleção no nó "Enviar Email" do Construtor de Fluxos
- [ ] Estado vazio educativo para primeiro acesso

**Prioridade:** Média **Referência de padrão:** Seguir a arquitetura estabelecida em Campanhas > RCS

---

### **US-07: Nó "Enviar Email" no Construtor de Fluxos — Seletor + Preview + Navegação**

**Como** gestor de marketing, **Quero** que ao configurar um nó "Enviar Email" no Construtor de Fluxos eu possa selecionar um template de email publicado, visualizar o preview e navegar para edição sem perder o contexto da jornada, **Para que** o fluxo de configuração de jornada seja idêntico para todos os canais.

**Critérios de aceite:**

- [ ] O painel do nó "Enviar Email" exibe: seletor de template, preview do email com conteúdo real (somente leitura)
- [ ] O seletor lista apenas templates de email publicados
- [ ] Botão "Editar este template" abre Campanhas > Email > editor, preservando contexto da jornada
- [ ] Botão "Criar novo template" abre Campanhas > Email > novo, preservando contexto da jornada
- [ ] Ao retornar, o usuário volta para o Construtor de Fluxos na jornada que estava editando
- [ ] Estado vazio: CTA "Criar primeiro template de email" com link para Campanhas > Email

**Prioridade:** Média **Dependência:** US-06

---

### **US-08: Limpeza de componentes técnicos**

**Como** desenvolvedor, **Quero** remover os componentes obsoletos que foram substituídos pelas novas telas e pelo novo padrão, **Para que** o código fique sem duplicações e mais fácil de manter.

**Critérios de aceite:**

- [ ] Preview simplificado de RCS (ChannelPreview) removido
- [ ] Wrapper do editor RCS em campanhas (RCSContentEditor) removido
- [ ] Editor de templates RCS antigo (RcsTemplateEditorPage) removido
- [ ] Rotas órfãs de /templates/rcs/\* removidas
- [ ] Build e testes passam sem erros após as remoções

**Prioridade:** Baixa (executar ao final de cada fase)

---

## **Ordem de execução**

```
Fase 1 — RCS
├── US-01: Consolidar Campanhas > RCS como único ponto de criação
├── US-02: Nó RCS no Construtor de Fluxos — seletor + preview + navegação
├── US-03: Remover aba RCS de Jornadas > Templates (critérios Fase 1)
└── US-08: Limpeza de componentes (parcial — RCS)

Fase 2 — SMS
├── US-04: Tela dedicada Campanhas > SMS
├── US-05: Nó SMS no Construtor de Fluxos — seletor + preview + navegação
└── US-03: Remover aba SMS de Jornadas > Templates (critérios Fase 2)

Fase 3 — Email
├── US-06: Tela dedicada Campanhas > Email
├── US-07: Nó Email no Construtor de Fluxos — seletor + preview + navegação
├── US-03: Remover aba Email de Jornadas > Templates (critérios Fase 3)
└── US-08: Limpeza de componentes (final)

Fase 4 — Templates de Jornadas (futura)
└── US-11: Transformar Jornadas > Templates em Templates de Jornadas (fluxos reutilizáveis do Builder)
```

---

## **Fluxo de navegação esperado no Construtor de Fluxos**

O ponto central deste epic é garantir que o usuário consiga ir e voltar entre o Construtor de Fluxos e as telas de edição de template sem fricção:

```
Construtor de Fluxos
  └── Clica no nó (ex: Enviar RCS)
        └── Painel lateral abre
              ├── Seleciona template publicado → preview aparece
              ├── "Criar novo template" → abre Campanhas > RCS > novo → salva/publica → volta ao Builder
              └── "Editar este template" → abre Campanhas > RCS > editor → salva → volta ao Builder
```

O retorno ao Builder deve sempre posicionar o usuário na jornada e no nó que estava configurando, sem perda de contexto.

## Histórico de status
- Backlog (backlog): 2026-04-10T11:28:44.286Z → 2026-04-13T14:31:23.187Z
- In Progress (started): 2026-04-13T14:31:23.187Z → 2026-04-15T11:41:03.788Z
- Pull Request (started): 2026-04-15T11:41:03.788Z → 2026-04-15T15:35:41.164Z
- In Progress (started): 2026-04-15T15:35:41.164Z → 2026-04-15T21:19:40.988Z
- Pull Request (started): 2026-04-15T21:19:40.988Z → 2026-04-15T22:38:20.408Z
- Product Review (started): 2026-04-15T22:38:20.408Z → 2026-06-22T17:15:36.155Z
- Released (completed): 2026-06-22T17:15:36.155Z → atual

## Relações
—

## Anexos
- Fix/send 448 consolidacao de canais — https://github.com/sendspeed0/sendspeed-engage-ai-flow-08/pull/41
