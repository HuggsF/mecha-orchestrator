import os
import sys
import time
import argparse
import requests
import json
from typing import Optional

# Importacao dos modulos locais
try:
    import claw_vision
    import claw_graph
    import claw_control
    import claw_brain
    import claw_ocr
except ImportError:
    # Se rodar a partir do diretorio pai, ajusta o path
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    import claw_vision
    import claw_graph
    import claw_control
    import claw_brain
    import claw_ocr

# Integração opcional com o FreeScout (Fase B/C) — incidentes do MECHA viram chamados.
try:
    import claw_freescout as fsc
except Exception:
    fsc = None

from pydantic import BaseModel, Field

class LoopConfig(BaseModel):
    max_steps: int = Field(default=15, description="Maximum number of action loop iterations")
    step_delay_sec: float = Field(default=2.0, description="Delay between steps in seconds")
    target_window_title: str = Field(..., description="Partial title of the window to target")
    goal: Optional[str] = Field(default=None, description="Natural language goal to guide the AI")


if getattr(sys, 'frozen', False):
    # Executável compilado (dados mutáveis na pasta do executável, recursos na temporária)
    BASE_DIR = os.path.dirname(sys.executable)
    STATIC_DIR = getattr(sys, '_MEIPASS', BASE_DIR)
else:
    # Script normal
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    STATIC_DIR = BASE_DIR


# ──────────────────────────────────────────────────────────────────────
# FASE 7 — Telemetria reativa para o dashboard (mecha.html)
# Estes globais são serializados em claw_status.json a cada update_claw_status().
# ──────────────────────────────────────────────────────────────────────
CLAW_EVENTS = []                                            # [{time, level, msg, id}]
CLAW_VISION = {"active": False, "using_image": False, "last_action": None}
CLAW_FIREWALL = {"armed": True, "block": None}             # block: {action, risk, reason, id}
CLAW_RECOVERY = {"misses": 0, "last": None}
CLAW_INCIDENT = {"number": None, "url": None, "kind": None}   # Fase C: último chamado FreeScout aberto pelo MECHA


def _clock() -> str:
    return time.strftime("%H:%M:%S")


def log_event(level: str, msg: str, max_keep: int = 60) -> None:
    """Adiciona um evento ao buffer lido pelo dashboard. Níveis: info/ok/warn/danger/vision."""
    CLAW_EVENTS.append({
        "time": _clock(),
        "level": level,
        "msg": msg,
        "id": f"{time.time():.3f}-{len(CLAW_EVENTS)}"
    })
    if len(CLAW_EVENTS) > max_keep:
        del CLAW_EVENTS[:-max_keep]
    print(f"  [Event/{level}] {msg}")


def report_incident(kind: str, title: str, detail_html: str, callback=None):
    """Fase B/C: abre (ou comenta) um chamado no FreeScout para um incidente do MECHA. Best-effort."""
    if not (fsc and fsc.enabled()):
        if callback:
            try:
                callback(None)
            except Exception as cb_err:
                print(f"  [FreeScout] Erro no callback de fallback: {cb_err}")
        return None

    def on_complete(inc):
        if inc and inc.get("number"):
            CLAW_INCIDENT.update({"number": inc.get("number"), "url": inc.get("url"), "kind": kind})
            log_event("info", f"Incidente no FreeScout: #{inc.get('number')} ({kind}).")
        if callback:
            try:
                callback(inc)
            except Exception as cb_err:
                print(f"  [FreeScout] Erro no callback de report_incident: {cb_err}")

    try:
        fsc.open_or_update_incident(kind, title, detail_html, callback=on_complete, sync=False)
    except Exception as e:
        print(f"  [FreeScout] Falha ao reportar incidente: {e}")
        if callback:
            try:
                callback(None)
            except Exception as cb_err:
                pass
        return None
    return None


def load_telegram_config():
    env_path = os.path.join(BASE_DIR, ".env")
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    if not (token and chat_id) and os.path.exists(env_path):
        try:
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        parts = line.split("=", 1)
                        if len(parts) == 2:
                            key = parts[0].strip()
                            val = parts[1].strip().strip('"').strip("'")
                            if key == "TELEGRAM_BOT_TOKEN":
                                token = val
                            elif key == "TELEGRAM_CHAT_ID":
                                chat_id = val
        except Exception as e:
            print(f"  [Telegram] Falha ao ler arquivo .env: {e}")
    return token, chat_id


