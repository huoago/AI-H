from src.utils.init_env import init_project_env
from src.core.file_processor import FileProcessor
from src.core.article_generator import ArticleGenerator
import logging

def test_full_process():
    try:
        # 初始化环境
        init_project_env()
        
        # 处理输入文件
        processor = FileProcessor()
        content = processor.process_file("test_input.txt")
        print("文件处理结果:", content)
        
        # 生成文章
        generator = ArticleGenerator()
        result = generator.generate(content, "新闻稿")
        print("生成结果:", result)
        
        return True
    except Exception as e:
        logging.error(f"测试失败: {str(e)}")
        return False

if __name__ == '__main__':
    test_full_process() 