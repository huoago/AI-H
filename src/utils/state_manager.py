from PyQt5.QtCore import QObject, pyqtSignal

class StateManager(QObject):
    # 定义信号
    model_loaded = pyqtSignal(bool)
    processing_started = pyqtSignal()
    processing_finished = pyqtSignal()
    error_occurred = pyqtSignal(str)
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            super().__init__()
            self.initialized = True
            self._is_model_loaded = False
            self._is_processing = False
    
    @property
    def is_model_loaded(self):
        return self._is_model_loaded
    
    @is_model_loaded.setter
    def is_model_loaded(self, value):
        self._is_model_loaded = value
        self.model_loaded.emit(value)
    
    @property
    def is_processing(self):
        return self._is_processing
    
    @is_processing.setter
    def is_processing(self, value):
        self._is_processing = value
        if value:
            self.processing_started.emit()
        else:
            self.processing_finished.emit() 