import unittest
from pathlib import Path
import sys

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.utils.init_env import init_project_env
from src.utils.config_manager import ConfigManager
from src.core.file_processor import FileProcessor
from src.core.article_generator import ArticleGenerator

class TestBasicFunctions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        init_project_env()
        cls.config = ConfigManager()
        
    def test_config_loading(self):
        """测试配置加载"""
        self.assertIsNotNone(self.config.get('model.name'))
        
    def test_file_processor(self):
        """测试文件处理"""
        processor = FileProcessor()
        test_file = Path(__file__).parent / 'test_input.txt'
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write("这是测试文本")
        
        content = processor.process_file(str(test_file))
        self.assertIsNotNone(content)
        
    def test_article_generator(self):
        """测试文章生成"""
        generator = ArticleGenerator()
        result = generator.generate("这是测试文本", "新闻稿")
        self.assertIsNotNone(result)

if __name__ == '__main__':
    unittest.main() 