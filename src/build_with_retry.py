import subprocess
import sys
import time
import logging
from pathlib import Path

def setup_logging():
    log_dir = Path('logs')
    log_dir.mkdir(exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.FileHandler('logs/build.log', encoding='utf-8'),
            logging.StreamHandler()
        ]
    )

def run_build(max_retries=3):
    setup_logging()
    
    for attempt in range(max_retries):
        try:
            logging.info(f"开始构建尝试 {attempt + 1}/{max_retries}")
            
            # 创建图标
            logging.info("正在创建图标...")
            subprocess.run([sys.executable, 'src/create_icon.py'], check=True)
            
            # 运行打包脚本
            logging.info("正在运行打包脚本...")
            subprocess.run(['build_package.bat'], check=True)
            
            # 检查结果
            if Path('release').exists():
                logging.info("构建成功！")
                return True
                
        except subprocess.CalledProcessError as e:
            logging.error(f"构建失败: {str(e)}")
            if attempt < max_retries - 1:
                wait_time = 5 * (attempt + 1)
                logging.info(f"等待 {wait_time} 秒后重试...")
                time.sleep(wait_time)
            else:
                logging.error("已达到最大重试次数，构建失败")
                return False
                
    return False

if __name__ == '__main__':
    success = run_build()
    sys.exit(0 if success else 1) 