import os
import sys
import json
import argparse
from typing import List, Tuple, Optional

try:
    from pydantic import BaseModel, Field, field_validator
    HAS_PYDANTIC = True
except ImportError:
    HAS_PYDANTIC = False
    print("Warning: Pydantic is not installed. Using fallback validator logic.")

try:
    from PIL import Image, ImageDraw, ImageFont
    HAS_PIL = True
except ImportError:
    HAS_PIL = False
    print("Warning: Pillow (PIL) is not installed. Image rendering will use dummy fallback.")

# --- classes de Validacao Pydantic ---
if HAS_PYDANTIC:
    class ShapeCommand(BaseModel):
        type: str  # "circle", "rectangle", "line", "text"
        coords: Tuple[int, int, int, int]  # (x1, y1, x2, y2)
        color: str = "#ffb000"
        width: int = 2
        text_content: Optional[str] = None

        @field_validator('coords')
        @classmethod
        def check_bounds(cls, coords: Tuple[int, int, int, int]) -> Tuple[int, int, int, int]:
            for c in coords:
                if c < 0 or c > 4000:
                    raise ValueError(f"Coordenada {c} fora dos limites fisicos permitidos (0 a 4000)")
            return coords

    class CanvasRequest(BaseModel):
        width: int = 800
        height: int = 600
        background: str = "#07090c"
        shapes: List[ShapeCommand]
        output_path: str
else:
    class ShapeCommand:
        def __init__(self, **kwargs):
            self.type = kwargs.get("type")
            self.coords = kwargs.get("coords")
            self.color = kwargs.get("color", "#ffb000")
            self.width = kwargs.get("width", 2)
            self.text_content = kwargs.get("text_content")
            for c in self.coords:
                if c < 0 or c > 4000:
                    raise ValueError(f"Coordenada {c} fora dos limites permitidos (0 a 4000)")

    class CanvasRequest:
        def __init__(self, **kwargs):
            self.width = kwargs.get("width", 800)
            self.height = kwargs.get("height", 600)
            self.background = kwargs.get("background", "#07090c")
            self.shapes = [ShapeCommand(**s) for s in kwargs.get("shapes", [])]
            self.output_path = kwargs.get("output_path")


# Motor de Desenho Pillow
def draw_canvas(req: CanvasRequest):
    # Assegura que o diretorio de destino exista
    out_dir = os.path.dirname(req.output_path)
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)

    if not HAS_PIL:
        print(f"[!] Pillow nao instalado. Criando arquivo de fallback dummy: {req.output_path}")
        with open(req.output_path, "w", encoding="utf-8") as f:
            f.write(f"DUMMY IMAGE FALLBACK\nWidth: {req.width}\nHeight: {req.height}\nBackground: {req.background}\n")
            for shape in req.shapes:
                f.write(f"Shape: {shape.type} Coords: {shape.coords} Color: {shape.color}\n")
        print("[+] Imagem Dummy criada com sucesso!")
        return

    # Criando o Canvas com cor de fundo
    # Hex to RGB
    bg_color = req.background.lstrip('#')
    bg_rgb = tuple(int(bg_color[i:i+2], 16) for i in (0, 2, 4))
    
    # Criando gradiente bonito se for a cor padrao
    image = Image.new("RGB", (req.width, req.height), bg_rgb)
    draw = ImageDraw.Draw(image)
    
    # Desenhar gradiente linear sutil no background
    if req.background == "#07090c":
        for y in range(req.height):
            # Gradiente de #07090c (RGB 7, 9, 12) para #1a2230 (RGB 26, 34, 48)
            r = int(7 + (26 - 7) * (y / req.height))
            g = int(9 + (34 - 9) * (y / req.height))
            b = int(12 + (48 - 12) * (y / req.height))
            draw.line([(0, y), (req.width, y)], fill=(r, g, b))

    # Renderizar formas vetoriais
    for shape in req.shapes:
        color_hex = shape.color.lstrip('#')
        # Suporta cores RGB simples
        try:
            color_rgb = tuple(int(color_hex[i:i+2], 16) for i in (0, 2, 4))
        except Exception:
            color_rgb = (255, 176, 0) # Gold fallback
            
        x1, y1, x2, y2 = shape.coords
        
        if shape.type == "line":
            draw.line([(x1, y1), (x2, y2)], fill=color_rgb, width=shape.width)
        elif shape.type == "rectangle":
            draw.rectangle([(x1, y1), (x2, y2)], outline=color_rgb, width=shape.width)
        elif shape.type == "circle":
            # Pillow usa bounding box para elipse/circulo
            draw.ellipse([(x1, y1), (x2, y2)], outline=color_rgb, width=shape.width)
        elif shape.type == "text":
            text = shape.text_content or "Text"
            # Escreve o texto com fonte padrao do Pillow
            draw.text((x1, y1), text, fill=color_rgb)
            
    # Salva a imagem
    image.save(req.output_path, "PNG")
    print(f"[+] Imagem vetorial renderizada e salva em: {req.output_path}")


