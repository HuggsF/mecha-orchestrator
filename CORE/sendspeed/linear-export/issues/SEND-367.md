# SEND-367 — EPIC - Equipe & Permissões

| Campo | Valor |
| -- | -- |
| Status | Backlog (backlog) |
| Prioridade | No priority |
| Responsável | — |
| Time | Sendspeed |
| Projeto | — |
| Labels | Implementação |
| Parent | — |
| Criada | 2026-03-06T12:24:21.861Z por paulo.ribeiro@sendspeed.com |
| Iniciada | — |
| Concluída | — |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-367-epic-equipe-permissoes |
| URL | https://linear.app/sendspeed/issue/SEND-367/epic-equipe-and-permissoes |

## Descrição

## **Glossário de Roles**

| UI Label | Backend Role | Nível | Acesso padrão |
| -- | -- | -- | -- |
| **Gestor** | `owner` | 1 | Total. Único, irremovível. |
| **Administrador** | `admin` | 2 | Total. Pode gerenciar membros. |
| **Membro** | `manager` / `employee` / `viewer` | 3 | Configurável por área (view/edit/nenhum). Sem acesso a Setup Empresa. |

> Os roles `manager`, `employee` e `viewer` do backend são tratados como "Membro" na UI. A distinção entre eles é feita via permissões granulares por área, não por role label.

## **Áreas da Plataforma e Semântica de Permissões (11 áreas)**

| Área | `view` (visualizar) | `edit` (editar) | Nota |
| -- | -- | -- | -- |
| Início | Página inicial | — | Sempre view-only |
| Segmentos | Lista, detalhes, filtros, tags | Criar/editar segmentos, regras, tags |  |
| Objetos | Grafo, detalhes de atributos | Criar/editar atributos, relações, instâncias |  |
| Regras | Lista de regras e políticas | Criar, editar, clonar regras |  |
| Dados e Integrações | Integrações ativas | Configurar, ativar, desativar |  |
| Companion | Componentes e biblioteca | Criar/editar cards, modais |  |
| Jornadas | Lista, analytics, templates | Criar/editar jornadas no builder |  |
| Audiência | Listas e contatos | Importar, criar listas, editar contatos |  |
| Integrações | Conectores ativos | Configurar, ativar |  |
| Segurança | Validador de usuários | Executar validações |  |
| Insights | Relatórios e sugestões | — | Sempre view-only |

> **Setup Empresa** é exclusiva de Gestor/Admin — não aparece no grid de permissões de membros.

## **US-01: Gestor Convida Novo Membro**

### **Descrição**

Como **Gestor**, quero convidar um usuário por email para que ele acesse a plataforma com permissões controladas.

### **Ator principal**

Gestor (role `owner`)

### **Pré-condições**

* O Gestor está autenticado e na seção **Setup Empresa > Equipe** (aba "Membros").
* O email do convidado ainda não está cadastrado no workspace.

### **Fluxo de Tela (passo a passo)**

```
┌─────────────────────────────────────────────────────────────┐
│  Setup Empresa > Equipe > Aba "Membros"                     │
│                                                             │
│  ┌──────────────────────┐                                   │
│  │ [+ Convidar Membro]  │  ← Botão primário (canto sup.)   │
│  └──────────────────────┘                                   │
│                 │                                           │
│                 ▼                                           │
│  ┌─────────────────────────────────────────────────┐        │
│  │          Modal / Drawer de Convite               │        │
│  │                                                   │        │
│  │  Nome*:       [_________________________]         │        │
│  │  Email*:      [_________________________]         │        │
│  │  Nível:       (•) Admin  ( ) Membro               │        │
│  │  Label:       [ex: Analista de CRM    ] (opc.)    │        │
│  │                                                   │        │
│  │  ── Se "Membro" selecionado ──                    │        │
│  │  Perfil de permissões:                            │        │
│  │    ( ) Template: Analista (view em tudo)           │        │
│  │    ( ) Template: Editor de Jornadas                │        │
│  │    ( ) Template: Operador CRM                     │        │
│  │    (•) Configurar manualmente                     │        │
│  │                                                   │        │
│  │  ── Grid de áreas (se manual) ──                  │        │
│  │  [Grid idêntico à aba Controle de Acesso]         │        │
│  │                                                   │        │
│  │  [Cancelar]            [Enviar Convite]           │        │
│  └─────────────────────────────────────────────────┘        │
│                 │                                           │
│                 ▼                                           │
│  Toast: "Convite enviado para joao@empresa.com"             │
│  Lista de membros atualiza: novo membro com badge "Pendente"│
└─────────────────────────────────────────────────────────────┘
```

1. Gestor clica em **"Convidar Membro"**.
2. Abre modal/drawer com campos: Nome, Email, Nível (Admin / Membro), Label opcional.
3. Se nível = **Admin**: nenhuma configuração de permissão necessária (admin tem acesso total).
4. Se nível = **Membro**: exibir seleção de template de permissão OU opção de configuração manual.
   * Templates pré-definidos: "Analista (view em tudo)", "Editor de Jornadas (edit em companion/jornadas)", "Operador CRM (edit em segmentos/audiência/regras)".
   * Configuração manual: grid de áreas com toggles view/edit (mesmo grid da aba "Controle de Acesso").
5. Gestor clica em **"Enviar Convite"**.
6. Sistema envia email com link de ativação.
7. Membro aparece na lista com status **"Pendente"** e badge amarelo.

### **Critérios de Aceitação**

