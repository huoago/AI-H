@echo off
echo 正在测试卸载过程...

REM 查找卸载程序
set "UNINSTALL_EXE=C:\Program Files\AI文章生成助手\unins000.exe"

if exist "%UNINSTALL_EXE%" (
    echo 正在卸载程序...
    start /wait "%UNINSTALL_EXE%" /SILENT /SUPPRESSMSGBOXES
    
    REM 检查是否完全卸载
    if exist "C:\Program Files\AI文章生成助手" (
        echo 卸载可能未完全完成
        exit /b 1
    ) else (
        echo 卸载成功
    )
) else (
    echo 未找到卸载程序
    exit /b 1
)

echo 测试完成！
pause 