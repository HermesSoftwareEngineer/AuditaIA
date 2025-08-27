#!/usr/bin/env bash
# Start script para Render - Simplificado

set -o errexit

echo "🚀 Iniciando AuditaIA..."

# Definir variáveis de ambiente
export FLASK_APP=src.app:create_app
export FLASK_ENV=production

# Executar migrações se DATABASE_URL estiver disponível
if [ "$DATABASE_URL" ]; then
    echo "📊 Executando migrações..."
    cd src
    python -c "
try:
    from app import create_app
    from flask_migrate import upgrade
    app = create_app()
    with app.app_context():
        upgrade()
    print('✅ Migrações concluídas')
except Exception as e:
    print(f'⚠️ Erro nas migrações: {e}')
" || echo "⚠️ Migrações falharam"
    cd ..
fi

# Iniciar aplicação
echo "🌐 Iniciando servidor..."
exec gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 60 src.app:create_app
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
