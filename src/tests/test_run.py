import unittest
from pathlib import Path
import sys
import os

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.run import run_app
from ai_article_generator.utils.config_manager import ConfigManager

class TestRun(unittest.TestCase):
    def setUp(self):
        self.test_file = Path('test_input.txt')
        self.test_file.write_text('这是测试文本。', encoding='utf-8')
        
    def tearDown(self):
        if self.test_file.exists():
            self.test_file.unlink()
            
        # 清理输出文件
        output_dir = Path('output')
        if output_dir.exists():
            for file in output_dir.glob('*'):
                file.unlink()
            output_dir.rmdir()
            
    def test_basic_run(self):
        """测试基本运行"""
        self.assertTrue(run_app())
        
    def test_config_loading(self):
        """测试配置加载"""
        config = ConfigManager()
        self.assertIsNotNone(config.get('model.name'))
        
    def test_article_generation(self):
        """测试文章生成"""
        from ai_article_generator.core.article_generator import ArticleGenerator
        
        generator = ArticleGenerator()
        result = generator.generate(str(self.test_file), '新闻')
        
        self.assertIsNotNone(result)
        self.assertTrue(len(result) > 0)

if __name__ == '__main__':
    unittest.main() 