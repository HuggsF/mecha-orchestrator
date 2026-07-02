# SEND-58 — [LEGADO] [SPIKE] Estudo do que precisa de Manutenção do legado de SMS

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | High |
| Responsável | Hugo Fernandes |
| Time | Sendspeed |
| Projeto | — |
| Labels | — |
| Parent | — |
| Criada | 2025-08-22T12:19:07.618Z por bruno.heidrich@sendspeed.com |
| Iniciada | 2025-08-27T15:13:13.979Z |
| Concluída | 2025-09-03T23:09:58.178Z |
| Arquivada | 2026-03-05T02:15:24.230Z |
| Vencimento | — |
| Branch | hugofernandes/send-58-legado-spike-estudo-do-que-precisa-de-manutencao-do-legado |
| URL | https://linear.app/sendspeed/issue/SEND-58/legado-spike-estudo-do-que-precisa-de-manutencao-do-legado-de-sms |

## Descrição

**Contexto**
Devido a bugs recentes e falta de manutenção, vamos dar atenção ao produto legado de SMS nesta semana.

**O que será feito**

* Revisar o funcionamento geral dos envios e retornos.
* Corrigir os principais erros identificados.
* Organizar de forma simples como identificar falhas e o que fazer.

**Pronto quando**

* Envios e confirmações acontecem sem falhas críticas.
* Os erros mais frequentes estão corrigidos.
* Existe um resumo curto do que foi feito e dos pontos de atenção.

@andrei.garcia testou as principais funcionalidades da plataforma e precisou realizar alguns ajustes:

* Configuração do servidor web APACHE ✅ 
* Downgrade da versão do PHP para o 7.4 ✅
* Ajustes necessários no código para compatibilidade com PHP 7.4 ✅

Hugo realizou o teste das principais funcionalidades das API's de entrada de sms individual, replicação de campanha diária e entrada de sms em bulking e precisou realizar alguns ajustes:

* Configuração do servidor web NGINX no servidor de redirecionamento de status ✅
* Migração de para servidor único de rabbitMQ✅ 
* Ajuste em variáveis de ambiente em projetos relacionados ao status ✅

## ⚠️ Ajustes necessários:

* Atualmente temos um espelhamento funcionando a partir das 00h que está ocasionando lock no banco e bloqueio de campanhas, é necessário retirar.
* Coleta de documentações dos principais projetos LEGADO existente:
  * APP Sendspeed
  * API Sendspeed
  * Postback Status Sendspeed
  * Encurtator de Links
  * CRON's de envios de sms's

## Histórico de status
- To-do (unstarted): 2025-08-22T12:19:07.618Z → 2025-08-27T15:13:13.947Z
- In Progress (started): 2025-08-27T15:13:13.947Z → 2025-08-28T19:50:27.813Z
- Pull Request (started): 2025-08-28T19:50:27.813Z → 2025-08-29T12:52:04.208Z
- Product Review (started): 2025-08-29T12:52:04.208Z → 2025-09-03T23:09:58.165Z
- Released (completed): 2025-09-03T23:09:58.165Z → atual

## Relações
—

## Anexos
—
