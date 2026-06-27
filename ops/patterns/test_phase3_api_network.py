import os
import sys
import json
import time
import asyncio
import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from qdrant_client_helper import QdrantRAGClient
from squad_orchestrator import SquadOrchestrator, CostTracker
from qa_squad_runner import QASquadRunner
from code_squad_runner import CodeSquadRunner
from devops_squad_runner import DevOpsSquadRunner
import telegram_bot
import amanda_teams_bot
from agent_bus import BusMessage, MessageType

WORKSPACE = r"c:\Users\huggs\OneDrive\Documentos\workspace"

# =============================================================================
# QDRANT CLIENT HELPER TESTS
# =============================================================================

def test_qdrant_rag_client_workflow(tmp_path):
    import qdrant_client_helper
    orig_path = qdrant_client_helper.DB_PATH
    qdrant_client_helper.DB_PATH = str(tmp_path / "qdrant_db")
    try:
        client = QdrantRAGClient()
        pid = client.upsert("hello world doc", {"source": "test"})
        assert pid != ""
        hits = client.search("hello world", limit=1)
        assert len(hits) >= 1
        assert hits[0]["text"] == "hello world doc"
    finally:
        qdrant_client_helper.DB_PATH = orig_path

def test_qdrant_rag_client_errors(tmp_path):
    import qdrant_client_helper
    orig_path = qdrant_client_helper.DB_PATH
    qdrant_client_helper.DB_PATH = str(tmp_path / "qdrant_db")
    try:
        client = QdrantRAGClient()
        
        # Trigger upsert error
        def failing_upsert(*args, **kwargs):
            raise RuntimeError("failing upsert")
        client.client.upsert = failing_upsert
        assert client.upsert("text") == ""
        
        # Trigger search error
        def failing_query(*args, **kwargs):
            raise RuntimeError("failing query")
        client.client.query_points = failing_query
        assert client.search("query") == []

        # Trigger get_embedding error when self.model is not None
        if client.model:
            def failing_encode(*args, **kwargs):
                raise RuntimeError("failing encode")
            client.model.encode = failing_encode
            emb = client._get_embedding("text")
            assert len(emb) == client.vector_size
    finally:
        qdrant_client_helper.DB_PATH = orig_path

# =============================================================================
# SQUAD ORCHESTRATOR TESTS
# =============================================================================

def test_cost_tracker_errors(tmp_path):
    db = str(tmp_path / "cost_db.json")
    tracker = CostTracker(db)
    
    # Register call
    cost = tracker.register_call("meta-llama/llama-3.3-70b-instruct", "prompt", "response")
    assert cost > 0
    assert tracker.current_spend == cost

    # Trigger load corrupted db
    with open(db, "w") as f:
        f.write("{corrupt")
    tracker2 = CostTracker(db)
    assert tracker2.current_spend == 0.0

    # Trigger save spend write exception
    tracker3 = CostTracker(str(tmp_path / "subdir" / "db.json"))
    os.makedirs(str(tmp_path / "subdir"), exist_ok=True)
    os.chmod(str(tmp_path / "subdir"), 0o444)
    try:
        tracker3.current_spend = 100.0
        tracker3._save_spend()  # Should handle OSError/PermissionError gracefully
    finally:
        os.chmod(str(tmp_path / "subdir"), 0o777)

def test_squad_orchestrator_load_config_errors():
    orc = SquadOrchestrator(WORKSPACE)
    assert orc._load_json("nonexistent_json_file.json") == {}

def test_squad_orchestrator_openrouter_api_call():
    orc = SquadOrchestrator(WORKSPACE)
    # Test mock path
    orig_key = orc.api_key
    orc.api_key = "MOCK_KEY"
    res = asyncio.run(orc._call_openrouter("meta-llama/llama-3.3-70b-instruct", "system", "user", "Linus", "topic"))
    assert "Calculator" in res

    # Test limit exceeded
    orc.tracker.current_spend = 9999.0
    orc.api_key = "some_key"
    res_limit = asyncio.run(orc._call_openrouter("meta-llama/llama-3.3-70b-instruct", "system", "user", "Linus", "topic"))
    assert "[LIMIT EXCEEDED]" in res_limit
    orc.tracker.current_spend = 0.0
    orc.api_key = orig_key

def test_squad_orchestrator_run_workflow_errors():
    orc = SquadOrchestrator(WORKSPACE)
    with pytest.raises(ValueError):
        asyncio.run(orc.run_workflow("dev_squad", "code_workflows", "nonexistent_pipeline", {}))

# =============================================================================
# SQUAD RUNNERS TESTS
# =============================================================================

def test_squad_runners():
    qr = QASquadRunner(WORKSPACE)
    res_qa = asyncio.run(qr.run_qa_audit("def add(a, b): return a + b"))
    assert "qa_final_report" in res_qa

    cr = CodeSquadRunner(WORKSPACE)
    res_code = asyncio.run(cr.run_spec_driven_dev("Create calculator"))
    assert "implementation" in res_code

    dr = DevOpsSquadRunner(WORKSPACE)
    res_devops = asyncio.run(dr.run_devops_deploy("Deploy cluster"))
    assert "infra_plan" in res_devops

# =============================================================================
# TELEGRAM BOT & WEBHOOK ENDPOINTS
# =============================================================================

@pytest.fixture
def tg_client(tmp_path):
    import telegram_bot
    # Save original paths
    orig_base = telegram_bot.BASE_DIR
    orig_status = telegram_bot.STATUS_FILE
    orig_preempt = telegram_bot.PREEMPT_FILE
    
    # Override
    telegram_bot.BASE_DIR = str(tmp_path / "subdir_tg")
    telegram_bot.STATUS_FILE = str(tmp_path / "subdir_tg" / "logs" / "claw_status.json")
    telegram_bot.PREEMPT_FILE = str(tmp_path / "subdir_tg" / "logs" / "claw_preempt.json")
    os.makedirs(os.path.join(telegram_bot.BASE_DIR, "logs"), exist_ok=True)
    
    from telegram_bot import app
    yield TestClient(app)
    
    # Restore
    telegram_bot.BASE_DIR = orig_base
    telegram_bot.STATUS_FILE = orig_status
    telegram_bot.PREEMPT_FILE = orig_preempt

def test_telegram_bot_endpoints(tg_client, tmp_path):
    # api_health
    resp = tg_client.get("/api/health")
    assert resp.status_code == 200
    assert "product" in resp.json()

    # api_status
    resp = tg_client.get("/api/status")
    assert resp.status_code == 200

    # api_tasks management
    # Clear tasks first
    resp = tg_client.post("/api/tasks/clear")
    assert resp.status_code == 200
    
    # Get tasks
    resp = tg_client.get("/api/tasks")
    assert resp.status_code == 200
    assert resp.json() == []

    # Add task
    resp = tg_client.post("/api/tasks", json={"description": "Test Task"})
    assert resp.status_code == 200
    
    # Add task missing description
    resp = tg_client.post("/api/tasks", json={})
    assert resp.status_code == 400

    # Complete task
    resp = tg_client.post("/api/tasks/done", json={"id": 1})
    assert resp.status_code == 200
    
    # Complete task missing id
    resp = tg_client.post("/api/tasks/done", json={})
    assert resp.status_code == 400

    # api_preempt
    resp = tg_client.post("/api/preempt", json={"action": "click", "params": {"x": 1, "y": 2}})
    assert resp.status_code == 200
    
    # api_preempt missing action
    resp = tg_client.post("/api/preempt", json={})
    assert resp.status_code == 400

    # api_bus/publish and poll
    valid_event = {
        "topic": "node.select",
        "sender": "test_suite",
        "timestamp": int(time.time() * 1000),
        "payload": {"node_id": "dashboard", "title": "Dashboard Admin"}
    }
    resp = tg_client.post("/api/bus/publish", json=valid_event)
    assert resp.status_code == 200

    # Invalid publish
    resp = tg_client.post("/api/bus/publish", json={"topic": "invalid"})
    assert resp.status_code == 400

    # Invalid JSON publish
    resp = tg_client.post("/api/bus/publish", data="invalid_json")
    assert resp.status_code == 400

    resp = tg_client.get("/api/bus/poll?since=0")
    assert resp.status_code == 200
    assert len(resp.json()["events"]) >= 1

def test_telegram_bot_websocket(tg_client):
    valid_event = {
        "topic": "node.select",
        "sender": "test_suite",
        "timestamp": int(time.time() * 1000),
        "payload": {"node_id": "dashboard", "title": "Dashboard Admin"}
    }
    with tg_client.websocket_connect("/ws/bus") as ws:
        # Publish
        ws.send_json({"action": "publish", "event": valid_event})
        # Subscribe
        ws.send_json({"action": "subscribe", "topics": ["node.select"]})

def test_telegram_bot_helpers(tmp_path):
    orig_status = telegram_bot.STATUS_FILE
    telegram_bot.STATUS_FILE = str(tmp_path / "status.json")
    try:
        # log_event_to_dashboard coverage
        telegram_bot.log_event_to_dashboard("info", "test event info")
        
        # wait_for_preempt_processed coverage
        telegram_bot.send_preempt_command("click")
        with open(telegram_bot.PREEMPT_FILE, "r") as f:
            data = json.load(f)
        data["processed"] = True
        with open(telegram_bot.PREEMPT_FILE, "w") as f:
            json.dump(data, f)
        assert telegram_bot.wait_for_preempt_processed(timeout=1.0) is True
    finally:
        telegram_bot.STATUS_FILE = orig_status

def test_telegram_bot_main_polling():
    import requests
    orig_get = requests.get
    def intercepting_get(*args, **kwargs):
        url = args[0]
        if "getMe" in url:
            class DummyMeResp:
                status_code = 200
            return DummyMeResp()
        elif "getUpdates" in url:
            params = kwargs.get("params", {})
            if params.get("offset") == -1:
                class DummyClearResp:
                    status_code = 200
                return DummyClearResp()
            else:
                raise KeyboardInterrupt()
        class DummyFallbackResp:
            status_code = 200
        return DummyFallbackResp()
            
    requests.get = intercepting_get
    try:
        telegram_bot.main()
    finally:
        requests.get = orig_get

