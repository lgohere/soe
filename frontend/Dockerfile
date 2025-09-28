FROM node:20-alpine AS runner
WORKDIR /app

ENV NODE_ENV=production
ENV PORT=3000
ENV HOST=0.0.0.0
ENV NITRO_PORT=3000
ENV NITRO_HOST=0.0.0.0
ENV NUXT_TELEMETRY_DISABLED=1

COPY --from=builder /app/.output /app/.output

USER node
EXPOSE 3000

CMD ["node", ".output/server/index.mjs"]