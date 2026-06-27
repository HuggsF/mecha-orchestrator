import os
import sys
import argparse
import json
import urllib.request
import urllib.error
import re
from typing import Tuple, Optional, List

try:
    from pydantic import BaseModel, Field
    HAS_PYDANTIC = True
except ImportError:
    HAS_PYDANTIC = False

# Configurar UTF-8 no stdout/stderr no Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

# Mapear Pydantic Models
if HAS_PYDANTIC:
    class BrainDecision(BaseModel):
        action: str  # "click", "wait", "type", "done"
        target_name: str
        relative_coords: Tuple[int, int]
        reason: str
        text_to_type: Optional[str] = None
else:
    class BrainDecision:
        def __init__(self, action, target_name, relative_coords, reason, text_to_type=None):
            self.action = action
            self.target_name = target_name
            self.relative_coords = relative_coords
            self.reason = reason
            self.text_to_type = text_to_type
        def model_dump(self):
            return {
                "action": self.action,
                "target_name": self.target_name,
                "relative_coords": self.relative_coords,
                "reason": self.reason,
                "text_to_type": self.text_to_type
            }

def clean_json_response(raw_text: str) -> str:
    """Extrai apenas a string JSON válida da resposta do LLM, limpando blocos de markdown e textos extras."""
    # Remove blocos de código markdown (```json ... ``` ou ``` ... ```)
    clean = re.sub(r"```[a-zA-Z]*", "", raw_text)
    # Tenta achar o primeiro '{' e o último '}'
    match = re.search(r"\{.*\}", clean, re.DOTALL)
    if match:
        return match.group(0).strip()
    return clean.strip()


def ask_ollama(prompt: str, model: str = "llama3", host: str = "127.0.0.1:11434") -> Optional[dict]:
    """Envia requisição HTTP POST ao Ollama local e retorna os dados brutos parseados do JSON."""
    url = f"http://{host}/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.2 # Baixa temperatura para respostas consistentes e determinísticas
        }
    }
    
    try:
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            url, 
            data=data, 
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=5.0) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            raw_response = res_data.get("response", "")
            
            # Limpar e parsear a decisão estruturada do JSON
            json_str = clean_json_response(raw_response)
            return json.loads(json_str)
    except Exception as e:
        # Silencia erros de rede para o fallback operar
        return None


def ask_gemini(prompt: str, api_key: str, image_base64: Optional[str] = None) -> Optional[dict]:
    """Envia requisição HTTP POST à API oficial do Google Gemini e retorna os dados de decisão (suporta multimodal)."""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    parts = [{"text": prompt}]
    if image_base64:
        parts.append({
            "inlineData": {
                "mimeType": "image/png",
                "data": image_base64
            }
        })
        
    payload = {
        "contents": [{
            "parts": parts
        }],
        "generationConfig": {
            "responseMimeType": "application/json",
            "temperature": 0.2
        }
    }
    
    try:
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=6.0) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            # Extrai o texto do Gemini
            raw_response = res_data["candidates"][0]["content"]["parts"][0]["text"]
            json_str = clean_json_response(raw_response)
            return json.loads(json_str)
    except Exception as e:
        return None


