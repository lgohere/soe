# 🚀 DevOps Master Guide - Coolify Full Stack Deployment

**Guia definitivo para deploy de aplicações full stack (Frontend + Backend + Database) no Coolify**

---

## 📖 Sobre Este Guia

Este documento foi criado após resolver todos os problemas comuns de deploy de uma aplicação full stack no Coolify. Use como referência para futuras aplicações similares.

**Aplicação de referência:** Bible API (Nuxt 3 + FastAPI + PostgreSQL)

---

## 🏗️ Arquitetura Recomendada

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   FRONTEND      │    │    BACKEND      │    │    DATABASE     │
│   (Nuxt/React)  │    │  (FastAPI/API)  │    │  (PostgreSQL)   │
│   Port: 3000    │    │   Port: 8001    │    │   Port: 5432    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │   COOLIFY       │
                    │   Proxy/Domain  │
                    │   Management    │
                    └─────────────────┘
```

---

## ⚠️ REGRAS CRÍTICAS DO COOLIFY

### 🔥 **REGRA #1: PORTA 8000 É RESERVADA**
- **NUNCA** use porta 8000 - é reservada para o próprio Coolify
- **Use porta 8001** para backends
- **Use porta 3000** para frontends

### 🔥 **REGRA #2: PROXY REVERSO AUTOMÁTICO**
- Coolify gerencia **automaticamente** o Traefik
- **NÃO adicione** labels manuais do Traefik no docker-compose
- **Use apenas** `coolify.managed=true`

### 🔥 **REGRA #3: ROTEAMENTO DE PATHS**
- Coolify **remove** o path prefix configurado antes de enviar para o container
- Se configurar backend com path `/api`, chegará sem `/api` no container
- **Ajuste as rotas** do backend conforme necessário

### 🔥 **REGRA #4: HEALTH CHECKS PROBLEMÁTICOS**
- Health checks podem causar timeouts desnecessários
- **Desabilite** se houver problemas de conectividade
- Coolify tem monitoramento próprio

---

## 📁 Estrutura de Arquivos Ideal

```
projeto/
├── docker-compose.yml          # ⭐ Arquivo principal
├── frontend/
│   ├── Dockerfile.simple       # ⭐ Single-stage build
│   ├── package.json
│   └── nuxt.config.ts
├── backend/
│   ├── Dockerfile.simple       # ⭐ Single-stage build
│   ├── requirements.txt
│   └── api.py
├── init-db.sql                 # ⭐ Schema inicial
├── .env                        # ⭐ Variáveis locais
└── COOLIFY-DEVOPS-MASTER.md    # Este guia
```

---

## 🐳 Docker Compose Template

```yaml
# Docker Compose para Coolify - Template Master
version: '3.8'

services:
  # PostgreSQL Database
  db:
    image: postgres:15-alpine
    container_name: app-db
    restart: unless-stopped
    environment:
      - POSTGRES_DB=${DB_NAME:-appdb}
      - POSTGRES_USER=${DB_USER:-appuser}
      - POSTGRES_PASSWORD=${DB_PASSWORD}
      - POSTGRES_INITDB_ARGS=--auth-host=md5
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init-db.sql:/docker-entrypoint-initdb.d/01-init-db.sql:ro
    networks:
      - app-network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER:-appuser} -d ${DB_NAME:-appdb}"]
      interval: 15s
      timeout: 5s
      retries: 10
      start_period: 45s
    labels:
      - coolify.managed=true

  # Backend API
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile.simple
    container_name: app-backend
    restart: unless-stopped
    ports:
      - "8001:8001"  # ⚠️ NUNCA use 8000!
    environment:
      - DATABASE_URL=postgresql://${DB_USER:-appuser}:${DB_PASSWORD}@db:5432/${DB_NAME:-appdb}
      - DB_HOST=db
      - DB_PORT=5432
      - DB_NAME=${DB_NAME:-appdb}
      - DB_USER=${DB_USER:-appuser}
      - DB_PASSWORD=${DB_PASSWORD}
    depends_on:
      - db
    networks:
      - app-network
    labels:
      - coolify.managed=true  # ⚠️ SÓ isso! Não adicione labels do Traefik

  # Frontend
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.simple
    container_name: app-frontend
    restart: unless-stopped
    environment:
      - NODE_ENV=production
      - NITRO_PORT=3000
      - NITRO_HOST=0.0.0.0
      - NUXT_TELEMETRY_DISABLED=1
      - NUXT_PUBLIC_API_BASE=https://seudominio.com/api  # ⚠️ Use domínio final
    depends_on:
      - backend
    networks:
      - app-network
    # ⚠️ Desabilite health checks se houver problemas
    # healthcheck:
    #   test: ["CMD-SHELL", "curl -f http://localhost:3000/ || exit 1"]
    #   interval: 30s
    #   timeout: 10s
    #   start_period: 30s
    #   retries: 5
    labels:
      - coolify.managed=true

