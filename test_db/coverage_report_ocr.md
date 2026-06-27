# Coverage Report: claw_ocr.py

## Status
- **Testes Implementados:** test_claw_ocr.py
- **Framework:** pytest + unittest.mock
- **TDD / Let it Fail:** Exceptions `ValueError` simuladas rigorosamente para falhas de HWND e Tesseract sem engolir erros. A base respeita 100% o design determinístico.

## Pendências DevOps Squad (Handoff)
1. Necessidade de garantir a disponibilidade do binário `Tesseract-OCR` (pytesseract) nos runners de CI/CD para execução contínua dos testes que verificam o motor óptico além do fallback Win32.
2. Como `get_child_controls_win32` requer Windows nativo, é necessário configurar runners Windows (ex: GitHub Actions `windows-latest`) ou usar wrappers compatíveis para os testes end-to-end do módulo.
