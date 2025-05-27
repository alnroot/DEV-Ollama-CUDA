"""Chat history service implementation."""

from typing import List, Dict, Any
from datetime import datetime

from ..core.interfaces import ChatHistoryInterface


class ChatHistory(ChatHistoryInterface):
    """Implementation of chat history operations using Singleton pattern."""
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self._messages: List[Dict[str, Any]] = []
            ChatHistory._initialized = True
    
    def add_message(self, message: Dict[str, Any]) -> None:
        """Add message to history."""
        message["timestamp"] = datetime.now().isoformat()
        self._messages.append(message)
    
    def get_history(self) -> List[Dict[str, Any]]:
        """Get chat history."""
        return self._messages.copy()
    
    def clear_history(self) -> None:
        """Clear chat history."""
        self._messages.clear() 