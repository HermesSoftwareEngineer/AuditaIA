from flask import Flask
from flask_cors import CORS
import os
import logging
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv
from .extensions import db, migrate

# Carrega as variáveis de ambiente do arquivo .env (se existir)
load_dotenv()

def create_app(test_config=None):
    app = Flask(__name__)
    
    # A configuração agora é unificada e baseada em variáveis de ambiente.
    # Use valores padrão apenas para facilitar o desenvolvimento se as variáveis não estiverem definidas.
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'a-dev-secret-key')
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'a-dev-jwt-secret-key')
    
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        raise ValueError("Aa variável de ambiente DATABASE_URL não foi configurada. Verifique seu arquivo .env ou as configurações do ambiente.")
        
    # Supabase/Heroku usam 'postgres://', mas SQLAlchemy 1.4+ prefere 'postgresql://'
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
        
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['DEBUG'] = os.environ.get('FLASK_ENV', 'development') == 'development'
    
    # Inicializar extensões
    db.init_app(app)
    migrate.init_app(app, db)

    # Configurar CORS baseado em variável de ambiente FRONTEND_ORIGIN
    frontend_origin = os.environ.get('FRONTEND_ORIGIN', '*')
    CORS(
        app,
        origins=[frontend_origin],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["Content-Type", "Authorization", "X-Requested-With"],
        supports_credentials=True
    )

    # Importar e registrar componentes da aplicação
    from app.routes.auth import bp as auth_bp, init_db_command
    from app.routes.repasses import bp as repasses_bp
    from app.routes.configuracoes import bp as configuracoes_bp
    from app.routes.bot import bp as bot_bp, init_bot_blueprint
    
    # Registrar rotas (blueprints)
    app.register_blueprint(auth_bp)
    app.register_blueprint(repasses_bp)
    app.register_blueprint(configuracoes_bp)
    app.register_blueprint(bot_bp)

    # Registrar comando CLI
    app.cli.add_command(init_db_command)
    
    # Rota de teste
    @app.route('/')
    def index():
        return {'message': 'AuditaIA API is running!'}
    
    return app
