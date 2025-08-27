from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
import os
import logging
from logging.handlers import RotatingFileHandler

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    
    # Configuração baseada no ambiente
    env = os.environ.get('FLASK_ENV', 'development')
    
    if env == 'production':
        from app.config.production import ProductionConfig
        app.config.from_object(ProductionConfig)
    else:
        # Configuração de desenvolvimento
        app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///auditaia.db')
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['DEBUG'] = True
    
    # Inicializar extensões
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Configurar CORS
    CORS(app, origins=app.config.get('CORS_ORIGINS', ['*']))
    
    # Configurar logging
    if not app.debug and not app.testing:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        
        file_handler = RotatingFileHandler(
            app.config.get('LOG_FILE', 'logs/auditaia.log'),
            maxBytes=10240000, backupCount=10
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        
        app.logger.setLevel(logging.INFO)
        app.logger.info('AuditaIA startup')
    
    # Importar modelos para que as migrações funcionem
    from app.models.user import User
    
    # Registrar blueprints
    from app.routes.auth import bp as auth_bp
    app.register_blueprint(auth_bp)
    
    # Route raiz
    @app.route('/')
    def index():
        return {
            'message': 'AuditaIA API',
            'version': '1.0.0',
            'status': 'running',
            'endpoints': {
                'auth': '/v1/auth/',
                'health': '/v1/auth/health'
            }
        }
    
    # Health check global
    @app.route('/health')
    def health():
        return {'status': 'healthy', 'service': 'auditaia'}, 200
    
    return app