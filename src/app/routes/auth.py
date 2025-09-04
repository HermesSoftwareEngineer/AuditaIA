from flask import Blueprint, request, jsonify, current_app, g
import jwt
from datetime import datetime, timedelta
from functools import wraps
from app.models.user import User
from app.extensions import db
from sqlalchemy import select, text
from sqlalchemy.exc import OperationalError
import os
import logging
import click
from flask.cli import with_appcontext

bp = Blueprint('auth', __name__, url_prefix='/v1/auth')

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # Tentar obter o token do cabeçalho Authorization
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(" ")[1]
        
        # Se não há token, retorna erro
        if not token:
            current_app.logger.warning("Tentativa de acesso sem token de autenticação")
            return jsonify({'message': 'Token ausente!'}), 401

        try:
            # Decodificar o token
            jwt_secret = current_app.config.get('JWT_SECRET_KEY', current_app.config['SECRET_KEY'])
            data = jwt.decode(token, jwt_secret, algorithms=["HS256"])
            # g.current_user = User.query.filter_by(id=data['user_id']).first()
            g.current_user = db.session.get(User, data['user_id'])
            
            if not g.current_user:
                current_app.logger.warning(f"Token com user_id inexistente: {data.get('user_id')}")
                return jsonify({'message': 'Usuário não encontrado!'}), 401
            
            current_app.logger.debug(f"Autenticação bem-sucedida para usuário: {g.current_user.username}")
                
        except jwt.ExpiredSignatureError:
            current_app.logger.warning("Tentativa de acesso com token expirado")
            return jsonify({'message': 'Token expirado!'}), 401
        except jwt.InvalidTokenError:
            current_app.logger.warning("Tentativa de acesso com token inválido")
            return jsonify({'message': 'Token inválido!'}), 401
        except Exception as e:
            current_app.logger.error(f"Erro na validação do token: {str(e)}")
            return jsonify({'message': 'Erro interno na autenticação!'}), 500

        return f(*args, **kwargs)

    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # Primeiro verifica se o usuário está autenticado
        token_decorator = token_required(lambda *args, **kwargs: None)
        result = token_decorator(*args, **kwargs)
        if result is not None:  # Isso significa que token_required retornou um erro
            return result
        
        # Agora verifica se o usuário é admin
        if not g.current_user.is_admin():
            current_app.logger.warning(f"Usuário {g.current_user.username} tentou acessar função restrita a administradores")
            return jsonify({'message': 'Acesso negado. Privilégios de administrador necessários!'}), 403

        current_app.logger.debug(f"Acesso administrativo concedido para usuário: {g.current_user.username}")
        return f(*args, **kwargs)
    
    return decorated

