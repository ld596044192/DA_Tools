# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['main_adb.py'],
             pathex=['.\\public.py,.\\quickly.py,.\\main_form.py,.\\screen_record.py,.\\linux_main.py,.\\pywinauto_adb.py'],
             binaries=[],
             datas=[('icon','icon'),('version','version'),('temp','temp'),('resources','resources')],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,  
          [],
          name='main_adb',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None , icon='adb.ico')
