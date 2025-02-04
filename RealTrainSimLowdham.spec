# -*- mode: python -*-
import os
block_cipher = None


a = Analysis([os.path.join("./RealTrainSimLowdham", 'main.py')],
             pathex=[],
             binaries=None,
             datas=None,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='RealTrainSimLowdham',
          debug=True,
          strip=False,
          upx=True,
          console=True,
		  # icon='Favicon.ico',
		  version='version.txt')
