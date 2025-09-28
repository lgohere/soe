<template>
  <div class="space-y-16">
    <!-- Chapter Header -->
    <div class="text-center" v-if="verses && verses.length > 0">
      <div class="mb-8">
        <NuxtLink :to="`/books/${verses[0].book_id}`" class="nav-link text-sm">
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
        v-if="verses[0].chapter_number > 1"
        @click="navigateChapter(-1)"
        class="btn-secondary text-sm"
      >
        Capítulo Anterior
      </button>
      <button
        @click="navigateChapter(1)"
        class="btn-secondary text-sm"
      >
        Próximo Capítulo
      </button>
    </div>

    <!-- Verses Display -->
    <div class="max-w-3xl mx-auto">
      <div v-if="verses" class="space-y-0">
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
  </div>
</template>

<script setup lang="ts">
import type { Verse } from '~/types'

// Get route params
const route = useRoute()
const router = useRouter()
const chapterId = Number(route.params.id)

const { getChapterVerses } = useApi()

// Fetch verses data
const { data: verses, pending, error, refresh } = await useLazyAsyncData(
  `chapter-${chapterId}-verses`,
  () => getChapterVerses(chapterId)
)

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

// Navigation functions
const navigateChapter = (direction: number) => {
  if (!verses.value || verses.value.length === 0) return

  const currentChapter = verses.value[0].chapter_number
  const newChapter = currentChapter + direction

  // For now, we'll implement basic navigation
  // In a real app, you'd need to find the next chapter ID
  console.log(`Navigate to chapter ${newChapter}`)
}
</script>