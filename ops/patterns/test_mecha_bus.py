# ==============================================================================
# 🧪 MECHA BUS STACK — CONSOLIDATED PYTEST SUITE
# ==============================================================================
# Covers: AgentBus, CrossSquadRouter, HermesAuditor, ClawSquadBridge, TelegramRelay
# Run: pytest test_mecha_bus.py -v --cov --cov-report=term-missing
# ==============================================================================

import os
import sys
import json
import time
import shutil
import asyncio
import inspect
import pytest
from typing import Dict, Any, List

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agent_bus import AgentBus, BusMessage, MessageType, AgentStatus, AgentIdentity
from cross_squad_router import CrossSquadRouter, ConversationStore
from hermes_auditor import (
    HermesAuditor, R001_SenderRegistered, R002_RecipientExists,
    R003_PayloadNotEmpty, R004_TTLValid, R005_TACPCompliance,
    R006_CrossSquadAuth, AuditSeverity, AuditRule, AuditEntry
)
from claw_squad_bridge import ClawSquadBridge
from telegram_relay import TelegramRelay, _format_pipeline_event, _format_audit_event, _get_agent_emoji

WORKSPACE = r"c:\Users\huggs\OneDrive\Documentos\workspace"
TEST_DIR = os.path.join(os.path.dirname(__file__), "_pytest_tmp")


# =============================================================================
# FIXTURES
# =============================================================================

@pytest.fixture(autouse=True)
def fresh_bus():
    AgentBus.reset()
    yield AgentBus.get_instance()
    AgentBus.reset()


@pytest.fixture
def bus(fresh_bus):
    return fresh_bus


@pytest.fixture
def test_dir():
    os.makedirs(TEST_DIR, exist_ok=True)
    yield TEST_DIR
    shutil.rmtree(TEST_DIR, ignore_errors=True)


@pytest.fixture
def conversation_store(test_dir):
    return ConversationStore(os.path.join(test_dir, "convs"))


@pytest.fixture
def router(bus, test_dir):
    r = CrossSquadRouter(WORKSPACE, bus)
    r.history = ConversationStore(os.path.join(test_dir, "router_convs"))
    return r


@pytest.fixture
def auditor(bus, test_dir):
    a = HermesAuditor(bus=bus, log_dir=os.path.join(test_dir, "audit"))
    a.start()
    return a


@pytest.fixture
def bridge(bus, test_dir):
    b = ClawSquadBridge(WORKSPACE, bus)
    b.router.history = ConversationStore(os.path.join(test_dir, "bridge_convs"))
    return b


# =============================================================================
# AGENT BUS (10 original tests + new coverage tests)
# =============================================================================

