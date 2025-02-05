@echo off
echo === 开始完整安装测试 ===

REM 安装必要的Python包
pip install psutil

REM 运行完整测试
python src/tests/test_full_installation.py

REM 显示测试报告
type installation_test_report.txt

echo.
echo === 测试完成 ===
pause 