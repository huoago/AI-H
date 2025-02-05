import sys
import importlib
import logging
from pathlib import Path

def check_dependencies():
    """检查依赖项是否已安装"""
    required_packages = [
        'PyQt5',
        'torch',
        'transformers',
        'pillow',
        'psutil',
        'python-docx',
        'pdfplumber',
        'python-pptx',
        'openpyxl',
        'pytesseract',
        'markdown',
        'beautifulsoup4'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            importlib.import_module(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
            
    return missing_packages

def setup_environment():
    """设置运行环境"""
    # 检查依赖
    missing = check_dependencies()
    if missing:
        print("缺少以下依赖包:")
        for package in missing:
            print(f"  - {package}")
        print("\n请运行: pip install -r requirements.txt")
        return False
        
    # 检查目录结构
    required_dirs = ['logs', 'output', 'models', 'templates']
    for dir_name in required_dirs:
        dir_path = Path(dir_name)
        dir_path.mkdir(exist_ok=True)
        
    return True

if __name__ == '__main__':
    if setup_environment():
        print("环境检查通过")
    else:
        print("环境检查失败")
        sys.exit(1) 