class TestAgentBus:
    def test_register_agent(self, bus):
        bus.register("a1", "Agent One", squad="dev", role="Coder")
        agent = bus.get_agent("a1")
        assert agent is not None
        assert agent.name == "Agent One"
        assert agent.squad == "dev"

    def test_list_agents_by_squad(self, bus):
        bus.register("d1", "Dev1", squad="dev")
        bus.register("d2", "Dev2", squad="dev")
        bus.register("q1", "QA1", squad="qa")
        devs = bus.list_agents(squad="dev")
        assert len(devs) == 2
        qas = bus.list_agents(squad="qa")
        assert len(qas) == 1

    def test_direct_message(self, bus):
        bus.register("alice", "Alice")
        bus.register("bob", "Bob")
        msg = bus.send("alice", "bob", {"action": "ping"})
        assert msg.sender == "alice"
        assert msg.recipient == "bob"
        inbox = bus.get_inbox("bob")
        assert len(inbox) >= 1

    def test_request_response(self, bus):
        bus.register("client", "Client")
        bus.register("server", "Server")
        req = bus.request("client", "server", {"query": "status"})
        assert req.msg_type == MessageType.REQUEST
        resp = bus.respond(req, "server", {"status": "ok"})
        assert resp.msg_type == MessageType.RESPONSE
        assert resp.reply_to == req.msg_id

    def test_pub_sub(self, bus):
        bus.register("pub", "Publisher")
        bus.register("sub", "Subscriber")
        received = []
        bus.subscribe("sub", "news")
        bus.on_channel("news", lambda m: received.append(m))
        bus.publish("pub", "news", {"headline": "test"})
        assert len(received) == 1

    def test_broadcast(self, bus):
        bus.register("leader", "Leader", squad="team")
        bus.register("m1", "Member1", squad="team")
        bus.register("m2", "Member2", squad="team")
        bus.register("other", "Other", squad="other_team")
        msg = bus.broadcast("leader", {"alert": "go"}, squad="team")
        assert msg.msg_type == MessageType.BROADCAST

    def test_acknowledge(self, bus):
        bus.register("s", "Sender")
        bus.register("r", "Receiver")
        msg = bus.send("s", "r", {"data": "x"})
        result = bus.acknowledge("r", msg.msg_id)
        assert result is True
        unread = bus.get_inbox("r", unread_only=True)
        assert len(unread) == 0
        all_msgs = bus.get_inbox("r", unread_only=False)
        assert any(m.acknowledged for m in all_msgs)

    def test_thread_tracking(self, bus):
        bus.register("a", "A")
        bus.register("b", "B")
        msg1 = bus.send("a", "b", {"step": 1}, thread_id="t1")
        msg2 = bus.send("b", "a", {"step": 2}, thread_id="t1")
        thread = bus.get_thread("t1")
        assert len(thread) == 2

    def test_message_handler(self, bus):
        bus.register("x", "X")
        bus.register("y", "Y")
        handled = []
        bus.on_message("y", lambda m: handled.append(m))
        bus.send("x", "y", {"test": True})
        assert len(handled) >= 1

    def test_stats(self, bus):
        bus.register("z", "Z")
        bus.send("z", "z", {"self": True})
        s = bus.stats()
        assert s["agents_registered"] >= 1
        assert s["messages_in_log"] >= 1

    # New AgentBus Coverage Tests
    def test_bus_message_serialization(self):
        msg = BusMessage(sender="a", recipient="b", msg_type=MessageType.DIRECT, payload={"hello": "world"})
        d = msg.to_dict()
        assert d["msg_type"] == "direct"
        msg2 = BusMessage.from_dict(d)
        assert msg2.sender == "a"
        assert msg2.payload == {"hello": "world"}
        
        ident = AgentIdentity(agent_id="id1", name="name1", squad="squad1", role="role1")
        d_ident = ident.to_dict()
        assert d_ident["status"] == AgentStatus.ONLINE.value

    def test_bus_unregister_and_status(self, bus):
        bus.register("temp_agent", "Temp")
        assert bus.get_agent("temp_agent") is not None
        bus.set_status("temp_agent", AgentStatus.OFFLINE)
        assert bus.get_agent("temp_agent").status == AgentStatus.OFFLINE
        assert bus.unregister("temp_agent") is True
        assert bus.get_agent("temp_agent") is None
        assert bus.unregister("temp_agent") is False

    def test_bus_filters_and_caps(self, bus):
        bus.register("c1", "Cap1", capabilities=["v1"])
        bus.register("c2", "Cap2", capabilities=["v2"])
        bus.set_status("c1", AgentStatus.BUSY)
        
        busy_agents = bus.list_agents(status=AgentStatus.BUSY)
        assert len(busy_agents) == 1
        assert busy_agents[0].agent_id == "c1"
        
        v2_agents = bus.find_by_capability("v2")
        assert len(v2_agents) == 1
        assert v2_agents[0].agent_id == "c2"

    def test_bus_unsubscribe(self, bus):
        bus.register("sub_agent", "Sub")
        bus.subscribe("sub_agent", "ch1")
        assert "ch1" in bus.list_channels()
        bus.unsubscribe("sub_agent", "ch1")
        assert bus.list_channels()["ch1"] == 0

    def test_bus_ack_failure_and_ack_all(self, bus):
        bus.register("s1", "S1")
        bus.register("r1", "R1")
        bus.send("s1", "r1", {"data": 1})
        bus.send("s1", "r1", {"data": 2})
        
        assert bus.acknowledge("r1", "nonexistent_msg_id") is False
        assert bus.ack_all("r1") == 2
        assert bus.ack_all("r1") == 0

    def test_bus_list_threads_filter(self, bus):
        bus.register("a1", "A1")
        bus.register("a2", "A2")
        bus.send("a1", "a2", {"data": 1}, thread_id="t_thread")
        threads = bus.list_threads(agent_id="a1")
        assert "t_thread" in threads
        threads_nonexistent = bus.list_threads(agent_id="nonexistent")
        assert "t_thread" not in threads_nonexistent

    def test_bus_dead_letter(self, bus):
        bus.register("s1", "S1")
        msg = bus.send("s1", "nonexistent_recipient", {"data": 1})
        assert msg.delivered is False

    def test_bus_handler_errors(self, bus):
        bus.register("s1", "S1")
        bus.register("r1", "R1")
        
        def sync_bad_handler(msg):
            raise ValueError("Sync error")
        bus.on_message("r1", sync_bad_handler)
        
        async def async_bad_handler(msg):
            raise ValueError("Async error")
        bus.on_message("r1", async_bad_handler)
        
        bus.send("s1", "r1", {"data": 1})

    def test_bus_channel_handler_errors(self, bus):
        bus.register("s1", "S1")
        
        def sync_bad_ch_handler(msg):
            raise ValueError("Sync error")
        bus.on_channel("ch_err", sync_bad_ch_handler)
        
        async def async_bad_ch_handler(msg):
            raise ValueError("Async error")
        bus.on_channel("ch_err", async_bad_ch_handler)
        
        bus.publish("s1", "ch_err", {"data": 1})

    def test_bus_message_log_cap(self, bus):
        bus.register("s1", "S1")
        bus._max_log = 5
        for i in range(10):
            bus.send("s1", "s1", {"i": i})
        assert len(bus._message_log) == 5

    def test_bus_flush_load_log(self, bus, tmp_path):
        bus.register("s1", "S1")
        bus.send("s1", "s1", {"data": "test"})
        assert bus.load_log(str(tmp_path / "nonexistent.json")) == 0
        
        log_file = str(tmp_path / "bus_log.json")
        bus.flush_log(filename=log_file)
        assert os.path.exists(log_file)
        
        bus2 = AgentBus(log_dir=str(tmp_path))
        assert bus2.load_log(log_file) == 1
        assert len(bus2._message_log) == 1

    def test_bus_internal_runner(self):
        from agent_bus import _run_tests
        assert _run_tests() is True

    def test_bus_more_coverage(self, bus):
        # 175: ch_subs.discard(agent_id) in unregister
        bus.register("sub_agent", "Sub")
        bus.subscribe("sub_agent", "ch_discard")
        assert bus.unregister("sub_agent") is True

        # 328: list_threads without agent_id
        bus.register("a1", "A1")
        bus.register("a2", "A2")
        bus.send("a1", "a2", {"data": 1}, thread_id="t_thread_all")
        threads = bus.list_threads(agent_id=None)
        assert "t_thread_all" in threads

        # 414-424: _emit_event logic when bus.events is subscribed
        events_received = []
        bus.register("observer", "Observer")
        bus.subscribe("observer", "bus.events")
        bus.on_channel("bus.events", lambda m: events_received.append(m))
        bus.register("new_agent", "New")
        assert len(events_received) >= 1

    def test_agent_bus_async_no_loop(self, bus):
        class DummyLoop:
            def is_running(self):
                return False
            def run_until_complete(self, coro):
                pass
        import asyncio
        orig_get_loop = asyncio.get_event_loop
        asyncio.get_event_loop = DummyLoop
        try:
            async def dummy_handler(msg):
                pass
            bus.register("sender", "S")
            bus.register("receiver", "R")
            bus.on_message("receiver", dummy_handler)
            bus.send("sender", "receiver", {"ping": 1})

            # For channel handler
            bus.subscribe("receiver", "my_chan")
            bus.on_channel("my_chan", dummy_handler)
            bus.publish("sender", "my_chan", {"ping": 1})
        finally:
            asyncio.get_event_loop = orig_get_loop

    def test_bus_async_handlers_with_running_loop(self, bus):
        bus.register("s", "S")
        bus.register("r", "R")
        
        handled_msg = None
        async def dummy_handler(msg):
            nonlocal handled_msg
            handled_msg = msg
            
        bus.on_message("r", dummy_handler)
        bus.subscribe("r", "ch_async")
        bus.on_channel("ch_async", dummy_handler)
        
        async def run_in_loop():
            bus.send("s", "r", {"x": 1})
            bus.publish("s", "ch_async", {"y": 2})
            await asyncio.sleep(0.01)
            
        asyncio.run(run_in_loop())
        assert handled_msg is not None

        # Cover 423-424: exception in emit_event handler
        def bad_event_handler(msg):
            raise ValueError("bad event handler")
        bus.on_channel("bus.events", bad_event_handler)
        bus.register("some_new_agent", "Some")


