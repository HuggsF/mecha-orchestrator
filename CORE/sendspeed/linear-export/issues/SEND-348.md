# SEND-348 — Bugs Ontologia UserIn - Bug visual no botão de copiar código

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | High |
| Responsável | paulo.ribeiro@sendspeed.com |
| Time | Sendspeed |
| Projeto | — |
| Labels | UserIn, Bug, User Story |
| Parent | — |
| Criada | 2026-02-24T14:06:23.321Z por paulo.ribeiro@sendspeed.com |
| Iniciada | 2026-03-02T16:37:07.479Z |
| Concluída | 2026-03-09T14:13:28.384Z |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-348-bugs-ontologia-userin-bug-visual-no-botao-de-copiar-codigo |
| URL | https://linear.app/sendspeed/issue/SEND-348/bugs-ontologia-userin-bug-visual-no-botao-de-copiar-codigo |

## Descrição

**Descrição:** O botão "Copiar" localizado no canto superior direito dos blocos de código (cURL, JavaScript, Python) nas seções de "Ingestão" e "Como alimentar [Objeto]" apresenta um bug visual. Embora a funcionalidade de copiar esteja funcionando, há um problema de exibição/layout no botão que prejudica a aparência da interface.

> **[Imagem 1 — transcrição]:** Screenshot de UI de um modal/painel do objeto **"Contact"** (badge System / contact). Subtítulo "Contacto CRM linkado ao perfil. Contem dados pessoais como nome, email, telefone." Botão "Abrir página". Métricas: **4 Campos, 1 Relações, 5 Atributos, 1 Grupos, 1 Catálogo**. Abas: Atributos, Explorador, Relações, + Campos Custom, Catálogo (1), Ingestão. Seção **"Como alimentar Contact — Código para enviar dados para esta entidade via API"**. Sub-seção "Ingerir objeto Contact completo" com abas de linguagem: cURL (ativa), JavaScript, Python. Bloco de código escuro com um `curl -X POST https://userin-ingestion-staging.fly.dev/ingest/objects` incluindo header `Authorization: Bearer ik_8cb3d511cb9b4f5e8e697c91a4c989ae`, `Content-Type: application/json` e payload JSON com objectType "contact", externalId "contact_001", attributes (firstName, lastName, email, phone, linkedAt), relationships. No canto superior direito do bloco há o botão **"Copiar"** (ícone + texto) — é onde ocorre o bug visual descrito. Abaixo, "Atualizar campos de Contact no perfil (Vários campos)" com novas abas cURL/JavaScript/Python e outro bloco de código com botão "Copiar".

**Sugestão de melhoria:** Corrigir o bug visual do botão "Copiar" para que ele seja exibido corretamente, garantindo alinhamento, espaçamento e aparência adequados dentro do bloco de código.

## Histórico de status
- Backlog (backlog): 2026-02-24T14:06:23.321Z → 2026-02-24T15:36:31.599Z
- Refining (backlog): 2026-02-24T15:36:31.599Z → 2026-03-02T12:26:53.771Z
- To-do (unstarted): 2026-03-02T12:26:53.771Z → 2026-03-02T16:37:07.489Z
- In Progress (started): 2026-03-02T16:37:07.489Z → 2026-03-03T12:12:10.920Z
- Product Review (started): 2026-03-03T12:12:10.920Z → 2026-03-03T12:12:12.426Z
- Pull Request (started): 2026-03-03T12:12:12.426Z → 2026-03-03T12:50:04.986Z
- Product Review (started): 2026-03-03T12:50:04.986Z → 2026-03-09T14:13:28.397Z
- Released (completed): 2026-03-09T14:13:28.397Z → atual

## Relações
—

## Anexos
—
