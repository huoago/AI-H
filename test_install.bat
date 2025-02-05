@echo off
echo 正在测试安装环境...

REM 检查Python环境
python --version
if errorlevel 1 (
    echo Python未安装或未添加到PATH
    exit /b 1
)

REM 检查Tesseract
where tesseract >nul 2>nul
if errorlevel 1 (
    echo Tesseract未安装或未添加到PATH
    echo 请安装Tesseract-OCR并设置环境变量
    exit /b 1
)

REM 安装依赖
echo 正在安装依赖...
pip install -r requirements.txt

REM 运行安装测试
echo 正在运行安装测试...
python src/tests/test_installation.py

REM 构建程序
echo 正在构建程序...
python build_release.py

REM 测试安装程序
echo 正在测试安装程序...
cd release\installer
start /wait AI文章生成助手_安装程序_v0.1.0.exe /SILENT /SUPPRESSMSGBOXES

REM 测试运行程序
echo 正在测试程序运行...
cd "C:\Program Files\AI文章生成助手"
start /wait AI文章生成助手.exe

echo 测试完成！
pause 