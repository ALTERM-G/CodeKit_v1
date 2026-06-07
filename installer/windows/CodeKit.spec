# -*- mode: python ; coding: utf-8 -*-
import os
import pyfiglet

# Get the path to the pyfiglet library
pyfiglet_path = os.path.dirname(pyfiglet.__file__)

a = Analysis(
    ['src\\main.py'],
    pathex=['src'],
    binaries=[],
    datas=[
        ('assets', 'assets'), # Your app's assets
        ('data', 'data'),     # Your app's data
        (os.path.join(pyfiglet_path, 'fonts'), 'pyfiglet/fonts') # Add pyfiglet fonts
    ],
    hiddenimports=[],
    hookspath=['hooks'],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    cipher=None,
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='CodeKit',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    icon='assets\\icons\\alterm-app.png',
)
