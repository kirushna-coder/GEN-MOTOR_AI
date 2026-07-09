from flask import Flask
from flask_cors import CORS
from app.config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    CORS(app)
    
    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.tools import tools_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(tools_bp, url_prefix='/api')
    
    @app.route('/api/health')
    def health():
        return {"status": "ok", "message": "Genmotor AI Platform API is running"}
        
    return app