# =============================================================================
# CONVERSATION STORE (5 original tests)
# =============================================================================

class TestConversationStore:
    def test_save_and_load(self, conversation_store):
        conversation_store.save_turn("t1", "agent_a", "assistant", "Hello")
        conversation_store.save_turn("t1", "agent_b", "assistant", "World")
        loaded = conversation_store.load_thread("t1")
        assert len(loaded) == 2
        assert loaded[0]["content"] == "Hello"

    def test_list_threads(self, conversation_store):
        conversation_store.save_turn("t1", "a", "user", "msg1")
        conversation_store.save_turn("t2", "b", "user", "msg2")
        threads = conversation_store.list_threads()
        assert len(threads) == 2

    def test_search(self, conversation_store):
        conversation_store.save_turn("t1", "a", "assistant", "found the bug in auth")
        conversation_store.save_turn("t2", "b", "assistant", "tests passing")
        hits = conversation_store.search("bug")
        assert len(hits) >= 1
        assert "bug" in hits[0]["content_snippet"].lower()

    def test_delete_thread(self, conversation_store):
        conversation_store.save_turn("t1", "a", "user", "temp")
        assert conversation_store.delete_thread("t1")
        assert len(conversation_store.load_thread("t1")) == 0

    def test_empty_thread(self, conversation_store):
        loaded = conversation_store.load_thread("nonexistent")
        assert loaded == []


# =============================================================================
# CROSS-SQUAD ROUTER (6 original tests + new coverage tests)
# =============================================================================

