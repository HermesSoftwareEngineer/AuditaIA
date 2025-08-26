#!/usr/bin/env bash
# Start script para Render

set -o errexit

echo "🚀 Iniciando AuditaIA..."

# Definir variáveis de ambiente
export FLASK_APP=src.app:create_app
export FLASK_ENV=production

# Executar migrações se necessário
if [ "$DATABASE_URL" ]; then
    cd src
    echo "📊 Verificando migrações..."
    python -m flask db upgrade || echo "⚠️ Sem migrações para executar"
    cd ..
fi

# Criar usuário admin inicial se não existir
if [ "$DATABASE_URL" ]; then
    echo "👤 Verificando usuário admin..."
    cd src
    python -c "
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models.user import User, db

app = create_app()
with app.app_context():
    try:
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin', 
                email=os.environ.get('ADMIN_EMAIL', 'admin@auditaia.com'), 
                user_type='admin'
            )
            admin.set_password(os.environ.get('ADMIN_PASSWORD', 'admin123'))
            db.session.add(admin)
            db.session.commit()
            print('✅ Usuário admin criado')
        else:
            print('ℹ️ Usuário admin já existe')
    except Exception as e:
        print(f'⚠️ Erro ao criar admin: {e}')
" || echo "⚠️ Erro na criação do usuário admin"
    cd ..
fi

# Iniciar aplicação com Gunicorn
echo "🌐 Iniciando servidor..."
exec gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 60 --keep-alive 5 --max-requests 1000 --preload src.app:create_app
