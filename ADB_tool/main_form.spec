# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['main_da.py,\\main_form.py'],
    pathex=['.\\adb_test_function\\customize_main.py,.\\adb_test_function\\linux_carmera_pywinauto.py,.\\adb_test_function\\linux_main.py,.\\adb_test_function\\public.py,.\\adb_test_function\\quickly.py,.\\adb_test_function\\screen_record.py'],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='main_form',
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
    icon='my-da.ico',
)