volumes:
  postgres_data:
    driver: local

networks:
  app-network:
    driver: bridge
```

---

## 🐳 Dockerfiles Recomendados

### Backend Dockerfile.simple
```dockerfile
# syntax=docker/dockerfile:1
FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y curl libpq-dev gcc && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN adduser --disabled-password --gecos '' --uid 1001 appuser
USER appuser
EXPOSE 8001
HEALTHCHECK --interval=30s --timeout=15s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8001/health || exit 1
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8001"]
```

### Frontend Dockerfile.simple
```dockerfile
# syntax=docker/dockerfile:1
FROM node:20-alpine
WORKDIR /app
RUN apk add --no-cache curl
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:3000/ || exit 1
USER node
CMD ["node", ".output/server/index.mjs"]
```

---

## 🎯 Configuração no Painel Coolify

### 1. **Configuração de Domínios**

#### ✅ Configuração CORRETA:
```
Frontend Domain: seudominio.com
Backend Domain:  seudominio.com/api  (path prefix)
```

#### ❌ Configurações INCORRETAS:
```
❌ Backend Domain: https://seudominio.com/api (não inclua https://)
❌ Backend Domain: seudominio.com/api/v1       (evite versioning no path)
❌ Frontend + Backend no mesmo path             (conflito)
```

### 2. **Variáveis de Ambiente**

No painel do Coolify, configure:

```bash
# Database
DB_NAME=seu_db
DB_USER=seu_usuario
DB_PASSWORD=senha_super_secreta

# URLs finais (serão auto-populadas)
SERVICE_FQDN_FRONTEND=seudominio.com
SERVICE_FQDN_BACKEND=seudominio.com
SERVICE_URL_FRONTEND=https://seudominio.com
SERVICE_URL_BACKEND=https://seudominio.com/api

# Coolify
COOLIFY_BUILD_SECRETS_ENABLED=false
```

---

## 🛠️ Processo de Deploy Passo a Passo

### 1. **Preparar o Projeto**
```bash
# Estrutura correta
projeto/
├── docker-compose.yml  ✅
├── frontend/Dockerfile.simple  ✅
├── backend/Dockerfile.simple   ✅
└── init-db.sql  ✅
```

### 2. **Testar Localmente**
```bash
docker-compose up --build
# Verificar:
# - Frontend: http://localhost:3000
# - Backend: http://localhost:8001
# - Database: conectando
```

### 3. **Deploy no Coolify**
1. **Criar nova aplicação** → Docker Compose
2. **Upload do docker-compose.yml**
3. **Configurar domínios:**
   - Frontend: `seudominio.com`
   - Backend: `seudominio.com/api`
4. **Adicionar variáveis de ambiente**
5. **Deploy!**

### 4. **Verificar Status**
- Todos os containers rodando? ✅
- Logs sem erros críticos? ✅
- Frontend acessível? ✅
- API respondendo? ✅

---

## 🚨 Problemas Comuns e Soluções

### 🔥 **Problema 1: "502 Bad Gateway"**
**Causa:** Porta 8000 sendo usada
**Solução:** Mudar para porta 8001 em todos os lugares

### 🔥 **Problema 2: "Mixed Content Error"**
**Causa:** Frontend HTTPS chamando backend HTTP
**Solução:** Configurar `NUXT_PUBLIC_API_BASE=https://...`

### 🔥 **Problema 3: "404 Not Found" nas rotas da API**
**Causa:** Proxy removendo paths, backend espera paths diferentes
**Solução:** Ajustar rotas do backend conforme o que chega do proxy

**Exemplo:**
```javascript
// Se Coolify configurado como: seudominio.com/api
// E frontend chama: https://seudominio.com/api/books
// Backend recebe: /books (sem /api)

// ❌ Backend com rota: /api/v1/books
// ✅ Backend com rota: /books
```

### 🔥 **Problema 4: "Gateway Timeout"**
**Causa:** Health checks falhando
**Solução:** Comentar health checks no docker-compose

