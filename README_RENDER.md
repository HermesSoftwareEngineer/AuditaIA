# Deploy no Render - AuditaIA

## Pré-requisitos
1. Conta no [Render](https://render.com)
2. Repositório no GitHub com o código
3. Arquivos `build.sh` e `start.sh` com permissão de execução

## Passos para Deploy

### 1. Preparar o Repositório
```bash
# Dar permissão de execução aos scripts
chmod +x build.sh start.sh

# Commit e push para GitHub
git add .
git commit -m "Configuração para deploy no Render"
git push origin main
```

### 2. Criar Banco de Dados PostgreSQL
1. No dashboard do Render, clique em "New +"
2. Selecione "PostgreSQL"
3. Configure:
   - Name: `auditaia-db`
   - Database: `auditaia`
   - User: `auditaia`
   - Region: `Oregon (US West)`
   - Plan: `Free`

### 3. Criar Web Service
1. No dashboard do Render, clique em "New +"
2. Selecione "Web Service"
3. Conecte seu repositório GitHub
4. Configure:
   - Name: `auditaia-api`
   - Environment: `Python 3`
   - Region: `Oregon (US West)`
   - Branch: `main`
   - Build Command: `./build.sh`
   - Start Command: `./start.sh`
   - Plan: `Free`

### 4. Configurar Variáveis de Ambiente
No Web Service, adicione as seguintes variáveis:

**Obrigatórias:**
- `FLASK_ENV` = `production`
- `DATABASE_URL` = [URL do PostgreSQL criado no passo 2]
- `SECRET_KEY` = [Gerar chave aleatória]
- `JWT_SECRET_KEY` = [Gerar chave aleatória]

**Opcionais:**
- `CORS_ORIGINS` = `*` (ou domínios específicos)
- `ADMIN_EMAIL` = `admin@auditaia.com`
- `ADMIN_PASSWORD` = [Senha segura para admin]

### 5. Deploy
1. Clique em "Create Web Service"
2. O Render executará automaticamente o build e deploy
3. Acompanhe os logs para verificar se tudo ocorreu bem

### 6. Acessar a Aplicação
- URL será fornecida pelo Render (formato: `https://auditaia-api.onrender.com`)
- Health check: `GET /health`
- Login: `POST /v1/auth/login`

## Credenciais Iniciais
- Usuário: `admin`
- Email: Valor de `ADMIN_EMAIL` ou `admin@auditaia.com`
- Senha: Valor de `ADMIN_PASSWORD` ou `admin123`

## Troubleshooting

### Erro de Build
- Verifique se `build.sh` tem permissão de execução
- Confirme se `requirements.txt` está correto

### Erro de Database
- Verifique se `DATABASE_URL` está correta
- Confirme se o serviço PostgreSQL está rodando

### Logs
- Acesse logs no dashboard do Render
- Use `render logs` CLI para logs em tempo real
