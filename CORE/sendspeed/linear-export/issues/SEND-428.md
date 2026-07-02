# SEND-428 — Especificações RCS — Validações, Alertas e Orientações por Formato

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | Medium |
| Responsável | Vinicius Carneiro |
| Time | Sendspeed |
| Projeto | — |
| Labels | — |
| Parent | — |
| Criada | 2026-03-26T01:34:05.523Z por paulo.ribeiro@sendspeed.com |
| Iniciada | 2026-04-15T16:38:14.422Z |
| Concluída | 2026-04-24T13:43:40.727Z |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-428-especificacoes-rcs-validacoes-alertas-e-orientacoes-por |
| URL | https://linear.app/sendspeed/issue/SEND-428/especificacoes-rcs-validacoes-alertas-e-orientacoes-por-formato |

## Descrição

## **Objetivo**

Definir as especificações técnicas do Google RCS Business Messaging por formato de mensagem, estabelecendo três camadas de aplicação:

1. **Validação** — o que o sistema deve bloquear ou rejeitar
2. **Alerta** — o que o sistema deve avisar sem bloquear (ex: truncagem, tamanho de arquivo)
3. **Orientação** — o que o editor deve mostrar para que o usuário saiba como usar cada formato

Fonte única: https://developers.google.com/business-communications/rcs-business-messaging/guides/learn/rich-cards
https://developers.google.com/business-communications/rcs-business-messaging/guides/build/messages/send

---

## **Ações Sugeridas (Suggested Replies e Suggested Actions)**

*Novo imput mas segue essas mesma regras para 'botões'*

**Aplica-se a TODOS os formatos: Text, Rich Card, Carousel e File.**

Ações sugeridas são botões que guiam o usuário por respostas predefinidas ou ações nativas do dispositivo. Aparecem em dois contextos:

| Contexto | Limite | Onde aparece |
| -- | -- | -- |
| **Dentro de um card** (rich card ou card do carrossel) | Máximo 4 | Abaixo do título/descrição, dentro do card |
| **Chip list** (abaixo da mensagem ou abaixo do carrossel) | Máximo 11 | Lista de chips abaixo de qualquer tipo de mensagem |

### **Regras comuns**

| Propriedade | Valor |
| -- | -- |
| Texto por ação | Máximo 25 caracteres |
| Payload de postback | Máximo 2.048 caracteres |

### **Tipos de ação**

| Tipo | Campos obrigatórios |
| -- | -- |
| **Responder** (Suggested Reply) | Texto do botão + postback data |
| **Abrir URL** (Open URL) | Texto + URL (http/https) |
| **Abrir URL em Webview** | Texto + URL + modo (Full / Half / Tall) |
| **Discar telefone** (Dial) | Texto + número de telefone |
| **Mostrar localização** (View Location) | Texto + latitude/longitude OU query de endereço |
| **Compartilhar localização** (Share Location) | Texto |
| **Criar evento no calendário** (Calendar) | Texto + título (100 chars) + descrição (500 chars) + data/hora início + data/hora fim |

### **Comportamento da chip list**

* A chip list só é exibida enquanto a mensagem for a **última da conversa**. Mensagens subsequentes a sobrescrevem.
* A chip list **não deve repetir** as opções que já estão dentro do card.
* Em carrosséis, a chip list **não deve funcionar como seletor** de itens do carrossel.

### **Comportamento no carrossel full-screen**

| Tipo de ação | O que acontece ao tocar |
| -- | -- |
| Abrir URL / Webview | Abre URL; ao voltar, restaura a visualização full-screen |
| Discar / Mostrar localização / Calendário | Abre o app correspondente; ao voltar, restaura full-screen |
| Compartilhar localização | Fecha o full-screen, abre Google Maps; ao enviar, volta ao chat normal |
| Responder (Reply) | Fecha o full-screen, envia a resposta no chat normal |

### **Alertas e Orientações UX**

* **Orientação geral:** "Ações sugeridas guiam o usuário para respostas rápidas ou ações nativas do celular (ligar, abrir mapa, criar evento). Limite-se às ações relevantes para o contexto da mensagem."
* **Alerta chip list:** "As ações sugeridas abaixo da mensagem ficam visíveis apenas enquanto esta for a última mensagem da conversa. Uma nova mensagem as oculta."
* **Alerta Open URL (vigente desde 09/03/2026):** "O Google Messages exibe a URL real abaixo dos botões 'Abrir URL' em rich cards e carrosséis. Prefira URLs curtas e amigáveis."
* **Helper text URL:** "Use URLs completas e diretas para que o ícone do app apareça no botão. URLs encurtadas exibem ícone genérico."
* **Alerta máximo atingido:** Dentro do card: "Máximo de 4 ações por cartão atingido." / Chip list: "Máximo de 11 ações sugeridas atingido."

