# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['Capstone_Project.py'],
    pathex=[],
    binaries=[],
    datas=[('/Users/huntergoat/Documents/Data Science /client_secret_667734235339-8dcrpkkbkpl15366mmemtqi6ls75mpcr.apps.googleusercontent.com.json', '.')],
    hiddenimports=[],
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
    name='Capstone_Project',
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
