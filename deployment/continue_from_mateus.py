#!/usr/bin/env python3
"""
Continue scraping from Mateus onwards
"""

from selenium_scraper import SeleniumBibleScraper

def main():
    print("=== CONTINUING FROM MATEUS ===")

    scraper = None
    try:
        scraper = SeleniumBibleScraper()

        # Load bible data
        bible_data = scraper.load_bible_data()
        new_testament_books = bible_data['new_testament']

        # Find starting point (Mateus)
        start_index = 0
        for i, book in enumerate(new_testament_books):
            if 'Mateus' in book['book']:
                start_index = i
                break

        # Get books from Mateus onwards
        books_to_scrape = new_testament_books[start_index:]

        print(f"Will scrape {len(books_to_scrape)} books from Mateus:")
        for book in books_to_scrape:
            print(f"  - {book['book']} ({book['chapters']} chapters)")

        print(f"\nStarting scraping...")
        successful_books = 0

        for book_data in books_to_scrape:
            try:
                book_name = book_data['book']
                print(f"\n📖 Starting {book_name}...")

                success = scraper.scrape_book(book_data)
                if success:
                    print(f"✓ Completed {book_name}")
                    successful_books += 1
                else:
                    print(f"⚠️  {book_name} completed with some errors")
                    successful_books += 1  # Count as success since some chapters were scraped

                # Short break between books
                import time
                time.sleep(3)

            except Exception as e:
                print(f"✗ Error scraping {book_data['book']}: {e}")
                continue

        print(f"\n=== SCRAPING COMPLETED ===")
        print(f"Successfully processed: {successful_books}/{len(books_to_scrape)} books")
        print(scraper.get_performance_summary())

    finally:
        if scraper:
            scraper.close()

if __name__ == "__main__":
    main()