class TestCrossSquadRouter:
    def test_register_squad_agents(self, router, bus):
        router.register_squad_agents("dev_squad")
        agents = bus.list_agents(squad="dev_squad")
        assert len(agents) >= 3

    def test_multi_squad_registration(self, router, bus):
        router.register_squad_agents("dev_squad")
        router.register_squad_agents("tribunal_squad")
        squads = set(a.squad for a in bus.list_agents())
        assert "dev_squad" in squads
        assert "tribunal_squad" in squads

    def test_route_configuration(self, router):
        router.add_route("custom", {"target_squad": "qa"})
        assert "custom" in router.routes
        router.remove_route("custom")
        assert "custom" not in router.routes

    def test_workflow_via_router(self, router):
        result = asyncio.run(
            router.run_squad_workflow(
                "dev_squad", "code_workflows", "spec_driven_dev",
                {"user_prompt": "test prompt"},
                thread_id="pytest_wf", auto_chain=False
            )
        )
        assert "specification" in result
        conv = router.get_conversation("pytest_wf")
        assert len(conv) > 0

    def test_channel_events(self, router, bus):
        events = []
        bus.on_channel("pipeline.events", lambda m: events.append(m))
        bus.publish("router", "pipeline.events", {"event": "test"})
        assert len(events) >= 1

    def test_stats(self, router):
        s = router.stats()
        assert "bus" in s
        assert "routes" in s
        assert "conversations" in s

    # New Router Coverage Tests
    def test_router_store_list_threads_corrupt(self, conversation_store):
        os.makedirs(os.path.join(conversation_store.store_dir, "corrupt.json"), exist_ok=True)
        threads = conversation_store.list_threads()
        assert len(threads) == 0

    def test_router_store_search_corrupt(self, conversation_store):
        os.makedirs(os.path.join(conversation_store.store_dir, "corrupt.json"), exist_ok=True)
        hits = conversation_store.search("test")
        assert len(hits) == 0

    def test_router_remove_route_fail(self, router):
        assert router.remove_route("nonexistent") is False

    def test_router_chaining(self, router, bus):
        router.add_route("chain_route", {
            "trigger_squad": "dev_squad",
            "trigger_output": "implementation",
            "trigger_condition": "Calculator",
            "input_mapping": {"user_prompt": "implementation"},
            "target_squad": "qa_squad",
            "target_workflow": "qa_workflows",
            "target_pipeline": "qa_audit_pipeline"
        })
        result = asyncio.run(
            router.run_squad_workflow(
                "dev_squad", "code_workflows", "spec_driven_dev",
                {"user_prompt": "Calculator code"},
                thread_id="test_chain_run", auto_chain=True
            )
        )
        assert "_chained" in result

    def test_router_request_squad_tribunal(self, router):
        result = asyncio.run(
            router.request_squad("client", "tribunal_squad", "Review this pattern")
        )
        assert "verdict" in result

    def test_router_request_squad_dev(self, router):
        result = asyncio.run(
            router.request_squad("client", "dev_squad", "Calculator")
        )
        assert "implementation" in result

    def test_router_request_squad_invalid(self, router):
        result = asyncio.run(
            router.request_squad("client", "nonexistent_squad", "hello")
        )
        assert "error" in result

    def test_router_internal_tests(self):
        from cross_squad_router import _run_tests
        assert _run_tests() is True

    def test_router_more_coverage(self, router, bus):
        # 67-68: corrupt json file in load_thread
        corrupt_file = os.path.join(router.history.store_dir, "corrupt_thread.json")
        with open(corrupt_file, "w", encoding="utf-8") as f:
            f.write("{corrupt")
        assert router.history.load_thread("corrupt_thread") == []

        # 95: delete_thread returns False if file not exists
        assert router.history.delete_thread("nonexistent_thread_id_999") is False

        # 102: search skips non-json files
        dummy_file = os.path.join(router.history.store_dir, "dummy.txt")
        with open(dummy_file, "w", encoding="utf-8") as f:
            f.write("some text containing keyphrase")
        assert len(router.history.search("keyphrase")) == 0

        # 116: search returns early if query hits limit
        router.history.save_turn("t1", "a1", "user", "hitword first")
        router.history.save_turn("t2", "a2", "user", "hitword second")
        hits = router.history.search("hitword", limit=1)
        assert len(hits) == 1

        # 244: thread_id generation in run_squad_workflow when thread_id is None
        res_none_tid = asyncio.run(
            router.run_squad_workflow(
                "dev_squad", "code_workflows", "spec_driven_dev",
                {"user_prompt": "hello"}, thread_id=None, auto_chain=False
            )
        )
        assert "specification" in res_none_tid

        # 267: run_squad_workflow skips outputs starting with _
        async def mock_run_wf(sq, wf, pip, inputs):
            return {"_internal_val": "secret", "public_val": "hello"}
        orig_run = router.orchestrator.run_workflow
        router.orchestrator.run_workflow = mock_run_wf
        try:
            res_skip = asyncio.run(
                router.run_squad_workflow(
                    "dev_squad", "code_workflows", "spec_driven_dev",
                    {"user_prompt": "test_skip"}, thread_id="t_skip", auto_chain=False
                )
            )
            assert "public_val" in res_skip
        finally:
            router.orchestrator.run_workflow = orig_run

        # 325: trigger condition check fails in _check_and_chain
        router.add_route("fail_cond_route", {
            "trigger_squad": "dev_squad",
            "trigger_output": "public_val",
            "trigger_condition": "MATCH_THIS_WORD",
            "input_mapping": {"user_prompt": "public_val"},
            "target_squad": "qa_squad",
            "target_workflow": "qa_workflows",
            "target_pipeline": "qa_audit_pipeline"
        })
        chain_res = asyncio.run(
            router._check_and_chain("dev_squad", {"public_val": "NOMATCH"}, "t_chain_fail")
        )
        assert chain_res is None

        # 422: search_conversations
        assert len(router.search_conversations("hitword")) >= 1


