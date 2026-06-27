import os
import json
import base64
import hmac
import hashlib
import pytest
from unittest.mock import patch, MagicMock

# Add patterns to sys path to allow importing amanda_teams_bot
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from amanda_teams_bot import (
    _safe_chat_id, clean_teams_mention, verify_teams_signature,
    _read_json, _atomic_write_json, health, handle_task_command
)

def test_safe_chat_id_valid():
    with patch.dict(os.environ, {"TELEGRAM_CHAT_ID": "12345"}):
        assert _safe_chat_id() == 12345

def test_safe_chat_id_invalid():
    with patch.dict(os.environ, {"TELEGRAM_CHAT_ID": "invalid"}):
        assert _safe_chat_id() == 0

def test_clean_teams_mention():
    text = '<at id="0">Amanda</at> Please help'
    assert clean_teams_mention(text) == 'Please help'

def test_verify_teams_signature_no_secret():
    with patch("amanda_teams_bot.SHARED_SECRET", ""), \
         patch("amanda_teams_bot.ALLOW_INSECURE", False):
        assert not verify_teams_signature(b"body", "HMAC something")

def test_verify_teams_signature_valid():
    secret = base64.b64encode(b"secretkey").decode("utf-8")
    body = b"testbody"
    computed_hmac = hmac.new(b"secretkey", body, hashlib.sha256).digest()
    sig = "HMAC " + base64.b64encode(computed_hmac).decode("utf-8")
    
    with patch("amanda_teams_bot.SHARED_SECRET", secret):
        assert verify_teams_signature(body, sig)

def test_verify_teams_signature_invalid():
    secret = base64.b64encode(b"secretkey").decode("utf-8")
    body = b"testbody"
    sig = "HMAC invalid"
    
    with patch("amanda_teams_bot.SHARED_SECRET", secret):
        assert not verify_teams_signature(body, sig)

def test_read_json_not_exists(tmp_path):
    path = tmp_path / "not_exists.json"
    assert _read_json(str(path), {"default": 1}) == {"default": 1}

def test_atomic_write_and_read_json(tmp_path):
    path = tmp_path / "test.json"
    data = {"key": "value"}
    _atomic_write_json(str(path), data)
    assert _read_json(str(path), {}) == data

def test_health():
    with patch("amanda_teams_bot.rag_client", True), patch("amanda_teams_bot.orchestrator", True):
        res = health()
        assert res["status"] == "online"
        assert res["qdrant_connected"] is True
        assert res["orchestrator_loaded"] is True

def test_handle_task_command_add(tmp_path):
    tasks_file = tmp_path / "logs" / "amanda_tasks.json"
    tasks_md = tmp_path / "AMANDA_TASKS.md"
    
    # Needs to mock the paths in the module
    with patch("amanda_teams_bot.OPS_DIR", str(tmp_path)), \
         patch("amanda_teams_bot.BASE_DIR", str(tmp_path)), \
         patch("amanda_teams_bot.log_event_to_dashboard"), \
         patch("amanda_teams_bot.publish_to_bus"):
         
        res = handle_task_command("/task add Do something")
        assert "Tarefa registrada" in res["text"]
        
        with open(tasks_file) as f:
            tasks = json.load(f)
            assert len(tasks) == 1
            assert tasks[0]["description"] == "Do something"
            assert tasks[0]["status"] == "pending"

def test_handle_task_command_done(tmp_path):
    tasks_file = tmp_path / "logs" / "amanda_tasks.json"
    tasks_md = tmp_path / "AMANDA_TASKS.md"
    
    # Pre-populate tasks
    tasks_file.parent.mkdir(parents=True, exist_ok=True)
    with open(tasks_file, "w") as f:
        json.dump([{"id": 1, "description": "Test", "status": "pending"}], f)
    
    with patch("amanda_teams_bot.OPS_DIR", str(tmp_path)), \
         patch("amanda_teams_bot.BASE_DIR", str(tmp_path)), \
         patch("amanda_teams_bot.log_event_to_dashboard"), \
         patch("amanda_teams_bot.publish_to_bus"):
         
        res = handle_task_command("/task done 1")
        assert "marcada como concluída" in res["text"]
        
        with open(tasks_file) as f:
            tasks = json.load(f)
            assert tasks[0]["status"] == "completed"

def test_handle_task_command_clear(tmp_path):
    tasks_file = tmp_path / "logs" / "amanda_tasks.json"
    
    tasks_file.parent.mkdir(parents=True, exist_ok=True)
    with open(tasks_file, "w") as f:
        json.dump([
            {"id": 1, "description": "Test", "status": "completed"},
            {"id": 2, "description": "Test 2", "status": "pending"}
        ], f)
    
    with patch("amanda_teams_bot.OPS_DIR", str(tmp_path)), \
         patch("amanda_teams_bot.BASE_DIR", str(tmp_path)), \
         patch("amanda_teams_bot.log_event_to_dashboard"), \
         patch("amanda_teams_bot.publish_to_bus"):
         
        res = handle_task_command("/task clear")
        assert "limpa" in res["text"]
        
        with open(tasks_file) as f:
            tasks = json.load(f)
            assert len(tasks) == 1
            assert tasks[0]["id"] == 2
