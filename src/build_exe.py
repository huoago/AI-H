import PyInstaller.__main__
import os
from pathlib import Path
import shutil
import json
from src.utils.create_icon import create_app_icon

def build_exe():
    """打包软件为exe"""
    print("开始打包...")
    
    # 获取项目根目录
    root_dir = Path(__file__).parent.parent
    dist_dir = root_dir / 'dist'
    build_dir = root_dir / 'build'
    
    # 清理旧的构建文件
    for dir_path in [dist_dir, build_dir]:
        if dir_path.exists():
            shutil.rmtree(dir_path)
            
    # 创建图标
    icon_path = create_app_icon()
    
    # 准备资源文件
    resources_dir = root_dir / 'resources'
    resources_dir.mkdir(exist_ok=True)
    
    # 复制配置文件
    config_dir = dist_dir / 'config'
    config_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(root_dir / 'src/config/config.json', config_dir)
    
    # 复制模板文件
    templates_dir = dist_dir / 'templates'
    templates_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(root_dir / 'src/templates/article_templates.json', templates_dir)
    
    # PyInstaller参数
    args = [
        'src/run.py',  # 主程序
        '--name=AI文章生成助手',  # 程序名称
        '--windowed',  # 无控制台窗口
        f'--icon={icon_path}',  # 图标
        '--noconfirm',  # 覆盖已存在的文件
        '--clean',  # 清理临时文件
        '--add-data=src/config;config',  # 添加配置文件
        '--add-data=src/templates;templates',  # 添加模板文件
        '--add-data=resources;resources',  # 添加资源文件
        '--hidden-import=torch',  # 添加隐藏导入
        '--hidden-import=transformers',
        '--hidden-import=PIL',
        '--hidden-import=pytesseract',
        '--collect-all=torch',  # 收集所有相关文件
        '--collect-all=transformers',
        '--collect-all=pytesseract',
    ]
    
    # 运行PyInstaller
    PyInstaller.__main__.run(args)
    
    print("打包完成！")
    
    # 创建启动器
    create_launcher()
    
def create_launcher():
    """创建启动器"""
    launcher_script = '''
@echo off
cd /d "%~dp0"
start "" "dist\\AI文章生成助手\\AI文章生成助手.exe"
    '''.strip()
    
    with open('启动AI文章生成助手.bat', 'w', encoding='utf-8') as f:
        f.write(launcher_script)
        
if __name__ == '__main__':
    build_exe() 