def send_telegram_notification(message: str, image_path: Optional[str] = None) -> None:
    token, chat_id = load_telegram_config()
    if not token or not chat_id:
        return
    try:
        if image_path and os.path.exists(image_path):
            url = f"https://api.telegram.org/bot{token}/sendPhoto"
            with open(image_path, "rb") as photo:
                r = requests.post(url, data={"chat_id": chat_id, "caption": message, "parse_mode": "Markdown"}, files={"photo": photo}, timeout=8)
        else:
            url = f"https://api.telegram.org/bot{token}/sendMessage"
            r = requests.post(url, json={"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}, timeout=8)
        r.raise_for_status()
    except Exception as e:
        print(f"  [Telegram] Erro ao enviar notificação: {e}")


def update_claw_status(loop_state: str, step: int, max_steps: int, last_seen_title: str, current_goal: Optional[str], last_thumbnail: Optional[str]) -> None:
    status_file = os.path.join(BASE_DIR, "logs", "claw_status.json")
    os.makedirs(os.path.dirname(status_file), exist_ok=True)
    data = {
        "loop_state": loop_state,
        "step": step,
        "max_steps": max_steps,
        "last_seen_title": last_seen_title,
        "current_goal": current_goal,
        "last_thumbnail": last_thumbnail,
        "timestamp": time.time(),
        # ── Fase 7: telemetria consumida pelos chips do dashboard ──
        "vision": CLAW_VISION,
        "firewall": CLAW_FIREWALL,
        "recovery": CLAW_RECOVERY,
        "incident": CLAW_INCIDENT,
        "events": CLAW_EVENTS[-30:],
    }
    try:
        with open(status_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"  [Status] Erro ao gravar status do claw: {e}")
def publish_to_bus(topic: str, payload: dict) -> None:
    try:
        url = "http://localhost:8585/api/bus/publish"
        event = {
            "topic": topic,
            "sender": "ClawActionLoop",
            "timestamp": int(time.time() * 1000),
            "payload": payload
        }
        requests.post(url, json=event, timeout=1.5)
    except Exception as e:
        print(f"  [Bus] Falha ao publicar: {e}")



def focus_window_by_title(target_title: str) -> bool:
    """
    Busca todas as janelas abertas no sistema e traz a primeira que coincidir
    com o título parcial para o primeiro plano.
    """
    import ctypes
    
    # EnumWindowsProc callback
    EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)
    
    found_hwnd = []
    
    def foreach_window(hwnd, lParam):
        if ctypes.windll.user32.IsWindowVisible(hwnd):
            length = ctypes.windll.user32.GetWindowTextLengthW(hwnd)
            if length > 0:
                buffer = ctypes.create_unicode_buffer(length + 1)
                ctypes.windll.user32.GetWindowTextW(hwnd, buffer, length + 1)
                title = buffer.value
                if target_title.lower() in title.lower():
                    found_hwnd.append((hwnd, title))
                    return False # Para a enumeração
        return True
        
    ctypes.windll.user32.EnumWindows(EnumWindowsProc(foreach_window), 0)
    
    if found_hwnd:
        hwnd, title = found_hwnd[0]
        # Mostra a janela se estiver minimizada
        # SW_RESTORE = 9
        ctypes.windll.user32.ShowWindow(hwnd, 9)
        # Traz para o primeiro plano
        ctypes.windll.user32.SetForegroundWindow(hwnd)
        print(f"  [AutoRecovery] Foco restaurado para a janela: '{title}' (HWND: {hwnd})")
        return True
        
    return False


def launch_target_app(target_title: str) -> bool:
    """
    Tenta relançar o aplicativo correspondente à janela alvo.
    """
    import subprocess
    import os
    
    print(f"  [AutoRecovery] Iniciando tentativa de relançamento para '{target_title}'...")
    
    # Caminho específico de recuperação se for o Obsidian
    if "obsidian" in target_title.lower():
        paths_to_check = [
            os.environ.get("CLAW_TARGET_APP_PATH"),
            os.path.expandvars(r"%LOCALAPPDATA%\Obsidian\Obsidian.exe"),
            os.path.expandvars(r"%USERPROFILE%\AppData\Local\Obsidian\Obsidian.exe"),
            os.path.expandvars(r"%PROGRAMFILES%\Obsidian\Obsidian.exe")
        ]
        
        for path in paths_to_check:
            if path and os.path.exists(path):
                print(f"  [AutoRecovery] Executando executável encontrado em: {path}")
                subprocess.Popen([path], shell=True)
                return True
                
        # Fallback se não encontrar o caminho explícito do Obsidian, tenta pelo shell
        print("  [AutoRecovery] Executável não localizado nos caminhos padrão. Tentando inicialização via URI protocol...")
        try:
            os.system("start obsidian://")
            return True
        except Exception as e:
            print(f"  [AutoRecovery] Erro ao tentar inicialização genérica: {e}")
            
    # Se for outra aplicação ou fallback genérico
    # Se o operador forneceu o caminho explícito na variável de ambiente, executa-o
    env_path = os.environ.get("CLAW_TARGET_APP_PATH")
    if env_path and os.path.exists(env_path):
        print(f"  [AutoRecovery] Executando caminho configurável: {env_path}")
        subprocess.Popen([env_path], shell=True)
        return True
        
    # Se tudo falhar, tenta iniciar via linha de comando padrão pelo shell
    try:
        # Se for o Obsidian ou outro app conhecido que possa ser aberto pelo nome
        app_name = "obsidian" if "obsidian" in target_title.lower() else target_title.split()[0]
        print(f"  [AutoRecovery] Executando comando de inicialização shell: start {app_name}")
        subprocess.Popen(f"start {app_name}", shell=True)
        return True
    except Exception as e:
        print(f"  [AutoRecovery] Erro na última tentativa de relançamento: {e}")
        
    return False


class ClawActionLoop:
    def __init__(self, config: LoopConfig):
        self.config = config
        self.map_manager = claw_graph.MetroidvaniaMap()
        self.window_miss_count = 0   # Fase 7: ciclos consecutivos com a janela alvo ausente
        
    def _execute_preempt_action(self, action: str, params: dict, step: int, last_seen_title: str, temp_thumb: Optional[str]) -> Optional[bool]:
        """
        Executa uma ação individual de preempção.
        Retorna False se o loop deve parar (stop), True se resume, None senão.
        """
        if action == "stop":
            print("  [Preempt] Comando /stop recebido. Abortando loop...")
            send_telegram_notification("🛑 *Loop Abortado* via comando remoto do Telegram.")
            return False

        elif action == "set_goal":
            new_goal = params.get("goal")
            if new_goal:
                self.config.goal = new_goal
                print(f"  [Preempt] Meta atualizada via Telegram para: {new_goal}")
                send_telegram_notification(f"🎯 *Meta Atualizada* via Telegram para:\n`{new_goal}`")
            return None

        elif action == "firewall_allow":
            CLAW_FIREWALL["block"] = None
            try:
                claw_control.LAST_BLOCK = None
            except Exception:
                pass
            log_event("ok", "Operador LIBEROU a ação bloqueada pelo firewall.")
            send_telegram_notification("✅ *Firewall*: ação liberada pelo operador.")
            publish_to_bus("claw.firewall", {"action_id": "firewall_action", "status": "allowed"})
            return None

        elif action == "firewall_block_confirm":
            CLAW_FIREWALL["block"] = None
            try:
                claw_control.LAST_BLOCK = None
            except Exception:
                pass
            log_event("danger", "Operador MANTEVE o bloqueio do firewall.")
            send_telegram_notification("🛡️ *Firewall*: bloqueio mantido pelo operador.")
            publish_to_bus("claw.firewall", {"action_id": "firewall_action", "status": "confirmed"})
            return None

        elif action == "click":
            x = params.get("x", 0)
            y = params.get("y", 0)
            print(f"  [Preempt] Executando clique manual remoto em ({x}, {y})")
            try:
                state_data = claw_vision.scan_active_window()
                bounds = state_data["bounds"]
                abs_x = bounds[0] + x
                abs_y = bounds[1] + y
                claw_control.simulate_click(abs_x, abs_y)
                send_telegram_notification(f"🖱️ *Clique Executado* remotamente em ({abs_x}, {abs_y}).")
            except Exception as click_err:
                send_telegram_notification(f"⚠️ *Falha ao executar clique remoto*: {click_err}")
            return None

        elif action == "type":
            text = params.get("text", "")
            print(f"  [Preempt] Executando digitação remota: '{text}'")
            try:
                claw_control.simulate_typing(text)
                send_telegram_notification(f"⌨️ *Digitação Executada* remotamente:\n`{text}`")
            except Exception as type_err:
                send_telegram_notification(f"⚠️ *Falha ao executar digitação remota*: {type_err}")
            return None

        elif action == "resume":
            return True

        return None

    def process_preemption(self, step: int, last_seen_title: str, temp_thumb: Optional[str]) -> bool:
        """
        Lê claw_preempt.json, executa comandos do operador remoto se pendentes e gerencia a pausa.
        Retorna False se o loop deve ser abortado (stop).
        """
        preempt_file = os.path.join(BASE_DIR, "logs", "claw_preempt.json")
        if not os.path.exists(preempt_file):
            return True

        try:
            with open(preempt_file, "r", encoding="utf-8") as f:
                cmd_data = json.load(f)
        except Exception as e:
            print(f"  [Preempt] Erro ao ler comandos de preempção: {e}")
            return True

        if cmd_data.get("processed", True):
            return True

        action = cmd_data.get("action")
        params = cmd_data.get("params", {})
        print(f"  [Preempt] Comando remoto recebido: {action} com {params}")

        # Marca como processado antes de executar para evitar loops em caso de falha
        cmd_data["processed"] = True
        try:
            with open(preempt_file, "w", encoding="utf-8") as f:
                json.dump(cmd_data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            # Let it fail: raise an exception early to prevent an infinite action loop
            raise RuntimeError(f"Falha crítica ao gravar status de preempção: {e}. Abortando para evitar execuções repetidas.") from e

        # Executa ações
        res = self._execute_preempt_action(action, params, step, last_seen_title, temp_thumb)
        if res is False:
            return False

        if action == "pause":
            print("  [Preempt] Entrando em modo PAUSA...")
            send_telegram_notification("⏸️ *MECHA Claw Pausado!* Aguardando comando `/resume` para continuar ou `/stop` para abortar.")
            update_claw_status("paused", step, self.config.max_steps, last_seen_title, self.config.goal, temp_thumb)
            
            # Loop de espera da pausa
            while True:
                # Checa botão de pânico local do host durante a pausa
                if claw_control.check_panic_button():
                    print("  [Preempt] Panic Button acionado durante a pausa.")
                    send_telegram_notification("⚠️ *PANIC BUTTON TRIGGERED!* Movimento físico do mouse abortou o loop pausado.")
                    return False

                time.sleep(1.0)
                
                # Lê preempt.json novamente para ver se veio resume ou stop ou outra ação
                try:
                    with open(preempt_file, "r", encoding="utf-8") as f:
                        paused_cmd = json.load(f)
                except Exception:
                    continue

                if not paused_cmd.get("processed", True):
                    p_action = paused_cmd.get("action")
                    p_params = paused_cmd.get("params", {})
                    
                    # Marca como processado
                    paused_cmd["processed"] = True
                    try:
                        with open(preempt_file, "w", encoding="utf-8") as f:
                            json.dump(paused_cmd, f, indent=4, ensure_ascii=False)
                    except Exception as e:
                        raise RuntimeError(f"Falha crítica ao gravar status de preempção em pausa: {e}. Abortando.") from e

                    res_p = self._execute_preempt_action(p_action, p_params, step, last_seen_title, temp_thumb)
                    if res_p is False:
                        return False
                    elif res_p is True: # resume
                        print("  [Preempt] Retomando execução...")
                        send_telegram_notification("▶️ *MECHA Claw Retomado!* Continuando execução do loop.")
                        update_claw_status("running", step, self.config.max_steps, last_seen_title, self.config.goal, temp_thumb)
                        break
                    else:
                        update_claw_status("paused", step, self.config.max_steps, last_seen_title, self.config.goal, temp_thumb)

        return True

    def start_loop(self) -> None:
        print("==========================================================")
        print("           MECHA CLAW ACTION LOOP (See-Think-Act)         ")
        print("==========================================================")
        print(f" [*] Janela Alvo: '{self.config.target_window_title}'")
        print(f" [*] Maximo de Etapas: {self.config.max_steps}")
        print(f" [*] Delay do Passo: {self.config.step_delay_sec} segundos")
        print(" [*] Mova o mouse bruscamente para acionar o PANIC BUTTON.")
        print("==========================================================")
        
        # Envia notificação de início
        send_telegram_notification(
            f"🚀 *MECHA Claw Loop Iniciado!*\n"
            f"🎯 *Meta*: `{self.config.goal}`\n"
            f"🖥️ *Janela Alvo*: `{self.config.target_window_title}`\n"
            f"⏱️ *Max Etapas*: {self.config.max_steps} | *Passo*: {self.config.step_delay_sec}s"
        )
        log_event("info", f"Loop iniciado — alvo '{self.config.target_window_title}', meta '{self.config.goal}'.")
        
        try:
            # Inicializa a posicao inicial esperada do mouse
            start_x, start_y = claw_control.get_cursor_position()
            claw_control.set_expected_position(start_x, start_y)
            
            last_state_id = None
            last_action_desc = None
            last_click_coord = None
            temp_thumb = None
            last_seen_title = "N/A"
            
            step = 0
            while step < self.config.max_steps:
                step += 1
                print(f"\n[*] Ciclo {step} de {self.config.max_steps}...")
                
                # Grava status inicial do ciclo
                update_claw_status("running", step, self.config.max_steps, last_seen_title, self.config.goal, temp_thumb)
                
                # 1. PROCESSAR PREEMPÇÃO REMOTA DO TELEGRAM
                if not self.process_preemption(step, last_seen_title, temp_thumb):
                    update_claw_status("stopped", step, self.config.max_steps, last_seen_title, self.config.goal, temp_thumb)
                    return
                
                # 2. CHECK PANIC BUTTON (Seguranca em primeiro lugar)
                if claw_control.check_panic_button():
                    print("\n==========================================================")
                    print(" [!] PANIC BUTTON TRIGGERED: Mouse movido manualmente!")
                    print(" [!] Controle da maquina devolvido ao operador humano.")
                    print("==========================================================")
                    send_telegram_notification("⚠️ *PANIC BUTTON TRIGGERED!* O mouse foi movido fisicamente pelo operador humano. Controle devolvido.")
                    log_event("danger", "Panic Button acionado — controle devolvido ao operador.")
                    update_claw_status("stopped", step, self.config.max_steps, last_seen_title, self.config.goal, temp_thumb)
                    return
                    
                # 3. SEE (Varredura Visual da janela ativa)
                try:
                    state_data = claw_vision.scan_active_window()
                    title = state_data["title"]
                    bounds = state_data["bounds"]
                    controls = state_data["controls"]
                    
                    last_seen_title = title # Atualiza para uso remoto
                    
                    print(f"  [See] Janela em Foco: '{title}'")
                    print(f"  [See] Coordenadas Fisicas: {bounds} | Controles: {len(controls)}")
                except Exception as e:
                    print(f"  [See] Falha ao obter dados da janela ativa: {e}")
                    send_telegram_notification(f"⚠️ *Alerta visual*: Falha ao escanear janela ativa: `{e}`")
                    time.sleep(self.config.step_delay_sec)
                    continue
                    
                # 4. THINK — verificação de foco + AUTO-RECUPERAÇÃO (Fase 7)
                if self.config.target_window_title.lower() not in title.lower():
                    self.window_miss_count += 1
                    CLAW_RECOVERY["misses"] = self.window_miss_count
                    log_event("warn", f"Janela alvo fora de foco ({self.window_miss_count}/3).")
                    print(f"  [Think] Janela Alvo nao esta em foco ({self.window_miss_count}/3). Tentando recuperar...")

                    # 1ª tentativa barata: trazer a janela existente para o primeiro plano
                    restored = focus_window_by_title(self.config.target_window_title)
                    if restored:
                        log_event("ok", "Janela alvo trazida de volta ao foco.")
                    elif self.window_miss_count >= 3:
                        # Janela ausente por 3 ciclos consecutivos: relança a aplicação
                        note = f"Janela '{self.config.target_window_title}' ausente por {self.window_miss_count} ciclos — relançando aplicação."
                        CLAW_RECOVERY["last"] = note
                        log_event("warn", note)
                        send_telegram_notification(f"➰ *Auto-Recuperação*: {note}")
                        # Fase B: registra a auto-recuperação como chamado no FreeScout
                        report_incident(
                            "recovery",
                            f"[MECHA] Auto-recuperação: '{self.config.target_window_title}' ausente",
                            f"<b>Janela alvo:</b> {self.config.target_window_title}<br>"
                            f"<b>Ciclos ausente:</b> {self.window_miss_count}<br>"
                            f"<b>Ação:</b> relançamento automático da aplicação.<br>"
                            f"<b>Meta:</b> {self.config.goal}"
                        )
                        if launch_target_app(self.config.target_window_title):
                            CLAW_RECOVERY["last"] = "Comando de relançamento disparado."
                            log_event("ok", "Comando de relançamento disparado.")
                            send_telegram_notification("✅ *Auto-Recuperação*: aplicação relançada. Aguardando reabrir...")
                        else:
                            CLAW_RECOVERY["last"] = "Falha ao relançar a aplicação alvo."
                            log_event("danger", "Falha ao relançar a aplicação alvo.")
                            send_telegram_notification("⚠️ *Auto-Recuperação*: não consegui relançar a aplicação automaticamente.")
                        # Reseta o contador e dá tempo para a aplicação abrir
                        self.window_miss_count = 0
                        CLAW_RECOVERY["misses"] = 0
                        update_claw_status("running", step, self.config.max_steps, last_seen_title, self.config.goal, temp_thumb)
                        time.sleep(self.config.step_delay_sec * 2)
                        continue

                    update_claw_status("running", step, self.config.max_steps, last_seen_title, self.config.goal, temp_thumb)
                    time.sleep(self.config.step_delay_sec)
                    continue
                else:
                    # Janela alvo em foco: zera o contador de recuperação
                    if self.window_miss_count > 0:
                        log_event("ok", "Janela alvo estável novamente.")
                    self.window_miss_count = 0
                    CLAW_RECOVERY["misses"] = 0
                    
                # Calcula o state_id de antemão para gerar o thumbnail correspondente
                import hashlib
                try:
                    controls_str = json.dumps(controls, sort_keys=True)
                except Exception:
                    controls_str = str(controls)
                raw_key = f"{title}-{controls_str}"
                state_id = hashlib.md5(raw_key.encode('utf-8')).hexdigest()
                
                # Captura a imagem para gerar o thumbnail
                try:
                    scene_img = claw_vision.capture_window_area(bounds)
                    temp_thumb = os.path.join(BASE_DIR, "assets", "temp_states", f"state_{state_id}.png")
                    claw_vision.save_window_thumbnail(scene_img, temp_thumb)
                    # Atualiza status com o thumbnail novo
                    update_claw_status("running", step, self.config.max_steps, last_seen_title, self.config.goal, temp_thumb)
                except Exception as img_err:
                    print(f"  [Think] Erro ao gerar thumbnail do estado: {img_err}")
                    
                # Registra o estado atual no grafo de navegacao (passando o visual_path)
                state_id = self.map_manager.add_state(title, controls, visual_path=temp_thumb)
                print(f"  [Think] Estado registrado no Grafo: {state_id}")
                publish_to_bus("nav.open", {
                    "view_id": state_id,
                    "route": title,
                    "source": "claw_scan"
                })
                
                # Registra a transição se viermos de um estado anterior
                if last_state_id and last_state_id != state_id and last_action_desc:
                    self.map_manager.add_transition(
                        last_state_id,
                        state_id,
                        "click",
                        last_click_coord,
                        last_action_desc
                    )
                    print(f"  [Think] Transicao registrada: {last_state_id} -> {state_id}")
                    
                # Sincronizar com o Obsidian automaticamente
                try:
                    self.map_manager.sync_to_obsidian()
                    print("  [Think] Cofre do Obsidian sincronizado com sucesso.")
                except Exception as e:
                    print(f"  [Think] Falha ao exportar notas para o Obsidian: {e}")
                
                # Se a meta estiver definida, chamamos o Cérebro Cognitivo
                action = "fallback"
                if self.config.goal:
                    print(f"  [Think] Meta do Operador: '{self.config.goal}'")
                    
                    # Obter OCR completo da janela ativa para contextualizar a IA
                    ocr_text = ""
                    try:
                        scene_img = claw_vision.capture_window_area(bounds)
                        ocr_result = claw_ocr.extract_text_from_image(scene_img, hwnd=state_data.get("handle", 0))
                        ocr_text = ocr_result.raw_text
                        self.map_manager.last_ocr_text = ocr_text
                        
                        # Se não tivermos controles nativos mas o OCR identificou termos, enriquecemos controls
                        if not controls:
                            ocr_controls = []
                            for reg in ocr_result.regions:
                                text = reg.text if hasattr(reg, 'text') else reg["text"]
                                if len(text) > 3:
                                    ocr_controls.append({
                                        "type": f"ocr_text_{text}",
                                        "relative_bounds": reg.box if hasattr(reg, 'box') else reg["box"]
                                    })
                            if ocr_controls:
                                controls = ocr_controls
                    except Exception as ocr_err:
                        print(f"  [Think] Erro ao obter OCR para o Cérebro: {ocr_err}")
                    
                    # Telemetria de Visão (Fase 7) — reflete se o Gemini multimodal será usado
                    gemini_on = bool(os.environ.get("GEMINI_API_KEY"))
                    CLAW_VISION["active"] = gemini_on
                    CLAW_VISION["using_image"] = bool(gemini_on and temp_thumb and os.path.exists(temp_thumb))
                    if CLAW_VISION["using_image"]:
                        log_event("vision", "Enviando frame ao Gemini para decisão multimodal.")
                    
                    print(f"  [Think] Enviando estado da tela ao Motor Cognitivo...")
                    decision = claw_brain.compute_next_action(
                        self.config.goal,
                        title,
                        ocr_text,
                        controls,
                        image_path=temp_thumb
                    )
                    
                    # Desempacotar decisão do cérebro
                    action = decision.action if hasattr(decision, 'action') else decision.get("action", "wait")
                    target_name = decision.target_name if hasattr(decision, 'target_name') else decision.get("target_name", "none")
                    coords = decision.relative_coords if hasattr(decision, 'relative_coords') else decision.get("relative_coords", (0, 0))
                    reason = decision.reason if hasattr(decision, 'reason') else decision.get("reason", "Sem justificativa.")
                    text_to_type = decision.text_to_type if hasattr(decision, 'text_to_type') else decision.get("text_to_type", None)
                    
                    print(f"  [Think] Decisão do Cérebro:")
                    print(f"   [+] Ação: {action}")
                    print(f"   [+] Alvo: {target_name}")
                    print(f"   [+] Coords Relativas: {coords}")
                    print(f"   [+] Justificativa: {reason}")
                    if text_to_type:
                        print(f"   [+] Texto a digitar: '{text_to_type}'")
                    
                    # Telemetria de Visão (Fase 7) — registra a decisão para o dashboard
                    CLAW_VISION["last_action"] = f"{action} · {target_name}"
                    log_event("judge", f"Juiz IA: Cérebro decidiu ação '{action}' no alvo '{target_name}'. Motivo: {reason}")
                    
                    if action == "done":
                        print("\n==========================================================")
                        print(f" [+] OBJETIVO CUMPRIDO: A IA determinou que a meta foi alcançada!")
                        print(f" [+] Justificativa: {reason}")
                        print("==========================================================")
                        send_telegram_notification(
                            f"✅ *OBJETIVO CUMPRIDO!*\n"
                            f"🎯 Meta alcançada com sucesso!\n"
                            f"💡 *Justificativa*: {reason}",
                            image_path=temp_thumb
                        )
                        log_event("ok", f"Objetivo cumprido: {reason}")
                        update_claw_status("done", step, self.config.max_steps, last_seen_title, self.config.goal, temp_thumb)
                        return
                    elif action == "wait":
                        print(f"  [Think] Cérebro decidiu aguardar. Motivo: {reason}")
                        time.sleep(self.config.step_delay_sec)
                        continue
                    elif action == "click":
                        rel_x, rel_y = coords
                        abs_x = bounds[0] + rel_x
                        abs_y = bounds[1] + rel_y
                        physical_action = "click"
                        action_desc = f"IA Clique: {target_name} ({reason})"
                        print(f"  [Think] Ação Escolhida por IA: Clique em ({abs_x}, {abs_y})")
                    elif action == "type":
                        rel_x, rel_y = coords
                        abs_x = bounds[0] + rel_x
                        abs_y = bounds[1] + rel_y
                        physical_action = "type"
                        action_desc = f"IA Digitação: {target_name} -> '{text_to_type}' ({reason})"
                        print(f"  [Think] Ação Escolhida por IA: Digitar '{text_to_type}' em ({abs_x}, {abs_y})")
                    else:
                        print(f"  [Think] Ação desconhecida '{action}' retornada pelo cérebro. Usando fallback...")
                        action = "fallback"
    
                if action == "fallback":
                    physical_action = "click"
                    # Fallback OCR: se não houver controles nativos de janela, tenta extrair blocos de texto clicáveis
                    if not controls:
                        print(f"  [Think] Nenhum controle nativo exposto. Iniciando busca OCR de fallback...")
                        try:
                            scene_img = claw_vision.capture_window_area(bounds)
                            ocr_result = claw_ocr.extract_text_from_image(scene_img, hwnd=state_data.get("handle", 0))
                            self.map_manager.last_ocr_text = ocr_result.raw_text
                            self.map_manager.save_graph()
                            
                            ocr_controls = []
                            for reg in ocr_result.regions:
                                text = reg.text if hasattr(reg, 'text') else reg["text"]
                                if len(text) > 3: # Ignora ruídos e termos curtos
                                    ocr_controls.append({
                                        "type": f"ocr_text_{text}",
                                        "relative_bounds": reg.box if hasattr(reg, 'box') else reg["box"]
                                    })
                            if ocr_controls:
                                print(f"  [Think] Encontrados {len(ocr_controls)} blocos textuais interativos via OCR.")
                                controls = ocr_controls
                            else:
                                print("  [Think] Nenhum texto relevante identificado por OCR na tela.")
                        except Exception as ocr_err:
                            print(f"  [Think] Erro na varredura OCR de fallback: {ocr_err}")
                    
                    # Decidir acao
                    if not controls:
                        print(f"  [Think] Nenhum controle detectado para interacao neste estado.")
                        time.sleep(self.config.step_delay_sec)
                        continue
                        
                    # Escolhe o primeiro controle disponivel
                    target_ctrl = controls[0]
                    cx1, cy1, cx2, cy2 = target_ctrl["relative_bounds"]
                    rel_x = cx1 + (cx2 - cx1) // 2
                    rel_y = cy1 + (cy2 - cy1) // 2
                    
                    # Converter para coordenadas fisicas absolutas na tela
                    abs_x = bounds[0] + rel_x
                    abs_y = bounds[1] + rel_y
                    
                    action_desc = f"Clicar no controle {target_ctrl['type']}"
                    print(f"  [Think] Acao escolhida: Clique no controle {target_ctrl['type']} em ({abs_x}, {abs_y})")
                
                # 5. ACT (Simulacao fisica de clique ou digitacao)
                if claw_control.check_panic_button():
                    print("\n [!] PANIC BUTTON TRIGGERED segundos antes do clique!")
                    send_telegram_notification("⚠️ *PANIC BUTTON TRIGGERED!* O mouse foi movido fisicamente pelo operador antes da ação física.")
                    update_claw_status("stopped", step, self.config.max_steps, last_seen_title, self.config.goal, temp_thumb)
                    return
                    
                try:
                    if physical_action == "click":
                        print(f"  [Act] Executando simulacao fisica de clique...")
                        claw_control.simulate_click(abs_x, abs_y)
                        print(f"  [Act] Clique efetuado com sucesso.")
                        log_event("ok", f"Ação física executada: Clique em ({abs_x}, {abs_y}) no elemento '{target_name}'")
                    elif physical_action == "type":
                        print(f"  [Act] Executando foco (clique) e simulacao fisica de digitacao...")
                        # Clicar primeiro para dar foco
                        claw_control.simulate_click(abs_x, abs_y)
                        time.sleep(0.15)
                        # Digitar
                        claw_control.simulate_typing(text_to_type or "")
                        print(f"  [Act] Digitacao efetuada com sucesso.")
                        log_event("ok", f"Ação física executada: Digitação de '{text_to_type}' em ({abs_x}, {abs_y})")
                    
                    # Salva dados do último clique para registrar transição no próximo ciclo
                    last_state_id = state_id
                    last_action_desc = action_desc
                    last_click_coord = (rel_x, rel_y)
                except Exception as e:
                    # Fase 7: distingue bloqueio do Firewall Cognitivo de uma falha física comum
                    block = getattr(claw_control, "LAST_BLOCK", None)
                    if block and "FIREWALL_BLOCK" in str(e).upper():
                        CLAW_FIREWALL["block"] = block
                        log_event("danger", f"FIREWALL bloqueou {block.get('action', 'ação')}: {block.get('reason', '')}")
                        publish_to_bus("claw.firewall", {
                            "action_id": block.get("id") or block.get("action"),
                            "risk": block.get("risk"),
                            "reason": block.get("reason"),
                            "context": block.get("context"),
                            "status": "blocked"
                        })
                        # Fase B: registra o bloqueio como chamado no FreeScout
                        def on_ticket_ready(ticket_info):
                            if ticket_info:
                                block["ticket"] = ticket_info.get("number")
                                block["ticket_url"] = ticket_info.get("url")
                                ticket_line = f"\n📋 Chamado FreeScout: #{ticket_info.get('number')}"
                            else:
                                ticket_line = ""
                            send_telegram_notification(
                                f"🛡️ *FIREWALL COGNITIVO* bloqueou `{block.get('action', 'ação')}`\n"
                                f"Risco: *{block.get('risk', '?')}* — {block.get('reason', '')}{ticket_line}\n"
                                f"Use `/resume` para liberar ou `/stop` para abortar."
                            )

                        report_incident(
                            "firewall",
                            f"[MECHA] Firewall bloqueou ação ({block.get('risk','?')})",
                            f"<b>Ação:</b> {block.get('action','?')}<br>"
                            f"<b>Risco:</b> {block.get('risk','?')}<br>"
                            f"<b>Motivo:</b> {block.get('reason','')}<br>"
                            f"<b>Contexto:</b> {block.get('context','')}<br>"
                            f"<b>Janela:</b> {last_seen_title}<br>"
                            f"<b>Meta:</b> {self.config.goal}",
                            callback=on_ticket_ready
                        )
                        update_claw_status("paused", step, self.config.max_steps, last_seen_title, self.config.goal, temp_thumb)
                    else:
                        print(f"  [Act] Falha ao efetuar acao fisica: {e}")
                        send_telegram_notification(f"⚠️ *Falha na ação física*: `{e}`")
                        log_event("danger", f"Falha na ação física: {e}")
                    last_state_id = None
                    last_action_desc = None
                    last_click_coord = None
                    
                time.sleep(self.config.step_delay_sec)
                
            print("\n[+] Loop de acoes atingiu o limite maximo de etapas configuradas.")
            send_telegram_notification(f"ℹ️ *FIM DO LOOP!* O Claw atingiu o limite máximo de {self.config.max_steps} etapas.")
            log_event("info", f"Fim do loop — limite de {self.config.max_steps} etapas atingido.")
            update_claw_status("finished", step, self.config.max_steps, last_seen_title, self.config.goal, temp_thumb)
            
        except Exception as global_err:
            print(f"\n[!] ERRO CRÍTICO NO LOOP: {global_err}")
            send_telegram_notification(f"❌ *ERRO CRÍTICO no Loop!* O processo do Claw falhou.\n⚠️ *Detalhes*: `{global_err}`")
            try:
                log_event("danger", f"Erro crítico no loop: {global_err}")
                update_claw_status("error", 0, self.config.max_steps, "ERROR", self.config.goal, None)
            except Exception:
                pass
            raise global_err


if __name__ == "__main__":
    # Configurar UTF-8 no stdout/stderr no Windows
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    parser = argparse.ArgumentParser(description="MECHA Claw See-Think-Act Action Loop")
    parser.add_argument("--target", type=str, help="Titulo parcial da janela a ser focada para acao")
    parser.add_argument("--goal", type=str, help="Objetivo/meta em linguagem natural para guiar a IA")
    args = parser.parse_args()
    
    if args.target:
        if HAS_PYDANTIC:
            cfg = LoopConfig(target_window_title=args.target, goal=args.goal)
        else:
            cfg = LoopConfig(target_window_title=args.target, goal=args.goal)
            
        loop = ClawActionLoop(cfg)
        loop.start_loop()
    else:
        parser.print_help()
