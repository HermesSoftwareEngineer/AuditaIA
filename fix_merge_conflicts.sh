#!/bin/bash

echo "🧹 Resolvendo conflitos de merge..."

# Abortar merge atual
git merge --abort

echo "🗑️ Removendo arquivos __pycache__ do Git..."

# Remover todos os arquivos __pycache__ do Git
git rm -r --cached src/ai/__pycache__/ 2>/dev/null || true
git rm -r --cached src/ai/nodes/__pycache__/ 2>/dev/null || true
git rm -r --cached src/app/__pycache__/ 2>/dev/null || true
git rm -r --cached **/__pycache__/ 2>/dev/null || true

# Remover arquivos __pycache__ do sistema de arquivos
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -name "*.pyc" -delete 2>/dev/null || true
find . -name "*.pyo" -delete 2>/dev/null || true

echo "📝 Adicionando .gitignore..."
git add .gitignore

echo "💾 Commitando limpeza..."
git commit -m "Remove __pycache__ files and add .gitignore"

echo "🔄 Tentando merge novamente..."
git merge main

if [ $? -eq 0 ]; then
    echo "✅ Merge realizado com sucesso!"
else
    echo "⚠️ Ainda há conflitos. Resolva manualmente e execute:"
    echo "   git add ."
    echo "   git commit -m 'Resolve merge conflicts'"
fi
