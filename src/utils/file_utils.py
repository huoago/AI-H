import os
import shutil
from datetime import datetime
import logging

class FileUtils:
    @staticmethod
    def create_output_dir():
        """创建输出目录"""
        try:
            output_dir = os.path.join(os.path.dirname(__file__), '../output')
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            return output_dir
        except Exception as e:
            logging.error(f"创建输出目录失败: {str(e)}")
            raise
    
    @staticmethod
    def get_output_filename(original_filename, prefix='generated_'):
        """生成输出文件名"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = os.path.basename(original_filename)
        name, ext = os.path.splitext(filename)
        return f"{prefix}{name}_{timestamp}{ext}"
    
    @staticmethod
    def save_file(content, filepath, mode='w', encoding='utf-8'):
        """保存文件内容"""
        try:
            with open(filepath, mode, encoding=encoding) as f:
                f.write(content)
            return True
        except Exception as e:
            logging.error(f"保存文件失败: {str(e)}")
            return False
    
    @staticmethod
    def backup_file(filepath):
        """备份文件"""
        try:
            if os.path.exists(filepath):
                backup_path = filepath + '.bak'
                shutil.copy2(filepath, backup_path)
                return True
        except Exception as e:
            logging.error(f"备份文件失败: {str(e)}")
            return False 