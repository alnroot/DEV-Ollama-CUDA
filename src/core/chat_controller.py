"""Main chat controller with dependency injection."""

from typing import List, Dict, Any
import threading

from .interfaces import (
    OllamaServiceInterface, 
    ModelRepositoryInterface, 
    ChatHistoryInterface,
    TechnicalStatsInterface,
    DockerCommandsInterface
)


class ChatController:
    """Main controller coordinating all chat operations."""
    
    def __init__(
        self, 
        ollama_service: OllamaServiceInterface,
        model_repository: ModelRepositoryInterface,
        chat_history: ChatHistoryInterface,
        technical_stats: TechnicalStatsInterface,
        docker_commands: DockerCommandsInterface
    ):
        self._ollama_service = ollama_service
        self._model_repository = model_repository
        self._chat_history = chat_history
        self._technical_stats = technical_stats
        self._docker_commands = docker_commands
    
    def get_available_models(self, service_type: str = "general") -> List[str]:
        """Get available models for a service."""
        return self._ollama_service.get_models(service_type)
    
    def get_popular_models(self) -> List[str]:
        """Get popular models."""
        return self._model_repository.get_popular_models()
    
    def send_message(self, message: str, model: str, service_type: str = "general") -> Dict[str, Any]:
        """Send a chat message."""
        # Add user message to history TODO: integrar memory service
        user_message = {
            "type": "user",
            "content": message,
            "model": model,
            "service": service_type
        }
        self._chat_history.add_message(user_message)
        
        # Get response from Ollama
        response = self._ollama_service.chat(message, model, service_type)
        
        # Add assistant response to history
        if response.get("success"):
            assistant_message = {
                "type": "assistant",
                "content": response["response"],
                "model": model,
                "service": service_type
            }
            self._chat_history.add_message(assistant_message)
        
        return response
    
    def download_model(self, model_name: str, service_type: str = "general") -> Dict[str, Any]:
        """Download a model in background."""
        def _download():
            return self._ollama_service.pull_model(model_name, service_type)
        
        # Start download in background thread
        thread = threading.Thread(target=_download)
        thread.daemon = True
        thread.start()
        
        return {"success": True, "message": f"Descarga de {model_name} iniciada en segundo plano"}
    
    def get_service_status(self) -> Dict[str, Any]:
        """Get status of all services."""
        return self._ollama_service.get_service_status()
    
    def get_chat_history(self) -> List[Dict[str, Any]]:
        """Get chat history."""
        return self._chat_history.get_history()
    
    def clear_chat_history(self) -> None:
        """Clear chat history."""
        self._chat_history.clear_history()
    
    def is_model_available(self, model: str, service_type: str = "general") -> bool:
        """Check if model is available."""
        return self._model_repository.is_model_available(model, service_type)
    
    def get_technical_stats(self) -> Dict[str, Any]:
        """Get comprehensive technical statistics."""
        return self._technical_stats.get_technical_stats()
    
    def start_docker_services(self) -> Dict[str, Any]:
        """Start Docker services."""
        return self._docker_commands.start_services()
    
    def stop_docker_services(self) -> Dict[str, Any]:
        """Stop Docker services."""
        return self._docker_commands.stop_services()
    
    def restart_docker_services(self) -> Dict[str, Any]:
        """Restart Docker services."""
        return self._docker_commands.restart_services()
    
    def get_docker_status(self) -> Dict[str, Any]:
        """Get Docker container status."""
        return self._docker_commands.get_container_status()
    
    def test_service_connections(self) -> Dict[str, Any]:
        """Test connectivity with all services."""
        return self._docker_commands.test_connection()