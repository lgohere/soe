-- Database initialization script for Coolify deployment
-- Creates database structure if not exists and loads backup data

-- Create database if not exists (will be ignored if already exists)
CREATE DATABASE IF NOT EXISTS bibliasoe;

-- Use the database
\c bibliasoe;

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE bibliasoe TO soe;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO soe;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO soe;

-- Create tables if they don't exist
CREATE TABLE IF NOT EXISTS books (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    testament VARCHAR(50) NOT NULL,
    url TEXT,
    total_chapters INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    biblical_order INTEGER
);

CREATE TABLE IF NOT EXISTS chapters (
    id SERIAL PRIMARY KEY,
    book_id INTEGER REFERENCES books(id) ON DELETE CASCADE,
    chapter_number INTEGER NOT NULL,
    total_verses INTEGER,
    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS verses (
    id SERIAL PRIMARY KEY,
    chapter_id INTEGER REFERENCES chapters(id) ON DELETE CASCADE,
    verse_number INTEGER NOT NULL,
    text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create bible_verses view if not exists
CREATE OR REPLACE VIEW bible_verses AS
SELECT
    b.name as book_name,
    b.testament,
    c.chapter_number,
    v.verse_number,
    v.text as verse_text
FROM books b
JOIN chapters c ON b.id = c.book_id
JOIN verses v ON c.id = v.chapter_id
ORDER BY b.biblical_order, c.chapter_number, v.verse_number;

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_chapters_book_id ON chapters(book_id);
CREATE INDEX IF NOT EXISTS idx_verses_chapter_id ON verses(chapter_id);
CREATE INDEX IF NOT EXISTS idx_books_testament ON books(testament);
CREATE INDEX IF NOT EXISTS idx_verses_text ON verses USING gin(to_tsvector('portuguese', text));