# AuditaIA API

## Configuração do Ambiente de Desenvolvimento Local

Siga estes passos para configurar e rodar a aplicação na sua máquina.

### 1. Pré-requisitos
- Python 3.8+
- `pip` e `venv`

### 2. Crie um Ambiente Virtual
```bash
# Crie o ambiente virtual
python -m venv venv

# Ative o ambiente
# No Windows:
venv\Scripts\activate
# No macOS/Linux:
source venv/bin/activate
```

### 3. Instale as Dependências
Com o ambiente ativado, instale os pacotes necessários:
```bash
pip install -r requirements.txt
```

### 4. Crie o Banco de Dados (Migrações)
Este comando criará o arquivo `auditaia.db` (se não existir) e criará todas as tabelas necessárias, como a tabela `user`.
```bash
# Certifique-se de que FLASK_APP está configurado
# No Windows (cmd):
set FLASK_APP=src.app:create_app
# No Windows (PowerShell):
$env:FLASK_APP="src.app:create_app"
# No macOS/Linux:
export FLASK_APP=src.app:create_app

# Execute o comando para aplicar as migrações
flask db upgrade
```
**Atenção:** Você precisa executar `flask db upgrade` toda vez que houver uma nova migração no código.

### 5. Rode a Aplicação
```bash
flask run
```
A API estará rodando em `http://127.0.0.1:5000`.

## Deploy no Render
O deploy é feito automaticamente via `render.yaml` quando você envia as mudanças para a branch `main` no GitHub.
