import pytest
from unittest.mock import patch, MagicMock
import os
import sys

# Append parent dir to path so we can import claw_control
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import claw_control

def test_check_panic_button_not_initialized():
    claw_control.LAST_EXPECTED_POS = (0, 0)
    assert claw_control.check_panic_button() is False

def test_check_panic_button_triggered():
    claw_control.set_expected_position(100, 100)
    with patch('claw_control.get_cursor_position', return_value=(200, 200)):
        assert claw_control.check_panic_button() is True

def test_check_panic_button_safe():
    claw_control.set_expected_position(100, 100)
    with patch('claw_control.get_cursor_position', return_value=(105, 105)):
        assert claw_control.check_panic_button() is False

def test_move_mouse_virtual_desktop_bounds():
    # If x or y outside virtual desktop, raises ValueError
    with patch('claw_control.ctypes.windll.user32.GetSystemMetrics') as mock_metrics:
        # Mock values for 1920x1080 screen
        def side_effect(code):
            if code == 76: return 0
            if code == 77: return 0
            if code == 78: return 1920
            if code == 79: return 1080
            return 0
        mock_metrics.side_effect = side_effect
        
        with pytest.raises(ValueError, match="Coordenadas de movimento invalidas"):
            claw_control.move_mouse(2000, 500)

def test_simulate_click_blocked_by_firewall():
    with patch('claw_control.validate_action_safety', return_value=False):
        with pytest.raises(PermissionError, match="FIREWALL_BLOCK"):
            claw_control.simulate_click(500, 500)

def test_simulate_typing_basic():
    """Test that simulate typing attempts to send input without error"""
    with patch('claw_control.ctypes.windll.user32.SendInput') as mock_send_input:
        with patch('claw_control.time.sleep'):
            claw_control.simulate_typing("A")
            assert mock_send_input.called
            assert mock_send_input.call_count == 2 # Down and Up

def test_validate_action_safety_out_of_bounds():
    """Test validate_action_safety allows click if out of active window bounds"""
    with patch('claw_control.ctypes.windll.user32.GetForegroundWindow', return_value=123):
        with patch('claw_control.claw_vision.get_window_bounds', return_value=(100, 100, 500, 500)):
            # x=50, y=50 is outside (100, 100, 500, 500)
            assert claw_control.validate_action_safety(50, 50) is True

def test_validate_action_safety_prohibited_word():
    """Test firewall blocks if prohibited word is detected via OCR"""
    with patch('claw_control.ctypes.windll.user32.GetForegroundWindow', return_value=123):
        with patch('claw_control.claw_vision.get_window_bounds', return_value=(0, 0, 800, 600)):
            with patch('claw_control.claw_vision.capture_window_area') as mock_capture:
                mock_img = MagicMock()
                mock_img.width = 800
                mock_img.height = 600
                mock_capture.return_value = mock_img
                
                with patch('claw_control.claw_ocr.extract_text_from_image') as mock_ocr:
                    mock_ocr_result = MagicMock()
                    mock_ocr_result.raw_text = "Confirmar DELETAR arquivo"
                    mock_ocr.return_value = mock_ocr_result
                    
                    assert claw_control.validate_action_safety(100, 100) is False
