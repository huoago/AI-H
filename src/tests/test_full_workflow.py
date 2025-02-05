import unittest
import sys
from pathlib import Path
import shutil
import time

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.utils.check_env import setup_environment
from src.utils.create_icon import create_app_icon
from src.core.article_generator import ArticleGenerator
from src.core.file_processor import FileProcessor
from PyQt5.QtWidgets import QApplication
from src.ui.main_window import MainWindow

class TestFullWorkflow(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """设置测试环境"""
        # 检查环境
        cls.assertTrue(setup_environment(), "环境检查失败")
        
        # 创建图标
        cls.icon_path = create_app_icon()
        cls.assertTrue(cls.icon_path.exists(), "图标创建失败")
        
        # 创建测试文件
        cls.test_dir = Path('test_files')
        cls.test_dir.mkdir(exist_ok=True)
        
        # 创建测试文本文件
        cls.text_file = cls.test_dir / 'test.txt'
        cls.text_file.write_text('这是一个测试文本，用于测试AI文章生成功能。', encoding='utf-8')
        
        # 创建测试图片
        cls.image_file = cls.test_dir / 'test.png'
        from PIL import Image, ImageDraw, ImageFont
        img = Image.new('RGB', (200, 100), color='white')
        d = ImageDraw.Draw(img)
        d.text((10, 10), "测试图片文本", fill='black')
        img.save(cls.image_file)
        
    @classmethod
    def tearDownClass(cls):
        """清理测试环境"""
        if cls.test_dir.exists():
            shutil.rmtree(cls.test_dir)
            
    def test_01_file_processing(self):
        """测试文件处理"""
        processor = FileProcessor()
        
        # 测试文本文件
        text_content = processor.process_file(self.text_file)
        self.assertIsNotNone(text_content)
        self.assertTrue(len(text_content) > 0)
        
        # 测试图片文件
        image_content = processor.process_file(self.image_file)
        self.assertIsNotNone(image_content)
        self.assertTrue(len(image_content) > 0)
        
    def test_02_article_generation(self):
        """测试文章生成"""
        generator = ArticleGenerator()
        
        # 测试不同模板
        templates = ['新闻', '博客', '论文']
        test_text = "这是测试输入文本。"
        
        for template in templates:
            result = generator.generate(test_text, template)
            self.assertIsNotNone(result)
            self.assertTrue(len(result) > 0)
            print(f"\n{template}模板生成结果:\n{result[:200]}...")
            
    def test_03_ui_workflow(self):
        """测试UI工作流"""
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        
        # 模拟用户操作
        def simulate_user_actions():
            # 输入文本
            window.input_text.setText("这是测试输入文本。")
            
            # 选择模板
            window.template_combo.setCurrentText("新闻")
            
            # 点击生成按钮
            window.generate_article()
            
            # 等待生成完成
            while window.progress.isVisible():
                time.sleep(0.1)
                QApplication.processEvents()
                
            # 检查结果
            result = window.output_text.toPlainText()
            self.assertTrue(len(result) > 0)
            print(f"\nUI生成结果:\n{result[:200]}...")
            
            # 关闭窗口
            window.close()
            
        # 使用定时器延迟执行模拟操作
        from PyQt5.QtCore import QTimer
        QTimer.singleShot(1000, simulate_user_actions)
        
        # 运行应用
        app.exec_()

def run_tests():
    # 创建测试套件
    suite = unittest.TestLoader().loadTestsFromTestCase(TestFullWorkflow)
    
    # 运行测试并生成报告
    with open('full_workflow_test_report.txt', 'w', encoding='utf-8') as f:
        runner = unittest.TextTestRunner(stream=f, verbosity=2)
        result = runner.run(suite)
        
        # 添加总结
        f.write("\n=== 测试总结 ===\n")
        f.write(f"运行测试数: {result.testsRun}\n")
        f.write(f"成功: {result.testsRun - len(result.failures) - len(result.errors)}\n")
        f.write(f"失败: {len(result.failures)}\n")
        f.write(f"错误: {len(result.errors)}\n")

if __name__ == '__main__':
    run_tests() 