| # | Critério | Verificação |
| -- | -- | -- |
| 01 | O botão "Convidar Membro" só é visível para Gestor e Admin | Renderização condicional |
| 02 | O campo "Email" valida formato de email antes de submeter | Validação client-side |
| 03 | Se o email já pertence a um membro do workspace, exibir erro inline: "Este email já está na equipe" | Validação com API |
| 04 | Se nível = Admin, a seção de permissões granulares NÃO aparece | Condicional no form |
| 05 | Se nível = Membro, ao menos uma área deve ter `view: true` antes de submeter | Validação client-side |
| 06 | Após submissão bem-sucedida, o novo membro aparece na lista com badge "Pendente" | Atualização da lista |
| 07 | Toast de sucesso aparece com o email do convidado | Feedback visual |
| 08 | Admin pode convidar apenas Membros (opção "Admin" oculta quando o ator é Admin) | Lógica de role |
| 09 | O campo Label é opcional e aceita até 50 caracteres | Validação |
| 10 | O modal fecha automaticamente após sucesso | UX flow |

### **Exceções e Edge Cases**

* **Email inválido:** Erro inline no campo, botão "Enviar" desabilitado.
* **Limite de membros atingido (se houver):** Erro no toast: "Limite de membros do plano atingido".
* **Erro de rede:** Toast de erro genérico com botão "Tentar novamente".
* **Admin tentando convidar outro Admin:** A opção "Admin" não aparece no seletor de nível.

### **Referências de Código**

* Tipo `CreateSubUserRequest` em `subUsers.ts` (campos: name, email, role)
* API `subUsersApi.ts` para chamada de criação
* `TeamSection.tsx` no ux-lab: botão "Convidar Membro" já existe (sem funcionalidade)

---

## **US-02: Membro Aceita Convite e Faz Primeiro Acesso**

### **Descrição**

Como **usuário convidado**, quero acessar a plataforma e ver apenas o que me foi permitido para que eu não fique confuso com funcionalidades inacessíveis.

### **Ator principal**

Novo membro (qualquer role de "Membro")

### **Pré-condições**

* O membro recebeu um email de convite com link de ativação.
* O convite ainda não expirou.

### **Fluxo de Tela (passo a passo)**

```
┌──────────────────────────────────────────────────────────────┐
│  Email recebido                                              │
│  "Você foi convidado para [NomeEmpresa] na UserIn"           │
│  [Aceitar Convite →]                                         │
│       │                                                      │
│       ▼                                                      │
│  Página de Ativação (/invite/:token)                         │
│  ┌────────────────────────────────────────┐                  │
│  │  "Bem-vindo à UserIn!"                 │                  │
│  │  Defina sua senha de acesso            │                  │
│  │                                        │                  │
│  │  Senha*:          [__________]         │                  │
│  │  Confirmar senha*:[__________]         │                  │
│  │                                        │                  │
│  │  [Ativar Conta e Entrar]               │                  │
│  └────────────────────────────────────────┘                  │
│       │                                                      │
│       ▼                                                      │
│  Redirect automático para login / sessão iniciada            │
│       │                                                      │
│       ▼                                                      │
│  Sidebar filtrada: APENAS menus com permissão view ou edit   │
│  Redirect para o primeiro menu disponível (não para "/")     │
│                                                              │
│  Exemplo (membro com acesso a Segmentos + Jornadas):         │
│  ┌────────────┐  ┌───────────────────────────┐               │
│  │ Sidebar    │  │  Segmentos (primeiro menu) │               │
│  │            │  │  [lista e detalhes]        │               │
│  │ Segmentos  │  │                            │               │
│  │ Jornadas   │  │                            │               │
│  │            │  │                            │               │
│  │ (só isso)  │  │                            │               │
│  └────────────┘  └───────────────────────────┘               │
└──────────────────────────────────────────────────────────────┘
```

1. Membro clica em "Aceitar Convite" no email.
2. Abre página `/invite/:token` com formulário de criação de senha.
3. Membro preenche senha e confirmação.
4. Clica em "Ativar Conta e Entrar".
5. Sistema cria a senha, ativa a conta e inicia sessão automaticamente.
6. Redirect para o **primeiro menu permitido** do membro (baseado nas permissões definidas pelo Gestor).
7. A sidebar exibe **apenas** os menus onde o membro tem `view: true` ou `edit: true`.

### **Critérios de Aceitação**

| # | Critério | Verificação |
| -- | -- | -- |
| 01 | Link do email redireciona para `/invite/:token` | Rota funcional |
| 02 | Se o token é inválido ou expirado, exibe mensagem de erro com link para solicitar novo convite | Tratamento de erro |
| 03 | Senha requer mínimo de 8 caracteres, ao menos 1 maiúscula e 1 número | Validação client-side |
| 04 | Após ativação, sessão é iniciada automaticamente (sem necessidade de login manual) | Auth flow |
| 05 | A sidebar mostra **apenas** menus com permissão `view` ou `edit` | `isMenuEnabled` + filtro |
| 06 | Menus sem nenhuma permissão ficam **completamente ocultos** (não desabilitados) | Não-renderização |
| 07 | O redirect pós-login vai para o **primeiro menu disponível**, não para `/` | Lógica de redirect |
| 08 | Se o membro não tem permissão em "Início", o redirect ignora `/` e vai para o próximo menu | Fallback inteligente |
| 09 | O status do membro na lista muda de "Pendente" para "Ativo" após ativação | Atualização de estado |
| 10 | A data de "último acesso" é registrada | Timestamp |

### **Exceções e Edge Cases**

* **Token expirado:** Página de erro com "Convite expirado. Solicite ao gestor um novo convite."
* **Token já utilizado:** Redirect para login com mensagem "Sua conta já foi ativada."
* **Membro sem nenhuma permissão:** Tela especial: "Você ainda não tem acesso a nenhuma área. Entre em contato com seu gestor." (sem sidebar).
* **Senhas não coincidem:** Erro inline abaixo do campo de confirmação.

### **Referências de Código**

* `ProtectedMenuRoute.tsx`: já faz redirect se menu desabilitado (ajustar fallback para primeiro menu permitido)
* `MenuPermissionsContext.tsx`: `isMenuEnabled()` já controla visibilidade
* `Sidebar.tsx`: já usa `permissions.isMenuEnabled(menuKey)` para filtrar menus

