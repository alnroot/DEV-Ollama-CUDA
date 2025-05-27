# 🤖 Ollama Chat - Interfaz Web Optimizada

Interfaz web moderna y optimizada para interactuar con múltiples servicios de Ollama con monitoreo en tiempo real del sistema.

## ✨ Características Principales

- 🎯 **Chat en tiempo real** con modelos Ollama locales
- 📥 **Descarga de modelos** populares con un click
- 🔄 **Selección de servicios** (General, Code, Text)
- 📊 **Estadísticas técnicas** avanzadas (GPU, CPU, Memoria)
- 🐳 **Gestión de Docker** integrada
- 🔌 **Test de conectividad** de servicios
- 📱 **Diseño responsivo** y moderno
- 🏗️ **Arquitectura modular** design patterns

## 🏛️ Arquitectura

La aplicación sigue una arquitectura modular con separación clara de responsabilidades:

```
📁 OllamaTest/
├── 📄 main.py              # 🚀 Punto de entrada principal
├── 📄 requirements.txt     # 📦 Dependencias del proyecto  
├── 📄 docker-compose.yml   # 🐳 Configuración de contenedores
├── 📄 README.md           # 📖 Documentación
├── 📁 .venv/              # 🐍 Entorno virtual Python
└── 📁 src/                # 📂 Código fuente modular
    ├── 📁 config/         # ⚙️ Configuración (Singleton)
    │   ├── __init__.py
    │   └── settings.py    # Settings centralizados
    ├── 📁 core/           # 🧠 Lógica de negocio principal
    │   ├── __init__.py
    │   ├── interfaces.py  # Interfaces (Inversión de dependencias)
    │   └── chat_controller.py # Controlador principal
    ├── 📁 services/       # 🔧 Servicios especializados
    │   ├── __init__.py
    │   ├── ollama_service.py     # Comunicación con Ollama
    │   ├── model_repository.py  # Gestión de modelos
    │   ├── chat_history.py      # Historial (Singleton)
    │   ├── technical_stats.py   # Estadísticas técnicas
    │   └── docker_commands.py   # Comandos Docker
    └── 📁 web/            # 🌐 Interfaz web
        ├── __init__.py
        ├── app.py         # Aplicación Flask con factory pattern
        └── templates/
            └── index.html # Interfaz única con panel futurista
```

## 🔧 Patrones de Diseño Implementados

### 1. **Singleton Pattern**
- `Settings`: Configuración única para toda la aplicación
- `ChatHistory`: Historial compartido entre sesiones

### 2. **Dependency Inversion Pattern**
- Interfaces abstractas definidas en `core/interfaces.py`
- Implementaciones concretas en `services/`
- Inyección de dependencias en el controlador principal

### 3. **Factory Pattern**
- `create_app()` para inicializar la aplicación Flask con todas sus dependencias

## 🚀 Instalación y Uso

### Prerrequisitos
- Python 3.8+
- Docker y Docker Compose
- Servicios Ollama corriendo en puertos 11434, 11435, 11436

### Instalación

1. **Clonar el repositorio:**
```bash
git clone <repository-url>
cd OllamaTest
```

2. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

3. **Iniciar la aplicación:**
```bash
python main.py
```

4. **Abrir en el navegador:**
```
http://localhost:5000
```

## 📋 Funcionalidades

### Chat
- Seleccionar servicio (General/Code/Text)
- Elegir modelo disponible
- Conversación en tiempo real
- Historial de chat persistente

### Gestión de Modelos
- Ver modelos disponibles por servicio
- Descargar modelos populares predefinidos
- Modelos sugeridos: `llama3.2:3b`, `llama3.2:1b`, `qwen2.5:7b`, `codellama:7b`, `mistral:7b`

### Estadísticas Técnicas
- Información de GPU (CUDA, memoria, compute capability)
- Métricas del modelo activo (arquitectura, parámetros, quantización)
- Uso de CPU, RAM y disco
- Rendimiento en tiempo real (tokens/segundo, tiempos de inferencia)

### Gestión de Servicios
- Iniciar/detener/reiniciar contenedores Docker
- Estado en tiempo real de servicios
- Test de conectividad automático

## 🔄 API Endpoints

### Chat y Modelos
- `GET /` - Interfaz web principal
- `GET /api/models/<service_type>` - Obtener modelos disponibles
- `GET /api/popular-models` - Obtener modelos populares
- `POST /api/chat` - Enviar mensaje al modelo
- `POST /api/download` - Descargar modelo
- `GET /api/status` - Estado de servicios

### Historial
- `GET /api/history` - Obtener historial
- `POST /api/clear-history` - Limpiar historial

### Funcionalidades Técnicas
- `GET /api/technical-stats` - Estadísticas técnicas avanzadas
- `POST /api/docker/start` - Iniciar servicios Docker
- `POST /api/docker/stop` - Detener servicios Docker
- `POST /api/docker/restart` - Reiniciar servicios Docker
- `GET /api/docker/status` - Estado de contenedores
- `GET /api/test-connections` - Test de conectividad

## 🛠️ Configuración

### Settings (Singleton)
```python
# src/config/settings.py
services = {
    "general": "http://localhost:11434",
    "code": "http://localhost:11435", 
    "text": "http://localhost:11436"
}

popular_models = [
    "llama3.2:3b", "llama3.2:1b", 
    "qwen2.5:7b", "codellama:7b", "mistral:7b"
]
```

