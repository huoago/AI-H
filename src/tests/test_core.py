import unittest
from pathlib import Path
import sys

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.core.article_generator import ArticleGenerator
from src.core.file_processor import FileProcessor

class TestCore(unittest.TestCase):
    def setUp(self):
        self.generator = ArticleGenerator()
        self.processor = FileProcessor()
        
    def test_article_generation(self):
        """测试文章生成"""
        input_text = "这是一个测试文本。"
        result = self.generator.generate(input_text, "新闻")
        self.assertIsNotNone(result)
        self.assertTrue(len(result) > 0)
        
    def test_file_processing(self):
        """测试文件处理"""
        # 创建测试文件
        test_file = Path("test.txt")
        test_file.write_text("测试内容", encoding='utf-8')
        
        try:
            result = self.processor.process_file(str(test_file))
            self.assertIsNotNone(result)
            self.assertTrue(len(result) > 0)
        finally:
            test_file.unlink()

if __name__ == '__main__':
    unittest.main() 