telas infobip

> **[Imagem 1 — transcrição]:** Screenshot de UI (editor Infobip RCS) — Painel de configuração de botão "Botão 1 - Mostrar localização". Dropdown de tipo com valor "Mostrar localização". Campos: "Texto" (placeholder "Insira o texto", com ícones de emoji e {} de variável); "Latitude" (placeholder "Insira a latitude (-90 a 90)", com ícone {}); "Longitude" (placeholder "Insira a longitude (-180 a 180)", com ícone {}); "Etiqueta (opcional)" (placeholder "Inserir etiqueta", ícones emoji e {}); "Retorno" (placeholder "Digite o valor de postback", ícone {}). Ícones de duplicar, excluir e recolher no cabeçalho do card.

> **[Imagem 2 — transcrição]:** Screenshot de UI (editor Infobip RCS) — Painel de configuração "Botão 1 - Solicitar localização". Dropdown de tipo "Solicitar localização". Campos: "Texto" (placeholder "Insira o texto", ícones emoji e {}); "Retorno" (placeholder "Digite o valor de postback", ícones emoji e {}). Cabeçalho com ícones de duplicar, excluir e recolher.

> **[Imagem 3 — transcrição]:** Screenshot de UI (editor Infobip RCS) — Painel "Botão 1 - Responder". Dropdown de tipo "Responder". Campos: "Texto" (placeholder "Insira o texto", ícones emoji e {}); "Retorno" (placeholder "Digite o valor de postback", ícone {}).

> **[Imagem 4 — transcrição]:** Screenshot de UI (editor Infobip RCS) — Painel "Botão 1 - Criar evento no calendário" (com ícone de alerta triangular vermelho). Dropdown de tipo "Criar evento no calendário". Campos: "Texto" (placeholder "Insira o texto"); "Retorno" (placeholder "Insira o valor"); "Data do evento" com opções de rádio "Fixa" (selecionado) e "Dinâmico"; "Data de início" (campo "Selecionar data" + "Select time", ambos com borda vermelha e erro "Inserir data inicial" com ícone de alerta); "Data de finalização" (campo "Selecionar data" + "Select time", borda vermelha, erro "Inserir data final"); "Deslocamento UTC" (dropdown "UTC±0 (horário de Greenwich, horário da Europa Oriental)"); "Título do evento" (placeholder "Inserir título do evento"); "Descrição do evento" (placeholder "Inserir descrição do evento"). Link no rodapé "+ ADICIONAR BOTÃO".

> **[Imagem 5 — transcrição]:** Screenshot de UI (editor Infobip RCS) — Seção "Botões do cartão avançado (1/4) (opcional)" com subtítulo "Adicione até 4 botões que aparecerão no cartão avançado." e ícone de lixeira. Card "Botão 1 - Discar telefone" (com ícone de alerta vermelho). Dropdown de tipo "Discar telefone". Campos: "Texto" (placeholder "Insira o texto", borda vermelha, erro "Texto não pode ficar vazio"); "Número de telefone" (placeholder "+14155552671", borda vermelha, erro "O número de telefone não pode ficar vazio"); "Retorno" (placeholder "Digite o valor de postback", ícone {}).

> **[Imagem 6 — transcrição]:** Screenshot de UI (editor Infobip RCS) — Painel "Botão 1 - URL aberto". Dropdown de tipo "URL aberto". Campos: "Texto" (placeholder "Insira o texto", ícones emoji e {}); "URL do website" (placeholder "https:// ou http://", ícone {}); "Retorno" (placeholder "Digite o valor de postback", ícone {}); "Aparência da URL para os usuários" com opções de rádio "Browser" (selecionado) e "Webview".

---

## **Formato 1 — TEXT (Mensagem de Texto)**

Mensagem de texto simples. Ideal para comunicação direta sem necessidade de mídia ou layout visual.

### **Campos e Validação**