def test_telegram_bot_threads(tmp_path):
    # Mock send_message and wait_for_preempt_processed to avoid actual HTTP posts/timeouts
    orig_send = telegram_bot.send_message
    telegram_bot.send_message = lambda chat_id, text: None
    orig_wait = telegram_bot.wait_for_preempt_processed
    telegram_bot.wait_for_preempt_processed = lambda *a, **kw: True
    
    # Mock AwesomeBotsOrchestrator and QdrantRAGClient to avoid actual LLM and DB connections
    from types import ModuleType
    import sys
    
    fake_orch_mod = ModuleType("awesome_bots_orchestrator")
    class DummyOrchestrator:
        def __init__(self, workspace):
            self.workspace = workspace
        async def run_tribunal(self, topic):
            return {
                "warlock": "warlock text",
                "amanda": "amanda text",
                "shura": "[1] Approved"
            }
    fake_orch_mod.AwesomeBotsOrchestrator = DummyOrchestrator
    
    fake_rag_mod = ModuleType("qdrant_client_helper")
    class DummyRAGClient:
        def __init__(self, *args, **kwargs):
            pass
        def search(self, query, limit=3):
            return [{"score": 0.99, "text": "mocked text", "metadata": {}}]
    fake_rag_mod.QdrantRAGClient = DummyRAGClient
    
    orig_orch_mod = sys.modules.get("awesome_bots_orchestrator")
    orig_rag_mod = sys.modules.get("qdrant_client_helper")
    
    sys.modules["awesome_bots_orchestrator"] = fake_orch_mod
    sys.modules["qdrant_client_helper"] = fake_rag_mod
    
    try:
        # Run threads synchronously for testing/coverage
        telegram_bot.run_tribunal_thread(123, "Test topic")
        telegram_bot.run_rag_thread(123, "kafka")
        
        # Playbook test
        pb_folder = os.path.join(telegram_bot.BASE_DIR, "intelligence", "playbooks")
        os.makedirs(pb_folder, exist_ok=True)
        test_pb_path = os.path.join(pb_folder, "test_pb.md")
        with open(test_pb_path, "w", encoding="utf-8") as f:
            f.write("- click 10 20\n- type 'hello'\n- wait 1\n- set_goal 'test'\n- custom_cmd params\n")
        try:
            telegram_bot.run_playbook_thread(123, "test_pb")
        finally:
            if os.path.exists(test_pb_path):
                os.remove(test_pb_path)
    finally:
        telegram_bot.send_message = orig_send
        telegram_bot.wait_for_preempt_processed = orig_wait
        if orig_orch_mod:
            sys.modules["awesome_bots_orchestrator"] = orig_orch_mod
        else:
            sys.modules.pop("awesome_bots_orchestrator", None)
        if orig_rag_mod:
            sys.modules["qdrant_client_helper"] = orig_rag_mod
        else:
            sys.modules.pop("qdrant_client_helper", None)

# =============================================================================
# AMANDA TEAMS BOT WEBHOOK ENDPOINTS
# =============================================================================

@pytest.fixture
def teams_client(tmp_path):
    import amanda_teams_bot
    # Save original paths
    orig_base = amanda_teams_bot.BASE_DIR
    orig_ops = amanda_teams_bot.OPS_DIR
    
    # Override
    amanda_teams_bot.BASE_DIR = str(tmp_path / "subdir_teams")
    amanda_teams_bot.OPS_DIR = str(tmp_path / "subdir_teams" / "ops")
    os.makedirs(os.path.join(amanda_teams_bot.OPS_DIR, "logs"), exist_ok=True)
    
    from amanda_teams_bot import app
    yield TestClient(app)
    
    # Restore
    amanda_teams_bot.BASE_DIR = orig_base
    amanda_teams_bot.OPS_DIR = orig_ops

def test_amanda_teams_bot_endpoints(teams_client):
    import amanda_teams_bot
    orig_secret = amanda_teams_bot.SHARED_SECRET
    orig_allow = amanda_teams_bot.ALLOW_INSECURE
    amanda_teams_bot.SHARED_SECRET = "some_secret_key"
    amanda_teams_bot.ALLOW_INSECURE = False
    try:
        # health
        resp = teams_client.get("/health")
        assert resp.status_code == 200
        assert resp.json()["status"] == "online"

        # webhook post without auth (signature missing)
        resp = teams_client.post("/webhook/teams", json={"text": "hello"})
        assert resp.status_code == 401
    finally:
        amanda_teams_bot.SHARED_SECRET = orig_secret
        amanda_teams_bot.ALLOW_INSECURE = orig_allow

    # webhook post with auth or insecure mode enabled
    orig_allow = amanda_teams_bot.ALLOW_INSECURE
    amanda_teams_bot.ALLOW_INSECURE = True
    try:
        # Normal query RAG flow
        payload = {
            "type": "message",
            "text": "test query",
            "from": {"name": "User"}
        }
        resp = teams_client.post("/webhook/teams", json=payload)
        assert resp.status_code == 200

        # /task list command
        payload_task = {
            "type": "message",
            "text": "/task list",
            "from": {"name": "User"}
        }
        resp = teams_client.post("/webhook/teams", json=payload_task)
        assert resp.status_code == 200

        # /tribunal topic command
        payload_trib = {
            "type": "message",
            "text": "/tribunal Test topic",
            "from": {"name": "User"}
        }
        resp = teams_client.post("/webhook/teams", json=payload_trib)
        assert resp.status_code == 200

        # /dev spec-driven command
        payload_dev = {
            "type": "message",
            "text": "/dev spec-driven Calculator",
            "from": {"name": "User"}
        }
        resp = teams_client.post("/webhook/teams", json=payload_dev)
        assert resp.status_code == 200

        # /qa source code command
        payload_qa = {
            "type": "message",
            "text": "/qa source.py test.py",
            "from": {"name": "User"}
        }
        resp = teams_client.post("/webhook/teams", json=payload_qa)
        assert resp.status_code == 200

    finally:
        amanda_teams_bot.ALLOW_INSECURE = orig_allow

def test_amanda_teams_bot_helpers():
    import amanda_teams_bot
    # Call signature checks and clean functions directly for coverage
    assert amanda_teams_bot.clean_teams_mention("<at>Amanda</at> hello") == "hello"
    
    # hmac verification checks
    orig_secret = amanda_teams_bot.SHARED_SECRET
    amanda_teams_bot.SHARED_SECRET = "some_secret_key"
    try:
        # Check signature verify failing
        assert amanda_teams_bot.verify_teams_signature(b"body", "invalid_sig") is False
    finally:
        amanda_teams_bot.SHARED_SECRET = orig_secret

    # Mock background tasks functions
    amanda_teams_bot.run_async_tribunal("topic", 123)
    amanda_teams_bot.run_async_dev_squad("prompt", 123)
    amanda_teams_bot.run_async_qa_squad("src.py", "test.py", 123)


def test_swagger_endpoints(tg_client, teams_client):
    # Telegram Bot Swagger
    resp_docs = tg_client.get("/docs")
    assert resp_docs.status_code == 200
    assert "swagger-ui" in resp_docs.text.lower() or "redoc" in resp_docs.text.lower()

    resp_openapi = tg_client.get("/openapi.json")
    assert resp_openapi.status_code == 200
    schema = resp_openapi.json()
    assert "paths" in schema
    assert "/api/bus/publish" in schema["paths"]
    assert "components" in schema
    assert "schemas" in schema["components"]
    assert "EventPublishRequest" in schema["components"]["schemas"]
    assert "EventPublishResponse" in schema["components"]["schemas"]

    # Amanda Teams Bot Swagger
    resp_docs_teams = teams_client.get("/docs")
    assert resp_docs_teams.status_code == 200
    assert "swagger-ui" in resp_docs_teams.text.lower() or "redoc" in resp_docs_teams.text.lower()

    resp_openapi_teams = teams_client.get("/openapi.json")
    assert resp_openapi_teams.status_code == 200
    schema_teams = resp_openapi_teams.json()
    assert "paths" in schema_teams
    assert "/webhook/teams" in schema_teams["paths"]
    assert "components" in schema_teams
    assert "schemas" in schema_teams["components"]
    assert "TeamsWebhookRequest" in schema_teams["components"]["schemas"]
    assert "TeamsWebhookResponse" in schema_teams["components"]["schemas"]
    assert "503" in schema_teams["paths"]["/webhook/teams"]["post"]["responses"]


def test_qdrant_rag_client_coverage(tmp_path):
    import importlib
    import sys
    import qdrant_client_helper
    from qdrant_client_helper import QdrantRAGClient
    from unittest.mock import patch, mock_open, MagicMock

    # Redirect DB_PATH to a temporary path during reload to prevent locking existing database
    orig_join = os.path.join
    def fake_join_init(a, b, *args):
        if b == "qdrant_db":
            return str(tmp_path / "temp_qdrant_db_init")
        return orig_join(a, b, *args)

    def fake_join_st(a, b, *args):
        if b == "qdrant_db":
            return str(tmp_path / "temp_qdrant_db_st")
        return orig_join(a, b, *args)

    # 1. Test .env reading failure (lines 27-28)
    orig_exists = os.path.exists
    def fake_exists(path):
        if path.endswith(".env"):
            return True
        return orig_exists(path)

    with patch("os.path.join", fake_join_init):
        with patch("builtins.open", mock_open()) as mock_file:
            mock_file.side_effect = IOError("Mocked open failure")
            with patch("os.path.exists", fake_exists):
                importlib.reload(qdrant_client_helper)

    # 1.5. Test sentence_transformers loading failure (lines 55-57)
    mock_st_fail = MagicMock()
    mock_st_fail.SentenceTransformer.side_effect = RuntimeError("Mocked sentence transformer load error")
    sys.modules["sentence_transformers"] = mock_st_fail

    orig_mock_emb = os.environ.get("MECHA_FORCE_MOCK_EMBEDDINGS")
    if "MECHA_FORCE_MOCK_EMBEDDINGS" in os.environ:
        del os.environ["MECHA_FORCE_MOCK_EMBEDDINGS"]
    
    def fake_exists_no_env(path):
        if path.endswith(".env"):
            return False
        return orig_exists(path)

    try:
        with patch("os.path.exists", fake_exists_no_env):
            with patch("os.path.join", fake_join_st):
                importlib.reload(qdrant_client_helper)
        qdrant_client_helper.DB_PATH = str(tmp_path / "temp_qdrant_db_fail")
        client_fail = QdrantRAGClient()
        assert client_fail.model is None
        client_fail.client.close()
        del client_fail
    finally:
        if orig_mock_emb is not None:
            os.environ["MECHA_FORCE_MOCK_EMBEDDINGS"] = orig_mock_emb
        if "sentence_transformers" in sys.modules:
            del sys.modules["sentence_transformers"]

    # 2. Test sentence_transformers loading success (lines 46-54, 78) using a mock module in sys.modules
    mock_st = MagicMock()
    mock_model = MagicMock()
    mock_model.encode.return_value = MagicMock(tolist=lambda: [0.1] * 384)
    mock_st.SentenceTransformer.return_value = mock_model
    sys.modules["sentence_transformers"] = mock_st

    if "MECHA_FORCE_MOCK_EMBEDDINGS" in os.environ:
        del os.environ["MECHA_FORCE_MOCK_EMBEDDINGS"]

    try:
        with patch("os.path.exists", fake_exists_no_env):
            with patch("os.path.join", fake_join_st):
                importlib.reload(qdrant_client_helper)
            
        # Re-patch DB_PATH in helper to use temp dir
        qdrant_client_helper.DB_PATH = str(tmp_path / "temp_qdrant_db_st")
        client = QdrantRAGClient()
        assert client.model is not None
        emb = client._get_embedding("hello")
        assert len(emb) == client.vector_size
        client.client.close()
        del client
    finally:
        if orig_mock_emb is not None:
            os.environ["MECHA_FORCE_MOCK_EMBEDDINGS"] = orig_mock_emb
        if "sentence_transformers" in sys.modules:
            del sys.modules["sentence_transformers"]

    # Restore state by reloading with mock embeddings active
    def fake_join_restore(a, b, *args):
        if b == "qdrant_db":
            return str(tmp_path / "temp_qdrant_db_restore")
        return orig_join(a, b, *args)

    with patch("os.path.join", fake_join_restore):
        importlib.reload(qdrant_client_helper)

    qdrant_client_helper.DB_PATH = str(tmp_path / "temp_qdrant_db_final")
    client = QdrantRAGClient()

    # 3. Test already existing collection path (line 70)
    client._init_collection()

    # 4. Test collection initialization exception path (lines 71-72)
    def failing_get_collections(*args, **kwargs):
        raise RuntimeError("db error")
    client.client.get_collections = failing_get_collections
    client._init_collection()

    # 5. Test real embedding encode failure fallback (lines 76-80)
    class DummyModel:
        def encode(self, text):
            raise RuntimeError("encode fail")
    client.model = DummyModel()
    emb = client._get_embedding("hello")
    assert len(emb) == client.vector_size


