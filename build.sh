#!/usr/bin/env bash
# Build script para Render - Simplificado

set -o errexit

echo "🔧 Instalando dependências..."
pip install --upgrade pip
pip install -r requirements.txt

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
