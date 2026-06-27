# ==============================================================================
# 📡 MECHA TELEGRAM RELAY - BUS → TELEGRAM REAL-TIME BRIDGE
# ==============================================================================
# Observes AgentBus channels and relays inter-agent communication to Telegram.
# Hugo can watch agents talking from his phone.
# ==============================================================================

import os
import sys
import json
import time
import urllib.request
import logging
from typing import Dict, Any, List, Optional

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger("MECHA_TelegramRelay")

from agent_bus import AgentBus, BusMessage, MessageType


# =============================================================================
# ENV LOADER
# =============================================================================

def _load_env():
    env_path = os.path.join(
        os.path.dirname(__file__), os.pardir, ".env"
    )
    env_path = os.path.normpath(env_path)
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if "=" in line and not line.startswith("#"):
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip())


_load_env()

TELEGRAM_TOKEN = os.environ.get(
    "MECHAHUGGIES_BOT_TOKEN",
    os.environ.get("TELEGRAM_BOT_TOKEN", "")
)
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "223442734")


# =============================================================================
# AGENT EMOJI MAP
# =============================================================================

AGENT_EMOJIS = {
    "warlock": "⚔️",       # ⚔️
    "amanda": "\U0001f6e1️",    # 🛡️
    "shura": "⚖️",         # ⚖️
    "uncle_bob": "\U0001f4d0",       # 📐
    "linus": "\U0001f4bb",           # 💻
    "kent_beck": "\U0001f9ea",       # 🧪
    "mitnick": "\U0001f50d",         # 🔍
    "claw": "\U0001f5b1️",      # 🖱️
    "router": "\U0001f500",          # 🔀
    "hermes": "\U0001f6e1️",    # 🛡️
}

SQUAD_EMOJIS = {
    "dev_squad": "\U0001f468‍\U0001f4bb",      # 👨‍💻
    "tribunal_squad": "⚖️",                # ⚖️
    "qa_squad": "\U0001f9ea",                        # 🧪
    "devops_squad": "\U0001f680",                    # 🚀
    "system": "⚙️",                        # ⚙️
}


def _get_agent_emoji(agent_id: str) -> str:
    if not agent_id:
        return "\U0001f916"
    for key, emoji in AGENT_EMOJIS.items():
        if key in agent_id.lower():
            return emoji
    return "\U0001f916"  # 🤖


def _get_squad_emoji(squad: str) -> str:
    return SQUAD_EMOJIS.get(squad or "", "\U0001f4e6")  # 📦


# =============================================================================
# TELEGRAM SENDER
# =============================================================================

def _send_telegram(text: str, parse_mode: str = None) -> Optional[int]:
    if not TELEGRAM_TOKEN:
        logger.warning("[RELAY] No Telegram token configured")
        return None

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    body = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text
    }
    if parse_mode:
        body["parse_mode"] = parse_mode

    try:
        data = json.dumps(body).encode("utf-8")
        req = urllib.request.Request(
            url, data=data,
            headers={"Content-Type": "application/json"}
        )
        resp = urllib.request.urlopen(req, timeout=10)
        result = json.loads(resp.read())
        if result.get("ok"):
            return result["result"]["message_id"]
        logger.error(f"[RELAY] Telegram error: {result}")
    except Exception as e:
        logger.error(f"[RELAY] Send failed: {e}")
    return None


# =============================================================================
# MESSAGE FORMATTERS
# =============================================================================

def _format_agent_message(msg: BusMessage) -> str:
    emoji = _get_agent_emoji(msg.sender)
    recipient = msg.recipient or "broadcast"

    payload_str = ""
    if isinstance(msg.payload, dict):
        content = msg.payload.get("content", msg.payload.get("action", ""))
        if content:
            payload_str = str(content)[:500]
        else:
            payload_str = json.dumps(msg.payload, ensure_ascii=False)[:500]
    else:
        payload_str = str(msg.payload)[:500]

    return (
        f"{emoji} {msg.sender} → {recipient}\n"
        f"{payload_str}"
    )


