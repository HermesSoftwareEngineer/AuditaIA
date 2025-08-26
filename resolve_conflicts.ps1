Write-Host "🧹 Resolvendo conflitos de merge definitivamente..." -ForegroundColor Yellow

# Remover todos os arquivos __pycache__ em conflito
Write-Host "🗑️ Removendo arquivos __pycache__ conflitantes..." -ForegroundColor Cyan

# Lista dos arquivos em conflito para remover
$conflictFiles = @(
    "src/ai/__pycache__/custom_types.cpython-311.pyc",
    "src/ai/__pycache__/graph.cpython-311.pyc", 
    "src/ai/__pycache__/llms.cpython-311.pyc",
    "src/ai/__pycache__/prompts_templates.cpython-311.pyc",
    "src/ai/nodes/__pycache__/coleta.cpython-311.pyc",
    "src/ai/nodes/__pycache__/decisor.cpython-311.pyc"
)

foreach ($file in $conflictFiles) {
    if (Test-Path $file) {
        Remove-Item $file -Force
        Write-Host "Removido: $file" -ForegroundColor Green
    }
    
    # Remover do Git também
    git rm --cached $file 2>$null
}

# Remover todos os diretórios __pycache__ restantes
Get-ChildItem -Path . -Recurse -Directory -Name "__pycache__" | ForEach-Object {
    $fullPath = Join-Path (Get-Location) $_
    Remove-Item $fullPath -Recurse -Force -ErrorAction SilentlyContinue
    Write-Host "Removido diretório: $fullPath" -ForegroundColor Green
}

# Remover arquivos .pyc individuais
Get-ChildItem -Path . -Recurse -File -Include "*.pyc", "*.pyo" | ForEach-Object {
    Remove-Item $_.FullName -Force
    Write-Host "Removido: $($_.FullName)" -ForegroundColor Green
}

Write-Host "✅ Limpeza concluída!" -ForegroundColor Green
