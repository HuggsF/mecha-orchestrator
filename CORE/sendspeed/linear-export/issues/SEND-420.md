# SEND-420 — 🚀 - Liquid: Resolver variáveis do payload do webhook nos templates

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | Urgent |
| Responsável | Vinicius Carneiro |
| Time | Sendspeed |
| Projeto | — |
| Labels | Implementação, User Story, UserIn |
| Parent | — |
| Criada | 2026-03-20T14:46:06.702Z por Vinicius Carneiro |
| Iniciada | 2026-03-20T19:02:55.503Z |
| Concluída | 2026-04-01T12:10:27.601Z |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-420--liquid-resolver-variaveis-do-payload-do-webhook-nos |
| URL | https://linear.app/sendspeed/issue/SEND-420/liquid-resolver-variaveis-do-payload-do-webhook-nos-templates |

## Descrição

> **Como** desenvolvedor configurando jornadas automatizadas
> **Quero** que as variáveis Liquid nos templates RCS sejam resolvidas usando dados do payload do webhook que iniciou a jornada
> **Para** personalizar mensagens em tempo real com dados externos (nome do jogador, valor do depósito, tipo de evento) sem depender apenas do perfil armazenado na plataforma.

**Puxar da Branch do Paulo para começar a trabalhar nessa história**

---

# 📈 Use Case: Mensagem de recuperação com dados do evento externo

A plataforma de jogos SevenX envia um webhook para a Userin quando um jogador acumula 5 derrotas consecutivas. O payload contém `{ "name": "Carlos", "losses": 5, "lastGame": "Fortune Tiger" }`. A jornada usa o template RCS "Recuperação" com o texto: "Oi {{ name }}, sabemos que {{ lastGame }} não foi fácil. Aqui está um bônus especial para você!". O Liquid deve resolver `{{ name }}` → "Carlos" e `{{ lastGame }}` → "Fortune Tiger" usando os dados do webhook, não do perfil.

# ✅ Critérios de aceite:

* O payload do webhook (`POST /offsite/trigger`) deve ser capturado e disponibilizado como contexto adicional para resolução de variáveis Liquid.
* O `liquidResolver` deve receber o payload como `enrichedData`, permitindo resolução de variáveis que não existem no perfil.
* Variáveis do perfil têm prioridade sobre variáveis do webhook (se existirem em ambos).
* Variáveis com default (`{{ name:Jogador }}`) devem funcionar quando nem perfil nem webhook possuem o valor.
* O `name` do template RCS (identificador no provedor) também deve ser resolvível via Liquid se necessário.

> **[Imagem 1 — transcrição]:** Screenshot de UI da plataforma UserIn (logo "UserIn" no topo esquerdo; topo direito "Português (Brasil)" e avatar "User Donald / User Donald Company"). Sidebar de navegação à esquerda com itens: Início, Segmentos, Objetos, Regras, Companion, Jornadas, Audiência, Campanhas (selecionado/destacado), Disparos, Segurança, Insights, Setup Empresa, Configurações. Conteúdo principal: seção "⚡ Canal de Envio" com quatro opções em botões — "SMS (em breve)", "RCS (em breve)" (selecionado, roxo), "WhatsApp (em breve)", "Email (em breve)". Abaixo, seção "💬 Mensagem" com subtítulo "Configure o conteúdo rico RCS: Rich Card, Carrossel ou Vídeo". Há um botão "{ } Variavel" e a dica "Use {{campo:padrao}} para personalizar". Campo de texto (textarea) com conteúdo "{{" e contador "2 caracteres". Mais abaixo, painel "Conteúdo RCS" com três abas: "Rich Card" (selecionada, azul), "Carrossel", "Vídeo". Área de upload tracejada "Clique para enviar" (ícones de imagem/vídeo), campos "Título do card" e um textarea com "{{", campo "Ver mais" com campo de "URL" ao lado (ícone de link) e um botão "+ Botão".

> **[Imagem 2 — transcrição]:** Screenshot de UI do editor de mensagem mostrando o seletor de variáveis (dropdown "Buscar variável...") aberto. Cabeçalho "Conteúdo" e label "Mensagem" com contador "0/3072". Textarea com placeholder "Comece a escrever a sua mensagem..." com ícone de emoji e botão "{ } Variável". Abaixo "UTF-8 Bytes: 0". Seção "Ações sugeridas (0/11) (opcional)" com texto "Ofereça aos clientes até 11 sugestões de respostas ou ações rápidas, como chamar um número ou co... localização." e link "+ ADICIONAR SUGESTÃO". Rodapé com "Salvar rascunho" e botão azul "Revisa..." (cortado). O dropdown aberto lista variáveis sob a categoria "PERFIL": "Primeiro Nome" (contact.firstName, ex: João), "Sobrenome" (contact.lastName, ex: Silva), "Email" (contact.email, ex: joao@email.com), "Telefone" (contact.phone, ex: +5511999...), "ID do Usuário" (parcialmente visível). No rodapé do dropdown há um campo "Campo custom: dynamicFields.signals.meuCampo".

# 🧩 Cenários de teste:

- [ ] Webhook com `{ "name": "Carlos" }` → template com `{{ name }}` resolve para "Carlos".
- [ ] Webhook com `{ "lastGame": "Fortune Tiger" }` e perfil sem `lastGame` → resolve para "Fortune Tiger".
- [ ] Perfil com `name: "João"` e webhook com `name: "Carlos"` → resolve para "João" (perfil tem prioridade).
- [ ] Template com `{{ city:São Paulo }}` sem valor no perfil ou webhook → resolve para "São Paulo".
- [ ] Webhook sem payload → variáveis são resolvidas apenas pelo perfil normalmente.
- [ ] Variáveis aninhadas do webhook (`{{ data.transaction.amount }}`) resolvem corretamente.

## Histórico de status
- Backlog (backlog): 2026-03-20T14:46:06.702Z → 2026-03-20T15:20:36.557Z
- To-do (unstarted): 2026-03-20T15:20:36.557Z → 2026-03-20T19:02:55.512Z
- In Progress (started): 2026-03-20T19:02:55.512Z → 2026-03-23T17:43:58.601Z
- Pull Request (started): 2026-03-23T17:43:58.601Z → 2026-03-24T17:29:10.861Z
- Product Review (started): 2026-03-24T17:29:10.861Z → 2026-03-25T13:31:29.402Z
- Done (started): 2026-03-25T13:31:29.402Z → 2026-03-25T13:31:37.986Z
- Product Review (started): 2026-03-25T13:31:37.986Z → 2026-03-31T18:24:38.053Z
- Release (started): 2026-03-31T18:24:38.053Z → 2026-04-01T12:10:27.615Z
- Released (completed): 2026-04-01T12:10:27.615Z → atual

## Relações
—

## Anexos
—
