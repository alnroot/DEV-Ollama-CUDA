"""Docker commands service implementation."""

import subprocess
import requests
from typing import Dict, Any

from ..core.interfaces import DockerCommandsInterface
from ..config.settings import Settings


class DockerCommandsService(DockerCommandsInterface):
    """Implementation of Docker commands operations."""
    
    def __init__(self):
        self._settings = Settings()
    
    def start_services(self) -> Dict[str, Any]:
        """Start all Docker services."""
        try:
            result = subprocess.run(["docker-compose", "up", "-d"], 
                                  capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                return {"success": True, "message": "Servicios iniciados correctamente"}
            else:
                return {"success": False, "error": result.stderr}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def stop_services(self) -> Dict[str, Any]:
        """Stop all Docker services."""
        try:
            result = subprocess.run(["docker-compose", "down"], 
                                  capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                return {"success": True, "message": "Servicios detenidos correctamente"}
            else:
                return {"success": False, "error": result.stderr}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def restart_services(self) -> Dict[str, Any]:
        """Restart all Docker services."""
        try:
            result = subprocess.run(["docker-compose", "restart"], 
                                  capture_output=True, text=True, timeout=60)
            if result.returncode == 0:
                return {"success": True, "message": "Servicios reiniciados correctamente"}
            else:
                return {"success": False, "error": result.stderr}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_container_status(self) -> Dict[str, Any]:
        """Get status of Docker containers."""
        try:
            result = subprocess.run(["docker-compose", "ps", "--format", "json"], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                return {"success": True, "status": result.stdout}
            else:
                return {"success": False, "error": result.stderr}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def test_connection(self) -> Dict[str, Any]:
        """Test connectivity with all services."""
        results = {}
        services = {
            "General": "http://localhost:11434",
            "Code": "http://localhost:11435", 
            "Text": "http://localhost:11436"
        }
        
        for name, url in services.items():
            try:
                response = requests.get(f"{url}/api/tags", timeout=5)
                if response.status_code == 200:
                    results[name] = {"status": "connected", "models": len(response.json().get("models", []))}
                else:
                    results[name] = {"status": "error", "code": response.status_code}
            except Exception as e:
                results[name] = {"status": "unavailable", "error": str(e)}
        
        return {"success": True, "connections": results} 