# Deploy no Render

## Passos para Deploy:

### 1. Prepare o Repositório
- Commit todas as mudanças no GitHub
- Certifique-se que `render.yaml` está na raiz do projeto

### 2. Configure no Render
1. Acesse [render.com](https://render.com)
2. Conecte sua conta GitHub
3. Clique em "New" → "Blueprint"
4. Selecione seu repositório
5. Render detectará automaticamente o `render.yaml`

### 3. Variáveis de Ambiente
Configure estas variáveis no dashboard do Render:
- `DATABASE_URL` - Será configurada automaticamente
- `JWT_SECRET` - Será gerada automaticamente
- `OPENAI_API_KEY` - Configure manualmente se necessário
- Outras variáveis específicas do seu projeto

### 4. Deploy
- Clique em "Apply" para iniciar o deploy
- Aguarde a construção e deploy automático
- Acesse sua aplicação pela URL fornecida

## Troubleshooting
- Verifique os logs no dashboard do Render
- Certifique-se que todas as dependências estão no package.json
- Verifique se o banco de dados está conectado corretamente
