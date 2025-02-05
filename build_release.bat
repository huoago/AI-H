@echo off
echo === 开始构建发布版本 ===

REM 检查Python环境
python --version
if errorlevel 1 (
    echo Python未安装或未添加到PATH
    exit /b 1
)

REM 安装依赖
pip install -r requirements.txt
pip install pyinstaller

REM 运行环境检查
python src/utils/check_env.py

REM 创建图标
python src/utils/create_icon.py

REM 打包程序
python src/build_exe.py

REM 创建发布包
if exist dist (
    echo 正在创建发布包...
    
    REM 创建发布目录
    mkdir release 2>nul
    
    REM 复制文件到发布目录
    xcopy /E /I /Y dist\AI文章生成助手 release\AI文章生成助手
    copy 启动AI文章生成助手.bat release\
    copy README.md release\
    copy requirements.txt release\
    
    REM 创建压缩包
    powershell Compress-Archive -Path release\* -DestinationPath AI文章生成助手_v1.0.0.zip -Force
    
    echo 发布包已创建：AI文章生成助手_v1.0.0.zip
) else (
    echo 构建失败！
)

echo.
echo === 构建完成 ===
pause 