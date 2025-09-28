import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
import os
from dotenv import load_dotenv
from typing import List, Dict, Optional, Tuple
import logging

load_dotenv()

class DatabaseManager:
    def __init__(self):
        self.connection_params = {
            'host': os.getenv('DB_HOST'),
            'port': os.getenv('DB_PORT'),
            'database': os.getenv('DB_NAME'),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD')
        }
        self.logger = logging.getLogger(__name__)

    @contextmanager
    def get_connection(self):
        conn = None
        try:
            conn = psycopg2.connect(**self.connection_params)
            yield conn
        except Exception as e:
            if conn:
                conn.rollback()
            self.logger.error(f"Database connection error: {e}")
            raise
        finally:
            if conn:
                conn.close()

    def execute_query(self, query: str, params: tuple = None, fetch: bool = False):
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, params)
                if fetch:
                    return cursor.fetchall()
                conn.commit()
                return cursor.rowcount

class Book:
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager

    def insert(self, name: str, testament: str, url: str, total_chapters: int) -> int:
        query = """
        INSERT INTO books (name, testament, url, total_chapters)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT DO NOTHING
        RETURNING id
        """
        with self.db.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (name, testament, url, total_chapters))
                result = cursor.fetchone()
                conn.commit()
                if result:
                    return result[0]
                else:
                    # Book already exists, get its ID
                    cursor.execute("SELECT id FROM books WHERE name = %s AND testament = %s", (name, testament))
                    return cursor.fetchone()[0]

    def get_all(self) -> List[Dict]:
        query = "SELECT * FROM books ORDER BY biblical_order"
        return self.db.execute_query(query, fetch=True)

    def get_by_id(self, book_id: int) -> Optional[Dict]:
        query = "SELECT * FROM books WHERE id = %s"
        result = self.db.execute_query(query, (book_id,), fetch=True)
        return result[0] if result else None

class Chapter:
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager

    def insert(self, book_id: int, chapter_number: int, total_verses: int = None) -> int:
        query = """
        INSERT INTO chapters (book_id, chapter_number, total_verses)
        VALUES (%s, %s, %s)
        ON CONFLICT (book_id, chapter_number)
        DO UPDATE SET
            total_verses = EXCLUDED.total_verses,
            updated_at = CURRENT_TIMESTAMP
        RETURNING id
        """
        with self.db.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (book_id, chapter_number, total_verses))
                result = cursor.fetchone()
                conn.commit()
                return result[0]

    def get_by_book_and_chapter(self, book_id: int, chapter_number: int) -> Optional[Dict]:
        query = "SELECT * FROM chapters WHERE book_id = %s AND chapter_number = %s"
        result = self.db.execute_query(query, (book_id, chapter_number), fetch=True)
        return result[0] if result else None

class Verse:
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager

    def insert_batch(self, verses_data: List[Tuple[int, int, str]]) -> int:
        query = """
        INSERT INTO verses (chapter_id, verse_number, text)
        VALUES (%s, %s, %s)
        ON CONFLICT (chapter_id, verse_number)
        DO UPDATE SET
            text = EXCLUDED.text,
            updated_at = CURRENT_TIMESTAMP
        """
        with self.db.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.executemany(query, verses_data)
                conn.commit()
                return cursor.rowcount

    def get_by_chapter(self, chapter_id: int) -> List[Dict]:
        query = "SELECT * FROM verses WHERE chapter_id = %s ORDER BY verse_number"
        return self.db.execute_query(query, (chapter_id,), fetch=True)

    def count_by_chapter(self, chapter_id: int) -> int:
        query = "SELECT COUNT(*) FROM verses WHERE chapter_id = %s"
        result = self.db.execute_query(query, (chapter_id,), fetch=True)
        return result[0]['count'] if result else 0