def _format_pipeline_event(msg: BusMessage) -> str:
    payload = msg.payload if isinstance(msg.payload, dict) else {}
    event = payload.get("event", "unknown")
    squad = payload.get("squad", "?")
    squad_emoji = _get_squad_emoji(squad)

    if event == "workflow.started":
        pipeline = payload.get("pipeline", "?")
        return f"{squad_emoji} Pipeline iniciado: {squad}/{pipeline}"

    if event == "workflow.completed":
        pipeline = payload.get("pipeline", "?")
        outputs = payload.get("output_vars", [])
        return (
            f"{squad_emoji} Pipeline concluido: {squad}/{pipeline}\n"
            f"Outputs: {', '.join(outputs)}"
        )

    if event == "step.completed":
        agent = payload.get("agent", "?")
        preview = payload.get("content_preview", "")[:500]
        emoji = _get_agent_emoji(agent)
        return f"{emoji} {agent} concluiu:\n{preview}"

    if event == "chain.triggered":
        source = payload.get("source_squad", "?")
        target = payload.get("target_squad", "?")
        return (
            f"\U0001f500 Auto-chain: {source} → {target}\n"
            f"Rota: {payload.get('route', '?')}"
        )

    if event == "claw.consultation_requested":
        action = payload.get("action", "?")
        return f"\U0001f5b1️ Claw pede consulta: '{action}'"

    if event == "claw.verdict_received":
        action = payload.get("action", "?")
        approved = payload.get("approved", False)
        icon = "✅" if approved else "❌"
        return f"{icon} Veredito Claw '{action}': {'APROVADO' if approved else 'BLOQUEADO'}"

    return f"⚙️ Event: {event} ({squad})"


def _format_audit_event(msg: BusMessage) -> str:
    payload = msg.payload if isinstance(msg.payload, dict) else {}
    event = payload.get("event", "unknown")

    if event == "audit.findings":
        findings = payload.get("findings", [])
        sender = payload.get("sender", "?")
        lines = [f"\U0001f6a8 Hermes flagou {len(findings)} achado(s) de '{sender}':"]
        for f in findings[:5]:
            icon = "❌" if f.get("severity") == "violation" else "⚠️"
            lines.append(f"  {icon} {f.get('rule_id')}: {f.get('detail', '')[:100]}")
        return "\n".join(lines)

    return f"\U0001f6e1️ Audit: {event}"


# =============================================================================
# TELEGRAM RELAY
# =============================================================================

