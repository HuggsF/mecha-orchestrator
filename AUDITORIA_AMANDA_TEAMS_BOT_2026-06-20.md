# 🛡️ Auditoria Técnica & Revisão de Qualidade — Ecossistema MECHA / Amanda Teams Bot

**Data:** 20/06/2026 · **Escopo:** `ops/patterns/amanda_teams_bot.py`, `AMANDA_TASKS.md`, `amanda_tasks.json`, `claw_status.json`, `MECHA_GUIDE.md`
**Status:** Correções de severidade Crítica/Alta/Média **aplicadas e verificadas** · Recomendações de arquitetura/segurança listadas para decisão.

---

## 1. Sumário executivo

A implementação está bem organizada e a persona/UX é consistente, mas a versão auditada continha **dois bugs que se manifestam em produção de forma silenciosa** (telemetria do dashboard zerada e `/qa` sem resposta), além de fragilidades de **resiliência local** (escrita não-atômica, bloqueio do event loop) e de **portabilidade Windows/PyInstaller** que o próprio escopo pediu para validar.

Foram aplicadas **12 correções** no `amanda_teams_bot.py`. Verificação: `py_compile` OK em Python 3.10.12 e **20/20 testes comportamentais** passando (histórico rolante, UTF-8/emoji, atomicidade, recuperação de JSON corrompido, regex de menção, `chat_id` resiliente, ausência de `.tmp` órfão).

| Sev. | ID | Achado | Status |
|------|----|--------|--------|
| 🔴 Crítico | C1 | Telemetria do dashboard zerada a cada evento (`json` usado antes do `import` local) | ✅ Corrigido |
| 🔴 Crítico | C2 | `/qa` nunca retornava o ack — caía no fluxo RAG/LLM | ✅ Corrigido |
| 🟠 Alto | H1 | Persistência sem atomicidade nem lock (race condition / corrupção) | ✅ Corrigido |
| 🟠 Alto | H2 | Pathing quebra sob PyInstaller onefile (perda de dados em `_MEIPASS`) | ✅ Corrigido |
| 🟠 Alto | H3 | Bloqueio do event loop (`requests`/`search` síncronos no handler async) | ✅ Corrigido |
| 🟡 Médio | M1 | `sys.stdout.reconfigure` sem guarda → crash sob `--noconsole` | ✅ Corrigido |
| 🟡 Médio | M2 | Regex de menção não casava `<at id="0">…</at>` | ✅ Corrigido |
| 🟡 Médio | M3 | `int(TELEGRAM_CHAT_ID)` → 500; ID pessoal hardcoded | ✅ Corrigido |
| 🟡 Médio | M4 | Telegram `parse_mode="Markdown"` com código → erro 400 silencioso | ✅ Corrigido |
| 🟡 Médio | M5 | Acesso a chaves de task sem `.get` → `KeyError` em schema drift | ✅ Corrigido |
| 🔵 Baixo | L1 | Tipagem incompleta / imports `typing` não usados | ✅ Corrigido |
| 🔒 Segurança | S1 | Webhook *fail-open* sem `SHARED_SECRET` | ⚠️ Mitigado (warning) + recomendação |
| 📐 Coerência | R1–R7 | Lacunas guia↔código e melhorias arquiteturais | 📋 Recomendado |

---

## 2. Achados por dimensão (escopo solicitado)

### 2.1 Robustez do webhook e subcomandos (`/webhook/teams`, `/task`, `/tribunal`, `/dev`, `/qa`)

**C2 — `/qa` nunca respondia (bug latente).** O bloco `/qa` montava `reply`, agendava a task em background e **terminava sem `return`**. Diferente de `/tribunal` e `/dev` (que retornam), o fluxo "vazava" para a seção *"4. Fluxo Normal"* e respondia ao Teams com a resposta do LLM para o texto literal `"/qa <arquivo>"` — o operador nunca via a confirmação documentada no guia.

```python
# ANTES — sem return; cai no fluxo RAG/LLM
        log_event_to_dashboard("info", f"QASquad ativado via Teams para: {source_path}")
    elif clean_text.startswith("/task") ...

# DEPOIS
        log_event_to_dashboard("info", f"QASquad ativado via Teams para: {source_path}")
        return {"type": "message", "text": reply}
```

**Tratamento de JSON/erros do endpoint — OK e mantido.** O parsing já está protegido (`try/except` → `HTTP 400`), a verificação de assinatura precede o parse, e os subcomandos validam argumentos vazios. O ponto frágil real não era o `try/except`, e sim a **lógica pós-validação** (C2 acima e a persistência em 2.2).

