# -*- coding: utf-8 -*-
"""
sendspeed_journey_handler — bridge AgentBus journey.* → pipeline sendspeed.
=============================================================================
Implementa a fase 2 event-driven do S3 (debate O6) sem engine nova:
  - Assina o canal "journey.events" no AgentBus singleton (get_instance)
  - Valida o EventEnvelope via dynamic_typing.py (Pydantic)
  - Roteia para run_squad_workflow('sendspeed_squad', ...) via CrossSquadRouter
  - Emite workflow.started / workflow.completed no canal "pipeline.events"
  - Reutiliza shura_daemon + cross_squad_router existentes (ORCH-01)
  - Sem scheduler, sem estado persistente novo

Tópicos suportados em journey.events:
  journey.trigger       → journey_batch_trigger_pipeline
  journey.otp           → journey_otp_fallback_pipeline
  journey.callback      → journey_callback_multicrm_fasttrack
  journey.rcs           → journey_rcs_encurtador
  journey.recovery      → journey_recuperacao_cadastro_userin

Uso programático (dentro do mesmo processo):
    handler = SendSpeedJourneyHandler(workspace_root)
    handler.attach()    # registra o on_channel no bus singleton
    handler.detach()    # remove (testes)

Uso como daemon one-shot (CI/teste):
    python sendspeed_journey_handler.py --once
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
import sys
import time
from typing import Any, Dict, Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agent_bus import AgentBus, BusMessage, MessageType
from squad_orchestrator import SquadOrchestrator

logger = logging.getLogger("MECHA_JourneyHandler")

# ---------------------------------------------------------------------------
# Constantes
# ---------------------------------------------------------------------------
HANDLER_AGENT_ID  = "sendspeed.journey_handler"
JOURNEY_CHANNEL   = "journey.events"
PIPELINE_CHANNEL  = "pipeline.events"
SQUAD_NAME        = "sendspeed_squad"
WORKFLOW_NAME     = "sendspeed_workflows"

# Mapa tópico → pipeline key
TOPIC_TO_PIPELINE: Dict[str, str] = {
    "journey.trigger":  "journey_batch_trigger_pipeline",
    "journey.otp":      "journey_otp_fallback_pipeline",
    "journey.callback": "journey_callback_multicrm_fasttrack",
    "journey.rcs":      "journey_rcs_encurtador",
    "journey.recovery": "journey_recuperacao_cadastro_userin",
}

# ---------------------------------------------------------------------------
# EventEnvelope — validado por dynamic_typing.py (Pydantic)
# ---------------------------------------------------------------------------
try:
    from kernel.validators.dynamic_typing import validate_event_envelope  # type: ignore
    _HAS_VALIDATOR = True
except ImportError:
    try:
        # fallback: path relativo quando chamado de dentro de ops/patterns
        _here = os.path.dirname(os.path.abspath(__file__))
        _root = os.path.normpath(os.path.join(_here, "..", ".."))
        sys.path.insert(0, os.path.join(_root, "kernel", "validators"))
        from dynamic_typing import validate_event_envelope  # type: ignore
        _HAS_VALIDATOR = True
    except ImportError:
        _HAS_VALIDATOR = False
        logger.warning("[JourneyHandler] dynamic_typing indisponível — validação de envelope desativada")


def _validate_envelope(data: Dict[str, Any]) -> tuple[bool, str]:
    """Valida o EventEnvelope. Retorna (ok, mensagem)."""
    if not _HAS_VALIDATOR:
        return True, "validator ausente (skip)"
    try:
        ok, msg = validate_event_envelope(data)
        return ok, msg
    except Exception as exc:
        return False, str(exc)


# ---------------------------------------------------------------------------
# Handler principal
# ---------------------------------------------------------------------------

class SendSpeedJourneyHandler:
    """
    Consome eventos do canal 'journey.events' e dispara pipelines sendspeed
    via SquadOrchestrator (sem CrossSquadRouter para evitar auto-chain) —
    o handoff para Shura ocorre via ORCH-01 quando necessário.
    """

    def __init__(self, workspace_root: Optional[str] = None, bus: Optional[AgentBus] = None):
        _here = os.path.dirname(os.path.abspath(__file__))
        self.workspace_root = workspace_root or os.path.normpath(
            os.path.join(_here, "..", "..", "..")
        )
        self.bus = bus or AgentBus.get_instance()
        self.orchestrator = SquadOrchestrator(self.workspace_root)
        self._attached = False
        self._processed = 0
        self._errors = 0

    # ------------------------------------------------------------------
    # Attach / detach
    # ------------------------------------------------------------------

    def attach(self) -> None:
        """Registra o handler no AgentBus singleton. Idempotente."""
        if self._attached:
            return
        if not self.bus.get_agent(HANDLER_AGENT_ID):
            self.bus.register(
                HANDLER_AGENT_ID,
                "SendSpeed Journey Handler",
                squad="sendspeed_squad",
                role="Journey Event Bridge (ORCH-09)",
                capabilities=["journey_routing", "pipeline_dispatch"],
            )
        self.bus.subscribe(HANDLER_AGENT_ID, JOURNEY_CHANNEL)
        self.bus.on_channel(JOURNEY_CHANNEL, self._on_journey_event)
        self._attached = True
        logger.info("[JourneyHandler] Attached ao canal '%s'", JOURNEY_CHANNEL)

    def detach(self) -> None:
        """Remove a assinatura (útil em testes para não acumular handlers)."""
        self.bus.unsubscribe(HANDLER_AGENT_ID, JOURNEY_CHANNEL)
        self._attached = False

    # ------------------------------------------------------------------
    # Handler de evento (síncrono — chamado pelo _fire_handlers do AgentBus)
    # ------------------------------------------------------------------

    def _on_journey_event(self, msg: BusMessage) -> None:
        """
        Processa um evento journey.* recebido no canal.
        Valida o envelope, mapeia para pipeline e dispara assincronamente.
        Nunca levanta exceção — falhas são emitidas como journey.error no bus.
        """
        try:
            payload = msg.payload or {}
            topic   = payload.get("topic") or payload.get("event") or ""
            sender  = payload.get("sender") or msg.sender or "unknown"
            ts      = payload.get("timestamp") or int(msg.timestamp)
            inner   = payload.get("payload") or payload

            # Normaliza para EventEnvelope
            envelope = {
                "topic":     topic,
                "sender":    sender,
                "timestamp": int(ts),
                "payload":   inner if isinstance(inner, dict) else {"raw": str(inner)},
            }

            ok, msg_val = _validate_envelope(envelope)
            if not ok:
                self._emit_error(topic, f"EventEnvelope inválido: {msg_val}", payload)
                return

            pipeline_key = TOPIC_TO_PIPELINE.get(topic)
            if not pipeline_key:
                self._emit_error(
                    topic,
                    f"Tópico '{topic}' não mapeado. Disponíveis: {list(TOPIC_TO_PIPELINE.keys())}",
                    payload,
                )
                return

            # Disparo assíncrono dentro do loop de eventos (se houver) ou síncrono
            user_prompt = (
                inner.get("user_prompt")
                or inner.get("prompt")
                or inner.get("description")
                or json.dumps(inner, ensure_ascii=False)[:500]
            )
            thread_id = inner.get("thread_id") or f"journey_{topic.replace('.','_')}_{int(time.time())}"

            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    asyncio.ensure_future(
                        self._dispatch(pipeline_key, user_prompt, thread_id, topic)
                    )
                else:
                    loop.run_until_complete(
                        self._dispatch(pipeline_key, user_prompt, thread_id, topic)
                    )
            except RuntimeError:
                # Sem event loop — roda em thread executor (modo daemon/CI)
                asyncio.run(self._dispatch(pipeline_key, user_prompt, thread_id, topic))

            self._processed += 1

        except Exception as exc:  # noqa: BLE001
            self._errors += 1
            logger.error("[JourneyHandler] Erro inesperado no handler: %s", exc)

    # ------------------------------------------------------------------
    # Dispatch assíncrono
    # ------------------------------------------------------------------

    async def _dispatch(
        self, pipeline_key: str, prompt: str, thread_id: str, topic: str
    ) -> Dict[str, Any]:
        """
        Carrega entry_inputs do pipeline (Let It Fail) e executa via orchestrator.
        Emite workflow.started e workflow.completed no canal pipeline.events.
        """
        # Carrega entry_inputs declarados no pipeline (S1 fix)
        workflow_data = self.orchestrator.load_workflow_config(WORKFLOW_NAME)
        pipeline = workflow_data.get(pipeline_key) or {}
        entry = pipeline.get("entry_inputs") or {"user_prompt": prompt}
        initial_inputs = {
            k: (prompt if v == "__prompt__" else v) for k, v in entry.items()
        }
        if not any(v == prompt for v in initial_inputs.values()):
            initial_inputs["user_prompt"] = prompt

        # workflow.started
        self.bus.publish(HANDLER_AGENT_ID, PIPELINE_CHANNEL, {
            "event":    "workflow.started",
            "squad":    SQUAD_NAME,
            "pipeline": pipeline_key,
            "topic":    topic,
            "thread_id": thread_id,
        })
        logger.info("[JourneyHandler] workflow.started — %s / %s", SQUAD_NAME, pipeline_key)

        try:
            results = await self.orchestrator.run_workflow(
                squad_name=SQUAD_NAME,
                workflow_name=WORKFLOW_NAME,
                pipeline_key=pipeline_key,
                initial_inputs=initial_inputs,
            )
            mock_flag = results.get("mock", False)

            # workflow.completed
            self.bus.publish(HANDLER_AGENT_ID, PIPELINE_CHANNEL, {
                "event":       "workflow.completed",
                "squad":       SQUAD_NAME,
                "pipeline":    pipeline_key,
                "topic":       topic,
                "thread_id":   thread_id,
                "output_vars": [k for k in results if not k.startswith("_")],
                "mock":        mock_flag,
            })
            logger.info("[JourneyHandler] workflow.completed — %s / %s (mock=%s)",
                        SQUAD_NAME, pipeline_key, mock_flag)
            return results

        except Exception as exc:  # noqa: BLE001
            self._emit_error(topic, f"Erro no workflow '{pipeline_key}': {exc}", {})
            raise

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _emit_error(self, topic: str, reason: str, original: Dict[str, Any]) -> None:
        self._errors += 1
        logger.warning("[JourneyHandler] journey.error — %s: %s", topic, reason)
        try:
            self.bus.publish(HANDLER_AGENT_ID, JOURNEY_CHANNEL, {
                "topic":    "journey.error",
                "sender":   HANDLER_AGENT_ID,
                "timestamp": int(time.time()),
                "payload":  {
                    "original_topic": topic,
                    "reason":         reason,
                    "original":       original,
                },
            })
        except Exception:
            pass

    def stats(self) -> Dict[str, Any]:
        return {
            "attached":  self._attached,
            "processed": self._processed,
            "errors":    self._errors,
            "topics":    list(TOPIC_TO_PIPELINE.keys()),
        }


# ---------------------------------------------------------------------------
# CLI one-shot (CI/debug)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser(description="SendSpeed Journey Handler — bridge AgentBus → pipeline")
    ap.add_argument("--once",  action="store_true", help="drena inbox e sai (modo CI)")
    ap.add_argument("--smoke", action="store_true", help="publica evento de teste e sai")
    args = ap.parse_args()

    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s %(name)s %(levelname)s %(message)s")

    _here = os.path.dirname(os.path.abspath(__file__))
    workspace = os.path.normpath(os.path.join(_here, "..", "..", ".."))
    os.environ.setdefault("MECHA_FORCE_MOCK_LLM", "1")

    bus = AgentBus.get_instance()
    h   = SendSpeedJourneyHandler(workspace_root=workspace, bus=bus)
    h.attach()

    if args.smoke:
        bus.publish("test.agent", JOURNEY_CHANNEL, {
            "topic":     "journey.otp",
            "sender":    "test.agent",
            "timestamp": int(time.time()),
            "payload":   {"user_prompt": "smoke test OTP fallback", "thread_id": "smoke_001"},
        })
        time.sleep(2)
        print("Stats:", h.stats())
    elif args.once:
        time.sleep(1)
        print("Stats:", h.stats())
    else:
        print("Handler attached. Ctrl+C para sair.")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            pass
