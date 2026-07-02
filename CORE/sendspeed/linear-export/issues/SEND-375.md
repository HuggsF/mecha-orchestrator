# SEND-375 — Bugs Audiência UserIn - Bug visual no modal de mapear colunas com muitas colunas

| Campo | Valor |
| -- | -- |
| Status | Released (completed) |
| Prioridade | Urgent |
| Responsável | Hugo Fernandes |
| Time | Sendspeed |
| Projeto | — |
| Labels | — |
| Parent | — |
| Criada | 2026-03-09T15:50:39.462Z por paulo.ribeiro@sendspeed.com |
| Iniciada | 2026-03-31T18:30:44.969Z |
| Concluída | 2026-06-22T17:15:56.570Z |
| Arquivada | — |
| Vencimento | — |
| Branch | hugofernandes/send-375-bugs-audiencia-userin-bug-visual-no-modal-de-mapear-colunas |
| URL | https://linear.app/sendspeed/issue/SEND-375/bugs-audiencia-userin-bug-visual-no-modal-de-mapear-colunas-com-muitas |

## Descrição

**Descrição:** O modal "Mapear Colunas" na funcionalidade de importação de arquivos apresenta bug visual quando a tabela de preview tem muitas colunas. O conteúdo fica cortado/sobreposto, dificultando a visualização e o mapeamento correto das colunas do arquivo importado.

**Caminho:** Audiência > Listas > Estáticas > Criar listas > Importar arquivo

**Sugestão de melhoria:** Ajustar o layout do modal para suportar visualização de tabelas com muitas colunas. Implementar scroll horizontal na área de preview da tabela ou redimensionar colunas dinamicamente.

> **[Imagem 1 — transcrição]:** Screenshot de UI de um modal da plataforma SendSpeed. Título do modal: "Mapear Colunas" (ícone de upload), com subtítulo "Indique qual coluna corresponde a cada campo". No topo direito da tela há indicadores "BR Português (Brasil)" e avatar "User Donald Company". À esquerda, fora do modal, vê-se "Voltar para Listas", o nome da lista "teste" / "tsetset" (badge "Est..."), aba "Membros (0)" e botão verde "Adicionar Contatos". Dentro do modal há uma seção "Preview do arquivo" com uma tabela de muitas colunas: nome, email, telefone, celular, cidade, estado, pais, cep, endereco, data_nascimento, genero. Linhas de dados: (1) Ana Paula Silva, ana.silva@email.c..., (11) 3456-7890, (11) 98765-4321, São Paulo, SP, Brasil, 01310-100, Av. Paulista 1000, 1990-03-15, Feminino; (2) Carlos Eduardo So..., carlos.souza@ema..., (21) 3123-4567, (21) 99123-4567, Rio de Janeiro, RJ, Brasil, 20040-020, Rua do Ouvidor 50, 1985-07-22, Masculino; (3) Fernanda Costa Li..., fernanda.lima@e..., (31) 3654-3210, (31) 97654-3210, Belo Horizonte, MG, Brasil, 30130-110, Av. Afonso Pena 2..., 1993-11-05, Feminino. As colunas da direita ficam cortadas/sobrepostas na borda do modal, demonstrando o bug visual. Abaixo, seção "Mapeamento de colunas:" com dropdowns: Telefone = "celular (ex: (11) 98765-4321)"; Nome = "nome"; LocalStorage ID = "Não mapear"; Email = "email"; External ID = "Não mapear" (estes últimos dois campos aparecem cortados à direita, fora da área visível do modal). Rodapé com caixa azul-clara: "Arquivo: contatos2.csv" e "Tamanho: 0.7 KB".

---

## 🎯 Priorização RICE — Score: 24.0 (#4 no To-do)

| Reach | Impact | Confidence | Effort | Score |
| -- | -- | -- | -- | -- |
| 6 | 1 (medium) | 100% | 0.25 meses | **24.0** |

**Justificativa:** Quick win de alto valor. Reach 6: usuários importando CSVs com muitas colunas são bloqueados visualmente. Impacto medium (1): modal fica inutilizável com colunas cortadas, impedindo mapeamento correto. Confidence 100%: bug visual claro, fix é overflow-x no container da tabela. Esforço mínimo (0.25 meses): adicionar scroll horizontal + ajustar responsividade do modal.

## Histórico de status
- Backlog (backlog): 2026-03-09T15:50:39.462Z → 2026-03-20T13:19:45.156Z
- Refining (backlog): 2026-03-20T13:19:45.156Z → 2026-03-31T14:49:25.608Z
- To-do (unstarted): 2026-03-31T14:49:25.608Z → 2026-03-31T18:30:45.131Z
- In Progress (started): 2026-03-31T18:30:45.131Z → 2026-06-22T17:15:56.631Z
- Released (completed): 2026-06-22T17:15:56.631Z → atual

## Relações
—

## Anexos
- fix(SEND-375): corrigir overflow no modal Mapear Colunas — https://github.com/sendspeed0/sendspeed-engage-ai-flow-08/pull/34
