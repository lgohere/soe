<template>
  <div class="space-y-6 sm:space-y-8">
    <!-- Page Header -->
    <div class="text-center">
      <h1 class="text-xl sm:text-2xl md:text-3xl font-normal text-gray-900 tracking-wide">
        Leitura das Sagradas Escrituras
      </h1>
    </div>

    <!-- Testament Navigation -->
    <div class="flex justify-center">
      <div class="flex border border-gray-200 rounded-none mx-auto w-full max-w-md sm:max-w-none sm:w-auto">
        <button
          @click="activeTestament = 'old_testament'"
          :class="[
            'flex-1 sm:flex-none px-3 sm:px-6 py-2 font-light text-xs sm:text-sm transition-all duration-300 focus:outline-none',
            activeTestament === 'old_testament'
              ? 'bg-[#304E69] text-white'
              : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50 bg-white'
          ]"
        >
          Antigo Testamento
        </button>
        <button
          @click="activeTestament = 'new_testament'"
          :class="[
            'flex-1 sm:flex-none px-3 sm:px-6 py-2 font-light text-xs sm:text-sm transition-all duration-300 border-l border-gray-200 focus:outline-none',
            activeTestament === 'new_testament'
              ? 'bg-[#304E69] text-white'
              : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50 bg-white'
          ]"
        >
          Novo Testamento
        </button>
      </div>
    </div>

    <!-- Books Grid -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3 sm:gap-4">
      <NuxtLink
        v-for="book in filteredBooks"
        :key="book.id"
        :to="`/acf/${getBookSlug(book.name)}`"
        class="card p-3 sm:p-4 group cursor-pointer hover:shadow-sm transition-all"
      >
        <div>
          <h3 class="text-base sm:text-lg md:text-xl font-normal text-gray-900 tracking-wide mb-1 sm:mb-2 group-hover:text-gray-700 transition-colors">
            {{ book.name }}
          </h3>
          <p class="text-xs sm:text-sm text-gray-500 font-light">
            {{ book.total_chapters }} capítulo{{ book.total_chapters !== 1 ? 's' : '' }}
          </p>
        </div>
      </NuxtLink>
    </div>

    <!-- Loading State -->
    <div v-if="pending" class="text-center py-12 sm:py-16">
      <div class="text-sm sm:text-base text-gray-500 font-light">Carregando livros...</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Book } from '~/types'

// Page meta
useHead({
  title: 'Bíblia Online',
  meta: [
    { name: 'description', content: 'Navegue pelos 66 livros da Bíblia com interface minimalista. Leitura bíblica compartilhada durante transmissões ao vivo.' },
    { property: 'og:title', content: 'Bíblia Online - Simplificando O Evangelho' },
    { property: 'og:description', content: 'Navegue pelos 66 livros da Bíblia com interface minimalista. Leitura bíblica compartilhada durante transmissões ao vivo.' },
    { property: 'og:url', content: 'https://soe.texts.com.br' }
  ]
})

// Reactive data
const activeTestament = ref<'old_testament' | 'new_testament'>('old_testament')
const { getBooks } = useApi()

// Fetch books data
const { data: books, pending } = await useLazyAsyncData('books', () => getBooks())

// Computed properties
const oldTestamentBooks = computed(() =>
  books.value?.filter(book => book.testament === 'old_testament') || []
)

const newTestamentBooks = computed(() =>
  books.value?.filter(book => book.testament === 'new_testament') || []
)

const filteredBooks = computed(() =>
  activeTestament.value === 'old_testament' ? oldTestamentBooks.value : newTestamentBooks.value
)

// Book name to slug mapping
const bookSlugMapping: Record<string, string> = {
  // Old Testament
  'Gênesis': 'gn',
  'Êxodo': 'ex',
  'Levítico': 'lv',
  'Números': 'nm',
  'Deuteronômio': 'dt',
  'Josué': 'js',
  'Juízes': 'jz',
  'Rute': 'rt',
  '1 Samuel': '1sm',
  '2 Samuel': '2sm',
  '1 Reis': '1rs',
  '2 Reis': '2rs',
  '1 Crônicas': '1cr',
  '2 Crônicas': '2cr',
  'Esdras': 'ed',
  'Neemias': 'ne',
  'Ester': 'et',
  'Jó': 'jó',
  'Salmos': 'sl',
  'Provérbios': 'pv',
  'Eclesiastes': 'ec',
  'Cântico dos Cânticos': 'ct',
  'Isaías': 'is',
  'Jeremias': 'jr',
  'Lamentações': 'lm',
  'Ezequiel': 'ez',
  'Daniel': 'dn',
  'Oséias': 'os',
  'Joel': 'jl',
  'Amós': 'am',
  'Obadias': 'ob',
  'Jonas': 'jn',
  'Miquéias': 'mq',
  'Naum': 'na',
  'Habacuque': 'hc',
  'Sofonias': 'sf',
  'Ageu': 'ag',
  'Zacarias': 'zc',
  'Malaquias': 'ml',
  // New Testament
  'Mateus': 'mt',
  'Marcos': 'mc',
  'Lucas': 'lc',
  'João': 'jo',
  'Atos': 'atos',
  'Romanos': 'rm',
  '1 Coríntios': '1co',
  '2 Coríntios': '2co',
  'Gálatas': 'gl',
  'Efésios': 'ef',
  'Filipenses': 'fp',
  'Colossenses': 'cl',
  '1 Tessalonicenses': '1ts',
  '2 Tessalonicenses': '2ts',
  '1 Timóteo': '1tm',
  '2 Timóteo': '2tm',
  'Tito': 'tt',
  'Filemom': 'fm',
  'Hebreus': 'hb',
  'Tiago': 'tg',
  '1 Pedro': '1pe',
  '2 Pedro': '2pe',
  '1 João': '1jo',
  '2 João': '2jo',
  '3 João': '3jo',
  'Judas': 'jd',
  'Apocalipse': 'ap'
}

// Function to get book slug from name
const getBookSlug = (bookName: string): string => {
  return bookSlugMapping[bookName] || bookName.toLowerCase()
}
</script>