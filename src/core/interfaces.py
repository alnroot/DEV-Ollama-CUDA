"""Interfaces for dependency inversion pattern."""

from abc import ABC, abstractmethod
from typing import List, Dict, Any


class OllamaServiceInterface(ABC):
    """Interface for Ollama service operations."""
    
    @abstractmethod
    def get_models(self, service_type: str) -> List[str]:
        """Get available models for a service."""
        pass
    
    @abstractmethod
    def chat(self, message: str, model: str, service_type: str) -> Dict[str, Any]:
        """Send chat message to model."""
        pass
    
    @abstractmethod
    def pull_model(self, model_name: str, service_type: str) -> Dict[str, Any]:
        """Download a model."""
        pass
    
    @abstractmethod
    def get_service_status(self) -> Dict[str, Any]:
        """Get status of all services."""
        pass


class ModelRepositoryInterface(ABC):
    """Interface for model repository operations."""
    
    @abstractmethod
    def get_popular_models(self) -> List[str]:
        """Get list of popular models."""
        pass
    
    @abstractmethod
    def is_model_available(self, model: str, service_type: str) -> bool:
        """Check if model is available."""
        pass


class ChatHistoryInterface(ABC):
    """Interface for chat history operations."""
    
    @abstractmethod
    def add_message(self, message: Dict[str, Any]) -> None:
        """Add message to history."""
        pass
    
    @abstractmethod
    def get_history(self) -> List[Dict[str, Any]]:
        """Get chat history."""
        pass
    
    @abstractmethod
    def clear_history(self) -> None:
        """Clear chat history."""
        pass


class TechnicalStatsInterface(ABC):
    """Interface for technical statistics operations."""
    
    @abstractmethod
    def get_technical_stats(self) -> Dict[str, Any]:
        """Get comprehensive technical statistics."""
        pass


class DockerCommandsInterface(ABC):
    """Interface for Docker commands operations."""
    
    @abstractmethod
    def start_services(self) -> Dict[str, Any]:
        """Start all Docker services."""
        pass
    
    @abstractmethod
    def stop_services(self) -> Dict[str, Any]:
        """Stop all Docker services."""
        pass
    
    @abstractmethod
    def restart_services(self) -> Dict[str, Any]:
        """Restart all Docker services."""
        pass
    
    @abstractmethod
    def get_container_status(self) -> Dict[str, Any]:
        """Get status of Docker containers."""
        pass
    
    @abstractmethod
    def test_connection(self) -> Dict[str, Any]:
        """Test connectivity with all services."""
        pass 