| Campo | Regra | Comportamento no editor |
| -- | -- | -- |
| Mensagem | Obrigatória, não pode ser vazia | Botão de avançar desabilitado se vazio |
| Tamanho | Máximo 3.072 caracteres | Contador regressivo; bloqueia no limite |
| Emojis | Permitidos | Informar que contam como 2–4 caracteres |
| Quebras de linha | Permitidas | — |

### **Ações sugeridas**

Chip list abaixo da mensagem: **máximo 11**. Ver seção "Ações Sugeridas" acima.

### **Alertas e Orientações UX**

* **Helper text — Basic Message:** "Mensagens com até 160 caracteres UTF-8 são cobradas como SMS (Basic Message). Acima disso, a cobrança segue o modelo RCS."
* **Helper text — link preview:** "Se a mensagem contiver uma URL, o dispositivo pode gerar um preview automático (imagem e título) se o site tiver tags OpenGraph configuradas."
* **Helper text — emojis:** "Caracteres especiais como emojis contam como 2 a 4 caracteres ou mais."

---

## **Formato 2 — RICH CARD (Cartão Avançado)**

Combina mídia, texto e ações em uma única mensagem. Ideal para destacar um único produto, oferta ou informação.

**Regra de conteúdo mínimo:** ao menos um dos três deve estar presente: mídia, título ou descrição.

### **Layout Vertical (mídia no topo)**

| Propriedade | Valor |
| -- | -- |
| Aspect ratios suportados | 2:1 / 16:9 / 7:3 |
| Altura da mídia — Curto | 112 dp |
| Altura da mídia — Médio | 168 dp |
| Altura da mídia — Alto | 264 dp |
| Altura mínima do card | 112 dp |
| Altura máxima do card | 344 dp |

> Se a mídia não corresponder à altura selecionada, o sistema aplica zoom e corte centralizado automático.

### **Layout Horizontal (mídia à esquerda ou direita)**

| Propriedade | Valor |
| -- | -- |
| Largura fixa da mídia | 128 dp |
| Aspect ratio | Sem ratio fixo |
| Altura | Escala com o conteúdo de texto |

### **Mídia**

| Propriedade | Detalhe |
| -- | -- |
| Imagem | JPEG, JPG, GIF, PNG |
| Vídeo | H.263, M4V, MP4, MPEG, MPEG-4, WebM |
| Áudio | **Não suportado em rich cards** |

### **Textos**

| Campo | Limite | Comportamento |
| -- | -- | -- |
| Título | 200 caracteres | Contador regressivo |
| Descrição | 2.000 caracteres | Contador regressivo |

> Caracteres especiais como emojis contam como 2 a 4 caracteres ou mais.

### **Thumbnail**

| Propriedade | Valor |
| -- | -- |
| Tamanho máximo | 100 KB |
| Tamanho recomendado | 50 KB ou menos |
| Formatos aceitos | JPEG, JPG, GIF, PNG |
| Aspect ratio | Deve corresponder ao da mídia original |

> A thumbnail permanece visível durante o download e em caso de falha. Se não fornecida, o dispositivo exibe um ícone padrão do tipo de arquivo. Tocar na thumbnail abre a visualização full-screen da mídia.

### **Ações sugeridas**

* Dentro do card: **máximo 4**
* Chip list abaixo do card: **máximo 11** (não deve repetir as do card)

Ver seção "Ações Sugeridas" acima.

### **Alertas e Orientações UX**

* **Helper text — mídia vertical:** "Se a imagem não corresponder à altura selecionada, o sistema aplica zoom e corte centralizado. Para controlar o resultado, especifique uma thumbnail."
* **Helper text — mídia horizontal:** "A mídia terá largura fixa de 128dp com altura proporcional ao texto."
* **Helper text — thumbnail:** "A thumbnail aparece enquanto a mídia carrega e permanece visível em caso de falha de download. Deve ter o mesmo aspect ratio da mídia original. Recomendado: até 50 KB."
* **Alerta sem conteúdo:** "Adicione ao menos mídia, título ou descrição para continuar."

---

## **Formato 3 — CAROUSEL (Carrossel)**

Conjunto de cartões verticais em scroll horizontal. Ideal para comparar múltiplos itens em uma única mensagem.

**Apenas cards verticais são permitidos. Todos os cards escalam para a altura do card mais alto.**

### **Estrutura Geral**