---

## **US-03: Membro Navega com Permissão de "Visualização"**

### **Descrição**

Como **membro com permissão de visualização** em qualquer área da plataforma, quero ver os dados sem poder modificar nada, para que eu possa monitorar sem risco de alterações acidentais.

### **Ator principal**

Membro com `view: true, edit: false` em uma área específica

> Este padrão se aplica a **todas as 11 áreas** e suas sub-páginas (ex: Segmentos tem Visão Geral, Usuários, Configurações, Tags). Não é uma tela específica — é um comportamento que cada área deve implementar.

### **Pré-condições**

* O membro está autenticado e tem permissão `view` (mas não `edit`) na área em questão.

### **Comportamento esperado (padrão para todas as áreas)**

1. Membro acessa a área via sidebar.
2. Dados carregam normalmente (listas, gráficos, detalhes, sub-páginas).
3. Botões de ação (Criar, Editar, Deletar) ficam **ocultos** — simplesmente não renderizados.
4. Colunas de "Ações" nas tabelas não existem para este usuário.
5. O membro pode navegar entre sub-páginas e clicar em itens para ver detalhes.
6. Nas páginas de detalhe, campos aparecem em **read-only** (inputs desabilitados ou texto estático).
7. Não há botões de "Salvar", "Editar" ou "Deletar".

### **Critérios de Aceitação**

| # | Critério | Verificação |
| -- | -- | -- |
| 01 | Menu da área aparece na sidebar (membro tem `view`) | Sidebar filter |
| 02 | Botões de criação (ex: "Criar Segmento") não são renderizados | Renderização condicional |
| 03 | Coluna "Ações" ou ícones de ação por linha não são renderizados | Renderização condicional |
| 04 | DropdownMenu de ações por item não é renderizado | Renderização condicional |
| 05 | Tabelas e gráficos exibem dados normalmente | Funcionalidade mantida |
| 06 | O membro pode clicar em uma linha para ver detalhes | Navegação funcional |
| 07 | Na página de detalhes, campos de formulário ficam em estado **read-only** | `readOnly` prop |
| 08 | Botões "Salvar", "Editar", "Deletar" não são renderizados nos detalhes | Renderização condicional |
| 09 | Nenhum tooltip "Sem permissão" é exibido — os elementos simplesmente não existem | Princípio "ocultar" |
| 10 | A URL de criação (ex: `/segments/create`) redireciona para a listagem se o membro só tem `view` | ProtectedMenuRoute |
| 11 | A URL de edição redireciona para o detalhe read-only se o membro só tem `view` | ProtectedMenuRoute |
| 12 | A experiência visual é "limpa" — parece uma interface completa dentro do escopo permitido | Revisão UX |

### **Componente Auxiliar Proposto**

```
interface PermissionGateProps {
  area: string;
  level: 'view' | 'edit';
  children: React.ReactNode;
  fallback?: React.ReactNode;
}

function PermissionGate({ area, level, children, fallback = null }: PermissionGateProps) {
  const { hasPermission } = useAreaPermissions();
  if (!hasPermission(area, level)) return <>{fallback}</>;
  return <>{children}</>;
}

// Uso:
<PermissionGate area="segmentos" level="edit">
  <Button>Criar Segmento</Button>
</PermissionGate>
```

### **Referências de Código**

* `Sidebar.tsx`: filtra menus via `permissions.isMenuEnabled()`
* `ProtectedMenuRoute.tsx`: redireciona acesso direto a URLs protegidas

---

## **US-04: Membro Navega com Permissão de "Edição"**

### **Descrição**

Como **membro com permissão de edição** em qualquer área da plataforma, quero criar, editar e gerenciar itens dessa área para que eu possa operar minha responsabilidade de forma autônoma.

### **Ator principal**

Membro com `view: true, edit: true` em uma área específica

> Este padrão se aplica a **todas as 11 áreas** e suas sub-páginas. A experiência é **idêntica à de um Admin** naquela área específica.

### **Pré-condições**

* O membro está autenticado e tem permissão `edit` na área em questão.

### **Comportamento esperado (padrão para todas as áreas)**

1. Membro acessa a área via sidebar.
2. Interface completa em todas as sub-páginas: botões de criação visíveis, colunas de ações presentes, formulários editáveis.
3. Pode criar novos itens, editar existentes e deletar.
4. A experiência é **idêntica à de um Admin** naquela área específica.

### **Critérios de Aceitação**

| # | Critério | Verificação |
| -- | -- | -- |
| 01 | Menu da área aparece na sidebar | Sidebar filter |
| 02 | Botões de criação (ex: "Criar Segmento") são renderizados e funcionais | Funcionalidade |
| 03 | Coluna "Ações" e DropdownMenu por item estão presentes | Renderização |
| 04 | O membro pode acessar rotas de criação (ex: `/segments/create`) e criar um item | Navegação + API |
| 05 | O membro pode acessar rotas de edição e salvar alterações | Navegação + API |
| 06 | A experiência é idêntica à de um Admin na mesma área | Paridade funcional |
| 07 | O membro NÃO pode acessar outras áreas onde não tem permissão (sidebar oculta, rotas protegidas) | Isolamento |
| 08 | Ações de delete exibem dialog de confirmação normalmente | UX consistente |

### **Exceções e Edge Cases**

* **Membro com** `edit` em Jornadas mas sem `edit` em Segmentos: No builder de jornadas, o seletor de segmentos funciona em modo read-only (pode selecionar segmentos existentes, não criar novos).
* **Conflito de área dependente:** Se uma ação em uma área requer acesso a outra área (ex: seleção de template no Companion), exibir itens existentes em modo read-only.

---

## **US-05: Membro Tenta Acessar URL Restrita Diretamente**

### **Descrição**

