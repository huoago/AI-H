from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QPushButton,
                           QTextEdit, QFileDialog, QComboBox, QLabel, QMessageBox,
                           QProgressBar, QHBoxLayout, QSpinBox, QCheckBox, QDialog)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from core.file_processor import FileProcessor
from core.article_generator import ArticleGenerator
from .template_dialog import TemplateDialog
import logging
import json
import os
from ..utils.config_manager import ConfigManager
from ..utils.error_handler import ErrorHandler

class GenerateThread(QThread):
    finished = pyqtSignal(str)
    error = pyqtSignal(str)
    
    def __init__(self, generator, text, template):
        super().__init__()
        self.generator = generator
        self.text = text
        self.template = template
        
    def run(self):
        try:
            result = self.generator.generate(self.text, self.template)
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.config = ConfigManager()
        self.generator = ArticleGenerator()
        self.processor = FileProcessor()
        self.init_ui()
        
    def init_ui(self):
        """初始化界面"""
        # 设置窗口属性
        self.setWindowTitle(self.config.get('ui.window_title', 'AI文章生成助手'))
        size = self.config.get('ui.window_size', {'width': 1000, 'height': 800})
        self.resize(size['width'], size['height'])
        
        # 创建中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建布局
        layout = QVBoxLayout(central_widget)
        
        # 添加控件
        self.create_widgets(layout)
        
    def create_widgets(self, layout):
        """创建控件"""
        # 文件选择按钮
        self.file_btn = QPushButton('选择文件')
        self.file_btn.clicked.connect(self.select_file)
        layout.addWidget(self.file_btn)
        
        # 输入文本框
        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText('在此输入或粘贴文本...')
        layout.addWidget(self.input_text)
        
        # 模板选择
        self.template_combo = QComboBox()
        templates = self.config.get('templates', [])
        for template in templates:
            self.template_combo.addItem(template['name'])
        layout.addWidget(self.template_combo)
        
        # 生成按钮
        self.generate_btn = QPushButton('生成')
        self.generate_btn.clicked.connect(self.generate_article)
        layout.addWidget(self.generate_btn)
        
        # 进度条
        self.progress = QProgressBar()
        self.progress.setVisible(False)
        layout.addWidget(self.progress)
        
        # 输出文本框
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setPlaceholderText('生成的文章将显示在这里...')
        layout.addWidget(self.output_text)
        
    def process_input_text(self, text):
        """处理输入文本"""
        # 检查是否包含两个回车的模板格式
        paragraphs = text.split('\n\n')
        if len(paragraphs) >= 2:
            # 显示识别到的要求
            requirements = paragraphs[0].strip()
            QMessageBox.information(self, "模板识别", 
                                  f"已识别到以下要求:\n{requirements}")
            
            # 更新UI显示
            self.input_text.setPlainText(text)
            self.template_combo.setCurrentText("自定义")
            
            return {
                'type': 'template',
                'requirements': requirements,
                'content': '\n\n'.join(paragraphs[1:]).strip()
            }
        
        return {
            'type': 'plain',
            'content': text
        }

    def select_file(self):
        """选择文件"""
        try:
            formats = self.config.get('file.supported_formats', 
                                    ['txt', 'pdf', 'docx', 'png', 'jpg'])
            filter_str = f"支持的文件 ({' '.join(f'*.{fmt}' for fmt in formats)})"
            
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "选择文件",
                "",
                filter_str
            )
            
            if file_path:
                self.progress.setVisible(True)
                self.progress.setRange(0, 0)  # 显示忙碌状态
                
                try:
                    content = self.processor.process_file(file_path)
                    if isinstance(content, dict):
                        self.process_input_text(content['content'])
                    else:
                        self.input_text.setText(content)
                finally:
                    self.progress.setVisible(False)
                    
        except Exception as e:
            ErrorHandler.show_error(str(e), parent=self)
            
    def generate_article(self):
        """生成文章"""
        text = self.input_text.toPlainText().strip()
        if not text:
            QMessageBox.warning(self, "警告", "请先输入或选择文本")
            return
            
        # 处理输入文本
        text_data = self.process_input_text(text)
        template = self.template_combo.currentText()
        
        # 禁用按钮，显示进度条
        self.generate_btn.setEnabled(False)
        self.progress.setVisible(True)
        self.progress.setRange(0, 0)
        
        # 创建生成线程
        self.thread = GenerateThread(self.generator, text_data, template)
        self.thread.finished.connect(self.on_generation_finished)
        self.thread.error.connect(self.on_generation_error)
        self.thread.start()
        
    def on_generation_finished(self, result):
        """生成完成"""
        self.output_text.setText(result)
        self.generate_btn.setEnabled(True)
        self.progress.setVisible(False)
        
    def on_generation_error(self, error):
        """生成错误"""
        ErrorHandler.show_error(error, parent=self)
        self.generate_btn.setEnabled(True)
        self.progress.setVisible(False)
        
    def manageTemplates(self):
        dialog = TemplateDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.load_templates()  # 重新加载模板列表 