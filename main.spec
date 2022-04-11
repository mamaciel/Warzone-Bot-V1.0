# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['C:/Users/marco/Documents/Warzone Stats Bot V1.0/main.py'],
             pathex=['C:/Users/marco/Documents/Warzone Stats Bot V1.0/dist/main/cv2', 'C:/Users/marco/anaconda3/Lib/site-packages/numpy'],
             binaries=[],
             datas=[('C:/Users/marco/Documents/Warzone Stats Bot V1.0/Pictures uncropped', 'Pictures uncropped/'), ('C:/Users/marco/Documents/Warzone Stats Bot V1.0/Pictures for WZ bot', 'Pictures for WZ bot/'), ('C:/Users/marco/Documents/Warzone Stats Bot V1.0/assets', 'assets/'), ('C:/Users/marco/Documents/Warzone Stats Bot V1.0/1ex.png', '.'), ('C:/Users/marco/Documents/Warzone Stats Bot V1.0/2ex.png', '.'), ('C:/Users/marco/Documents/Warzone Stats Bot V1.0/3ex.png', '.'), ('C:/Users/marco/Documents/Warzone Stats Bot V1.0/4ex.png', '.'), ('C:/Users/marco/Documents/Warzone Stats Bot V1.0/5ex.png', '.'), ('C:/Users/marco/Documents/Warzone Stats Bot V1.0/6ex.png', '.'), ('C:/Users/marco/Documents/Warzone Stats Bot V1.0/7ex.png', '.'), ('C:/Users/marco/Documents/Warzone Stats Bot V1.0/8ex.png', '.'), ('C:/Users/marco/Documents/Warzone Stats Bot V1.0/11ex.png', '.'), ('C:/Users/marco/Documents/Warzone Stats Bot V1.0/13ex.png', '.'), ('C:/Users/marco/Documents/Warzone Stats Bot V1.0/14example.png', '.'), ('C:/Users/marco/Documents/Warzone Stats Bot V1.0/screenshot2.png', '.')],
             hiddenimports=['numpy'],
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
          [],
          exclude_binaries=True,
          name='main',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None , icon='C:\\Users\\marco\\Documents\\Warzone Stats Bot V1.0\\icon.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas, 
               strip=False,
               upx=True,
               upx_exclude=[],
               name='main')