Como **membro sem permissão** em uma área (ex: Regras), se eu digitar `/regras` na URL, devo ser redirecionado para minha página inicial para que eu não veja uma tela de erro ou conteúdo proibido.

### **Ator principal**

Membro sem permissão (`view: false, edit: false`) na área em questão

### **Pré-condições**

* O membro está autenticado.
* O membro não tem nenhuma permissão (nem view) na área cuja URL digitou manualmente.

### **Fluxo de Tela (passo a passo)**

```
┌──────────────────────────────────────────────────────────────┐
│  Barra de endereço: /regras                                  │
│       │                                                      │
│       ▼                                                      │
│  ProtectedMenuRoute verifica:                                │
│    isMenuEnabled("regras") → false                           │
│       │                                                      │
│       ▼                                                      │
│  Redirect para → primeiro menu disponível do membro          │
│  (NÃO para "/" se o membro não tem permissão de "Início")    │
│       │                                                      │
│       ▼                                                      │
│  Toast discreto (topo da página, desaparece em 4s):          │
│  ┌─────────────────────────────────────────────────┐         │
│  │ ⓘ  Você não tem acesso a essa área              │         │
│  └─────────────────────────────────────────────────┘         │
│                                                              │
│  Página do primeiro menu permitido carrega normalmente       │
└──────────────────────────────────────────────────────────────┘
```

1. Membro digita manualmente uma URL de área restrita (ex: `/regras`).
2. `ProtectedMenuRoute` intercepta e verifica `isMenuEnabled("regras")`.
3. Permissão retorna `false`.
4. Redirect para o **primeiro menu disponível** do membro.
5. Toast discreto aparece: "Você não tem acesso a essa área" (desaparece em 4 segundos).

### **Critérios de Aceitação**

| # | Critério | Verificação |
| -- | -- | -- |
| 01 | `ProtectedMenuRoute` intercepta a rota antes de renderizar qualquer conteúdo | Guard funcional |
| 02 | Redirect vai para o **primeiro menu disponível** do membro, não para `/` | Lógica de fallback |
| 03 | Toast discreto "Você não tem acesso a essa área" aparece no destino | Feedback visual |
| 04 | O toast desaparece automaticamente em 4 segundos | Timer |
| 05 | Nenhum conteúdo da área restrita é renderizado momentaneamente (sem flash) | Ordem de guards |
| 06 | O redirect funciona para URLs profundas também (ex: `/regras/123/edit`) | Cobertura de rotas |
| 07 | O comportamento é idêntico para navegação via browser back/forward | History handling |
| 08 | Se o membro não tem acesso a NENHUMA área, redireciona para tela de "Sem acesso" | Edge case |

### **Alteração Necessária no Código Existente**

O `ProtectedMenuRoute.tsx` atual redireciona para `fallbackPath = '/'`. Precisa ser ajustado para calcular o primeiro menu disponível:

```
// Proposta de ajuste no ProtectedMenuRoute
const getFirstAvailableMenu = (permissions: MenuPermissionsContextType): string => {
  const menuOrder = ['inicio', 'segmentos', 'objetos', 'regras', /* ... */];
  for (const menu of menuOrder) {
    if (permissions.isMenuEnabled(menu)) {
      return MENU_TO_PATH[menu]; // ex: 'inicio' → '/', 'segmentos' → '/segments'
    }
  }
  return '/no-access';
};
```

### **Referências de Código**

* `ProtectedMenuRoute.tsx` (linhas 18-69): lógica de redirect atual usa `fallbackPath = '/'`

---

## **US-06: Admin Gerencia Permissões de um Membro**

### **Descrição**

Como **Administrador**, quero ajustar as permissões de um membro existente para que eu possa expandir ou restringir seu acesso conforme a necessidade do negócio.

### **Ator principal**

Administrador (role `admin`) ou Gestor (role `owner`)

### **Pré-condições**

* O ator está autenticado e na seção **Setup Empresa > Equipe**.
* O membro-alvo existe e tem role "Membro" (não é Gestor nem Admin).

### **Fluxo de Tela (passo a passo)**

```
┌──────────────────────────────────────────────────────────────┐
│  Setup Empresa > Equipe > Aba "Membros"                      │
│                                                              │
│  Lista de membros:                                           │
│  ┌────────────────────────────────────────────────────┐      │
│  │ JO  João Oliveira   Membro  Analista CRM  5/17 ⋯  │      │
│  └────────────────────────────────────────────────────┘      │
│       │  Clica no membro (ou no "⋯")                         │
│       ▼                                                      │
│  Painel lateral / Drawer do membro:                          │
│  ┌─────────────────────────────────────────────────┐         │
│  │  João Oliveira                                   │         │
│  │  joao@empresa.com · Membro · Analista de CRM    │         │
│  │                                                  │         │
│  │  [Dados]  [Controle de Acesso]  [Histórico]      │         │
│  │            ───────────────────                    │         │
│  │                                                  │         │
│  │  Ações rápidas:                                  │         │
│  │  [Selecionar tudo (view)]  [Limpar tudo]         │         │
│  │  [Copiar permissões de...]  [Aplicar template]   │         │
│  │                                                  │         │
│  │  ┌─────────────────────────────────────────┐     │         │
│  │  │ Área             │ Visualizar │ Editar  │     │         │
│  │  ├──────────────────┼────────────┼─────────┤     │         │
│  │  │ 🏠 Início        │    ✓       │   —     │     │         │
│  │  │ 👥 Segmentos     │    ✓       │   ✓     │     │         │
│  │  │ 📦 Objetos       │    ○       │   ○     │     │         │
│  │  │ 🛡️ Regras        │    ○       │   ○     │     │         │
│  │  │ 🔗 Jornadas      │    ✓       │   ○     │     │         │
│  │  │ ...              │   ...      │  ...    │     │         │
│  │  └─────────────────────────────────────────┘     │         │
│  │                                                  │         │
│  │  5 de 11 áreas com acesso                        │         │
│  │                                                  │         │
│  │  [Cancelar]                [Salvar Permissões]   │         │
│  └─────────────────────────────────────────────────┘         │
│       │                                                      │
│       ▼                                                      │
│  Toast: "Permissões de João Oliveira atualizadas"            │
│  Log no histórico: "Maria Santos alterou permissões..."      │
└──────────────────────────────────────────────────────────────┘
```

