# Stage 1: Build
FROM node:18-alpine AS builder

# Instalar dependências de build para pacotes nativos
RUN apk add --no-cache python3 make g++ libc6-compat

WORKDIR /app

# Copiar apenas arquivos de dependências primeiro
COPY package*.json ./

# Instalar dependências com fallback inteligente
RUN npm ci --verbose || npm install --verbose

# Copiar código-fonte
COPY . .

# Configurar Nitro para servidor Node.js
ENV NITRO_PRESET=node
ENV NUXT_TELEMETRY_DISABLED=1

# Build do Nuxt 3
RUN npm run build

# Stage 2: Runtime
FROM node:18-alpine AS runner

WORKDIR /app

# Variáveis de ambiente para produção
ENV NODE_ENV=production
ENV NITRO_PORT=3000
ENV NITRO_HOST=0.0.0.0
ENV NUXT_TELEMETRY_DISABLED=1

# Instalar curl para healthcheck
RUN apk add --no-cache curl

# Criar usuário não-root para segurança
RUN addgroup -g 1001 nodejs && \
    adduser -D -s /bin/sh -u 1001 -G nodejs node

# Copiar apenas a saída do build SSR
COPY --from=builder /app/.output /app/.output

# Mudar para usuário não-root
USER node

# Expor porta
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:3000/ || exit 1

# Iniciar servidor Nuxt 3 SSR
CMD ["node", ".output/server/index.mjs"]