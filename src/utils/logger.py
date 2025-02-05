import logging
import os
from datetime import datetime

def setup_logger():
    """设置日志配置"""
    # 创建logs目录
    if not os.path.exists('logs'):
        os.makedirs('logs')
        
    # 设置日志文件名
    log_file = f'logs/app_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
    
    # 配置日志
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    ) 