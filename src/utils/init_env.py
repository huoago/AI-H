import os
import logging
from pathlib import Path

def init_project_env():
    """初始化项目环境"""
    # 创建项目目录结构
    project_dirs = [
        'logs',
        'models',
        'templates',
        'config',
        'output'
    ]
    
    try:
        # 获取项目根目录
        root_dir = Path(__file__).parent.parent
        
        # 创建必要的目录
        for dir_name in project_dirs:
            dir_path = root_dir / dir_name
            dir_path.mkdir(exist_ok=True)
            
        # 设置日志
        log_dir = root_dir / 'logs'
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s [%(levelname)s] %(message)s',
            handlers=[
                logging.FileHandler(log_dir / 'app.log', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        
        return True
    except Exception as e:
        print(f"初始化环境失败: {str(e)}")
        return False 