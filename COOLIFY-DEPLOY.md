# 🚀 Manual DevOps Sênior - Deploy Coolify VPS Debian

## 📋 **CHECKLIST PRÉ-DEPLOY**

### ✅ **Arquivos Essenciais Verificados:**
- [x] `docker-compose.yml` - Configurado para Coolify
- [x] `init-db.sql` - Script de inicialização automática
- [x] `manual_backup.sql` - Dados completos (5.8MB)
- [x] `frontend/Dockerfile` - Otimizado com health checks
- [x] `backend/Dockerfile` - Configurado com libpq-dev
- [x] `.coolifyignore` - Ignorar arquivos desnecessários

---

## 🔧 **CONFIGURAÇÃO COOLIFY - PASSO A PASSO**

### **1. CRIAR PROJETO NO COOLIFY**

```bash
# Acesse: https://[IP_VPS]:8000
# Login no painel Coolify
```

**Configurações do Projeto:**
- **Nome**: `biblia-soe`
- **Tipo**: `Docker Compose`
- **Repository**: Seu repositório Git privado
- **Branch**: `master`
- **Docker Compose Path**: `docker-compose.yml`

---

### **2. VARIÁVEIS DE AMBIENTE - CRÍTICAS**

**⚠️ Configure EXATAMENTE estas variáveis:**

```bash
# Database Configuration (OBRIGATÓRIAS)
DB_NAME=bibliasoe
DB_USER=soe
DB_PASSWORD=SuaSenhaForteAqui123!

# Domain Configuration
DOMAIN=soe.texts.com.br

# Network Configuration (IMPORTANTE)
NUXT_PUBLIC_API_BASE=http://backend:8000/api/v1
```

**🚨 ATENÇÃO:**
- Use senha forte no `DB_PASSWORD`
- `NUXT_PUBLIC_API_BASE` deve usar nome interno `backend`
- NÃO use URLs externas na comunicação interna

---

### **3. CONFIGURAÇÃO DE DOMÍNIO**

**DNS Records necessários:**
```
Type: A
Name: soe
Value: [IP_DA_VPS]
TTL: 300
```

**No Coolify:**
- Vá em **Domains** → **Add Domain**
- Domain: `soe.texts.com.br`
- ✅ **HTTPS Enabled** (SSL automático)
- ✅ **Redirect to HTTPS**

---

### **4. CONFIGURAÇÕES AVANÇADAS**

#### **Build Settings:**
- **Build Pack**: `Docker Compose`
- **Port**: `3000` (frontend será exposto)
- **Restart Policy**: `unless-stopped`

#### **Resource Limits (Recomendado):**
```yaml
# Para VPS com 2GB RAM:
frontend:
  memory: 512M
  cpu: 0.5

backend:
  memory: 256M
  cpu: 0.3

db:
  memory: 512M
  cpu: 0.2
```

---

## 🗃️ **INICIALIZAÇÃO AUTOMÁTICA DO BANCO**

### **Como Funciona:**

1. **Primeiro Deploy**: PostgreSQL inicia vazio
2. **Scripts Automáticos**:
   - `init-db.sql` → Cria tabelas e estrutura
   - `manual_backup.sql` → Importa todos os versículos
3. **Resultado**: Banco populado automaticamente

### **Verificação dos Dados:**
```sql
-- Conectar no container DB e verificar
SELECT COUNT(*) FROM verses;
-- Esperado: 31,106 versículos
```

---

## 🚀 **PROCESSO DE DEPLOY**

### **Deploy Inicial:**
1. **Configure** todas as variáveis de ambiente
2. **Adicione** o domínio `soe.texts.com.br`
3. **Click Deploy** → Aguarde 5-10 minutos
4. **Monitore** logs de cada container
5. **Verifique** health checks (todos devem ficar GREEN)

