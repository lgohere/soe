# Bible Web Scraping Project

Efficient web scraping solution for extracting Bible content from bibliaonline.com.br and storing it in PostgreSQL database.

## Features

- **Respectful Scraping**: Random delays between requests and proper headers
- **Error Handling**: Retry logic and comprehensive error handling
- **Database Storage**: PostgreSQL with optimized schema and indexes
- **Batch Processing**: Efficient batch inserts for verses
- **Logging**: Comprehensive logging to file and console
- **Flexible Execution**: Command-line options for different scraping scenarios

## Database Schema

- **books**: Store book information (name, testament, URL, chapters)
- **chapters**: Store chapter information linked to books
- **verses**: Store individual verses linked to chapters
- **Indexes**: Optimized for fast querying
- **View**: `bible_verses` for easy querying across all tables

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Setup PostgreSQL database and update `.env` file with your credentials

3. Initialize database schema:
```bash
python main.py --init-db
```

## Usage

### Full Bible Scraping
```bash
python main.py
```

### Scrape Specific Testament
```bash
python main.py --testament old_testament
python main.py --testament new_testament
```

### Scrape Specific Book
```bash
python main.py --book "Gênesis"
python main.py --book "Mateus"
```

### View Statistics
```bash
python main.py --stats
```

### Custom Delay Range
```bash
python main.py --delay 2 5  # 2-5 seconds between requests
```

## Configuration

The scraper uses the `Biblia web-scrapping.json` file for book configuration, which contains:
- Book names
- URLs
- Chapter counts
- Testament classification

## Data Extraction

The scraper extracts:
- **Verse Numbers**: From `<span class="v">` elements
- **Verse Text**: From `<span class="t">` elements
- **Chapter Information**: Automatically calculated
- **Book Metadata**: From configuration file

## Error Handling

- Retry logic for failed requests
- Exponential backoff for temporary failures
- Comprehensive logging
- Database transaction safety
- Duplicate handling with UPSERT operations

## Performance Optimizations

- Session reuse for HTTP requests
- Batch inserts for verses
- Database indexes for fast queries
- Connection pooling
- Memory-efficient processing

## Example Query

After scraping, you can query the data:

```sql
-- Get all verses from Genesis chapter 1
SELECT * FROM bible_verses
WHERE book_name = 'Gênesis' AND chapter_number = 1;

-- Count verses by book
SELECT book_name, COUNT(*) as verse_count
FROM bible_verses
GROUP BY book_name;
```

## Logs

Scraping logs are saved to `scraping.log` with detailed information about:
- URLs being processed
- Verses extracted per chapter
- Errors and retries
- Performance metrics