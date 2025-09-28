import type { Book, Chapter, Verse, SearchResult, Stats } from '~/types'

export const useApi = () => {
  const config = useRuntimeConfig()
  const baseURL = config.public.apiBase

  // Books API
  const getBooks = async (): Promise<Book[]> => {
    return await $fetch<Book[]>(`${baseURL}/books`)
  }

  const getBookChapters = async (bookId: number): Promise<Chapter[]> => {
    return await $fetch<Chapter[]>(`${baseURL}/books/${bookId}/chapters`)
  }

  // Chapters API
  const getChapterVerses = async (chapterId: number): Promise<Verse[]> => {
    return await $fetch<Verse[]>(`${baseURL}/chapters/${chapterId}/verses`)
  }

  // Verses API
  const getVerse = async (verseId: number): Promise<Verse> => {
    return await $fetch<Verse>(`${baseURL}/verses/${verseId}`)
  }

  const getRandomVerse = async (): Promise<Verse> => {
    return await $fetch<Verse>(`${baseURL}/verses/random`)
  }

  const getVerseByReference = async (book: string, chapter: number, verse: number): Promise<Verse> => {
    return await $fetch<Verse>(`${baseURL}/verse/${book}/${chapter}/${verse}`)
  }

  // Search API
  const searchVerses = async (query: string, limit: number = 10): Promise<Verse[]> => {
    return await $fetch<Verse[]>(`${baseURL}/search`, {
      query: { q: query, limit: limit.toString() }
    })
  }

  // Stats API
  const getStats = async (): Promise<Stats> => {
    return await $fetch<Stats>(`${baseURL}/stats`)
  }

  return {
    getBooks,
    getBookChapters,
    getChapterVerses,
    getVerse,
    getRandomVerse,
    getVerseByReference,
    searchVerses,
    getStats
  }
}