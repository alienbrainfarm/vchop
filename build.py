#!/usr/bin/env python3
"""
Build script for creating a standalone vchop executable using PyInstaller.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def install_pyinstaller():
    """Install PyInstaller if not already installed."""
    try:
        import PyInstaller
        print(f"PyInstaller {PyInstaller.__version__} already installed.")
    except ImportError:
        print("Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

def clean_build_dirs():
    """Clean previous build directories."""
    dirs_to_clean = ["build", "dist"]
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            print(f"Cleaning {dir_name}/ directory...")
            shutil.rmtree(dir_name)

def create_spec_file():
    """Create PyInstaller spec file if it doesn't exist."""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['src/main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'PyQt5.QtCore',
        'PyQt5.QtGui', 
        'PyQt5.QtWidgets',
        'cv2',
        'PIL',
        'scenedetect',
        'tqdm',
    ],
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
    name='vchop',
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
    entitlements_file=None,
    icon=None,
)
'''
    
    spec_file = "vchop.spec"
    if not os.path.exists(spec_file):
        print(f"Creating {spec_file}...")
        with open(spec_file, 'w') as f:
            f.write(spec_content)
    else:
        print(f"{spec_file} already exists.")

def build_executable():
    """Build the executable using PyInstaller."""
    spec_file = "vchop.spec"
    
    print("Building executable with PyInstaller...")
    cmd = [sys.executable, "-m", "PyInstaller", spec_file, "--clean"]
    
    try:
        subprocess.check_call(cmd)
        print("Build completed successfully!")
        
        # Check if executable was created
        exe_path = Path("dist/vchop.exe" if sys.platform == "win32" else "dist/vchop")
        if exe_path.exists():
            print(f"Executable created: {exe_path}")
            print(f"Size: {exe_path.stat().st_size / (1024*1024):.1f} MB")
        else:
            print("Warning: Executable not found in expected location.")
            
    except subprocess.CalledProcessError as e:
        print(f"Build failed with error: {e}")
        sys.exit(1)

def main():
    """Main build process."""
    print("=== vchop Build Script ===")
    
    # Ensure we're in the right directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # Install PyInstaller
    install_pyinstaller()
    
    # Clean previous builds
    clean_build_dirs()
    
    # Create spec file
    create_spec_file()
    
    # Build executable
    build_executable()
    
    print("\n=== Build Complete ===")
    print("The standalone executable is available in the dist/ directory.")

if __name__ == "__main__":
    main()