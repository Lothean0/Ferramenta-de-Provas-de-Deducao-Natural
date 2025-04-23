from servidor.app.routes.node_routes import node_bp
from servidor.app.routes.rules_routes import rules_bp
from servidor.app.routes.file_routes import file_bp
from servidor.app.routes.misc_routes import misc_bp

def register_routes(app):
    app.register_blueprint(node_bp, url_prefix="/api")
    app.register_blueprint(rules_bp, url_prefix="/api")
    app.register_blueprint(file_bp, url_prefix="/api")
    app.register_blueprint(misc_bp, url_prefix="/api")
