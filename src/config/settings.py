"""Configuration settings using Singleton pattern."""

class Settings:
    """Singleton configuration class."""
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self._services = {
                "general": "http://localhost:11434",
                "code": "http://localhost:11435", 
                "text": "http://localhost:11436"
            }
            self._popular_models = [
                "llama3.2:1b",      # Modelo más pequeño primero
                "llama3.2:3b",
                "qwen2.5:3b",       # Versión más pequeña
                "codellama:7b-instruct",  # Versión instruct es más eficiente
                "mistral:7b-instruct"     # Versión instruct
            ]
            self._request_timeout = 120     # Aumentar timeout para modelos grandes
            self._pull_timeout = 600        # Aumentar timeout para descargas
            self._connection_timeout = 10   # Timeout de conexión rápido
            self._read_timeout = 90         # Timeout de lectura optimizado
            Settings._initialized = True
    
    @property
    def services(self):
        return self._services
    
    @property
    def popular_models(self):
        return self._popular_models
    
    @property
    def request_timeout(self):
        return self._request_timeout
    
    @property
    def pull_timeout(self):
        return self._pull_timeout
    
    @property
    def connection_timeout(self):
        return self._connection_timeout
    
    @property
    def read_timeout(self):
        return self._read_timeout 