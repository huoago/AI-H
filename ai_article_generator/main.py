import sys
import os
from pathlib import Path
from PyQt5.QtWidgets import QApplication
from .ui.main_window import MainWindow
from .utils.init_env import init_project_env
from .utils.config_manager import ConfigManager
import logging

def main():
    try:
        # 初始化环境
        if not init_project_env():
            sys.exit(1)
            
        # 初始化配置
        config = ConfigManager()
        
        # 创建应用
        app = QApplication(sys.argv)
        
        # 创建主窗口
        window = MainWindow()
        
        # 设置窗口标题和大小
        window.setWindowTitle(config.get('ui.window_title', 'AI文章生成助手'))
        size = config.get('ui.window_size', {'width': 1000, 'height': 800})
        window.setGeometry(100, 100, size['width'], size['height'])
        
        window.show()
        
        # 运行应用
        sys.exit(app.exec_())
        
    except Exception as e:
        logging.error(f"程序启动失败: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main() 