| Propriedade | Regra | Comportamento no editor |
| -- | -- | -- |
| Número de cards | **Mínimo 2 / Máximo 10** | Botão "Adicionar" some ao atingir 10. Bloqueia salvar com menos de 2 |
| Largura | Pequeno (180dp fixa) ou Médio (296dp fixa) | Select único — aplica a todos os cards |
| Altura máxima — Small | 542 dp | — |
| Altura máxima — Medium | 592 dp | — |

### **Por card**

| Campo | Limite | Comportamento |
| -- | -- | -- |
| Mídia | Opcional — URL http/https | Validação inline |
| Tipo de mídia | Imagem (JPEG, PNG, GIF) ou Vídeo (MP4, WebM, etc.) | Áudio não suportado |
| Altura da mídia | Curto (112dp) / Médio (168dp) / Alto (264dp) | Select |
| Título | 200 caracteres (opcional) | Contador regressivo |
| Descrição | 2.000 caracteres (opcional) | Contador regressivo |
| Botões dentro do card | Máximo 4 | Botão "Adicionar" some ao atingir 4 |
| Texto por botão | 25 caracteres | Contador por campo |

### **Thumbnail (por card)**

Mesmas regras do Rich Card: máximo 100 KB (recomendado 50 KB), mesmo aspect ratio da mídia, formatos JPEG/JPG/GIF/PNG.

### **Ações sugeridas**

* Dentro de cada card: **máximo 4**
* Chip list abaixo do carrossel inteiro: **máximo 11** (não deve repetir opções dos cards nem funcionar como seletor de itens)

Ver seção "Ações Sugeridas" acima.

### **Truncagem automática**

Quando o conteúdo de um card excede a altura máxima, o Google aplica truncagem nesta ordem:

1. Descrição reduzida a 1 linha
2. Título reduzido a 1 linha
3. Sugestões removidas
4. Descrição removida completamente
5. Título removido completamente

> O Google ativa **automaticamente** uma visualização full-screen quando há truncagem. O usuário toca na área de texto ou no botão "Mais" para expandir. Não requer configuração do desenvolvedor.

### **Full-screen (especificações)**

| Propriedade | Valor |
| -- | -- |
| Altura da mídia | 264 dp (sempre Tall) |
| Largura da mídia | Largura da tela menos 32 dp (16 dp de margem por lado) |
| Scroll vertical | Disponível quando o texto ultrapassa a área visível |
| Swipe horizontal | Navega entre os cards |
| Sugestões | Permanecem fixas ("floating") na base da tela |

### **Alertas e Orientações UX**

* **Alerta ao salvar com 1 card:** "O carrossel precisa de no mínimo 2 cartões. Adicione mais um ou mude para o formato Cartão Avançado."
* **Alerta de truncagem potencial:** "Cartões com muito texto podem ser cortados automaticamente pelo dispositivo. Prefira títulos curtos e descrições concisas."
* **Helper text — largura:** "Pequeno (180dp) é ideal para listas longas com muitos itens. Médio (296dp) destaca melhor cada item com mais espaço para texto."
* **Helper text — geral:** "Ideal para comparar múltiplos produtos, planos ou opções. O primeiro item deve ser a escolha mais relevante."
* **Helper text — escala:** "Todos os cards escalam para a altura do card mais alto. Se o conteúdo não preencher a altura mínima, espaço em branco é adicionado na base."

---

## **Formato 4 — FILE (Arquivo)**

Envio de arquivo como mídia standalone. Ideal para documentos, vídeos longos ou arquivos de áudio que não se encaixam em rich card.

### **Campos e Validação**

| Campo | Regra | Comportamento |
| -- | -- | -- |
| URL do arquivo | Obrigatória — http/https | Validação inline |
| Thumbnail | Opcional — URL http/https | Máximo 100 KB (recomendado 50 KB) |

### **Formatos suportados**

| Tipo | Formatos | Funciona em Rich Card? |
| -- | -- | -- |
| Imagem | JPEG, JPG, GIF, PNG | Sim |
| Vídeo | H.263, M4V, MP4, MPEG, MPEG-4, WebM | Sim |
| Áudio | AAC, MP3, OGG, 3GPP, MP4 audio | **Não** — apenas como arquivo standalone |
| PDF | .pdf | Apenas Índia (Google Messages) |

### **Ações sugeridas**

Chip list abaixo do arquivo: **máximo 11**. Ver seção "Ações Sugeridas" acima.

### **Alertas e Orientações UX**

