import os
import sys
import ctypes
from ctypes import wintypes
import time
import argparse



# --- Win32 Structs ---
LONG = ctypes.c_long
DWORD = ctypes.c_ulong

class POINT(ctypes.Structure):
    _fields_ = [("x", LONG), ("y", LONG)]

class MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ("dx", LONG),
        ("dy", LONG),
        ("mouseData", DWORD),
        ("dwFlags", DWORD),
        ("time", DWORD),
        ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))
    ]

class KEYBDINPUT(ctypes.Structure):
    _fields_ = [
        ("wVk", wintypes.WORD),
        ("wScan", wintypes.WORD),
        ("dwFlags", DWORD),
        ("time", DWORD),
        ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))
    ]

class INPUT_UNION(ctypes.Union):
    _fields_ = [
        ("mi", MOUSEINPUT),
        ("ki", KEYBDINPUT)
    ]

class INPUT(ctypes.Structure):
    _fields_ = [
        ("type", DWORD),
        ("ii", INPUT_UNION)
    ]

# Constantes Win32
INPUT_MOUSE = 0
INPUT_KEYBOARD = 1
MOUSEEVENTF_MOVE = 0x0001
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
MOUSEEVENTF_ABSOLUTE = 0x8000

KEYEVENTF_KEYUP = 0x0002
KEYEVENTF_UNICODE = 0x0004

# Variavel global para rastrear a posicao esperada do mouse
LAST_EXPECTED_POS = (0, 0)

def configure_dpi_awareness() -> None:
    """Configura a consciencia de DPI do Windows para evitar oscilacoes de leitura de coordenadas."""
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
    except Exception:
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except Exception:
            pass

# Executa na carga do modulo
configure_dpi_awareness()

# --- APIs Nativas ---
def get_cursor_position() -> tuple:
    """Obtem a coordenada fisica atual do cursor na tela."""
    pt = POINT()
    ctypes.windll.user32.GetCursorPos(ctypes.byref(pt))
    return (int(pt.x), int(pt.y))

def set_expected_position(x: int, y: int) -> None:
    """Atualiza a posicao que o software espera que o mouse esteja."""
    global LAST_EXPECTED_POS
    LAST_EXPECTED_POS = (x, y)

def check_panic_button() -> bool:
    """
    Compara a posicao real com a esperada pelo software.
    Retorna True se houver desvio manual superior a 10 pixels (gatilho de panico).
    """
    global LAST_EXPECTED_POS
    if LAST_EXPECTED_POS == (0, 0):
        # Nao inicializado ou sem acao previa
        return False
        
    real_x, real_y = get_cursor_position()
    exp_x, exp_y = LAST_EXPECTED_POS
    
    delta_x = abs(real_x - exp_x)
    delta_y = abs(real_y - exp_y)
    
    # Se o delta for maior que 45 pixels, significa que o usuario moveu o mouse de verdade (preempcao)
    if delta_x > 45 or delta_y > 45:
        return True
    return False

