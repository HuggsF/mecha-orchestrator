# SEND-385 — Instalação e configuração do Microsoft Clarity — UserIn

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | High |
| Responsável | — |
| Time | Sendspeed |
| Projeto | — |
| Labels | UserIn, User Story |
| Parent | — |
| Criada | 2026-03-13T14:53:45.603Z por Vinicius Carneiro |
| Iniciada | — |
| Concluída | 2026-06-22T17:16:33.510Z |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-385-instalacao-e-configuracao-do-microsoft-clarity-userin |
| URL | https://linear.app/sendspeed/issue/SEND-385/instalacao-e-configuracao-do-microsoft-clarity-userin |

## Descrição

> **Contexto**
>
> Implementar o Microsoft Clarity na plataforma UserIn para rastreamento de comportamento de usuários autenticados. A integração deve identificar cada usuário pelo ID interno, enriquecer as sessões com atributos de role e clientId, e estar ativa em todas as páginas da aplicação.

---

**Etapa 1 — Criar o projeto no Clarity**

**1**

Criar uma conta e projeto em `clarity.microsoft.com`.

**2**

Acessar `Settings → Overview` e copiar o **Project ID** gerado. Esse ID é necessário nas etapas seguintes.

---

**Etapa 2 — Instalar o script base**

Dois caminhos possíveis. Usar apenas um deles:

**Via NPM (recomendado)**

**1**

Instalar o pacote:

```
npm install @microsoft/clarity
```

**2**

Inicializar no entry point da aplicação (`main.ts` ou equivalente), antes da montagem dos componentes:

```
import Clarity from '@microsoft/clarity'

Clarity.init('SEU_PROJECT_ID')
```

**Via script manual**

**1**

Acessar `Settings → Setup → Get tracking code` no painel do Clarity e copiar o snippet gerado.

**2**

Colar o snippet dentro do `<head>` global da aplicação.

---

**Etapa 3 — Identify API (mapeamento de usuários)**

**1**

Chamar a Identify API logo após a autenticação do usuário, e em cada carregamento de página da aplicação autenticada.

**Via NPM**

```
import Clarity from '@microsoft/clarity'

Clarity.identify(
  currentUser.id,    // custom-id — obrigatório
  undefined,         // custom-session-id — opcional
  undefined,         // custom-page-id — opcional
  currentUser.name   // friendly-name — opcional, aparece no dashboard
)
```

**Via script manual**

```
window.clarity(
  'identify',
  currentUser.id,
  undefined,
  undefined,
  currentUser.name
)
```

O `custom-id` é o único parâmetro obrigatório. O Clarity faz hash desse valor no client antes de enviar — não trafega em plain text. O `friendly-name` é o valor exibido no dashboard no lugar do hash.

Evitar usar e-mail como `custom-id` sem validação jurídica prévia — é considerado PII mesmo que seja enviado com hash.

---

**Etapa 4 — Custom Tags (role e clientId)**

**1**

Adicionar as custom tags após a chamada de identify. Tags ficam disponíveis nos filtros do painel em até 2 horas após as primeiras sessões gravadas.

**Via NPM**

```
Clarity.set('role', currentUser.role)
Clarity.set('client_id', currentUser.clientId)
```

**Via script manual**

```
window.clarity('set', 'role', currentUser.role)
window.clarity('set', 'client_id', currentUser.clientId)
```

Os valores de `role` devem seguir os tipos definidos na plataforma. Alinhar com o time de produto antes da implementação. Não há limite de número de custom tags por projeto.

---

**Etapa 5 — Verificação da instalação**

**1**

Acessar o painel do projeto no Clarity. Sessões em tempo real aparecem imediatamente após a instalação correta do script.

**2**

Confirmar via DevTools: inspecionar a aba **Network** e verificar se há requisições POST para `https://www.clarity.ms/collect` durante a navegação.

**3**

Em Recordings, verificar se as sessões aparecem com o **Custom ID** preenchido (não apenas o Clarity ID anônimo).

---

**Critérios de aceite**

\- Script inicializado em todas as páginas da aplicação autenticada

\- Requisições POST visíveis em `clarity.ms/collect` no DevTools

\- Sessões aparecem no dashboard com Custom ID preenchido

\- Filtros por `role` e `client_id` funcionando no painel de Recordings

\- Nenhum impacto mensurável no tempo de carregamento (o script é assíncrono)

---

Impacto em códigoSim — entry point + hook de autenticação

Referência: [https://learn.microsoft.com/en-us/clarity/](https://learn.microsoft.com/en-us/clarity/)

**Nota para o dev**

Escolher apenas um caminho de instalação (NPM ou script manual) e manter consistência nas chamadas subsequentes. A Identify API e as Custom Tags têm sintaxe diferente dependendo do método escolhido — misturar os dois pode causar erros silenciosos. A chamada da Identify API deve rodar em toda navegação autenticada, não só no login.

---

## 🎯 Priorização RICE — Score: 16.0

| Reach | Impact | Confidence | Effort | Score |
| -- | -- | -- | -- | -- |
| 10 | 1 (medium) | 80% | 0.5 meses | **16.0** |

**Justificativa:** Reach 10: beneficia toda a equipe de produto com dados de UX. Impacto medium (1): habilita decisões baseadas em dados de comportamento real. Confidence 80%: Clarity bem documentado. Esforço 0.5 meses: instalação + identify + tags + validação.

## Histórico de status
- Backlog (backlog): 2026-03-13T14:53:45.603Z → 2026-03-20T12:47:25.046Z
- Refining (backlog): 2026-03-20T12:47:25.046Z → 2026-03-31T12:33:23.472Z
- To-do (unstarted): 2026-03-31T12:33:23.472Z → 2026-06-22T17:16:33.526Z
- Released (completed): 2026-06-22T17:16:33.526Z → atual

## Relações
—

## Anexos
—
