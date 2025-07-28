# Build Instructions for vchop

This document explains how to create a standalone executable and Windows installer for vchop.

## Prerequisites

### For Building Executable
- Python 3.7 or higher
- All dependencies installed: `pip install -r requirements.txt`
- PyInstaller (automatically installed by build script)

### For Creating Windows Installer (Windows only)
- NSIS (Nullsoft Scriptable Install System) installed
- Download from: https://nsis.sourceforge.io/Main_Page

## Building the Executable

### Method 1: Using Python Build Script (Recommended)

#### On Windows:
```batch
build.bat
```

#### On Linux/macOS:
```bash
python build.py
```

### Method 2: Manual PyInstaller Command
```bash
# Install PyInstaller first
pip install pyinstaller

# Build with spec file
pyinstaller vchop.spec --clean
```

The executable will be created in the `dist/` directory:
- Windows: `dist/vchop.exe`
- Linux/macOS: `dist/vchop`

## Creating Windows Installer

### Prerequisites
1. Build the executable first (see above)
2. Install NSIS from https://nsis.sourceforge.io/Main_Page

### Building the Installer

1. Open command prompt in the vchop directory
2. Run NSIS compiler:
```batch
"C:\Program Files (x86)\NSIS\makensis.exe" vchop.nsi
```

Or use the NSIS GUI:
1. Right-click on `vchop.nsi`
2. Select "Compile NSIS Script"

The installer will be created as `vchop-1.0.0-setup.exe`

## Build Output

### Executable
- **Size**: ~130-140 MB (includes Python runtime and all dependencies)
- **Dependencies**: Self-contained, no external dependencies needed
- **Platforms**: Windows (.exe), Linux, macOS

### Installer Features
- **Start Menu shortcuts**: Creates application shortcuts in Start Menu
- **Desktop shortcut**: Optional desktop shortcut
- **Uninstaller**: Automatic uninstall capability
- **Registry entries**: Proper Add/Remove Programs integration
- **Upgrade handling**: Automatically removes previous versions

## Customization

### Build Configuration
Edit `vchop.spec` to customize:
- Hidden imports
- Excluded modules
- Icon file
- Console/windowed mode

### Installer Configuration
Edit `vchop.nsi` to customize:
- Version information
- Install directory
- Shortcuts
- License file
- Application icon

## Troubleshooting

### Build Issues
- **Missing modules**: Add to `hiddenimports` in `vchop.spec`
- **Large file size**: Add modules to `excludes` in `vchop.spec`
- **Import errors**: Check console output for missing dependencies

### Installer Issues
- **NSIS not found**: Install NSIS and add to PATH
- **Missing executable**: Build executable first
- **Permission errors**: Run as administrator

## File Structure

```
vchop/
├── build.py          # Python build script
├── build.bat         # Windows build script
├── vchop.spec        # PyInstaller specification
├── vchop.nsi         # NSIS installer script
├── dist/             # Build output directory
│   └── vchop[.exe]   # Standalone executable
└── build/            # PyInstaller build cache
```

## Notes

- The executable is completely standalone and includes the Python runtime
- First run may be slower due to PyInstaller's extraction process
- The installer handles proper Windows integration and uninstallation
- Build artifacts are excluded from git via `.gitignore`