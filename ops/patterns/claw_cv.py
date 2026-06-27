import os
import sys
import argparse
import json
from PIL import Image, ImageDraw
import time

try:
    from pydantic import BaseModel, Field
    HAS_PYDANTIC = True
except ImportError:
    HAS_PYDANTIC = False

try:
    import cv2
    import numpy as np
    HAS_OPENCV = True
except ImportError:
    HAS_OPENCV = False

# --- Configurar UTF-8 no stdout/stderr no Windows ---
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')


# --- Pydantic Data Models ---
if HAS_PYDANTIC:
    class MatchResult(BaseModel):
        found: bool = False
        center_coord: tuple = (0, 0)
        confidence: float = 0.0
        box: tuple = (0, 0, 0, 0)
else:
    class MatchResult:
        def __init__(self, found=False, center_coord=(0, 0), confidence=0.0, box=(0, 0, 0, 0)):
            self.found = found
            self.center_coord = center_coord
            self.confidence = confidence
            self.box = box
        def model_dump(self):
            return {
                "found": self.found,
                "center_coord": self.center_coord,
                "confidence": self.confidence,
                "box": self.box
            }


# --- Algoritmos de Visao ---
def locate_template_pillow(scene: Image.Image, template: Image.Image, threshold: float = 0.85) -> MatchResult:
    """
    Busca o template na cena usando Pillow purista (fallback).
    Varre a cena com amostragens inteligentes para performance de CPU.
    """
    sw, sh = scene.size
    tw, th = template.size
    
    if tw > sw or th > sh:
        if HAS_PYDANTIC:
            return MatchResult()
        else:
            return MatchResult()
            
    # Converter imagens para RGB
    scene_rgb = scene.convert("RGB")
    temp_rgb = template.convert("RGB")
    
    best_conf = 0.0
    best_loc = (0, 0)
    
    # Grid de passos de pixel para busca rapida
    step_x = max(1, tw // 4)
    step_y = max(1, th // 4)
    
    # Fase 1: Coarse Search (Varredura de baixa resolucao)
    for y in range(0, sh - th, step_y):
        for x in range(0, sw - tw, step_x):
            # Compara cantos e centro do template para validacao rapida
            pts = [(0, 0), (tw//2, th//2), (tw-1, th-1)]
            match_score = 0
            for px, py in pts:
                s_pix = scene_rgb.getpixel((x + px, y + py))
                t_pix = temp_rgb.getpixel((px, py))
                diff = sum(abs(s_pix[i] - t_pix[i]) for i in range(3))
                if diff < 45: # Delta toleravel de cor
                    match_score += 1
            
            # Se a amostragem for promissora, faz a varredura fina
            if match_score >= 2:
                # Fase 2: Fine Search (Contagem detalhada de diferenca de pixels)
                diff_sum = 0
                sample_pts = 0
                for ty in range(0, th, max(1, th//6)):
                    for tx in range(0, tw, max(1, tw//6)):
                        s_pix = scene_rgb.getpixel((x + tx, y + ty))
                        t_pix = temp_rgb.getpixel((tx, ty))
                        diff_sum += sum(abs(s_pix[i] - t_pix[i]) for i in range(3))
                        sample_pts += 1
                        
                avg_diff = diff_sum / (sample_pts * 3 * 255.0)
                conf = 1.0 - avg_diff
                
                if conf > best_conf:
                    best_conf = conf
                    best_loc = (x, y)
                    
    if best_conf >= threshold:
        cx = best_loc[0] + tw // 2
        cy = best_loc[1] + th // 2
        box = (best_loc[0], best_loc[1], best_loc[0] + tw, best_loc[1] + th)
        if HAS_PYDANTIC:
            return MatchResult(found=True, center_coord=(cx, cy), confidence=best_conf, box=box)
        else:
            return MatchResult(found=True, center_coord=(cx, cy), confidence=best_conf, box=box)
            
    if HAS_PYDANTIC:
        return MatchResult(confidence=best_conf)
    else:
        return MatchResult(confidence=best_conf)


def locate_template_opencv(scene: Image.Image, template: Image.Image, threshold: float = 0.85) -> MatchResult:
    """Busca o template de forma ultra-rapida usando OpenCV (matchTemplate)."""
    if not HAS_OPENCV:
        # Fallback automatico
        return locate_template_pillow(scene, template, threshold)
        
    # Converter imagens PIL para NumPy arrays (RGB para BGR)
    scene_cv = cv2.cvtColor(np.array(scene), cv2.COLOR_RGB2BGR)
    temp_cv = cv2.cvtColor(np.array(template), cv2.COLOR_RGB2BGR)
    
    # matchTemplate
    res = cv2.matchTemplate(scene_cv, temp_cv, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    
    if max_val >= threshold:
        tx, ty = max_loc
        tw, th = template.size
        cx = tx + tw // 2
        cy = ty + th // 2
        box = (tx, ty, tx + tw, ty + th)
        if HAS_PYDANTIC:
            return MatchResult(found=True, center_coord=(cx, cy), confidence=float(max_val), box=box)
        else:
            return MatchResult(found=True, center_coord=(cx, cy), confidence=float(max_val), box=box)
            
    if HAS_PYDANTIC:
        return MatchResult(confidence=float(max_val))
    else:
        return MatchResult(confidence=float(max_val))


def find_target_on_screen(template_name: str, threshold: float = 0.85) -> dict:
    """
    Carrega o template e tenta localiza-lo na tela ativa capturada.
    Garante a criacao da pasta de templates de assets.
    """
    assets_dir = "c:/Users/huggs/OneDrive/Documentos/workspace/.mecha/ops/assets/templates"
    if not os.path.exists(assets_dir):
        os.makedirs(assets_dir, exist_ok=True)
        
    template_path = os.path.join(assets_dir, template_name)
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Template visual nao encontrado na pasta de assets: {template_path}")
        
    # 1. Capturar a tela ativa (See) usando claw_vision
    import claw_vision
    hwnd = claw_vision.get_active_window_handle()
    bounds = claw_vision.get_window_bounds(hwnd)
    scene_img = claw_vision.capture_window_area(bounds)
    template_img = Image.open(template_path)
    
    # 2. Localizar (OpenCV ou Pillow)
    result = locate_template_opencv(scene_img, template_img, threshold)
    
    # Converte coordenadas relativas para absolutas na tela fisica
    res_dict = result.model_dump() if hasattr(result, 'model_dump') else result.model_dump() if HAS_PYDANTIC else result.model_dump()
    if res_dict["found"]:
        rx, ry = res_dict["center_coord"]
        abs_x = bounds[0] + rx
        abs_y = bounds[1] + ry
        res_dict["absolute_center"] = (abs_x, abs_y)
        
    return res_dict


def run_test_vision():
    print("[*] Iniciando teste de Visao por Computador (Template Matching)...")
    
    # Criar uma imagem de cena mock
    scene = Image.new("RGB", (600, 400), "#07090c")
    draw = ImageDraw.Draw(scene)
    # Desenhar um botao dourado na coordenada (250, 180)
    draw.rectangle([(250, 180), (350, 220)], fill="#ffb000")
    draw.text((275, 195), "CLICK ME", fill="#07090c")
    
    # Criar o template do botao
    template = Image.new("RGB", (100, 40), "#ffb000")
    tdraw = ImageDraw.Draw(template)
    tdraw.text((25, 15), "CLICK ME", fill="#07090c")
    
    # Rodar buscas
    print("[*] Buscando via Pillow...")
    p_res = locate_template_pillow(scene, template)
    print(f" [+] Pillow Result -> Encontrado: {p_res.found} | Centro: {p_res.center_coord} | Confianca: {p_res.confidence:.2f}")
    
    if HAS_OPENCV:
        print("[*] Buscando via OpenCV...")
        cv_res = locate_template_opencv(scene, template)
        print(f" [+] OpenCV Result -> Encontrado: {cv_res.found} | Centro: {cv_res.center_coord} | Confianca: {cv_res.confidence:.2f}")
    else:
        print("[*] OpenCV nao disponivel. Pulando teste OpenCV.")
        
    if p_res.found and p_res.center_coord == (300, 200):
        print("[+] Teste de Visao concluido com sucesso!")
        return True
    else:
        print("[!] Falha: Coordenada de acerto invalida.")
        return False


if __name__ == "__main__":
    # Forcar UTF-8 no stdout/stderr no Windows
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    
    parser = argparse.ArgumentParser(description="MECHA Claw Computer Vision target finder")
    parser.add_argument("--test-vision", action="store_true", help="Roda o teste unitario de busca de template")
    parser.add_argument("--find", type=str, help="Procura um icone especifico na tela ativa")
    args = parser.parse_args()
    
    if args.test_vision:
        success = run_test_vision()
        sys.exit(0 if success else 1)
    elif args.find:
        try:
            res = find_target_on_screen(args.find)
            print(json.dumps(res, indent=2))
            sys.exit(0)
        except Exception as e:
            print(f"[!] ERRO: {e}")
            sys.exit(1)
    else:
        parser.print_help()
