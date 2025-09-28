#!/usr/bin/env python3
"""
Bible Scraper with Selenium - Main execution script
"""

import argparse
import sys
import logging
from selenium_scraper import SeleniumBibleScraper
from models import DatabaseManager

def setup_database():
    """Initialize database with schema"""
    try:
        db_manager = DatabaseManager()

        with open('database_schema.sql', 'r', encoding='utf-8') as f:
            schema_sql = f.read()

        # Execute schema (skip database creation part)
        schema_lines = schema_sql.split('\n')
        filtered_lines = []
        skip_until_connect = False

        for line in schema_lines:
            if line.strip().startswith('CREATE DATABASE'):
                skip_until_connect = True
                continue
            elif line.strip().startswith('\\c bibliasoe'):
                skip_until_connect = False
                continue
            elif not skip_until_connect:
                filtered_lines.append(line)

        filtered_schema = '\n'.join(filtered_lines)

        with db_manager.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(filtered_schema)
                conn.commit()

        print("Database schema initialized successfully!")
        return True

    except Exception as e:
        print(f"Error initializing database: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Bible Scraper with Selenium')
    parser.add_argument('--testament', choices=['old_testament', 'new_testament'],
                       help='Scrape specific testament only')
    parser.add_argument('--init-db', action='store_true',
                       help='Initialize database schema')
    parser.add_argument('--book', type=str,
                       help='Scrape specific book only (partial name matching)')
    parser.add_argument('--delay', type=float, nargs=2, default=[0.3, 1.0],
                       help='Delay range between requests (min max in seconds)')

    args = parser.parse_args()

    # Initialize database if requested
    if args.init_db:
        if setup_database():
            print("Database initialized successfully!")
        else:
            print("Failed to initialize database")
            sys.exit(1)
        return

    # Initialize scraper
    scraper = None
    try:
        scraper = SeleniumBibleScraper(delay_range=tuple(args.delay))

        # Scrape specific book
        if args.book:
            try:
                bible_data = scraper.load_bible_data()
                all_books = bible_data['old_testament'] + bible_data['new_testament']

                # Find book by partial name match
                matching_books = [book for book in all_books
                                if args.book.lower() in book['book'].lower()]

                if not matching_books:
                    print(f"No books found matching '{args.book}'")
                    sys.exit(1)

                if len(matching_books) > 1:
                    print(f"Multiple books found matching '{args.book}':")
                    for book in matching_books:
                        print(f"  - {book['book']}")
                    print("Please be more specific.")
                    sys.exit(1)

                book_to_scrape = matching_books[0]
                print(f"Scraping book with Selenium: {book_to_scrape['book']}")

                success = scraper.scrape_book(book_to_scrape)
                if success:
                    print(f"Successfully scraped {book_to_scrape['book']}")
                else:
                    print(f"Failed to completely scrape {book_to_scrape['book']}")

                print(scraper.get_performance_summary())

            except Exception as e:
                print(f"Error scraping book: {e}")
                sys.exit(1)
            return

        # Full scraping
        try:
            print("Starting Bible scraping with Selenium...")
            print(f"Testament filter: {args.testament or 'All'}")
            print(f"Delay range: {args.delay[0]}-{args.delay[1]} seconds")

            successful, total = scraper.scrape_all_books(args.testament)

            print(f"\n=== Scraping Completed ===")
            print(f"Successfully scraped: {successful}/{total} books")
            print(scraper.get_performance_summary())

        except KeyboardInterrupt:
            print("\nScraping interrupted by user")
            sys.exit(1)
        except Exception as e:
            print(f"Error during scraping: {e}")
            sys.exit(1)

    finally:
        if scraper:
            scraper.close()

if __name__ == "__main__":
    main()