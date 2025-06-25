@echo off
chcp 65001 >nul
setlocal EnableDelayedExpansion

echo =============================================
echo          Gacha Machine Application Launcher
echo =============================================
echo          Version 2.0 - Smart Installation
echo =============================================
echo.

:: Change to script directory
cd /d "%~dp0"
echo [INFO] Working directory: %CD%
echo.

echo [STEP 1/6] Comprehensive Python Detection...
echo.

:: Method 1: Check if python command works
echo [CHECK] Testing 'python' command...
python --version >nul 2>&1
if %errorlevel% == 0 (
    for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
    echo [SUCCESS] Python !PYTHON_VERSION! found via 'python' command
    set PYTHON_CMD=python
    goto :python_found
)

:: Method 2: Check if py launcher works
echo [CHECK] Testing 'py' launcher...
py --version >nul 2>&1
if %errorlevel% == 0 (
    for /f "tokens=2" %%i in ('py --version 2^>^&1') do set PYTHON_VERSION=%%i
    echo [SUCCESS] Python !PYTHON_VERSION! found via 'py' launcher
    set PYTHON_CMD=py
    goto :python_found
)

:: Method 3: Check common installation paths
echo [CHECK] Searching common Python installation paths...
set PYTHON_PATHS[0]=C:\Python3*\python.exe
set PYTHON_PATHS[1]=C:\Python4*\python.exe
set PYTHON_PATHS[2]=%LOCALAPPDATA%\Programs\Python\Python3*\python.exe
set PYTHON_PATHS[3]=%PROGRAMFILES%\Python3*\python.exe
set PYTHON_PATHS[4]=%PROGRAMFILES(X86)%\Python3*\python.exe

for /L %%i in (0,1,4) do (
    for %%j in (!PYTHON_PATHS[%%i]!) do (
        if exist "%%j" (
            for /f "tokens=2" %%v in ('"%%j" --version 2^>^&1') do set PYTHON_VERSION=%%v
            echo [SUCCESS] Python !PYTHON_VERSION! found at: %%j
            set PYTHON_CMD="%%j"
            goto :python_found
        )
    )
)

:: Python not found - provide installation guidance
echo [ERROR] Python not detected on this system
echo.
echo ========== PYTHON INSTALLATION REQUIRED ==========
echo.
echo This application requires Python 3.6 or higher to run.
echo.
echo [OPTION 1] Download from Official Website:
echo   1. Visit: https://www.python.org/downloads/
echo   2. Download the latest Python 3.x version
echo   3. During installation, IMPORTANT:
echo      ✓ Check "Add Python to PATH" 
echo      ✓ Check "Install for all users" (optional)
echo      ✓ Check "tcl/tk and IDLE" (required for GUI)
echo.
echo [OPTION 2] Download via Microsoft Store:
echo   1. Open Microsoft Store
echo   2. Search for "Python 3"
echo   3. Install "Python 3.x" by Python Software Foundation
echo.
echo [OPTION 3] Auto-download (if available):
set /p auto_install="Would you like to try automatic download? (y/n): "
if /i "%auto_install%"=="y" (
    echo [INFO] Attempting to download Python installer...
    goto :auto_download_python
)

echo.
echo Please install Python and run this script again.
pause
exit /b 1

:auto_download_python
echo [INFO] Checking for winget (Windows Package Manager)...
winget --version >nul 2>&1
if %errorlevel% == 0 (
    echo [SUCCESS] Winget found, attempting Python installation...
    echo [INFO] This may take several minutes...
    winget install Python.Python.3.11 --silent --accept-package-agreements --accept-source-agreements
    if !errorlevel! == 0 (
        echo [SUCCESS] Python installation completed!
        echo [INFO] Please restart this script to continue.
        pause
        exit /b 0
    ) else (
        echo [WARNING] Automatic installation failed.
        echo Please install Python manually using Option 1 or 2 above.
        pause
        exit /b 1
    )
) else (
    echo [INFO] Winget not available, cannot auto-install.
    echo Please install Python manually using Option 1 or 2 above.
    pause
    exit /b 1
)

:python_found
echo.
echo [STEP 2/6] Python version check skipped
echo [INFO] Using detected Python installation
echo.

