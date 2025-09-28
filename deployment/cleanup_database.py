#!/usr/bin/env python3
"""
Clean up database duplicates and consolidate data
"""

from models import DatabaseManager

def cleanup_database():
    """Remove duplicate books and consolidate data"""
    db_manager = DatabaseManager()

    with db_manager.get_connection() as conn:
        with conn.cursor() as cursor:
            print("=== CLEANING UP DATABASE ===")

            # Get all books with duplicates
            cursor.execute("""
                SELECT name, array_agg(id ORDER BY id) as book_ids
                FROM books
                GROUP BY name
                HAVING COUNT(*) > 1
            """)

            duplicates = cursor.fetchall()

            for book_name, book_ids in duplicates:
                print(f"\nProcessing {book_name} (IDs: {book_ids})")

                # Keep the first book ID, merge others into it
                main_book_id = book_ids[0]
                duplicate_ids = book_ids[1:]

                print(f"  Keeping book ID {main_book_id}, merging {duplicate_ids}")

                # Move all chapters from duplicate books to main book
                for dup_id in duplicate_ids:
                    # Update chapters to point to main book
                    cursor.execute("""
                        UPDATE chapters
                        SET book_id = %s
                        WHERE book_id = %s
                        AND chapter_number NOT IN (
                            SELECT chapter_number
                            FROM chapters
                            WHERE book_id = %s
                        )
                    """, (main_book_id, dup_id, main_book_id))

                    moved_chapters = cursor.rowcount
                    print(f"    Moved {moved_chapters} unique chapters from book {dup_id}")

                    # Delete remaining duplicate chapters
                    cursor.execute("DELETE FROM chapters WHERE book_id = %s", (dup_id,))
                    deleted_chapters = cursor.rowcount
                    print(f"    Deleted {deleted_chapters} duplicate chapters from book {dup_id}")

                    # Delete the duplicate book
                    cursor.execute("DELETE FROM books WHERE id = %s", (dup_id,))
                    print(f"    Deleted duplicate book {dup_id}")

            conn.commit()
            print("\n✓ Database cleanup completed!")

def check_final_stats():
    """Check final statistics"""
    db_manager = DatabaseManager()

    with db_manager.get_connection() as conn:
        with conn.cursor() as cursor:
            # Total counts
            cursor.execute("""
                SELECT
                    COUNT(DISTINCT b.id) as total_books,
                    COUNT(DISTINCT c.id) as total_chapters,
                    COUNT(v.id) as total_verses
                FROM books b
                LEFT JOIN chapters c ON b.id = c.book_id
                LEFT JOIN verses v ON c.id = v.chapter_id
            """)

            stats = cursor.fetchone()
            print(f"\n=== FINAL STATISTICS ===")
            print(f"Total Books: {stats[0]}")
            print(f"Total Chapters: {stats[1]}")
            print(f"Total Verses: {stats[2]}")

            # Check for incomplete books
            cursor.execute("""
                SELECT
                    b.name,
                    b.total_chapters as expected,
                    COUNT(DISTINCT c.chapter_number) as actual,
                    b.total_chapters - COUNT(DISTINCT c.chapter_number) as missing
                FROM books b
                LEFT JOIN chapters c ON b.id = c.book_id
                GROUP BY b.id, b.name, b.total_chapters
                HAVING COUNT(DISTINCT c.chapter_number) != b.total_chapters
                ORDER BY missing DESC
            """)

            incomplete = cursor.fetchall()

            if incomplete:
                print(f"\n=== INCOMPLETE BOOKS ===")
                for name, expected, actual, missing in incomplete:
                    print(f"{name}: {actual}/{expected} chapters ({missing} missing)")
            else:
                print(f"\n✓ All books complete!")

def main():
    cleanup_database()
    check_final_stats()

if __name__ == "__main__":
    main()