1. Admin/Gestor clica no membro na lista (ou no menu "⋯" → "Gerenciar permissões").
2. Abre painel lateral/drawer com abas: **Dados**, **Controle de Acesso**, **Histórico**.
3. Na aba "Controle de Acesso": grid com todas as 11 áreas e toggles view/edit.
4. Ações rápidas disponíveis:
   * "Selecionar tudo (visualização)" — marca `view: true` em todas as áreas.
   * "Limpar tudo" — remove todas as permissões.
   * "Copiar permissões de..." — abre seletor de outro membro.
   * "Aplicar template" — abre seletor de template pré-definido.
5. Marca/desmarca toggles conforme necessário.
   * Regra: desmarcar `view` automaticamente desmarca `edit`.
   * Regra: marcar `edit` automaticamente marca `view`.
   * Áreas view-only (Início, Insights): toggle de `edit` desabilitado.
6. Clica em "Salvar Permissões".
7. Toast de confirmação.
8. Registro no histórico de auditoria.

### **Critérios de Aceitação**

| # | Critério | Verificação |
| -- | -- | -- |
| 01 | O grid exibe todas as 11 áreas | Listagem completa |
| 02 | Desmarcar `view` automaticamente desmarca `edit` na mesma área | Lógica de toggle |
| 03 | Marcar `edit` automaticamente marca `view` na mesma área | Lógica de toggle |
| 04 | Áreas view-only (Início, Insights) têm toggle de `edit` desabilitado (com indicador) | UI behavior |
| 05 | "Selecionar tudo (view)" marca `view: true` em todas as áreas | Ação rápida |
| 06 | "Limpar tudo" solicita confirmação antes de executar | Safety check |
| 07 | "Copiar permissões de..." abre seletor com lista de outros membros | Funcionalidade |
| 08 | Após salvar, toast "Permissões de [nome] atualizadas" aparece | Feedback |
| 09 | Registro no histórico: "[ator] alterou permissões de [membro] em [data]" | Auditoria |
| 10 | O contador "X de 11 áreas com acesso" atualiza em tempo real ao alterar toggles | Contagem dinâmica |
| 11 | Admin NÃO pode editar permissões de outro Admin ou do Gestor (grid não aparece para esses roles) | Restrição de role |
| 12 | Se nenhuma permissão está marcada, aviso: "Este membro não terá acesso a nenhuma área" | Feedback preventivo |
| 13 | As alterações de permissão são aplicadas imediatamente após salvar (sem necessidade de re-login) | Efeito imediato |

### **Exceções e Edge Cases**

* **Admin tenta editar permissões de outro Admin:** O grid de permissões não aparece. Mensagem: "Administradores têm acesso total à plataforma."
* **Gestor edita permissões de Admin:** Não se aplica — Admin tem acesso total. Se quiser restringir, deve rebaixar para Membro primeiro.
* **Conflito de sessão:** Se o membro-alvo está logado, suas permissões atualizam na próxima navegação (ou via polling/WebSocket).

### **Referências de Código**

* `TeamSection.tsx` (ux-lab): aba "Controle de Acesso" com grid funcional (linhas 547-716)
* `togglePermission()` (linha 161): lógica de view/edit interdependentes já implementada no protótipo

---

## **US-07: Gestor Promove Membro para Admin**

### **Descrição**

Como **Gestor**, quero promover um membro para Administrador para que ele possa ajudar a gerenciar a equipe e ter acesso total à plataforma.

### **Ator principal**

Gestor (role `owner`) — exclusivo

### **Pré-condições**

* O Gestor está autenticado.
* O membro-alvo tem role "Membro" (não é Admin nem Gestor).

### **Fluxo de Tela (passo a passo)**

```
┌──────────────────────────────────────────────────────────────┐
│  Setup Empresa > Equipe > Aba "Membros"                      │
│                                                              │
│  Lista de membros:                                           │
│  ┌────────────────────────────────────────────────────┐      │
│  │ JO  João Oliveira   Membro  Analista CRM     ⋯    │      │
│  └────────────────────────────────────────────────────┘      │
│       │  Clica em "⋯"                                        │
│       ▼                                                      │
│  DropdownMenu:                                               │
│  ┌──────────────────────────┐                                │
│  │ ✏️  Editar dados          │                                │
│  │ 🔒 Gerenciar permissões  │                                │
│  │ ⬆️  Promover a Admin      │  ← Apenas o Gestor vê isto    │
│  │ ─────────────────────── │                                │
│  │ 🗑️  Remover da equipe    │                                │
│  └──────────────────────────┘                                │
│       │  Clica em "Promover a Admin"                         │
│       ▼                                                      │
│  ConfirmDialog:                                              │
│  ┌─────────────────────────────────────────────────┐         │
│  │  ⚠️  Promover a Administrador?                   │         │
│  │                                                  │         │
│  │  João Oliveira receberá:                         │         │
│  │  • Acesso total à plataforma                      │         │
│  │  • Permissão para convidar e remover membros     │         │
│  │  • Permissão para configurar acessos             │         │
│  │                                                  │         │
│  │  As permissões granulares atuais serão removidas  │         │
│  │  pois Admins têm acesso total automático.        │         │
│  │                                                  │         │
│  │  [Cancelar]              [Confirmar Promoção]    │         │
│  └─────────────────────────────────────────────────┘         │
│       │                                                      │
│       ▼                                                      │
│  Badge muda: "Membro" → "Admin" (azul)                       │
│  Label customizado é mantido (opcional visual)               │
│  Toast: "João Oliveira foi promovido a Administrador"        │
└──────────────────────────────────────────────────────────────┘
```

