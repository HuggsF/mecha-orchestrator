import os
import sys
import ctypes
from ctypes import wintypes
import hashlib
from PIL import Image, ImageGrab
import json

from typing import Tuple, List

try:
    from pydantic import BaseModel, Field, field_validator
    HAS_PYDANTIC = True
except ImportError:
    HAS_PYDANTIC = False



# --- Win32 Structures ---
class RECT(ctypes.Structure):
    _fields_ = [
        ("left", ctypes.c_long),
        ("top", ctypes.c_long),
        ("right", ctypes.c_long),
        ("bottom", ctypes.c_long)
    ]

# --- Pydantic Data Models ---
if HAS_PYDANTIC:
    class ControlNode(BaseModel):
        type: str
        relative_bounds: Tuple[int, int, int, int]  # (x1, y1, x2, y2)
        color_hash: str

        @field_validator('relative_bounds')
        @classmethod
        def validate_bounds(cls, v: Tuple[int, int, int, int]) -> Tuple[int, int, int, int]:
            x1, y1, x2, y2 = v
            if x1 < 0 or y1 < 0 or x2 < x1 or y2 < y1:
                raise ValueError(f"Invalid relative bounds: {v}")
            return v

    class WindowState(BaseModel):
        handle: int
        title: str
        bounds: Tuple[int, int, int, int]  # (left, top, right, bottom)
        controls: List[ControlNode]

        @field_validator('bounds')
        @classmethod
        def validate_window_bounds(cls, v: Tuple[int, int, int, int]) -> Tuple[int, int, int, int]:
            left, top, right, bottom = v
            if right < left or bottom < top:
                raise ValueError(f"Invalid window bounds: {v}")
            return v

    class ScreenshotSize(BaseModel):
        width: int = Field(..., gt=0, description="Screenshot width in pixels")
        height: int = Field(..., gt=0, description="Screenshot height in pixels")
else:
    class ControlNode:
        def __init__(self, type: str, relative_bounds: Tuple[int, int, int, int], color_hash: str):
            self.type = type
            self.relative_bounds = relative_bounds
            self.color_hash = color_hash
        def model_dump(self):
            return {"type": self.type, "relative_bounds": self.relative_bounds, "color_hash": self.color_hash}

    class WindowState:
        def __init__(self, handle: int, title: str, bounds: Tuple[int, int, int, int], controls: list):
            self.handle = handle
            self.title = title
            self.bounds = bounds
            self.controls = controls
        def model_dump(self):
            return {
                "handle": self.handle,
                "title": self.title,
                "bounds": self.bounds,
                "controls": [c.model_dump() if hasattr(c, 'model_dump') else c for c in self.controls]
            }

    class ScreenshotSize:
        def __init__(self, width: int, height: int):
            if width <= 0 or height <= 0:
                raise ValueError("Screenshot dimensions must be positive")
            self.width = width
            self.height = height

# --- Win32 Native Calls ---
def configure_dpi_awareness() -> None:
    """Configura o Windows para nao distorcer as coordenadas da janela (High DPI)."""
    try:
        # Tenta SetProcessDpiAwareness(2) -> PROCESS_PER_MONITOR_DPI_AWARE
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
        # print("[*] DPI Awareness: Process Per Monitor V2 configurado.")
    except Exception:
        try:
            # Fallback para Windows Vista+
            ctypes.windll.user32.SetProcessDPIAware()
            # print("[*] DPI Awareness: Process DPI Aware configurado.")
        except Exception as e:
            print(f"[!] Erro ao configurar DPI Awareness: {e}")

def get_active_window_handle() -> int:
    """Obtem o HWND da janela ativa."""
    return ctypes.windll.user32.GetForegroundWindow()

def get_window_bounds(hwnd: int) -> tuple:
    """Calcula os limites físicos da janela no monitor."""
    rect = RECT()
    result = ctypes.windll.user32.GetWindowRect(hwnd, ctypes.byref(rect))
    if not result:
        raise ValueError(f"Nao foi possivel obter limites para a janela HWND: {hwnd}")
    
    # Validar limites logicos razoaveis (0 a 8000)
    for coord in (rect.left, rect.top, rect.right, rect.bottom):
        if coord < -10000 or coord > 10000:
            raise ValueError(f"Coordenadas da janela invalidas no Windows: ({rect.left}, {rect.top}, {rect.right}, {rect.bottom})")
            
    return (int(rect.left), int(rect.top), int(rect.right), int(rect.bottom))

def get_window_title(hwnd: int) -> str:
    """Obtem o titulo textual da janela em formato Unicode (UTF-16)."""
    length = ctypes.windll.user32.GetWindowTextLengthW(hwnd)
    if length == 0:
        return "Untitled Window"
    
    buffer = ctypes.create_unicode_buffer(length + 1)
    ctypes.windll.user32.GetWindowTextW(hwnd, buffer, length + 1)
    return buffer.value.strip()

# --- Image Processing & Control Detection (RAM Only) ---
def capture_window_area(bounds: tuple) -> Image.Image:
    """Captura a sub-regiao da tela fisica."""
    left, top, right, bottom = bounds
    width = right - left
    height = bottom - top
    
    # Previne capturas de janelas minimizadas ou invalidas
    if width <= 0 or height <= 0:
        raise ValueError(f"Area de janela invalida para captura: {width}x{height}")
        
    # ImageGrab.grab faz a captura direta do display do Windows
    return ImageGrab.grab(bbox=(left, top, right, bottom))

