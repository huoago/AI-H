import json
import os
import logging

class ConfigManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'config'):
            self.config_path = os.path.join(os.path.dirname(__file__), 
                                          '../config/config.json')
            self.load_config()
    
    def load_config(self):
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
            else:
                logging.warning("配置文件不存在，使用默认配置")
                self.config = {
                    "model": {"name": "THUDM/chatglm2-6b"},
                    "ocr": {"languages": ["chi_sim", "eng"]},
                    "ui": {
                        "window_title": "AI文章生成助手",
                        "window_size": {"width": 1000, "height": 800}
                    }
                }
        except Exception as e:
            logging.error(f"加载配置失败: {str(e)}")
            raise
    
    def get(self, key, default=None):
        keys = key.split('.')
        value = self.config
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default 