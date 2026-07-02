# SEND-318 — Bugs e melhorias Journey Builder UserIn - Front cortando conteúdo e botão de copiar trigger

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | Medium |
| Responsável | paulo.ribeiro@sendspeed.com |
| Time | Sendspeed |
| Projeto | — |
| Labels | — |
| Parent | — |
| Criada | 2026-02-10T19:26:30.684Z por paulo.ribeiro@sendspeed.com |
| Iniciada | 2026-02-12T14:17:00.700Z |
| Concluída | 2026-02-18T16:12:43.868Z |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-318-bugs-e-melhorias-journey-builder-userin-front-cortando |
| URL | https://linear.app/sendspeed/issue/SEND-318/bugs-e-melhorias-journey-builder-userin-front-cortando-conteudo-e |

## Descrição

**Descrição:** O conteúdo do modal está cortando no lado direito, impedindo que o usuário veja informações completas e possivelmente interaja com elementos da interface. Além disso, é necessário conferir se o botão de copiar o código do trigger está funcionando corretamente. O texto "Frequência de Execução" aparece duplicado no modal: uma vez como título do botão e outra logo abaixo com a descrição "Controla quantas vezes este trigger pode disparar para o mesmo usuário".

> **[Imagem 1 — transcrição]:** Screenshot de UI de um painel lateral de configuração de card "Trigger Manual" (badge "trigger", ícone verde de play) com subtítulo "Inicia via código JavaScript no site" e "X" para fechar. Bloco verde "Trigger Manual via JavaScript" com o texto "Esta jornada será iniciada quando você chamar o código abaixo no s..." (cortado à direita). Seção "Código para disparar:" com um bloco de código escuro: `// Trigger manual para: Jornada (P.R) TESTE UX` / `window.__JourneyInsiteEngine?.triggerJourney('6989e76f9c4a...` (cortado) / `reason: 'manual',` / `userData: {` / `// Dados opcionais do usuário` / `// customField: 'valor'` / `}` / `});`. Seção "Como usar:" com passos numerados: 1. Salve a jornada para gerar o ID; 2. Copie o código acima; 3. Cole no seu site onde deseja disparar a jornada; 4. Chame quando o usuário realizar a ação desejada (click, submit, etc... — cortado). Faixa "Pronto! Use o código acima para iniciar esta jorn..." (cortada). Abaixo, dois blocos roxos duplicados "Frequência de Execução" (o segundo com a descrição "Controla quantas vezes este trigger pode disparar para o mesmo us..." cortada). Início de opção com radio "Sempre — Executa toda vez que o trigger bater". Demonstra o conteúdo do modal cortado à direita e o texto "Frequência de Execução" duplicado.

**Sugestão de melhoria:**

* Ajustar a largura do modal para garantir que todo conteúdo seja visível
* Verificar e corrigir a funcionalidade do botão de copiar código do trigger
* Consolidar o texto "Frequência de Execução", colocando a descrição explicativa diretamente no primeiro campo, evitando duplicação.

## Histórico de status
- Backlog (backlog): 2026-02-10T19:26:30.684Z → 2026-02-12T14:17:00.713Z
- Product Review (started): 2026-02-12T14:17:00.713Z → 2026-02-18T16:12:43.896Z
- Released (completed): 2026-02-18T16:12:43.896Z → atual

## Relações
—

## Anexos
—