def test_squad_orchestrator_coverage(tmp_path):
    from squad_orchestrator import SquadOrchestrator, CostTracker
    from unittest.mock import patch, mock_open
    import builtins

    # 1. CostTracker corrupt file (lines 59-63)
    db_file = tmp_path / "corrupt_cost.json"
    with open(db_file, "w") as f:
        f.write("corrupted json")
    tracker = CostTracker(str(db_file))
    assert tracker.current_spend == 0.0
    
    # Trigger Exception in CostTracker._save_spend (lines 62-63)
    tracker._save_spend()

    # 2. CostTracker save spend exception (lines 69-70)
    tracker_err = CostTracker(str(tmp_path / "nonexistent_dir" / "cost.json"))
    orig_open = builtins.open
    def fake_open(file, mode="r", *args, **kwargs):
        if "nonexistent_dir" in str(file) and "w" in mode:
            raise IOError("Mocked write error")
        return orig_open(file, mode, *args, **kwargs)
    with patch("builtins.open", fake_open):
        tracker_err._save_spend()

    # 3. SquadOrchestrator _load_json error (lines 121-122)
    orc = SquadOrchestrator(WORKSPACE)
    corrupt_squad_file = tmp_path / "corrupt_squad.json"
    with open(corrupt_squad_file, "w") as f:
        f.write("corrupt")
    orc._load_json(str(corrupt_squad_file))

    # 4. Mock responses for specific agent names (lines 211, 218, 225, 284)
    assert "ACUSAÇÃO" in orc._get_mock_response("Warlock", "topic")
    assert "DEFESA" in orc._get_mock_response("Amanda", "topic")
    assert "ARCHITECT" in orc._get_mock_response("Shura", "topic")
    assert "[MOCK]" in orc._get_mock_response("UnknownAgent", "topic")

    # 5. OpenRouter call with real key path simulation (lines 316-319)
    orc.api_key = "VALID_KEY"
    orc.tracker.current_spend = 0.0

    class DummyHTTPResponse:
        def raise_for_status(self):
            pass
        def json(self):
            return {
                "choices": [{
                    "message": {
                        "content": "Real OpenRouter Response"
                    }
                }]
            }

    with patch("requests.post", return_value=DummyHTTPResponse()):
        res = asyncio.run(orc._call_openrouter("meta-llama/llama-3.3-70b-instruct", "system", "user", "Linus", "topic"))
        assert res == "Real OpenRouter Response"
        assert orc.tracker.current_spend > 0.0

    # 6. SquadOrchestrator._load_api_key reading from .env file (lines 97-106)
    fake_workspace = tmp_path / "workspace"
    os.makedirs(fake_workspace / ".mecha" / "ops", exist_ok=True)
    with open(fake_workspace / ".mecha" / "ops" / ".env", "w") as f:
        f.write("OPENROUTER_API_KEY=ENV_FILE_KEY\n")
    orig_env_key = os.environ.get("OPENROUTER_API_KEY")
    if "OPENROUTER_API_KEY" in os.environ:
        del os.environ["OPENROUTER_API_KEY"]
    try:
        orc_env = SquadOrchestrator(str(fake_workspace))
        assert orc_env.api_key == "ENV_FILE_KEY"
        
        # Exception read (lines 104-106)
        def fake_open_err(file, mode="r", *args, **kwargs):
            if ".env" in str(file):
                raise IOError("Mocked env read error")
            return orig_open(file, mode, *args, **kwargs)
        with patch("builtins.open", fake_open_err):
            orc_env_err = SquadOrchestrator(str(fake_workspace))
            assert orc_env_err.api_key == "MOCK_KEY"
    finally:
        if orig_env_key is not None:
            os.environ["OPENROUTER_API_KEY"] = orig_env_key

    # 7. run_workflow circular dependency / bottleneck check (lines 366-367)
    circular_pipeline = {
        "circular_run": {
            "name": "Circular Workflow",
            "steps": [
                {
                    "step_id": 1,
                    "agent": "Linus",
                    "input_source": "step_2_output"
                },
                {
                    "step_id": 2,
                    "agent": "Kent Beck",
                    "input_source": "step_1_output"
                }
            ]
        }
    }
    orc.load_workflow_config = lambda name: circular_pipeline
    orc.load_squad_config = lambda name: {"Linus": {}, "Kent Beck": {}}

    with pytest.raises(RuntimeError) as exc_info:
        asyncio.run(orc.run_workflow("squad", "workflow", "circular_run", {}))
    assert "Gargalo de dependência detectado" in str(exc_info.value)


# =============================================================================
# COMPREHENSIVE BOT EDGE CASES & EXCEPTION PATHS COVERAGE
# =============================================================================

