// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  devtools: { enabled: true },
  modules: ['@nuxtjs/tailwindcss'],
  css: ['~/assets/css/main.css'],

  // Minimal reading interface configuration
  app: {
    head: {
      title: 'Simplificando O Evangelho - Bíblia Online',
      titleTemplate: '%s - Simplificando O Evangelho',
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1, maximum-scale=5, user-scalable=yes' },
        { name: 'format-detection', content: 'telephone=no' },
        { name: 'description', content: 'Plataforma minimalista para leitura bíblica compartilhada durante transmissões ao vivo. Interface clean e elegante para acompanhar a Palavra de Deus.' },
        { name: 'theme-color', content: '#304E69' },
        { name: 'author', content: 'Simplificando O Evangelho' },
        { name: 'keywords', content: 'bíblia, evangelho, transmissão, ao vivo, palavra de deus, leitura bíblica, acf, almeida corrigida fiel' },

        // Open Graph / Facebook
        { property: 'og:type', content: 'website' },
        { property: 'og:site_name', content: 'Simplificando O Evangelho' },
        { property: 'og:title', content: 'Simplificando O Evangelho - Bíblia Online' },
        { property: 'og:description', content: 'Plataforma minimalista para leitura bíblica durante transmissões ao vivo. Acompanhe a Palavra de Deus com interface clean e elegante.' },
        { property: 'og:image', content: 'https://soe.texts.com.br/whatsapp-image.png' },
        { property: 'og:image:alt', content: 'Simplificando O Evangelho - Bíblia Online' },
        { property: 'og:image:width', content: '1200' },
        { property: 'og:image:height', content: '630' },
        { property: 'og:url', content: 'https://soe.texts.com.br' },
        { property: 'og:locale', content: 'pt_BR' },

        // Twitter Card
        { name: 'twitter:card', content: 'summary_large_image' },
        { name: 'twitter:site', content: '@simplificandoevangelho' },
        { name: 'twitter:title', content: 'Simplificando O Evangelho - Bíblia Online' },
        { name: 'twitter:description', content: 'Plataforma minimalista para leitura bíblica durante transmissões ao vivo. Acompanhe a Palavra de Deus com interface clean e elegante.' },
        { name: 'twitter:image', content: 'https://soe.texts.com.br/whatsapp-image.png' },

        // WhatsApp específico
        { property: 'og:image:type', content: 'image/png' },
        { name: 'mobile-web-app-capable', content: 'yes' },
        { name: 'apple-mobile-web-app-capable', content: 'yes' },
        { name: 'apple-mobile-web-app-status-bar-style', content: 'default' },
        { name: 'apple-mobile-web-app-title', content: 'Simplificando O Evangelho' },

        // SEO adicional
        { name: 'robots', content: 'index, follow' },
        { name: 'googlebot', content: 'index, follow' },
        { name: 'language', content: 'pt-BR' }
      ],
      link: [
        { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' },
        { rel: 'apple-touch-icon', sizes: '180x180', href: '/apple-touch-icon.png' },
        { rel: 'icon', type: 'image/png', sizes: '32x32', href: '/favicon-32x32.png' },
        { rel: 'icon', type: 'image/png', sizes: '16x16', href: '/favicon-16x16.png' },
        { rel: 'manifest', href: '/site.webmanifest' },
        { rel: 'canonical', href: 'https://soe.texts.com.br' },
        { rel: 'preconnect', href: 'https://fonts.googleapis.com' },
        { rel: 'preconnect', href: 'https://fonts.gstatic.com', crossorigin: '' },
        { rel: 'stylesheet', href: 'https://fonts.googleapis.com/css2?family=Inter:wght@200;300;400;500&display=swap' }
      ]
    }
  },

  // Runtime config for API
  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE || process.env.API_BASE || 'http://localhost:8001/api/v1'
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