@echo off
echo =============================================
echo          扭蛋机应用程序启动器
echo =============================================
echo.
echo 正在检查Python环境...

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未检测到Python，请先安装Python 3.6+
    echo 您可以从 https://www.python.org/downloads/ 下载安装
    echo.
    pause
    exit /b 1
)

echo [成功] 检测到Python环境
echo 正在检查tkinter...

python -c "import tkinter" >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未检测到tkinter库
    echo tkinter是Python的标准GUI库，需要在安装Python时勾选"tcl/tk and IDLE"选项
    echo 请重新安装Python，确保包含tkinter组件
    echo.
    pause
    exit /b 1
)

echo [成功] 检测到tkinter
echo 正在检查其他依赖包...

python -c "from PIL import Image" >nul 2>&1
if %errorlevel% neq 0 (
    echo [提示] 正在安装依赖包...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo [错误] 依赖包安装失败
        echo.
        pause
        exit /b 1
    )
)

echo [成功] 依赖包检查完成
echo.
echo =============================================
echo          正在启动扭蛋机应用...
echo =============================================
echo.

python run_gacha.py

if %errorlevel% neq 0 (
    echo.
    echo [错误] 应用程序异常退出，错误码: %errorlevel%
    echo.
    pause
    exit /b %errorlevel%
)

exit /b 0 