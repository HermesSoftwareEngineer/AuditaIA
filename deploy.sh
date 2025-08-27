#!/bin/bash

echo "🚀 Preparando deploy para Render..."

# Verificar se requirements.txt existe
if [ ! -f requirements.txt ]; then
    echo "❌ Arquivo requirements.txt não encontrado!"
    exit 1
fi

# Verificar se render.yaml existe
if [ ! -f render.yaml ]; then
    echo "❌ Arquivo render.yaml não encontrado!"
    exit 1
fi

# Remover arquivos Docker se existirem
echo "🧹 Removendo arquivos Docker..."
rm -f Dockerfile docker-compose.yml .dockerignore

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
git commit -m "Prepare for Render deployment" || echo "Nada para commitar"

# Push para GitHub
echo "📤 Enviando para GitHub..."
git push origin main

echo "✅ Projeto preparado para deploy!"
echo ""
echo "🌐 Próximos passos no Render:"
echo "1. Vá para render.com"
echo "2. Conecte seu repositório GitHub"
echo "3. Crie novo Blueprint"
echo "4. Configure variáveis de ambiente se necessário"
echo "5. Deploy automático será iniciado"
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