class TelegramRelay:
    """
    Subscribes to AgentBus channels and relays messages to Telegram.

    Channels observed:
    - pipeline.events → workflow start/complete/step events
    - squad.* → step completions per squad
    - audit.events → Hermes violations
    - claw.commands → Claw actions
    - claw.verdicts → Claw verdicts
    """

    def __init__(self, bus: AgentBus = None,
                 channels: List[str] = None,
                 relay_direct: bool = False,
                 throttle_seconds: float = 1.0):
        self.bus = bus or AgentBus.get_instance()
        self.channels = channels or [
            "pipeline.events",
            "audit.events",
            "claw.commands",
            "claw.verdicts",
            "squad.dev_squad",
            "squad.tribunal_squad",
            "squad.qa_squad",
            "squad.devops_squad",
        ]
        self.relay_direct = relay_direct
        self.throttle = throttle_seconds
        self._last_send = 0
        self._active = False
        self._message_count = 0

    def start(self):
        if not self.bus.get_agent("telegram_relay"):
            self.bus.register(
                "telegram_relay", "Telegram Relay",
                squad="system", role="Observer",
                capabilities=["telegram", "relay"]
            )

        for channel in self.channels:
            self.bus.subscribe("telegram_relay", channel)
            self.bus.on_channel(channel, self._on_channel_message)

        if self.relay_direct:
            self.bus.on_message("telegram_relay", self._on_direct_message)

        self._active = True
        logger.info(f"[RELAY] Started — observing {len(self.channels)} channels")

        _send_telegram(
            "\U0001f4e1 MECHA Relay ativo\n"
            f"Canais: {', '.join(self.channels)}\n"
            f"Chat: {TELEGRAM_CHAT_ID}"
        )

    def stop(self):
        self._active = False
        _send_telegram(
            f"\U0001f6d1 MECHA Relay desligado\n"
            f"Mensagens retransmitidas: {self._message_count}"
        )
        logger.info(f"[RELAY] Stopped ({self._message_count} messages relayed)")

    def _on_channel_message(self, msg: BusMessage):
        if not self._active or msg.sender == "telegram_relay":
            return
        self._throttle_and_send(msg, is_channel=True)

    def _on_direct_message(self, msg: BusMessage):
        if not self._active or msg.sender == "telegram_relay":
            return
        self._throttle_and_send(msg, is_channel=False)

    def _throttle_and_send(self, msg: BusMessage, is_channel: bool):
        now = time.time()
        if now - self._last_send < self.throttle:
            time.sleep(self.throttle - (now - self._last_send))

        if is_channel:
            channel = msg.channel or ""
            if "pipeline" in channel:
                text = _format_pipeline_event(msg)
            elif "audit" in channel:
                text = _format_audit_event(msg)
            elif "claw" in channel:
                text = _format_pipeline_event(msg)
            elif "squad." in channel:
                text = _format_pipeline_event(msg)
            else:
                text = _format_agent_message(msg)
        else:
            text = _format_agent_message(msg)

        mid = _send_telegram(text)
        if mid:
            self._message_count += 1
            self._last_send = time.time()

    # -------------------------------------------------------------------------
    # MANUAL SEND (for scripts/tests)
    # -------------------------------------------------------------------------

    @staticmethod
    def send(text: str) -> Optional[int]:
        return _send_telegram(text)

    def stats(self) -> Dict[str, Any]:
        return {
            "active": self._active,
            "channels": self.channels,
            "messages_relayed": self._message_count,
            "relay_direct": self.relay_direct,
            "chat_id": TELEGRAM_CHAT_ID
        }


# =============================================================================
# INTEGRATED TEST — runs real pipeline + sends to telegram
# =============================================================================

def _run_live_test():  # pragma: no cover
    import asyncio
    from cross_squad_router import CrossSquadRouter
    from hermes_auditor import HermesAuditor

    print("=" * 60)
    print("  MECHA TELEGRAM RELAY — LIVE TEST")
    print("=" * 60)

    AgentBus.reset()
    bus = AgentBus.get_instance()

    # Setup stack
    relay = TelegramRelay(bus=bus, throttle_seconds=1.5)
    relay.start()

    auditor = HermesAuditor(bus=bus)
    auditor.start()

    router = CrossSquadRouter(
        r"c:\Users\huggs\OneDrive\Documentos\workspace", bus
    )

    print("\n[*] Running tribunal pipeline with Telegram relay...\n")

    async def run():
        results = await router.run_squad_workflow(
            "tribunal_squad", "tribunal_workflows", "tribunal_pipeline",
            {"user_prompt": "Claw quer executar 'npm install unknown-pkg'. Aprovar?"},
            thread_id="relay_test_live",
            auto_chain=False
        )
        return results

    results = asyncio.run(run())

    # Send summary
    verdict = str(results.get("verdict", ""))[:200]
    relay.send(
        f"\U0001f3c1 Pipeline concluido\n"
        f"Veredito: {verdict}\n"
        f"Msgs retransmitidas: {relay._message_count}"
    )

    relay.stop()

    print(f"\n[*] Done — {relay._message_count} messages sent to Telegram")
    print("=" * 60)


if __name__ == "__main__":  # pragma: no cover
    _run_live_test()
