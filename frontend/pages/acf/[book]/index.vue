<template>
  <div class="space-y-8 sm:space-y-16">
    <!-- Book Header -->
    <div class="text-center" v-if="book">
      <div class="mb-6 sm:mb-8">
        <NuxtLink to="/" class="nav-link text-xs sm:text-sm touch-target">
          ← Livros
        </NuxtLink>
      </div>
      <h1 class="text-xl sm:text-2xl md:text-3xl font-normal text-gray-900 tracking-wide">
        {{ book.name }}
      </h1>
      <p class="text-xs sm:text-sm text-gray-500 font-light mt-2 sm:mt-4">
        {{ book.testament === 'old_testament' ? 'Antigo Testamento' : 'Novo Testamento' }}
      </p>
    </div>

    <!-- Chapters Grid -->
    <div class="chapter-nav" v-if="chapters">
      <NuxtLink
        v-for="chapter in chapters"
        :key="chapter.id"
        :to="`/acf/${bookSlug}/${chapter.chapter_number}`"
        class="card p-3 sm:p-4 text-center group cursor-pointer hover:shadow-sm transition-all touch-target"
      >
        <div class="text-base sm:text-lg font-normal text-gray-900 group-hover:text-gray-700 transition-colors">
          {{ chapter.chapter_number }}
        </div>
      </NuxtLink>
    </div>

    <!-- Loading State -->
    <div v-if="pending" class="text-center py-12 sm:py-16">
      <div class="text-sm sm:text-base text-gray-500 font-light">Carregando capítulos...</div>
    </div>

    <!-- Error State -->
    <div v-if="error" class="text-center py-12 sm:py-16">
      <div class="text-sm sm:text-base text-gray-600 mb-6">Erro ao carregar o livro</div>
      <button @click="refresh()" class="btn-secondary touch-target">
        Tentar novamente
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Book, Chapter } from '~/types'

// Get route params
const route = useRoute()
const bookSlug = route.params.book as string

// Bible book mapping from slug to name and ID
const bookMapping = {
  // Old Testament
  'gn': { name: 'Gênesis', id: 4 },
  'ex': { name: 'Êxodo', id: 20 },
  'lv': { name: 'Levítico', id: 21 },
  'nm': { name: 'Números', id: 22 },
  'dt': { name: 'Deuteronômio', id: 23 },
  'js': { name: 'Josué', id: 24 },
  'jz': { name: 'Juízes', id: 25 },
  'rt': { name: 'Rute', id: 26 },
  '1sm': { name: '1 Samuel', id: 27 },
  '2sm': { name: '2 Samuel', id: 28 },
  '1rs': { name: '1 Reis', id: 29 },
  '2rs': { name: '2 Reis', id: 30 },
  '1cr': { name: '1 Crônicas', id: 31 },
  '2cr': { name: '2 Crônicas', id: 32 },
  'ed': { name: 'Esdras', id: 33 },
  'ne': { name: 'Neemias', id: 34 },
  'et': { name: 'Ester', id: 35 },
  'jó': { name: 'Jó', id: 36 },
  'sl': { name: 'Salmos', id: 37 },
  'pv': { name: 'Provérbios', id: 38 },
  'ec': { name: 'Eclesiastes', id: 39 },
  'ct': { name: 'Cântico dos Cânticos', id: 40 },
  'is': { name: 'Isaías', id: 41 },
  'jr': { name: 'Jeremias', id: 42 },
  'lm': { name: 'Lamentações', id: 43 },
  'ez': { name: 'Ezequiel', id: 44 },
  'dn': { name: 'Daniel', id: 45 },
  'os': { name: 'Oséias', id: 46 },
  'jl': { name: 'Joel', id: 47 },
  'am': { name: 'Amós', id: 48 },
  'ob': { name: 'Obadias', id: 49 },
  'jn': { name: 'Jonas', id: 50 },
  'mq': { name: 'Miquéias', id: 51 },
  'na': { name: 'Naum', id: 52 },
  'hc': { name: 'Habacuque', id: 53 },
  'sf': { name: 'Sofonias', id: 54 },
  'ag': { name: 'Ageu', id: 55 },
  'zc': { name: 'Zacarias', id: 56 },
  'ml': { name: 'Malaquias', id: 57 },
  // New Testament
  'mt': { name: 'Mateus', id: 58 },
  'mc': { name: 'Marcos', id: 3 },
  'lc': { name: 'Lucas', id: 77 },
  'jo': { name: 'João', id: 78 },
  'atos': { name: 'Atos', id: 79 },
  'rm': { name: 'Romanos', id: 80 },
  '1co': { name: '1 Coríntios', id: 81 },
  '2co': { name: '2 Coríntios', id: 82 },
  'gl': { name: 'Gálatas', id: 83 },
  'ef': { name: 'Efésios', id: 84 },
  'fp': { name: 'Filipenses', id: 7 },
  'cl': { name: 'Colossenses', id: 86 },
  '1ts': { name: '1 Tessalonicenses', id: 87 },
  '2ts': { name: '2 Tessalonicenses', id: 88 },
  '1tm': { name: '1 Timóteo', id: 89 },
  '2tm': { name: '2 Timóteo', id: 90 },
  'tt': { name: 'Tito', id: 91 },
  'fm': { name: 'Filemom', id: 6 },
  'hb': { name: 'Hebreus', id: 93 },
  'tg': { name: 'Tiago', id: 94 },
  '1pe': { name: '1 Pedro', id: 95 },
  '2pe': { name: '2 Pedro', id: 96 },
  '1jo': { name: '1 João', id: 97 },
  '2jo': { name: '2 João', id: 10 },
  '3jo': { name: '3 João', id: 11 },
  'jd': { name: 'Judas', id: 2 },
  'ap': { name: 'Apocalipse', id: 101 }
}

