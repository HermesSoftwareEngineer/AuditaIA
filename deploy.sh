#!/bin/bash

echo "🚀 Preparando deploy com Docker..."

# Verificar se requirements.txt existe
if [ ! -f requirements.txt ]; then
    echo "❌ Arquivo requirements.txt não encontrado!"
    exit 1
fi

# Verificar se Dockerfile existe
if [ ! -f Dockerfile ]; then
    echo "❌ Dockerfile não encontrado!"
    exit 1
fi

# Verificar se docker-compose.yml existe
if [ ! -f docker-compose.yml ]; then
    echo "❌ docker-compose.yml não encontrado!"
    exit 1
fi

# Verificar estrutura do projeto
echo "📁 Verificando estrutura do projeto..."
if [ ! -d "src" ]; then
    echo "❌ Pasta src não encontrada!"
    exit 1
fi

if [ ! -f "src/app.py" ]; then
    echo "❌ Arquivo src/app.py não encontrado!"
    exit 1
fi

# Fazer commit das mudanças
echo "💾 Commitando mudanças..."
git add .
git commit -m "Configuração para deploy com Docker" || echo "Nada para commitar"

# Push para GitHub
echo "📤 Enviando para GitHub..."
git push origin main

echo "✅ Projeto preparado para deploy!"
echo ""
echo "🌐 Para rodar localmente:"
echo "1. Execute: docker-compose up --build"
echo "2. Acesse: http://localhost:5000"