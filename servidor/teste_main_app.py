"""

ISTO VAI SERVIR PARA QUANDO TIVERMOS A BUILD DO CLIENT

"""

import os
from flask import Flask, send_from_directory
from flask_cors import CORS

from app.routes.node_routes import node_bp
from app.routes.rules_routes import rules_bp
from app.routes.file_routes import file_bp
from app.routes.misc_routes import misc_bp

from app.config import Config


UPLOAD_FOLDER = 'uploads'
DOWNLOAD_FOLDER = 'downloads'

app = Flask(__name__, static_folder='dist', static_url_path='/')
app.config.from_object(Config)
CORS(app, origins="*")

# Register your route Blueprints
app.register_blueprint(node_bp, url_prefix='/api')
app.register_blueprint(rules_bp, url_prefix='/api')
app.register_blueprint(file_bp, url_prefix='/api')
app.register_blueprint(misc_bp, url_prefix='/api')

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

if __name__ == '__main__':
    app.run(debug=True, port=3000)
