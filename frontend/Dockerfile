FROM node:20-alpine

# Install dependencies including curl for health checks
RUN apk add --no-cache python3 make g++ libc6-compat curl

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install all dependencies
RUN npm ci --include=dev || npm install --include=dev

# Copy source code
COPY . .

# Set environment variables
ENV NODE_ENV=production
ENV NITRO_PRESET=node-server
ENV NUXT_TELEMETRY_DISABLED=1
ENV PORT=3000
ENV HOST=0.0.0.0
ENV NITRO_PORT=3000
ENV NITRO_HOST=0.0.0.0

# Build the application
RUN npm run build

# Create non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nuxt -u 1001 -G nodejs && \
    chown -R nuxt:nodejs /app

USER nuxt

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:3000/ || exit 1

CMD ["node", ".output/server/index.mjs"]