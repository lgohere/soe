#!/usr/bin/env python3
"""
Script to recover failed chapters from error log
"""

import re
from selenium_scraper import SeleniumBibleScraper

def parse_failed_chapters(error_file):
    """Parse the error file to extract failed chapters"""
    failed_chapters = []

    with open(error_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pattern to match failed URLs
    pattern = r'Failed to load https://www\.bibliaonline\.com\.br/acf/([^/]+)/(\d+)'
    matches = re.findall(pattern, content)

    # Remove duplicates while preserving order
    seen = set()
    for book_code, chapter in matches:
        key = (book_code, int(chapter))
        if key not in seen:
            failed_chapters.append(key)
            seen.add(key)

    return failed_chapters

def get_book_name_from_code(code):
    """Map book codes to full names"""
    book_mapping = {
        'dt': 'Deuteronômio',
        'jó': 'Jó',
        'sl': 'Salmos',
        'jr': 'Jeremias',
        'mt': 'Mateus'
    }
    return book_mapping.get(code, code)

def main():
    print("=== RECOVERING FAILED CHAPTERS ===")

    # Parse failed chapters
    failed_chapters = parse_failed_chapters('erro.txt')

    print(f"Found {len(failed_chapters)} failed chapters:")
    for book_code, chapter in failed_chapters:
        book_name = get_book_name_from_code(book_code)
        print(f"  - {book_name} {chapter}")

    if not failed_chapters:
        print("No failed chapters found!")
        return

    # Initialize scraper
    scraper = None
    try:
        scraper = SeleniumBibleScraper()

        # Load bible data to get book info
        bible_data = scraper.load_bible_data()
        all_books = bible_data['old_testament'] + bible_data['new_testament']

        # Create book mapping
        book_map = {}
        for book in all_books:
            # Extract book code from URL
            url = book['url']
            code = url.split('/')[-1]
            book_map[code] = book

        print(f"\nStarting recovery process...")
        recovered_count = 0

        for book_code, chapter_num in failed_chapters:
            try:
                if book_code not in book_map:
                    print(f"✗ Book code '{book_code}' not found in mapping")
                    continue

                book_data = book_map[book_code]
                book_name = book_data['book']
                book_url = book_data['url']

                print(f"\n📖 Recovering {book_name} chapter {chapter_num}...")

                # Get book ID from database
                book_id = scraper.book_model.insert(
                    book_name,
                    'old_testament' if book_data in bible_data['old_testament'] else 'new_testament',
                    book_url,
                    book_data['chapters']
                )

                # Try to scrape the specific chapter
                success = scraper.scrape_chapter(book_id, book_url, chapter_num)

                if success:
                    print(f"✓ Successfully recovered {book_name} {chapter_num}")
                    recovered_count += 1
                else:
                    print(f"✗ Failed to recover {book_name} {chapter_num}")

                # Small delay between recoveries
                import time
                time.sleep(2)

            except Exception as e:
                print(f"✗ Error recovering {book_code} {chapter_num}: {e}")
                continue

        print(f"\n=== RECOVERY COMPLETE ===")
        print(f"Recovered: {recovered_count}/{len(failed_chapters)} chapters")
        print(scraper.get_performance_summary())

    finally:
        if scraper:
            scraper.close()

if __name__ == "__main__":
    main()