def compute_next_action(goal: str, window_title: str, ocr_text: str, controls: List[dict], image_path: Optional[str] = None) -> BrainDecision:
    """
    Orquestra a tomada de decisão. Monta o prompt, consulta os LLMs (suporta análise de imagem multimodal) e executa fallback se offline.
    """
    # 1. Montagem do prompt sistêmico
    prompt = f"""Você é o cérebro cognitivo do MECHA SDK Claw, um agente automatizado de interação com o Windows.
Sua tarefa é decidir a próxima ação (clicar, esperar, digitar ou terminar) com base nos elementos visíveis na janela do usuário para cumprir a meta especificada.

META DO OPERADOR HUMANO: "{goal}"
JANELA EM FOCO ATIVA: "{window_title}"

CONTROLES NATIVOS DA JANELA (Win32):
{json.dumps(controls, indent=2) if controls else "Nenhum controle Win32 detectado."}

TEXTO EXTRAÍDO DA TELA (OCR):
"{ocr_text if ocr_text else "Nenhum texto identificado."}"

REGRAS DE RESPOSTA (ESTRITAS):
1. Você deve responder EXCLUSIVAMENTE com uma estrutura JSON contendo a próxima ação lógica.
2. Não adicione textos extras, introduções, justificativas fora do JSON ou blocos markdown adicionais.
3. Se o objetivo foi totalmente cumprido, retorne "action": "done".
4. Se você precisa clicar em um texto/botão específico, retorne "action": "click", indique o "target_name" do botão/texto e forneça as coordenadas "relative_coords" [x, y] centrais dele.
5. Se você precisa digitar algo em um campo de texto/input, retorne "action": "type", indique o "target_name", as coordenadas "relative_coords" [x, y] dele, e preencha "text_to_type" com a string a ser digitada.
6. Se precisar esperar um carregamento ou processamento, retorne "action": "wait".

FORMATO JSON ESPERADO (PARA CLICK):
{{
  "action": "click",
  "target_name": "nome_do_botao_ou_texto",
  "relative_coords": [x, y],
  "reason": "Justificativa curta da escolha."
}}

FORMATO JSON ESPERADO (PARA TYPE):
{{
  "action": "type",
  "target_name": "nome_do_campo",
  "relative_coords": [x, y],
  "text_to_type": "texto a digitar aqui",
  "reason": "Justificativa curta da escolha."
}}
"""

    decision_data = None
    
    # 2. Tentar API Gemini se chave estiver disponível
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key:
        image_base64 = None
        if image_path and os.path.exists(image_path):
            import base64
            try:
                with open(image_path, "rb") as img_file:
                    image_base64 = base64.b64encode(img_file.read()).decode("utf-8")
            except Exception as e:
                print(f"  [Brain] Erro ao codificar imagem: {e}")
                
        decision_data = ask_gemini(prompt, api_key, image_base64)
        
    # 3. Tentar Ollama local se Gemini falhar ou estiver sem chave
    if not decision_data:
        decision_data = ask_ollama(prompt)
        
    # 4. Processar decisão ou executar Engine de Fallback Determinístico
    if decision_data and isinstance(decision_data, dict):
        try:
            # Valida chaves mínimas obrigatórias
            action = decision_data.get("action", "wait")
            target = decision_data.get("target_name", "none")
            coords = decision_data.get("relative_coords", [0, 0])
            reason = decision_data.get("reason", "IA Decision")
            text_to_type = decision_data.get("text_to_type", None)
            
            # Garante que coords seja tupla de ints
            tuple_coords = (int(coords[0]), int(coords[1]))
            
            if HAS_PYDANTIC:
                return BrainDecision(action=action, target_name=target, relative_coords=tuple_coords, reason=reason, text_to_type=text_to_type)
            else:
                return BrainDecision(action, target, tuple_coords, reason, text_to_type)
        except Exception:
            pass # Falha de parseamento de dados do LLM, cai no fallback

    # --- ENGINE DETERMINÍSTICA DE FALLBACK (OFFLINE) ---
    goal_words = goal.lower().split()
    target_coord = (0, 0)
    target_name = "none"
    reason = "Fallback determinístico: Primeiro controle nativo selecionado."
    action = "wait"
    
    # Tenta achar primeiro controle que atenda
    if controls:
        action = "click"
        ctrl = controls[0]
        bounds = ctrl.get("relative_bounds", (0, 0, 0, 0))
        cx = bounds[0] + (bounds[2] - bounds[0]) // 2
        cy = bounds[1] + (bounds[3] - bounds[1]) // 2
        target_coord = (cx, cy)
        target_name = ctrl.get("type", "button")
    
    # Se achamos, retorna o clique do fallback
    if HAS_PYDANTIC:
        return BrainDecision(action=action, target_name=target_name, relative_coords=target_coord, reason=reason, text_to_type=None)
    else:
        return BrainDecision(action, target_name, target_coord, reason, None)


def run_test_brain() -> bool:
    print("[*] Iniciando teste do Motor Cognitivo (claw_brain.py)...")
    
    # Roda uma decisão mockada com LLMs simulados offline
    goal = "clique no botao Login"
    window = "Opera - Login Portal"
    ocr = "Digite seu usuario\nLogin\nCadastre-se"
    controls = [{"type": "button", "relative_bounds": (100, 50, 180, 75)}]
    
    # Como os LLMs estarão offline em builds normais de CI, ele deve reverter para o fallback com sucesso
    print("[*] Computando próxima ação...")
    decision = compute_next_action(goal, window, ocr, controls)
    
    dec_dict = decision.model_dump() if hasattr(decision, 'model_dump') else decision.model_dump() if HAS_PYDANTIC else decision.model_dump()
    print(f" [+] Decisão gerada: {dec_dict}")
    
    # O fallback deve ter decidido clicar no controle [100, 50, 180, 75] -> centro (140, 62)
    if dec_dict["action"] == "click" and dec_dict["relative_coords"] == (140, 62):
        print("[+] Teste do Motor Cognitivo concluído com sucesso!")
        return True
    else:
        print("[!] Falha no teste de fallback cognitivo.")
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MECHA Claw Cognitive Brain Engine")
    parser.add_argument("--test-brain", action="store_true", help="Roda o teste unitário cognitivo")
    args = parser.parse_args()
    
    if args.test_brain:
        success = run_test_brain()
        sys.exit(0 if success else 1)
    else:
        parser.print_help()
