# SEND-312 — Bugs e melhorias Journey Builder UserIn - Perda de configurações ao sair sem salvar

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | High |
| Responsável | paulo.ribeiro@sendspeed.com |
| Time | Sendspeed |
| Projeto | — |
| Labels | — |
| Parent | — |
| Criada | 2026-02-10T14:08:26.524Z por paulo.ribeiro@sendspeed.com |
| Iniciada | 2026-02-12T16:00:37.499Z |
| Concluída | 2026-02-18T16:59:32.171Z |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-312-bugs-e-melhorias-journey-builder-userin-perda-de |
| URL | https://linear.app/sendspeed/issue/SEND-312/bugs-e-melhorias-journey-builder-userin-perda-de-configuracoes-ao-sair |

## Descrição

##

**Descrição:** Quando o usuário sai da página ou dá missclick fora do builder sem salvar, ele perde toda a configuração que estava criando. Isso gera frustração e perda de trabalho, especialmente em fluxos complexos que levam tempo para configurar.

> **[Imagem 1 — transcrição]:** Screenshot de UI da plataforma "UserIn" (logo laranja/azul no topo esquerdo). Seletor de idioma "BR Português (Brasil)" e usuário "User Donald / User Donald Company" no topo direito. Menu lateral esquerdo: Início, Segmentos, Análises, Regras, Companion (expandido: Componentes, Meus Cards, Jornadas), Audiência, Campanhas, Jornadas (expandido: Builder — selecionado, Analytics, Templates), Integrações, Setup Empresa. Área central: título "Nova Jornada" com badge "Rascunho" e seletor "InSite"; barra de ações no topo direito: "Organizar", "Importar", "Exportar", "Simular", "Ativar", toggle "Auto" (ligado, verde) e botão "Salvar" (azul). Painel "Componentes" ("Clique para adicionar ao canvas") com seção "GATILHOS": Evento ("Inicia quando um evento ocorre (deposit, register, etc.)"), Entra no Segmento ("Inicia quando usuário entra em um segmento (regra da plataforma)"), Webhook ("Inicia via chamada de API externa"), Regra da Plataforma ("Inicia quando uma regra existente dá match"), Trigger Manual ("Inicia via código JavaScript no site"); seção "CONDIÇÕES": Tem Tag? ("Verifica se usuário possui uma tag"), Atributo do Usuário ("Verifica atributo do usuário"), Regra da Plataforma ("Aplica uma regra existente ou cria nova inline"). O canvas à direita está vazio. Demonstra a tela do Journey Builder (Nova Jornada em Rascunho) onde as configurações são perdidas ao sair sem salvar.

##

### **Sugestão de melhoria:**

Implementar salvamento automático como rascunho a cada X segundos quando houver alterações, OU exibir um pop-up de aviso antes do usuário sair da página alertando que ele vai perder as configurações não salvas, com opções para cancelar, sair sem salvar ou salvar antes de sair.

## Histórico de status
- Backlog (backlog): 2026-02-10T14:08:26.524Z → 2026-02-12T14:11:59.998Z
- To-do (unstarted): 2026-02-12T14:11:59.998Z → 2026-02-12T16:00:37.508Z
- In Progress (started): 2026-02-12T16:00:37.508Z → 2026-02-12T18:20:25.527Z
- Pull Request (started): 2026-02-12T18:20:25.527Z → 2026-02-12T18:52:16.522Z
- Product Review (started): 2026-02-12T18:52:16.522Z → 2026-02-18T16:59:32.240Z
- Released (completed): 2026-02-18T16:59:32.240Z → atual

## Relações
—

## Anexos
—
