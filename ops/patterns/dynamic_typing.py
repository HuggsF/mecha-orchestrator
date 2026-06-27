import os
import sys
import re
import yaml
import argparse
from typing import Dict, Tuple




try:
    from pydantic import BaseModel, Field, field_validator
    HAS_PYDANTIC = True
except ImportError:
    HAS_PYDANTIC = False
    print("Warning: Pydantic is not installed. Using fallback validation logic.")

# Mapeamento de emojis para otimizacao de tokens
EMOJI_VOCAB = {
    "pipeline": "🚀",
    "database": "🌌",
    "security": "🛡️",
    "hardware": "🕹️",
    "documentation": "📓",
    "architecture": "🕸️",
    "testing": "🧪"
}

# --- fallback Pydantic classes se nao estiver disponivel ---
if HAS_PYDANTIC:
    class Frontmatter(BaseModel):
        project_name: str
        conversation_id: str
        date: str
        emoji_rail: str

        @field_validator('emoji_rail')
        @classmethod
        def check_rail(cls, v: str) -> str:
            v = str(v)
            if "➔" not in v:
                raise ValueError("O emoji_rail deve conter elementos separados por '➔' (ex: 📓 ➔ 🧬 ➔ 💻)")
            return v

    class PlanData(BaseModel):
        frontmatter: Frontmatter
        goal_description: str
        user_review_notes: str
        proposed_changes_content: str
        automated_tests_commands: str
        manual_verification_steps: str

    class EventEnvelope(BaseModel):
        topic: str
        sender: str
        timestamp: int
        payload: dict
else:
    class FrontmatterFallback:
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)
            if "emoji_rail" in kwargs and "➔" not in str(kwargs["emoji_rail"]):
                raise ValueError("O emoji_rail deve conter elementos separados por '➔'")
    
    class PlanDataFallback:
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)

    class EventEnvelopeFallback:
        def __init__(self, **kwargs):
            for k in ("topic", "sender", "timestamp", "payload"):
                if k not in kwargs:
                    raise ValueError(f"Campo obrigatorio ausente: {k}")
            self.topic = str(kwargs["topic"])
            self.sender = str(kwargs["sender"])
            self.timestamp = int(kwargs["timestamp"])
            self.payload = dict(kwargs["payload"])


def validate_event_envelope(data: dict) -> Tuple[bool, str]:
    try:
        if HAS_PYDANTIC:
            EventEnvelope(**data)
        else:
            EventEnvelopeFallback(**data)
        return True, "Envelope validado com sucesso."
    except Exception as e:
        return False, str(e)



# AST Validation: Verifica hierarquia de titulos Markdown (H1 -> H2 -> H3 sem saltar niveis)
def validate_headings_ast(content: str) -> Tuple[bool, str]:
    lines = content.splitlines()
    headings = []
    
    # Ignora blocos de codigo code fence ao procurar headings
    in_code_block = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue
            
        if stripped.startswith("#"):
            parts = stripped.split(" ", 1)
            if parts[0] and all(c == "#" for c in parts[0]):
                level = len(parts[0])
                headings.append((level, stripped))
                
    # Valida hierarquia: nao podemos saltar niveis (ex: H1 -> H3 sem H2)
    last_level = 0
    for level, text in headings:
        if level > last_level + 1:
            return False, f"Erro AST: Pulo de hierarquia detectado (H{last_level} para H{level}) na linha: '{text}'"
        last_level = level
        
    return True, "Estrutura AST de titulos validada com sucesso."


# Parse de Markdown com YAML Frontmatter
def parse_markdown_with_frontmatter(file_path: str) -> Tuple[Dict, str]:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Arquivo nao encontrado: {file_path}")
        
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Match YAML Frontmatter
    frontmatter_match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)', content, re.DOTALL)
    if not frontmatter_match:
        return {}, content
        
    frontmatter_yaml = frontmatter_match.group(1)
    body_content = frontmatter_match.group(2)
    
    try:
        metadata = yaml.safe_load(frontmatter_yaml)
    except Exception as e:
        raise ValueError(f"Erro ao parsear YAML do Frontmatter: {e}")
        
    return metadata, body_content


# Compressao de tokens usando o dicionario de emojis
def compress_tokens(text: str) -> str:
    compressed = text
    for word, emoji in EMOJI_VOCAB.items():
        # Substitui a palavra pelo emoji de forma case-insensitive
        pattern = re.compile(re.escape(word), re.IGNORECASE)
        compressed = pattern.sub(emoji, compressed)
    return compressed


# Descompressao de emojis de volta para palavras
def decompress_tokens(text: str) -> str:
    decompressed = text
    for word, emoji in EMOJI_VOCAB.items():
        decompressed = decompressed.replace(emoji, word)
    return decompressed


# Execucao principal de validacao
def run_validation(file_path: str) -> bool:
    print(f"[*] Carregando arquivo para validacao: {file_path}")
    metadata, body = parse_markdown_with_frontmatter(file_path)
        
    if not metadata:
        raise ValueError("Erro de validacao: Frontmatter YAML nao encontrado no topo do arquivo.")
        
    print("[*] Validando Frontmatter...")
    if HAS_PYDANTIC:
        Frontmatter(**metadata)
    else:
        FrontmatterFallback(**metadata)
    print("[+] Frontmatter validado com sucesso!")
            
    print("[*] Validando hierarquia AST de titulos...")
    success, msg = validate_headings_ast(body)
    if not success:
        raise ValueError(msg)
    print(f"[+] {msg}")
    
    # Demonstra compressao semantica de tokens
    compressed = compress_tokens(body[:200])
    print("[*] Amostra de compressao semantica de tokens (Emoji Rails):")
    print(f"    Original: {body[:100].strip()}...")
    print(f"    Comprimido: {compressed.strip()}...")
    
    print("[+] VALIDACAO COMPLETA: Arquivo 100% conforme!")
    return True


if __name__ == "__main__":
    # Forcar UTF-8 no stdout/stderr no Windows
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    parser = argparse.ArgumentParser(description="MECHA Dynamic Typing & AST Validator CLI")
    parser.add_argument("--validate", type=str, help="Caminho do arquivo Markdown a ser validado")
    parser.add_argument("--compress", type=str, help="Texto a ser comprimido em tokens emoji")
    parser.add_argument("--decompress", type=str, help="Texto contendo emojis a ser descomprimido")
    
    args = parser.parse_args()
    
    if args.validate:
        try:
            success = run_validation(args.validate)
            sys.exit(0 if success else 1)
        except Exception as e:
            print(f"[!] FALHA CRITICA DE CONTRATO (Let It Fail): {e}", file=sys.stderr)
            import traceback
            traceback.print_exc()
            sys.exit(1)
    elif args.compress:
        print(compress_tokens(args.compress))
    elif args.decompress:
        print(decompress_tokens(args.decompress))
    else:
        parser.print_help()
