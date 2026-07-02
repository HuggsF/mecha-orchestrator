# SEND-317 — Bugs e melhorias Journey Builder UserIn - Botão 'Frequência de Execução' não intuitivo e texto duplicado

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | No priority |
| Responsável | paulo.ribeiro@sendspeed.com |
| Time | Sendspeed |
| Projeto | — |
| Labels | — |
| Parent | — |
| Criada | 2026-02-10T19:20:26.697Z por paulo.ribeiro@sendspeed.com |
| Iniciada | 2026-02-12T17:21:16.265Z |
| Concluída | 2026-02-18T16:25:14.820Z |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-317-bugs-e-melhorias-journey-builder-userin-botao-frequencia-de |
| URL | https://linear.app/sendspeed/issue/SEND-317/bugs-e-melhorias-journey-builder-userin-botao-frequencia-de |

## Descrição

**Descrição:** Quando o usuário clica no botão 'Frequência de Execução', o dropdown abre mas não há nenhum estímulo visual de que isso aconteceu. O usuário precisa rolar a tela para baixo para perceber que o dropdown está aberto, o que gera confusão e a sensação de que o botão não funcionou. Além disso, o texto aparece praticamente duplicado: o título "Frequência de Execução" aparece duas vezes, sendo que na segunda vez vem acompanhado da descrição "Controla quantas vezes este trigger pode disparar para o mesmo usuário".

> **[Imagem 1 — transcrição]:** Screenshot de UI de um painel lateral de configuração de um card do tipo "Evento" (badge "trigger", ícone verde de raio) com o subtítulo "Inicia quando um evento ocorre (deposit, register, etc.)" e um "X" para fechar. Lista de eventos com radio buttons: "Aposta" (Quando usuário faz uma aposta), "Saque" (Quando usuário solicita saque), "KYC Completo" (Quando KYC é aprovado), "Início de Sessão" (Quando uma sessão é iniciada), "Fim de Sessão" (Quando uma sessão termina). Abaixo, dois blocos roxos praticamente duplicados: o primeiro "Frequência de Execução" com um dropdown "Por sessão"; o segundo "Frequência de Execução" com a descrição "Controla quantas vezes este trigger pode disparar para o mesmo usuário". Demonstra o texto "Frequência de Execução" duplicado e o dropdown pouco visível.

**Sugestão de melhoria:**

* Garantir que ao clicar no botão, o dropdown abra de forma visível na tela atual (scroll automático ou posicionamento adequado do dropdown)
* Adicionar feedback visual claro de que o dropdown está aberto (seta animada, mudança de cor, etc)
  Consolidar o texto explicativo diretamente no primeiro campo, evitando duplicação

## Histórico de status
- Backlog (backlog): 2026-02-10T19:20:26.697Z → 2026-02-12T14:34:31.829Z
- To-do (unstarted): 2026-02-12T14:34:31.829Z → 2026-02-12T17:21:16.284Z
- In Progress (started): 2026-02-12T17:21:16.284Z → 2026-02-12T18:20:31.944Z
- Pull Request (started): 2026-02-12T18:20:31.944Z → 2026-02-12T18:52:19.141Z
- Product Review (started): 2026-02-12T18:52:19.141Z → 2026-02-18T16:25:14.833Z
- Released (completed): 2026-02-18T16:25:14.833Z → atual

## Relações
—

## Anexos
—
