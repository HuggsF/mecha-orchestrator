# ==============================================================================
# 🔀 MECHA CROSS-SQUAD ROUTER - INTER-SQUAD COMMUNICATION + HISTORY
# ==============================================================================
# Bridges the AgentBus with SquadOrchestrator to enable:
# - Cross-squad workflow chaining (DevSquad → QASquad → DevOpsSquad)
# - Conversation history persistence per thread
# - Squad-to-squad request/response
# - Pipeline completion events on bus channels
# ==============================================================================

import os
import sys
import json
import time
import asyncio
import logging
from typing import Dict, Any, List, Optional

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger("MECHA_CrossSquadRouter")

from agent_bus import AgentBus, BusMessage, MessageType, AgentStatus
from squad_orchestrator import SquadOrchestrator


# =============================================================================
# CONVERSATION HISTORY STORE
# =============================================================================

class ConversationStore:
    """Persistent conversation history backed by JSON files."""

    def __init__(self, store_dir: str):
        self.store_dir = store_dir
        os.makedirs(store_dir, exist_ok=True)

    def _thread_path(self, thread_id: str) -> str:
        safe_id = thread_id.replace("/", "_").replace("\\", "_")
        return os.path.join(self.store_dir, f"{safe_id}.json")

    def save_turn(self, thread_id: str, agent_id: str, role: str,
                  content: str, metadata: Dict[str, Any] = None):
        path = self._thread_path(thread_id)
        history = self.load_thread(thread_id)
        history.append({
            "agent_id": agent_id,
            "role": role,
            "content": content,
            "metadata": metadata or {},
            "timestamp": time.time()
        })
        with open(path, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2, ensure_ascii=False)

    def load_thread(self, thread_id: str) -> List[Dict[str, Any]]:
        path = self._thread_path(thread_id)
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return []

    def list_threads(self) -> List[Dict[str, Any]]:
        threads = []
        for fname in os.listdir(self.store_dir):
            if fname.endswith(".json"):
                tid = fname[:-5]
                path = os.path.join(self.store_dir, fname)
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    threads.append({
                        "thread_id": tid,
                        "turns": len(data),
                        "last_activity": data[-1]["timestamp"] if data else 0,
                        "agents": list(set(t["agent_id"] for t in data))
                    })
                except Exception:
                    pass
        return sorted(threads, key=lambda t: t["last_activity"], reverse=True)

    def delete_thread(self, thread_id: str) -> bool:
        path = self._thread_path(thread_id)
        if os.path.exists(path):
            os.remove(path)
            return True
        return False

    def search(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        results = []
        query_lower = query.lower()
        for fname in os.listdir(self.store_dir):
            if not fname.endswith(".json"):
                continue
            path = os.path.join(self.store_dir, fname)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                for turn in data:
                    if query_lower in turn.get("content", "").lower():
                        results.append({
                            "thread_id": fname[:-5],
                            "agent_id": turn["agent_id"],
                            "content_snippet": turn["content"][:200],
                            "timestamp": turn["timestamp"]
                        })
                        if len(results) >= limit:
                            return results
            except Exception:
                pass
        return results


# =============================================================================
# ROUTE DEFINITION
# =============================================================================

SQUAD_ROUTES = {
    "dev_to_qa": {
        "trigger_squad": "dev",
        "trigger_output": "audit_report",
        "trigger_condition": "[APROVADO]",
        "target_squad": "qa",
        "target_workflow": "qa_workflows",
        "target_pipeline": "qa_audit_pipeline",
        "input_mapping": {
            "source_code": "implementation",
            "test_code": "tests"
        }
    },
    "qa_to_devops": {
        "trigger_squad": "qa",
        "trigger_output": "qa_final_report",
        "trigger_condition": "[APROVADO]",
        "target_squad": "devops",
        "target_workflow": "devops_workflows",
        "target_pipeline": "devops_deploy_pipeline",
        "input_mapping": {
            "user_prompt": "qa_final_report"
        }
    },
    "any_to_tribunal": {
        "trigger_squad": "*",
        "trigger_output": None,
        "trigger_condition": None,
        "target_squad": "tribunal",
        "target_workflow": "tribunal_workflows",
        "target_pipeline": "tribunal_pipeline",
        "input_mapping": {
            "user_prompt": "_request_payload"
        }
    }
}


# =============================================================================
# CROSS-SQUAD ROUTER
# =============================================================================

class CrossSquadRouter:
    """
    Routes messages and workflow outputs between squads via the AgentBus.

    Features:
    - Auto-registers squad agents on the bus when a workflow starts
    - Publishes step completions to bus channels
    - Chains workflows across squads based on route definitions
    - Persists full conversation history per thread
    - Enables direct squad-to-squad requests via bus
    """

    def __init__(self, workspace_root: str, bus: AgentBus = None):
        self.workspace_root = workspace_root
        self.bus = bus or AgentBus.get_instance()
        self.orchestrator = SquadOrchestrator(workspace_root)
        self.history = ConversationStore(
            os.path.join(workspace_root, ".mecha", "ops", "logs", "conversations")
        )
        self.routes = dict(SQUAD_ROUTES)
        self._register_system_agent()

    def _register_system_agent(self):
        if not self.bus.get_agent("router"):
            self.bus.register(
                "router", "CrossSquadRouter",
                squad="system", role="Message Router",
                capabilities=["routing", "chaining", "history"]
            )

    # -------------------------------------------------------------------------
    # SQUAD AGENT REGISTRATION
    # -------------------------------------------------------------------------

    def register_squad_agents(self, squad_name: str):
        personas = self.orchestrator.load_squad_config(squad_name)
        for agent_name, config in personas.items():
            agent_id = self._agent_id(agent_name, squad_name)
            if not self.bus.get_agent(agent_id):
                self.bus.register(
                    agent_id, agent_name,
                    squad=squad_name,
                    role=config.get("role", "Agent"),
                    capabilities=self._extract_capabilities(config)
                )
            self.bus.subscribe(agent_id, f"squad.{squad_name}")
            self.bus.subscribe(agent_id, "pipeline.events")

    def _agent_id(self, agent_name: str, squad_name: str) -> str:
        return f"{squad_name}.{agent_name.lower().replace(' ', '_')}"

    def _extract_capabilities(self, config: dict) -> List[str]:
        role = config.get("role", "").lower()
        caps = []
        if "audit" in role or "security" in role:
            caps.append("security")
        if "architect" in role or "spec" in role:
            caps.append("architecture")
        if "implement" in role or "coder" in role:
            caps.append("coding")
        if "test" in role or "qa" in role:
            caps.append("testing")
        if "compliance" in role or "review" in role:
            caps.append("compliance")
        if "judge" in role or "lead" in role:
            caps.append("judgment")
        return caps

    # -------------------------------------------------------------------------
    # WORKFLOW EXECUTION WITH BUS INTEGRATION
    # -------------------------------------------------------------------------

    async def run_squad_workflow(self, squad_name: str, workflow_name: str,
                                 pipeline_key: str, initial_inputs: Dict[str, Any],
                                 thread_id: str = None, auto_chain: bool = True) -> Dict[str, Any]:
        if not thread_id:
            thread_id = f"workflow_{squad_name}_{int(time.time())}"

        self.register_squad_agents(squad_name)

        self.bus.publish("router", "pipeline.events", {
            "event": "workflow.started",
            "squad": squad_name,
            "pipeline": pipeline_key,
            "thread_id": thread_id
        })

        self.history.save_turn(
            thread_id, "router", "system",
            f"Workflow started: {squad_name}/{pipeline_key}",
            {"inputs_keys": list(initial_inputs.keys())}
        )

        results = await self.orchestrator.run_workflow(
            squad_name, workflow_name, pipeline_key, initial_inputs
        )

        for var_name, content in results.items():
            if var_name.startswith("_"):
                continue
            agent_id = self._find_agent_for_output(squad_name, workflow_name, pipeline_key, var_name)
            self.history.save_turn(
                thread_id, agent_id or f"{squad_name}.unknown",
                "assistant", str(content)[:2000],
                {"output_var": var_name}
            )
            self.bus.publish("router", f"squad.{squad_name}", {
                "event": "step.completed",
                "agent": agent_id,
                "output_var": var_name,
                "content_preview": str(content)[:500],
                "thread_id": thread_id
            })

        self.bus.publish("router", "pipeline.events", {
            "event": "workflow.completed",
            "squad": squad_name,
            "pipeline": pipeline_key,
            "thread_id": thread_id,
            "output_vars": [k for k in results.keys() if not k.startswith("_")]
        })

        if auto_chain:
            chain_results = await self._check_and_chain(squad_name, results, thread_id)
            if chain_results:
                results["_chained"] = chain_results

        return results

    def _find_agent_for_output(self, squad_name: str, workflow_name: str,
                                pipeline_key: str, output_var: str) -> Optional[str]:
        workflow_data = self.orchestrator.load_workflow_config(workflow_name)
        pipeline = workflow_data.get(pipeline_key, {})
        for step in pipeline.get("steps", []):
            if step.get("output_var") == output_var:
                return self._agent_id(step.get("agent", "unknown"), squad_name)
        return None

    # -------------------------------------------------------------------------
    # AUTO-CHAINING
    # -------------------------------------------------------------------------

    async def _check_and_chain(self, source_squad: str, results: Dict[str, Any],
                                thread_id: str) -> Optional[Dict[str, Any]]:
        norm_source = source_squad.replace("_squad", "")
        for route_name, route in self.routes.items():
            trigger_squad = route["trigger_squad"]
            norm_trigger = trigger_squad.replace("_squad", "")
            if trigger_squad != "*" and norm_trigger != norm_source:
                continue

            trigger_output = route.get("trigger_output")
            trigger_condition = route.get("trigger_condition")

            if trigger_output:
                output_value = str(results.get(trigger_output, ""))
                if trigger_condition and trigger_condition not in output_value:
                    continue

            target_inputs = {}
            for target_key, source_key in route["input_mapping"].items():
                if source_key in results:
                    target_inputs[target_key] = results[source_key]

            if not target_inputs:
                continue

            target_squad_file = route["target_squad"]
            if not target_squad_file.endswith("_squad"):
                target_squad_file += "_squad"

            logger.info(f"[ROUTER] Auto-chaining: {source_squad} -> {target_squad_file} via route '{route_name}'")

            self.bus.publish("router", "pipeline.events", {
                "event": "chain.triggered",
                "route": route_name,
                "source_squad": source_squad,
                "target_squad": target_squad_file,
                "thread_id": thread_id
            })

            self.history.save_turn(
                thread_id, "router", "system",
                f"Auto-chaining to {target_squad_file}/{route['target_pipeline']}",
                {"route": route_name}
            )

            chain_result = await self.run_squad_workflow(
                target_squad_file,
                route["target_workflow"],
                route["target_pipeline"],
                target_inputs,
                thread_id=thread_id,
                auto_chain=True  # Allow multi-hop chaining dev_squad -> qa_squad -> devops_squad
            )
            return chain_result

        return None

    # -------------------------------------------------------------------------
    # DIRECT SQUAD REQUEST (via bus)
    # -------------------------------------------------------------------------

    async def request_squad(self, requester: str, target_squad: str,
                             prompt: str, thread_id: str = None) -> Dict[str, Any]:
        if not thread_id:
            thread_id = f"request_{target_squad}_{int(time.time())}"

        self.history.save_turn(thread_id, requester, "user", prompt)

        self.bus.publish("router", f"squad.{target_squad}.lead", {
            "action": "squad_request",
            "requester": requester,
            "prompt": prompt,
            "thread_id": thread_id
        })

        target_squad_norm = target_squad.replace("_squad", "")

        route = self.routes.get("any_to_tribunal")
        if target_squad_norm == "tribunal" and route:
            result = await self.run_squad_workflow(
                "tribunal_squad", "tribunal_workflows", "tribunal_pipeline",
                {"user_prompt": prompt},
                thread_id=thread_id, auto_chain=False
            )
            return result

        squad_workflows = {
            "dev": ("code_workflows", "spec_driven_dev", {"user_prompt": prompt}),
            "qa": ("qa_workflows", "qa_audit_pipeline", {"source_code": prompt, "test_code": ""}),
            "devops": ("devops_workflows", "devops_deploy_pipeline", {"user_prompt": prompt}),
        }

        if target_squad_norm in squad_workflows:
            wf_name, pipeline, inputs = squad_workflows[target_squad_norm]
            return await self.run_squad_workflow(
                target_squad_norm + "_squad", wf_name, pipeline, inputs,
                thread_id=thread_id, auto_chain=True  # Enable auto-chaining for requests
            )

        return {"error": f"Unknown squad: {target_squad}"}

    # -------------------------------------------------------------------------
    # CONVERSATION HISTORY ACCESS
    # -------------------------------------------------------------------------

    def get_conversation(self, thread_id: str) -> List[Dict[str, Any]]:
        return self.history.load_thread(thread_id)

    def list_conversations(self) -> List[Dict[str, Any]]:
        return self.history.list_threads()

    def search_conversations(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        return self.history.search(query, limit)

    # -------------------------------------------------------------------------
    # CUSTOM ROUTES
    # -------------------------------------------------------------------------

    def add_route(self, name: str, route_config: Dict[str, Any]):
        self.routes[name] = route_config
        logger.info(f"[ROUTER] Route added: {name}")

    def remove_route(self, name: str) -> bool:
        if name in self.routes:
            del self.routes[name]
            return True
        return False

    # -------------------------------------------------------------------------
    # TELEMETRY
    # -------------------------------------------------------------------------

    def stats(self) -> Dict[str, Any]:
        return {
            "bus": self.bus.stats(),
            "routes": list(self.routes.keys()),
            "conversations": len(self.history.list_threads()),
            "orchestrator_spend": self.orchestrator.tracker.current_spend
        }


# =============================================================================
# TESTS
# =============================================================================

def _run_tests():  # pragma: no cover
    import shutil

    print("=" * 60)
    print("  MECHA CROSS-SQUAD ROUTER — UNIT TESTS")
    print("=" * 60)

    workspace = "c:\\Users\\huggs\\OneDrive\\Documentos\\workspace"
    test_conv_dir = os.path.join(os.path.dirname(__file__), "_test_conversations")

    AgentBus.reset()
    bus = AgentBus.get_instance()
    router = CrossSquadRouter(workspace, bus)
    router.history = ConversationStore(test_conv_dir)
    results = {}

    # Test 1: Squad Agent Registration
    try:
        router.register_squad_agents("dev_squad")
        agents = bus.list_agents(squad="dev_squad")
        assert len(agents) >= 3, f"Expected >=3 dev_squad agents, got {len(agents)}"
        results["squad_registration"] = True
        print(f" [OK] Test 1: Squad Agent Registration ({len(agents)} agents)")
    except Exception as e:
        results["squad_registration"] = False
        print(f" [FAIL] Test 1: {e}")

    # Test 2: Multi-Squad Registration
    try:
        router.register_squad_agents("tribunal_squad")
        all_agents = bus.list_agents()
        squads = set(a.squad for a in all_agents if a.squad)
        assert "dev_squad" in squads
        assert "tribunal_squad" in squads
        assert "system" in squads
        results["multi_squad"] = True
        print(f" [OK] Test 2: Multi-Squad Registration ({len(squads)} squads)")
    except Exception as e:
        results["multi_squad"] = False
        print(f" [FAIL] Test 2: {e}")

    # Test 3: Conversation History Persistence
    try:
        thread_id = "test_thread_001"
        router.history.save_turn(thread_id, "warlock", "assistant", "Essa config tem furos.")
        router.history.save_turn(thread_id, "amanda", "assistant", "Discordo, esta limpo.")
        router.history.save_turn(thread_id, "shura", "assistant", "Aprovado. [1]")
        loaded = router.history.load_thread(thread_id)
        assert len(loaded) == 3
        assert loaded[0]["agent_id"] == "warlock"
        assert loaded[2]["content"] == "Aprovado. [1]"
        results["history_persistence"] = True
        print(" [OK] Test 3: Conversation History Persistence")
    except Exception as e:
        results["history_persistence"] = False
        print(f" [FAIL] Test 3: {e}")

    # Test 4: Thread Listing
    try:
        router.history.save_turn("test_thread_002", "linus", "assistant", "Codigo implementado.")
        threads = router.history.list_threads()
        assert len(threads) >= 2
        results["thread_listing"] = True
        print(f" [OK] Test 4: Thread Listing ({len(threads)} threads)")
    except Exception as e:
        results["thread_listing"] = False
        print(f" [FAIL] Test 4: {e}")

    # Test 5: Conversation Search
    try:
        hits = router.history.search("furos")
        assert len(hits) >= 1
        assert "furos" in hits[0]["content_snippet"].lower()
        results["search"] = True
        print(f" [OK] Test 5: Conversation Search ({len(hits)} hits)")
    except Exception as e:
        results["search"] = False
        print(f" [FAIL] Test 5: {e}")

    # Test 6: Bus Channel Events
    try:
        events_received = []
        bus.on_channel("pipeline.events", lambda msg: events_received.append(msg))
        bus.publish("router", "pipeline.events", {
            "event": "workflow.test",
            "squad": "test"
        })
        assert len(events_received) >= 1
        results["channel_events"] = True
        print(f" [OK] Test 6: Bus Channel Events ({len(events_received)} events)")
    except Exception as e:
        results["channel_events"] = False
        print(f" [FAIL] Test 6: {e}")

    # Test 7: Route Configuration
    try:
        router.add_route("test_route", {
            "trigger_squad": "test",
            "target_squad": "dev",
            "target_workflow": "code_workflows",
            "target_pipeline": "spec_driven_dev",
            "input_mapping": {"user_prompt": "output"}
        })
        assert "test_route" in router.routes
        router.remove_route("test_route")
        assert "test_route" not in router.routes
        results["route_config"] = True
        print(" [OK] Test 7: Route Configuration")
    except Exception as e:
        results["route_config"] = False
        print(f" [FAIL] Test 7: {e}")

    # Test 8: Squad Workflow via Router (mock)
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(
            router.run_squad_workflow(
                "dev_squad", "code_workflows", "spec_driven_dev",
                {"user_prompt": "Create a simple logger class"},
                thread_id="test_workflow_run", auto_chain=False
            )
        )
        assert "specification" in result
        assert "implementation" in result
        conv = router.get_conversation("test_workflow_run")
        assert len(conv) > 0
        results["workflow_run"] = True
        print(f" [OK] Test 8: Squad Workflow via Router ({len(conv)} turns logged)")
        loop.close()
    except Exception as e:
        results["workflow_run"] = False
        print(f" [FAIL] Test 8: {e}")

    # Test 9: Stats
    try:
        s = router.stats()
        assert "bus" in s
        assert "routes" in s
        assert "conversations" in s
        results["stats"] = True
        print(f" [OK] Test 9: Stats (agents={s['bus']['agents_registered']}, routes={len(s['routes'])})")
    except Exception as e:
        results["stats"] = False
        print(f" [FAIL] Test 9: {e}")

    # Cleanup test artifacts
    try:
        shutil.rmtree(test_conv_dir, ignore_errors=True)
    except Exception:
        pass

    # Summary
    print("\n" + "=" * 60)
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    for name, ok in results.items():
        print(f"  {'[PASS]' if ok else '[FAIL]'} {name}")
    print(f"\n  RESULT: {passed}/{total} tests passed")
    print("=" * 60)
    return passed == total


if __name__ == "__main__":  # pragma: no cover
    success = _run_tests()
    sys.exit(0 if success else 1)