### **Monitoramento:**
```bash
# Via Coolify Dashboard:
- Frontend: Status "healthy"
- Backend: Status "healthy"
- Database: Status "healthy"

# URLs para testar:
✅ https://soe.texts.com.br → Frontend
✅ https://soe.texts.com.br/api/health → Backend
✅ https://soe.texts.com.br/api/docs → Swagger
```

---

## 🔍 **TROUBLESHOOTING - PROBLEMAS COMUNS**

### **❌ Container Frontend crashando:**
```bash
# Verificar logs
docker logs biblia-frontend --tail 50

# Problemas comuns:
1. NUXT_PUBLIC_API_BASE incorreto
2. Node.js out of memory
3. Build assets corrompidos

# Solução:
1. Verificar variáveis de ambiente
2. Rebuild do zero
3. Limpar cache Docker
```

### **❌ Backend não conecta no banco:**
```bash
# Verificar conectividade
docker exec biblia-backend python -c "
import psycopg2
conn = psycopg2.connect('postgresql://soe:PASSWORD@db:5432/bibliasoe')
print('✅ Conexão OK')
"

# Problemas comuns:
1. Senha DB_PASSWORD incorreta
2. Nome do banco errado
3. Network não funcionando

# Solução:
1. Verificar todas variáveis DB_*
2. Restart dos containers
3. Verificar logs PostgreSQL
```

### **❌ Banco vazio após deploy:**
```bash
# Verificar se scripts rodaram
docker exec biblia-db ls -la /docker-entrypoint-initdb.d/

# Deve mostrar:
# init-db.sql
# restore.sql (manual_backup.sql)

# Se vazio, re-deploy necessário
```

### **❌ SSL não funcionando:**
```bash
# Verificar DNS
nslookup soe.texts.com.br

# Verificar se Coolify consegue gerar certificado
# Logs: Settings → SSL → View Logs

# Problemas comuns:
1. DNS não propagado (aguarde 24h)
2. Firewall bloqueando porta 80/443
3. Rate limit Let's Encrypt
```

---

## ⚡ **OTIMIZAÇÕES VPS DEBIAN**

### **Configurações do Sistema:**
```bash
# Aumentar limites de arquivo (se necessário)
echo "fs.file-max = 100000" >> /etc/sysctl.conf

# Configurar swap (se <4GB RAM)
fallocate -l 2G /swapfile
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile
echo "/swapfile none swap sw 0 0" >> /etc/fstab

# Limpar logs antigos automaticamente
echo "0 2 * * * root find /var/log -name '*.log' -type f -mtime +7 -delete" >> /etc/crontab
```

### **Docker Optimizations:**
```bash
# Configurar logging driver
echo '{"log-driver": "json-file", "log-opts": {"max-size": "10m", "max-file": "3"}}' > /etc/docker/daemon.json
systemctl restart docker

# Limpar recursos não utilizados semanalmente
echo "0 3 * * 0 root docker system prune -f" >> /etc/crontab
```

---

## 📊 **MONITORAMENTO E MANUTENÇÃO**

### **Health Checks Automáticos:**
```bash
# Script para verificar saúde da aplicação
#!/bin/bash
echo "🔍 Verificando saúde da aplicação..."

# Frontend
if curl -f -s https://soe.texts.com.br > /dev/null; then
  echo "✅ Frontend: OK"
else
  echo "❌ Frontend: ERRO"
fi

# Backend
if curl -f -s https://soe.texts.com.br/api/health > /dev/null; then
  echo "✅ Backend: OK"
else
  echo "❌ Backend: ERRO"
fi

# Database
if docker exec biblia-db pg_isready -U soe -d bibliasoe; then
  echo "✅ Database: OK"
else
  echo "❌ Database: ERRO"
fi
```

### **Backup Automático:**
```bash
# Backup diário do banco (adicionar ao cron)
#!/bin/bash
BACKUP_DIR="/opt/backups/biblia"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR
docker exec biblia-db pg_dump -U soe bibliasoe > $BACKUP_DIR/backup_$DATE.sql

# Manter apenas 7 dias de backup
find $BACKUP_DIR -name "backup_*.sql" -mtime +7 -delete

echo "✅ Backup realizado: backup_$DATE.sql"
```

