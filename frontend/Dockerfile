FROM node:20-alpine AS builder

# Dependências de build para eventuais pacotes nativos
RUN apk add --no-cache python3 make g++ libc6-compat

WORKDIR /app

# Copia manifestos primeiro (melhor cache)
COPY package*.json ./

# Instalação COM devDependencies
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

ENV NODE_ENV=production
ENV PORT=3000
ENV HOST=0.0.0.0
ENV NITRO_PORT=3000
ENV NITRO_HOST=0.0.0.0
ENV NUXT_TELEMETRY_DISABLED=1

# Copia apenas a saída do build do stage builder
COPY --from=builder /app/.output /app/.output

# Usa o usuário padrão já existente da imagem Node
USER node

EXPOSE 3000

CMD ["node", ".output/server/index.mjs"]