# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['mecha_app.py'],
    pathex=['patterns'],
    binaries=[],
    datas=[('patterns', 'patterns'), ('mecha.html', '.'), ('templates', 'templates'), ('assets', 'assets')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['torch', 'tensorflow', 'numpy', 'pandas', 'matplotlib', 'scipy', 'tensorboard', 'onnx', 'sympy', 'jinja2'],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='mecha_app',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
