# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['c1sc.py'],
    pathex=[],
    binaries=[],
    datas=[('Keysight-Logo.png', '.'), ('switch_connector_name_dict.py', '.'), ('manual_switch_control.py', '.')],
    hiddenimports=['kivy', 'kivy.core', 'kivy.uix', 'kivy.graphics', 'kivy_deps.angle', 'kivy_deps.glew', 'kivy_deps.sdl2', 'enchant'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='SwitchApp',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
