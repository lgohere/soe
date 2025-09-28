<template>
  <div class="space-y-16">
    <!-- Chapter Header -->
    <div class="text-center" v-if="verses && verses.length > 0">
      <div class="mb-8">
        <NuxtLink :to="`/acf/${bookSlug}`" class="nav-link text-sm">
          ← {{ verses[0].book_name }}
        </NuxtLink>
      </div>
      <h1 class="chapter-title">
        {{ verses[0].book_name }} {{ verses[0].chapter_number }}
      </h1>
    </div>

    <!-- Chapter Navigation -->
    <div class="flex justify-center space-x-8" v-if="verses && verses.length > 0">
      <button
        v-if="chapterNumber > 1"
        @click="navigateChapter(-1)"
        class="btn-secondary text-sm"
      >
        Capítulo Anterior
      </button>
      <button
        v-if="hasNextChapter"
        @click="navigateChapter(1)"
        class="btn-secondary text-sm"
      >
        Próximo Capítulo
      </button>
    </div>

    <!-- Verses Display -->
    <div class="max-w-3xl mx-auto">
      <div v-if="verses" class="space-y-0 pb-32">
        <div
          v-for="verse in verses"
          :key="verse.id"
          class="verse-container flex items-start space-x-6"
          :id="`verse-${verse.verse_number}`"
        >
          <!-- Verse Number -->
          <div class="flex-shrink-0 w-8 text-center">
            <span class="text-sm text-gray-400 font-light">{{ verse.verse_number }}</span>
          </div>

          <!-- Verse Text -->
          <div class="flex-1">
            <p class="verse-text">
              {{ verse.text }}
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="pending" class="text-center py-16">
      <div class="text-base text-gray-500 font-light">Carregando versículos...</div>
    </div>

    <!-- Error State -->
    <div v-if="error" class="text-center py-16">
      <div class="text-base text-gray-600 mb-6">Erro ao carregar o capítulo</div>
      <button @click="refresh()" class="btn-secondary">
        Tentar novamente
      </button>
    </div>

    <!-- Modern Floating Navigation (appears at bottom when scrolled to end) -->
    <Transition
      enter-active-class="transition-all duration-500 ease-out"
      enter-from-class="opacity-0 translate-y-full"
      enter-to-class="opacity-100 translate-y-0"
      leave-active-class="transition-all duration-300 ease-in"
      leave-from-class="opacity-100 translate-y-0"
      leave-to-class="opacity-0 translate-y-full"
    >
      <div
        v-if="showFloatingNav && verses && verses.length > 0"
        class="fixed bottom-0 left-0 right-0 bg-white/95 backdrop-blur-md border-t border-gray-200 shadow-lg z-40"
      >
        <div class="max-w-4xl mx-auto px-6 py-4">
          <div class="flex justify-between items-center">
            <!-- Previous Chapter -->
            <button
              v-if="chapterNumber > 1"
              @click="navigateChapter(-1)"
              class="flex items-center space-x-3 px-6 py-3 text-gray-700 hover:text-gray-900 hover:bg-gray-50 rounded-lg transition-all duration-200 group"
            >
              <svg class="w-5 h-5 transform group-hover:-translate-x-1 transition-transform duration-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
              </svg>
              <div class="text-left">
                <div class="text-xs text-gray-500 font-light">Anterior</div>
                <div class="text-sm font-medium">{{ bookInfo.name }} {{ chapterNumber - 1 }}</div>
              </div>
            </button>

            <!-- Spacer if no previous chapter -->
            <div v-else class="w-32"></div>

            <!-- Chapter Info -->
            <div class="text-center">
              <div class="text-xs text-gray-500 font-light">Capítulo</div>
              <div class="text-lg font-medium text-gray-900">{{ chapterNumber }}</div>
            </div>

            <!-- Next Chapter -->
            <button
              v-if="hasNextChapter"
              @click="navigateChapter(1)"
              class="flex items-center space-x-3 px-6 py-3 text-gray-700 hover:text-gray-900 hover:bg-gray-50 rounded-lg transition-all duration-200 group"
            >
              <div class="text-right">
                <div class="text-xs text-gray-500 font-light">Próximo</div>
                <div class="text-sm font-medium">{{ bookInfo.name }} {{ chapterNumber + 1 }}</div>
              </div>
              <svg class="w-5 h-5 transform group-hover:translate-x-1 transition-transform duration-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
              </svg>
            </button>

            <!-- Spacer if no next chapter -->
            <div v-else class="w-32"></div>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup lang="ts">