def test_telegram_bot_comprehensive(tmp_path):
    import telegram_bot
    import sys
    import requests
    import time
    import builtins
    import os
    from unittest.mock import patch
    from types import ModuleType
    true_orig_send_message = telegram_bot.send_message

    # 0. sys.frozen and dynamic_typing ImportError reload test (run first to avoid overriding coverage)
    import importlib
    orig_frozen = getattr(sys, "frozen", False)
    orig_executable = getattr(sys, "executable", None)
    orig_meipass = getattr(sys, "_MEIPASS", None)
    orig_dt = sys.modules.get("dynamic_typing")

    sys.frozen = True
    sys.executable = str(tmp_path / "main.exe")
    sys._MEIPASS = str(tmp_path / "_MEIPASS")
    os.makedirs(sys._MEIPASS, exist_ok=True)
    sys.modules["dynamic_typing"] = None

    try:
        importlib.reload(telegram_bot)
        assert telegram_bot.validate_event_envelope({}) == (True, "Fallback")
    finally:
        if orig_frozen is False:
            if hasattr(sys, "frozen"): del sys.frozen
        else:
            sys.frozen = orig_frozen
        if orig_executable is None:
            if hasattr(sys, "executable"): del sys.executable
        else:
            sys.executable = orig_executable
        if orig_meipass is None:
            if hasattr(sys, "_MEIPASS"): del sys._MEIPASS
        else:
            sys._MEIPASS = orig_meipass
        if orig_dt:
            sys.modules["dynamic_typing"] = orig_dt
        else:
            if "dynamic_typing" in sys.modules: del sys.modules["dynamic_typing"]
        importlib.reload(telegram_bot)

    # 1. _scrub_token coverage
    assert "bot***" in telegram_bot._scrub_token("bot12345:abc-123_xyz")

    # 2. EventHub WebSocket failures & dead connection removal
    class FakeWS:
        def __init__(self):
            self.closed = False
        async def send_json(self, event):
            raise RuntimeError("ws send error")

    fake_ws = FakeWS()
    hub = telegram_bot.EventHub()
    hub.subscribe(fake_ws)
    assert fake_ws in hub.connections

    orig_loop = telegram_bot._UVICORN_LOOP
    class FakeLoop:
        def is_running(self):
            return True

    orig_run_coroutine = asyncio.run_coroutine_threadsafe
    def fake_run_coroutine(coro, loop):
        raise RuntimeError("run_coroutine_threadsafe error")

    asyncio.run_coroutine_threadsafe = fake_run_coroutine
    telegram_bot._UVICORN_LOOP = FakeLoop()
    try:
        success, msg = hub.publish({"topic": "node.select", "sender": "test", "timestamp": 123, "payload": {}})
        assert success is True
        assert fake_ws not in hub.connections
    finally:
        asyncio.run_coroutine_threadsafe = orig_run_coroutine
        telegram_bot._UVICORN_LOOP = orig_loop

    # unsubscribe coverage
    hub.subscribe(fake_ws)
    hub.unsubscribe(fake_ws)
    assert fake_ws not in hub.connections

    # get_events coverage
    hub.buffer.append({"timestamp": 100})
    hub.buffer.append({"timestamp": 200})
    assert len(hub.get_events(150)) == 1

    # 3. select_working_token coverage
    orig_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    orig_huggies = os.environ.get("MECHAHUGGIES_BOT_TOKEN")
    orig_req_get = requests.get

    try:
        if "TELEGRAM_BOT_TOKEN" in os.environ: del os.environ["TELEGRAM_BOT_TOKEN"]
        if "MECHAHUGGIES_BOT_TOKEN" in os.environ: del os.environ["MECHAHUGGIES_BOT_TOKEN"]
        assert telegram_bot.select_working_token() == ""

        os.environ["TELEGRAM_BOT_TOKEN"] = "token1"
        class SuccessResp:
            status_code = 200
        requests.get = lambda url, **kw: SuccessResp()
        assert telegram_bot.select_working_token() == "token1"

        del os.environ["TELEGRAM_BOT_TOKEN"]
        os.environ["MECHAHUGGIES_BOT_TOKEN"] = "token2"
        assert telegram_bot.select_working_token() == "token2"

        os.environ["TELEGRAM_BOT_TOKEN"] = "token1"
        def fake_get_t1_t2(url, **kw):
            if "token1" in url:
                class FailResp:
                    status_code = 401
                return FailResp()
            return SuccessResp()
        requests.get = fake_get_t1_t2
        assert telegram_bot.select_working_token() == "token2"

        def failing_get(*args, **kwargs):
            raise RuntimeError("Request failed")
        requests.get = failing_get
        os.environ["TELEGRAM_BOT_TOKEN"] = "token1"
        assert telegram_bot.select_working_token() in ("token1", "token2")
    finally:
        requests.get = orig_req_get
        if orig_token is not None:
            os.environ["TELEGRAM_BOT_TOKEN"] = orig_token
        else:
            if "TELEGRAM_BOT_TOKEN" in os.environ: del os.environ["TELEGRAM_BOT_TOKEN"]
        if orig_huggies is not None:
            os.environ["MECHAHUGGIES_BOT_TOKEN"] = orig_huggies
        else:
            if "MECHAHUGGIES_BOT_TOKEN" in os.environ: del os.environ["MECHAHUGGIES_BOT_TOKEN"]

    # 4. send_photo coverage
    temp_photo = tmp_path / "photo.jpg"
    with open(temp_photo, "w") as f:
        f.write("fake photo")

    orig_post = requests.post
    posted_args = []
    def fake_post(url, **kwargs):
        posted_args.append((url, kwargs))
        class Dummy:
            status_code = 200
        return Dummy()

    requests.post = fake_post
    try:
        telegram_bot.send_photo(12345, str(temp_photo), "Hello photo")
        assert len(posted_args) == 1
        assert posted_args[0][0].endswith("/sendPhoto")

        def fail_post(url, **kwargs):
            raise RuntimeError("connection error")
        requests.post = fail_post
        telegram_bot.send_photo(12345, str(temp_photo), "Hello photo")
    finally:
        requests.post = orig_post

    # 5. log_event_to_dashboard error recovery and write exception
    orig_status_file = telegram_bot.STATUS_FILE
    telegram_bot.STATUS_FILE = str(tmp_path / "corrupt_status.json")
    try:
        with open(telegram_bot.STATUS_FILE, "w") as f:
            f.write("corrupt")
        telegram_bot.log_event_to_dashboard("info", "test recover")
        with open(telegram_bot.STATUS_FILE, "r") as f:
            data = json.load(f)
        assert len(data["events"]) == 1

        telegram_bot.STATUS_FILE = str(tmp_path / "nonexistent_dir" / "status.json")
        telegram_bot.log_event_to_dashboard("info", "test write err")
    finally:
        telegram_bot.STATUS_FILE = orig_status_file

    # 6. wait_for_preempt_processed coverage
    orig_preempt = telegram_bot.PREEMPT_FILE
    telegram_bot.PREEMPT_FILE = str(tmp_path / "preempt_wait.json")
    try:
        assert telegram_bot.wait_for_preempt_processed(timeout=0.1) is False
        with open(telegram_bot.PREEMPT_FILE, "w") as f:
            f.write("corrupt")
        assert telegram_bot.wait_for_preempt_processed(timeout=0.1) is False
        with open(telegram_bot.PREEMPT_FILE, "w") as f:
            json.dump({"processed": False}, f)
        assert telegram_bot.wait_for_preempt_processed(timeout=0.1) is False
    finally:
        telegram_bot.PREEMPT_FILE = orig_preempt

    # 7. run_tribunal_thread coverage
    fake_orch_mod = ModuleType("awesome_bots_orchestrator")
    class DummyOrchestrator:
        def __init__(self, workspace):
            self.workspace = workspace
        async def run_tribunal(self, topic):
            if "fail" in topic:
                raise RuntimeError("orchestrator crash")
            veredito = "[1]" if "approve" in topic else "[0]"
            return {
                "warlock": "warlock text",
                "amanda": "amanda text",
                "shura": veredito
            }
    fake_orch_mod.AwesomeBotsOrchestrator = DummyOrchestrator

    fake_worker_mod = ModuleType("ghost_worker")
    class DummyWorker:
        def __init__(self, workspace):
            self.workspace = workspace
        def process_audit(self, lead, veredito):
            return f"Processed lead {lead} with veredito {veredito}"
    fake_worker_mod.GhostWorker = DummyWorker

    orig_orch_mod = sys.modules.get("awesome_bots_orchestrator")
    orig_worker_mod = sys.modules.get("ghost_worker")

    sys.modules["awesome_bots_orchestrator"] = fake_orch_mod
    sys.modules["ghost_worker"] = fake_worker_mod

    orig_send = telegram_bot.send_message
    try:
        tg_msgs = []
        telegram_bot.send_message = lambda cid, text: tg_msgs.append(text)

        telegram_bot.run_tribunal_thread(999, "#123 {Lead A} approve")
        assert len(tg_msgs) == 2
        assert "Lead A" in tg_msgs[1]
        assert "APROVADO [1]" in tg_msgs[1]
        tg_msgs.clear()

        telegram_bot.run_tribunal_thread(999, "lead: Lead B\nrejected")
        assert "Lead B" in tg_msgs[1]
        assert "REJEITADO [0]" in tg_msgs[1]
        tg_msgs.clear()

        telegram_bot.run_tribunal_thread(999, "ShortLine approve")
        assert "ShortLine" in tg_msgs[1]
        tg_msgs.clear()

        telegram_bot.run_tribunal_thread(999, "This is a very long first line of the topic that is longer than fifty characters in total. approve")
        assert "..." in tg_msgs[1]
        tg_msgs.clear()

        telegram_bot.run_tribunal_thread(999, "fail topic")
        assert any("Erro ao rodar o Tribunal" in m for m in tg_msgs)
    finally:
        telegram_bot.send_message = orig_send
        if orig_orch_mod:
            sys.modules["awesome_bots_orchestrator"] = orig_orch_mod
        else:
            del sys.modules["awesome_bots_orchestrator"]
        if orig_worker_mod:
            sys.modules["ghost_worker"] = orig_worker_mod
        else:
            del sys.modules["ghost_worker"]

    # 8. run_rag_thread coverage
    fake_qdrant_mod = ModuleType("qdrant_client_helper")
    class DummyRAGClient:
        def search(self, query, limit=3):
            if "fail" in query:
                raise RuntimeError("qdrant fail")
            if "empty" in query:
                return []
            return [{"score": 0.99, "text": "matched text", "metadata": "some_meta"}]
    fake_qdrant_mod.QdrantRAGClient = DummyRAGClient

    orig_qdrant_mod = sys.modules.get("qdrant_client_helper")
    sys.modules["qdrant_client_helper"] = fake_qdrant_mod

    try:
        tg_msgs = []
        telegram_bot.send_message = lambda cid, text: tg_msgs.append(text)

        telegram_bot.run_rag_thread(999, "normal query")
        assert any("matched text" in m for m in tg_msgs)
        tg_msgs.clear()

        telegram_bot.run_rag_thread(999, "empty query")
        assert any("Nenhum contexto correspondente" in m for m in tg_msgs)
        tg_msgs.clear()

        telegram_bot.run_rag_thread(999, "fail query")
        assert any("Erro ao consultar RAG" in m for m in tg_msgs)
    finally:
        telegram_bot.send_message = orig_send
        if orig_qdrant_mod:
            sys.modules["qdrant_client_helper"] = orig_qdrant_mod
        else:
            del sys.modules["qdrant_client_helper"]

    # 9. run_playbook_thread coverage
    pb_dir = tmp_path / "intelligence" / "playbooks"
    os.makedirs(pb_dir, exist_ok=True)
    orig_base_dir = telegram_bot.BASE_DIR
    telegram_bot.BASE_DIR = str(tmp_path)

    preempt_cmds = []
    orig_preempt_cmd = telegram_bot.send_preempt_command
    telegram_bot.send_preempt_command = lambda act, par=None: preempt_cmds.append((act, par))
    orig_wait_preempt = telegram_bot.wait_for_preempt_processed
    telegram_bot.wait_for_preempt_processed = lambda *a, **kw: True
    try:
        tg_msgs = []
        telegram_bot.send_message = lambda cid, text: tg_msgs.append(text)

        telegram_bot.run_playbook_thread(999, "not_found")
        assert any("encontrado" in m for m in tg_msgs)
        tg_msgs.clear()

        pb_path = pb_dir / "empty.md"
        with open(pb_path, "w") as f:
            f.write("no step lines")
        telegram_bot.run_playbook_thread(999, "empty")
        assert any("instru" in m for m in tg_msgs)
        tg_msgs.clear()

        pb_path = pb_dir / "comp.md"
        with open(pb_path, "w") as f:
            f.write(
                "- click 10 20\n"
                "- click coords_fail\n"
                "- type 'some text'\n"
                "- set_goal 'achieve matrix'\n"
                "- wait 1\n"
                "- wait non_int\n"
                "- custom_cmd arg\n"
            )
        telegram_bot.run_playbook_thread(999, "comp")
        assert any("Coordenadas" in m or "coords" in m.lower() or "click" in m.lower() for m in tg_msgs)
        assert ("click", {"x": 10, "y": 20}) in preempt_cmds
        assert ("type", {"text": "some text"}) in preempt_cmds
        assert ("set_goal", {"goal": "achieve matrix"}) in preempt_cmds
        assert ("custom_cmd", {"params": "arg"}) in preempt_cmds
        tg_msgs.clear()

        pb_path = pb_dir / "err.md"
        with open(pb_path, "w") as f:
            f.write("- click 10 20")

        orig_open_playbook = builtins.open
        def fake_open_playbook(file, mode="r", *args, **kwargs):
            if "err.md" in str(file):
                raise RuntimeError("read error")
            return orig_open_playbook(file, mode, *args, **kwargs)

        builtins.open = fake_open_playbook
        try:
            telegram_bot.run_playbook_thread(999, "err")
            assert any("Erro ao rodar playbook" in m for m in tg_msgs)
        finally:
            builtins.open = orig_open_playbook
    finally:
        telegram_bot.BASE_DIR = orig_base_dir
        telegram_bot.send_preempt_command = orig_preempt_cmd
        telegram_bot.wait_for_preempt_processed = orig_wait_preempt

    # 10. is_claw_loop_online coverage
    orig_status_file = telegram_bot.STATUS_FILE
    telegram_bot.STATUS_FILE = str(tmp_path / "loop_status.json")
    try:
        assert telegram_bot.is_claw_loop_online() is False
        with open(telegram_bot.STATUS_FILE, "w") as f:
            f.write("{}")
        assert telegram_bot.is_claw_loop_online() is True

        orig_exists = os.path.exists
        def fake_exists_err(path):
            if path == telegram_bot.STATUS_FILE:
                raise OSError("disk failure")
            return orig_exists(path)
        os.path.exists = fake_exists_err
        try:
            assert telegram_bot.is_claw_loop_online() is False
        finally:
            os.path.exists = orig_exists
    finally:
        telegram_bot.STATUS_FILE = orig_status_file

    # 11. handle_task_command coverage
    orig_base_dir = telegram_bot.BASE_DIR
    telegram_bot.BASE_DIR = str(tmp_path)
    os.makedirs(str(tmp_path / "logs"), exist_ok=True)
    telegram_bot.STATUS_FILE = os.path.join(telegram_bot.BASE_DIR, "logs", "claw_status.json")

    try:
        res = telegram_bot.handle_task_command("/task list")
        assert "stack de tarefas está limpa" in res["text"]

        res = telegram_bot.handle_task_command("/task add")
        assert "Por favor, descreva a tarefa" in res["text"]

        res = telegram_bot.handle_task_command("/task add Build CI pipeline")
        assert "Tarefa registrada com sucesso" in res["text"]

        res = telegram_bot.handle_task_command("/task list")
        assert "Build CI pipeline" in res["text"]

        res = telegram_bot.handle_task_command("/task done")
        assert "especifique o ID" in res["text"]

        res = telegram_bot.handle_task_command("/task done abc")
        assert "ID da tarefa precisa ser um número inteiro" in res["text"]

        res = telegram_bot.handle_task_command("/task done 99")
        assert "não encontrada" in res["text"]

        res = telegram_bot.handle_task_command("/task done 1")
        assert "marcada como concluída" in res["text"]

        res = telegram_bot.handle_task_command("/task clear")
        assert "Fila de tarefas limpa" in res["text"]

        tasks_file = os.path.join(telegram_bot.BASE_DIR, "logs", "amanda_tasks.json")
        with open(tasks_file, "w") as f:
            f.write("corrupt")
        res = telegram_bot.handle_task_command("/task list")
        assert "stack de tarefas está limpa" in res["text"]

        orig_atomic_write = telegram_bot._atomic_write_json
        telegram_bot._atomic_write_json = lambda path, data: (_ for _ in ()).throw(OSError("mock write failure"))
        try:
            telegram_bot.handle_task_command("/task add Task with failing write")
        finally:
            telegram_bot._atomic_write_json = orig_atomic_write
    finally:
        telegram_bot.BASE_DIR = orig_base_dir

    # 12. handle_update commands coverage
    orig_authorized = telegram_bot.AUTHORIZED_CHAT_ID
    telegram_bot.AUTHORIZED_CHAT_ID = 55555
    tg_msgs = []
    orig_send = telegram_bot.send_message
    telegram_bot.send_message = lambda cid, text: tg_msgs.append((cid, text))
    try:
        telegram_bot.handle_update({"message": {"chat": {"id": 11111}, "text": "/status", "from": {"username": "hack"}}})
        assert len(tg_msgs) == 1
        assert "Acesso não autorizado" in tg_msgs[0][1]
    finally:
        telegram_bot.AUTHORIZED_CHAT_ID = orig_authorized
        tg_msgs.clear()

    telegram_bot.AUTHORIZED_CHAT_ID = None
    try:
        orig_online_check = telegram_bot.is_claw_loop_online
        telegram_bot.is_claw_loop_online = lambda: False
        try:
            telegram_bot.handle_update({"message": {"chat": {"id": 123}, "text": "/pause", "from": {"username": "operator"}}})
            assert len(tg_msgs) == 1
            assert "O robô Claw está OFFLINE" in tg_msgs[0][1]
        finally:
            telegram_bot.is_claw_loop_online = orig_online_check
            tg_msgs.clear()

        telegram_bot.handle_update({"message": {"chat": {"id": 123}, "text": "/start", "from": {"username": "operator"}}})
        assert any("Mecha Huggs Workforce Studio" in m[1] for m in tg_msgs)
        tg_msgs.clear()

        orig_status_file = telegram_bot.STATUS_FILE
        telegram_bot.STATUS_FILE = str(tmp_path / "status_update.json")
        try:
            telegram_bot.handle_update({"message": {"chat": {"id": 123}, "text": "/status", "from": {"username": "operator"}}})
            assert any("Nenhum status registrado" in m[1] for m in tg_msgs)
            tg_msgs.clear()

            with open(telegram_bot.STATUS_FILE, "w") as f:
                f.write("{corrupt")
            telegram_bot.handle_update({"message": {"chat": {"id": 123}, "text": "/status", "from": {"username": "operator"}}})
            assert any("Erro ao ler arquivo de status" in m[1] for m in tg_msgs)
            tg_msgs.clear()

            with open(telegram_bot.STATUS_FILE, "w") as f:
                json.dump({"loop_state": "idle", "step": 1, "max_steps": 10, "last_seen_title": "Editor", "current_goal": "write tests", "last_thumbnail": "missing.jpg"}, f)
            telegram_bot.handle_update({"message": {"chat": {"id": 123}, "text": "/status", "from": {"username": "operator"}}})
            assert any("Status do MECHA Claw" in m[1] for m in tg_msgs)
            tg_msgs.clear()

            temp_thumb = tmp_path / "thumb.jpg"
            with open(temp_thumb, "w") as f:
                f.write("image")
            with open(telegram_bot.STATUS_FILE, "w") as f:
                json.dump({"loop_state": "idle", "step": 1, "max_steps": 10, "last_seen_title": "Editor", "current_goal": "write tests", "last_thumbnail": str(temp_thumb)}, f)

            photos_sent = []
            telegram_bot.send_photo = lambda cid, path, cap: photos_sent.append((cid, path, cap))
            try:
                telegram_bot.handle_update({"message": {"chat": {"id": 123}, "text": "/status", "from": {"username": "operator"}}})
                assert len(photos_sent) == 1
                assert photos_sent[0][1] == str(temp_thumb)
            finally:
                telegram_bot.send_photo = telegram_bot.send_photo
        finally:
            telegram_bot.STATUS_FILE = orig_status_file
            tg_msgs.clear()

        telegram_bot.is_claw_loop_online = lambda: True
        preempt_commands = []
        telegram_bot.send_preempt_command = lambda act, par=None: preempt_commands.append((act, par))
        try:
            telegram_bot.handle_update({"message": {"chat": {"id": 123}, "text": "/pause", "from": {"username": "operator"}}})
            assert ("pause", None) in preempt_commands

            telegram_bot.handle_update({"message": {"chat": {"id": 123}, "text": "/resume", "from": {"username": "operator"}}})
            assert ("resume", None) in preempt_commands

            telegram_bot.handle_update({"message": {"chat": {"id": 123}, "text": "/stop", "from": {"username": "operator"}}})
            assert ("stop", None) in preempt_commands

            telegram_bot.handle_update({"message": {"chat": {"id": 123}, "text": "/set_goal", "from": {"username": "operator"}}})
            assert "Uso correto" in tg_msgs[-1][1]

            telegram_bot.handle_update({"message": {"chat": {"id": 123}, "text": "/set_goal Test Goal", "from": {"username": "operator"}}})
            assert ("set_goal", {"goal": "Test Goal"}) in preempt_commands

            telegram_bot.handle_update({"message": {"chat": {"id": 123}, "text": "/click 100", "from": {"username": "operator"}}})
            assert "Uso correto" in tg_msgs[-1][1]

            telegram_bot.handle_update({"message": {"chat": {"id": 123}, "text": "/click abc 200", "from": {"username": "operator"}}})
            assert "números inteiros" in tg_msgs[-1][1]

            telegram_bot.handle_update({"message": {"chat": {"id": 123}, "text": "/click 100 200", "from": {"username": "operator"}}})
            assert ("click", {"x": 100, "y": 200}) in preempt_commands

            telegram_bot.handle_update({"message": {"chat": {"id": 123}, "text": "/type", "from": {"username": "operator"}}})
            assert "Uso correto" in tg_msgs[-1][1]

            telegram_bot.handle_update({"message": {"chat": {"id": 123}, "text": "/type write code", "from": {"username": "operator"}}})
            assert ("type", {"text": "write code"}) in preempt_commands
        finally:
            telegram_bot.is_claw_loop_online = orig_online_check
            telegram_bot.send_preempt_command = orig_preempt_cmd
            preempt_commands.clear()
            tg_msgs.clear()

        telegram_bot.handle_update({"message": {"chat": {"id": 123}, "text": "/rag", "from": {"username": "operator"}}})
        assert "Uso correto" in tg_msgs[-1][1]

        telegram_bot.handle_update({"message": {"chat": {"id": 123}, "text": "/tribunal", "from": {"username": "operator"}}})
        assert "Uso correto" in tg_msgs[-1][1]

        telegram_bot.is_claw_loop_online = lambda: True
        try:
            telegram_bot.handle_update({"message": {"chat": {"id": 123}, "text": "/run_playbook", "from": {"username": "operator"}}})
            assert "Uso correto" in tg_msgs[-1][1]
        finally:
            telegram_bot.is_claw_loop_online = orig_online_check

        telegram_bot.handle_update({"message": {"chat": {"id": 123}, "text": "hello bot", "from": {"username": "operator"}}})
        assert "Olá! Eu sou" in tg_msgs[-1][1]
        tg_msgs.clear()

        telegram_bot.handle_update({"message": {"chat": {"id": 123}}})
        telegram_bot.handle_update({"other": "field"})
        assert len(tg_msgs) == 0

        # 13. is_port_available and start_http_server coverage
        assert telegram_bot.is_port_available(99999) is False

        import uvicorn
        orig_run = uvicorn.run
        called_run_args = []
        def fake_run(*args, **kwargs):
            called_run_args.append((args, kwargs))
        uvicorn.run = fake_run
        try:
            telegram_bot.start_http_server()
            assert len(called_run_args) == 1
        finally:
            uvicorn.run = orig_run

        # 14. Extra event_hub, send_message, log_event_to_dashboard, run_tribunal_thread & start_http_server coverage
        # publish invalid envelope
        success, msg = telegram_bot.event_hub.publish({"topic": 123, "sender": "test", "timestamp": 123, "payload": {}})
        assert success is False

        # send_message exception coverage
        orig_post = requests.post
        requests.post = lambda *args, **kwargs: (_ for _ in ()).throw(requests.RequestException("connection fail"))
        try:
            telegram_bot.send_message(12345, "hello")
        finally:
            requests.post = orig_post

        # log_event_to_dashboard safe check for non-dict status file
        orig_status_file = telegram_bot.STATUS_FILE
        telegram_bot.STATUS_FILE = str(tmp_path / "list_status.json")
        try:
            with open(telegram_bot.STATUS_FILE, "w") as f:
                f.write("[1, 2, 3]")
            telegram_bot.log_event_to_dashboard("info", "msg")
            with open(telegram_bot.STATUS_FILE, "r") as f:
                data = json.load(f)
            assert isinstance(data, dict)
            assert len(data["events"]) == 1

            # non-list events check
            with open(telegram_bot.STATUS_FILE, "w") as f:
                f.write(json.dumps({"events": "not_a_list"}))
            telegram_bot.log_event_to_dashboard("info", "msg2")
            with open(telegram_bot.STATUS_FILE, "r") as f:
                data = json.load(f)
            assert isinstance(data["events"], list)
            assert len(data["events"]) == 1
        finally:
            telegram_bot.STATUS_FILE = orig_status_file

        # raise OSError on write in log_event_to_dashboard
        orig_open = builtins.open
        def fake_open_err(file, mode="r", *args, **kwargs):
            if "claw_status.json" in str(file) and "w" in mode:
                raise OSError("mock write error")
            return orig_open(file, mode, *args, **kwargs)
        with patch("builtins.open", fake_open_err):
            telegram_bot.log_event_to_dashboard("info", "msg")

        # event_hub.publish exception on claw.log
        orig_publish = telegram_bot.event_hub.publish
        telegram_bot.event_hub.publish = lambda *a, **kw: (_ for _ in ()).throw(RuntimeError("publish fail"))
        try:
            telegram_bot.log_event_to_dashboard("info", "msg publish error")
        finally:
            telegram_bot.event_hub.publish = orig_publish

        # run_tribunal_thread matching scope_match
        fake_orch_mod = ModuleType("awesome_bots_orchestrator")
        fake_orch_mod.AwesomeBotsOrchestrator = DummyOrchestrator
        fake_worker_mod = ModuleType("ghost_worker")
        fake_worker_mod.GhostWorker = DummyWorker
        
        orig_orch_mod = sys.modules.get("awesome_bots_orchestrator")
        orig_worker_mod = sys.modules.get("ghost_worker")
        
        sys.modules["awesome_bots_orchestrator"] = fake_orch_mod
        sys.modules["ghost_worker"] = fake_worker_mod
        try:
            telegram_bot.run_tribunal_thread(999, "#{456} {MySpecialLead} approve")
        finally:
            if orig_orch_mod:
                sys.modules["awesome_bots_orchestrator"] = orig_orch_mod
            else:
                del sys.modules["awesome_bots_orchestrator"]
            if orig_worker_mod:
                sys.modules["ghost_worker"] = orig_worker_mod
            else:
                del sys.modules["ghost_worker"]

        # handle_task_command errors and non-dict states
        orig_open_md = builtins.open
        def fake_open_md_err(file, mode="r", *args, **kwargs):
            if "AMANDA_TASKS.md" in str(file) and "w" in mode:
                raise OSError("mock write error")
            return orig_open_md(file, mode, *args, **kwargs)
        
        orig_base_dir = telegram_bot.BASE_DIR
        telegram_bot.BASE_DIR = str(tmp_path)
        os.makedirs(str(tmp_path / "logs"), exist_ok=True)
        telegram_bot.STATUS_FILE = os.path.join(telegram_bot.BASE_DIR, "logs", "claw_status.json")
        tasks_file = os.path.join(telegram_bot.BASE_DIR, "logs", "amanda_tasks.json")
        try:
            # non-dict STATUS_FILE
            with open(telegram_bot.STATUS_FILE, "w") as f:
                f.write("[1, 2, 3]")
            # non-dict tasks_file
            with open(tasks_file, "w") as f:
                f.write('{"tasks": "not_a_list"}')
                
            telegram_bot.handle_task_command("/task add Task with non-dict base states")

            with patch("builtins.open", fake_open_md_err):
                telegram_bot.handle_task_command("/task add Task that fails to write MD")
        finally:
            telegram_bot.BASE_DIR = orig_base_dir

        # publish_to_bus exception in handle_task_command
        telegram_bot.event_hub.publish = lambda *a, **kw: (_ for _ in ()).throw(RuntimeError("publish fail"))
        try:
            telegram_bot.handle_task_command("/task add Task that fails to publish")
        finally:
            telegram_bot.event_hub.publish = orig_publish

        # /rag query, /tribunal topic, /run_playbook pb, /task list routing in handle_update
        orig_run_rag = telegram_bot.run_rag_thread
        orig_run_trib = telegram_bot.run_tribunal_thread
        orig_run_play = telegram_bot.run_playbook_thread
        
        called_targets = []
        telegram_bot.run_rag_thread = lambda cid, q: called_targets.append(("rag", q))
        telegram_bot.run_tribunal_thread = lambda cid, t: called_targets.append(("tribunal", t))
        telegram_bot.run_playbook_thread = lambda cid, n: called_targets.append(("playbook", n))
        
        try:
            telegram_bot.handle_update({"message": {"chat": {"id": 123}, "text": "/rag normal query", "from": {"username": "operator"}}})
            assert ("rag", "normal query") in called_targets
            
            telegram_bot.handle_update({"message": {"chat": {"id": 123}, "text": "/tribunal debate topic", "from": {"username": "operator"}}})
            assert ("tribunal", "debate topic") in called_targets
            
            telegram_bot.handle_update({"message": {"chat": {"id": 123}, "text": "/run_playbook my_playbook", "from": {"username": "operator"}}})
            assert ("playbook", "my_playbook") in called_targets
            
            telegram_bot.handle_update({"message": {"chat": {"id": 123}, "text": "/task list", "from": {"username": "operator"}}})
            
        finally:
            telegram_bot.run_rag_thread = orig_run_rag
            telegram_bot.run_tribunal_thread = orig_run_trib
            telegram_bot.run_playbook_thread = orig_run_play

        # start_http_server dynamic port fallback
        orig_is_available = telegram_bot.is_port_available
        telegram_bot.is_port_available = lambda port: False
        called_ports = []
        def fake_run_ports(app, host, port, **kwargs):
            called_ports.append(port)
        uvicorn.run = fake_run_ports
        try:
            telegram_bot.start_http_server()
            assert len(called_ports) == 1
            assert called_ports[0] > 0
        finally:
            telegram_bot.is_port_available = orig_is_available
            uvicorn.run = orig_run

        # main polling loop normal update response and KeyboardInterrupt
        orig_get = requests.get
        orig_sleep = time.sleep
        time.sleep = lambda *a: None
        
        class DummyUpdatesResp:
            status_code = 200
            def json(self):
                return {
                    "ok": True,
                    "result": [{
                        "update_id": 9999,
                        "message": {
                            "chat": {"id": 12345},
                            "text": "hello polling test",
                            "from": {"username": "polling_user"}
                        }
                    }]
                }
                
        poll_counter = 0
        def fake_polling_get(url, *args, **kwargs):
            nonlocal poll_counter
            if "getMe" in url:
                class DummyMe:
                    status_code = 200
                return DummyMe()
            elif "getUpdates" in url:
                params = kwargs.get("params", {})
                if params.get("offset") == -1:
                    class DummyCleanup:
                        status_code = 200
                        def json(self):
                            return {"ok": True, "result": []}
                    return DummyCleanup()
                
                poll_counter += 1
                if poll_counter == 1:
                    return DummyUpdatesResp()
                else:
                    raise KeyboardInterrupt()
            class DummyFallback:
                status_code = 200
            return DummyFallback()
            
        requests.get = fake_polling_get
        updates_handled = []
        orig_handle_update = telegram_bot.handle_update
        telegram_bot.handle_update = lambda update: updates_handled.append(update)
        orig_token = telegram_bot.TOKEN
        telegram_bot.TOKEN = "mock_token"
        try:
            telegram_bot.main()
            assert len(updates_handled) == 1
            assert updates_handled[0]["update_id"] == 9999
        finally:
            telegram_bot.TOKEN = orig_token
            requests.get = orig_get
            time.sleep = orig_sleep
            telegram_bot.handle_update = orig_handle_update
    finally:
        telegram_bot.AUTHORIZED_CHAT_ID = orig_authorized
        telegram_bot.send_message = true_orig_send_message


