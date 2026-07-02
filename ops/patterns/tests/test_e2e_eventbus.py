import os
import sys
import time
import asyncio
import threading
import requests
import json
import socket

# Configurar UTF-8 no stdout/stderr no Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

# Ajusta o path para importar modulos locais
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from telegram_bot import app
import uvicorn
from websockets.sync.client import connect

def get_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]

def run_server(port):
    # Configura o uvicorn para rodar silencioso
    config = uvicorn.Config(app, host="127.0.0.1", port=port, log_level="warning")
    server = uvicorn.Server(config)
    
    # Inicializa loop próprio da thread
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        loop.run_until_complete(server.serve())
    except Exception as e:
        print(f"Erro no servidor de testes: {e}")

def test_eventbus_e2e():
    print("============================================================")
    print("        INICIANDO TESTE E2E DO EVENT BUS DO MECHA           ")
    print("============================================================")
    
    port = get_free_port()
    
    # Executa o servidor em segundo plano
    srv_thread = threading.Thread(target=run_server, args=(port,), daemon=True)
    srv_thread.start()
    
    # Aguarda o binding do servidor
    time.sleep(2.0)
    
    base_url = f"http://127.0.0.1:{port}"
    ws_url = f"ws://127.0.0.1:{port}/ws/bus"
    
    try:
        # 1. Testar endpoint REST de falha (Assinatura malformada)
        print("[*] Testando validação de envelope malformado (REST)...")
        malformed = {"topic": "test", "sender": "test_agent"}
        resp = requests.post(f"{base_url}/api/bus/publish", json=malformed)
        assert resp.status_code == 400, f"Esperava 400, obteve {resp.status_code}"
        print(" [OK] Rejeição de envelope inválido validada.")

        # 2. Testar endpoint REST de sucesso (Envelope válido)
        print("[*] Testando publicação de envelope válido (REST)...")
        valid_event = {
            "topic": "node.select",
            "sender": "test_suite",
            "timestamp": int(time.time() * 1000),
            "payload": {"node_id": "dashboard", "title": "Dashboard Admin"}
        }
        resp = requests.post(f"{base_url}/api/bus/publish", json=valid_event)
        assert resp.status_code == 200, f"Esperava 200, obteve {resp.status_code}"
        print(" [OK] Publicação REST validada com sucesso.")

        # 3. Testar WebSocket (Inscrição e Transmissão)
        print("[*] Testando WebSocket subscription e broadcast...")
        with connect(ws_url) as ws_sub:
            # Envia assinatura nos tópicos
            ws_sub.send(json.dumps({
                "action": "subscribe",
                "topics": ["node.select"]
            }))
            time.sleep(0.5)
            
            with connect(ws_url) as ws_pub:
                valid_event_ws = {
                    "topic": "node.select",
                    "sender": "ws_publisher",
                    "timestamp": int(time.time() * 1000),
                    "payload": {"node_id": "login", "title": "Login Page"}
                }
                ws_pub.send(json.dumps({
                    "action": "publish",
                    "event": valid_event_ws
                }))
                
                # Recebe a mensagem transmitida pelo barramento no assinante
                time.sleep(0.5)
                received_raw = ws_sub.recv()
                received = json.loads(received_raw)
                assert received.get("topic") == "node.select"
                assert received.get("sender") == "ws_publisher"
                print(" [OK] Transmissão WebSocket de ponta a ponta validada.")

        # 4. Testar polling REST e buffer circular
        print("[*] Testando polling REST e persistência no buffer...")
        resp = requests.get(f"{base_url}/api/bus/poll?since=0")
        assert resp.status_code == 200, f"Esperava 200, obteve {resp.status_code}"
        events = resp.json().get("events", [])
        
        # O buffer deve conter tanto a mensagem do REST quanto do WS
        assert len(events) >= 2, f"Esperava ao menos 2 eventos, obteve {len(events)}"
        topics_found = [e.get("topic") for e in events]
        assert "node.select" in topics_found
        print(" [OK] Polling REST e buffer circular validados.")
        
        print("\n============================================================")
        print(" [⚖️ EVENT BUS E2E] VERDICT: APROVADO! 100% SUCESSO.")
        print("============================================================")
        return True
    except Exception as e:
        print(f"\n [ALERT] Erro na suite de testes do EventBus: {e}")
        return False

if __name__ == "__main__":
    success = test_eventbus_e2e()
    sys.exit(0 if success else 1)
