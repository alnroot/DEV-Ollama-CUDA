"""Flask web application with dependency injection."""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

from ..core.chat_controller import ChatController
from ..services.ollama_service import OllamaService
from ..services.model_repository import ModelRepository
from ..services.chat_history import ChatHistory
from ..services.technical_stats import TechnicalStatsService
from ..services.docker_commands import DockerCommandsService


def create_app() -> Flask:
    """Factory function to create Flask app with dependencies."""
    app = Flask(__name__)
    CORS(app)
    
    # Dependency injection
    ollama_service = OllamaService()
    model_repository = ModelRepository(ollama_service)
    chat_history = ChatHistory()
    technical_stats = TechnicalStatsService()
    docker_commands = DockerCommandsService()
    controller = ChatController(
        ollama_service, 
        model_repository, 
        chat_history,
        technical_stats,
        docker_commands
    )
    
    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/api/models/<service_type>')
    def get_models(service_type):
        models = controller.get_available_models(service_type)
        return jsonify(models)
    
    @app.route('/api/popular-models')
    def get_popular_models():
        models = controller.get_popular_models()
        return jsonify(models)
    
    @app.route('/api/chat', methods=['POST'])
    def chat():
        data = request.get_json()
        message = data.get('message', '')
        model = data.get('model', '')
        service_type = data.get('service_type', 'general')
        
        if not message or not model:
            return jsonify({"success": False, "error": "Mensaje y modelo requeridos"}), 400
        
        response = controller.send_message(message, model, service_type)
        return jsonify(response)
    
    @app.route('/api/download', methods=['POST'])
    def download_model():
        data = request.get_json()
        model_name = data.get('model_name', '')
        service_type = data.get('service_type', 'general')
        
        if not model_name:
            return jsonify({"success": False, "error": "Nombre del modelo requerido"}), 400
        
        response = controller.download_model(model_name, service_type)
        return jsonify(response)
    
    @app.route('/api/status')
    def status():
        status_data = controller.get_service_status()
        return jsonify(status_data)
    
    @app.route('/api/history')
    def history():
        history_data = controller.get_chat_history()
        return jsonify(history_data)
    
    @app.route('/api/clear-history', methods=['POST'])
    def clear_history():
        controller.clear_chat_history()
        return jsonify({"success": True, "message": "Historial eliminado"})
    
    @app.route('/api/technical-stats')
    def technical_stats():
        stats = controller.get_technical_stats()
        return jsonify(stats)
    
    @app.route('/api/docker/start', methods=['POST'])
    def start_docker():
        result = controller.start_docker_services()
        return jsonify(result)
    
    @app.route('/api/docker/stop', methods=['POST'])
    def stop_docker():
        result = controller.stop_docker_services()
        return jsonify(result)
    
    @app.route('/api/docker/restart', methods=['POST'])
    def restart_docker():
        result = controller.restart_docker_services()
        return jsonify(result)
    
    @app.route('/api/docker/status')
    def docker_status():
        status = controller.get_docker_status()
        return jsonify(status)
    
    @app.route('/api/test-connections')
    def test_connections():
        connections = controller.test_service_connections()
        return jsonify(connections)
    
    return app 