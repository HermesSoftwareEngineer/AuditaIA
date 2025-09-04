from flask import Flask
from flask_cors import CORS
import os
from .logger import setup_logging
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv
from .extensions import db, migrate

# Carrega as variáveis de ambiente do arquivo .env (se existir)
load_dotenv()

def create_app(test_config=None):
    app = Flask(__name__)
    
    # Configurar logging primeiro para poder usar durante a inicialização
    setup_logging(app)
    app.logger.info("Iniciando aplicação AuditaIA")
    
    # A configuração agora é unificada e baseada em variáveis de ambiente.
    # Use valores padrão apenas para facilitar o desenvolvimento se as variáveis não estiverem definidas.
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'a-dev-secret-key')
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'a-dev-jwt-secret-key')
    app.logger.info("Configurações básicas carregadas")
    
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        app.logger.error("DATABASE_URL não configurada. Aplicação não pode iniciar.")
        raise ValueError("Aa variável de ambiente DATABASE_URL não foi configurada. Verifique seu arquivo .env ou as configurações do ambiente.")
        
    # Supabase/Heroku usam 'postgres://', mas SQLAlchemy 1.4+ prefere 'postgresql://'
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
        app.logger.debug("URL do banco corrigida de 'postgres://' para 'postgresql://'")
        
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['DEBUG'] = os.environ.get('FLASK_ENV', 'development') == 'development'
    app.logger.info(f"Modo de execução: {os.environ.get('FLASK_ENV', 'development')}")
    
    # Inicializar extensões
    try:
        db.init_app(app)
        migrate.init_app(app, db)
        app.logger.info("Conexão com o banco de dados inicializada com sucesso")
    except Exception as e:
        app.logger.error(f"Erro ao inicializar banco de dados: {str(e)}")
        raise

    # Configurar CORS baseado em variável de ambiente FRONTEND_ORIGIN
    frontend_origin = os.environ.get('FRONTEND_ORIGIN', '*')
    CORS(
        app,
        origins=[frontend_origin],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["Content-Type", "Authorization", "X-Requested-With"],
        supports_credentials=True
    )
    app.logger.info(f"CORS configurado com origin: {frontend_origin}")

    # Importar e registrar componentes da aplicação
    app.logger.debug("Carregando blueprints...")
    try:
        from app.routes.auth import bp as auth_bp, init_db_command
        from app.routes.repasses import bp as repasses_bp
        from app.routes.configuracoes import bp as configuracoes_bp
        from app.routes.bot import bp as bot_bp, init_bot_blueprint
        
        # Registrar rotas (blueprints)
        app.register_blueprint(auth_bp)
        app.logger.debug("Blueprint 'auth' registrado")
        
        app.register_blueprint(repasses_bp)
        app.logger.debug("Blueprint 'repasses' registrado")
        
        app.register_blueprint(configuracoes_bp)
        app.logger.debug("Blueprint 'configuracoes' registrado")
        
        app.register_blueprint(bot_bp)
        app.logger.debug("Blueprint 'bot' registrado")

        # Registrar comando CLI
        app.cli.add_command(init_db_command)
        app.logger.info("Todos os blueprints e comandos registrados com sucesso")
    except Exception as e:
        app.logger.error(f"Erro ao carregar blueprints: {str(e)}")
        raise
    
    # Rota de teste
    @app.route('/')
    def index():
        app.logger.debug("Rota index acessada")
        return {'message': 'AuditaIA API is running!'}
    
    app.logger.info("Aplicação AuditaIA inicializada com sucesso")
    return app