def test_telegram_bot_endpoints_comprehensive(tg_client, tmp_path):
    import telegram_bot
    # status file doesn't exist
    if os.path.exists(telegram_bot.STATUS_FILE):
        os.remove(telegram_bot.STATUS_FILE)
    resp = tg_client.get("/api/status")
    assert resp.status_code == 200
    assert "No status found" in resp.json()["error"]

    # status file corrupted
    with open(telegram_bot.STATUS_FILE, "w") as f:
        f.write("{corrupt")
    resp = tg_client.get("/api/status")
    assert resp.status_code == 200
    assert "error" in resp.json()

    # tasks file corrupted
    tasks_file = os.path.join(telegram_bot.BASE_DIR, "logs", "amanda_tasks.json")
    with open(tasks_file, "w") as f:
        f.write("{corrupt")
    resp = tg_client.get("/api/tasks")
    assert resp.status_code == 200
    assert resp.json() == []

    # clear tasks error path
    orig_handle = telegram_bot.handle_task_command
    def failing_handle(*args, **kwargs):
        raise ValueError("simulated handler error")
    telegram_bot.handle_task_command = failing_handle
    try:
        resp = tg_client.post("/api/tasks/clear")
        assert resp.status_code == 500
        assert "simulated handler error" in resp.json()["error"]
    finally:
        telegram_bot.handle_task_command = orig_handle

    # send_message exception paths (lines 187-191)
    import requests
    orig_token = telegram_bot.TOKEN
    telegram_bot.TOKEN = "mock_token"
    orig_post = requests.post
    
    # Success path
    requests.post = lambda url, json, timeout: None
    telegram_bot.send_message(1234, "hello")
    
    # Exception path
    def post_fail(*args, **kwargs):
        raise RuntimeError("send_message failed")
    requests.post = post_fail
    telegram_bot.send_message(1234, "hello")
    
    telegram_bot.TOKEN = orig_token
    requests.post = orig_post

    # log_event_to_dashboard with events not a list (line 531)
    orig_status_file = telegram_bot.STATUS_FILE
    telegram_bot.STATUS_FILE = str(tmp_path / "events_not_list.json")
    try:
        with open(telegram_bot.STATUS_FILE, "w") as f:
            f.write(json.dumps({"events": "not_a_list"}))
        telegram_bot.handle_task_command("/task add Dummy task to trigger status file checks")
    finally:
        telegram_bot.STATUS_FILE = orig_status_file

    # failed publish in /api/bus/publish (line 853)
    orig_publish = telegram_bot.event_hub.publish
    telegram_bot.event_hub.publish = lambda *args: (False, "Simulated publish error")
    try:
        resp = tg_client.post("/api/bus/publish", json={"topic": "t", "sender": "s", "timestamp": 123, "payload": {}})
        assert resp.status_code == 400
        assert "Simulated publish error" in resp.json()["error"]
    finally:
        telegram_bot.event_hub.publish = orig_publish

    # health endpoint OSError path (line 864-865)
    orig_exists = os.path.exists
    def exists_fail(path):
        if "claw_status.json" in str(path):
            raise OSError("mock exist error")
        return orig_exists(path)
    os.path.exists = exists_fail
    try:
        resp = tg_client.get("/api/health")
        assert resp.status_code == 200
        assert resp.json()["claw_loop"] == "offline"
    finally:
        os.path.exists = orig_exists

    # tasks file does not exist in GET /api/tasks (line 893)
    if os.path.exists(tasks_file):
        os.remove(tasks_file)
    resp = tg_client.get("/api/tasks")
    assert resp.status_code == 200
    assert resp.json() == []

    # missing description in POST /api/tasks (line 899)
    resp = tg_client.post("/api/tasks", json={"description": "   "})
    assert resp.status_code == 400
    assert "Missing description" in resp.json()["error"]


