# SEND-483 — 3. Padronização e de-para de status de callback por cliente

| Campo | Valor |
| -- | -- |
| Status | To-do (unstarted) |
| Prioridade | No priority |
| Responsável | thiago.melin@sendspeed.com |
| Time | Sendspeed |
| Projeto | — |
| Labels | — |
| Parent | — |
| Criada | 2026-06-02T17:47:44.037Z por Vinicius Carneiro |
| Iniciada | — |
| Concluída | — |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-483-3-padronizacao-e-de-para-de-status-de-callback-por-cliente |
| URL | https://linear.app/sendspeed/issue/SEND-483/3-padronizacao-e-de-para-de-status-de-callback-por-cliente |

## Descrição

> ***Quero** parametrizar, por cliente, o de-para entre o status retornado pelo fornecedor (de) e o status entregue ao cliente (para), agrupando múltiplos status de fornecedor em um único status de saída, com um default aplicado quando não houver customização*
***Para** que cada cliente receba os status já tratados e padronizados, mantendo um comportamento previsível mesmo sem configuração específica*

### 📈 Use Case:

Cada fornecedor retorna seus próprios códigos de status. Hoje eles são repassados crus ao cliente. A plataforma passa a aplicar uma etapa de tratamento antes do encaminhamento: os callbacks do fornecedor são agrupados e normalizados num conjunto padrão de status, configurável por cliente via de-para. Cliente sem configuração específica recai sobre o de-para default, em vez de receber o código bruto.

### ✅ Critérios de aceite:

* Há uma etapa de tratamento dos dados antes do encaminhamento ao cliente — o callback não é repassado cru, é normalizado
* O de-para suporta agrupamento (muitos-para-um): múltiplos status de fornecedor (de) podem ser agrupados em um único status de saída (para). Ex: vários códigos de erro da Infobip → Rejected
* É possível parametrizar o de-para por cliente, associando status de fornecedor — de (ex: Infobip, Pushfy e outros) — ao status entregue ao cliente — para (ex: Smartico - SevenX, Smartico - Open)
* O conjunto padrão de status de saída é: Delivered, Undelivered, Rejected
* Para a Smartico, não existe status "Undelivered" explícito: undelivered é contabilizado pelo gap entre os números enviados e os que retornaram Delivered ou Rejected
* A janela de corte dos status é de 24h
* O status bruto original do fornecedor é retido internamente (log/auditoria), mesmo que apenas o status agrupado seja enviado ao cliente — preserva capacidade de diagnóstico
* Existe um de-para default da plataforma (Sent / Delivered / Rejected), aplicado automaticamente a qualquer cliente sem configuração própria
* O default é obrigatório: nenhum status bruto de fornecedor chega ao cliente, mesmo sem parametrização específica
* Alterar o de-para de um cliente (ex: Smartico - SevenX) não afeta outros clientes (ex: Smartico - Open) nem o default

### 🧩 Cenários de teste:

- [ ] Configurar agrupamento para o Cliente A (vários códigos do Infobip → Rejected) e verificar que todos chegam como Rejected
- [ ] Receber callback de um cliente sem configuração própria e verificar que o de-para default é aplicado
- [ ] Verificar que nenhum cliente recebe código bruto de fornecedor em nenhum cenário (com ou sem config)
- [ ] Verificar que o status bruto original fica registrado internamente mesmo após o agrupamento
- [ ] Receber status de fornecedor fora de qualquer agrupamento e verificar log + tratamento definido
- [ ] Alterar o de-para do Cliente A e verificar que o Cliente B (que usa o default) não é afetado
- [ ] Configurar de-paras diferentes para dois fornecedores do mesmo cliente (ex: Infobip e Pushfy) e validar cada agrupamento
- [ ] Consultar o histórico de versões do de-para de um cliente e verificar registro da alteração

## Histórico de status
- To-do (unstarted): 2026-06-02T17:47:44.037Z → atual

## Relações
—

## Anexos
—
