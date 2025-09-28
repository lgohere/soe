# 🚀 Deploy no Coolify - Guia Completo

## 📋 Pré-requisitos

1. **Servidor VPS** com Coolify instalado
2. **Domínio** `texts.com.br` apontando para o IP da VPS
3. **Git repository** do projeto
4. **Backup** do banco de dados local

## 🗃️ 1. Backup do Banco Local

Antes de fazer o deploy, execute o backup:

```bash
# Execute no diretório do projeto
./backup_database.sh
```

Isso criará um arquivo em `./database_backups/biblia_backup_YYYYMMDD_HHMMSS.sql`

## 🌐 2. Configuração do Domínio

### DNS Configuration
Configure os seguintes registros DNS para `texts.com.br`:

```
Type: A
Name: soe
Value: [IP_DA_VPS]
TTL: 300
```

Resultado: `soe.texts.com.br` → IP da VPS

## 🔧 3. Deploy no Coolify

### 3.1 Criar Novo Projeto
1. Acesse o painel do Coolify
2. Clique em **"New Project"**
3. Nome: `biblia-soe`

### 3.2 Adicionar Aplicação
1. Dentro do projeto, clique **"New Resource"**
2. Selecione **"Docker Compose"**
3. Configurações:
   - **Name**: `biblia-app`
   - **Repository**: URL do seu repositório Git
   - **Branch**: `main` ou `master`
   - **Base Directory**: `/` (raiz)
   - **Compose File**: `docker-compose.yml`

### 3.3 Configurar Variáveis de Ambiente
Na aba **Environment Variables**, adicione:

```bash
# Domínio principal
DOMAIN=soe.texts.com.br

# Banco de dados - IMPORTANTE: Use uma senha forte!
DB_NAME=bibliasoe
DB_USER=soe
DB_PASSWORD=sua_senha_super_segura_aqui

# API Configuration
NUXT_PUBLIC_API_BASE=https://soe.texts.com.br/api
```

### 3.4 Configurar Domínios
Na aba **Domains**, adicione:
- **Domain**: `soe.texts.com.br`
- **HTTPS**: ✅ Enabled (SSL automático)

## 📊 4. Restaurar Dados do Banco

### 4.1 Aguardar Deploy
1. Clique em **"Deploy"**
2. Aguarde todos os containers subirem (pode levar 5-10 minutos)
3. Verifique se todos os services estão **healthy**

### 4.2 Transferir Backup para VPS
```bash
# Copie o arquivo de backup para a VPS
scp ./database_backups/biblia_backup_*.sql root@[IP_VPS]:/tmp/

# Ou use rsync
rsync -avz ./database_backups/ root@[IP_VPS]:/tmp/backups/
```

### 4.3 Restaurar no Container
```bash
# SSH na VPS
ssh root@[IP_VPS]

# Verificar containers rodando
docker ps | grep biblia

# Copiar backup para o container PostgreSQL
docker cp /tmp/biblia_backup_*.sql biblia-db:/tmp/

# Restaurar dados
docker exec -i biblia-db psql -U soe -d bibliasoe -f /tmp/biblia_backup_*.sql

# Verificar se dados foram restaurados
docker exec -i biblia-db psql -U soe -d bibliasoe -c "SELECT COUNT(*) FROM verses;"
```

## ✅ 5. Verificação do Deploy

### 5.1 Testes de Conectividade
```bash
# Testar frontend
curl -I https://soe.texts.com.br
# Esperado: HTTP/2 200

# Testar API
curl -I https://soe.texts.com.br/api/health
# Esperado: HTTP/2 200

# Testar endpoint específico
curl https://soe.texts.com.br/api/v1/books | jq '.[:2]'
# Esperado: JSON com primeiros 2 livros
```

### 5.2 Verificar Logs
No Coolify:
1. Acesse **Deployments** → **Latest Deployment**
2. Verifique logs de cada serviço:
   - `frontend`: deve mostrar Nuxt started
   - `backend`: deve mostrar FastAPI serving
   - `db`: deve mostrar PostgreSQL ready

### 5.3 Health Checks
```bash
# Verificar health dos containers
docker ps --format "table {{.Names}}\t{{.Status}}"

# Output esperado:
# biblia-frontend    Up (healthy)
# biblia-backend     Up (healthy)
# biblia-db          Up (healthy)
```

## 🔧 6. Troubleshooting

### Problema: Container não sobe
```bash
# Ver logs detalhados
docker logs biblia-frontend --tail 50
docker logs biblia-backend --tail 50
docker logs biblia-db --tail 50
```

### Problema: API não responde
```bash
# Verificar se backend consegue conectar no DB
docker exec biblia-backend curl -f http://localhost:8000/health

# Verificar conectividade do banco
docker exec biblia-db pg_isready -U soe -d bibliasoe
```

### Problema: Frontend não carrega
```bash
# Verificar se frontend consegue acessar backend
docker exec biblia-frontend curl -f http://backend:8000/health

# Verificar variável de ambiente da API
docker exec biblia-frontend env | grep NUXT_PUBLIC_API_BASE
```

## 📈 7. Monitoramento

### Logs em Tempo Real
```bash
# Acompanhar todos os logs
docker-compose logs -f

# Log específico
docker logs -f biblia-backend
```

### Performance
- **Frontend**: https://soe.texts.com.br (deve carregar < 2s)
- **API Health**: https://soe.texts.com.br/api/health (deve responder < 500ms)
- **API Stats**: https://soe.texts.com.br/api/v1/stats

## 🎯 8. URLs Finais

✅ **Site Principal**: https://soe.texts.com.br
✅ **API**: https://soe.texts.com.br/api
✅ **Documentação**: https://soe.texts.com.br/api/docs
✅ **Health Check**: https://soe.texts.com.br/api/health

---

## 💡 Comandos Úteis

```bash
# Restart específico
docker-compose restart frontend
docker-compose restart backend

# Ver uso de recursos
docker stats

# Backup automático (agendar via cron)
docker exec biblia-db pg_dump -U soe bibliasoe > backup_$(date +%Y%m%d).sql

# Update da aplicação (re-deploy)
# No Coolify: Project → Deployments → Deploy Latest
```

## 🆘 Suporte

Em caso de problemas:
1. Verificar logs no Coolify
2. Verificar health checks dos containers
3. Verificar conectividade DNS
4. Verificar SSL certificate

**Deploy concluído com sucesso!** 🎉