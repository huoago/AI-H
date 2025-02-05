import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.utils.init_env import init_project_env
from src.utils.config_manager import ConfigManager
from src.core.article_generator import ArticleGenerator
import logging

def test_environment():
    """测试环境初始化"""
    try:
        # 初始化环境
        if not init_project_env():
            print("环境初始化失败")
            return False
            
        print("环境初始化成功")
        return True
    except Exception as e:
        print(f"测试失败: {str(e)}")
        return False

def test_model():
    """测试模型加载"""
    try:
        generator = ArticleGenerator()
        print("模型加载成功")
        return True
    except Exception as e:
        print(f"模型加载失败: {str(e)}")
        return False

def main():
    print("开始测试...")
    
    # 测试环境初始化
    if not test_environment():
        return
        
    # 测试模型加载
    if not test_model():
        return
        
    print("测试完成")

if __name__ == '__main__':
    main() 