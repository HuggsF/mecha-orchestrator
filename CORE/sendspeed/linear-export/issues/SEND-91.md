# SEND-91 — [LEGADO][REFACTORY] — Status do callback dos disparos pela InfoBip

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | No priority |
| Responsável | Hugo Fernandes |
| Time | Sendspeed |
| Projeto | — |
| Labels | Tech Story |
| Parent | — |
| Criada | 2025-09-05T13:58:04.962Z por bruno.heidrich@sendspeed.com |
| Iniciada | 2025-10-23T18:59:16.128Z |
| Concluída | 2025-10-31T13:12:53.044Z |
| Arquivada | 2026-05-06T22:26:32.714Z |
| Vencimento | — |
| Branch | hugofernandes/send-91-legadorefactory-status-do-callback-dos-disparos-pela-infobip |
| URL | https://linear.app/sendspeed/issue/SEND-91/legadorefactory-status-do-callback-dos-disparos-pela-infobip |

## Descrição

**Como** Head de Produto,
**quero** que a plataforma **puxe e mostre** os status de entrega da InfoBip,
**para** dar visibilidade aos clientes e usarmos esses dados internamente.

**Pronto quando**

* Existe um **mapa simples** de status **InfoBip → nossos status** (enviado, entregue, não entregue, pendente/erro) **aplicado** no sistema.
* Para **novos disparos**, recebemos e **guardamos** o status com campos mínimos: *messageId*, número, status, data/hora e motivo/operadora (**sem duplicar**).
* Nas telas de **Campanhas/Envios**, vejo:
  * **contagens por status**,
  * **status atual por mensagem**,
  * **filtros** por período e status.
* Consigo **exportar CSV** (período + status). — Ainda não disponível. 
* Feito um **backfill curto** (ex.: últimos **7 dias**, ou o período que você definir) e validada uma amostra nas telas.


Campanha teste:

> **[Imagem 1 — transcrição]:** Screenshot de UI (tema escuro) de uma tela de acompanhamento de status de disparos/campanha da SendSpeed. No canto superior direito há um botão laranja "Download do CSV #1" (ícone de download). Barra de filtros com três campos: "Telefone" (input com ícone de telefone, vazio), "Texto da Mensagem" (input com ícone de balão, vazio) e "Data" (intervalo "29/10/2025" a "30/10/2025") seguido de um botão verde "Pesquisar". Duas seções de métricas: **"Status: SendSpeed"** com "0 Pendentes" (ícone de banco de dados) e "205 Erros" (ícone de alerta/triângulo); **"Status: Operadora"** com "48.796 Em fila" (ícone de avião de papel/enviar), além de um ícone verde de check e dois ícones (bloqueado e X/erro) sem números visíveis. Há duas barras de progresso: uma cheia "100% — 50.049" e outra "2.? — 49.844". Abaixo, uma barra de abas/contadores: "Pendentes 0", "Erros 205", "Em fila 48.796" (aba ativa, destacada em verde), "Entregues 976", "Não entregues 72", "Inválidas 0". Em seguida uma tabela com colunas: TELEFONE, TEXTO DA MENSAGEM, AGENDADA PARA, ENVIADO EM, STATUS RECEBIDO EM. Linhas listadas (todas com o mesmo texto de mensagem): telefones 5521982307074, 5511941239729, 5511993451356, 5555992436666, 5594992475241, 5551993506190. Texto da mensagem em todas as linhas: "(donaldbet) Na Donald se diverte e ainda tem 30% de CASHBACK! Aqui nos jogamos junto com você! Acesse agora e JOGUE! https://donald.bet.br". Colunas de data em todas as linhas: AGENDADA PARA "29/10/2025 16:21:00", ENVIADO EM "29/10/2025 16:52:28", STATUS RECEBIDO EM "29/10/2025 16:52:28". A imagem demonstra a tela de contagens por status (mapeamento SendSpeed x Operadora), filtros por período e a listagem de mensagens por status com os campos de callback da InfoBip.

## Histórico de status
- To-do (unstarted): 2025-09-05T13:58:04.962Z → 2025-09-25T18:00:11.481Z
- Paused (unstarted): 2025-09-25T18:00:11.481Z → 2025-10-23T18:59:16.146Z
- Pull Request (started): 2025-10-23T18:59:16.146Z → 2025-10-30T19:26:56.064Z
- Product Review (started): 2025-10-30T19:26:56.064Z → 2025-10-31T13:12:53.063Z
- Released (completed): 2025-10-31T13:12:53.063Z → atual

## Relações
—

## Anexos
—
