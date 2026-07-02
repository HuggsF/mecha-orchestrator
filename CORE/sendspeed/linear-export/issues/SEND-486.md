# SEND-486 — 2. Refatoração da estrutura de jornadas

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | High |
| Responsável | thiago.melin@sendspeed.com |
| Time | Sendspeed |
| Projeto | — |
| Labels | Melhoria, User Story, UserIn |
| Parent | — |
| Criada | 2026-06-02T18:08:25.042Z por Vinicius Carneiro |
| Iniciada | — |
| Concluída | 2026-06-22T17:50:05.364Z |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-486-2-refatoracao-da-estrutura-de-jornadas |
| URL | https://linear.app/sendspeed/issue/SEND-486/2-refatoracao-da-estrutura-de-jornadas |

## Descrição

> **Como** time de engenharia responsável pela plataforma de jornadas
> **Quero** eliminar o código redundante que trata o mesmo fluxo em múltiplos lugares, consolidando em uma estrutura única
> **Para** reduzir falhas causadas por divergência entre cópias do mesmo fluxo e tornar a manutenção mais previsível

### 📈 Use Case:

Hoje o mesmo fluxo de jornada é tratado por trechos de código duplicados; uma correção precisa ser replicada em vários pontos, e quando não é, surgem inconsistências. A refatoração consolida esses caminhos sem alterar o comportamento observável das jornadas.

### ✅ Critérios de aceite:

* Comportamento das jornadas existentes permanece idêntico (refatoração sem mudança funcional)
* Os caminhos duplicados que tratam o mesmo fluxo são consolidados em um único ponto
* Cobertura de testes dos fluxos afetados existentes antes de mexer no código (rede de segurança para regressão)

### 🧩 Cenários de teste:

- [ ] Suite de regressão das jornadas existentes passa 100% antes e depois da refatoração
- [ ] Executar as N jornadas mais usadas em produção e comparar saída antes/depois (devem ser idênticas)
- [ ] Verificar que uma correção em um fluxo não exige mais alteração em múltiplos arquivos
- [ ] Medir a métrica de baseline pós-refatoração e comparar com o valor anterior
- [ ] Teste de carga: jornada de alto volume mantém ou melhora o tempo de processamento

## Histórico de status
- To-do (unstarted): 2026-06-02T18:08:25.042Z → 2026-06-22T17:50:05.380Z
- Released (completed): 2026-06-22T17:50:05.380Z → atual

## Relações
—

## Anexos
—
