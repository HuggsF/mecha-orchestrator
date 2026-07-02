# SEND-515 — 1. Validar e configurar o use case de recuperação de cadastro na UserIn — cliente Apostou

| Campo | Valor |
| -- | -- |
| Status | In Progress (started) |
| Prioridade | No priority |
| Responsável | — |
| Time | Sendspeed |
| Projeto | — |
| Labels | UserIn, User Story |
| Parent | — |
| Criada | 2026-06-22T17:47:43.242Z por Vinicius Carneiro |
| Iniciada | 2026-06-24T17:09:59.279Z |
| Concluída | — |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-515-1-validar-e-configurar-o-use-case-de-recuperacao-de-cadastro |
| URL | https://linear.app/sendspeed/issue/SEND-515/1-validar-e-configurar-o-use-case-de-recuperacao-de-cadastro-na-userin |

## Descrição

**Como** Apostou (cliente), via UserIn

**Quero** que, após o usuário fechar o modal de registro, seja apresentado um modal com criativo da Apostou e trocado o banner interno do registro, levando o usuário de volta ao cadastro

**Para** aumentar a taxa de cadastros completos

### 📈 Use Case

Usuários abrem o modal de registro e fecham sem concluir. Ao fechar, a UserIn exibe (sem delay) um modal de recuperação com criativo estático da Apostou e troca o banner interno do registro via Smart Block; ao interagir, o modal de registro reabre. Roda no site da Apostou (whitelabel NGX) sem integração em tempo real. Validação funcional na homologação da Apostou; validação de impacto em produção, por antes/depois (A/B indisponível na ferramenta).

### ✅ Critérios de aceite

* Ao fechar o modal de registro, o modal de recuperação aparece imediatamente (sem delay), com o criativo estático da Apostou
* O banner interno do registro é trocado via Smart Block pela peça da Apostou
* Ao interagir com o modal de recuperação, o modal de registro é reaberto
* Exibido no máximo 1x por sessão (evita loop fechar→recuperação→registro→fechar)
* Criativos são imagens estáticas (não GIF/vídeo), validados sem travamento em device antigo/3G
* Ligável/desligável por flag, sem novo deploy
* DoD configuração (homologação Apostou): modal, troca de banner via Smart Block e reabertura do registro funcionam ponta a ponta
* DoD validação de impacto (produção): instrumentação de eventos + medição antes/depois com baseline definido, resultado tratado como direcional (não causal)

### 🧩 Cenários de teste

* Fechar o modal de registro → recuperação aparece imediatamente com o criativo correto
* Banner interno trocado via Smart Block pela peça correta
* Interagir com a recuperação → registro reabre
* Fechar de novo na mesma sessão → recuperação não reaparece (1x/sessão)
* Device antigo/3G → imagens estáticas carregam sem travar
* Flag desligada → nada aparece, fluxo normal
* Homologação Apostou → fluxo completo (modal + banner Smart Block + reabertura) validado
* Eventos do funil disparam (exibido / banner trocado / reaberto / concluído)

### Medição (antes/depois)

* Universo: usuários que fecharam o modal de registro
* Métrica primária: taxa de conclusão de cadastro (concluídos ÷ quem fechou o registro), janela depois vs baseline antes
* Baseline: janela comparável (mesmo mix de campanha/tráfego, volume suficiente)
* Resultado é direcional, não causal — confundido por campanha/sazonalidade; não cravar causalidade

## Histórico de status
- To-do (unstarted): 2026-06-22T17:47:43.242Z → 2026-06-24T17:09:59.289Z
- In Progress (started): 2026-06-24T17:09:59.289Z → atual

## Relações
—

## Anexos
—