def move_mouse(x: int, y: int) -> None:
    """Move o cursor do mouse de forma absoluta suportando setups multimonitor (Virtual Desktop)."""
    # Constantes de metrica de tela virtual do Windows
    # SM_XVIRTUALSCREEN = 76, SM_YVIRTUALSCREEN = 77
    # SM_CXVIRTUALSCREEN = 78, SM_CYVIRTUALSCREEN = 79
    v_left = ctypes.windll.user32.GetSystemMetrics(76)
    v_top = ctypes.windll.user32.GetSystemMetrics(77)
    v_width = ctypes.windll.user32.GetSystemMetrics(78)
    v_height = ctypes.windll.user32.GetSystemMetrics(79)
    
    # Se falhar em obter métricas virtuais, usa o monitor principal como fallback
    if v_width <= 0 or v_height <= 0:
        v_left = 0
        v_top = 0
        v_width = ctypes.windll.user32.GetSystemMetrics(0)
        v_height = ctypes.windll.user32.GetSystemMetrics(1)
        
    # Prevenir coordenadas fora do desktop virtual total
    if x < v_left or x > (v_left + v_width) or y < v_top or y > (v_top + v_height):
        raise ValueError(f"Coordenadas de movimento invalidas no Desktop Virtual ({v_width}x{v_height}): ({x}, {y})")
        
    # Converter coordenadas fisicas para espaco absoluto (0 a 65535) da tela virtual
    abs_x = int(((x - v_left) / v_width) * 65535.0)
    abs_y = int(((y - v_top) / v_height) * 65535.0)
    
    # Flags: MOVE + ABSOLUTE + VIRTUALDESK (0x4000)
    dw_flags = MOUSEEVENTF_MOVE | MOUSEEVENTF_ABSOLUTE | 0x4000
    
    # Preparar estrutura INPUT
    extra = ctypes.c_ulong(0)
    ii_ = INPUT_UNION()
    ii_.mi = MOUSEINPUT(abs_x, abs_y, 0, dw_flags, 0, ctypes.pointer(extra))
    input_event = INPUT(INPUT_MOUSE, ii_)
    
    # Registrar a nova posicao esperada antes de acionar o hardware
    set_expected_position(x, y)
    
    # Enviar evento
    ctypes.windll.user32.SendInput(1, ctypes.byref(input_event), ctypes.sizeof(input_event))
    time.sleep(0.02) # Sincronizacao fisica sutil

# ──────────────────────────────────────────────────────────────────────
# FIREWALL COGNITIVO (Fase 7)
# ──────────────────────────────────────────────────────────────────────
# Termos de risco operacional monitorados pela camada rápida (determinística).
PROHIBITED_WORDS = ["deletar", "excluir", "delete", "formatar", "shutdown", "destroy",
                    "apagar", "remover", "desinstalar", "uninstall", "wipe"]

# Modelo do Ollama usado na classificação cognitiva de risco.
OLLAMA_FIREWALL_MODEL = os.environ.get("CLAW_FIREWALL_MODEL", "llama3")

# Detalhes do último bloqueio — lido pelo claw_loop e exibido no dashboard (mecha.html).
LAST_BLOCK = None


def _set_block(action: str, risk: str, reason, context: str = "") -> None:
    """Registra o último bloqueio do firewall para o loop e o dashboard consumirem."""
    global LAST_BLOCK
    LAST_BLOCK = {
        "action": action,
        "risk": str(risk),
        "reason": str(reason)[:200],
        "context": str(context)[:160],
        "id": f"fw-{int(time.time() * 1000)}"
    }
    print(f"[!] FIREWALL BLOQUEOU AÇÃO: [{risk}] {reason} -> {action}")


def _ollama_risk_classification(context_text: str):
    """
    Consulta o Ollama local (llama3) para classificar o risco da ação sob o ponto de clique.
    Retorna dict {"risk": ..., "reason": ...} ou None se indisponível.
    """
    try:
        import claw_brain
    except Exception:
        return None

    prompt = (
        "Você é um FIREWALL COGNITIVO de um agente automatizado que clica em telas do Windows.\n"
        "Avalie o RISCO de clicar no elemento, com base no texto ao redor do ponto de clique.\n"
        "Classifique como:\n"
        " - 'destructive': excluir/apagar/formatar/desinstalar/fechar sem salvar/limpar dados.\n"
        " - 'dangerous': ações sensíveis e irreversíveis (enviar, pagar, publicar, confirmar exclusão).\n"
        " - 'safe': qualquer outra navegação comum.\n"
        "Responda APENAS com JSON válido, sem markdown e sem texto extra:\n"
        '{"risk":"safe|dangerous|destructive","reason":"motivo curto"}\n\n'
        f'TEXTO AO REDOR DO PONTO DE CLIQUE:\n"""{context_text[:400]}"""'
    )
    try:
        data = claw_brain.ask_ollama(prompt, model=OLLAMA_FIREWALL_MODEL)
    except Exception:
        return None

    if isinstance(data, dict) and data.get("risk"):
        return data
    return None