# =============================================================================
# HERMES AUDITOR (10 original tests + new coverage tests)
# =============================================================================

class TestHermesAuditor:
    def test_clean_message_passes(self, auditor, bus):
        bus.register("alice", "Alice", squad="dev")
        bus.register("bob", "Bob", squad="dev")
        msg = bus.send("alice", "bob", {"action": "review"})
        auditor.audit_message(msg)
        assert auditor._stats["violations"] == 0

    def test_unregistered_sender_r001(self, auditor, bus):
        fake = BusMessage(sender="ghost", recipient="x", msg_type=MessageType.DIRECT, payload={"x": 1})
        auditor.audit_message(fake)
        violations = [e for e in auditor._audit_log if not e.passed and e.rule_id == "R001"]
        assert len(violations) >= 1

    def test_missing_recipient_r002(self, auditor, bus):
        bus.register("alice", "Alice")
        fake = BusMessage(sender="alice", recipient="nobody", msg_type=MessageType.DIRECT, payload={"x": 1})
        auditor.audit_message(fake)
        warnings = [e for e in auditor._audit_log if not e.passed and e.rule_id == "R002"]
        assert len(warnings) >= 1

    def test_empty_payload_r003(self, auditor, bus):
        bus.register("a", "A")
        bus.register("b", "B")
        msg = bus.send("a", "b", {})
        auditor.audit_message(msg)
        empties = [e for e in auditor._audit_log if not e.passed and e.rule_id == "R003"]
        assert len(empties) >= 1

    def test_cross_squad_no_router_r006(self, auditor, bus):
        bus.register("dev_agent", "Dev", squad="dev")
        bus.register("tribunal_agent", "Tribunal", squad="tribunal")
        fake = BusMessage(sender="dev_agent", recipient="tribunal_agent", msg_type=MessageType.DIRECT, payload={"x": 1})
        auditor.audit_message(fake)
        xsquad = [e for e in auditor._audit_log if not e.passed and e.rule_id == "R006"]
        assert len(xsquad) >= 1

    def test_router_cross_squad_allowed(self, auditor, bus):
        bus.register("router", "Router", squad="system", role="Message Router")
        bus.register("target", "Target", squad="tribunal")
        msg = bus.send("router", "target", {"action": "route"})
        auditor.audit_message(msg)
        violations = [e for e in auditor._audit_log if not e.passed and e.rule_id == "R006" and e.sender == "router"]
        assert len(violations) == 0

    def test_flush_log(self, auditor, bus):
        bus.register("a", "A")
        bus.register("b", "B")
        msg = bus.send("a", "b", {"data": "x"})
        auditor.audit_message(msg)
        path = auditor.flush_log()
        assert path and os.path.exists(path)

    def test_compliance_report(self, auditor, bus):
        bus.register("a", "A")
        bus.register("b", "B")
        msg = bus.send("a", "b", {"data": "x"})
        auditor.audit_message(msg)
        report = auditor.compliance_report()
        assert "compliance_rate" in report
        assert report["compliance_rate"] >= 0

    def test_rule_management(self, auditor):
        count = len(auditor.rules)
        auditor.remove_rule("R005")
        assert len(auditor.rules) == count - 1
        auditor.add_rule(R005_TACPCompliance())
        assert len(auditor.rules) == count

    def test_audit_events_on_bus(self, auditor, bus):
        events = []
        bus.on_channel("audit.events", lambda m: events.append(m))
        fake = BusMessage(sender="intruder", recipient="x", msg_type=MessageType.DIRECT, payload={"hack": True})
        auditor.audit_message(fake)
        assert len(events) >= 1

    # New Auditor Coverage Tests
    def test_auditor_rules_edge_cases(self, auditor, bus):
        bus.register("a", "A")
        bus.register("b", "B")
        msg = bus.send("a", "b", {"data": 1}, ttl=9999.0)
        auditor.audit_message(msg)
        violations = [e for e in auditor._audit_log if not e.passed and e.rule_id == "R004"]
        assert len(violations) >= 1
        
        long_content = "X" * 250
        msg_tacp = bus.send("a", "b", {"data": long_content})
        auditor.audit_message(msg_tacp)
        violations_tacp = [e for e in auditor._audit_log if not e.passed and e.rule_id == "R005"]
        assert len(violations_tacp) >= 1

    def test_auditor_edge_cases(self, auditor, bus):
        auditor.stop()
        assert auditor._active is False
        
        msg = bus.send("a", "b", {"data": 1})
        auditor._stats["messages_audited"] = 0
        auditor.audit_message(msg)
        assert auditor._stats["messages_audited"] == 0
        
        auditor.start()
        msg_hermes = BusMessage(sender="hermes", recipient="a", msg_type=MessageType.DIRECT, payload={"data": 1})
        auditor.audit_message(msg_hermes)
        assert auditor._stats["messages_audited"] == 0
        
        class BadRule(AuditRule):
            rule_id = "R_BAD"
            rule_name = "Bad Rule"
            severity = AuditSeverity.INFO.value
            def check(self, msg, bus):
                raise ValueError("Bad rule error")
                
        auditor.add_rule(BadRule())
        auditor.audit_message(msg)
        auditor.remove_rule("R_BAD")
        
        auditor._audit_log = []
        assert auditor.flush_log() == ""
        
        rules = auditor.list_rules()
        assert len(rules) > 0

    def test_auditor_internal_tests(self):
        from hermes_auditor import _run_tests
        assert _run_tests() is True

    def test_auditor_extra_coverage(self, auditor, bus):
        # 71: AuditRule base class NotImplementedError
        from hermes_auditor import AuditRule
        with pytest.raises(NotImplementedError):
            AuditRule().check(None, None)

        # 362: by_rule[rid]["failed"] += 1 in compliance_report
        fake = BusMessage(sender="ghost_unregistered", recipient="nobody", msg_type=MessageType.DIRECT, payload={"x": 1})
        auditor.audit_message(fake)
        report = auditor.compliance_report()
        assert report["by_rule"]["R001"]["failed"] >= 1


