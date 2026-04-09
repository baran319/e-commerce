# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['run_exe.py'],
    pathex=[],
    binaries=[],
    datas=[('app/templates', 'app/templates'), ('app/static', 'app/static'), ('instance', 'instance')],
    hiddenimports=['flask', 'flask_sqlalchemy', 'flask_login', 'flask_wtf', 'flask_migrate', 'email_validator', 'wtforms', 'werkzeug', 'sqlalchemy', 'jinja2', 'click', 'itsdangerous', 'dotenv'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
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
    name='FitMarket',
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
