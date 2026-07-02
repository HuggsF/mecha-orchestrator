# SEND-485 — 1. Lista fria sem fallback obrigatório e sem deduplicação de numeros no upload

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | Urgent |
| Responsável | thiago.melin@sendspeed.com |
| Time | Sendspeed |
| Projeto | — |
| Labels | Ambas, Melhoria |
| Parent | — |
| Criada | 2026-06-02T18:02:17.666Z por Vinicius Carneiro |
| Iniciada | — |
| Concluída | 2026-06-22T17:16:11.687Z |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-485-1-lista-fria-sem-fallback-obrigatorio-e-sem-deduplicacao-de |
| URL | https://linear.app/sendspeed/issue/SEND-485/1-lista-fria-sem-fallback-obrigatorio-e-sem-deduplicacao-de-numeros-no |

## Descrição

> **Como** operador de marketing
> **Quero** configurar e disparar campanhas de lista fria com fallback opcional e deduplicação automática de números na importação da lista
> **Para** concluir o fluxo de disparo sozinho, sem abrir ticket de suporte e sem enviar mensagens duplicadas para o mesmo número

### 📈 Use Case:

O operador importa uma lista fria, o sistema remove números duplicados e inválidos antes do disparo informando o que foi removido, decide se quer ou não fallback naquela campanha, e dispara — tudo sem depender do time de suporte.

### ✅ Critérios de aceite:

* O fallback deixa de ser obrigatório e passa a ser configurável por campanha, com um default explícito e por default desligado.
* Na importação da lista, o sistema identifica números repetidos dentro da mesma lista e pergunta se o usuário gostaria ou não de remover os duplicados. **\[se for muito dificil, cancelar\]**
* O sistema valida e rejeita números em formato inválido, indicando a linha e o motivo do erro
* O operador consegue concluir importação + configuração + disparo sem nenhuma etapa que exija intervenção manual do suporte
* O sistema de upload de lista não pode duplicar numeros aleatóriamente
* Métrica de sucesso: taxa de tickets de suporte abertos durante disparo de lista fria cai para zero

### 🧩 Cenários de teste:

- [ ] Importar lista com 1.4m números, sem haver duplicação.
- [ ] Disparar campanha com fallback desativado e verificar que nenhuma mensagem de fallback é enviada
- [ ] Disparar campanha com fallback ativado e verificar comportamento idêntico ao atual
- [ ] Importar lista com números em formato inválido e duplicados e verificar mensagem de erro com número da linha **\[caso haja a possibilidade\]**
- [ ]  Concluir um disparo de ponta a ponta sem acionar suporte

## Histórico de status
- To-do (unstarted): 2026-06-02T18:02:17.666Z → 2026-06-22T17:16:11.733Z
- Released (completed): 2026-06-22T17:16:11.733Z → atual

## Relações
—

## Anexos
—