* **Helper text — thumbnail:** "Sem thumbnail, o dispositivo exibe um ícone genérico do tipo de arquivo. Recomendado: até 50 KB, mesmo aspect ratio do arquivo."
* **Alerta PDF:** "Arquivos PDF só são suportados no Google Messages na Índia."
* **Helper text — áudio:** "Áudio é suportado como arquivo standalone mas NÃO funciona dentro de rich cards ou carrosséis."
* **Helper text — geral:** "Use este formato para documentos, vídeos longos ou áudio. Para mensagens com texto e botões, prefira o Cartão Avançado."

---

## **Limites Gerais (todos os formatos)**

### **Tamanho de arquivo**

| Propriedade | Limite |
| -- | -- |
| Arquivo único (qualquer mídia) | 100 MiB |
| Total de anexos por mensagem | 100 MiB |
| Payload JSON (AgentMessage) | 250 KB |
| Texto da mensagem | 3.072 caracteres |

> 1 MiB = 1.048.576 bytes. O limite de 250 KB do payload aplica-se à estrutura JSON da mensagem, não ao arquivo de mídia (que é referenciado via URL ou upload separado).

### **Cache e Entrega**

| Propriedade | Valor |
| -- | -- |
| Cache de mídia | 60 dias (File ID reutilizável) |
| Retenção de mensagens não entregues | 30 dias |
| TTL máximo (expireTime / ttl) | 15 dias após o envio |
| TTL mínimo recomendado | 10 segundos |
| Status entregue no prazo | DELIVERED |
| Status expirado sem entrega | TTL_EXPIRATION_REVOKED |
| Dispositivo sem RCS | Erro 404 NOT_FOUND — acionar fallback |
| Recurso não suportado | Erro 400 INVALID_ARGUMENT — mensagem não entregue |
| Fallback quando RCS indisponível | SMS / MMS (configurável) |

**Orientação UX — cache:** "Não use URLs únicas para o mesmo arquivo. A plataforma não suporta alto volume de URLs únicas. Reutilize a mesma URL para arquivos idênticos."

**Orientação UX — forceRefresh:** "Defina forceRefresh como false para evitar atraso na entrega. Usar true força novo download mesmo com cache válido."

---

## **Fontes**

https://developers.google.com/business-communications/rcs-business-messaging/guides/learn/rich-cards

https://developers.google.com/business-communications/rcs-business-messaging/guides/build/messages/send

---

## 🎯 Priorização RICE — Score: 4.8

| Reach | Impact | Confidence | Effort | Score |
| -- | -- | -- | -- | -- |
| 6 | 2 (high) | 80% | 2 meses | **4.8** |

**Justificativa:** Card de documentação técnica que serve de base para @SEND-426 e @SEND-425. Reach 6: devs implementando RCS. Impacto high (2): sem essas specs, validações ficam incompletas ou erradas. Confidence 80%: specs Google são públicas. Esforço 2 meses: implementar validações, alertas e orientações em cada formato no editor.

## Histórico de status
- Backlog (backlog): 2026-03-26T01:34:05.523Z → 2026-03-26T12:19:07.056Z
- Refining (backlog): 2026-03-26T12:19:07.056Z → 2026-03-31T12:33:51.022Z
- To-do (unstarted): 2026-03-31T12:33:51.022Z → 2026-04-02T13:07:11.617Z
- In Progress (started): 2026-04-02T13:07:11.617Z → 2026-04-02T15:33:04.710Z
- Pull Request (started): 2026-04-02T15:33:04.710Z → 2026-04-02T18:09:05.007Z
- Product Review (started): 2026-04-02T18:09:05.007Z → 2026-04-06T13:54:45.147Z
- To-do (unstarted): 2026-04-06T13:54:45.147Z → 2026-04-15T16:38:14.438Z
- In Progress (started): 2026-04-15T16:38:14.438Z → 2026-04-15T20:07:07.219Z
- Pull Request (started): 2026-04-15T20:07:07.219Z → 2026-04-16T18:14:54.199Z
- Product Review (started): 2026-04-16T18:14:54.199Z → 2026-04-24T13:43:40.751Z
- Released (completed): 2026-04-24T13:43:40.751Z → atual

## Relações
- Related to: SEND-426 — 📨 Implementar validação de regras de envio de RCS
- Related to: SEND-425 — 📱 Implementar validação de regras de envio de SMS

## Anexos
—