// Get book info from mapping
const bookInfo = bookMapping[bookSlug as keyof typeof bookMapping]

if (!bookInfo) {
  throw createError({ statusCode: 404, statusMessage: 'Livro não encontrado' })
}

const { getBookChapters } = useApi()

// Fetch chapters data
const { data: chapters, pending, error, refresh } = await useLazyAsyncData(
  `book-${bookInfo.id}-chapters`,
  () => getBookChapters(bookInfo.id)
)

// Create book object
const book = computed<Book | null>(() => {
  if (!chapters.value || chapters.value.length === 0) return null

  return {
    id: bookInfo.id,
    name: bookInfo.name,
    testament: ['gn', 'ex', 'lv', 'nm', 'dt', 'js', 'jz', 'rt', '1sm', '2sm', '1rs', '2rs', '1cr', '2cr', 'ed', 'ne', 'et', 'jó', 'sl', 'pv', 'ec', 'ct', 'is', 'jr', 'lm', 'ez', 'dn', 'os', 'jl', 'am', 'ob', 'jn', 'mq', 'na', 'hc', 'sf', 'ag', 'zc', 'ml'].includes(bookSlug)
      ? 'old_testament' : 'new_testament',
    url: '',
    total_chapters: chapters.value.length,
    created_at: '',
    updated_at: ''
  }
})

// Set dynamic page title and meta
watchEffect(() => {
  if (book.value) {
    const testament = book.value.testament === 'old_testament' ? 'Antigo Testamento' : 'Novo Testamento'
    useHead({
      title: `${book.value.name}`,
      meta: [
        { name: 'description', content: `Leia ${book.value.name} (${testament}) com ${book.value.total_chapters} capítulos na Bíblia Online. Interface minimalista para acompanhar transmissões ao vivo.` },
        { property: 'og:title', content: `${book.value.name} - Simplificando O Evangelho` },
        { property: 'og:description', content: `Leia ${book.value.name} (${testament}) com ${book.value.total_chapters} capítulos na Bíblia Online. Interface minimalista para acompanhar transmissões ao vivo.` },
        { property: 'og:url', content: `https://soe.texts.com.br/acf/${bookSlug}` },
        { name: 'keywords', content: `${book.value.name}, ${testament}, bíblia, evangelho, simplificando o evangelho, acf` }
      ]
    })
  }
})
</script>