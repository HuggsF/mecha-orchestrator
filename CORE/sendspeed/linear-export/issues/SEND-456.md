# SEND-456 — 🚀 - Envio de arquivos via RCS com integração completa ao UserIn

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | Urgent |
| Responsável | andrei.garcia@externo.sendspeed.com |
| Time | Sendspeed |
| Projeto | — |
| Labels | User Story, UserIn, Implementação |
| Parent | — |
| Criada | 2026-04-14T19:33:37.375Z por Vinicius Carneiro |
| Iniciada | — |
| Concluída | 2026-06-22T17:16:06.046Z |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-456--envio-de-arquivos-via-rcs-com-integracao-completa-ao-userin |
| URL | https://linear.app/sendspeed/issue/SEND-456/envio-de-arquivos-via-rcs-com-integracao-completa-ao-userin |

## Descrição

> **Como** operador de marketing
> **Quero** fazer upload e enviar arquivos (documentos, imagens, vídeos) em templates RCS com preview, validação automática e acompanhamento de interações
> **Para** criar campanhas RCS mais ricas e interativas, monitorar o engajamento dos usuários com os arquivos e segmentar audiências baseado nas interações

---

# 📈 Use Case: 

O operador precisa criar templates RCS com arquivos anexados no editor visual da Sendspeed, visualizar preview em tempo real, enviar através do Journey Builder e acompanhar métricas de interação (cliques, downloads) via UserIn para otimizar futuras campanhas.

# ✅ Critérios de aceite:

* O sistema deve permitir upload de arquivos (documentos, imagens, vídeos) durante a criação de templates RCS no editor visual
* Deve exibir preview em tempo real dos arquivos anexados no template
* O sistema deve validar formato, tamanho e qualidade dos arquivos automaticamente
* Deve gerar URLs públicas seguras para os arquivos processados
* Os templates RCS com arquivos devem ser compatíveis com o Journey Builder para envio automatizado
* O sistema deve processar envios via Multi-Queue Kafka mantendo a infraestrutura existente
* Deve capturar e processar callbacks de fornecedores RCS sobre status de entrega
* A integração com UserIn deve registrar eventos de interação com arquivos (cliques, downloads)
* O sistema deve permitir segmentação de usuários baseada nas interações com arquivos
* Deve integrar-se aos sistemas de métricas e analytics existentes na plataforma
* As mensagens RCS enviadas devem incluir corretamente os arquivos anexados

# 🧩 Cenários de teste:

- [ ] Upload de imagem PNG de 2MB em template RCS e verificar preview instantâneo
- [ ] Tentar upload de arquivo com formato não suportado e validar mensagem de erro
- [ ] Criar jornada com template RCS contendo vídeo e verificar envio automatizado
- [ ] Simular clique em arquivo PDF enviado via RCS e verificar registro no UserIn
- [ ] Testar envio de arquivo de 10MB e verificar processamento via Kafka
- [ ] Verificar callback de fornecedor RCS sobre falha na entrega de arquivo
- [ ] Criar segmento de usuários que baixaram documentos específicos
- [ ] Validar métricas de interação com arquivos no dashboard analytics
- [ ] Testar upload simultâneo de múltiplos arquivos em um template
- [ ] Verificar comportamento com arquivo corrompido durante upload
- [ ] Testar preview de arquivo de vídeo de 50MB antes do envio
- [ ] Validar geração de URL pública para documento Word anexado

---

Funcionalidade crítica que expande significativamente as capacidades de marketing RCS da plataforma, integrando múltiplos sistemas existentes

## Histórico de status
- Backlog (backlog): 2026-04-14T19:33:37.375Z → 2026-04-14T19:36:56.955Z
- Refining (backlog): 2026-04-14T19:36:56.955Z → 2026-04-16T12:38:00.807Z
- To-do (unstarted): 2026-04-16T12:38:00.807Z → 2026-06-22T17:16:06.056Z
- Released (completed): 2026-06-22T17:16:06.056Z → atual

## Relações
—

## Anexos
—
