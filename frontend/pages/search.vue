<template>
  <div class="space-y-16">
    <!-- Search Header -->
    <div class="text-center">
      <h1 class="chapter-title" style="letter-spacing: 0pt; font-family:cursive">Buscar Versículos</h1>
    </div>

    <!-- Search Form -->
    <div class="max-w-xl mx-auto">
      <form @submit.prevent="performSearch" class="space-y-8">
        <div>
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Digite sua busca..."
            class="input-field"
            :disabled="searching"
          >
        </div>

        <div class="text-center">
          <button
            type="submit"
            :disabled="!searchQuery.trim() || searching"
            class="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {{ searching ? 'Buscando...' : 'Buscar' }}
          </button>
        </div>
      </form>
    </div>

    <!-- Search Results -->
    <div v-if="searchResults.length > 0" class="max-w-3xl mx-auto">
      <div class="mb-12 text-center">
        <h2 class="text-lg font-light text-gray-900 mb-2">
          {{ searchResults.length }} resultado{{ searchResults.length !== 1 ? 's' : '' }}
        </h2>
        <p class="text-sm text-gray-500 font-light">{{ lastSearchQuery }}</p>
      </div>

      <div class="space-y-8">
        <div
          v-for="verse in searchResults"
          :key="verse.id"
          class="border-b border-gray-100 pb-8 last:border-b-0"
        >
          <div class="mb-4">
            <span class="text-sm text-gray-500 font-light">
              {{ verse.book_name }} {{ verse.chapter_number }}:{{ verse.verse_number }}
            </span>
          </div>

          <p class="verse-text mb-4" v-html="highlightSearchTerm(verse.text)"></p>

          <NuxtLink
            :to="`/chapters/${verse.chapter_id}`"
            class="nav-link text-sm"
          >
            Ler capítulo completo
          </NuxtLink>
        </div>
      </div>
    </div>

    <!-- No Results -->
    <div v-if="hasSearched && searchResults.length === 0 && !searching" class="text-center py-16">
      <div class="text-base text-gray-600 mb-4">
        Nenhum versículo encontrado
      </div>
      <p class="text-sm text-gray-500">
        Tente usar palavras diferentes
      </p>
    </div>

    <!-- Quick Search Suggestions -->
    <div v-if="!hasSearched" class="max-w-xl mx-auto">
      <h3 class="text-base font-light text-gray-900 mb-6 text-center">Sugestões</h3>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
        <button
          v-for="suggestion in quickSearches"
          :key="suggestion"
          @click="quickSearch(suggestion)"
          class="btn-secondary text-sm py-2 px-4"
        >
          {{ suggestion }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Verse } from '~/types'

// Page meta
useHead({
  title: 'Buscar Versículos',
  meta: [
    { name: 'description', content: 'Busque versículos específicos na Bíblia com nossa ferramenta de busca minimalista. Encontre passagens por palavra-chave.' },
    { property: 'og:title', content: 'Buscar Versículos - Simplificando O Evangelho' },
    { property: 'og:description', content: 'Busque versículos específicos na Bíblia com nossa ferramenta de busca minimalista. Encontre passagens por palavra-chave.' },
    { property: 'og:url', content: 'https://soe.texts.com.br/search' }
  ]
})

// Reactive data
const searchQuery = ref('')
const lastSearchQuery = ref('')
const searchResults = ref<Verse[]>([])
const searching = ref(false)
const hasSearched = ref(false)

const { searchVerses } = useApi()

// Quick search suggestions
const quickSearches = [
  'amor', 'fé', 'esperança', 'paz',
  'Jesus', 'Deus', 'salvação', 'perdão'
]

// Search function
const performSearch = async () => {
  if (!searchQuery.value.trim() || searching.value) return

  searching.value = true
  lastSearchQuery.value = searchQuery.value.trim()

  try {
    searchResults.value = await searchVerses(lastSearchQuery.value, 20)
    hasSearched.value = true
  } catch (error) {
    console.error('Erro na busca:', error)
    searchResults.value = []
  } finally {
    searching.value = false
  }
}

// Quick search function
const quickSearch = (term: string) => {
  searchQuery.value = term
  performSearch()
}

// Highlight search terms in results
const highlightSearchTerm = (text: string): string => {
  if (!lastSearchQuery.value) return text

  const regex = new RegExp(`(${lastSearchQuery.value})`, 'gi')
  return text.replace(regex, '<mark class="bg-gray-100 text-gray-900 font-medium">$1</mark>')
}

</script>