@bp.route('/register', methods=['POST'])
@admin_required  # Apenas admins podem registrar novos usuários
def register():
    """
    POST /v1/auth/register
    Cria um novo usuário. Apenas administradores podem acessar.
    Corpo JSON:
        {
            "username": "string",
            "email": "string",
            "password": "string",
            "user_type": "string" (opcional, padrão 'user')
        }
    Respostas:
        201: Usuário criado com sucesso
        400: Dados incompletos
        409: Usuário ou email já existe
    """
    try:
        current_app.logger.info("Tentativa de registro de novo usuário por administrador")
        data = request.get_json()
        
        # Verificar dados
        if not data or not data.get('username') or not data.get('password') or not data.get('email'):
            current_app.logger.warning("Tentativa de registro com dados incompletos")
            return jsonify({'message': 'Username, email e password são obrigatórios!'}), 400
        
        # Verificar se usuário já existe
        # if User.query.filter_by(username=data['username']).first():
        if db.session.execute(select(User).filter_by(username=data['username'])).scalar_one_or_none():
            current_app.logger.warning(f"Tentativa de registro de username já existente: {data['username']}")
            return jsonify({'message': 'Usuário já existe!'}), 409
        
        # if User.query.filter_by(email=data['email']).first():
        if db.session.execute(select(User).filter_by(email=data['email'])).scalar_one_or_none():
            current_app.logger.warning(f"Tentativa de registro com email já cadastrado: {data['email']}")
            return jsonify({'message': 'Email já cadastrado!'}), 409
        
        # Criar novo usuário
        new_user = User(
            username=data['username'], 
            email=data['email'],
            user_type=data.get('user_type', 'user')  # Default é 'user'
        )
        new_user.set_password(data['password'])
        
        db.session.add(new_user)
        db.session.commit()
        
        current_app.logger.info(f"Novo usuário criado com sucesso: {new_user.username} (tipo: {new_user.user_type})")
        return jsonify({
            'message': 'Usuário criado com sucesso!',
            'user': {
                'id': new_user.id,
                'username': new_user.username,
                'email': new_user.email,
                'user_type': new_user.user_type
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Erro ao criar usuário: {str(e)}", exc_info=True)
        return jsonify({'message': 'Erro interno do servidor'}), 500

@bp.route('/login', methods=['POST'])
def login():
    """
    POST /v1/auth/login
    Realiza login do usuário e retorna um token JWT.
    Corpo JSON:
        {
            "email": "string",
            "password": "string"
        }
    Respostas:
        200: Login realizado com sucesso + token JWT
        401: Dados ausentes ou senha inválida
        404: Usuário não encontrado
    """
    try:
        current_app.logger.info("Tentativa de login")
        data = request.get_json()
        
        if not data or not data.get('email') or not data.get('password'):
            current_app.logger.warning("Tentativa de login com dados incompletos")
            return jsonify({'message': 'Email e senha são obrigatórios'}), 401
        
        # user = User.query.filter_by(email=data['email']).first()
        user = db.session.execute(select(User).filter_by(email=data['email'])).scalar_one_or_none()
        
        if not user:
            current_app.logger.warning(f"Tentativa de login com email não cadastrado: {data['email']}")
            return jsonify({'message': 'Credenciais inválidas'}), 401
        
        if user.check_password(data['password']):
            # Usar JWT_SECRET_KEY se disponível, senão usar SECRET_KEY
            jwt_secret = current_app.config.get('JWT_SECRET_KEY', current_app.config['SECRET_KEY'])
            
            # Gerar token JWT com expiração configurável
            expires_delta = current_app.config.get('JWT_ACCESS_TOKEN_EXPIRES', timedelta(hours=24))
            
            token = jwt.encode({
                'user_id': user.id,
                'user_type': user.user_type,
                'exp': datetime.utcnow() + expires_delta,
                'iat': datetime.utcnow()
            }, jwt_secret, algorithm='HS256')
            
            current_app.logger.info(f"Login bem-sucedido para usuário: {user.username}")
            return jsonify({
                'message': 'Login realizado com sucesso',
                'token': token,
                'expires_in': expires_delta.total_seconds(),
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'user_type': user.user_type
                }
            })
        
        current_app.logger.warning(f"Tentativa de login com senha incorreta para usuário: {user.username}")
        return jsonify({'message': 'Credenciais inválidas'}), 401
        
    except Exception as e:
        current_app.logger.error(f"Erro no login: {str(e)}", exc_info=True)
        return jsonify({'message': 'Erro interno do servidor'}), 500

@bp.route('/me', methods=['GET'])
@token_required
def get_user_profile():
    """
    GET /v1/auth/me
    Retorna os dados do usuário autenticado.
    Cabeçalho:
        Authorization: Bearer <token>
    Respostas:
        200: Dados do usuário
        401: Token ausente/inválido
    """
    user = g.current_user
    current_app.logger.debug(f"Perfil acessado pelo usuário: {user.username}")
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'user_type': user.user_type,
        'created_at': user.created_at
    })

@bp.route('/user/<int:user_id>', methods=['DELETE'])
@token_required
def delete_user(user_id):
    """
    DELETE /v1/auth/user/<user_id>
    Exclui um usuário pelo ID. Apenas admins ou o próprio usuário podem excluir.
    Cabeçalho:
        Authorization: Bearer <token>
    Respostas:
        200: Usuário excluído com sucesso
        403: Acesso negado
        404: Usuário não encontrado
    """
    # user = User.query.get(user_id)
    user = db.session.get(User, user_id)
    if not user:
        current_app.logger.warning(f"Tentativa de exclusão de usuário inexistente: ID {user_id}")
        return jsonify({'message': 'Usuário não encontrado!'}), 404

    # Só admins ou o próprio usuário podem excluir
    if not (g.current_user.is_admin() or g.current_user.id == user_id):
        current_app.logger.warning(f"Usuário {g.current_user.username} tentou excluir outro usuário sem permissão: ID {user_id}")
        return jsonify({'message': 'Acesso negado!'}), 403

    current_app.logger.info(f"Usuário {user.username} (ID {user_id}) excluído por {g.current_user.username}")
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'Usuário excluído com sucesso.'}), 200

@bp.route('/user/<int:user_id>', methods=['PUT'])
@token_required
def update_user(user_id):
    """
    PUT /v1/auth/user/<user_id>
    Atualiza dados de um usuário pelo ID. Apenas admins ou o próprio usuário podem atualizar.
    Para alterar a senha, é necessário fornecer a senha atual.
    Cabeçalho:
        Authorization: Bearer <token>
    Corpo JSON (campos opcionais):
        {
            "username": "string",
            "email": "string",
            "current_password": "string", (necessário para alteração de senha)
            "new_password": "string",
            "user_type": "string" (apenas admin)
        }
    Respostas:
        200: Usuário atualizado com sucesso
        400: Senha atual incorreta
        403: Acesso negado
        404: Usuário não encontrado
    """
    # user = User.query.get(user_id)
    user = db.session.get(User, user_id)
    if not user:
        current_app.logger.warning(f"Tentativa de atualização de usuário inexistente: ID {user_id}")
        return jsonify({'message': 'Usuário não encontrado!'}), 404

    # Só admins ou o próprio usuário podem atualizar
    if not (g.current_user.is_admin() or g.current_user.id == user_id):
        current_app.logger.warning(f"Usuário {g.current_user.username} tentou atualizar outro usuário sem permissão: ID {user_id}")
        return jsonify({'message': 'Acesso negado!'}), 403

    data = request.get_json()
    changes = []
    
    # Atualiza campos permitidos
    if 'username' in data:
        user.username = data['username']
        changes.append("username")
    if 'email' in data:
        user.email = data['email']
        changes.append("email")
        
    # Verificação de senha para alteração
    if 'new_password' in data:
        # Se não for admin, exige senha atual
        if not g.current_user.is_admin() or g.current_user.id == user_id:
            if 'current_password' not in data or not user.check_password(data['current_password']):
                current_app.logger.warning(f"Tentativa de alteração de senha com senha atual incorreta para usuário: {user.username}")
                return jsonify({'message': 'Senha atual incorreta!'}), 400
                
        user.set_password(data['new_password'])
        changes.append("password")
        
    # Apenas admin pode alterar user_type
    if g.current_user.is_admin() and 'user_type' in data:
        user.user_type = data['user_type']
        changes.append("user_type")

    db.session.commit()
    current_app.logger.info(f"Usuário {user.username} (ID {user_id}) atualizado por {g.current_user.username}. Campos alterados: {', '.join(changes)}")
    return jsonify({'message': 'Usuário atualizado com sucesso.'}), 200

@bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint para monitoramento"""
    try:
        db_status = "disconnected"
        if hasattr(db, 'engine'):
            try:
                # result = db.session.execute(db.text('SELECT 1'))
                db.session.execute(text('SELECT 1'))
                db_status = "connected"
                current_app.logger.debug("Health check realizado com sucesso: banco de dados conectado")
            except Exception as e:
                db_status = f"error: {str(e)}"
                current_app.logger.error(f"Health check falhou na conexão com o banco de dados: {str(e)}")
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat(),
            'service': 'auditaia-auth',
            'database': db_status,
            'version': '1.0.0'
        }), 200
    except Exception as e:
        current_app.logger.error(f"Health check falhou: {str(e)}")
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 500

@bp.route('/status', methods=['GET'])
def status():
    """Status endpoint simplificado"""
    current_app.logger.debug("Status endpoint acessado")
    return jsonify({
        'message': 'AuditaIA API está funcionando',
        'timestamp': datetime.utcnow().isoformat(),
        'endpoints': {
            'auth': '/v1/auth/',
            'health': '/v1/auth/health',
            'login': '/v1/auth/login',
            'register': '/v1/auth/register (admin only)'
        }
    }), 200

@bp.route('/first-setup', methods=['POST'])
def first_setup():
    """
    POST /v1/auth/first-setup
    Cria o primeiro usuário admin se nenhum usuário existir.
    
    Corpo JSON:
        {
            "username": "string",
            "email": "string",
            "password": "string"
        }
    """
    try:
        current_app.logger.info("Tentativa de configuração inicial (first-setup)")
        data = request.get_json()
        
        # Validar dados básicos
        if not all([data.get('username'), data.get('email'), data.get('password')]):
            current_app.logger.warning("Tentativa de configuração inicial com dados incompletos")
            return jsonify({'message': 'Username, email e password são obrigatórios!'}), 400
            
        # Verificar se já existem usuários
        if db.session.execute(select(User)).first():
            current_app.logger.warning("Tentativa de configuração inicial quando já existem usuários")
            return jsonify({'message': 'Sistema já possui usuários cadastrados!'}), 409
            
        # Criar primeiro admin
        admin_user = User(
            username=data['username'], 
            email=data['email'],
            user_type='admin'
        )
        admin_user.set_password(data['password'])
        
        db.session.add(admin_user)
        db.session.commit()
        
        current_app.logger.info(f"Primeiro administrador criado com sucesso: {admin_user.username}")
        return jsonify({
            'message': 'Primeiro administrador criado com sucesso!',
            'user': {
                'id': admin_user.id,
                'username': admin_user.username,
                'email': admin_user.email
            }
        }), 201
        
    except OperationalError:
        db.session.rollback()
        current_app.logger.error("Erro operacional no banco de dados durante configuração inicial")
        return jsonify({'message': "Erro de banco de dados. Verifique se o banco foi inicializado."}), 500
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Erro na configuração inicial: {str(e)}", exc_info=True)
        return jsonify({'message': 'Erro interno do servidor'}), 500

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Limpa os dados existentes e cria novas tabelas."""
    try:
        # Garante que o modelo User seja importado
        from app.models.user import User
        
        # Mostra as tabelas que serão criadas
        click.echo(f"Modelos registrados: {db.Model.registry._class_registry.keys()}")
        current_app.logger.info(f"Inicializando banco de dados. Modelos: {db.Model.registry._class_registry.keys()}")
        
        # Cria as tabelas
        db.create_all()
        current_app.logger.info("Banco de dados inicializado com sucesso")
        click.echo('Banco de dados inicializado com sucesso.')
    except Exception as e:
        current_app.logger.error(f"Erro ao inicializar banco de dados: {str(e)}", exc_info=True)
        click.echo(f'ERRO ao inicializar banco: {str(e)}')