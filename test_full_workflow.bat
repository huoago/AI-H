@echo off
echo === 开始全流程测试 ===

REM 检查Python环境
python --version
if errorlevel 1 (
    echo Python未安装或未添加到PATH
    exit /b 1
)

REM 安装依赖
pip install -r requirements.txt

REM 运行环境检查
python src/utils/check_env.py

REM 创建图标
python src/utils/create_icon.py

REM 运行完整测试
python src/tests/test_full_workflow.py

REM 显示测试报告
type full_workflow_test_report.txt

echo.
echo === 测试完成 ===
pause 