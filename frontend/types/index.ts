export interface Book {
  id: number
  name: string
  testament: 'old_testament' | 'new_testament'
  url: string
  total_chapters: number
  created_at: string
  updated_at: string
}

export interface Chapter {
  id: number
  book_id: number
  chapter_number: number
  total_verses: number
  scraped_at: string
  created_at: string
  updated_at: string
  book_name: string
}

export interface Verse {
  id: number
  chapter_id: number
  verse_number: number
  text: string
  created_at: string
  updated_at: string
  chapter_number: number
  book_name: string
  testament: string
  book_id?: number
  relevance_score?: number
}

export interface SearchResult {
  verses: Verse[]
  total: number
  query: string
}

export interface Stats {
  total_books: number
  total_chapters: number
  total_verses: number
  old_testament_books: number
  new_testament_books: number
  avg_verse_length: number
  api_version: string
  target_audience: string
  last_updated: string
  database_status: string
}