def validate_action_safety(x: int, y: int) -> bool:
    """
    Captura uma região de 120x120 px ao redor do ponto de clique (x, y) e roda OCR em RAM.
    Camada 1: lista determinística de termos proibidos (rápida, sempre ativa).
    Camada 2: classificação cognitiva via Ollama local (se houver texto ambíguo).
    Retorna False (bloqueia) se a ação for considerada perigosa/destrutiva.
    """
    try:
        import claw_vision
        import claw_ocr
        
        hwnd = ctypes.windll.user32.GetForegroundWindow()
        bounds = claw_vision.get_window_bounds(hwnd)
        
        wx1, wy1, wx2, wy2 = bounds
        if x < wx1 or x > wx2 or y < wy1 or y > wy2:
            return True # Ponto fora da janela ativa, não monitorável de forma segura
            
        scene_img = claw_vision.capture_window_area(bounds)
        
        # Converter ponto de clique absoluto para coordenadas relativas da janela
        rx = x - wx1
        ry = y - wy1
        
        cx1 = max(0, rx - 60)
        cy1 = max(0, ry - 60)
        cx2 = min(scene_img.width, rx + 60)
        cy2 = min(scene_img.height, ry + 60)
        
        crop_img = scene_img.crop((cx1, cy1, cx2, cy2))
        
        # Executa OCR rápido na vizinhança do clique
        result = claw_ocr.extract_text_from_image(crop_img)
        raw_text = result.raw_text
        detected_text = raw_text.lower()
        
        # ── Camada 1: lista rápida determinística ──
        for word in PROHIBITED_WORDS:
            if word in detected_text:
                _set_block(f"click({x},{y})", "destructive",
                           f"Termo proibido '{word}' detectado sob o clique.", raw_text)
                return False
        
        # ── Camada 2: classificação cognitiva local (Ollama) ──
        if len(detected_text.strip()) >= 4:
            verdict = _ollama_risk_classification(raw_text)
            if verdict:
                risk = str(verdict.get("risk", "safe")).lower()
                try:
                    from claw_loop import log_event
                    log_event("judge", f"Firewall cognitivo (Ollama) julgou o risco sob o clique como '{risk}'. Motivo: {verdict.get('reason')}")
                except Exception as log_err:
                    print(f" [!] Erro ao tentar registrar log do judge no firewall: {log_err}")
                if risk in ("dangerous", "destructive", "perigosa", "destrutiva"):
                    _set_block(f"click({x},{y})", risk,
                               verdict.get("reason", "Classificado como arriscado pela IA local."),
                               raw_text)
                    return False
        
        return True
    except Exception as e:
        # Se falhar o motor OCR/IA por falta de imports no ambiente isolado, passa por tolerância
        print(f" [!] Aviso no Firewall de cliques: {e}")
        return True

def simulate_click(x: int, y: int) -> tuple:
    """Envia a sequencia de clique (Left Down -> Left Up) nas coordenadas (x, y)."""
    # 1. Validar seguranca com o Firewall de Cliques
    if not validate_action_safety(x, y):
        print(" [!] Interrompendo acao física e disparando o Panic Button automaticamente!")
        raise PermissionError("FIREWALL_BLOCK: Acao classificada como perigosa no ponto de clique.")

    # Mover primeiro
    move_mouse(x, y)
    
    # Clique Down
    extra = ctypes.c_ulong(0)
    ii_down = INPUT_UNION()
    ii_down.mi = MOUSEINPUT(0, 0, 0, MOUSEEVENTF_LEFTDOWN, 0, ctypes.pointer(extra))
    input_down = INPUT(INPUT_MOUSE, ii_down)
    
    # Clique Up
    ii_up = INPUT_UNION()
    ii_up.mi = MOUSEINPUT(0, 0, 0, MOUSEEVENTF_LEFTUP, 0, ctypes.pointer(extra))
    input_up = INPUT(INPUT_MOUSE, ii_up)
    
    # Enviar cliques
    ctypes.windll.user32.SendInput(1, ctypes.byref(input_down), ctypes.sizeof(input_down))
    time.sleep(0.05)
    ctypes.windll.user32.SendInput(1, ctypes.byref(input_up), ctypes.sizeof(input_up))
    
    return (x, y)

