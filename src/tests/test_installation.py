import sys
import os
from pathlib import Path
import unittest
import subprocess
import shutil

class TestInstallation(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path('test_installation')
        self.test_dir.mkdir(exist_ok=True)
        
    def tearDown(self):
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
            
    def test_dependencies(self):
        """测试依赖项安装"""
        try:
            # 测试PyQt5
            import PyQt5
            self.assertTrue(True, "PyQt5 已安装")
            
            # 测试 Tesseract
            import pytesseract
            pytesseract.get_tesseract_version()
            self.assertTrue(True, "Tesseract 已安装")
            
            # 测试 Torch
            import torch
            self.assertTrue(True, "Torch 已安装")
            
            # 测试 Transformers
            import transformers
            self.assertTrue(True, "Transformers 已安装")
            
        except ImportError as e:
            self.fail(f"依赖项缺失: {str(e)}")
            
    def test_model_download(self):
        """测试模型下载"""
        try:
            from transformers import AutoTokenizer
            tokenizer = AutoTokenizer.from_pretrained(
                "uer/gpt2-chinese-cluecorpussmall",
                trust_remote_code=True
            )
            self.assertTrue(True, "模型下载成功")
        except Exception as e:
            self.fail(f"模型下载失败: {str(e)}")
            
    def test_program_launch(self):
        """测试程序启动"""
        exe_path = Path('dist/AI文章生成助手.exe')
        if not exe_path.exists():
            self.skipTest("可执行文件不存在，请先构建程序")
            
        try:
            # 启动程序（使用subprocess以便可以控制进程）
            process = subprocess.Popen([str(exe_path)])
            # 等待几秒检查程序是否崩溃
            import time
            time.sleep(3)
            
            # 检查进程是否还在运行
            if process.poll() is None:
                self.assertTrue(True, "程序正常运行")
            else:
                self.fail("程序启动后立即退出")
                
        finally:
            # 确保关闭程序
            if process.poll() is None:
                process.terminate()
                process.wait()

if __name__ == '__main__':
    unittest.main() 