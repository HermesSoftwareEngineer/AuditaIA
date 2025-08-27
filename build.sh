#!/usr/bin/env bash
# Build script para Render - Com tratamento de erros

set -o errexit

echo "🔧 Atualizando pip..."
python -m pip install --upgrade pip

echo "📦 Instalando dependências principais..."
# Instalar dependências uma por uma para melhor diagnóstico
pip install --no-cache-dir Flask==3.0.0
pip install --no-cache-dir Werkzeug==3.0.1
pip install --no-cache-dir Flask-SQLAlchemy==3.1.1
pip install --no-cache-dir Flask-Migrate==4.0.5
pip install --no-cache-dir Flask-CORS==4.0.0
pip install --no-cache-dir PyJWT==2.8.0
pip install --no-cache-dir python-dotenv==1.0.0
pip install --no-cache-dir psycopg2-binary==2.9.9
pip install --no-cache-dir gunicorn==21.2.0

echo "📁 Criando diretórios necessários..."
mkdir -p logs

echo "✅ Build concluído!"
echo "🗄️ Configurando banco de dados..."
# Render executa as migrações automaticamente se DATABASE_URL estiver configurado
export FLASK_APP=src.app:create_app
cd src

# Inicializar banco se necessário
if [ "$DATABASE_URL" ]; then
    echo "📊 Executando migrações..."
    python -m flask db upgrade || echo "⚠️ Migrações falharam ou não necessárias"
fi

echo "✅ Build concluído!"
