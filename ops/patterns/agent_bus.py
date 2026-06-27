# ==============================================================================
# 🚀 MECHA AGENT BUS - CENTRALIZED INTER-AGENT COMMUNICATION
# ==============================================================================
# Core message bus for agent-to-agent, agent-to-squad, and broadcast messaging.
# Replaces file-based IPC with in-memory pub/sub + persistent message log.
# ==============================================================================

import os
import sys
import json
import time
import uuid
import asyncio
import inspect
import logging
from enum import Enum
from typing import Dict, Any, List, Optional, Callable, Set
from dataclasses import dataclass, field, asdict

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger("MECHA_AgentBus")


# =============================================================================
# MESSAGE TYPES
# =============================================================================

class MessageType(str, Enum):
    DIRECT = "direct"
    BROADCAST = "broadcast"
    CHANNEL = "channel"
    REQUEST = "request"
    RESPONSE = "response"
    EVENT = "event"


class AgentStatus(str, Enum):
    ONLINE = "online"
    BUSY = "busy"
    OFFLINE = "offline"


# =============================================================================
# MESSAGE MODEL
# =============================================================================

@dataclass
class BusMessage:
    sender: str
    recipient: str
    msg_type: MessageType
    payload: Dict[str, Any]
    channel: Optional[str] = None
    reply_to: Optional[str] = None
    thread_id: Optional[str] = None
    msg_id: str = field(default_factory=lambda: f"msg_{uuid.uuid4().hex[:12]}")
    timestamp: float = field(default_factory=time.time)
    ttl: float = 300.0
    delivered: bool = False
    acknowledged: bool = False

    def to_dict(self) -> dict:
        d = asdict(self)
        d["msg_type"] = self.msg_type.value
        return d

    @classmethod
    def from_dict(cls, data: dict) -> "BusMessage":
        data["msg_type"] = MessageType(data["msg_type"])
        return cls(**data)

    @property
    def is_expired(self) -> bool:
        return (time.time() - self.timestamp) > self.ttl


# =============================================================================
# AGENT IDENTITY
# =============================================================================

@dataclass
class AgentIdentity:
    agent_id: str
    name: str
    squad: Optional[str] = None
    role: Optional[str] = None
    status: AgentStatus = AgentStatus.ONLINE
    capabilities: List[str] = field(default_factory=list)
    registered_at: float = field(default_factory=time.time)

    def to_dict(self) -> dict:
        d = asdict(self)
        d["status"] = self.status.value
        return d


# =============================================================================
# AGENT BUS - CORE
# =============================================================================

