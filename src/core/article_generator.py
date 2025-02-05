import logging
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from ..utils.config_manager import ConfigManager
from ..utils.error_handler import ErrorHandler

class ArticleGenerator:
    def __init__(self):
        self.config = ConfigManager()
        self.model = None
        self.tokenizer = None
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self._load_model()
        
    def _load_model(self):
        """加载模型"""
        try:
            model_name = self.config.get('model.name')
            cache_dir = self.config.get('model.cache_dir')
            
            logging.info(f"正在加载模型: {model_name}")
            
            self.tokenizer = AutoTokenizer.from_pretrained(
                model_name,
                cache_dir=cache_dir,
                trust_remote_code=True
            )
            
            self.model = AutoModelForCausalLM.from_pretrained(
                model_name,
                cache_dir=cache_dir,
                trust_remote_code=True
            ).to(self.device)
            
            logging.info("模型加载完成")
            
        except Exception as e:
            ErrorHandler.show_error(f"模型加载失败: {str(e)}")
            raise
            
    def generate(self, text_data, template_name):
        """生成文章"""
        try:
            # 获取模板
            templates = self.config.get('templates', [])
            template = next((t for t in templates if t['name'] == template_name), None)
            
            if not template:
                raise ValueError(f"未找到模板: {template_name}")
            
            # 处理输入数据
            if isinstance(text_data, dict) and text_data['type'] == 'template':
                # 使用要求作为提示词
                prompt = f"{text_data['requirements']}\n\n原文内容:\n{text_data['content']}"
            else:
                # 使用普通模板
                prompt = template['prompt'].format(content=text_data)
            
            max_length = template.get('max_length', 2000)
            temperature = self.config.get('model.temperature', 0.7)
            
            # 生成文章
            inputs = self.tokenizer(prompt, return_tensors='pt').to(self.device)
            
            outputs = self.model.generate(
                **inputs,
                max_length=max_length,
                temperature=temperature,
                do_sample=True,
                pad_token_id=self.tokenizer.pad_token_id
            )
            
            result = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # 移除原始提示词
            result = result[len(prompt):].strip()
            
            return result
            
        except Exception as e:
            ErrorHandler.show_error(f"文章生成失败: {str(e)}")
            raise 