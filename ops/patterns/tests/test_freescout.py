import os
import unittest
from unittest.mock import patch, MagicMock
import urllib.error
import threading

# Set environment variables for testing before importing
os.environ["FREESCOUT_URL"] = "http://test-freescout.local"
os.environ["FREESCOUT_API_KEY"] = "test-api-key"
os.environ["FREESCOUT_MAILBOX_ID"] = "42"

import claw_freescout as fsc


class TestFreeScout(unittest.TestCase):

    def setUp(self):
        # Reset open incidents cache for clean tests
        fsc._OPEN.clear()

    @patch("urllib.request.urlopen")
    def test_enabled(self, mock_urlopen):
        # Test enabled with valid configuration
        self.assertTrue(fsc.enabled())

        # Test disabled with empty URL
        with patch.dict(os.environ, {"FREESCOUT_URL": ""}):
            self.assertFalse(fsc.enabled())

        # Test disabled with empty API Key
        with patch.dict(os.environ, {"FREESCOUT_API_KEY": ""}):
            self.assertFalse(fsc.enabled())

        # Test invalid URL scheme
        with patch.dict(os.environ, {"FREESCOUT_URL": "not-a-url"}):
            self.assertFalse(fsc.enabled())

    @patch("urllib.request.urlopen")
    def test_req_success(self, mock_urlopen):
        # Mock successful API call
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.read.return_value = b'{"status": "ok", "id": 123}'
        mock_urlopen.return_value.__enter__.return_value = mock_response

        status, data = fsc._req("GET", "/api/test")
        self.assertEqual(status, 200)
        self.assertEqual(data, {"status": "ok", "id": 123})

    @patch("urllib.request.urlopen")
    def test_req_http_error(self, mock_urlopen):
        # Mock HTTP Error (e.g. 404)
        mock_err = urllib.error.HTTPError(
            url="http://test-freescout.local/api/test",
            code=404,
            msg="Not Found",
            hdrs=None,
            fp=MagicMock()
        )
        mock_err.fp.read.return_value = b'{"error": "not found"}'
        mock_urlopen.side_effect = mock_err

        status, data = fsc._req("GET", "/api/test")
        self.assertEqual(status, 404)
        self.assertEqual(data, {"error": "not found"})

    @patch("urllib.request.urlopen")
    def test_req_connection_failure(self, mock_urlopen):
        # Mock a connection timeout / DNS failure
        mock_urlopen.side_effect = Exception("DNS Resolution Failed")

        status, data = fsc._req("GET", "/api/test")
        self.assertEqual(status, 0)
        self.assertIsNone(data)

    @patch("urllib.request.urlopen")
    def test_create_conversation(self, mock_urlopen):
        # Mock creation response
        mock_response = MagicMock()
        mock_response.status = 201
        mock_response.read.return_value = b'{"id": 999, "number": 1001}'
        mock_urlopen.return_value.__enter__.return_value = mock_response

        # Test synchronous call
        res = fsc.open_or_update_incident("firewall", "Test Subject", "Test Body", sync=True)
        self.assertEqual(res, {"number": 1001, "id": 999, "url": "http://test-freescout.local/conversation/999"})
        self.assertEqual(fsc._OPEN["firewall"], {"id": 999, "number": 1001})

    @patch("urllib.request.urlopen")
    def test_add_note_on_existing_incident(self, mock_urlopen):
        # Pre-populate _OPEN to simulate existing incident
        fsc._OPEN["firewall"] = {"id": 999, "number": 1001}

        # Mock successful note creation
        mock_response = MagicMock()
        mock_response.status = 201
        mock_response.read.return_value = b'{"status": "created"}'
        mock_urlopen.return_value.__enter__.return_value = mock_response

        res = fsc.open_or_update_incident("firewall", "Another Subject", "New Detail", sync=True)
        self.assertEqual(res, {"number": 1001, "id": 999, "url": "http://test-freescout.local/conversation/999"})
        
        # Verify it attempted to add note (url contains 999/threads)
        called_req = mock_urlopen.call_args[0][0]
        self.assertTrue(called_req.full_url.endswith("/api/conversations/999/threads"))

    @patch("urllib.request.urlopen")
    def test_asynchronous_incident_reporting(self, mock_urlopen):
        mock_response = MagicMock()
        mock_response.status = 201
        mock_response.read.return_value = b'{"id": 888, "number": 2002}'
        mock_urlopen.return_value.__enter__.return_value = mock_response

        callback_result = None
        event = threading.Event()

        def test_callback(res):
            nonlocal callback_result
            callback_result = res
            event.set()

        # Run asynchronously (default sync=False)
        res = fsc.open_or_update_incident("recovery", "Async Subject", "Async Body", callback=test_callback)
        self.assertIsNone(res)  # Returns None immediately

        # Wait for background worker to execute the task
        success = event.wait(timeout=2.0)
        self.assertTrue(success)
        self.assertEqual(callback_result, {"number": 2002, "id": 888, "url": "http://test-freescout.local/conversation/888"})
        self.assertEqual(fsc._OPEN["recovery"], {"id": 888, "number": 2002})

    def test_config_env_overrides(self):
        # Test overrides via env variables
        with patch.dict(os.environ, {
            "FREESCOUT_URL": "https://custom-fs.net/",
            "FREESCOUT_API_KEY": "custom-key",
            "FREESCOUT_MAILBOX_ID": "5",
            "FREESCOUT_TIMEOUT": "4.5",
            "FREESCOUT_CUSTOMER_EMAIL": "robot@mecha.io",
            "FREESCOUT_CUSTOMER_FIRST_NAME": "Automation",
            "FREESCOUT_CUSTOMER_LAST_NAME": "Engine"
        }):
            cfg = fsc.get_config()
            self.assertEqual(cfg["url"], "https://custom-fs.net")
            self.assertEqual(cfg["api_key"], "custom-key")
            self.assertEqual(cfg["mailbox_id"], 5)
            self.assertEqual(cfg["timeout"], 4.5)
            self.assertEqual(cfg["customer_email"], "robot@mecha.io")
            self.assertEqual(cfg["customer_first_name"], "Automation")
            self.assertEqual(cfg["customer_last_name"], "Engine")
