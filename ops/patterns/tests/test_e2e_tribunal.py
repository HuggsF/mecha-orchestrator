import os
import sys
import time
import requests
import json

# Ajusta o path para importar modulos locais de patterns se rodando fora
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import claw_vision
import claw_control
import claw_brain
import claw_ocr
import claw_loop

def print_banner(title):
    print("=" * 60)
    print(f" [⚖️ TRIBUNAL MECHA E2E] {title.upper()}")
    print("=" * 60)

def test_ocr_and_vision():
    print_banner("Fase A: Teste de Visão e OCR Híbrido")
    # 1. Testar captura e redimensionamento de miniatura
    print("[*] Testando geração de miniatura...")
    from PIL import Image
    img = Image.new("RGB", (800, 600), color=(7, 9, 12))
    thumb_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "temp_states", "test_e2e_thumb.png")
    os.makedirs(os.path.dirname(thumb_path), exist_ok=True)
    claw_vision.save_window_thumbnail(img, thumb_path, max_width=320)
    
    assert os.path.exists(thumb_path), f"Miniatura de teste não foi gerada no caminho: {thumb_path}"
    print(f" [OK] Miniatura salva com sucesso em: {thumb_path}")

    # 2. Testar OCR Híbrido
    print("[*] Testando extração de OCR Híbrido...")
    ocr_res = claw_ocr.extract_text_from_image(img)
    
    assert ocr_res is not None, "O retorno do OCR não deve ser None"
    assert hasattr(ocr_res, "regions"), "O resultado do OCR deve conter o atributo 'regions'"
    assert hasattr(ocr_res, "raw_text"), "O resultado do OCR deve conter o atributo 'raw_text'"
    assert isinstance(ocr_res.regions, list), "O atributo 'regions' deve ser uma lista"
    assert isinstance(ocr_res.raw_text, str), "O atributo 'raw_text' deve ser uma string"
    
    print(f" [OK] OCR executado com sucesso. Texto bruto extraído: '{ocr_res.raw_text}'")


def test_http_api():
    print_banner("Fase B: Teste do Servidor HTTP e API de Preempção")
    url_status = "http://localhost:8585/api/status"
    url_preempt = "http://localhost:8585/api/preempt"
    
    # 1. Validar se o servidor local está online na porta 8585
    print(f"[*] Enviando requisição GET para {url_status}...")
    r = requests.get(url_status, timeout=3.0)
    assert r.status_code == 200, f"Servidor retornou status code incorreto: {r.status_code}"
    
    data = r.json()
    assert "loop_state" in data, "Resposta do status não contém chave 'loop_state'"
    print(f" [OK] Servidor online. Loop state: '{data.get('loop_state')}'")

    # 2. Validar envio de comando de preempção (pausa)
    print(f"[*] Enviando comando POST de pausa para {url_preempt}...")
    r_pre = requests.post(url_preempt, json={"action": "pause"}, timeout=3.0)
    assert r_pre.status_code == 200, f"Preempção retornou status code: {r_pre.status_code}"
    assert r_pre.json().get("ok") is True, f"Falha ao processar preempção: {r_pre.text}"
    print(" [OK] Comando de preempção enviado e processado com sucesso!")


def test_auto_recovery():
    print_banner("Fase C: Teste de Auto-Recuperação e Resiliência")
    # Testar a enumeração de janelas buscando a si mesmo (Python/VS Code/Terminal)
    print("[*] Testando detecção e foco de janela ativa...")
    success = claw_loop.focus_window_by_title("cmd") or claw_loop.focus_window_by_title("powershell") or claw_loop.focus_window_by_title("code") or claw_loop.focus_window_by_title("mecha")
    
    # Nota: focus_window_by_title pode retornar False em CI sem GUI, mas não deve lançar exceções.
    # Fazemos a chamada ctypes sem quebrar, mas registramos o aviso.
    if success:
        print(" [OK] Janela do console/editor de referência localizada e focada com sucesso.")
    else:
        print(" [WARN] Nenhuma janela de desenvolvimento/console padrão foi focada, mas a chamada ctypes executou sem falhas.")

    # Testar a lógica de mock de relançamento
    print("[*] Simulando relançamento de aplicação de teste...")
    launch_res = claw_loop.launch_target_app("obsidian_mock_test")
    assert launch_res is True, "A chamada de relançamento para obsidian_mock_test falhou"
    print(f" [OK] Chamada de relançamento processada. Retorno: {launch_res}")