class AgentBus:
    """
    Centralized message bus for MECHA inter-agent communication.

    Features:
    - Agent registry with identity, squad, role, capabilities
    - Direct messaging (agent-to-agent)
    - Channel-based pub/sub
    - Broadcast to all agents or squad members
    - Per-agent inbox with TTL expiry
    - Async message handlers
    - Persistent message log (JSON)
    - Thread-based conversation tracking
    """

    _instance: Optional["AgentBus"] = None

    def __init__(self, log_dir: Optional[str] = None):
        self._agents: Dict[str, AgentIdentity] = {}
        self._inboxes: Dict[str, List[BusMessage]] = {}
        self._channels: Dict[str, Set[str]] = {}
        self._handlers: Dict[str, List[Callable]] = {}
        self._channel_handlers: Dict[str, List[Callable]] = {}
        self._threads: Dict[str, List[str]] = {}
        self._message_log: List[BusMessage] = []
        self._log_dir = log_dir or self._default_log_dir()
        self._max_log = 500
        os.makedirs(self._log_dir, exist_ok=True)

    @classmethod
    def get_instance(cls, log_dir: Optional[str] = None) -> "AgentBus":
        if cls._instance is None:
            cls._instance = cls(log_dir)
        return cls._instance

    @classmethod
    def reset(cls):
        cls._instance = None

    @staticmethod
    def _default_log_dir() -> str:
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base, "logs", "bus")

    # -------------------------------------------------------------------------
    # AGENT REGISTRY
    # -------------------------------------------------------------------------

    def register(self, agent_id: str, name: str, squad: str = None,
                 role: str = None, capabilities: List[str] = None) -> AgentIdentity:
        identity = AgentIdentity(
            agent_id=agent_id,
            name=name,
            squad=squad,
            role=role,
            capabilities=capabilities or []
        )
        self._agents[agent_id] = identity
        self._inboxes.setdefault(agent_id, [])
        logger.info(f"[BUS] Agent registered: {agent_id} ({name}) squad={squad}")
        self._emit_event("agent.registered", {"agent_id": agent_id, "name": name, "squad": squad})
        return identity

    def unregister(self, agent_id: str) -> bool:
        if agent_id in self._agents:
            del self._agents[agent_id]
            self._inboxes.pop(agent_id, None)
            for ch_subs in self._channels.values():
                ch_subs.discard(agent_id)
            logger.info(f"[BUS] Agent unregistered: {agent_id}")
            self._emit_event("agent.unregistered", {"agent_id": agent_id})
            return True
        return False

    def set_status(self, agent_id: str, status: AgentStatus):
        if agent_id in self._agents:
            self._agents[agent_id].status = status
            self._emit_event("agent.status_changed", {"agent_id": agent_id, "status": status.value})

    def get_agent(self, agent_id: str) -> Optional[AgentIdentity]:
        return self._agents.get(agent_id)

    def list_agents(self, squad: str = None, status: AgentStatus = None) -> List[AgentIdentity]:
        agents = list(self._agents.values())
        if squad:
            agents = [a for a in agents if a.squad == squad]
        if status:
            agents = [a for a in agents if a.status == status]
        return agents

    def find_by_capability(self, capability: str) -> List[AgentIdentity]:
        return [a for a in self._agents.values() if capability in a.capabilities]

    # -------------------------------------------------------------------------
    # CHANNELS (PUB/SUB)
    # -------------------------------------------------------------------------

    def subscribe(self, agent_id: str, channel: str):
        self._channels.setdefault(channel, set()).add(agent_id)
        logger.info(f"[BUS] {agent_id} subscribed to #{channel}")

    def unsubscribe(self, agent_id: str, channel: str):
        if channel in self._channels:
            self._channels[channel].discard(agent_id)

    def list_channels(self) -> Dict[str, int]:
        return {ch: len(subs) for ch, subs in self._channels.items()}

    # -------------------------------------------------------------------------
    # MESSAGING
    # -------------------------------------------------------------------------

    def send(self, sender: str, recipient: str, payload: Dict[str, Any],
             msg_type: MessageType = MessageType.DIRECT,
             channel: str = None, reply_to: str = None,
             thread_id: str = None, ttl: float = 300.0) -> BusMessage:

        if not thread_id:
            thread_id = f"thread_{uuid.uuid4().hex[:8]}"

        msg = BusMessage(
            sender=sender,
            recipient=recipient,
            msg_type=msg_type,
            payload=payload,
            channel=channel,
            reply_to=reply_to,
            thread_id=thread_id,
            ttl=ttl
        )

        self._track_thread(msg)
        self._log_message(msg)

        if msg_type == MessageType.BROADCAST:
            self._deliver_broadcast(msg, sender)
        elif msg_type == MessageType.CHANNEL and channel:
            self._deliver_channel(msg, channel)
        else:
            self._deliver_direct(msg, recipient)

        self._fire_handlers(msg)
        return msg

    def request(self, sender: str, recipient: str, payload: Dict[str, Any],
                thread_id: str = None, ttl: float = 300.0) -> BusMessage:
        return self.send(sender, recipient, payload,
                         msg_type=MessageType.REQUEST, thread_id=thread_id, ttl=ttl)

    def respond(self, original: BusMessage, responder: str,
                payload: Dict[str, Any]) -> BusMessage:
        return self.send(
            sender=responder,
            recipient=original.sender,
            payload=payload,
            msg_type=MessageType.RESPONSE,
            reply_to=original.msg_id,
            thread_id=original.thread_id
        )

    def broadcast(self, sender: str, payload: Dict[str, Any],
                  squad: str = None) -> BusMessage:
        recipient = f"squad:{squad}" if squad else "*"
        return self.send(sender, recipient, payload, msg_type=MessageType.BROADCAST)

    def publish(self, sender: str, channel: str, payload: Dict[str, Any]) -> BusMessage:
        return self.send(sender, f"channel:{channel}", payload,
                         msg_type=MessageType.CHANNEL, channel=channel)

    # -------------------------------------------------------------------------
    # INBOX
    # -------------------------------------------------------------------------

    def get_inbox(self, agent_id: str, unread_only: bool = True,
                  limit: int = 50) -> List[BusMessage]:
        inbox = self._inboxes.get(agent_id, [])
        self._purge_expired(agent_id)
        if unread_only:
            inbox = [m for m in inbox if not m.acknowledged]
        return inbox[:limit]

    def acknowledge(self, agent_id: str, msg_id: str) -> bool:
        for msg in self._inboxes.get(agent_id, []):
            if msg.msg_id == msg_id:
                msg.acknowledged = True
                return True
        return False

    def ack_all(self, agent_id: str) -> int:
        count = 0
        for msg in self._inboxes.get(agent_id, []):
            if not msg.acknowledged:
                msg.acknowledged = True
                count += 1
        return count

    def inbox_count(self, agent_id: str) -> Dict[str, int]:
        inbox = self._inboxes.get(agent_id, [])
        return {
            "total": len(inbox),
            "unread": len([m for m in inbox if not m.acknowledged]),
            "expired": len([m for m in inbox if m.is_expired])
        }

    # -------------------------------------------------------------------------
    # THREADS
    # -------------------------------------------------------------------------

    def get_thread(self, thread_id: str) -> List[BusMessage]:
        msg_ids = self._threads.get(thread_id, [])
        return [m for m in self._message_log if m.msg_id in msg_ids]

    def list_threads(self, agent_id: str = None) -> Dict[str, int]:
        if agent_id:
            return {
                tid: len(mids) for tid, mids in self._threads.items()
                if any(
                    m.sender == agent_id or m.recipient == agent_id
                    for m in self._message_log if m.msg_id in mids
                )
            }
        return {tid: len(mids) for tid, mids in self._threads.items()}

    # -------------------------------------------------------------------------
    # HANDLERS (ASYNC HOOKS)
    # -------------------------------------------------------------------------

    def on_message(self, agent_id: str, handler: Callable):
        self._handlers.setdefault(agent_id, []).append(handler)

    def on_channel(self, channel: str, handler: Callable):
        self._channel_handlers.setdefault(channel, []).append(handler)

    # -------------------------------------------------------------------------
    # INTERNAL DELIVERY
    # -------------------------------------------------------------------------

    def _deliver_direct(self, msg: BusMessage, recipient: str):
        if recipient in self._inboxes:
            self._inboxes[recipient].append(msg)
            msg.delivered = True
        else:
            logger.warning(f"[BUS] Agent {recipient} not found. Message queued in dead letter.")

    def _deliver_broadcast(self, msg: BusMessage, sender: str):
        target_squad = None
        if msg.recipient.startswith("squad:"):
            target_squad = msg.recipient.split(":", 1)[1]

        for aid in self._agents:
            if aid == sender:
                continue
            if target_squad and self._agents[aid].squad != target_squad:
                continue
            clone = BusMessage(
                sender=msg.sender, recipient=aid, msg_type=msg.msg_type,
                payload=msg.payload, channel=msg.channel,
                thread_id=msg.thread_id, msg_id=f"{msg.msg_id}_{aid}",
                timestamp=msg.timestamp, ttl=msg.ttl
            )
            self._inboxes.setdefault(aid, []).append(clone)
            clone.delivered = True

    def _deliver_channel(self, msg: BusMessage, channel: str):
        subscribers = self._channels.get(channel, set())
        for aid in subscribers:
            if aid == msg.sender:
                continue
            clone = BusMessage(
                sender=msg.sender, recipient=aid, msg_type=msg.msg_type,
                payload=msg.payload, channel=channel,
                thread_id=msg.thread_id, msg_id=f"{msg.msg_id}_{aid}",
                timestamp=msg.timestamp, ttl=msg.ttl
            )
            self._inboxes.setdefault(aid, []).append(clone)
            clone.delivered = True

    def _fire_handlers(self, msg: BusMessage):
        for handler in self._handlers.get(msg.recipient, []):
            try:
                if inspect.iscoroutinefunction(handler):
                    loop = asyncio.get_event_loop()
                    if loop.is_running():
                        asyncio.ensure_future(handler(msg))
                    else:
                        loop.run_until_complete(handler(msg))
                else:
                    handler(msg)
            except Exception as e:
                logger.error(f"[BUS] Handler error for {msg.recipient}: {e}")

        if msg.channel:
            for handler in self._channel_handlers.get(msg.channel, []):
                try:
                    if inspect.iscoroutinefunction(handler):
                        loop = asyncio.get_event_loop()
                        if loop.is_running():
                            asyncio.ensure_future(handler(msg))
                        else:
                            loop.run_until_complete(handler(msg))
                    else:
                        handler(msg)
                except Exception as e:
                    logger.error(f"[BUS] Channel handler error for #{msg.channel}: {e}")

    def _emit_event(self, event_name: str, data: Dict[str, Any]):
        for handler in self._channel_handlers.get("bus.events", []):
            try:
                evt_msg = BusMessage(
                    sender="bus.system",
                    recipient="channel:bus.events",
                    msg_type=MessageType.EVENT,
                    payload={"event": event_name, **data},
                    channel="bus.events"
                )
                handler(evt_msg)
            except Exception:
                pass

    # -------------------------------------------------------------------------
    # THREAD TRACKING
    # -------------------------------------------------------------------------

    def _track_thread(self, msg: BusMessage):
        self._threads.setdefault(msg.thread_id, []).append(msg.msg_id)

    # -------------------------------------------------------------------------
    # PERSISTENCE
    # -------------------------------------------------------------------------

    def _log_message(self, msg: BusMessage):
        self._message_log.append(msg)
        if len(self._message_log) > self._max_log:
            self._message_log = self._message_log[-self._max_log:]

    def _purge_expired(self, agent_id: str):
        if agent_id in self._inboxes:
            self._inboxes[agent_id] = [m for m in self._inboxes[agent_id] if not m.is_expired]

    def flush_log(self, filename: str = None) -> str:
        fname = filename or f"bus_log_{int(time.time())}.json"
        path = os.path.join(self._log_dir, fname)
        data = [m.to_dict() for m in self._message_log]
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        logger.info(f"[BUS] Log flushed: {path} ({len(data)} messages)")
        return path

    def load_log(self, path: str) -> int:
        if not os.path.exists(path):
            return 0
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        loaded = [BusMessage.from_dict(d) for d in data]
        self._message_log.extend(loaded)
        for msg in loaded:
            self._track_thread(msg)
        return len(loaded)

    # -------------------------------------------------------------------------
    # TELEMETRY
    # -------------------------------------------------------------------------

    def stats(self) -> Dict[str, Any]:
        return {
            "agents_registered": len(self._agents),
            "agents_online": len([a for a in self._agents.values() if a.status == AgentStatus.ONLINE]),
            "channels": len(self._channels),
            "total_subscriptions": sum(len(s) for s in self._channels.values()),
            "messages_in_log": len(self._message_log),
            "active_threads": len(self._threads),
            "inboxes": {aid: self.inbox_count(aid) for aid in self._agents}
        }


