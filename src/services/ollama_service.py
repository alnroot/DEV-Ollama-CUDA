"""Ollama service implementation."""

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from typing import List, Dict, Any
import time

from ..core.interfaces import OllamaServiceInterface
from ..config.settings import Settings


class OllamaService(OllamaServiceInterface):
    """Implementation of Ollama service operations."""
    
    def __init__(self):
        self._settings = Settings()
        self._session = self._create_optimized_session()
        self._model_cache = {}
        self._cache_timeout = 60  # Cache de modelos por 60 segundos
    
    def _create_optimized_session(self) -> requests.Session:
        """Create an optimized requests session with connection pooling and retries."""
        session = requests.Session()
        
        # Configurar estrategia de retry
        retry_strategy = Retry(
            total=3,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS", "POST"],
            backoff_factor=1
        )
        
        # Configurar adapter con connection pooling
        adapter = HTTPAdapter(
            max_retries=retry_strategy,
            pool_connections=10,
            pool_maxsize=20,
            pool_block=False
        )
        
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        # Headers optimizados
        session.headers.update({
            'Connection': 'keep-alive',
            'Content-Type': 'application/json'
        })
        
        return session
    
    def get_models(self, service_type: str = "general") -> List[str]:
        """Get available models for a service with caching."""
        try:
            current_time = time.time()
            cache_key = f"models_{service_type}"
            
            # Verificar cache
            if (cache_key in self._model_cache and 
                current_time - self._model_cache[cache_key].get('timestamp', 0) < self._cache_timeout):
                return self._model_cache[cache_key]['models']
            
            service_url = self._settings.services.get(service_type, self._settings.services["general"])
            response = self._session.get(f"{service_url}/api/tags", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                models = [model["name"] for model in data.get("models", [])]
                
                # Guardar en cache
                self._model_cache[cache_key] = {
                    'models': models,
                    'timestamp': current_time
                }
                
                return models
            return []
        except Exception as e:
            print(f"Error getting models: {e}")
            # Retornar cache si existe, aunque esté expirado
            cache_key = f"models_{service_type}"
            return self._model_cache.get(cache_key, {}).get('models', [])
    
    def chat(self, message: str, model: str, service_type: str = "general") -> Dict[str, Any]:
        """Send chat message to model with optimized configuration."""
        try:
            service_url = self._settings.services.get(service_type, self._settings.services["general"])
            
            payload = {
                "model": model,
                "prompt": message,
                "stream": False,
                "options": {
                    "num_predict": 512,  # Limitar tokens de respuesta
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "num_ctx": 2048,  # Contexto más pequeño para respuestas más rápidas
                    "num_batch": 128,
                    "num_gqa": 1,
                    "num_gpu": -1,  # Usar toda la GPU disponible
                    "main_gpu": 0,
                    "low_vram": False,
                    "f16_kv": True,
                    "use_mlock": True,
                    "use_mmap": True
                }
            }
            
            response = self._session.post(
                f"{service_url}/api/generate", 
                json=payload, 
                timeout=self._settings.request_timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "success": True,
                    "response": result.get("response", ""),
                    "model": model,
                    "service": service_type,
                    "metrics": {
                        "eval_duration": result.get("eval_duration", 0),
                        "load_duration": result.get("load_duration", 0),
                        "prompt_eval_duration": result.get("prompt_eval_duration", 0),
                        "total_duration": result.get("total_duration", 0)
                    }
                }
            else:
                return {
                    "success": False,
                    "error": f"Error {response.status_code}: {response.text}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def pull_model(self, model_name: str, service_type: str = "general") -> Dict[str, Any]:
        """Download a model."""
        try:
            service_url = self._settings.services.get(service_type, self._settings.services["general"])
            
            payload = {"name": model_name}
            response = requests.post(
                f"{service_url}/api/pull", 
                json=payload, 
                timeout=self._settings.pull_timeout
            )
            
            if response.status_code == 200:
                return {"success": True, "message": f"Modelo {model_name} descargado correctamente"}
            else:
                return {"success": False, "error": f"Error descargando modelo: {response.status_code}"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_service_status(self) -> Dict[str, Any]:
        """Get status of all services."""
        status = {}
        for service_name, url in self._settings.services.items():
            try:
                response = requests.get(f"{url}/api/tags", timeout=5)
                status[service_name] = {
                    "status": "online" if response.status_code == 200 else "error",
                    "models": len(response.json().get("models", [])) if response.status_code == 200 else 0
                }
            except:
                status[service_name] = {"status": "offline", "models": 0}
        
        return status 