**Melhoria estrutural aplicada.** A lógica de `/task` (≈100 linhas com `def save_tasks` redefinida a cada request) foi extraída para uma função de módulo `handle_task_command(text) -> Dict[str, str]`, testável isoladamente e com região crítica protegida por lock. O handler passou a delegar:

```python
    elif clean_text.startswith("/task") or clean_text.startswith("/todo"):
        return handle_task_command(clean_text)
```

**M2 — Regex de menção.** `r"<at>.*?</at>"` não casa as menções reais do Teams, que vêm com atributos (`<at id="0">Amanda</at>`). Sem isso, o texto sujo chega ao roteador de comandos e ao RAG.

```python
# DEPOIS
clean = re.sub(r"<at\b[^>]*>.*?</at>", "", text, flags=re.IGNORECASE | re.DOTALL)
```

**M3 — `chat_id`.** `int(TELEGRAM_CHAT_ID)` lança `ValueError` (→ HTTP 500) se a env for não-numérica, *antes* de agendar a task. Havia ainda um **ID pessoal hardcoded** (`223442734`) como fallback — vazamento + *code smell* — e o parâmetro `chat_id` é, na prática, **morto** (as `run_async_*` leem a env diretamente em `send_telegram_notification`). Substituído por `_safe_chat_id()` resiliente; ID removido.

---

### 2.2 Persistência (JSON + Markdown), race conditions e UTF-8 no Windows

**C1 — Telemetria do dashboard zerada a cada evento (crítico).** Em `log_event_to_dashboard`, `json.load(f)` era chamado na **linha 99**, mas `import json` aparecia **dentro da mesma função na linha 105**. Em Python, o `import` local marca `json` como variável **local em todo o escopo**, então a leitura na linha 99 lançava `UnboundLocalError` — engolido pelo `except Exception`. Resultado: `data` voltava sempre vazio, e a cada chamada o histórico era **truncado para 1 evento**.

