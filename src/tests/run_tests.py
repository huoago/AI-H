import sys
from pathlib import Path
import unittest

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.utils.check_env import setup_environment

def run_all_tests():
    """运行所有测试"""
    # 首先检查环境
    if not setup_environment():
        print("环境检查失败，请先安装所需依赖")
        return False
        
    # 加载所有测试
    loader = unittest.TestLoader()
    start_dir = Path(__file__).parent
    suite = loader.discover(start_dir)
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()

if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1) 