---

## 🎯 **CHECKLIST FINAL DE VALIDAÇÃO**

### **✅ Deploy Successful Checklist:**

1. **Containers Health:**
   - [ ] Frontend: Status "healthy" no Coolify
   - [ ] Backend: Status "healthy" no Coolify
   - [ ] Database: Status "healthy" no Coolify

2. **URLs Funcionais:**
   - [ ] `https://soe.texts.com.br` → Carrega interface
   - [ ] `https://soe.texts.com.br/api/health` → Retorna JSON
   - [ ] `https://soe.texts.com.br/api/docs` → Swagger UI

3. **Dados Corretos:**
   - [ ] Banco populado com 31,106 versículos
   - [ ] API retorna livros/capítulos/versículos
   - [ ] Frontend consegue buscar dados

4. **SSL/HTTPS:**
   - [ ] Certificado SSL válido e automático
   - [ ] Redirect HTTP → HTTPS funcionando
   - [ ] Sem warnings de segurança

### **🚨 Se ALGUM item falhar:**
1. Verificar logs específicos no Coolify
2. Consultar seção Troubleshooting acima
3. Re-deploy se necessário
4. Aguardar propagação DNS (até 24h)

---

## 📝 **COMANDOS ÚTEIS - COLA DE EMERGÊNCIA**

```bash
# Ver todos containers
docker ps -a

# Logs em tempo real
docker logs -f biblia-frontend
docker logs -f biblia-backend
docker logs -f biblia-db

# Restart específico
docker-compose restart frontend
docker-compose restart backend

# Conectar no banco
docker exec -it biblia-db psql -U soe -d bibliasoe

# Verificar dados
docker exec biblia-db psql -U soe -d bibliasoe -c "SELECT COUNT(*) FROM verses;"

# Re-deploy forçado (no Coolify)
# Projects → biblia-soe → Deployments → Deploy Latest

# Limpar cache Docker (emergência)
docker system prune -a -f
```

---

## 🎉 **RESULTADO FINAL ESPERADO**

**✅ Aplicação Funcionando:**
- **Frontend**: Interface minimalista carregando em https://soe.texts.com.br
- **Backend**: API respondendo em https://soe.texts.com.br/api
- **Database**: 31,106 versículos acessíveis via API
- **Performance**: Carregamento < 2 segundos
- **SSL**: Certificado automático válido
- **Monitoramento**: Health checks verdes

**🎯 Esta configuração resolve:**
1. ✅ Problema de backup manual do banco (automático)
2. ✅ Configurações de rede inconsistentes (fixado)
3. ✅ Health checks falhando (otimizado)
4. ✅ Variables de ambiente conflitantes (padronizado)
5. ✅ Deploy manual complexo (automatizado)
6. ✅ SSL/DNS issues (configuração correta)
7. ✅ Otimizações específicas para VPS Debian

---

## 💡 **TEMPLATE PARA FUTURAS APLICAÇÕES**

Este guia serve como **template base** para todas as aplicações futuras que precisem de:

- ✅ **Frontend**: Nuxt/Vue.js/React
- ✅ **Backend**: FastAPI/Express/Laravel
- ✅ **Database**: PostgreSQL/MySQL
- ✅ **Deploy**: Coolify em VPS Debian
- ✅ **SSL**: Certificados automáticos
- ✅ **Monitoramento**: Health checks

**🔄 Para reaproveitar:**
1. Copie estrutura de Dockerfiles
2. Adapte docker-compose.yml
3. Configure variáveis de ambiente
4. Execute checklist de validação
5. Implemente monitoramento

---

**📞 SUPORTE TÉCNICO:**
- Logs sempre no Coolify Dashboard
- Troubleshooting sections específicas acima
- Commands úteis na cola de emergência
- Health checks automáticos implementados

**🎯 DEPLOY STATUS: PRODUCTION READY** 🚀