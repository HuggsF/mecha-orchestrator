# SEND-234 — [MELHORIA] Modal da Roleta com z-index Prioritário e Fundo Semitransparente

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | Urgent |
| Responsável | peterson.marques@sendspeed.com |
| Time | Sendspeed |
| Projeto | — |
| Labels | — |
| Parent | — |
| Criada | 2025-10-31T13:46:34.613Z por Vinicius Carneiro |
| Iniciada | 2025-11-03T12:57:59.746Z |
| Concluída | 2025-11-14T13:59:13.541Z |
| Arquivada | 2026-05-20T22:16:09.416Z |
| Vencimento | — |
| Branch | hugofernandes/send-234-melhoria-modal-da-roleta-com-z-index-prioritario-e-fundo |
| URL | https://linear.app/sendspeed/issue/SEND-234/melhoria-modal-da-roleta-com-z-index-prioritario-e-fundo |

## Descrição

**Como** analista de produto

**Quero** visualizar o **Modal da Roleta** com prioridade visual (acima de outros modais, como o de registro) e com um **fundo semitransparente**

**Para** manter a imersão na experiência da roleta sem perder a referência visual do conteúdo do site atrás

---

### **Critérios de Aceite:**

* O **Modal da Roleta** deve ter um **z-index superior** ao modal de registro (ex: z-index: 2000 ou conforme padrão do stack de modais).
* O fundo do modal deve usar **overlay semitransparente**, permitindo que o conteúdo do site continue **visível ao fundo**, mas levemente ofuscado (exemplo: background: rgba(0,0,0,0.6)).
* O componente deve **seguir o mesmo padrão visual** dos modais existentes (bordas, espaçamento, sombra, animação de entrada e saída).
* O botão de fechar (❌) deve estar visível, no mesmo padrão dos outros modais, e fechar corretamente o modal da roleta sem afetar o modal de registro.
* Testar cenários de sobreposição:
  * Modal de registro aberto + abertura da roleta → roleta deve aparecer por cima.
  * Roleta aberta + abertura do modal de registro → registro deve ficar atrás.

## Histórico de status
- To-do (unstarted): 2025-10-31T13:46:34.613Z → 2025-11-03T12:57:59.761Z
- In Progress (started): 2025-11-03T12:57:59.761Z → 2025-11-10T13:16:21.266Z
- Product Review (started): 2025-11-10T13:16:21.266Z → 2025-11-14T13:59:13.553Z
- Released (completed): 2025-11-14T13:59:13.553Z → atual

## Relações
—

## Anexos
—
