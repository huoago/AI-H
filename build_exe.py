import PyInstaller.__main__
import sys
import os
from pathlib import Path

def build_exe():
    # 获取项目根目录
    root_dir = Path(__file__).parent
    
    # 定义资源文件
    datas = [
        (str(root_dir / 'ai_article_generator/config'), 'config'),
        (str(root_dir / 'ai_article_generator/templates'), 'templates'),
    ]
    
    # PyInstaller参数
    args = [
        'ai_article_generator/main.py',  # 主程序入口
        '--name=AI文章生成助手',  # 生成的exe名称
        '--windowed',  # 使用GUI模式
        '--icon=resources/icon.ico',  # 程序图标
        '--add-data=ai_article_generator/config;config',  # 添加配置文件
        '--add-data=ai_article_generator/templates;templates',  # 添加模板文件
        '--hidden-import=torch',
        '--hidden-import=transformers',
        '--hidden-import=pytesseract',
        '--hidden-import=pdfplumber',
        '--hidden-import=PIL',
        '--hidden-import=docx',
        '--hidden-import=openpyxl',
        '--hidden-import=markdown',
        '--hidden-import=pptx',
        '--hidden-import=bs4',
        '--noconfirm',  # 不确认覆盖
        '--clean',  # 清理临时文件
        '--onefile',  # 打包成单个文件
    ]
    
    # 运行PyInstaller
    PyInstaller.__main__.run(args)

if __name__ == '__main__':
    build_exe() 