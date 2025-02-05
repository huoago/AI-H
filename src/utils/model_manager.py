import os
import logging
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from .state_manager import StateManager

class ModelManager:
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.state_manager = StateManager()
        
    def load_model(self, model_name='THUDM/chatglm2-6b'):
        try:
            logging.info(f"正在加载模型 {model_name}")
            self.state_manager.is_processing = True
            
            self.tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
            self.model = AutoModelForCausalLM.from_pretrained(
                model_name,
                trust_remote_code=True,
                device_map='auto' if self.device == 'cuda' else None
            )
            
            if self.device == 'cpu':
                self.model = self.model.float()
                
            self.state_manager.is_model_loaded = True
            logging.info("模型加载完成")
            return True
            
        except Exception as e:
            self.state_manager.error_occurred.emit(str(e))
            logging.error(f"模型加载失败: {str(e)}")
            return False
        finally:
            self.state_manager.is_processing = False
            
    def generate(self, prompt, max_length=2000, temperature=0.7):
        if not self.model or not self.tokenizer:
            raise RuntimeError("模型未加载")
            
        try:
            inputs = self.tokenizer(prompt, return_tensors='pt').to(self.device)
            outputs = self.model.generate(
                **inputs,
                max_length=max_length,
                temperature=temperature,
                do_sample=True,
                pad_token_id=self.tokenizer.pad_token_id
            )
            return self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        except Exception as e:
            logging.error(f"生成失败: {str(e)}")
            raise 