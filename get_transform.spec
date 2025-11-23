# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for Get_transform
Builds a standalone executable that includes all dependencies
"""

import sys
from pathlib import Path

# Define project paths
project_root = Path(SPECPATH)
get_transform_dir = project_root / 'Get_transform'

# Analysis: scan for all imports and dependencies
a = Analysis(
    # Entry point script
    [str(get_transform_dir / 'launch.py')],
    
    # Additional paths to search for imports
    pathex=[str(get_transform_dir)],
    
    # Binary dependencies (auto-detected)
    binaries=[],
    
    # Data files to include (config templates, etc.)
    datas=[
        (str(get_transform_dir / 'requirements.txt'), 'Get_transform'),
    ],
    
    # Hidden imports (packages not auto-detected)
    hiddenimports=[
        'bs4',
        'beautifulsoup4',
        'soupsieve',
        'html.parser',
        'pathlib',
    ],
    
    # Hooks directory
    hookspath=[],
    
    # Runtime hooks
    hooksconfig={},
    runtime_hooks=[],
    
    # Exclusions (reduce size)
    excludes=[
        'tkinter',
        'matplotlib',
        'numpy',
        'pandas',
        'PIL',
        'PyQt5',
        'PyQt6',
        'PySide2',
        'PySide6',
        'wx',
    ],
    
    # Windows-specific
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    
    # Enable console for debugging
    noarchive=False,
)

# PYZ: compress Python bytecode
pyz = PYZ(a.pure, a.zipped_data)

# EXE: create executable
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='get_transform',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,  # Enable UPX compression if available
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Console application (CLI)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    
    # Windows icon (optional)
    # icon='icon.ico',
)
