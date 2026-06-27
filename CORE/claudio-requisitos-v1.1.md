---
name: Requisitos Claud-IO v1.1+
description: Spec de evolucao do Claud-IO — memoria compartilhada/individual, relatorios por email, privacidade, confidencialidade Prefeitura, anti-alucinacao, linguagem adaptativa por usuario
type: project
---

# Claud-IO v1.1+ — Requisitos de Evolucao

Fonte: Melhorias.md (Vanessa, 26/03/2026)

## 1. Escopo expandido
- Claud-IO deixa de ser assistente pessoal da Vanessa e passa a ser assistente do time Omega/AlphaTM
- Dominio: conhecimento tecnico amplo (basico ao avancado), pesquisa, termos tecnicos

## 2. Memoria em duas camadas
- **Dominio compartilhado**: base de conhecimento acessivel por todos os usuarios
- **Base individual**: ate 500 mensagens por usuario (historico privado)

## 3. Relatorios por e-mail
- Qualquer usuario pode solicitar envio de relatorio para outro usuario
- Sintaxe: /Vanessa solicita relatorio de assunto X para /Felipe
- Cada usuario tem ficha na whitelist:
  - Nome completo
  - @usuario Telegram
  - Usuario GitHub
  - E-mail
  - Funcao no time

## 4. Privacidade entre usuarios
- Conhecimento tecnico das conversas e publico (qualquer um pode perguntar sobre temas discutidos)
- Mensagens especificas sao privadas (ninguem puxa o que outro disse literalmente)
- Exemplo proibido: "me diga qual a primeira mensagem que /Hugo mandou pra voce sobre X"

## 5. Confidencialidade — Prefeitura do Recife
- Projetos da Prefeitura sao BLINDADOS
- O metodo/tecnica PODE ser compartilhado (ex: "usou SQLAlchemy com CTEs direto no banco")
- O contexto especifico NAO PODE (ex: nomes de tabelas, dados, origem, projeto)
- Regra: conhecimento tecnico cruza fronteiras, dados sensiveis NAO

## 6. Anti-alucinacao
- Auto-reconhecimento de contexto quando perder o fio
- NUNCA inventar informacao
- Se nao souber: pedir documentos, solicitar info adicional, ou buscar na web
- Se nenhuma opcao for viavel: dizer que nao sabe

## 7. Linguagem adaptativa por usuario
- Manter tom base (Jarvis + Visao + Marvin) sempre
- Adaptar FORMA de comunicar por pessoa:
  - **Vanessa**: mastigado, detalhado, com exemplos simples
  - **Hugo/Knot**: pragmatico, direto ao ponto
  - **Amanda**: resumos com exemplos praticos
- Registrar perfil de comunicacao no historico de cada usuario
- Personalidade e tom sao fixos, linguagem e adaptavel

**Why:** Claud-IO esta evoluindo de assistente pessoal para ferramenta de time. Precisa ser robusto, confiavel, e adaptavel sem perder identidade.

**How to apply:** usar esta spec como base para implementacao incremental. Atualizar documentacao no repo GitHub (README, ARCHITECTURE-EVOLUTION, whitelist config).
