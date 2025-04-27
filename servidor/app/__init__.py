import os

from flask import Flask, send_from_directory
from flask_cors import CORS
from servidor.app.config import Config
from servidor.app.routes import register_routes


def create_app():

    base_dir = os.path.abspath(os.path.dirname(__file__))
    project_root = os.path.abspath(os.path.join(base_dir, '..'))

    app = Flask(__name__, static_folder=os.path.join(project_root, 'dist'), static_url_path='/')

    app.config.from_object(Config)

    CORS(app, origins="*")

    register_routes(app)
    register_static_routes(app)

    return app


def register_static_routes(app):

    @app.route('/')
    def serve_index():
        return send_from_directory(app.static_folder, 'index.html')

    @app.route('/<path:path>')
    def serve_react_app(path):
        file_path = os.path.join(app.static_folder, path)
        if os.path.exists(file_path):
            return send_from_directory(app.static_folder, path)
        else:
            return send_from_directory(app.static_folder, 'index.html')