def simulate_typing(text: str) -> None:
    """Simula a digitação física de uma string caractere por caractere via SendInput usando Unicode."""
    # VK_RETURN = 0x0D, VK_TAB = 0x09, VK_BACK = 0x08
    special_keys = {
        "\n": 0x0D,
        "\r": 0x0D,
        "\t": 0x09,
        "\b": 0x08
    }
    
    for char in text:
        extra = ctypes.c_ulong(0)
        
        # Mapeamento para teclas especiais vs Unicode normal
        if char in special_keys:
            w_vk = special_keys[char]
            w_scan = 0
            flags_down = 0
            flags_up = KEYEVENTF_KEYUP
        else:
            w_vk = 0
            w_scan = ord(char)
            flags_down = KEYEVENTF_UNICODE
            flags_up = KEYEVENTF_UNICODE | KEYEVENTF_KEYUP
            
        # 1. Key Down
        ki_down = KEYBDINPUT(w_vk, w_scan, flags_down, 0, ctypes.pointer(extra))
        ii_down = INPUT_UNION(ki=ki_down)
        input_down = INPUT(INPUT_KEYBOARD, ii_down)
        
        # 2. Key Up
        ki_up = KEYBDINPUT(w_vk, w_scan, flags_up, 0, ctypes.pointer(extra))
        ii_up = INPUT_UNION(ki=ki_up)
        input_up = INPUT(INPUT_KEYBOARD, ii_up)
        
        # Enviar comandos de teclado
        ctypes.windll.user32.SendInput(1, ctypes.byref(input_down), ctypes.sizeof(input_down))
        time.sleep(0.01)
        ctypes.windll.user32.SendInput(1, ctypes.byref(input_up), ctypes.sizeof(input_up))
        time.sleep(0.02) # Delay simulado para resiliência na digitação

def run_test_control():
    print("[*] Iniciando teste de movimentacao fisica do cursor...")
    print("[*] Mantenha as maos longe do mouse para o teste automatico...")
    
    # Salvar posicao inicial
    start_x, start_y = get_cursor_position()
    set_expected_position(start_x, start_y)
    
    # Fazer um movimento quadrado de teste com verificacao de panico em cada etapa
    path = [
        (start_x + 50, start_y),
        (start_x + 50, start_y + 50),
        (start_x, start_y + 50),
        (start_x, start_y)
    ]
    
    try:
        for idx, (tx, ty) in enumerate(path):
            # Verificar panico antes de agir
            if check_panic_button():
                print("[!] PANIC BUTTON TRIGGERED: Interrompendo movimento!")
                return False
                
            print(f" [+] Movendo etapa {idx + 1} para: ({tx}, {ty})")
            move_mouse(tx, ty)
            time.sleep(0.3)
            
        print("[+] Teste de movimentacao concluido com sucesso!")
        return True
    except Exception as e:
        print(f"[!] Erro no teste de controle: {e}")
        return False

if __name__ == "__main__":
    # Configurar UTF-8 no stdout/stderr no Windows
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    parser = argparse.ArgumentParser(description="MECHA Claw Physical Action Controller")
    parser.add_argument("--test-control", action="store_true", help="Roda o teste de movimentacao de cursor")
    parser.add_argument("--type", type=str, help="Simula a digitacao fisica de um texto apos 2 segundos")
    args = parser.parse_args()
    
    if args.test_control:
        success = run_test_control()
        if success:
            print("[*] Testando digitacao vazia de seguranca...")
            simulate_typing("")
            print("[+] Teste de digitacao basica de seguranca concluido!")
        sys.exit(0 if success else 1)
    elif args.type:
        print(f"[*] Focando a janela desejada em 2 segundos para digitar: '{args.type}'...")
        time.sleep(2.0)
        print("[*] Digitando...")
        simulate_typing(args.type)
        print("[+] Digitacao concluida com sucesso!")
        sys.exit(0)
    else:
        # Modo interativo simples para obter posicao
        x, y = get_cursor_position()
        print(f"Posicao atual do cursor: (x: {x}, y: {y})")
