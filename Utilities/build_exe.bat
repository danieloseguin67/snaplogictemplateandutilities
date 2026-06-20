@echo off
setlocal

set SCRIPT=translate_pipeline_description_to_md.py
set APP_NAME=translate_pipeline_description_to_md
set OUTPUT_DIR=dist
set BUILD_DIR=build

echo ============================================
echo  Building EXE for %APP_NAME%
echo ============================================

:: Check Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found on PATH. Please install Python and try again.
    exit /b 1
)

:: Install PyInstaller if not already installed
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo PyInstaller not found. Installing...
    pip install pyinstaller
    if errorlevel 1 (
        echo ERROR: Failed to install PyInstaller.
        exit /b 1
    )
)

:: Build as a directory bundle (--onedir) so we can patch the Tcl files afterward.
:: PyInstaller may bundle an init.tcl that requires a different Tcl version than the
:: DLL installed with Anaconda. We fix this with a post-build patch (see below).
echo.
echo Running PyInstaller...
pyinstaller --clean --onedir --windowed --name %APP_NAME% "%SCRIPT%"

if errorlevel 1 (
    echo.
    echo ERROR: Build failed.
    exit /b 1
)

:: Post-build: replace the bundled init.tcl with the one from the active Python's Tcl
:: installation. PyInstaller sometimes bundles an init.tcl that requires a newer Tcl
:: version than the DLL shipped with Anaconda, causing a runtime version conflict.
:: Copying the correct init.tcl from Anaconda's Library\lib\tcl8.6 fixes the mismatch.
echo.
echo Patching bundled init.tcl to match installed Tcl DLL version...
python "%~dp0patch_tcl_init.py" "%OUTPUT_DIR%\%APP_NAME%"
if errorlevel 1 (
    echo WARNING: init.tcl patch step failed - EXE may still crash on startup.
)

echo.
echo ============================================
echo  Build complete!
echo  EXE location: %OUTPUT_DIR%\%APP_NAME%\%APP_NAME%.exe
echo ============================================

endlocal
