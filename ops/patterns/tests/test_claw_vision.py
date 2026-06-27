import pytest
from unittest.mock import patch, MagicMock
from PIL import Image
import os
import sys

# Append parent dir to path so we can import claw_vision
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import claw_vision

def test_get_window_bounds_invalid():
    """Test get_window_bounds raises ValueError for invalid coords"""
    with patch('claw_vision.ctypes.windll.user32.GetWindowRect') as mock_rect:
        mock_rect.return_value = 1
        def side_effect(hwnd, rect_ptr):
            rect_ptr._obj.left = 11000
            rect_ptr._obj.top = 0
            rect_ptr._obj.right = 100
            rect_ptr._obj.bottom = 100
            return 1
        mock_rect.side_effect = side_effect
        with pytest.raises(ValueError):
            claw_vision.get_window_bounds(123)

def test_get_window_bounds_failure():
    """Test get_window_bounds raises ValueError when GetWindowRect fails"""
    with patch('claw_vision.ctypes.windll.user32.GetWindowRect', return_value=0):
        with pytest.raises(ValueError, match="Nao foi possivel obter limites"):
            claw_vision.get_window_bounds(123)

def test_capture_window_area_invalid_bounds():
    """Test capture_window_area raises ValueError for invalid area"""
    with pytest.raises(ValueError, match="Area de janela invalida"):
        claw_vision.capture_window_area((100, 100, 50, 50))

def test_save_window_thumbnail(tmp_path):
    """Test save_window_thumbnail properly resizes and saves"""
    img = Image.new('RGB', (800, 600), color='red')
    out_path = os.path.join(tmp_path, "thumb.png")
    saved_path = claw_vision.save_window_thumbnail(img, out_path, max_width=320)
    assert saved_path == out_path
    assert os.path.exists(out_path)
    
    saved_img = Image.open(out_path)
    assert saved_img.size == (320, 240)

def test_scan_active_window_no_hwnd():
    with patch('claw_vision.get_active_window_handle', return_value=0):
        with pytest.raises(ValueError, match="Nenhuma janela ativa"):
            claw_vision.scan_active_window()

def test_detect_visual_controls_basic():
    """Test visual control detection with a basic image"""
    img = Image.new('RGB', (100, 100), color='white')
    # Draw a black rectangle to simulate a control
    from PIL import ImageDraw
    draw = ImageDraw.Draw(img)
    draw.rectangle([20, 20, 80, 40], fill="black")
    
    controls = claw_vision.detect_visual_controls(img)
    assert isinstance(controls, list)