def test_telegram_bot_websocket_edge_cases(tg_client):
    with tg_client.websocket_connect("/ws/bus") as ws:
        ws.send_json({"action": "subscribe", "topics": ["test.topic"]})
    # Non-json send triggers exception handling
    with tg_client.websocket_connect("/ws/bus") as ws:
        ws.send_text("non-json")


def test_telegram_bot_main_edge_cases():
    import telegram_bot
    import requests
    import time

    orig_get = requests.get
    orig_sleep = time.sleep

    def sleep_interrupt(*args):
        raise KeyboardInterrupt()

    try:
        # getMe raises exception
        def get_fail_getme(url, *args, **kwargs):
            if "getMe" in url:
                raise RuntimeError("getme failed")
            return orig_get(url, *args, **kwargs)
        requests.get = get_fail_getme
        time.sleep = sleep_interrupt
        try:
            telegram_bot.main()
        except KeyboardInterrupt:
            pass

        # complex polling flows
        counter = 0
        def get_complex_flow(url, *args, **kwargs):
            nonlocal counter
            if "getMe" in url:
                class Dummy:
                    status_code = 200
                return Dummy()
            elif "getUpdates" in url:
                params = kwargs.get("params", {})
                if params.get("offset") == -1:
                    raise RuntimeError("initial clean queue fail")
                else:
                    counter += 1
                    if counter == 1:
                        class DummyFail:
                            status_code = 500
                        return DummyFail()
                    elif counter == 2:
                        raise RuntimeError("polling exception")
                    else:
                        raise KeyboardInterrupt()
            class DummyFallback:
                status_code = 200
            return DummyFallback()

        requests.get = get_complex_flow
        time.sleep = lambda *a: None
        try:
            telegram_bot.main()
        except KeyboardInterrupt:
            pass
    finally:
        requests.get = orig_get
        time.sleep = orig_sleep