1. Gestor clica em "⋯" no membro-alvo.
2. No DropdownMenu, clica em **"Promover a Admin"**.
3. ConfirmDialog abre com explicação clara do impacto:
   * Acesso total à plataforma.
   * Permissões granulares atuais serão removidas (admin = acesso total).
4. Gestor confirma.
5. Badge do membro muda de "Membro" para "Admin".
6. Toast de sucesso.
7. Registro no histórico de auditoria.

### **Critérios de Aceitação**

| # | Critério | Verificação |
| -- | -- | -- |
| 01 | A opção "Promover a Admin" só aparece para o **Gestor** (admin não pode promover outros a admin) | Visibilidade por role |
| 02 | A opção NÃO aparece para membros que já são Admin | Condicional |
| 03 | ConfirmDialog explica claramente o impacto: acesso total, remoção de permissões granulares | Conteúdo do dialog |
| 04 | Após promoção, o badge muda de "Membro" para "Admin" imediatamente | Atualização visual |
| 05 | As permissões granulares do membro são removidas do banco (admin bypassa permissões) | Backend cleanup |
| 06 | O counter de "X/11 áreas" desaparece (admins não têm counter) | UI cleanup |
| 07 | O `customLabel` é preservado (ex: ainda mostra "Analista de CRM" como referência) | Dados mantidos |
| 08 | Toast: "[nome] foi promovido a Administrador" | Feedback |
| 09 | Registro no histórico: "Gestor promoveu [nome] de Membro para Administrador" | Auditoria |
| 10 | A promoção tem efeito imediato na sessão do membro promovido | Real-time |

### **Exceções e Edge Cases**

* **Gestor tenta promover o único admin:** Permitido (sem limite de admins).
* **Admin tenta acessar "Promover a Admin":** A opção simplesmente não aparece no DropdownMenu.
* **Erro de rede na promoção:** Toast de erro, estado não muda. Dialog permanece aberto para retry.

### **Referências de Código**

* `canManageRole()` em `subUsers.ts` (linha 103): owner pode gerenciar tudo
* `ChangeRoleRequest` em `subUsers.ts` (linha 58): tipo para request de mudança de role

---

## **US-08: Membro Vê Seu Próprio Perfil de Acesso**

### **Descrição**

Como **membro**, quero saber quais áreas eu posso acessar para que eu entenda meu escopo de trabalho sem precisar perguntar ao gestor.

### **Ator principal**

Membro (qualquer role de "Membro")

### **Pré-condições**

* O membro está autenticado.

### **Fluxo de Tela (passo a passo)**

```
┌──────────────────────────────────────────────────────────────┐
│  Menu do usuário (canto superior direito) → "Meu Perfil"     │
│       │                                                      │
│       ▼                                                      │
│  Configurações > Meu Perfil                                  │
│                                                              │
│  ┌─────────────────────────────────────────────────┐         │
│  │  Dados Pessoais                                  │         │
│  │  Nome: João Oliveira                             │         │
│  │  Email: joao@empresa.com                         │         │
│  │  Role: Membro · Analista de CRM                  │         │
│  └─────────────────────────────────────────────────┘         │
│                                                              │
│  ┌─────────────────────────────────────────────────┐         │
│  │  🔒 Meu Acesso                                   │         │
│  │                                                  │         │
│  │  Permissões gerenciadas pelo gestor da conta.    │         │
│  │  Entre em contato para solicitar alterações.     │         │
│  │                                                  │         │
│  │  ┌─────────────────────────────────────────┐     │         │
│  │  │ Área            │ Nível                 │     │         │
│  │  ├─────────────────┼───────────────────────┤     │         │
│  │  │ Início          │ 🟢 Visualizar         │     │         │
│  │  │ Segmentos       │ 🔵 Editar             │     │         │
│  │  │ Objetos         │ ⚫ Sem acesso          │     │         │
│  │  │ Regras          │ ⚫ Sem acesso          │     │         │
│  │  │ Jornadas        │ 🟢 Visualizar         │     │         │
│  │  │ Audiência       │ 🟢 Visualizar         │     │         │
│  │  │ Companion       │ ⚫ Sem acesso          │     │         │
│  │  │ ...             │ ...                   │     │         │
│  │  └─────────────────────────────────────────┘     │         │
│  │                                                  │         │
│  │  5 de 11 áreas disponíveis                       │         │
│  └─────────────────────────────────────────────────┘         │
└──────────────────────────────────────────────────────────────┘
```

1. Membro acessa "Meu Perfil" via menu do usuário (canto superior direito).
2. Página mostra dados pessoais (nome, email, role, label).
3. Seção **"Meu Acesso"** lista todas as 11 áreas com badges coloridos:
   * **Editar** (badge azul): `edit: true`
   * **Visualizar** (badge verde): `view: true, edit: false`
   * **Sem acesso** (badge cinza): `view: false, edit: false`
4. Texto explicativo: "Permissões gerenciadas pelo gestor da conta. Entre em contato para solicitar alterações."
5. O membro pode **ver** suas permissões mas **não pode alterá-las**.

### **Critérios de Aceitação**

| # | Critério | Verificação |
| -- | -- | -- |
| 01 | A seção "Meu Acesso" aparece na página de perfil do membro | Renderização |
| 02 | Lista todas as 11 áreas com badge de nível | Completude |
| 03 | Badge "Editar" em azul para áreas com `edit: true` | Visual |
| 04 | Badge "Visualizar" em verde para áreas com `view: true, edit: false` | Visual |
| 05 | Badge "Sem acesso" em cinza para áreas com `view: false, edit: false` | Visual |
| 06 | Nenhum toggle ou botão de edição de permissão está presente | Somente leitura |
| 07 | Texto explicativo sobre contato com gestor é exibido | Orientação |
| 08 | Contador "X de 11 áreas disponíveis" é exibido | Resumo |
| 09 | Para Gestor e Admin, a seção "Meu Acesso" NÃO aparece (eles têm acesso total) | Condicional por role |
| 10 | Para Gestor/Admin, exibir badge discreto: "Acesso total à plataforma" | Visual alternativo |