echo [STEP 3/6] Checking tkinter...
%PYTHON_CMD% -c "import tkinter; print('tkinter version:', tkinter.TkVersion)" >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] tkinter library not detected
    echo.
    echo tkinter is required for the GUI interface.
    echo [SOLUTION] Reinstall Python and ensure "tcl/tk and IDLE" is selected
    echo.
    pause
    exit /b 1
)
echo [SUCCESS] tkinter detected and working
echo.

echo [STEP 4/6] Checking project files...
if not exist "requirements.txt" (
    echo [ERROR] requirements.txt not found
    echo Please ensure you're running this script from the project root directory
    pause
    exit /b 1
)

if not exist "run_gacha.py" (
    echo [ERROR] run_gacha.py not found
    echo Please ensure you're running this script from the project root directory
    pause
    exit /b 1
)

if not exist "gacha_app" (
    echo [ERROR] gacha_app directory not found
    echo Please ensure all project files are present
    pause
    exit /b 1
)
echo [SUCCESS] All project files verified
echo.

echo [STEP 5/6] Installing/Checking dependencies...
echo [INFO] Upgrading pip to latest version...
%PYTHON_CMD% -m pip install --upgrade pip --quiet >nul 2>&1

echo [INFO] Checking Pillow...
%PYTHON_CMD% -c "from PIL import Image; print('Pillow:', Image.__version__)" >nul 2>&1
set pillow_status=%errorlevel%

echo [INFO] Checking matplotlib...
%PYTHON_CMD% -c "import matplotlib; print('matplotlib:', matplotlib.__version__)" >nul 2>&1
set matplotlib_status=%errorlevel%

if %pillow_status% neq 0 (
    echo [INFO] Installing Pillow...
    %PYTHON_CMD% -m pip install Pillow>=9.0.0
    if !errorlevel! neq 0 (
        echo [ERROR] Failed to install Pillow
        echo [TIP] Try: %PYTHON_CMD% -m pip install --upgrade pip
        pause
        exit /b 1
    )
)

if %matplotlib_status% neq 0 (
    echo [INFO] Installing matplotlib...
    %PYTHON_CMD% -m pip install matplotlib>=3.5.0
    if !errorlevel! neq 0 (
        echo [ERROR] Failed to install matplotlib
        echo [TIP] Try: %PYTHON_CMD% -m pip install --upgrade pip
        pause
        exit /b 1
    )
)

:: Final dependency check
echo [INFO] Final dependency verification...
%PYTHON_CMD% -m pip install -r requirements.txt --quiet
if %errorlevel% neq 0 (
    echo [WARNING] Some dependencies might not be installed correctly
    echo [INFO] Attempting manual installation...
    %PYTHON_CMD% -m pip install -r requirements.txt
    if !errorlevel! neq 0 (
        echo [ERROR] Failed to install dependencies
        echo [TIP] Try running: %PYTHON_CMD% -m pip install --upgrade pip
        pause
        exit /b 1
    )
)
echo [SUCCESS] All dependencies installed successfully
echo.

echo [STEP 6/6] Starting Gacha Machine Application...
echo =============================================
echo          Launching Application...
echo =============================================
echo.

%PYTHON_CMD% run_gacha.py

set app_exit_code=%errorlevel%
echo.

if %app_exit_code% neq 0 (
    echo [ERROR] Application exited with error code: %app_exit_code%
    echo.
    if %app_exit_code% == 1 (
        echo [CAUSE] Import error - missing dependencies
        echo [SOLUTION] Try reinstalling: %PYTHON_CMD% -m pip install -r requirements.txt
    ) else if %app_exit_code% == 2 (
        echo [CAUSE] Runtime error
        echo [SOLUTION] Check the error details above
    ) else (
        echo [CAUSE] Unexpected error
        echo [SOLUTION] Please check the console output above
    )
    echo.
    pause
    exit /b %app_exit_code%
) else (
    echo [SUCCESS] Application closed normally
)

echo.
echo ===============================================
echo    Thank you for using Gacha Machine! 🎲
echo ===============================================
timeout /t 3 /nobreak >nul
exit /b 0 