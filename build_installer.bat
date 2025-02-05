@echo off
echo 正在构建exe文件...
python build_exe.py

echo 正在创建安装程序...
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer.iss

echo 完成！
pause 