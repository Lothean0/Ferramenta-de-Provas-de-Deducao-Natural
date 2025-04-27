__version__ = "2025.04.27"

from servidor.config import C_RED, C_YELLOW, C_END

try:
    from servidor.app.routes.node_routes import node_bp
    from servidor.app.routes.rules_routes import rules_bp
    from servidor.app.routes.file_routes import file_bp
    from servidor.app.routes.misc_routes import misc_bp
    print(f"{__package__} package " + C_YELLOW + f"(version {__version__}) " + C_END + f"is working.")


    def register_routes(app):
        app.register_blueprint(node_bp, url_prefix="/api")
        app.register_blueprint(rules_bp, url_prefix="/api")
        app.register_blueprint(file_bp, url_prefix="/api")
        app.register_blueprint(misc_bp, url_prefix="/api")


except ImportError as e:
    print(C_RED + f"Error importing coq_codegen package: {e}" + C_END)