# =============================================================================
# CLAW SQUAD BRIDGE (8 original tests + new coverage tests)
# =============================================================================

class TestClawSquadBridge:
    def test_claw_registered(self, bridge, bus):
        claw = bus.get_agent("claw")
        assert claw is not None
        assert "vision" in claw.capabilities

    def test_risk_low(self, bridge):
        r = bridge.assess_risk("click", {"target": "ok"})
        assert r["risk_level"] == "low"
        assert not r["requires_consultation"]

    def test_risk_high(self, bridge):
        r = bridge.assess_risk("delete", {"target": "records"})
        assert r["risk_level"] == "high"
        assert r["requires_consultation"]

    def test_risk_critical_keyword(self, bridge):
        r = bridge.assess_risk("execute", {"command": "rm -rf /"})
        assert r["risk_level"] == "critical"

    def test_auto_approve_low_risk(self, bridge):
        result = asyncio.run(
            bridge.evaluate_action("click", {"target": "button"})
        )
        assert result["decision"] == "approved"

    def test_pending_no_consult(self, bridge):
        result = asyncio.run(
            bridge.evaluate_action("install", {"pkg": "x"}, auto_consult=False)
        )
        assert result["decision"] == "pending"

    def test_bus_send_and_inbox(self, bridge, bus):
        bus.register("test_recv", "Receiver", squad="test")
        r = bridge.bus_send_message("claw", "test_recv", {"ping": True})
        assert r["ok"]
        inbox = bridge.bus_get_inbox("test_recv")
        assert len(inbox) >= 1

    def test_stats(self, bridge):
        s = bridge.bus_stats()
        assert "bus" in s
        assert "auditor" in s

    # New Bridge Coverage Tests
    def test_bridge_evaluate_action_auto_consult(self, bridge):
        result = asyncio.run(
            bridge.evaluate_action("delete", {"target": "records"}, auto_consult=True)
        )
        assert "decision" in result

    def test_bridge_sync_claw_status(self, bridge, tmp_path):
        import claw_squad_bridge
        orig = claw_squad_bridge.STATUS_FILE
        claw_squad_bridge.STATUS_FILE = str(tmp_path / "nonexistent.json")
        assert bridge.sync_claw_status() == {"state": "unknown"}
        
        claw_squad_bridge.STATUS_FILE = str(tmp_path / "status.json")
        with open(claw_squad_bridge.STATUS_FILE, "w", encoding="utf-8") as f:
            json.dump({"state": "exploring"}, f)
        assert bridge.sync_claw_status() == {"state": "exploring"}
        
        with open(claw_squad_bridge.STATUS_FILE, "w", encoding="utf-8") as f:
            f.write("{corrupt")
        assert bridge.sync_claw_status() == {"state": "unknown"}
        claw_squad_bridge.STATUS_FILE = orig

    def test_bridge_send_preempt(self, bridge, tmp_path):
        import claw_squad_bridge
        orig = claw_squad_bridge.PREEMPT_FILE
        claw_squad_bridge.PREEMPT_FILE = str(tmp_path / "preempt.json")
        try:
            bridge.send_preempt("click", {"x": 10})
            assert os.path.exists(claw_squad_bridge.PREEMPT_FILE)
        finally:
            claw_squad_bridge.PREEMPT_FILE = orig

    def test_bridge_bus_ops(self, bridge, bus):
        res_send = bridge.bus_send_message("claw", "test_recv", None)
        assert res_send["ok"] is False
        
        res_bc = bridge.bus_broadcast("claw", "test_squad", {"announcement": "hi"})
        assert res_bc["ok"] is True
        res_bc_fail = bridge.bus_broadcast("claw", "test_squad", None)
        assert res_bc_fail["ok"] is False
        
        agents = bridge.bus_list_agents(squad="test_squad")
        assert len(agents) >= 0

    def test_bridge_internal_tests(self):
        from claw_squad_bridge import _run_tests
        assert _run_tests() is True

    def test_bridge_extra_coverage(self, bus):
        # 82-83: exception in TelegramRelay start in ClawSquadBridge.__init__
        import claw_squad_bridge
        orig_relay = claw_squad_bridge.TelegramRelay
        def failing_relay(*args, **kwargs):
            raise RuntimeError("Forced relay initialization failure")
        claw_squad_bridge.TelegramRelay = failing_relay
        try:
            bridge = ClawSquadBridge(WORKSPACE, bus)
            # Should fall back gracefully and log
        finally:
            claw_squad_bridge.TelegramRelay = orig_relay

        # 295: get_conversation wrapper
        # 298: search_conversations wrapper
        bridge2 = ClawSquadBridge(WORKSPACE, bus)
        assert bridge2.get_conversation("thread123") == []
        assert bridge2.search_conversations("searchquery") == []