import type { Verse } from '~/types'

// Get route params
const route = useRoute()
const router = useRouter()
const bookSlug = route.params.book as string
const chapterNumber = Number(route.params.chapter)

// Bible book mapping from slug to name and ID
const bookMapping = {
  // Old Testament
  'gn': { name: 'Gênesis', id: 4, maxChapters: 50 },
  'ex': { name: 'Êxodo', id: 20, maxChapters: 40 },
  'lv': { name: 'Levítico', id: 21, maxChapters: 27 },
  'nm': { name: 'Números', id: 22, maxChapters: 36 },
  'dt': { name: 'Deuteronômio', id: 23, maxChapters: 34 },
  'js': { name: 'Josué', id: 24, maxChapters: 24 },
  'jz': { name: 'Juízes', id: 25, maxChapters: 21 },
  'rt': { name: 'Rute', id: 26, maxChapters: 4 },
  '1sm': { name: '1 Samuel', id: 27, maxChapters: 31 },
  '2sm': { name: '2 Samuel', id: 28, maxChapters: 24 },
  '1rs': { name: '1 Reis', id: 29, maxChapters: 22 },
  '2rs': { name: '2 Reis', id: 30, maxChapters: 25 },
  '1cr': { name: '1 Crônicas', id: 31, maxChapters: 29 },
  '2cr': { name: '2 Crônicas', id: 32, maxChapters: 36 },
  'ed': { name: 'Esdras', id: 33, maxChapters: 10 },
  'ne': { name: 'Neemias', id: 34, maxChapters: 13 },
  'et': { name: 'Ester', id: 35, maxChapters: 10 },
  'jó': { name: 'Jó', id: 36, maxChapters: 42 },
  'sl': { name: 'Salmos', id: 37, maxChapters: 150 },
  'pv': { name: 'Provérbios', id: 38, maxChapters: 31 },
  'ec': { name: 'Eclesiastes', id: 39, maxChapters: 12 },
  'ct': { name: 'Cântico dos Cânticos', id: 40, maxChapters: 8 },
  'is': { name: 'Isaías', id: 41, maxChapters: 66 },
  'jr': { name: 'Jeremias', id: 42, maxChapters: 52 },
  'lm': { name: 'Lamentações', id: 43, maxChapters: 5 },
  'ez': { name: 'Ezequiel', id: 44, maxChapters: 48 },
  'dn': { name: 'Daniel', id: 45, maxChapters: 12 },
  'os': { name: 'Oséias', id: 46, maxChapters: 14 },
  'jl': { name: 'Joel', id: 47, maxChapters: 3 },
  'am': { name: 'Amós', id: 48, maxChapters: 9 },
  'ob': { name: 'Obadias', id: 49, maxChapters: 1 },
  'jn': { name: 'Jonas', id: 50, maxChapters: 4 },
  'mq': { name: 'Miquéias', id: 51, maxChapters: 7 },
  'na': { name: 'Naum', id: 52, maxChapters: 3 },
  'hc': { name: 'Habacuque', id: 53, maxChapters: 3 },
  'sf': { name: 'Sofonias', id: 54, maxChapters: 3 },
  'ag': { name: 'Ageu', id: 55, maxChapters: 2 },
  'zc': { name: 'Zacarias', id: 56, maxChapters: 14 },
  'ml': { name: 'Malaquias', id: 57, maxChapters: 4 },
  // New Testament
  'mt': { name: 'Mateus', id: 58, maxChapters: 28 },
  'mc': { name: 'Marcos', id: 3, maxChapters: 16 },
  'lc': { name: 'Lucas', id: 77, maxChapters: 24 },
  'jo': { name: 'João', id: 78, maxChapters: 21 },
  'atos': { name: 'Atos', id: 79, maxChapters: 28 },
  'rm': { name: 'Romanos', id: 80, maxChapters: 16 },
  '1co': { name: '1 Coríntios', id: 81, maxChapters: 16 },
  '2co': { name: '2 Coríntios', id: 82, maxChapters: 13 },
  'gl': { name: 'Gálatas', id: 83, maxChapters: 6 },
  'ef': { name: 'Efésios', id: 84, maxChapters: 6 },
  'fp': { name: 'Filipenses', id: 7, maxChapters: 4 },
  'cl': { name: 'Colossenses', id: 86, maxChapters: 4 },
  '1ts': { name: '1 Tessalonicenses', id: 87, maxChapters: 5 },
  '2ts': { name: '2 Tessalonicenses', id: 88, maxChapters: 3 },
  '1tm': { name: '1 Timóteo', id: 89, maxChapters: 6 },
  '2tm': { name: '2 Timóteo', id: 90, maxChapters: 4 },
  'tt': { name: 'Tito', id: 91, maxChapters: 3 },
  'fm': { name: 'Filemom', id: 6, maxChapters: 1 },
  'hb': { name: 'Hebreus', id: 93, maxChapters: 13 },
  'tg': { name: 'Tiago', id: 94, maxChapters: 5 },
  '1pe': { name: '1 Pedro', id: 95, maxChapters: 5 },
  '2pe': { name: '2 Pedro', id: 96, maxChapters: 3 },
  '1jo': { name: '1 João', id: 97, maxChapters: 5 },
  '2jo': { name: '2 João', id: 10, maxChapters: 1 },
  '3jo': { name: '3 João', id: 11, maxChapters: 1 },
  'jd': { name: 'Judas', id: 2, maxChapters: 1 },
  'ap': { name: 'Apocalipse', id: 101, maxChapters: 22 }
}