# =============================================================================
# TEST RUNNER
# =============================================================================

def _run_tests():  # pragma: no cover
    print("=" * 60)
    print("  MECHA AGENT BUS — UNIT TESTS")
    print("=" * 60)

    bus = AgentBus(log_dir=os.path.join(os.path.dirname(__file__), "_test_bus_logs"))
    results = {}

    # Test 1: Agent Registration
    try:
        a1 = bus.register("warlock", "Warlock", squad="tribunal", role="Security Auditor",
                          capabilities=["security", "audit"])
        a2 = bus.register("amanda", "Amanda", squad="tribunal", role="Compliance Reviewer",
                          capabilities=["compliance", "defense"])
        a3 = bus.register("shura", "Shura 255", squad="tribunal", role="Lead Architect",
                          capabilities=["architecture", "judgment"])
        a4 = bus.register("linus", "Linus", squad="dev", role="Implementer",
                          capabilities=["coding", "systems"])
        assert len(bus.list_agents()) == 4
        assert len(bus.list_agents(squad="tribunal")) == 3
        assert len(bus.find_by_capability("security")) == 1
        results["registration"] = True
        print(" [OK] Test 1: Agent Registration")
    except Exception as e:
        results["registration"] = False
        print(f" [FAIL] Test 1: {e}")

    # Test 2: Direct Messaging
    try:
        msg = bus.send("warlock", "amanda", {"text": "Sua defesa tem furos logicos."})
        assert msg.delivered
        inbox = bus.get_inbox("amanda")
        assert len(inbox) == 1
        assert inbox[0].payload["text"] == "Sua defesa tem furos logicos."
        results["direct_msg"] = True
        print(" [OK] Test 2: Direct Messaging")
    except Exception as e:
        results["direct_msg"] = False
        print(f" [FAIL] Test 2: {e}")

    # Test 3: Request/Response
    try:
        req = bus.request("shura", "warlock", {"action": "analyze", "target": "kafka_config"})
        assert req.msg_type == MessageType.REQUEST
        resp = bus.respond(req, "warlock", {"verdict": "dangerous", "reason": "race condition"})
        assert resp.msg_type == MessageType.RESPONSE
        assert resp.reply_to == req.msg_id
        assert resp.thread_id == req.thread_id
        thread = bus.get_thread(req.thread_id)
        assert len(thread) == 2
        results["request_response"] = True
        print(" [OK] Test 3: Request/Response")
    except Exception as e:
        results["request_response"] = False
        print(f" [FAIL] Test 3: {e}")

    # Test 4: Channel Pub/Sub
    try:
        bus.subscribe("warlock", "security-alerts")
        bus.subscribe("amanda", "security-alerts")
        bus.subscribe("shura", "security-alerts")
        pub_msg = bus.publish("linus", "security-alerts", {"alert": "SQL injection found"})
        w_inbox = bus.get_inbox("warlock", unread_only=False)
        a_inbox = bus.get_inbox("amanda", unread_only=False)
        s_inbox = bus.get_inbox("shura", unread_only=False)
        sec_w = [m for m in w_inbox if m.channel == "security-alerts"]
        sec_a = [m for m in a_inbox if m.channel == "security-alerts"]
        sec_s = [m for m in s_inbox if m.channel == "security-alerts"]
        assert len(sec_w) == 1
        assert len(sec_a) == 1
        assert len(sec_s) == 1
        results["pub_sub"] = True
        print(" [OK] Test 4: Channel Pub/Sub")
    except Exception as e:
        results["pub_sub"] = False
        print(f" [FAIL] Test 4: {e}")

    # Test 5: Broadcast (squad-scoped)
    try:
        bus.broadcast("shura", {"announcement": "Tribunal session starting"}, squad="tribunal")
        w_msgs = [m for m in bus.get_inbox("warlock", unread_only=False) if m.msg_type == MessageType.BROADCAST]
        a_msgs = [m for m in bus.get_inbox("amanda", unread_only=False) if m.msg_type == MessageType.BROADCAST]
        l_msgs = [m for m in bus.get_inbox("linus", unread_only=False) if m.msg_type == MessageType.BROADCAST]
        assert len(w_msgs) >= 1
        assert len(a_msgs) >= 1
        assert len(l_msgs) == 0  # Linus is dev squad, not tribunal
        results["broadcast"] = True
        print(" [OK] Test 5: Squad-Scoped Broadcast")
    except Exception as e:
        results["broadcast"] = False
        print(f" [FAIL] Test 5: {e}")

    # Test 6: Acknowledge & Inbox Count
    try:
        inbox_before = bus.inbox_count("amanda")
        assert inbox_before["unread"] > 0
        bus.ack_all("amanda")
        inbox_after = bus.inbox_count("amanda")
        assert inbox_after["unread"] == 0
        results["ack"] = True
        print(" [OK] Test 6: Acknowledge & Inbox Count")
    except Exception as e:
        results["ack"] = False
        print(f" [FAIL] Test 6: {e}")

    # Test 7: Message Handler
    try:
        handler_received = []
        bus.on_message("linus", lambda msg: handler_received.append(msg))
        bus.send("shura", "linus", {"task": "implement calculator"})
        assert len(handler_received) == 1
        assert handler_received[0].payload["task"] == "implement calculator"
        results["handler"] = True
        print(" [OK] Test 7: Message Handler")
    except Exception as e:
        results["handler"] = False
        print(f" [FAIL] Test 7: {e}")

    # Test 8: Thread Tracking
    try:
        threads = bus.list_threads(agent_id="warlock")
        assert len(threads) > 0
        results["threads"] = True
        print(" [OK] Test 8: Thread Tracking")
    except Exception as e:
        results["threads"] = False
        print(f" [FAIL] Test 8: {e}")

    # Test 9: Log Persistence
    try:
        log_path = bus.flush_log("test_bus_log.json")
        assert os.path.exists(log_path)
        bus2 = AgentBus(log_dir=bus._log_dir)
        loaded = bus2.load_log(log_path)
        assert loaded > 0
        results["persistence"] = True
        print(" [OK] Test 9: Log Persistence")
        # Cleanup
        os.remove(log_path)
        os.rmdir(bus._log_dir)
    except Exception as e:
        results["persistence"] = False
        print(f" [FAIL] Test 9: {e}")

    # Test 10: Stats Telemetry
    try:
        s = bus.stats()
        assert s["agents_registered"] == 4
        assert s["channels"] >= 1
        assert s["messages_in_log"] > 0
        results["stats"] = True
        print(" [OK] Test 10: Stats Telemetry")
    except Exception as e:
        results["stats"] = False
        print(f" [FAIL] Test 10: {e}")

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
