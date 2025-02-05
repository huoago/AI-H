@echo off
echo === 开始构建发布包 ===

REM 检查Python环境
python --version
if errorlevel 1 (
    echo Python未安装或未添加到PATH
    exit /b 1
)

REM 检查必要工具
where pyinstaller >nul 2>nul
if errorlevel 1 (
    echo 正在安装PyInstaller...
    pip install pyinstaller
)

REM 安装依赖
pip install -r requirements.txt

REM 构建发布包
python src/build_package.py

REM 检查构建结果
if exist release (
    echo 发布包构建成功！
    echo 发布包位置：release/
    echo   - installer/: 安装程序
    echo   - portable/: 便携版
    echo   - docs/: 文档
) else (
    echo 构建失败！
)

pause 