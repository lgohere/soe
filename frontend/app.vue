<template>
  <div class="min-h-screen bg-white">
    <!-- Minimal Header -->
    <header class="border-b border-gray-100 bg-white sticky top-0 z-50">
      <div class="max-w-4xl mx-auto px-6">
        <div class="flex justify-between items-center py-6">
          <div class="flex items-center">
            <NuxtLink to="/" class="flex items-center hover:opacity-80 transition-opacity">
              <img
                src="/images/soe-icon.png"
                alt="Simplificando O Evangelho"
                class="w-auto"
                style=" height: 3.7rem; "
              />
            </NuxtLink>
          </div>
          <nav class="flex items-center justify-center space-x-8" style="font-family: cursive;">
            <NuxtLink
              to="/search"
              class="text-lg transition-colors font-light flex items-center"
              :class="$route.path.startsWith('/search') ? 'text-brand-primary' : 'text-gray-600 hover:text-brand-primary'"
            >
              Buscar
            </NuxtLink>
            <div class="flex items-center">
              <img
                src="/images/orbe-icon.png"
                alt="Orbe"
                class="w-auto" style="height: 5rem;"
              />
            </div>
          </nav>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="max-w-4xl mx-auto px-6 py-12">
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