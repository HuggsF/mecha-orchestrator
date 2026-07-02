# RONIN × QLoRA — Camada de configuração de agentes em pesos, não em prompt

> Avaliação do PR HuggsF/ronin#1 (AI-OS Creative DNA Platform, 78 commits, 277 testes)
> e blueprint do "canivete suíço": 1 modelo base quantizado + N adapters QLoRA minúsculos,
> um por passport/persona/lane, hot-swap em runtime. Data: 2026-07-02.

## 1. O que o RONIN já entrega (avaliação do PR)

O PR #1 monta exatamente a infraestrutura que um pipeline de fine-tuning leve precisa
e que normalmente é o trabalho difícil:

| Peça do RONIN | Papel no pipeline QLoRA |
|---|---|
| `DNAPassport` (Creator/Brand/Product/Audience) + `EmotionalMix` (7 dims [0,1] + x_custom, validadas) | **Schema de condicionamento** — a "configuração do agente" já é paramétrica e serializável (passport.json). É o rótulo do dataset. |
| `RuleGenerator` (LLM-first + lookup fallback) + `MixerBot` | **Gerador de dataset sintético** — produz pares instrução→saída condicionados ao passport (self-instruct barato). |
| `ContentBot` (zero-shot via passport rules) | **Professor** — as saídas dele, aprovadas, viram exemplos de treino (distilação do modelo grande no pequeno). |
| `FidelityBot` (LLM judge vs emotional mix, média ponderada) + gate 0.80 do `CompositorBot` | **Filtro de rejection sampling + eval harness** — só entra no dataset o que passa o gate; e é a métrica de aceitação do adapter treinado. |
| `SpawnEngine` (clona template → `instances/{client_id}/`, injeta passport nas 5 lanes, rollback atômico) | **Fábrica de adapters** — o spawn ganha um passo: registrar/treinar o adapter do cliente. Adapter mora na instância. |
| `AnalyticsBot` (engagement retroalimentação) + `GapScanner`/`GapCron` | **Flywheel de re-treino** — engajamento pondera exemplos; gaps de dimensão disparam augmentation dirigida e refresh do adapter. |
| `spiral_02_llm` (`model_router`, `LayerResult` economics) | **Roteador adapter-aware** — decide base+adapter local vs API, e o LayerResult já mede o delta de custo. |
| `spiral_07_evolution` (`self_improver`) + `scheduler` (spiral_08) | **Cadência** — job de re-treino agendado quando o GapCron acusa drift. |

Veredito: o repo não precisa de módulos novos para "ter fine-tuning" — precisa de UMA
ponte (trainer) e três extensões pequenas em módulos existentes.

## 2. O canivete suíço (arquitetura alvo)

```
                    base 4-bit (NF4) servido 1x — ex.: Qwen2.5-7B / Llama-3.1-8B
                                        |
        +----------------+--------------+----------------+
        | adapter        | adapter      | adapter        |   10-50 MB cada
        | client_A/lane2 | client_A/l3  | client_B/lane2 |   (safetensors LoRA)
        +----------------+--------------+----------------+
                 selecionado por passport_id + lane (hot-swap por request)
```

- **QLoRA**: base congelado quantizado em 4-bit NF4 (bitsandbytes) + LoRA r=8..16,
  alpha=16..32, alvo q/k/v/o (+gate/up/down se sobrar VRAM) → 0,1-0,5% dos parâmetros
  treináveis. Treino de um adapter: 200-1000 pares, 2-3 epochs, lr 1e-4..2e-4 — minutos/
  poucas horas em GPU de consumo (unsloth ou peft+trl).
- **Serving**: Ollama importa adapter LoRA sobre base GGUF (o RONIN já fala Ollama — o
  models.yaml histórico referencia `ollama/nomic-embed-text`); para multi-adapter por
  request, llama.cpp `--lora` ou vLLM multi-LoRA (S-LoRA style). O `model_router` escolhe.
- **Divisão de responsabilidade (crítica)**: QLoRA aprende FORMA (voz, tom, política de
  formato, persona — o que hoje é o passport injetado no prompt). Fatos ficam no RAG
  (spiral_04_knowledge / Qdrant+Neo4j do MECHA). Task fica no prompt. Não assar
  conhecimento em peso — ele desatualiza e não tem cite/verify.