# =============================================================================
# AMANDA TEAMS BOT COMPREHENSIVE EDGE CASES & EXCEPTION PATHS COVERAGE
# =============================================================================

def test_amanda_teams_bot_comprehensive(tmp_path):
    import amanda_teams_bot
    import sys
    import os
    import requests
    import uvicorn
    import base64
    import hmac
    import hashlib
    import builtins
    from unittest.mock import patch
    from types import ModuleType

    # 0. amanda reload & sys.modules import error coverage (run first to avoid overriding coverage)
    import importlib
    orig_teams_secret = os.environ.get("TEAMS_SHARED_SECRET")
    orig_allow_insecure = os.environ.get("MECHA_ALLOW_INSECURE")
    if "TEAMS_SHARED_SECRET" in os.environ: del os.environ["TEAMS_SHARED_SECRET"]
    if "MECHA_ALLOW_INSECURE" in os.environ: del os.environ["MECHA_ALLOW_INSECURE"]
    
    orig_m_qdr = sys.modules.get("qdrant_client_helper")
    orig_m_orc = sys.modules.get("awesome_bots_orchestrator")
    orig_m_cod = sys.modules.get("code_squad_runner")
    orig_m_qa = sys.modules.get("qa_squad_runner")
    
    try:
        # Trigger ModuleNotFoundError for dependencies
        sys.modules["qdrant_client_helper"] = None
        sys.modules["awesome_bots_orchestrator"] = None
        sys.modules["code_squad_runner"] = None
        sys.modules["qa_squad_runner"] = None
        
        importlib.reload(amanda_teams_bot)
        assert amanda_teams_bot.rag_client is None
        assert amanda_teams_bot.orchestrator is None
        assert amanda_teams_bot.dev_squad_runner is None
        assert amanda_teams_bot.qa_squad_runner is None
        
        # Trigger successful import branch coverage
        os.environ["MECHA_ALLOW_INSECURE"] = "1"
        class MockClass:
            def __init__(self, *args, **kwargs): pass
        from types import ModuleType
        m_qdr = ModuleType("qdrant_client_helper")
        m_qdr.QdrantRAGClient = MockClass
        m_orc = ModuleType("awesome_bots_orchestrator")
        m_orc.AwesomeBotsOrchestrator = MockClass
        m_cod = ModuleType("code_squad_runner")
        m_cod.CodeSquadRunner = MockClass
        m_qa = ModuleType("qa_squad_runner")
        m_qa.QASquadRunner = MockClass
        
        sys.modules["qdrant_client_helper"] = m_qdr
        sys.modules["awesome_bots_orchestrator"] = m_orc
        sys.modules["code_squad_runner"] = m_cod
        sys.modules["qa_squad_runner"] = m_qa
        
        importlib.reload(amanda_teams_bot)
        assert amanda_teams_bot.rag_client is not None
        assert amanda_teams_bot.orchestrator is not None
        assert amanda_teams_bot.dev_squad_runner is not None
        assert amanda_teams_bot.qa_squad_runner is not None
        
    finally:
        # Restore environment and sys modules
        if orig_teams_secret is not None:
            os.environ["TEAMS_SHARED_SECRET"] = orig_teams_secret
        if orig_allow_insecure is not None:
            os.environ["MECHA_ALLOW_INSECURE"] = orig_allow_insecure
            
        for name, mod in [
            ("qdrant_client_helper", orig_m_qdr),
            ("awesome_bots_orchestrator", orig_m_orc),
            ("code_squad_runner", orig_m_cod),
            ("qa_squad_runner", orig_m_qa)
        ]:
            if mod is not None:
                sys.modules[name] = mod
            else:
                if name in sys.modules: del sys.modules[name]
        importlib.reload(amanda_teams_bot)

    # 1. sys.frozen base dirs resolution
    sys.frozen = True
    sys.executable = "/dummy/exe_dir/main.exe"
    try:
        res = amanda_teams_bot._resolve_base_dirs()
        assert len(res) == 3
    finally:
        if hasattr(sys, "frozen"):
            del sys.frozen

    # 2. _safe_chat_id coverage
    orig_chat_env = os.environ.get("TELEGRAM_CHAT_ID")
    try:
        os.environ["TELEGRAM_CHAT_ID"] = "not_an_int"
        assert amanda_teams_bot._safe_chat_id() == 0
        os.environ["TELEGRAM_CHAT_ID"] = ""
        assert amanda_teams_bot._safe_chat_id() == 0
    finally:
        if orig_chat_env is not None:
            os.environ["TELEGRAM_CHAT_ID"] = orig_chat_env
        else:
            if "TELEGRAM_CHAT_ID" in os.environ: del os.environ["TELEGRAM_CHAT_ID"]

    # 3. _read_json error handling
    assert amanda_teams_bot._read_json("nonexistent_file.json", {"fallback": 42}) == {"fallback": 42}
    temp_json = tmp_path / "bad.json"
    with open(temp_json, "w") as f:
        f.write("corrupt")
    assert amanda_teams_bot._read_json(str(temp_json), []) == []

    # 4. _atomic_write_json failure
    try:
        amanda_teams_bot._atomic_write_json(str(tmp_path / "nonexistent_dir" / "out.json"), {"ok": 1})
    except Exception:
        pass

    # 5. log_event_to_dashboard write error
    orig_status_file = amanda_teams_bot.STATUS_FILE
    amanda_teams_bot.STATUS_FILE = str(tmp_path / "nonexistent_dir" / "status.json")
    try:
        amanda_teams_bot.log_event_to_dashboard("info", "test write failure")
    finally:
        amanda_teams_bot.STATUS_FILE = orig_status_file

    # 6. verify_teams_signature exception
    orig_secret = amanda_teams_bot.SHARED_SECRET
    amanda_teams_bot.SHARED_SECRET = "invalid_base64_secret"
    try:
        assert amanda_teams_bot.verify_teams_signature(b"body", "sig") is False
    finally:
        amanda_teams_bot.SHARED_SECRET = orig_secret

    # 7. clean_teams_mention tag formats
    assert amanda_teams_bot.clean_teams_mention("<at id=\"123\">Amanda</at> test query") == "test query"

    # 8. publish_to_bus error handling
    orig_post = requests.post
    requests.post = lambda *a, **kw: (_ for _ in ()).throw(requests.RequestException("bus post fail"))
    try:
        amanda_teams_bot.publish_to_bus("topic", {})
    finally:
        requests.post = orig_post

    # 9. send_telegram_notification chunks and exceptions
    orig_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    orig_chat = os.environ.get("TELEGRAM_CHAT_ID")
    os.environ["TELEGRAM_BOT_TOKEN"] = "token"
    os.environ["TELEGRAM_CHAT_ID"] = "12345"

    posts_called = []
    requests.post = lambda url, json, **kw: posts_called.append(json)
    try:
        amanda_teams_bot.send_telegram_notification("hello")
        assert len(posts_called) == 1
        assert posts_called[0]["text"] == "hello"
        posts_called.clear()

        large_msg = "x" * 4500
        amanda_teams_bot.send_telegram_notification(large_msg)
        assert len(posts_called) == 2
        posts_called.clear()

        requests.post = lambda *a, **kw: (_ for _ in ()).throw(requests.RequestException("connection fail"))
        amanda_teams_bot.send_telegram_notification("hello")
    finally:
        requests.post = orig_post
        if orig_token is not None:
            os.environ["TELEGRAM_BOT_TOKEN"] = orig_token
        else:
            if "TELEGRAM_BOT_TOKEN" in os.environ: del os.environ["TELEGRAM_BOT_TOKEN"]
        if orig_chat is not None:
            os.environ["TELEGRAM_CHAT_ID"] = orig_chat
        else:
            if "TELEGRAM_CHAT_ID" in os.environ: del os.environ["TELEGRAM_CHAT_ID"]

    # 10. Missing squad runners fallback checks
    orig_orch = amanda_teams_bot.orchestrator
    orig_dev = amanda_teams_bot.dev_squad_runner
    orig_qa = amanda_teams_bot.qa_squad_runner

    amanda_teams_bot.orchestrator = None
    amanda_teams_bot.dev_squad_runner = None
    amanda_teams_bot.qa_squad_runner = None
    try:
        amanda_teams_bot.run_async_tribunal("topic", 123)
        amanda_teams_bot.run_async_dev_squad("prompt", 123)
        amanda_teams_bot.run_async_qa_squad("src.py", "test.py", 123)
    finally:
        amanda_teams_bot.orchestrator = orig_orch
        amanda_teams_bot.dev_squad_runner = orig_dev
        amanda_teams_bot.qa_squad_runner = orig_qa

    # 11. run_async_tribunal approved/rejected/fail states
    class MockOrch:
        def __init__(self, check_ver):
            self.check_ver = check_ver
        async def run_tribunal(self, topic):
            if "fail" in topic:
                raise RuntimeError("debate error")
            return {"shura": self.check_ver}

    try:
        amanda_teams_bot.orchestrator = MockOrch("[1] Approve")
        amanda_teams_bot.run_async_tribunal("topic", 123)

        amanda_teams_bot.orchestrator = MockOrch("[0] Reject")
        amanda_teams_bot.run_async_tribunal("topic", 123)

        amanda_teams_bot.orchestrator = MockOrch("fail")
        amanda_teams_bot.run_async_tribunal("fail topic", 123)
    finally:
        amanda_teams_bot.orchestrator = orig_orch

    # 12. run_async_dev_squad success and exception
    class MockDevRunner:
        async def run_spec_driven_dev(self, prompt):
            if "fail" in prompt:
                raise RuntimeError("runner error")
            return {
                "specification": "spec text",
                "implementation": "impl text",
                "tests": "tests text",
                "audit_report": "audit text"
            }
    try:
        amanda_teams_bot.dev_squad_runner = MockDevRunner()
        amanda_teams_bot.run_async_dev_squad("build app", 123)
        amanda_teams_bot.run_async_dev_squad("fail app", 123)
    finally:
        amanda_teams_bot.dev_squad_runner = orig_dev

    # 13. run_async_qa_squad files combinations & exception
    class MockQARunner:
        async def run_qa_audit(self, source, tests):
            if "fail" in source:
                raise RuntimeError("qa error")
            return {
                "lint_report": "lint text",
                "design_report": "design text",
                "perf_report": "perf text",
                "qa_final_report": "qa final text"
            }
    try:
        amanda_teams_bot.qa_squad_runner = MockQARunner()
        amanda_teams_bot.run_async_qa_squad("nonexistent_src.py", "nonexistent_test.py", 123)

        temp_src = tmp_path / "src.py"
        with open(temp_src, "w") as f:
            f.write("def add(a, b): return a + b")
        amanda_teams_bot.run_async_qa_squad(str(temp_src), "", 123)

        temp_test = tmp_path / "test.py"
        with open(temp_test, "w") as f:
            f.write("def test_add(): assert add(1, 2) == 3")
        amanda_teams_bot.run_async_qa_squad(str(temp_src), str(temp_test), 123)

        with open(temp_src, "w") as f:
            f.write("fail source content")
        amanda_teams_bot.run_async_qa_squad(str(temp_src), "", 123)
    finally:
        amanda_teams_bot.qa_squad_runner = orig_qa

    # 14. query_openrouter_amanda connection exception
    requests.post = lambda *a, **kw: (_ for _ in ()).throw(requests.RequestException("LLM network failure"))
    try:
        res = amanda_teams_bot.query_openrouter_amanda("query", "context")
        assert "conectar a Irminsul" in res
    finally:
        requests.post = orig_post

    # 15. handle_task_command coverage
    orig_base = amanda_teams_bot.BASE_DIR
    orig_ops = amanda_teams_bot.OPS_DIR
    amanda_teams_bot.BASE_DIR = str(tmp_path)
    amanda_teams_bot.OPS_DIR = str(tmp_path)
    os.makedirs(str(tmp_path / "logs"), exist_ok=True)
    amanda_teams_bot.STATUS_FILE = os.path.join(amanda_teams_bot.OPS_DIR, "logs", "claw_status.json")
    try:
        amanda_teams_bot.handle_task_command("/task add Build deployment script")
        res = amanda_teams_bot.handle_task_command("/task list")
        assert "Build deployment script" in res["text"]
        amanda_teams_bot.handle_task_command("/task done 1")
        amanda_teams_bot.handle_task_command("/task clear")

        orig_write = amanda_teams_bot._atomic_write_json
        amanda_teams_bot._atomic_write_json = lambda path, data: (_ for _ in ()).throw(OSError("fail write"))
        try:
            amanda_teams_bot.handle_task_command("/task add failing task")
        finally:
            amanda_teams_bot._atomic_write_json = orig_write
    finally:
        amanda_teams_bot.BASE_DIR = orig_base
        amanda_teams_bot.OPS_DIR = orig_ops

    # 16. start_server coverage
    orig_run = uvicorn.run
    called = []
    uvicorn.run = lambda *a, **kw: called.append(True)
    try:
        amanda_teams_bot.start_server()
        assert len(called) == 1
    finally:
        uvicorn.run = orig_run



    # 18. log_event_to_dashboard safe check for non-dict status file and non-list events
    orig_status_file = amanda_teams_bot.STATUS_FILE
    amanda_teams_bot.STATUS_FILE = str(tmp_path / "amanda_list_status.json")
    try:
        with open(amanda_teams_bot.STATUS_FILE, "w") as f:
            f.write("[1, 2, 3]")
        amanda_teams_bot.log_event_to_dashboard("info", "msg")
        with open(amanda_teams_bot.STATUS_FILE, "r") as f:
            data = json.load(f)
        assert isinstance(data, dict)
        
        with open(amanda_teams_bot.STATUS_FILE, "w") as f:
            f.write(json.dumps({"events": "not_a_list"}))
        amanda_teams_bot.log_event_to_dashboard("info", "msg2")
        with open(amanda_teams_bot.STATUS_FILE, "r") as f:
            data = json.load(f)
        assert isinstance(data["events"], list)
    finally:
        amanda_teams_bot.STATUS_FILE = orig_status_file

    # 19. verify_teams_signature with a valid HMAC
    secret_key = b"my_teams_secret_key"
    orig_secret = amanda_teams_bot.SHARED_SECRET
    amanda_teams_bot.SHARED_SECRET = base64.b64encode(secret_key).decode("utf-8")
    try:
        body_bytes = b"my teams message body"
        computed_hmac = hmac.new(secret_key, body_bytes, hashlib.sha256).digest()
        computed_sig = base64.b64encode(computed_hmac).decode("utf-8")
        assert amanda_teams_bot.verify_teams_signature(body_bytes, "HMAC " + computed_sig) is True
        assert amanda_teams_bot.verify_teams_signature(body_bytes, "HMAC invalid_sig") is False
    finally:
        amanda_teams_bot.SHARED_SECRET = orig_secret

    # 20. send_telegram_notification missing envs and parse_mode
    orig_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    orig_chat = os.environ.get("TELEGRAM_CHAT_ID")
    if "TELEGRAM_BOT_TOKEN" in os.environ: del os.environ["TELEGRAM_BOT_TOKEN"]
    try:
        assert amanda_teams_bot.send_telegram_notification("ignored msg") is None
    finally:
        if orig_token is not None: os.environ["TELEGRAM_BOT_TOKEN"] = orig_token

    os.environ["TELEGRAM_BOT_TOKEN"] = "token"
    os.environ["TELEGRAM_CHAT_ID"] = "12345"
    posts_called = []
    orig_post = requests.post
    requests.post = lambda url, json, **kw: posts_called.append(json)
    try:
        amanda_teams_bot.send_telegram_notification("hello", parse_mode="Markdown")
        assert len(posts_called) == 1
        assert posts_called[0]["parse_mode"] == "Markdown"
    finally:
        requests.post = orig_post
        if orig_token is not None:
            os.environ["TELEGRAM_BOT_TOKEN"] = orig_token
        else:
            if "TELEGRAM_BOT_TOKEN" in os.environ: del os.environ["TELEGRAM_BOT_TOKEN"]
        if orig_chat is not None:
            os.environ["TELEGRAM_CHAT_ID"] = orig_chat
        else:
            if "TELEGRAM_CHAT_ID" in os.environ: del os.environ["TELEGRAM_CHAT_ID"]

    # 21. query_openrouter_amanda key checking and request content return
    orig_key = amanda_teams_bot.OPENROUTER_KEY
    amanda_teams_bot.OPENROUTER_KEY = "MOCK_KEY"
    try:
        res = amanda_teams_bot.query_openrouter_amanda("my query", "my context")
        assert "Saudações, Operador" in res
        
        amanda_teams_bot.OPENROUTER_KEY = "REAL_KEY"
        class DummyHTTPResponse:
            def raise_for_status(self): pass
            def json(self):
                return {"choices": [{"message": {"content": "Amanda LLM output"}}]}
        requests.post = lambda *a, **kw: DummyHTTPResponse()
        res = amanda_teams_bot.query_openrouter_amanda("my query", "my context")
        assert res == "Amanda LLM output"
    finally:
        amanda_teams_bot.OPENROUTER_KEY = orig_key
        requests.post = orig_post

    # 22. persist with OSError on generating AMANDA_TASKS.md
    orig_open = builtins.open
    def fake_open_md_err(file, mode="r", *args, **kwargs):
        if "AMANDA_TASKS.md" in str(file) and "w" in mode:
            raise OSError("mock write error")
        return orig_open(file, mode, *args, **kwargs)
    
    orig_base = amanda_teams_bot.BASE_DIR
    orig_ops = amanda_teams_bot.OPS_DIR
    amanda_teams_bot.BASE_DIR = str(tmp_path)
    amanda_teams_bot.OPS_DIR = str(tmp_path)
    os.makedirs(str(tmp_path / "logs"), exist_ok=True)
    
    with patch("builtins.open", fake_open_md_err):
        amanda_teams_bot.handle_task_command("/task add Task that fails to write MD")
        
    # 23. handle_task_command with non-list tasks and empty/invalid arguments
    tasks_file = os.path.join(amanda_teams_bot.OPS_DIR, "logs", "amanda_tasks.json")
    with open(tasks_file, "w") as f:
        f.write('{"tasks": "not_a_list"}')
    res = amanda_teams_bot.handle_task_command("/task add Build script")
    assert "Tarefa registrada" in res["text"]
    
    res = amanda_teams_bot.handle_task_command("/task add")
    assert "Por favor, descreva" in res["text"]
    
    res = amanda_teams_bot.handle_task_command("/task done")
    assert "especifique o ID" in res["text"]
    
    res = amanda_teams_bot.handle_task_command("/task done #not_an_int")
    assert "ID da tarefa precisa ser um número inteiro" in res["text"]
    
    res = amanda_teams_bot.handle_task_command("/task done 999")
    assert "não encontrada" in res["text"]
    
    amanda_teams_bot.BASE_DIR = orig_base
    amanda_teams_bot.OPS_DIR = orig_ops


