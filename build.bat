@echo off
REM Windows batch file to build vchop executable

echo === vchop Windows Build Script ===

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python and try again
    pause
    exit /b 1
)

REM Run the build script
echo Running build script...
python build.py

if errorlevel 1 (
    echo Build failed!
    pause
    exit /b 1
)

echo.
echo Build completed successfully!
echo The executable is available in the dist\ directory.
echo.
pause