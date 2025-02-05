import logging
import sys
import traceback
from PyQt5.QtWidgets import QMessageBox

class ErrorHandler:
    @staticmethod
    def setup_exception_handling():
        """设置全局异常处理"""
        sys.excepthook = ErrorHandler.handle_exception
        
    @staticmethod
    def handle_exception(exc_type, exc_value, exc_traceback):
        """处理未捕获的异常"""
        # 记录错误日志
        logging.error("未捕获的异常:", exc_info=(exc_type, exc_value, exc_traceback))
        
        # 显示错误对话框
        error_msg = f"发生错误:\n{str(exc_value)}\n\n是否查看详细信息？"
        detail_msg = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
        
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setText(error_msg)
        msg_box.setDetailedText(detail_msg)
        msg_box.exec_()
        
    @staticmethod
    def show_error(message, title="错误", parent=None):
        """显示错误消息"""
        QMessageBox.critical(parent, title, message)
        logging.error(message) 