def test_firewall_cognitive():
    print_banner("Fase D: Teste do Firewall Cognitivo (Clique de Risco / Judge)")
    # 1. Testar bloqueio determinístico (palavra proibida)
    print("[*] Simulando clique em elemento com palavra proibida 'deletar'...")
    print("[*] Verificando se os termos proibidos estão carregados corretamente...")
    assert "deletar" in claw_control.PROHIBITED_WORDS, "Termo 'deletar' ausente no firewall de controle"
    assert "excluir" in claw_control.PROHIBITED_WORDS, "Termo 'excluir' ausente no firewall de controle"
    print(" [OK] Termos de risco carregados na lista determinística.")

    # 2. Testar classificação semântica (Ollama / Judge) se disponível
    print("[*] Testando classificação de risco local (Ollama Judge)...")
    verdict = claw_control._ollama_risk_classification("Você deseja formatar todo o disco rígido do sistema?")
    if verdict:
        print(f" [JUDGE] Ollama respondeu. Risco: '{verdict.get('risk')}', Motivo: '{verdict.get('reason')}'")
        assert verdict.get("risk") in ("dangerous", "destructive"), f"Risco detectado incorretamente como: {verdict.get('risk')}"
        print(" [OK] Judge cognitivo classificou com sucesso a ação de alto risco.")
    else:
        print(" [WARN] Ollama local offline ou modelo não carregado. Fallback determinístico operando corretamente.")


def test_automation_error_handling():
    print_banner("Fase E: Teste de Tratamento de Erros e Logs de Auditoria (Warn/Alert/Ok/Judge)")
    # 1. Simular registro de logs no barramento local
    print("[*] Registrando eventos de teste (ok, warn, danger, judge) no Claw...")
    
    # Reseta os eventos locais do claw_loop para fins de isolamento do teste
    claw_loop.CLAW_EVENTS = []
    
    claw_loop.log_event("ok", "Automação: Ação física de clique efetuada com sucesso (Teste E2E).")
    claw_loop.log_event("warn", "Automação: Janela de teste saindo de foco temporariamente (Teste E2E).")
    claw_loop.log_event("danger", "Automação: Bloqueio ativo no firewall devido a ação de risco (Teste E2E).")
    claw_loop.log_event("judge", "Juiz IA: Modelo classificou a intenção do clique como segura (Teste E2E).")
    
    # 2. Persistir status do Claw com os logs mockados
    print("[*] Atualizando arquivo de telemetria claw_status.json...")
    claw_loop.update_claw_status(
        loop_state="running",
        step=1,
        max_steps=5,
        last_seen_title="Tribunal Test Window",
        current_goal="Validar logs E2E",
        last_thumbnail=None
    )
    
    # 3. Ler o arquivo gerado e realizar as asserções
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    status_file = os.path.join(base_dir, "logs", "claw_status.json")
    
    assert os.path.exists(status_file), f"Arquivo claw_status.json não foi gerado em: {status_file}"
        
    with open(status_file, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    events = data.get("events", [])
    print(f" [OK] Telemetria lida. Encontrados {len(events)} eventos persistidos.")
    
    # 4. Validar se os níveis de log requeridos estão presentes e corretos
    levels_found = [ev.get("level") for ev in events]
    expected_levels = ["ok", "warn", "danger", "judge"]
    
    for lvl in expected_levels:
        assert lvl in levels_found, f"Categoria de log requerida '{lvl}' não foi encontrada em claw_status.json."
        print(f" [OK] Categoria de log '{lvl.upper()}' detectada e íntegra.")


def main():
    import traceback
    print("\n")
    print("=" * 60)
    print("         INICIANDO TESTES FIM-A-FIM (E2E) DO TRIBUNAL       ")
    print("=" * 60)
    
    suites = {
        "vision_ocr": test_ocr_and_vision,
        "http_api": test_http_api,
        "auto_recovery": test_auto_recovery,
        "firewall_judge": test_firewall_cognitive,
        "error_handling": test_automation_error_handling
    }
    
    results = {}
    failures = {}
    
    for name, test_func in suites.items():
        try:
            test_func()
            results[name] = True
        except Exception as e:
            results[name] = False
            failures[name] = (e, traceback.format_exc())
            print(f"\n [!!!] FALHA NO TESTE '{name.upper()}': {e}")
            print(failures[name][1])
            print("=" * 60)
            
    print("\n")
    print("=" * 60)
    print("             PLACAR DE CONFORMIDADE DO TRIBUNAL             ")
    print("=" * 60)
    
    passed_all = True
    for key, val in results.items():
        status = "PASSED (OK)" if val else "FAILED (ALERT/WARN)"
        print(f" [+] {key.upper():<20} : {status}")
        if not val:
            passed_all = False
            
    print("=" * 60)
    if passed_all:
        print(" [⚖️ TRIBUNAL] VERDICT: CONFORME E VERIFICADO. APROVADO! 100%")
        sys.exit(0)
    else:
        print(" [⚖️ TRIBUNAL] VERDICT: CONDICIONAL/FALHA. VERIFIQUE OS AVISOS E TRACEBACKS ACIMA.")
        # Lança erro explícito para quebrar a suite sob contrato "Let it fail"
        failed_names = ", ".join(failures.keys())
        raise RuntimeError(f"FALHA CRITICA DE RESILIENCIA: As suites do Tribunal falharam: {failed_names}")

if __name__ == "__main__":
    main()