## 🔗 Dependencias

```txt
requests>=2.31.0      # HTTP requests
docker>=6.1.0         # Docker integration  
python-dotenv>=1.0.0  # Environment variables
flask>=2.3.0          # Web framework
flask-cors>=4.0.0     # CORS support
psutil>=5.9.0         # System monitoring
```

## 📱 Interfaz de Usuario

- **Diseño futurista** con tema cyberpunk y efectos de neón
- **Panel de estadísticas en tiempo real** con estilo consola hacker
- **Barras de progreso animadas** que cambian de color según la carga
- **Indicadores LED pulsantes** para estado de servicios
- **Responsive** para desktop y móvil
- **Chat estilo messenger** con mensajes diferenciados
- **Efectos de escaneo** y animaciones fluidas

## 🧪 Extensibilidad

La arquitectura modular permite fácil extensión:

1. **Nuevos servicios**: Implementar interfaces en `services/`
2. **Nuevas funcionalidades**: Agregar al controlador principal
3. **Nuevas interfaces**: Definir en `core/interfaces.py`
4. **Configuración**: Modificar `config/settings.py`

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.

---

**Desarrollado con ❤️ usando arquitectura modular y patrones de diseño modernos** 

## ⚡ Optimizaciones de Rendimiento

### 🚀 Mejoras Implementadas

1. **Configuración GPU Optimizada**
   - GPU principal usa toda la memoria disponible (`OLLAMA_GPU_LAYERS=-1`)
   - Servicios secundarios solo usan CPU para evitar competencia
   - Flash Attention habilitado para mayor eficiencia
   - Límites de modelos cargados simultáneamente

2. **Connection Pooling & Caching**
   - Reutilización de conexiones HTTP con `requests.Session`
   - Cache de modelos disponibles (60 segundos)
   - Cache de estadísticas técnicas (30 segundos)
   - Retry automático con backoff exponencial

3. **Monitoreo Inteligente**
   - Estadísticas actualizadas cada 15 segundos (antes 5s)
   - Cache de logs de Docker para reducir subprocess calls
   - Detección de GPU con cache de 5 minutos

4. **Configuración de Modelos Optimizada**
   - Contexto reducido para respuestas más rápidas (2048 tokens)
   - Límite de predicción ajustado (512 tokens)
   - Parámetros optimizados para RTX 4070 Laptop

## 🔧 Comandos de Despliegue

### Modo Optimizado (Solo servicio principal)
```bash
docker-compose up -d ollama
```

### Modo Multi-Servicio (Si necesitas separación)
```bash
docker-compose --profile multi-service up -d
```

## 📊 Monitoreo de Rendimiento

El panel de estadísticas muestra:
- **GPU**: Utilización, memoria y drivers
- **CPU**: Uso, cores y frecuencia
- **Memoria**: RAM disponible y utilizada
- **Performance**: Tokens/seg, tiempo de inferencia
- **Servicios**: Estado de conexión

## 🎯 Recomendaciones Adicionales

### este caso de uso es mi rtx 4070:

1. **Usar modelos cuantizados menores**:
   ```bash
   # Mejores opciones para tu GPU
   ollama pull llama3.2:1b    # Más rápido
   ollama pull llama3.2:3b    # Buen balance
   ollama pull qwen2.5:3b     # Eficiente para código
   ```

2. **Configuración de energía**:
   - Asegúrate que la laptop esté conectada
   - Modo de rendimiento alto en Windows
   - GPU no limitada por thermal throttling

3. **Memoria del sistema**:
   - Mínimo 16GB RAM recomendado
   - Cerrar aplicaciones innecesarias

### Benchmarks Esperados

Con las optimizaciones aplicadas:
- **Tiempo de carga inicial**: ~15-20 segundos (antes 25s)
- **Tokens por segundo**: 15-25 (modelos 3B), 8-15 (modelos 7B)
- **Tiempo de respuesta promedio**: 2-5 segundos

## 🐳 Docker Compose Optimizado

Configuración actual optimizada para una sola GPU:
- Servicio principal: Toda la GPU + 8GB RAM
- Servicios secundarios: Solo CPU (opcional)
- Memory mapping y lock optimizados

## 💡 Troubleshooting

### Si sigues experimentando lentitud:

1. **Verificar uso de GPU**:
   ```bash
   nvidia-smi -l 1
   ```

2. **Monitorear logs en tiempo real**:
   ```bash
   docker logs -f ollama-service
   ```

3. **Verificar temperaturas**:
   - GPU < 83°C
   - CPU < 85°C

4. **Liberar memoria de modelos**:
   ```bash
   curl -X POST http://localhost:11434/api/generate -d '{"model": "", "keep_alive": 0}'
   ```

## 🚀 Instalación Rápida

```bash
# Clonar repositorio
git clone <repo-url>
cd OllamaTest

# Crear entorno virtual
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# o
.venv\Scripts\activate     # Windows

# Instalar dependencias
pip install -r requirements.txt

# Iniciar servicios optimizados
docker-compose up -d ollama

# Iniciar interfaz web
python main.py
```

Visita: http://localhost:5000 