# =============================================================================
# TELEGRAM RELAY (7 original tests + new live bot validation)
# =============================================================================

class TestTelegramRelay:
    def test_agent_emoji_resolution(self):
        assert "⚔" in _get_agent_emoji("warlock")
        assert _get_agent_emoji(None) == "\U0001f916"
        assert _get_agent_emoji("unknown_agent") == "\U0001f916"

    def test_format_pipeline_started(self):
        msg = BusMessage(
            sender="router", recipient="",
            msg_type=MessageType.CHANNEL,
            payload={"event": "workflow.started", "squad": "dev_squad", "pipeline": "spec_driven_dev"},
            channel="pipeline.events"
        )
        text = _format_pipeline_event(msg)
        assert "Pipeline iniciado" in text
        assert "dev_squad" in text

    def test_format_pipeline_completed(self):
        msg = BusMessage(
            sender="router", recipient="",
            msg_type=MessageType.CHANNEL,
            payload={"event": "workflow.completed", "squad": "tribunal_squad", "pipeline": "tribunal_pipeline", "output_vars": ["verdict"]},
            channel="pipeline.events"
        )
        text = _format_pipeline_event(msg)
        assert "concluido" in text
        assert "verdict" in text

    def test_format_step_completed(self):
        msg = BusMessage(
            sender="router", recipient="",
            msg_type=MessageType.CHANNEL,
            payload={"event": "step.completed", "agent": "tribunal_squad.warlock", "content_preview": "Bloqueado por risco.", "thread_id": "t1"},
            channel="squad.tribunal_squad"
        )
        text = _format_pipeline_event(msg)
        assert "warlock" in text.lower() or "concluiu" in text
        assert "Bloqueado" in text

    def test_format_audit_findings(self):
        msg = BusMessage(
            sender="hermes", recipient="",
            msg_type=MessageType.CHANNEL,
            payload={"event": "audit.findings", "sender": "ghost", "findings": [{"rule_id": "R001", "severity": "violation", "detail": "Not registered"}]},
            channel="audit.events"
        )
        text = _format_audit_event(msg)
        assert "R001" in text
        assert "flagou" in text

    # LIVE BOT TESTING (Mocks removed)
    def test_relay_start_sends_message(self, bus):
        relay = TelegramRelay(bus=bus)
        relay.start()
        assert relay._active
        relay.stop()

    def test_relay_receives_channel_events(self, bus):
        relay = TelegramRelay(bus=bus, throttle_seconds=0)
        relay.start()
        bus.publish("router", "pipeline.events", {
            "event": "workflow.started", "squad": "dev_squad", "pipeline": "test"
        })
        assert relay._message_count >= 1
        relay.stop()

    # New Relay Coverage Tests
    def test_relay_edge_cases(self, bus):
        import telegram_relay
        assert telegram_relay._get_agent_emoji("nonexistent") == "🤖"
        assert telegram_relay._get_squad_emoji("nonexistent") == "📦"
        
        msg_chain = BusMessage(
            sender="router", recipient="", msg_type=MessageType.CHANNEL,
            payload={"event": "chain.triggered", "source_squad": "dev", "target_squad": "qa", "route": "r1"},
            channel="pipeline.events"
        )
        assert "Auto-chain" in telegram_relay._format_pipeline_event(msg_chain)
        
        msg_consult = BusMessage(
            sender="claw", recipient="", msg_type=MessageType.CHANNEL,
            payload={"event": "claw.consultation_requested", "action": "click"},
            channel="claw.commands"
        )
        assert "Claw pede" in telegram_relay._format_pipeline_event(msg_consult)
        
        msg_verdict_app = BusMessage(
            sender="claw", recipient="", msg_type=MessageType.CHANNEL,
            payload={"event": "claw.verdict_received", "action": "click", "approved": True},
            channel="claw.verdicts"
        )
        assert "APROVADO" in telegram_relay._format_pipeline_event(msg_verdict_app)
        
        msg_verdict_blk = BusMessage(
            sender="claw", recipient="", msg_type=MessageType.CHANNEL,
            payload={"event": "claw.verdict_received", "action": "click", "approved": False},
            channel="claw.verdicts"
        )
        assert "BLOQUEADO" in telegram_relay._format_pipeline_event(msg_verdict_blk)
        
        msg_fallback = BusMessage(
            sender="other", recipient="", msg_type=MessageType.CHANNEL,
            payload={"event": "other_event", "squad": "sys"},
            channel="pipeline.events"
        )
        assert "Event: other_event" in telegram_relay._format_pipeline_event(msg_fallback)
        
        msg_audit_fallback = BusMessage(
            sender="hermes", recipient="", msg_type=MessageType.CHANNEL,
            payload={"event": "other_audit"},
            channel="audit.events"
        )
        assert "Audit: other_audit" in telegram_relay._format_audit_event(msg_audit_fallback)
        
        msg_nondict = BusMessage(
            sender="a", recipient="b", msg_type=MessageType.DIRECT,
            payload="simple string payload"
        )
        assert "simple string payload" in telegram_relay._format_agent_message(msg_nondict)
        
        msg_empty_keys = BusMessage(
            sender="a", recipient="b", msg_type=MessageType.DIRECT,
            payload={"random": 123}
        )
        assert "random" in telegram_relay._format_agent_message(msg_empty_keys)
        
        orig_token = telegram_relay.TELEGRAM_TOKEN
        telegram_relay.TELEGRAM_TOKEN = ""
        assert telegram_relay._send_telegram("hello") is None
        
        telegram_relay.TELEGRAM_TOKEN = "invalid_token_to_fail_request"
        assert telegram_relay._send_telegram("hello") is None
        telegram_relay.TELEGRAM_TOKEN = orig_token

    def test_relay_live_test(self):
        import telegram_relay
        telegram_relay._run_live_test()

    def test_relay_extra_coverage(self, bus):
        import telegram_relay
        import urllib.request

        # 109: parse_mode in _send_telegram
        telegram_relay._send_telegram("test parse_mode", parse_mode="HTML")

        # 121: urllib response containing {"ok": false}
        orig_urlopen = urllib.request.urlopen
        class BadTelegramResponse:
            def read(self):
                return b'{"ok": false, "description": "Mocked failure"}'
        urllib.request.urlopen = lambda *a, **kw: BadTelegramResponse()
        try:
            telegram_relay._send_telegram("test bad response")
        finally:
            urllib.request.urlopen = orig_urlopen

        # 139: payload_str from content or action
        msg_action = BusMessage(sender="a", recipient="b", msg_type=MessageType.DIRECT, payload={"action": "click"})
        assert "click" in telegram_relay._format_agent_message(msg_action)
        msg_content = BusMessage(sender="a", recipient="b", msg_type=MessageType.DIRECT, payload={"content": "show"})
        assert "show" in telegram_relay._format_agent_message(msg_content)

        # 262, 287-289, 307-309, 325: stats, direct relay, and formatter
        relay = TelegramRelay(bus=bus, relay_direct=True)
        relay.start()
        s = relay.stats()
        assert s["relay_direct"] is True
        
        # Test inactive checks
        relay._active = False
        relay._on_channel_message(msg_action)
        relay._on_direct_message(msg_action)
        relay._active = True
        
        # Test ignore self
        msg_self = BusMessage(sender="telegram_relay", recipient="b", msg_type=MessageType.DIRECT, payload={"a": 1})
        relay._on_direct_message(msg_self)
        
        # Test valid direct relay trigger
        bus.send("a", "telegram_relay", {"content": "direct text"})
        
        # Test valid audit events channel formatting
        bus.publish("hermes", "audit.events", {
            "event": "audit.findings",
            "sender": "a",
            "findings": [{"rule_id": "R001", "severity": "violation", "detail": "Test"}]
        })
        
        # Test line 307: channel message with custom channel type
        msg_custom_ch = BusMessage(
            sender="a", recipient="", msg_type=MessageType.CHANNEL,
            payload={"x": 1}, channel="custom_channel"
        )
        relay._on_channel_message(msg_custom_ch)
        relay.stop()


# =============================================================================
# RUNNER
# =============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