## 3. Mudanças mínimas no RONIN (por módulo, sem criar subsistema novo)

1. **`instances/template/`**: + `adapters/` (vazio) e campos em `meta.json`:
   `adapter_status: none|training|ready`, `adapter_path`, `adapter_metrics`.
2. **`SpawnEngine.spawn()`**: após injetar passport, enfileira `train_adapter(passport_id)`
   (EventBus, canal `adapter.jobs`) — não bloqueia o spawn; status `pending` já existe.
3. **NOVO (única peça nova) `spiral_07_evolution/adapter_trainer.py`**:
   - `build_dataset(passport)` → RuleGenerator/MixerBot geram pares; ContentBot gera
     candidatos; FidelityBot filtra ≥ gate; AnalyticsBot pondera (quando houver histórico).
   - `train(passport_id, dataset)` → peft/unsloth QLoRA, salva em `instances/{id}/adapters/`.
   - `evaluate(adapter)` → FidelityBot num held-out; promove só se ≥ baseline zero-shot
     (mesmo padrão de graduação por piso do rag-dojo: adapter só gradua com D ≥ piso).
4. **`spiral_02_llm/model_router.py`**: rota `local+adapter` quando
   `meta.adapter_status == ready` e a task é de geração on-voice; fallback para o fluxo
   atual (API + passport no prompt) caso contrário. LayerResult registra `adapter_id`.
5. **`ContentBot`**: quando servido por adapter, ENCOLHE o prompt (remove as regras do
   passport injetadas) — é aqui que a economia de tokens se materializa por request.
6. **`GapCron`**: novo auditor `AdapterAuditor` — fidelity média da semana < gate ou
   passport editado → flag `adapter_stale` → re-treino agendado.

## 4. Ponte com o MECHA

- Personas do debate (Hiansen/Henrique/Rodolfo) e agentes do bus são candidatos a
  adapters sobre o mesmo base local → debates O6 e squad-runs com custo marginal ~zero.
- Registrar cada adapter na ontologia como ADAPTER (estilo hexagonal do NeuroQuest):
  `adapter:qlora.<passport_id>.<lane>` -[IMPLEMENTA]-> port de geração; espelha o
  registry de adapters já usado no ecossistema.
- rag-dojo espirais 04/05 (cognitive/economics) são o lugar de medir: custo/req,
  fidelity delta adapter-vs-zero-shot, tokens poupados por request.

## 5. Riscos (lente Rodolfo)

1. **Drift catastrófico em dataset pequeno** — mitigar: lr baixo, poucas epochs,
   eval held-out com FidelityBot ANTES de promover, e manter zero-shot como fallback.
2. **Sprawl de adapters** — sem registry vira o novo debris: meta.json + ontologia
   obrigatórios; GapScanner audita órfãos.
3. **Paridade de avaliador** — mesmo LLM judge (mesma versão/temperatura) entre baseline
   e adapter, ou a comparação mente (lição do embedder BGE vs MiniLM no MECHA).
4. **VRAM** — QLoRA 7-8B r=16 exige ~10-12GB; se a GPU local não der, treinar em spot
   cloud e só SERVIR local (adapter é portátil por design).
5. **1 teste pré-existente falhando** (`test_zero_shot_catalog`) — resolver antes de
   fazer do ZeroShotCatalog parte do pipeline de dataset.

## 6. Prova de conceito sugerida (1 passport, 1 lane)

1. Escolher 1 cliente/passport real → `build_dataset` ≈ 300 pares filtrados pelo gate.
2. Treinar adapter r=16 sobre Qwen2.5-7B-Instruct 4-bit (unsloth), ~1-2h.
3. A/B: 20 tasks de ContentBot — zero-shot+passport-no-prompt vs adapter+prompt-enxuto.
4. Critério de GO: fidelity(adapter) ≥ fidelity(zero-shot) E tokens/req caindo ≥ 40%.
5. Se GO: implementar itens do §3 na ordem 3 → 1 → 2 → 4 → 5 → 6.
