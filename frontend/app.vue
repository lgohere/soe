<template>
  <div class="min-h-screen bg-white">
    <!-- Minimal Header -->
    <header class="border-b border-gray-100 bg-white sticky top-0 z-50">
      <div class="max-w-4xl mx-auto px-4 sm:px-6">
        <div class="flex justify-between items-center py-4 sm:py-6">
          <div class="flex items-center">
            <NuxtLink to="/" class="flex items-center hover:opacity-80 transition-opacity">
              <img
                src="/images/soe-icon.png"
                alt="Simplificando O Evangelho"
                class="w-auto h-8 sm:h-12 md:h-14"
              />
            </NuxtLink>
          </div>
          <nav class="flex items-center justify-center space-x-4 sm:space-x-8">
            <NuxtLink
              to="/search"
              class="transition-colors flex items-center p-2"
              :class="$route.path.startsWith('/search') ? 'text-brand-primary' : 'text-gray-600 hover:text-brand-primary'"
              title="Buscar na Bíblia"
            >
              <!-- Ícone de lupa com livro -->
              <svg class="w-6 h-6 sm:w-7 sm:h-7" fill="currentColor" viewBox="0 0 24 24">
                <path d="M15.5 14h-.79l-.28-.27A6.471 6.471 0 0 0 16 9.5 6.5 6.5 0 1 0 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/>
                <path d="M7 9h5v1H7zm0-2h5v1H7z" opacity="0.6"/>
              </svg>
            </NuxtLink>
            <div class="flex items-center">
              <img
                src="/images/orbe-icon.png"
                alt="Orbe"
                class="w-auto h-12 sm:h-16 md:h-20"
              />
            </div>
          </nav>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="max-w-4xl mx-auto px-4 sm:px-6 py-8 sm:py-12">
      <NuxtPage />
    </main>
  </div>
</template>

<style>
/* Global accessibility improvements */
* {
  scroll-behavior: smooth;
}

/* Focus indicators for keyboard navigation */
button:focus,
a:focus,
input:focus {
  outline: 3px solid #3b82f6;
  outline-offset: 2px;
}

/* High contrast text */
body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* Custom brand color */
.text-brand-primary {
  color: #304E69 !important;
}

.hover\:text-brand-primary:hover {
  color: #304E69 !important;
}
</style>