// Get book info from mapping
const bookInfo = bookMapping[bookSlug as keyof typeof bookMapping]

if (!bookInfo) {
  throw createError({ statusCode: 404, statusMessage: 'Livro não encontrado' })
}

if (chapterNumber < 1 || chapterNumber > bookInfo.maxChapters) {
  throw createError({ statusCode: 404, statusMessage: 'Capítulo não encontrado' })
}

const { getBookChapters, getChapterVerses } = useApi()

// Get chapters to find the correct chapter ID
const { data: chapters } = await useLazyAsyncData(
  `book-${bookInfo.id}-chapters`,
  () => getBookChapters(bookInfo.id)
)

// Find the chapter ID for the current chapter number
const chapterId = computed(() => {
  if (!chapters.value) return null
  const chapter = chapters.value.find((c: any) => c.chapter_number === chapterNumber)
  return chapter?.id || null
})

// Fetch verses data
const { data: verses, pending, error, refresh } = await useLazyAsyncData(
  `chapter-${chapterId.value}-verses`,
  () => chapterId.value ? getChapterVerses(chapterId.value) : null,
  {
    watch: [chapterId]
  }
)

// Check if there's a next chapter
const hasNextChapter = computed(() => {
  return chapterNumber < bookInfo.maxChapters
})

// Set dynamic page title
watchEffect(() => {
  if (verses.value && verses.value.length > 0) {
    const firstVerse = verses.value[0]
    useHead({
      title: `${firstVerse.book_name} ${firstVerse.chapter_number}`,
      meta: [
        { name: 'description', content: `Leia ${firstVerse.book_name} capítulo ${firstVerse.chapter_number} com ${verses.value.length} versículos` }
      ]
    })
  }
})

// Scroll detection for floating navigation
const showFloatingNav = ref(false)

const handleScroll = () => {
  const windowHeight = window.innerHeight
  const documentHeight = document.documentElement.scrollHeight
  const scrollTop = window.pageYOffset || document.documentElement.scrollTop

  // Show floating nav ONLY when user reaches the very bottom (within 10px of the end)
  const distanceFromBottom = documentHeight - (scrollTop + windowHeight)
  showFloatingNav.value = distanceFromBottom <= 10
}

// Setup scroll listener
onMounted(() => {
  window.addEventListener('scroll', handleScroll, { passive: true })
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})

// Navigation functions
const navigateChapter = (direction: number) => {
  const newChapter = chapterNumber + direction

  if (newChapter >= 1 && newChapter <= bookInfo.maxChapters) {
    router.push(`/acf/${bookSlug}/${newChapter}`)
  }
}
</script>