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
# Define a variável de ambiente para os comandos do Flask
export FLASK_APP=src.app:create_app

# Inicializar banco se necessário
if [ "$DATABASE_URL" ]; then
    echo "📊 Executando migrações..."
    # Executa o comando a partir da raiz do projeto
    python -m flask db upgrade || echo "⚠️ Migrações falharam ou não necessárias"
fi

echo "✅ Build concluído!"
