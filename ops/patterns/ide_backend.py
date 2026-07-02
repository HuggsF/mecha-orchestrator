import os
import sys
import json
import asyncio
from typing import Dict, Any, AsyncGenerator, List
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# ── Path resolution ────────────────────────────────────────────────────────────
WORKSPACE_ROOT = os.path.normpath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..")
)
_patterns_path = os.path.dirname(os.path.abspath(__file__))
_superpowers_path = os.path.join(WORKSPACE_ROOT, ".superpowers")
for p in [_patterns_path, _superpowers_path]:
    if p not in sys.path:
        sys.path.insert(0, p)

from squad_orchestrator import SquadOrchestrator, MODEL_CODER, MODEL_DEFAULT
from qdrant_client_helper import QdrantRAGClient

try:
    from plugin_registry import SuperpowersRegistry
    _superpowers_reg = SuperpowersRegistry(WORKSPACE_ROOT)
    active_superpowers = _superpowers_reg.boot() or []
except ImportError:
    active_superpowers = []

# ── App setup ──────────────────────────────────────────────────────────────────
app = FastAPI(title="Antigravity IDE Backend", version="3.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

orchestrator = SquadOrchestrator(WORKSPACE_ROOT)

# Lazy-init RAG client — expensive to boot (loads MiniLM)
_rag_client: QdrantRAGClient | None = None

def get_rag() -> QdrantRAGClient:
    global _rag_client
    if _rag_client is None:
        print("[IDE v3] Bootstrapping Qdrant RAG client…")
        _rag_client = QdrantRAGClient()
    return _rag_client

# ── Squad catalog ──────────────────────────────────────────────────────────────
SQUAD_CATALOG: Dict[str, Dict] = {
    "dev_squad": {
        "label": "Code Squad",
        "icon": "⚙️",
        "workflow": "code_workflows",
        "pipelines": ["spec_driven_dev"],
        "input_key": "user_prompt",
        "color": "cyan",
        "agents": ["Uncle Bob", "Linus", "Kent Beck", "Mitnick"],
    },
    "qa_squad": {
        "label": "QA Squad",
        "icon": "🧪",
        "workflow": "qa_workflows",
        "pipelines": ["full_qa_pipeline"],
        "input_key": "implementation",
        "color": "emerald",
        "agents": ["Sonar", "Fowler", "Locust", "Kent Beck"],
    },
    "devops_squad": {
        "label": "DevOps Squad",
        "icon": "🚢",
        "workflow": "devops_workflows",
        "pipelines": ["infra_provision_pipeline"],
        "input_key": "deployment_spec",
        "color": "amber",
        "agents": ["Terraform", "Kubernetes", "Gitlab", "SRE"],
    },
    "tribunal_squad": {
        "label": "Hermes Tribunal",
        "icon": "⚖️",
        "workflow": "tribunal_workflows",
        "pipelines": ["hermes_tribunal_pipeline"],
        "input_key": "proposal",
        "color": "purple",
        "agents": ["Warlock", "Amanda", "Shura"],
    },
    "product_squad": {
        "label": "Product",
        "icon": "🗺️",
        "workflow": "product_workflows",
        "pipelines": ["product_pipeline"],
        "input_key": "user_prompt",
        "color": "rose",
        "agents": ["Planner", "Architect", "Executor", "Integrator"],
    },
}

# ── SSE helper ─────────────────────────────────────────────────────────────────
def _sse(event: str, data: dict) -> str:
    return f"event: {event}\ndata: {json.dumps(data, ensure_ascii=False)}\n\n"

# ── RAG context retrieval ──────────────────────────────────────────────────────
def _fetch_rag_context(query: str, limit: int = 4) -> List[Dict]:
    """Query Qdrant mecha_collection for relevant chunks."""
    try:
        rag = get_rag()
        hits = rag.search(query, limit=limit)
        return [
            {
                "score": round(h["score"], 4),
                "text": h["text"][:400],
                "source": h["metadata"].get("source", h["metadata"].get("topic", "knowledge_base")),
            }
            for h in hits
            if h["score"] > 0.15
        ]
    except Exception as e:
        print(f"[IDE v3] RAG search error: {e}")
        return []

def _build_rag_context_block(chunks: List[Dict]) -> str:
    if not chunks:
        return ""
    lines = ["[ANTIGRAVITY KNOWLEDGE BASE — RAG CONTEXT]"]
    for i, c in enumerate(chunks, 1):
        lines.append(f"\n[{i}] (score={c['score']}) {c['source']}\n{c['text']}")
    lines.append("\n[END OF RAG CONTEXT — use the above to inform your response]\n")
    return "\n".join(lines)

# ── Streaming workflow ─────────────────────────────────────────────────────────
async def stream_workflow(
    squad_name: str,
    workflow_name: str,
    pipeline_key: str,
    initial_inputs: Dict[str, Any],
    use_rag: bool = True,
) -> AsyncGenerator[str, None]:

    yield _sse("boot", {
        "squad": squad_name,
        "pipeline": pipeline_key,
        "message": f"Booting pipeline [{pipeline_key}]…",
    })

    # RAG retrieval
    rag_chunks: List[Dict] = []
    if use_rag:
        user_text = next(iter(initial_inputs.values()), "")
        yield _sse("rag_search", {"query": user_text[:120], "status": "searching"})
        rag_chunks = await asyncio.get_event_loop().run_in_executor(
            None, _fetch_rag_context, user_text
        )
        yield _sse("rag_done", {
            "hits": len(rag_chunks),
            "chunks": rag_chunks,
        })

    rag_block = _build_rag_context_block(rag_chunks)

    personas = orchestrator.load_squad_config(squad_name)
    workflow_data = orchestrator.load_workflow_config(workflow_name)
    pipeline = workflow_data.get(pipeline_key)

    if not pipeline:
        yield _sse("error", {"message": f"Pipeline '{pipeline_key}' not found."})
        return

    env = {**initial_inputs}
    steps = pipeline.get("steps", [])
    executed: set = set()

    while len(executed) < len(steps):
        ready = []
        for step in steps:
            sid = step.get("step_id")
            if sid in executed:
                continue
            deps = []
            if step.get("input_source"):
                deps.append(step["input_source"])
            if step.get("input_sources"):
                deps.extend(step["input_sources"])
            if all(d in env for d in deps):
                ready.append(step)

        if not ready:
            unresolved = [s.get("agent") for s in steps if s.get("step_id") not in executed]
            yield _sse("error", {"message": f"DAG bottleneck: {unresolved}"})
            return

        # Announce wave
        wave_agents = [s.get("agent") for s in ready]
        yield _sse("wave_start", {"agents": wave_agents, "parallel": len(ready) > 1})

        for step in ready:
            agent_name = step.get("agent")
            agent_cfg = personas.get(agent_name, {})
            yield _sse("agent_start", {
                "agent": agent_name,
                "role": agent_cfg.get("role", "Agent"),
                "step_id": step.get("step_id"),
                "description": step.get("description", ""),
            })

        async def run_step(step):
            agent_name = step.get("agent")
            agent_cfg = personas.get(agent_name, {})
            system_prompt = agent_cfg.get("system_prompt", "")

            # Inject RAG context into system prompt
            if rag_block:
                system_prompt = rag_block + "\n\n" + system_prompt

            step_inputs = []
            if step.get("input_source"):
                src = step["input_source"]
                step_inputs.append(f"[{src.upper()}]:\n{env[src]}")
            if step.get("input_sources"):
                for src in step["input_sources"]:
                    step_inputs.append(f"[{src.upper()}]:\n{env[src]}")

            user_content = "\n\n".join(step_inputs)
            model = MODEL_CODER if agent_name in ["Linus", "Kent Beck"] else MODEL_DEFAULT
            result = await orchestrator._call_openrouter(
                model, system_prompt, user_content, agent_name, str(initial_inputs)
            )
            return step, result

        results = await asyncio.gather(*[run_step(s) for s in ready])

        for step, result in results:
            out_var = step.get("output_var")
            env[out_var] = result
            executed.add(step.get("step_id"))
            yield _sse("agent_done", {
                "agent": step.get("agent"),
                "step_id": step.get("step_id"),
                "output_var": out_var,
                "content": result,
            })

    yield _sse("pipeline_done", {
        "message": "Pipeline complete. All agents finished.",
        "rag_hits": len(rag_chunks),
        "outputs": list(env.keys()),
    })

    # Auto-Ingestão
    yield _sse("ingestion_start", {"message": "Iniciando auto-ingestão RAG dos resultados..."})
    try:
        import os
        import asyncio
        docs_dir = os.path.join(WORKSPACE_ROOT, "docs")
        os.makedirs(docs_dir, exist_ok=True)
        log_path = os.path.join(docs_dir, f"workflow_latest_output.md")
        
        with open(log_path, "w", encoding="utf-8") as f:
            f.write(f"# Execução Automática\n\n**Workflow:** {workflow_name}\n**Pipeline:** {pipeline_key}\n\n")
            for k, v in env.items():
                f.write(f"## {k}\n\n{v}\n\n")

        mecha_dir = os.path.join(WORKSPACE_ROOT, ".mecha")
        proc = await asyncio.create_subprocess_exec(
            "python", "ops/patterns/dorkling_rag_ingester.py",
            cwd=mecha_dir,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await proc.communicate()
        if proc.returncode == 0:
            yield _sse("ingestion_done", {"message": "Resultados recém-gerados foram ingeridos no Qdrant com sucesso!"})
        else:
            err_msg = stderr.decode('utf-8', errors='replace').strip()
            yield _sse("error", {"message": f"Aviso de Ingestão: {err_msg}"})
    except Exception as e:
        yield _sse("error", {"message": f"Falha na auto-ingestão: {str(e)}"})

# ── Models ─────────────────────────────────────────────────────────────────────
class ComposerRequest(BaseModel):
    squad_name: str
    user_prompt: str
    pipeline_key: str = ""
    use_rag: bool = True

class RagRequest(BaseModel):
    query: str
    limit: int = 5

# ── Routes ─────────────────────────────────────────────────────────────────────
@app.get("/health")
def health():
    return {
        "status": "ok",
        "version": "3.0.0",
        "workspace": WORKSPACE_ROOT,
        "superpowers": active_superpowers,
        "squads": list(SQUAD_CATALOG.keys()),
        "telemetry": {"spend": orchestrator.tracker.current_spend},
    }

@app.get("/api/v1/squads")
def list_squads():
    return SQUAD_CATALOG

@app.post("/api/v1/rag/search")
def rag_search(req: RagRequest):
    """Direct RAG search endpoint — returns Antigravity knowledge chunks."""
    chunks = _fetch_rag_context(req.query, req.limit)
    return {"query": req.query, "hits": len(chunks), "results": chunks}

@app.post("/api/v1/compose")
async def compose(req: ComposerRequest):
    catalog = SQUAD_CATALOG.get(req.squad_name)
    if not catalog:
        raise HTTPException(400, f"Unknown squad: {req.squad_name}")
    pipeline_key = req.pipeline_key or catalog["pipelines"][0]
    initial_inputs = {catalog["input_key"]: req.user_prompt}
    return StreamingResponse(
        stream_workflow(
            req.squad_name,
            catalog["workflow"],
            pipeline_key,
            initial_inputs,
            req.use_rag,
        ),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )

# --- MCP servers (real config from ~/.cursor/mcp.json, sanitized) ---
MCP_CONFIG_PATH = "~/.cursor/mcp.json"  # source of truth (configuravel)


@app.get("/api/v1/mcp/servers")
def list_mcp_servers():
    import json
    import os
    from pathlib import Path
    from urllib.parse import urlparse

    cfg = Path(os.path.expanduser(MCP_CONFIG_PATH))
    if not cfg.exists():
        return {"configPath": str(cfg), "error": "config not found", "servers": []}
    try:
        data = json.loads(cfg.read_text(encoding="utf-8"))
    except Exception as exc:
        return {"configPath": str(cfg), "error": "parse error: %s" % exc, "servers": []}

    out = []
    for name, spec in (data.get("mcpServers") or {}).items():
        entry = {"name": name, "status": "configured"}
        if isinstance(spec, dict):
            if spec.get("url"):
                entry["transport"] = "remote"
                try:
                    entry["host"] = urlparse(spec["url"]).hostname or ""
                except Exception:
                    entry["host"] = ""
            elif spec.get("command"):
                entry["transport"] = "stdio"
                entry["command"] = Path(str(spec["command"])).name
                args = spec.get("args") or []
                entry["argsCount"] = len(args) if isinstance(args, list) else 0
            else:
                entry["transport"] = "unknown"
        out.append(entry)
    return {"configPath": str(cfg), "count": len(out), "servers": out}


if __name__ == "__main__":
    import uvicorn
    print(f"[Antigravity IDE v3] Workspace: {WORKSPACE_ROOT}")
    print(f"[Antigravity IDE v3] Superpowers: {active_superpowers}")
    uvicorn.run(app, host="0.0.0.0", port=8000)
