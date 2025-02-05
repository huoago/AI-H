import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.utils.init_env import init_project_env
from src.main import main
import logging

if __name__ == '__main__':
    try:
        # 初始化环境
        if not init_project_env():
            print("环境初始化失败")
            sys.exit(1)
            
        # 运行主程序
        main()
    except Exception as e:
        logging.error(f"程序启动失败: {str(e)}")
        print(f"错误: {str(e)}")
        sys.exit(1) 