### **Componente de UI — Badge de Role no Header**

Além da seção "Meu Acesso", incluir um badge discreto no menu do usuário (canto superior direito):

```
┌──────────────────────┐
│  JO  João Oliveira   │
│  Membro              │  ← Badge com cor do role
│  5/11 áreas          │  ← Tooltip opcional
└──────────────────────┘
```

### **Exceções e Edge Cases**

* **Membro sem nenhuma permissão:** Seção mostra "Você ainda não tem acesso a nenhuma área. Entre em contato com o gestor."
* **Permissões alteradas enquanto membro visualiza:** A lista não atualiza em real-time (reload necessário). Possível implementação futura com WebSocket.

---

## **US-09: Gestor Remove Membro da Equipe**

### **Descrição**

Como **Gestor**, quero remover um membro da equipe para que ele não tenha mais acesso à plataforma.

### **Ator principal**

Gestor (role `owner`) ou Admin (role `admin`, apenas para membros)

### **Pré-condições**

* O ator está autenticado e na seção **Setup Empresa > Equipe**.
* O membro-alvo não é o Gestor (Gestor é irremovível).

### **Fluxo de Tela (passo a passo)**

```
┌──────────────────────────────────────────────────────────────┐
│  Setup Empresa > Equipe > Aba "Membros"                      │
│                                                              │
│  Lista de membros:                                           │
│  ┌────────────────────────────────────────────────────┐      │
│  │ JO  João Oliveira   Membro  Analista CRM     ⋯    │      │
│  └────────────────────────────────────────────────────┘      │
│       │  Clica em "⋯" → "Remover da equipe"                  │
│       ▼                                                      │
│  ConfirmDialog (destructive):                                │
│  ┌─────────────────────────────────────────────────┐         │
│  │  🔴 Remover membro?                              │         │
│  │                                                  │         │
│  │  Tem certeza que deseja remover João Oliveira    │         │
│  │  da equipe?                                      │         │
│  │                                                  │         │
│  │  Esta ação:                                      │         │
│  │  • Revogará todo o acesso imediatamente          │         │
│  │  • Invalidará a sessão ativa do membro           │         │
│  │  • NÃO apaga dados criados por ele               │         │
│  │                                                  │         │
│  │  Digite "REMOVER" para confirmar:                │         │
│  │  [_____________________]                         │         │
│  │                                                  │         │
│  │  [Cancelar]         [Remover Membro] (vermelho)  │         │
│  └─────────────────────────────────────────────────┘         │
│       │                                                      │
│       ▼                                                      │
│  Membro removido da lista                                    │
│  Toast: "João Oliveira foi removido da equipe"               │
│  Sessão do membro invalidada imediatamente                   │
└──────────────────────────────────────────────────────────────┘
```

1. Gestor/Admin clica em "⋯" no membro-alvo.
2. Seleciona **"Remover da equipe"**.
3. ConfirmDialog **destructive** abre com aviso claro:
   * Revogação imediata de acesso.
   * Invalidação de sessão ativa.
   * Dados criados não são apagados.
4. O Gestor digita "REMOVER" para confirmar (safety check para ação destrutiva).
5. Membro é removido da lista.
6. Toast de confirmação.
7. Sessão do membro é invalidada imediatamente (token revogado).

### **Critérios de Aceitação**

| # | Critério | Verificação |
| -- | -- | -- |
| 01 | A opção "Remover da equipe" aparece no DropdownMenu para Gestor (qualquer membro) e Admin (apenas membros) | Visibilidade por role |
| 02 | A opção NÃO aparece para o Gestor no próprio DropdownMenu (Gestor é irremovível) | Proteção |
| 03 | Admin NÃO pode remover outro Admin (opção oculta) | Restrição de role |
| 04 | ConfirmDialog tem estilo destructive (borda/botão vermelho) | Visual |
| 05 | Exige digitação de "REMOVER" para confirmar | Safety check |
| 06 | Botão "Remover Membro" fica desabilitado até que "REMOVER" seja digitado corretamente | Validação |
| 07 | Após remoção, o membro desaparece da lista imediatamente | Atualização da UI |
| 08 | Sessão do membro removido é invalidada (se estava logado, é deslogado imediatamente) | Segurança |
| 09 | Toast: "[nome] foi removido da equipe" | Feedback |
| 10 | Registro no histórico: "[ator] removeu [nome] da equipe em [data]" | Auditoria |
| 11 | Dados criados pelo membro (segmentos, jornadas, etc.) permanecem na plataforma | Preservação de dados |

### **Exceções e Edge Cases**

* **Tentativa de remover o Gestor via API (burlar UI):** Backend retorna 403 Forbidden.
* **Membro com sessão ativa:** Token JWT é invalidado server-side (blacklist ou revogação).
* **Erro de rede na remoção:** Toast de erro, dialog permanece aberto. Membro não é removido.

### **Referências de Código**

* `canManageUser()` em `subUsers.ts` (linha 117): verifica se o ator pode gerenciar o alvo
* `TeamSection.tsx`: ícone de cadeado para Gestor (irremovível, linha 330)

---

## **US-10: Gestor Reenvia Convite Pendente**

### **Descrição**

Como **Gestor**, quero reenviar o convite para um membro que não aceitou para que ele receba o link novamente e possa ativar sua conta.

### **Ator principal**

Gestor (role `owner`) ou Admin (role `admin`)

### **Pré-condições**

