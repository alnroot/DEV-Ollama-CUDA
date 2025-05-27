#!/usr/bin/env python3
"""
Ollama Chat - Minimal Web Interface
Main entry point for the application
"""

from src.web.app import create_app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True) 