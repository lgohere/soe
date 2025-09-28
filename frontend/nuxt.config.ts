// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  devtools: { enabled: true },
  modules: ['@nuxtjs/tailwindcss'],
  css: ['~/assets/css/main.css'],

  // Minimal reading interface configuration
  app: {
    head: {
      title: 'Simplificando O Evangelho',
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        { name: 'description', content: 'Plataforma minimalista para leitura bíblica compartilhada durante transmissões ao vivo. Interface clean e elegante para acompanhar a Palavra de Deus.' },
        { name: 'theme-color', content: '#ffffff' },
        { name: 'author', content: 'Simplificando O Evangelho' }
      ],
      link: [
        { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' },
        { rel: 'preconnect', href: 'https://fonts.googleapis.com' },
        { rel: 'preconnect', href: 'https://fonts.gstatic.com', crossorigin: '' },
        { rel: 'stylesheet', href: 'https://fonts.googleapis.com/css2?family=Inter:wght@200;300;400;500&display=swap' }
      ]
    }
  },

  // Runtime config for API
  runtimeConfig: {
    public: {
      apiBase: process.env.API_BASE || 'http://localhost:8000/api/v1'
    }
  },

  // Accessibility and performance
  experimental: {
    payloadExtraction: false
  },

  nitro: {
    preset: 'node-server'
  }
})