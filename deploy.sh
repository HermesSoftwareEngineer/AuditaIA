#!/bin/bash

echo "🚀 Iniciando deploy do AuditaIA..."

# Verificar se .env existe
if [ ! -f .env ]; then
    echo "❌ Arquivo .env não encontrado! Copie .env.example para .env e configure as variáveis."
    exit 1
fi

# Parar containers existentes
echo "⏹️  Parando containers existentes..."
docker-compose down

# Construir imagens
echo "🔨 Construindo imagens..."
docker-compose build --no-cache

# Subir banco de dados
echo "🗄️  Iniciando banco de dados..."
docker-compose up -d db

# Aguardar banco estar pronto
echo "⏳ Aguardando banco de dados..."
sleep 10

# Executar migrações
echo "📊 Executando migrações do banco..."
docker-compose run --rm app flask db upgrade

# Criar usuário admin inicial (se não existir)
echo "👤 Criando usuário admin inicial..."
docker-compose run --rm app python -c "
from app import create_app
from app.models.user import User, db

app = create_app()
with app.app_context():
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(username='admin', email='admin@auditaia.com', user_type='admin')
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print('Usuário admin criado: admin/admin123')
    else:
        print('Usuário admin já existe')
"

# Subir aplicação
echo "🚀 Iniciando aplicação..."
docker-compose up -d

echo "✅ Deploy concluído!"
echo "📍 Aplicação disponível em: http://localhost:5000"
echo "📊 Banco de dados disponível em: localhost:5432"
echo ""
echo "🔑 Credenciais iniciais:"
echo "   Usuário: admin"
echo "   Senha: admin123"
echo ""
echo "📋 Para acompanhar os logs: docker-compose logs -f"
