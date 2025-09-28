# Multi-stage Dockerfile for Nuxt 3 SSR
FROM node:18-alpine AS builder

# Diretório de trabalho
WORKDIR /app

# Copiar apenas arquivos de dependências primeiro
COPY package*.json ./

# Instalar dependências (garantindo que npm existe)
RUN npm install --frozen-lockfile --verbose

# Copiar código-fonte
COPY . .

# Build do Nuxt 3
RUN npm run build

# Stage 2: Runtime apenas com o necessário
FROM node:18-alpine AS production

# Instalar curl para health checks
RUN apk add --no-cache curl

# Diretório de trabalho
WORKDIR /app

# Copiar apenas o build e package.json do stage anterior
COPY --from=builder /app/.output ./output
COPY --from=builder /app/package*.json ./

# Instalar apenas dependências de produção
RUN npm ci --only=production --verbose && npm cache clean --force

# Criar usuário não-root
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nuxt -u 1001 -G nodejs

# Mudar ownership
RUN chown -R nuxt:nodejs /app

# Trocar para usuário não-root
USER nuxt

# Expor porta
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:3000/ || exit 1

# Iniciar servidor Nuxt 3 SSR
CMD ["node", "./output/server/index.mjs"]