> **Evidência em produção:** `claw_status.json` continha **apenas 1 evento** (`"Nova task #2"`), embora `amanda_tasks.json` comprove **duas** operações de criação (tasks #1 e #2). A telemetria "em tempo real" do guia estava, de fato, quebrada.

Correção: `import json` movido para o topo do módulo (era a **única** fonte de `json`; também havia um import local redundante no bloco `/task`). Leitura passou a usar helper resiliente e a função preserva os 30 eventos.

**H1 — Atomicidade e concorrência.** As gravações usavam `open(path, "w")` (trunca-e-escreve). Sob múltiplos workers/processos `uvicorn`, ou crash no meio da escrita, isso gera **arquivo truncado/corrompido** e **leituras parciais** concorrentes (tanto de `amanda_tasks.json` quanto de `claw_status.json`, que outros componentes do MECHA também tocam). Aplicado:

```python
_FILE_LOCK = threading.RLock()        # serializa read-modify-write no processo
def _atomic_write_json(path, data):   # tmp + fsync + os.replace (atômico)
    ...
    os.replace(tmp_path, path)
```

`os.replace` é atômico no mesmo filesystem (Windows e POSIX), eliminando o estado intermediário visível. A sequência ler→modificar→gravar de `/task` e a escrita do dashboard rodam sob `_FILE_LOCK`.

> **Nota de concorrência multi-processo:** o `RLock` protege apenas dentro do processo. Se o deploy usar `uvicorn --workers N` (>1) ou múltiplos processos, recomenda-se `filelock`/`portalocker` para exclusão entre processos. A escrita atômica já protege os *leitores* mesmo nesse cenário.

**UTF-8 / Windows.** O tratamento de UTF-8 está **correto**: todas as aberturas usam `encoding="utf-8"` e `ensure_ascii=False`. Teste confirmou *round-trip* de `"çãé 🌸"` no JSON e no `.md`. O ponto real de risco no Windows não era a decodificação dos arquivos, e sim a saída do console (tratado em M1).

**M5 — Schema drift.** O código acessava `t["status"]`, `t["id"]`, etc. diretamente; um item legado sem alguma chave derrubaria a renderização. Trocado por `t.get(...)` com defaults.

---

### 2.3 Compatibilidade de pathing no Windows / PyInstaller

**H2 — `BASE_DIR`/`OPS_DIR` sob PyInstaller (alto).** O cálculo dependia de `__file__`. Em build **onefile**, `__file__` aponta para o diretório temporário `_MEIPASS` (extraído e **apagado ao sair**). Logo `.env`, `logs/`, `amanda_tasks.json`, `claw_status.json` e `AMANDA_TASKS.md` seriam resolvidos/gravados num diretório efêmero → **perda total de persistência** no executável empacotado. Aplicado resolvedor *frozen-aware* + escape hatch por env:

```python
def _resolve_base_dirs() -> Tuple[str, str, str]:
    if getattr(sys, "frozen", False):
        exe_dir = os.path.dirname(os.path.abspath(sys.executable))
        ...
PATTERNS_DIR, OPS_DIR, BASE_DIR = _resolve_base_dirs()
BASE_DIR = os.environ.get("MECHA_BASE_DIR", BASE_DIR)   # override p/ onefile/Docker
OPS_DIR  = os.environ.get("MECHA_OPS_DIR",  OPS_DIR)
```

**M1 — `sys.stdout.reconfigure`.** Sob PyInstaller `--noconsole` (windowed), `sys.stdout`/`stderr` podem ser `None` → `AttributeError` **no import** (crash antes de subir o servidor). Protegido com checagem `hasattr` + `try/except`, aplicado a `stdout` e `stderr`.

> **Ainda pendente para empacotar (recomendação):** o `sys.path.insert` + imports dinâmicos (`qdrant_client_helper`, `awesome_bots_orchestrator`, `code_squad_runner`, `qa_squad_runner`) exigem **`--hidden-import`** (ou `--collect-submodules`) no `.spec` do PyInstaller, pois o analisador estático não os detecta. O `sys.path.insert` foi condicionado a execução **não-congelada**.

---

### 2.4 Coerência RAG-Native e UX da persona (Shadow Processor)

O fluxo de conversa livre (sem `/`) **respeita o desenho RAG-Native**: faz `rag_client.search(...)` no Qdrant, injeta os *hits* como contexto e chama o LLM com o *system prompt* da persona (terminologia Irminsul/Akasha, tom direto). Mantido — e tornado mais robusto:

**H3 — Bloqueio do event loop.** `rag_client.search` e `requests.post` (até 25s) eram chamados **sincronamente dentro do handler `async`**, **serializando todas as requisições** (incluindo `/health`). Movidos para threadpool:

```python
hits = await run_in_threadpool(lambda: rag_client.search(clean_text, limit=3))
reply_text = await run_in_threadpool(query_openrouter_amanda, clean_text, context_str)
```

Parsing dos *hits* tornado defensivo (`h.get("metadata") or {}`), evitando `KeyError`/`TypeError` caso o `QdrantRAGClient` mude o contrato de retorno.

**Observação operacional (R4).** Os 4 módulos de integração **existem** em `ops/patterns/`. Contudo, `QdrantRAGClient()` é instanciado **no import**; se faltar o pacote `qdrant_client` ou o servidor Qdrant estiver fora, `rag_client = None` e o RAG **degrada silenciosamente** — a "resposta esperada" do guia (ex.: *"playbooks em `.mecha/intelligence/playbooks/`"*) não se cumpre, e no modo `MOCK_KEY` a Amanda devolve um texto fixo. O `/health` já expõe `qdrant_connected`; vale refletir esse estado também na fala da persona.

---

## 3. Aderência aos padrões MECHA (tipagem, segurança, resiliência)

**Tipagem (L1).** Adicionado alias `Task = Dict[str, Any]`; anotações de retorno em `health() -> Dict[str, Any]`, `teams_webhook(...) -> Dict[str, Any]`, `run_async_* -> None`, `start_server() -> None`, helpers internos. Imports de `typing` antes não usados (`Dict/Any/List`) agora têm uso real (+`Optional`, `Tuple`).

**Segurança (S1 — fail-open).** `verify_teams_signature` retorna `True` quando `SHARED_SECRET` está vazio. Sem o segredo, o webhook aceita requisições **não assinadas** e qualquer um pode disparar DevSquad/QASquad/Tribunal (custo de API e execução). Mitigação aplicada: **warning explícito no startup**. **Recomendação:** em produção, *fail-closed* (ex.: exigir segredo, liberando o modo aberto só com `MECHA_ALLOW_INSECURE=1` explícito).

**Resiliência local.** Coberta por C1/H1/H3/M1: leitura tolerante a falhas, escrita atômica, não-bloqueio do loop e proteção do console. Comportamento validado por testes (seção 5).

---

## 4. Coerência com o `MECHA_GUIDE.md` (recomendações)

- **R1 — Tribunal × Telegram.** O guia (II.2) afirma que o veredito de Shura 255 é "emitido no Telegram", e o ack do `/tribunal` repete a promessa. Porém `run_async_tribunal` **não chama** `send_telegram_notification` (ao contrário de `/dev` e `/qa`) — depende do `orchestrator.run_tribunal` notificar por conta própria. **Verificar** o orchestrator; se ele não publicar, o resultado se perde silenciosamente.
- **R2 — Timeout do Teams.** O chat livre é síncrono; com latência de RAG+LLM pode **estourar o limite (~5s)** do conector do Teams. Recomenda-se o mesmo padrão dos demais comandos: **ack imediato + resposta via Telegram**, ou reduzir `AMANDA_LLM_TIMEOUT` (agora configurável).
- **R3 — Sincronia do `AMANDA_TASKS.md`.** O espelho só é regenerado em **mutações** (`add`/`done`/`clear`). O guia diz "sincroniza instantaneamente"; um `/task list` ou edição externa do JSON **não** ressincroniza o `.md`. Opcional: regenerar no `list`.
- **R4 — Estado do RAG na persona** (ver 2.4).
- **R6 — Copy do mock.** O fallback menciona *"persistência local em SQLite"*, divergente da arquitetura real (JSON + Qdrant). Ajustar para coerência.
- **R7 — `index.js` enviado.** O arquivo anexado é o **"Kapture MCP Server" (Node/WebSocket)** — não pertence ao ecossistema MECHA auditado e ficou **fora do escopo**. Posso auditá-lo à parte se desejar.

---

## 5. Verificação realizada

- **Compilação:** `python3 -m py_compile amanda_teams_bot.py` → OK em **Python 3.10.12**.
  - *(Captado na verificação: uma 1ª tentativa de correção usou `{}` dentro de uma f-string — `SyntaxError` em Python < 3.12. Reescrito sem chaves aninhadas para garantir portabilidade.)*
- **Testes comportamentais (20/20 PASS)**, contra diretório temporário (sem tocar arquivos reais), cobrindo:
  - histórico do dashboard **acumula** e respeita o teto de 30 (regressão direta de C1);
  - `/task add|list|done|clear` e alias `/todo`, IDs incrementais;
  - **UTF-8 + emoji** preservados em JSON e `.md`;
  - recuperação de **JSON corrompido** sem derrubar;
  - escrita **sem `.tmp` órfão**;
  - `clean_teams_mention` com atributos; `_safe_chat_id` resiliente.

---

## 6. Mapa alteração → correção

| ID | Local no código | Correção |
|----|-----------------|----------|
| C1 | topo do módulo + `log_event_to_dashboard` | `import json` global; leitura resiliente; histórico preservado |
| C2 | bloco `/qa` no webhook | `return {"type":"message","text":reply}` |
| H1 | `_FILE_LOCK`, `_read_json`, `_atomic_write_json`, `handle_task_command` | lock + escrita atômica + leitura tolerante |
| H2 | `_resolve_base_dirs` + overrides de env | pathing *frozen-aware* |
| H3 | fluxo normal do webhook | `run_in_threadpool` para RAG e LLM |
| M1 | bloco de `reconfigure` | guarda `hasattr`/`try` p/ stdout/stderr |
| M2 | `clean_teams_mention` | regex com atributos + flags |
| M3 | `_safe_chat_id` + chamadas | parse resiliente; ID hardcoded removido |
| M4 | `send_telegram_notification` | `parse_mode` opcional (texto puro) + chunk seguro |
| M5 | `handle_task_command` | `.get(...)` defensivo |
| L1 | módulo todo | `Task` alias + anotações de retorno |
| S1 | startup | `logger.warning` quando sem `SHARED_SECRET` |

---

## 7. Próximos passos sugeridos (não aplicados — exigem sua decisão)

1. **Segurança:** tornar o webhook *fail-closed* em produção (flag `MECHA_ALLOW_INSECURE`).
2. **Teams ↔ Telegram:** migrar o chat livre para ack+push (R2) e fechar a lacuna do Tribunal (R1).
3. **PyInstaller:** adicionar `--hidden-import` para os 4 helpers no `.spec`.
4. **Multi-processo:** adotar `filelock` se for rodar com `--workers > 1`.
5. **Suite de testes:** versionar os testes desta auditoria em `ops/patterns/tests/` para regressão contínua.

*— Fim da auditoria. Ring 0 estável; telemetria restaurada.*
