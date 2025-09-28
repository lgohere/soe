# ---------- Stage 1: Build (com devDependencies) ----------
FROM node:20-alpine AS builder

# Dependências de build para eventuais pacotes nativos
RUN apk add --no-cache python3 make g++ libc6-compat

WORKDIR /app

# Copia manifestos primeiro (melhor cache)
COPY package*.json ./

# Instalação COM devDependencies (não defina NODE_ENV=production aqui)
# Se o lockfile estiver ok, ci; senão, fallback p/ install
RUN npm ci --include=dev --verbose || npm install --include=dev --verbose

# Copia o restante do código
COPY . .

# Configura SSR como servidor Node
ENV NITRO_PRESET=node
ENV NUXT_TELEMETRY_DISABLED=1

# Compila o Nuxt (gera .output)
RUN npm run build

# ---------- Stage 2: Runtime (somente servidor Nitro) ----------
FROM node:20-alpine AS runner
WORKDIR /app

# Aqui sim é produção
ENV NODE_ENV=production
ENV PORT=3000
ENV HOST=0.0.0.0
ENV NITRO_PORT=3000
ENV NITRO_HOST=0.0.0.0
ENV NUXT_TELEMETRY_DISABLED=1

# Usuário não-root
RUN addgroup -S nodejs && adduser -S node -G nodejs

# Copia APENAS a saída do build
COPY --from=builder /app/.output /app/.output

USER node
EXPOSE 3000

# Sobe o servidor SSR do Nitro
CMD ["node", ".output/server/index.mjs"]