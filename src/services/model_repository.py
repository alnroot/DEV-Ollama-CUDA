"""Model repository implementation."""

from typing import List

from ..core.interfaces import ModelRepositoryInterface, OllamaServiceInterface
from ..config.settings import Settings


class ModelRepository(ModelRepositoryInterface):
    """Implementation of model repository operations."""
    
    def __init__(self, ollama_service: OllamaServiceInterface):
        self._settings = Settings()
        self._ollama_service = ollama_service
    
    def get_popular_models(self) -> List[str]:
        """Get list of popular models."""
        return self._settings.popular_models
    
    def is_model_available(self, model: str, service_type: str = "general") -> bool:
        """Check if model is available."""
        available_models = self._ollama_service.get_models(service_type)
        return model in available_models 