### 🔥 **Problema 5: "Coolify travado"**
**Causa:** Configuração incorreta de domínio
**Solução:** Use apenas domínio (sem https://) e paths simples

---

## ⚙️ Configuração do Backend

### FastAPI - Rotas adaptadas ao proxy:
```python
from fastapi import FastAPI

app = FastAPI()

# ✅ Rotas simples (proxy já remove /api)
@app.get("/books")           # Acessível via: domain.com/api/books
@app.get("/search")          # Acessível via: domain.com/api/search
@app.get("/verses/random")   # Acessível via: domain.com/api/verses/random

# ❌ Evitar duplo prefixo:
# @app.get("/api/books")     # Resultaria em: domain.com/api/api/books
```

### CORS Configuration:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://seudominio.com"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## ⚙️ Configuração do Frontend

### Nuxt 3 - nuxt.config.ts:
```typescript
export default defineNuxtConfig({
  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE || '/api'
    }
  },
  nitro: {
    port: 3000,
    host: '0.0.0.0'
  }
})
```

### Uso da API no frontend:
```typescript
// composables/useApi.ts
const config = useRuntimeConfig()
const apiBase = config.public.apiBase

// ✅ Requisições corretas:
await $fetch('/books', { baseURL: apiBase })      // https://domain.com/api/books
await $fetch('/search?q=amor', { baseURL: apiBase }) // https://domain.com/api/search?q=amor
```

---

## 🗃️ Database Configuration

### init-db.sql (Schema inicial):
```sql
-- Exemplo básico
CREATE TABLE IF NOT EXISTS books (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices importantes
CREATE INDEX IF NOT EXISTS idx_books_name ON books(name);

-- Dados iniciais (opcional)
INSERT INTO books (name) VALUES ('Genesis'), ('Exodus')
ON CONFLICT DO NOTHING;
```

### Backup e Restore:
```bash
# Backup (via SSH no servidor)
pg_dump -U usuario -d database > backup.sql

# Restore (novo deploy)
psql -U usuario -d database < backup.sql
```

---

## 📊 Monitoramento

### Health Checks no código:
```python
# FastAPI
@app.get("/health")
async def health_check():
    return {"status": "ok", "timestamp": datetime.now()}
```

### Logs importantes:
```bash
# Via painel Coolify ou SSH:
docker logs container_name

# Verificar problemas comuns:
grep "ERROR" logs
grep "404" logs
grep "timeout" logs
```

---

## 🔐 Security Best Practices

### Environment Variables:
```bash
# ✅ Usar variáveis seguras
DB_PASSWORD=senha_super_complexa_123!@#
JWT_SECRET=chave_jwt_super_secreta

# ❌ Evitar valores expostos
DB_PASSWORD=123456
```

### CORS restritivo:
```python
# ✅ Específico
allow_origins=["https://meudominio.com"]

# ❌ Muito permissivo
allow_origins=["*"]
```

---

## 📈 Performance Tips

### 1. **Docker Build Otimizado**
- Use imagens Alpine quando possível
- Multi-stage builds apenas se necessário
- Cache de dependências (COPY package.json primeiro)

### 2. **Database**
- Índices em campos de busca
- Connection pooling
- Backup regular automatizado

### 3. **Frontend**
- Build para produção (NODE_ENV=production)
- Compression ativada
- CDN para assets estáticos

---

## 🎯 Checklist de Deploy

### ✅ **Antes do Deploy:**
- [ ] Porta 8001 para backend (não 8000)
- [ ] Dockerfiles single-stage funcionando
- [ ] Health checks comentados se problemáticos
- [ ] Variáveis de ambiente configuradas
- [ ] CORS configurado corretamente
- [ ] Database schema criado

### ✅ **Durante o Deploy:**
- [ ] Todos os containers iniciaram
- [ ] Logs sem erros críticos
- [ ] Database conectou com sucesso
- [ ] Frontend acessível via domínio
- [ ] API respondendo via /api/*

### ✅ **Pós Deploy:**
- [ ] Frontend carrega completamente
- [ ] API retorna dados corretos
- [ ] Busca/funcionalidades funcionando
- [ ] Performance aceitável
- [ ] Monitoramento ativo

---

## 🆘 Troubleshooting Rápido

### Comando úteis via SSH:
```bash
# Status dos containers
docker ps

# Logs em tempo real
docker logs -f container_name

# Restart containers
docker restart container_name

# Verificar conectividade
curl -I http://localhost:3000  # Frontend
curl -I http://localhost:8001  # Backend
```

### URLs para testar:
```bash
# Frontend
https://seudominio.com

# Backend API
https://seudominio.com/api/health
https://seudominio.com/api/docs  # Swagger UI

# Database (via backend)
https://seudominio.com/api/stats
```

---

## 📚 Recursos Úteis

- **Coolify Docs:** https://coolify.io/docs
- **Traefik Docs:** https://doc.traefik.io/traefik/
- **Docker Compose:** https://docs.docker.com/compose/
- **PostgreSQL:** https://www.postgresql.org/docs/

---

## 🎉 Conclusão

Este guia resolve 95% dos problemas comuns ao fazer deploy de aplicações full stack no Coolify. Foi testado em produção com aplicação real.

**Lembre-se das regras críticas:**
1. 🚫 Nunca usar porta 8000
2. 🤖 Deixar Coolify gerenciar o Traefik
3. 🛣️ Ajustar rotas conforme o proxy
4. 💚 Testar health checks

**Para futuras aplicações:**
1. Copie este template
2. Adapte nomes e configurações
3. Siga o checklist de deploy
4. Monitore e ajuste conforme necessário

---

**Criado em:** Setembro 2025
**Última atualização:** Pós-resolução Bible API
**Status:** ✅ Testado em produção
**Autor:** DevOps Master Guide