def run_test_generation():
    print("[*] Iniciando geracao de teste do Canvas...")
    # Define caminhos
    output_dir = "c:/Users/huggs/OneDrive/Documentos/workspace/.mecha/ops/maps/out"
    output_file = os.path.join(output_dir, "test_canvas.png")
    
    shapes = [
        # Circulo principal (Representando o Claw)
        {
            "type": "circle",
            "coords": (350, 250, 450, 350),
            "color": "#4fc3f7", # Light Blue
            "width": 3
        },
        # Linhas de conexao da rede de pixels explorados
        {
            "type": "line",
            "coords": (400, 300, 100, 100),
            "color": "#ffb000", # Gold
            "width": 2
        },
        {
            "type": "line",
            "coords": (400, 300, 700, 500),
            "color": "#00e676", # Green Neon
            "width": 2
        },
        # Caixa delimitadora da area ativa do monitor
        {
            "type": "rectangle",
            "coords": (50, 50, 750, 550),
            "color": "#ff1744", # Red
            "width": 1
        },
        # Texto de metadados
        {
            "type": "text",
            "coords": (70, 70, 0, 0),
            "color": "#ffffff",
            "text_content": "CLAW CANVAS: Exploration Pixel Active Grid"
        },
        {
            "type": "text",
            "coords": (70, 510, 0, 0),
            "color": "#4fc3f7",
            "text_content": "Coordinates: (x: 400, y: 300) | State: SCANNING"
        }
    ]
    
    req_data = {
        "width": 800,
        "height": 600,
        "background": "#07090c",
        "shapes": shapes,
        "output_path": output_file
    }
    
    try:
        if HAS_PYDANTIC:
            req = CanvasRequest(**req_data)
        else:
            req = CanvasRequest(**req_data)
            
        draw_canvas(req)
        print(f"[+] Teste do Canvas gerado com sucesso!")
        return True
    except Exception as e:
        print(f"[!] ERRO na geracao de teste do canvas: {e}")
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CLAW Vector Drawing Canvas Engine")
    parser.add_argument("--draw", type=str, help="Caminho do arquivo JSON contendo o CanvasRequest")
    parser.add_argument("--test", action="store_true", help="Gera um desenho de teste de coordenadas do Claw")
    
    args = parser.parse_args()
    
    if args.test:
        success = run_test_generation()
        sys.exit(0 if success else 1)
    elif args.draw:
        if not os.path.exists(args.draw):
            print(f"[!] JSON nao encontrado: {args.draw}")
            sys.exit(1)
        try:
            with open(args.draw, "r") as f:
                data = json.load(f)
            if HAS_PYDANTIC:
                req = CanvasRequest(**data)
            else:
                req = CanvasRequest(**data)
            draw_canvas(req)
            sys.exit(0)
        except Exception as e:
            print(f"[!] ERRO ao renderizar JSON: {e}")
            sys.exit(1)
    else:
        parser.print_help()
