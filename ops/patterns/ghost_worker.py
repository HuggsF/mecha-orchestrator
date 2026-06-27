import os
import sys
import json
import time
import logging

# Enforce UTF-8 encoding output for Windows terminals (Bug CP1252 bypass)
sys.stdout.reconfigure(encoding='utf-8')

# Setup logger
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger("MECHA_GhostWorker")

# Setup paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATUS_FILE = os.path.join(BASE_DIR, "logs", "claw_status.json")

class GhostWorker:
    """
    Executes automated operations post-veredito of the Hermes Tribunal.
    Dispatches simulated Outreach [1] or silently purges lead [0] from operational DNA.
    """
    def __init__(self, workspace_root: str = None):
        self.workspace_root = workspace_root or os.path.dirname(BASE_DIR)
        
    def log_event_to_dashboard(self, level: str, msg: str) -> None:
        """Logs telemetry event to claw_status.json for dashboard visibility."""
        if os.path.exists(STATUS_FILE):
            try:
                with open(STATUS_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception:
                data = {}
        else:
            data = {}

        events = data.get("events", [])
        if not isinstance(events, list):
            events = []

        new_event = {
            "time": time.strftime("%H:%M:%S"),
            "level": level,  # info, ok, warn, danger, vision
            "msg": msg,
            "id": f"ghost_{time.time()}_{hash(msg)}"
        }
        events.append(new_event)
        data["events"] = events[-30:]  # Keep last 30 events

        try:
            os.makedirs(os.path.dirname(STATUS_FILE), exist_ok=True)
            with open(STATUS_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Erro ao logar no dashboard do Ghost Worker: {e}")

    def process_audit(self, lead_name: str, veredito: str) -> str:
        """
        Processes the audit result.
        - [1] Approved: Triggers Outreach action (logs 'ok', 'Outreach disparado para lead: [Lead]')
        - [0] Aborted: Performs Silent Purge (logs 'danger', 'Lead purgado da memória.')
        """
        logger.info(f"Processando veredito do Tribunal para lead: '{lead_name}'...")
        
        # Check if the verdict contains [1] (Approved) or [0] (Rejected)
        if "[1]" in veredito:
            msg = f"Outreach disparado para lead: {lead_name}"
            self.log_event_to_dashboard("ok", msg)
            logger.info(f"[Outreach Action] Aprovado: {msg}")
            return f"✅ **Outreach disparado para lead:** `{lead_name}` (Ações iniciadas via Ghost Worker)"
        elif "[0]" in veredito:
            msg = f"Lead purgado da memória: {lead_name}"
            self.log_event_to_dashboard("danger", msg)
            logger.info(f"[Purge Action] Abortado: {msg}")
            return f"💀 **Lead purgado da memória:** `{lead_name}` (Expurgado dos engrams operacionais)"
        else:
            # Fallback if verdict is ambiguous
            msg = f"Veredito inconclusivo para lead '{lead_name}'. Mantendo em quarentena."
            self.log_event_to_dashboard("warn", msg)
            logger.warning(f"[Quarantine Action] Inconclusivo: {msg}")
            return f"⚠️ **Veredito inconclusivo para lead:** `{lead_name}`. Nenhuma ação executada."

if __name__ == "__main__":
    # Test runner
    worker = GhostWorker()
    print("[*] Executando teste do Ghost Worker...")
    
    res_ok = worker.process_audit("Test Lead Alpha", "O veredito final é aprovação. [1]")
    print(f"Resultado Aprovado: {res_ok}")
    
    res_fail = worker.process_audit("Test Lead Beta", "O veredito final é rejeição. [0]")
    print(f"Resultado Rejeitado: {res_fail}")
