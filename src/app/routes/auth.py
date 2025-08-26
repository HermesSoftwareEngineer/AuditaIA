from flask import Blueprint, request, jsonify, current_app, g
import jwt
from datetime import datetime, timedelta
from functools import wraps
from app.models.user import User, db
import os
import logging

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
            return jsonify({'message': 'Token ausente!'}), 401

        try:
            # Decodificar o token
            jwt_secret = current_app.config.get('JWT_SECRET_KEY', current_app.config['SECRET_KEY'])
            data = jwt.decode(token, jwt_secret, algorithms=["HS256"])
            g.current_user = User.query.filter_by(id=data['user_id']).first()
            
            if not g.current_user:
                return jsonify({'message': 'Usuário não encontrado!'}), 401
                
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token expirado!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token inválido!'}), 401
        except Exception as e:
            logging.error(f"Erro na validação do token: {str(e)}")
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
            return jsonify({'message': 'Acesso negado. Privilégios de administrador necessários!'}), 403

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
        data = request.get_json()
        
        # Verificar dados
        if not data or not data.get('username') or not data.get('password') or not data.get('email'):
            return jsonify({'message': 'Username, email e password são obrigatórios!'}), 400
        
        # Verificar se usuário já existe
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'message': 'Usuário já existe!'}), 409
        
        if User.query.filter_by(email=data['email']).first():
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
        logging.error(f"Erro ao criar usuário: {str(e)}")
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
        data = request.get_json()
        
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({'message': 'Email e senha são obrigatórios'}), 401
        
        user = User.query.filter_by(email=data['email']).first()
        
        if not user:
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
        
        return jsonify({'message': 'Credenciais inválidas'}), 401
        
    except Exception as e:
        logging.error(f"Erro no login: {str(e)}")
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
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'Usuário não encontrado!'}), 404

    # Só admins ou o próprio usuário podem excluir
    if not (g.current_user.is_admin() or g.current_user.id == user_id):
        return jsonify({'message': 'Acesso negado!'}), 403

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
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'Usuário não encontrado!'}), 404

    # Só admins ou o próprio usuário podem atualizar
    if not (g.current_user.is_admin() or g.current_user.id == user_id):
        return jsonify({'message': 'Acesso negado!'}), 403

    data = request.get_json()
    
    # Atualiza campos permitidos
    if 'username' in data:
        user.username = data['username']
    if 'email' in data:
        user.email = data['email']
        
    # Verificação de senha para alteração
    if 'new_password' in data:
        # Se não for admin, exige senha atual
        if not g.current_user.is_admin() or g.current_user.id == user_id:
            if 'current_password' not in data or not user.check_password(data['current_password']):
                return jsonify({'message': 'Senha atual incorreta!'}), 400
                
        user.set_password(data['new_password'])
        
    # Apenas admin pode alterar user_type
    if g.current_user.is_admin() and 'user_type' in data:
        user.user_type = data['user_type']

    db.session.commit()
    return jsonify({'message': 'Usuário atualizado com sucesso.'}), 200

@bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint para monitoramento"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'service': 'auditaia-auth'
    }), 200

@bp.route('/first-setup', methods=['POST'])
def first_setup():
    """
    POST /v1/auth/first-setup
    Cria o primeiro usuário admin se nenhum usuário existir.
    Usado apenas na configuração inicial.
    Corpo JSON:
        {
            "username": "string",
            "email": "string",
            "password": "string"
        }
    Respostas:
        201: Admin criado com sucesso
        400: Dados incompletos
        409: Já existem usuários no sistema
    """
    try:
        # Verificar se já existem usuários
        if User.query.first():
            return jsonify({'message': 'Sistema já possui usuários cadastrados!'}), 409
        
        data = request.get_json()
        
        if not data or not data.get('username') or not data.get('password') or not data.get('email'):
            return jsonify({'message': 'Username, email e password são obrigatórios!'}), 400
        
        # Criar primeiro admin
        admin_user = User(
            username=data['username'], 
            email=data['email'],
            user_type='admin'
        )
        admin_user.set_password(data['password'])
        
        db.session.add(admin_user)
        db.session.commit()
        
        return jsonify({
            'message': 'Primeiro administrador criado com sucesso!',
            'user': {
                'id': admin_user.id,
                'username': admin_user.username,
                'email': admin_user.email,
                'user_type': admin_user.user_type
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        logging.error(f"Erro ao criar primeiro admin: {str(e)}")
        return jsonify({'message': 'Erro interno do servidor'}), 500

def init_auth_blueprint():
    return bp