* O membro-alvo tem status **"Pendente"** (convite enviado mas não aceito).

### **Fluxo de Tela (passo a passo)**

```
┌──────────────────────────────────────────────────────────────┐
│  Setup Empresa > Equipe > Aba "Membros"                      │
│                                                              │
│  Lista de membros:                                           │
│  ┌────────────────────────────────────────────────────┐      │
│  │ CM  Carlos Mendes   Membro  ⏳ Pendente       ⋯    │      │
│  └────────────────────────────────────────────────────┘      │
│       │  Clica em "⋯"                                        │
│       ▼                                                      │
│  DropdownMenu:                                               │
│  ┌──────────────────────────┐                                │
│  │ 📧 Reenviar convite      │  ← Só para status "Pendente"  │
│  │ ✏️  Editar dados          │                                │
│  │ 🔒 Gerenciar permissões  │                                │
│  │ ─────────────────────── │                                │
│  │ ❌ Cancelar convite       │                                │
│  └──────────────────────────┘                                │
│       │  Clica em "Reenviar convite"                         │
│       ▼                                                      │
│  Toast: "Convite reenviado para carlos@empresa.com"          │
│  Badge "Pendente" permanece                                  │
│  Timestamp do convite atualiza internamente                  │
└──────────────────────────────────────────────────────────────┘
```

1. Gestor/Admin identifica membro com badge **"Pendente"** na lista.
2. Clica em "⋯" → **"Reenviar convite"**.
3. Sistema reenvia email com novo link de ativação (token anterior é invalidado).
4. Toast: "Convite reenviado para [email]".
5. Badge "Pendente" permanece (membro ainda não aceitou).

### **Critérios de Aceitação**

| # | Critério | Verificação |
| -- | -- | -- |
| 01 | A opção "Reenviar convite" só aparece para membros com status "Pendente" | Condicional |
| 02 | A opção NÃO aparece para membros com status "Ativo" | Condicional |
| 03 | O reenvio gera um novo token (o anterior é invalidado) | Segurança |
| 04 | Toast: "Convite reenviado para [email]" | Feedback |
| 05 | O badge "Pendente" permanece após reenvio | Status mantido |
| 06 | Opção adicional "Cancelar convite" disponível para membros pendentes | Funcionalidade |
| 07 | "Cancelar convite" remove o membro da lista e invalida o token | Cleanup |
| 08 | Cooldown de 60 segundos entre reenvios (evitar spam) | Rate limiting |
| 09 | Se cooldown ativo, botão mostra "Reenviar em Xs" desabilitado | Feedback visual |
| 10 | Registro no histórico: "[ator] reenviou convite para [email] em [data]" | Auditoria |

### **Exceções e Edge Cases**

* **Reenvio muito frequente:** Cooldown de 60 segundos entre reenvios. Botão desabilitado com timer.
* **Email não chega:** Não há retry automático. Gestor pode tentar novamente após cooldown.
* **Membro ativou entre o clique e o reenvio (race condition):** Backend retorna que o membro já está ativo. Toast: "Este membro já ativou a conta."

---

## **Resumo de Componentes de UI Necessários**

| Componente | Status | User Stories Relacionadas |
| -- | -- | -- |
| Modal de Convite de Membro | **Novo** | US-01 |
| Página de Ativação (`/invite/:token`) | **Novo** | US-02 |
| `PermissionGate` (wrapper condicional) | **Novo** | US-03, US-04 |
| Seção "Meu Acesso" no perfil | **Novo** | US-08 |
| Badge de role no header | **Novo** | US-08 |
| ConfirmDialog destructive (remoção) | **Novo** | US-09 |
| Tela "Sem acesso" (`/no-access`) | **Novo** | US-02, US-05 |
| Grid de Permissões (drawer) | **Evoluir** | US-06 |
| DropdownMenu de membro | **Evoluir** | US-07, US-09, US-10 |
| `ProtectedMenuRoute` (redirect smart) | **Evoluir** | US-05 |
| Toast de acesso negado | **Evoluir** | US-05 |
| Aba "Histórico" de auditoria | **Evoluir** | US-06, US-07, US-09, US-10 |

---

## **Estratégia de Visibilidade — Resumo Executivo**

**Princípio:** "Se você não pode usar, você não vê."

| Cenário | Comportamento |
| -- | -- |
| Membro sem permissão na área | Menu **oculto** na sidebar |
| Membro com `view` na área | Menu visível, botões de ação **ocultos** |
| Membro com `edit` na área | Experiência **completa** (igual Admin nessa área) |
| Acesso direto via URL a área restrita | **Redirect** para primeiro menu disponível + toast |
| Membro visualiza detalhe (view-only) | Campos **read-only**, sem botões de salvar/editar |

**Por que ocultar e não desabilitar:**

* Menos frustração para o membro
* Menos carga cognitiva (menos elementos visuais)
* Interface parece "completa" dentro do escopo permitido
* Sem tooltips de "Sem permissão" poluindo a experiência

---

## **Prioridade de Implementação Sugerida**

| Prioridade | User Story | Justificativa |
| -- | -- | -- |
| P0 | US-01 | Sem convite, não há membros para gerenciar |
| P0 | US-02 | Sem ativação, convite não serve |
| P0 | US-03 | Core da experiência de membro restrito |
| P0 | US-05 | Segurança: proteger rotas de acesso direto |
| P1 | US-04 | Extensão natural da US-03 |
| P1 | US-06 | Gestão de permissões é o coração do módulo |
| P1 | US-09 | Remoção é operação crítica de segurança |
| P2 | US-07 | Promoção de role é operação menos frequente |
| P2 | US-08 | Informacional — melhora UX mas não bloqueia funcionalidade |
| P2 | US-10 | Conveniência — reenvio de convite |

## Histórico de status
- Backlog (backlog): 2026-03-06T12:24:21.861Z → atual

## Relações
—

## Anexos
—
