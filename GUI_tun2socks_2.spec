# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['GUI_tun2socks_2.py'],
    pathex=[],
    binaries=[],
    datas=[('proxy.txt', '.'), ('dns-saved.txt', '.'), ('def-gw-info.txt', '.'), ('tun_if.txt', '.'), ('tun2socks-windows-amd64.exe', '.'), ('tun2socks.exe', '.'), ('wintun.dll', '.'), ('VEthernet.dll', '.'), ('libtcpip.dll', '.'), ('libasio.dll', '.'), ('animation.gif', '.'), ('icon.ico', '.'), ('icon.png', '.'), ('background.png', '.'), ('w20', 'w20'), ('dnscrypt-proxy', 'dnscrypt-proxy'), ('Driver', 'Driver'), ('fakestun', 'fakestun')],
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
    [],
    exclude_binaries=True,
    name='GUI_tun2socks_2',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    uac_admin=True,
    icon=['icon.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='GUI_tun2socks_2',
)
