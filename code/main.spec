# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

import os
import skrf as rf


a = Analysis(['main.py'],
             pathex=['D:\\python_test\\python-smith-chart-antenna-matching\\code'],
             binaries=[],
             datas=[(os.path.join(os.path.dirname(rf.__file__), 'data/*'), 'skrf/data/')],
             hiddenimports=[],
             hookspath=[],
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
          [],
          exclude_binaries=True,
          name='main',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='main')
