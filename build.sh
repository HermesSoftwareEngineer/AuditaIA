#!/usr/bin/env bash
# Build script para Render

set -o errexit

echo "🔧 Atualizando pip..."
python -m pip install --upgrade pip

echo "📦 Instalando dependências..."
pip install --no-cache-dir -r requirements.txt

echo "📁 Criando diretórios necessários..."
mkdir -p logs

echo "🗄️ Configurando banco de dados..."
export FLASK_APP=src.app:create_app
cd src

# Inicializar banco se necessário
if [ "$DATABASE_URL" ]; then
    echo "📊 Executando migrações..."
    python -m flask db upgrade || echo "⚠️ Migrações falharam ou não necessárias"
fi

echo "✅ Build concluído!"
