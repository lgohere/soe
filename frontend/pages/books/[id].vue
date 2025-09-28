<template>
  <div class="space-y-16">
    <!-- Book Header -->
    <div class="text-center" v-if="book">
      <div class="mb-8">
        <NuxtLink to="/" class="nav-link text-sm">
          ← Livros
        </NuxtLink>
      </div>
      <h1 class="chapter-title">
        {{ book.name }}
      </h1>
      <p class="text-sm text-gray-500 font-light mt-4">
        {{ book.testament === 'old_testament' ? 'Antigo Testamento' : 'Novo Testamento' }}
      </p>
    </div>

    <!-- Chapters Grid -->
    <div class="chapter-nav" v-if="chapters">
      <NuxtLink
        v-for="chapter in chapters"
        :key="chapter.id"
        :to="`/chapters/${chapter.id}`"
        class="card p-4 text-center group cursor-pointer"
      >
        <div class="text-lg font-light text-gray-900 group-hover:text-gray-700 transition-colors">
          {{ chapter.chapter_number }}
        </div>
      </NuxtLink>
    </div>

    <!-- Loading State -->
    <div v-if="pending" class="text-center py-16">
      <div class="text-base text-gray-500 font-light">Carregando capítulos...</div>
    </div>

    <!-- Error State -->
    <div v-if="error" class="text-center py-16">
      <div class="text-base text-gray-600 mb-6">Erro ao carregar o livro</div>
      <button @click="refresh()" class="btn-secondary">
        Tentar novamente
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Book, Chapter } from '~/types'

// Get route params
const route = useRoute()
const bookId = Number(route.params.id)

// Page meta will be set dynamically after book loads
const { getBookChapters } = useApi()

// Fetch chapters data
const { data: chapters, pending, error, refresh } = await useLazyAsyncData(
  `book-${bookId}-chapters`,
  () => getBookChapters(bookId)
)

// Get book info from chapters data (first chapter contains book info)
const book = computed<Book | null>(() => {
  if (!chapters.value || chapters.value.length === 0) return null

  const firstChapter = chapters.value[0]
  return {
    id: bookId,
    name: firstChapter.book_name,
    testament: firstChapter.book_name.includes('Samuel') ||
               firstChapter.book_name.includes('Reis') ||
               firstChapter.book_name.includes('Crônicas') ||
               ['Gênesis', 'Êxodo', 'Levítico', 'Números', 'Deuteronômio', 'Josué', 'Juízes', 'Rute', 'Esdras', 'Neemias', 'Ester', 'Jó', 'Salmos', 'Provérbios', 'Eclesiastes', 'Cântico dos Cânticos', 'Isaías', 'Jeremias', 'Lamentações', 'Ezequiel', 'Daniel', 'Oséias', 'Joel', 'Amós', 'Obadias', 'Jonas', 'Miquéias', 'Naum', 'Habacuque', 'Sofonias', 'Ageu', 'Zacarias', 'Malaquias'].includes(firstChapter.book_name)
               ? 'old_testament' : 'new_testament',
    url: '',
    total_chapters: chapters.value.length,
    created_at: '',
    updated_at: ''
  }
})

// Set dynamic page title
watchEffect(() => {
  if (book.value) {
    useHead({
      title: `${book.value.name}`,
      meta: [
        { name: 'description', content: `Leia ${book.value.name} com ${book.value.total_chapters} capítulos` }
      ]
    })
  }
})
</script>