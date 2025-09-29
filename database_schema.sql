-- Database schema for Bible scraping project

CREATE DATABASE bibliasoe;

-- Connect to the database
\c bibliasoe;

-- Create tables
CREATE TABLE IF NOT EXISTS books (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    testament VARCHAR(20) NOT NULL CHECK (testament IN ('old_testament', 'new_testament')),
    url VARCHAR(255) NOT NULL,
    total_chapters INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS chapters (
    id SERIAL PRIMARY KEY,
    book_id INTEGER REFERENCES books(id) ON DELETE CASCADE,
    chapter_number INTEGER NOT NULL,
    total_verses INTEGER,
    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(book_id, chapter_number)
);

CREATE TABLE IF NOT EXISTS verses (
    id SERIAL PRIMARY KEY,
    chapter_id INTEGER REFERENCES chapters(id) ON DELETE CASCADE,
    verse_number INTEGER NOT NULL,
    text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(chapter_id, verse_number)
);

-- Create indexes for better performance
CREATE INDEX idx_books_testament ON books(testament);
CREATE INDEX idx_chapters_book_id ON chapters(book_id);
CREATE INDEX idx_chapters_book_chapter ON chapters(book_id, chapter_number);
CREATE INDEX idx_verses_chapter_id ON verses(chapter_id);
CREATE INDEX idx_verses_chapter_verse ON verses(chapter_id, verse_number);

-- Create a view for easy querying
CREATE OR REPLACE VIEW bible_verses AS
SELECT
    b.name as book_name,
    b.testament,
    c.chapter_number,
    v.verse_number,
    v.text as verse_text,
    v.created_at
FROM books b
JOIN chapters c ON b.id = c.book_id
JOIN verses v ON c.id = v.chapter_id
ORDER BY b.id, c.chapter_number, v.verse_number;