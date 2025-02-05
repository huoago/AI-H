from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton, 
                            QListWidget, QTextEdit, QLabel, QMessageBox,
                            QInputDialog, QFileDialog)
from PyQt5.QtCore import Qt
import json
import os
import logging

class TemplateDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.templates = {}
        self.template_path = os.path.join(os.path.dirname(__file__), 
                                        '../templates/article_templates.json')
        self.initUI()
        self.loadTemplates()
        
    def initUI(self):
        self.setWindowTitle('模板管理')
        self.setGeometry(200, 200, 800, 600)
        
        layout = QHBoxLayout()
        
        # 左侧模板列表
        left_layout = QVBoxLayout()
        self.template_list = QListWidget()
        self.template_list.currentItemChanged.connect(self.onTemplateSelected)
        left_layout.addWidget(QLabel('模板列表'))
        left_layout.addWidget(self.template_list)
        
        # 模板操作按钮
        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton('新建模板')
        self.add_btn.clicked.connect(self.addTemplate)
        self.import_btn = QPushButton('导入模板')
        self.import_btn.clicked.connect(self.importTemplate)
        self.export_btn = QPushButton('导出模板')
        self.export_btn.clicked.connect(self.exportTemplate)
        self.delete_btn = QPushButton('删除模板')
        self.delete_btn.clicked.connect(self.deleteTemplate)
        
        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.import_btn)
        btn_layout.addWidget(self.export_btn)
        btn_layout.addWidget(self.delete_btn)
        left_layout.addLayout(btn_layout)
        
        layout.addLayout(left_layout)
        
        # 右侧模板编辑
        right_layout = QVBoxLayout()
        right_layout.addWidget(QLabel('提示语:'))
        self.prompt_edit = QTextEdit()
        right_layout.addWidget(self.prompt_edit)
        
        params_layout = QHBoxLayout()
        params_layout.addWidget(QLabel('最大长度:'))
        self.max_length_edit = QTextEdit()
        self.max_length_edit.setMaximumHeight(30)
        params_layout.addWidget(self.max_length_edit)
        
        params_layout.addWidget(QLabel('温度:'))
        self.temperature_edit = QTextEdit()
        self.temperature_edit.setMaximumHeight(30)
        params_layout.addWidget(self.temperature_edit)
        
        right_layout.addLayout(params_layout)
        
        # 保存按钮
        save_layout = QHBoxLayout()
        self.save_btn = QPushButton('保存修改')
        self.save_btn.clicked.connect(self.saveTemplate)
        save_layout.addWidget(self.save_btn)
        right_layout.addLayout(save_layout)
        
        layout.addLayout(right_layout)
        self.setLayout(layout)
        
    def loadTemplates(self):
        try:
            if os.path.exists(self.template_path):
                with open(self.template_path, 'r', encoding='utf-8') as f:
                    self.templates = json.load(f)
            else:
                # 创建默认模板
                self.templates = {
                    "学术论文": {
                        "prompt": "请将以下内容改写成学术论文格式...",
                        "max_length": 2000,
                        "temperature": 0.7
                    }
                }
                self.saveTemplates()
                
            self.updateTemplateList()
        except Exception as e:
            logging.error(f"加载模板失败: {str(e)}")
            QMessageBox.warning(self, "错误", f"加载模板失败: {str(e)}")
            
    def updateTemplateList(self):
        self.template_list.clear()
        self.template_list.addItems(self.templates.keys())
        
    def saveTemplates(self):
        try:
            os.makedirs(os.path.dirname(self.template_path), exist_ok=True)
            with open(self.template_path, 'w', encoding='utf-8') as f:
                json.dump(self.templates, f, ensure_ascii=False, indent=4)
        except Exception as e:
            logging.error(f"保存模板失败: {str(e)}")
            QMessageBox.warning(self, "错误", f"保存模板失败: {str(e)}")
            
    def onTemplateSelected(self, current, previous):
        if current is None:
            return
            
        template_name = current.text()
        template = self.templates.get(template_name)
        if template:
            self.prompt_edit.setText(template['prompt'])
            self.max_length_edit.setText(str(template['max_length']))
            self.temperature_edit.setText(str(template['temperature']))
            
    def addTemplate(self):
        name, ok = QInputDialog.getText(self, '新建模板', '请输入模板名称:')
        if ok and name:
            if name in self.templates:
                QMessageBox.warning(self, "错误", "模板名称已存在")
                return
                
            self.templates[name] = {
                "prompt": "请将以下内容改写成指定格式...",
                "max_length": 2000,
                "temperature": 0.7
            }
            self.updateTemplateList()
            self.saveTemplates()
            
    def importTemplate(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "导入模板",
            "",
            "JSON文件 (*.json)"
        )
        
        if file_name:
            try:
                with open(file_name, 'r', encoding='utf-8') as f:
                    new_templates = json.load(f)
                self.templates.update(new_templates)
                self.updateTemplateList()
                self.saveTemplates()
                QMessageBox.information(self, "成功", "模板导入成功")
            except Exception as e:
                QMessageBox.warning(self, "错误", f"导入失败: {str(e)}")
                
    def exportTemplate(self):
        current = self.template_list.currentItem()
        if not current:
            QMessageBox.warning(self, "错误", "请先选择要导出的模板")
            return
            
        template_name = current.text()
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "导出模板",
            f"{template_name}.json",
            "JSON文件 (*.json)"
        )
        
        if file_name:
            try:
                with open(file_name, 'w', encoding='utf-8') as f:
                    json.dump({template_name: self.templates[template_name]}, 
                            f, ensure_ascii=False, indent=4)
                QMessageBox.information(self, "成功", "模板导出成功")
            except Exception as e:
                QMessageBox.warning(self, "错误", f"导出失败: {str(e)}")
                
    def deleteTemplate(self):
        current = self.template_list.currentItem()
        if not current:
            QMessageBox.warning(self, "错误", "请先选择要删除的模板")
            return
            
        template_name = current.text()
        reply = QMessageBox.question(self, '确认删除', 
                                   f'确定要删除模板 "{template_name}" 吗？',
                                   QMessageBox.Yes | QMessageBox.No)
                                   
        if reply == QMessageBox.Yes:
            del self.templates[template_name]
            self.updateTemplateList()
            self.saveTemplates()
            
    def saveTemplate(self):
        current = self.template_list.currentItem()
        if not current:
            QMessageBox.warning(self, "错误", "请先选择要保存的模板")
            return
            
        template_name = current.text()
        try:
            max_length = int(self.max_length_edit.toPlainText())
            temperature = float(self.temperature_edit.toPlainText())
            
            if not (500 <= max_length <= 5000):
                raise ValueError("最大长度必须在500-5000之间")
            if not (0.1 <= temperature <= 1.0):
                raise ValueError("温度必须在0.1-1.0之间")
                
            self.templates[template_name] = {
                "prompt": self.prompt_edit.toPlainText(),
                "max_length": max_length,
                "temperature": temperature
            }
            
            self.saveTemplates()
            QMessageBox.information(self, "成功", "模板保存成功")
        except ValueError as e:
            QMessageBox.warning(self, "错误", str(e))
        except Exception as e:
            QMessageBox.warning(self, "错误", f"保存失败: {str(e)}") 