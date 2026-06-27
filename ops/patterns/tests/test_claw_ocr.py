import pytest
import sys
import os
from unittest.mock import patch, MagicMock
from PIL import Image

# Add parent directory to sys.path to allow importing claw_ocr
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import claw_ocr

def test_extract_text_from_image_no_hwnd_no_tesseract():
    # If no tesseract and hwnd <= 0, should raise ValueError
    img = Image.new('RGB', (10, 10))
    with patch('claw_ocr.HAS_TESSERACT', False):
        with pytest.raises(ValueError, match="Falha no OCR: Tesseract não está disponível/falhou e nenhum HWND Win32 válido foi fornecido para fallback."):
            claw_ocr.extract_text_from_image(img, hwnd=0)

def test_extract_text_from_image_fallback_win32():
    img = Image.new('RGB', (10, 10))
    mock_controls = [{"text": "MockText", "box": (0, 0, 10, 10), "center_coord": (5, 5)}]
    
    with patch('claw_ocr.HAS_TESSERACT', False), \
         patch('claw_ocr.get_child_controls_win32', return_value=mock_controls):
        result = claw_ocr.extract_text_from_image(img, hwnd=123)
        assert result.raw_text == "MockText"
        assert len(result.regions) == 1
        assert result.regions[0].text == "MockText"

@patch('claw_ocr.HAS_TESSERACT', True)
@patch('claw_ocr.pytesseract.image_to_data')
def test_extract_text_from_image_tesseract(mock_image_to_data):
    mock_data = {
        'text': ['Test', ''],
        'conf': ['90', '-1'],
        'left': [10, 0],
        'top': [10, 0],
        'width': [50, 0],
        'height': [20, 0]
    }
    mock_image_to_data.return_value = mock_data
    
    img = Image.new('RGB', (100, 100))
    result = claw_ocr.extract_text_from_image(img, hwnd=0)
    assert "Test" in result.raw_text
    assert len(result.regions) == 1
    assert result.regions[0].text == "Test"
    assert result.regions[0].confidence == 0.9

@patch('claw_ocr.HAS_TESSERACT', True)
@patch('claw_ocr.pytesseract.image_to_data', side_effect=Exception("Tesseract Error"))
def test_extract_text_from_image_tesseract_failure(mock_image_to_data):
    img = Image.new('RGB', (100, 100))
    with pytest.raises(ValueError, match="O Tesseract falhou e nenhum HWND de fallback foi fornecido"):
        claw_ocr.extract_text_from_image(img, hwnd=0)

def test_get_child_controls_win32_invalid_hwnd():
    # Calling get_child_controls_win32 with an invalid HWND should fail and raise ValueError
    with patch('ctypes.windll.user32.GetWindowRect', return_value=0):
        with pytest.raises(ValueError, match="HWND inválido ou inacessível em get_child_controls_win32"):
            claw_ocr.get_child_controls_win32(999999)
