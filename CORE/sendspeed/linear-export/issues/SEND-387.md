# SEND-387 — 🚀 - Deploy da chipfarm do Bruno Heidrich para monitoramento de fornecedores SMS

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | No priority |
| Responsável | — |
| Time | Sendspeed |
| Projeto | — |
| Labels | User Story, Criar, Sendspeed |
| Parent | — |
| Criada | 2026-03-13T14:53:46.125Z por Vinicius Carneiro |
| Iniciada | — |
| Concluída | 2026-06-22T17:18:47.243Z |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-387--deploy-da-chipfarm-do-bruno-heidrich-para-monitoramento-de |
| URL | https://linear.app/sendspeed/issue/SEND-387/deploy-da-chipfarm-do-bruno-heidrich-para-monitoramento-de |

## Descrição

> **Como** responsável de qualidade de envio da Sendspeed
> **Quero** subir a chipfarm desenvolvida pelo Bruno Heidrich para monitorar e medir a eficácia dos nossos fornecedores de SMS (Infobip e Pushfy)
> **Para** garantir que estamos entregando mensagens com a melhor taxa de entrega, velocidade e qualidade, tendo dados reais para cobrar SLAs e tomar decisões de roteamento entre fornecedores

---

# 📈 Use Case: Monitoramento de qualidade dos fornecedores Infobip e Pushfy via chipfarm

A Sendspeed dispara campanhas de SMS através de dois fornecedores: Infobip e Pushfy. Para garantir qualidade, a chipfarm do Bruno Heidrich funciona como um "receptor de teste" com múltiplos chips de diferentes operadoras (Claro, Vivo, TIM, Oi):

1. **Setup**: A chipfarm possui chips reais de cada operadora. Quando uma campanha é disparada, uma amostra de mensagens é enviada para números dos chips da chipfarm (números de teste conhecidos).
2. **Medição automática**: A chipfarm recebe os SMS nos chips e registra automaticamente:
   * **Taxa de entrega**: % de mensagens que efetivamente chegaram ao chip (ex: Infobip entregou 98% via Vivo, mas apenas 91% via TIM)
   * **Latência de entrega**: Tempo entre o envio e o recebimento no chip (ex: Pushfy entrega em 3s na Claro, mas 12s na Oi)
   * **Integridade da mensagem**: Se o conteúdo recebido é idêntico ao enviado (caracteres especiais, encoding, truncamento)
   * **Taxa de falha por operadora**: Qual operadora tem mais falhas por fornecedor
   * **Disponibilidade**: Uptime de cada fornecedor ao longo do tempo
3. **Dashboard comparativo**: Na plataforma Sendspeed, o gestor acessa o dashboard de qualidade de fornecedores e vê um comparativo lado a lado:

## Histórico de status
- Backlog (backlog): 2026-03-13T14:53:46.125Z → 2026-06-22T17:18:47.248Z
- Released (completed): 2026-06-22T17:18:47.248Z → atual

## Relações
—

## Anexos
—