def detect_visual_controls(img: Image.Image) -> list:
    """
    Detecta de forma simples botoes e controles em memoria RAM.
    Converte para tons de cinza e encontra mudancas abruptas de brilho (contornos).
    """
    # Converte para Grayscale (L)
    gray = img.convert("L")
    w, h = gray.size
    
    # Amostra de pixels para detectar contornos rapidos
    # Para performance, fazemos uma varredura em grid (passo de 10 pixels)
    step = 12
    controls = []
    
    # Matriz para marcar areas ja identificadas
    visited = [[False for _ in range(w)] for _ in range(h)]
    
    for y in range(step, h - step, step):
        for x in range(step, w - step, step):
            if visited[y][x]:
                continue
                
            # Delta de contraste vertical/horizontal
            val = gray.getpixel((x, y))
            right_val = gray.getpixel((x + 4, y))
            down_val = gray.getpixel((x, y + 4))
            
            # Se a diferenca de brilho for acentuada, encontramos uma borda de controle
            if abs(val - right_val) > 25 or abs(val - down_val) > 25:
                # Estender caixa delimitadora de controle
                x1, y1 = max(0, x - 20), max(0, y - 10)
                x2, y2 = min(w, x + 60), min(h, y + 20)
                
                # Marcar regiao como visitada
                for vy in range(y1, y2):
                    for vx in range(x1, x2):
                        if vy < h and vx < w:
                            visited[vy][vx] = True
                
                # Gerar hash visual simples da regiao do botao
                crop_area = gray.crop((x1, y1, x2, y2))
                pixel_data = bytes(crop_area.getdata())
                color_hash = hashlib.md5(pixel_data).hexdigest()[:4]
                
                # Definir o tipo do controle com base na proporcao da caixa
                ctrl_w = x2 - x1
                ctrl_h = y2 - y1
                ctrl_type = "button" if ctrl_w > ctrl_h * 2 else "input"
                
                if HAS_PYDANTIC:
                    node = ControlNode(type=ctrl_type, relative_bounds=(x1, y1, x2, y2), color_hash=color_hash)
                else:
                    node = ControlNode(type=ctrl_type, relative_bounds=(x1, y1, x2, y2), color_hash=color_hash)
                controls.append(node)
                
                # Limite maximo de controles detectados para nao sobrecarregar o grafo
                if len(controls) >= 12:
                    return controls
                    
    return controls

def scan_active_window() -> dict:
    """Executa o pipeline completo de varredura real do Windows."""
    configure_dpi_awareness()
    hwnd = get_active_window_handle()
    if not hwnd:
        raise ValueError("Nenhuma janela ativa em foco encontrada.")
        
    title = get_window_title(hwnd)
    bounds = get_window_bounds(hwnd)
    
    # Processa estritamente em RAM
    img = capture_window_area(bounds)
    controls = detect_visual_controls(img)
    
    if HAS_PYDANTIC:
        state = WindowState(handle=hwnd, title=title, bounds=bounds, controls=controls)
    else:
        state = WindowState(handle=hwnd, title=title, bounds=bounds, controls=controls)
        
    return state.model_dump() if hasattr(state, 'model_dump') else state.model_dump() if HAS_PYDANTIC else state.model_dump()

def save_window_thumbnail(img: Image.Image, output_path: str, max_width: int = 320) -> str:
    """
    Redimensiona proporcionalmente a imagem da janela para max_width e a salva como PNG.
    Cria os diretórios pai caso não existam.
    """
    parent_dir = os.path.dirname(output_path)
    if parent_dir:
        os.makedirs(parent_dir, exist_ok=True)
        
    w, h = img.size
    if w > max_width:
        ratio = max_width / float(w)
        new_h = int(float(h) * ratio)
        try:
            resample_filter = Image.Resampling.LANCZOS
        except AttributeError:
            resample_filter = Image.ANTIALIAS
            
        img_resized = img.resize((max_width, new_h), resample_filter)
    else:
        img_resized = img
        
    img_resized.save(output_path, format="PNG", optimize=True)
    return output_path

if __name__ == "__main__":
    # Configurar UTF-8 no stdout/stderr no Windows
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    # Execucao via cli para teste rapido
    try:
        print("[*] Iniciando varredura da janela ativa no Windows...")
        # Aguarda 2 segundos para o usuario dar foco na janela desejada
        import time
        print("[*] Focando tela... Aguarde 2 segundos...")
        time.sleep(2)
        
        state_data = scan_active_window()
        print("\n==========================================================")
        print(f" [+] JANELA CAPTURADA: {state_data['title']}")
        print(f" [+] HWND: {state_data['handle']}")
        print(f" [+] LIMITES (bounds): {state_data['bounds']}")
        print(f" [+] CONTROLES DETECTADOS: {len(state_data['controls'])}")
        print("==========================================================")
        
        for idx, ctrl in enumerate(state_data['controls']):
            bounds = ctrl['relative_bounds']
            print(f"  [{idx + 1}] Tipo: {ctrl['type']} | Bounds Relativo: {bounds} | Hash: {ctrl['color_hash']}")
        print("==========================================================")
        sys.exit(0)
    except Exception as e:
        print(f"[!] ERRO na varredura ativa: {e}")
        sys.exit(1)
