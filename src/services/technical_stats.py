"""Technical statistics service implementation."""

import subprocess
import re
import psutil
import time
from typing import Dict, Any

from ..core.interfaces import TechnicalStatsInterface


class TechnicalStatsService(TechnicalStatsInterface):
    """Implementation of technical statistics operations."""
    
    def __init__(self):
        self._cache = {}
        self._cache_timeout = 30  # Cache por 30 segundos
        self._last_docker_logs_check = 0
        self._docker_logs_cache = ""
    
    def get_technical_stats(self) -> Dict[str, Any]:
        """Get comprehensive technical statistics with caching."""
        try:
            current_time = time.time()
            
            # Usar cache si está disponible y no ha expirado
            if ('stats' in self._cache and 
                current_time - self._cache.get('timestamp', 0) < self._cache_timeout):
                # Solo actualizar stats de sistema (son más baratos)
                self._cache['stats']['system'] = self._get_system_info()
                return self._cache['stats']
            
            # Obtener logs solo si han pasado más de 30 segundos
            logs = self._get_docker_logs_cached(current_time)
            
            # Parse technical information
            gpu_info = self._parse_gpu_info(logs)
            
            # If no GPU info from logs, try system detection (cache por más tiempo)
            if not gpu_info or not any(gpu_info.values()):
                if 'gpu_system' not in self._cache or current_time - self._cache.get('gpu_timestamp', 0) > 300:
                    gpu_info = self._detect_system_gpu()
                    self._cache['gpu_system'] = gpu_info
                    self._cache['gpu_timestamp'] = current_time
                else:
                    gpu_info = self._cache.get('gpu_system', {})
            
            tech_stats = {
                "gpu": gpu_info,
                "model": self._parse_model_info(logs),
                "memory": self._parse_memory_info(logs),
                "system": self._get_system_info(),
                "performance": self._parse_performance_info(logs)
            }
            
            # Guardar en cache
            self._cache['stats'] = tech_stats
            self._cache['timestamp'] = current_time
            
            return tech_stats
            
        except Exception as e:
            print(f"Error getting technical stats: {e}")
            return self._cache.get('stats', {})
    
    def _get_docker_logs_cached(self, current_time: float) -> str:
        """Get Docker logs with caching to reduce subprocess calls."""
        if current_time - self._last_docker_logs_check > 30:  # Solo cada 30 segundos
            try:
                result = subprocess.run([
                    "docker", "logs", "--tail", "50", "ollama-service"  # Reducir tail a 50
                ], capture_output=True, text=True, encoding='utf-8', errors='ignore', timeout=5)
                
                self._docker_logs_cache = (result.stdout or "") + (result.stderr or "")
                self._last_docker_logs_check = current_time
            except Exception as e:
                print(f"Error getting docker logs: {e}")
        
        return self._docker_logs_cache
    
    def _parse_gpu_info(self, logs: str) -> Dict[str, str]:
        """Parse GPU information from logs."""
        gpu_info = {}
        
        # Search for GPU information patterns
        gpu_patterns = {
            "name": r"Device \d+: (.+?), compute capability",
            "compute_capability": r"compute capability (\d+\.\d+)",
            "total_memory": r'total="([^"]+)"',
            "available_memory": r'available="([^"]+)"',
            "cuda_version": r"CUDA\.0\.ARCHS=([0-9,]+)",
            "driver_version": r"driver=(\d+\.\d+)"
        }
        
        for key, pattern in gpu_patterns.items():
            match = re.search(pattern, logs)
            if match:
                gpu_info[key] = match.group(1)
        
        return gpu_info
    
    def _parse_model_info(self, logs: str) -> Dict[str, str]:
        """Parse active model information."""
        model_info = {}
        
        model_patterns = {
            "architecture": r"general\.architecture.*?=\s*(\w+)",
            "name": r"general\.name.*?=\s*(.+)",
            "context_length": r"llama\.context_length.*?=\s*(\d+)",
            "embedding_length": r"llama\.embedding_length.*?=\s*(\d+)",
            "block_count": r"llama\.block_count.*?=\s*(\d+)",
            "attention_heads": r"llama\.attention\.head_count.*?=\s*(\d+)",
            "file_size": r"file size\s*=\s*([\d.]+ \w+)",
            "model_params": r"model params\s*=\s*([\d.]+ \w+)",
            "quantization": r"file type\s*=\s*(\w+)",
            "vocab_size": r"n_vocab\s*=\s*(\d+)"
        }
        
        for key, pattern in model_patterns.items():
            match = re.search(pattern, logs)
            if match:
                model_info[key] = match.group(1).strip()
        
        return model_info
    
    def _parse_memory_info(self, logs: str) -> Dict[str, str]:
        """Parse memory information."""
        memory_info = {}
        
        memory_patterns = {
            "gpu_memory_required": r'memory\.required\.full="([^"]+)"',
            "gpu_memory_allocated": r'memory\.required\.allocations="\[([^\]]+)\]"',
            "weights_total": r'memory\.weights\.total="([^"]+)"',
            "kv_memory": r'memory\.required\.kv="([^"]+)"',
            "graph_memory": r'memory\.graph\.full="([^"]+)"',
            "cuda_buffer": r'CUDA0 model buffer size\s*=\s*([\d.]+ \w+)',
            "kv_buffer": r'CUDA0 KV buffer size\s*=\s*([\d.]+ \w+)',
            "compute_buffer": r'CUDA0 compute buffer size\s*=\s*([\d.]+ \w+)',
            "layers_offloaded": r'offloaded (\d+)/(\d+) layers to GPU'
        }
        
        for key, pattern in memory_patterns.items():
            match = re.search(pattern, logs)
            if match:
                if key == "layers_offloaded":
                    memory_info[key] = f"{match.group(1)}/{match.group(2)}"
                else:
                    memory_info[key] = match.group(1)
        
        return memory_info
    
    def _parse_performance_info(self, logs: str) -> Dict[str, str]:
        """Parse performance metrics."""
        performance_info = {}
        
        performance_patterns = {
            "load_time": r'load time\s*=\s*([\d.]+ ms)',
            "sample_time": r'sample time\s*=\s*([\d.]+ ms)',
            "prompt_eval_time": r'prompt eval time\s*=\s*([\d.]+ ms)',
            "eval_time": r'eval time\s*=\s*([\d.]+ ms)',
            "total_time": r'total time\s*=\s*([\d.]+ ms)',
            "tokens_per_second": r'(\d+\.?\d*) tokens per second',
            "prompt_tokens": r'prompt eval count:\s*(\d+)',
            "generated_tokens": r'eval count:\s*(\d+)',
            "inference_speed": r'inference:\s*([\d.]+ ms/token)',
            "batch_size": r'batch size:\s*(\d+)'
        }
        
        for key, pattern in performance_patterns.items():
            match = re.search(pattern, logs)
            if match:
                performance_info[key] = match.group(1)
        
        return performance_info
    
    def _get_system_info(self) -> Dict[str, Any]:
        """Get system information using psutil."""
        try:
            # CPU information
            cpu_info = {
                "physical_cores": psutil.cpu_count(logical=False),
                "logical_cores": psutil.cpu_count(logical=True),
                "cpu_usage": f"{psutil.cpu_percent(interval=1):.1f}%",
                "cpu_freq": f"{psutil.cpu_freq().current:.0f} MHz" if psutil.cpu_freq() else "N/A"
            }
            
            # Memory information
            memory = psutil.virtual_memory()
            memory_info = {
                "total": f"{memory.total / (1024**3):.1f} GB",
                "available": f"{memory.available / (1024**3):.1f} GB",
                "used": f"{memory.used / (1024**3):.1f} GB",
                "percentage": f"{memory.percent:.1f}%"
            }
            
            # Disk information
            disk = psutil.disk_usage('/')
            disk_info = {
                "total": f"{disk.total / (1024**3):.1f} GB",
                "free": f"{disk.free / (1024**3):.1f} GB",
                "used": f"{disk.used / (1024**3):.1f} GB",
                "percentage": f"{(disk.used / disk.total) * 100:.1f}%"
            }
            
            return {
                "cpu": cpu_info,
                "memory": memory_info,
                "disk": disk_info
            }
            
        except Exception as e:
            print(f"Error getting system info: {e}")
            return {}
    
    def _detect_system_gpu(self) -> Dict[str, str]:
        """Detect GPU information from system commands."""
        gpu_info = {}
        
        try:
            # Try nvidia-smi first
            result = subprocess.run(
                ["nvidia-smi", "--query-gpu=name,memory.total,compute_cap", "--format=csv,noheader,nounits"], 
                capture_output=True, text=True, timeout=5
            )
            
            if result.returncode == 0 and result.stdout.strip():
                lines = result.stdout.strip().split('\n')
                if lines:
                    parts = lines[0].split(', ')
                    if len(parts) >= 3:
                        gpu_info["name"] = parts[0].strip()
                        gpu_info["total_memory"] = f"{parts[1].strip()} MB"
                        gpu_info["compute_capability"] = parts[2].strip()
                        gpu_info["driver_version"] = self._get_nvidia_driver_version()
                        gpu_info["cuda_version"] = self._get_cuda_version()
                        return gpu_info
        except:
            pass
        
        try:
            # Try Windows WMIC command
            result = subprocess.run(
                ["wmic", "path", "win32_VideoController", "get", "name", "/format:list"],
                capture_output=True, text=True, timeout=5
            )
            
            if result.returncode == 0:
                for line in result.stdout.split('\n'):
                    if line.startswith('Name=') and 'NVIDIA' in line:
                        gpu_name = line.split('=', 1)[1].strip()
                        gpu_info["name"] = gpu_name
                        gpu_info["total_memory"] = "N/A"
                        gpu_info["compute_capability"] = "N/A"
                        gpu_info["driver_version"] = "N/A"
                        gpu_info["cuda_version"] = "N/A"
                        break
        except:
            pass
        
        # Fallback values
        if not gpu_info:
            gpu_info = {
                "name": "No GPU detected",
                "total_memory": "N/A",
                "compute_capability": "N/A",
                "driver_version": "N/A",
                "cuda_version": "N/A"
            }
        
        return gpu_info
    
    def _get_nvidia_driver_version(self) -> str:
        """Get NVIDIA driver version."""
        try:
            result = subprocess.run(
                ["nvidia-smi", "--query-gpu=driver_version", "--format=csv,noheader"], 
                capture_output=True, text=True, timeout=3
            )
            if result.returncode == 0:
                return result.stdout.strip()
        except:
            pass
        return "N/A"
    
    def _get_cuda_version(self) -> str:
        """Get CUDA version."""
        try:
            result = subprocess.run(
                ["nvcc", "--version"], 
                capture_output=True, text=True, timeout=3
            )
            if result.returncode == 0:
                for line in result.stdout.split('\n'):
                    if 'release' in line.lower():
                        parts = line.split('release')
                        if len(parts) > 1:
                            version = parts[1].split(',')[0].strip()
                            return f"CUDA {version}"
        except:
            pass
        
        try:
            # Alternative: check nvidia-smi CUDA version
            result = subprocess.run(
                ["nvidia-smi"], 
                capture_output=True, text=True, timeout=3
            )
            if result.returncode == 0:
                for line in result.stdout.split('\n'):
                    if 'CUDA Version:' in line:
                        cuda_version = line.split('CUDA Version:')[1].strip().split()[0]
                        return f"CUDA {cuda_version}"
        except:
            pass
            
        return "N/A" 