def test_amanda_teams_bot_webhook_edge_cases(teams_client):
    import amanda_teams_bot

    orig_secret = amanda_teams_bot.SHARED_SECRET
    orig_allow = amanda_teams_bot.ALLOW_INSECURE

    # 1. Fail-closed 503
    amanda_teams_bot.SHARED_SECRET = ""
    amanda_teams_bot.ALLOW_INSECURE = False
    try:
        resp = teams_client.post("/webhook/teams", json={"text": "hello"})
        assert resp.status_code == 503
        assert "configurado" in resp.json()["detail"]
    finally:
        amanda_teams_bot.SHARED_SECRET = orig_secret
        amanda_teams_bot.ALLOW_INSECURE = orig_allow

    # 2. 401 Missing Authorization header when SHARED_SECRET set
    amanda_teams_bot.SHARED_SECRET = "some_secret"
    amanda_teams_bot.ALLOW_INSECURE = False
    try:
        resp = teams_client.post("/webhook/teams", json={"text": "hello"})
        assert resp.status_code == 401

        # 3. 403 Invalid signature
        resp = teams_client.post("/webhook/teams", json={"text": "hello"}, headers={"Authorization": "HMAC bad_signature"})
        assert resp.status_code == 403
    finally:
        amanda_teams_bot.SHARED_SECRET = orig_secret
        amanda_teams_bot.ALLOW_INSECURE = orig_allow

    # 4. Command missing arguments
    amanda_teams_bot.ALLOW_INSECURE = True
    try:
        resp = teams_client.post("/webhook/teams", json={"text": "/tribunal"})
        assert "especifique" in resp.json()["text"]

        resp = teams_client.post("/webhook/teams", json={"text": "/dev"})
        assert "especifique" in resp.json()["text"]

        resp = teams_client.post("/webhook/teams", json={"text": "/qa"})
        assert "especifique" in resp.json()["text"]

        # 5. RAG client search failure
        orig_rag = amanda_teams_bot.rag_client
        class FailingRAG:
            def search(self, text, limit=3):
                raise RuntimeError("rag lookup crash")
        amanda_teams_bot.rag_client = FailingRAG()
        try:
            resp = teams_client.post("/webhook/teams", json={"text": "search keyword"})
            assert resp.status_code == 200
        finally:
            amanda_teams_bot.rag_client = orig_rag

        # 6. RAG client search success
        class SuccessRAG:
            def search(self, text, limit=3):
                return [{"metadata": {"file_name": "test_doc.txt"}, "text": "matched text content"}]
        amanda_teams_bot.rag_client = SuccessRAG()
        try:
            resp = teams_client.post("/webhook/teams", json={"text": "search keyword"})
            assert resp.status_code == 200
        finally:
            amanda_teams_bot.rag_client = orig_rag

        # 7. Validation error handler (missing 'text') returns 400
        resp = teams_client.post("/webhook/teams", json={})
        assert resp.status_code == 400

    finally:
        amanda_teams_bot.ALLOW_INSECURE = orig_allow
