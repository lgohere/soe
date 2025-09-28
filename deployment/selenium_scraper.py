import time
import json
import logging
from typing import List, Dict, Tuple, Optional
from models import DatabaseManager, Book, Chapter, Verse
import random
import re
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup

class SeleniumBibleScraper:
    def __init__(self, delay_range: Tuple[float, float] = (1.0, 2.0)):
        self.delay_range = delay_range

        # Simple tracking
        self.request_count = 0
        self.start_time = datetime.now()
        self.success_count = 0
        self.errors_count = 0

        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('selenium_scraping.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

        # Database setup
        self.db_manager = DatabaseManager()
        self.book_model = Book(self.db_manager)
        self.chapter_model = Chapter(self.db_manager)
        self.verse_model = Verse(self.db_manager)

        # Initialize browser
        self.driver = None
        self.setup_browser()

    def setup_browser(self):
        """Setup Chrome browser with optimized options"""
        chrome_options = Options()

        # Optimize for speed and stealth
        chrome_options.add_argument("--headless")  # Run in background
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-images")  # Don't load images
        # chrome_options.add_argument("--disable-javascript")  # Keep JS enabled for dynamic content
        chrome_options.add_argument("--disable-plugins")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-background-timer-throttling")
        chrome_options.add_argument("--disable-renderer-backgrounding")
        chrome_options.add_argument("--disable-backgrounding-occluded-windows")

        # Random user agent rotation
        user_agents = [
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ]
        chrome_options.add_argument(f"--user-agent={random.choice(user_agents)}")

        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.set_page_load_timeout(15)
            self.driver.implicitly_wait(5)
            self.logger.info("Browser initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize browser: {e}")
            raise

    def simple_delay(self):
        """Simple delay between requests"""
        delay = random.uniform(*self.delay_range)
        time.sleep(delay)

    def get_page_content(self, url: str, retries: int = 3) -> Optional[BeautifulSoup]:
        """Get page content using Selenium with retry logic"""
        for attempt in range(retries):
            try:
                # Simple delay between requests
                self.simple_delay()

                self.logger.info(f"Loading: {url} (attempt {attempt + 1}/{retries})")
                self.request_count += 1

                # Check if browser is still alive
                try:
                    self.driver.current_url
                except Exception as browser_error:
                    self.logger.warning(f"Browser died, reinitializing: {browser_error}")
                    self.setup_browser()

                # Load the page
                self.driver.get(url)

                # Wait for main content to load
                WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located((By.TAG_NAME, "main"))
                )

                # Wait a bit more for content to fully render
                time.sleep(3)

                # Get page source and parse
                page_source = self.driver.page_source
                soup = BeautifulSoup(page_source, 'lxml')

                self.success_count += 1
                self.logger.info(f"✓ Page loaded successfully")

                return soup

            except Exception as e:
                self.errors_count += 1
                self.logger.warning(f"✗ Attempt {attempt + 1} failed for {url}: {e}")

                if attempt < retries - 1:
                    # Wait longer between retries
                    wait_time = (attempt + 1) * 5
                    self.logger.info(f"Waiting {wait_time}s before retry...")
                    time.sleep(wait_time)

                    # Try to recover the browser if needed
                    try:
                        self.driver.current_url
                    except:
                        self.logger.warning("Browser seems dead, reinitializing...")
                        try:
                            self.driver.quit()
                        except:
                            pass
                        self.setup_browser()

        self.logger.error(f"✗ FAILED to load {url} after {retries} attempts - SKIPPING")
        return None

    def parse_verses(self, soup: BeautifulSoup) -> List[Tuple[int, str]]:
        """Extract verses from the HTML content"""
        verses = []

        # Find the main content area
        main_content = soup.find('main')
        if not main_content:
            self.logger.warning("No main content found")
            return verses

        # Find all verse paragraphs
        verse_paragraphs = main_content.find_all('p', {'data-v': True})

        for p in verse_paragraphs:
            try:
                # Extract verse number
                verse_span = p.find('span', class_='v')
                if not verse_span:
                    continue

                verse_number_text = verse_span.get_text(strip=True)
                verse_number = int(re.sub(r'\D', '', verse_number_text))

                # Extract verse text
                text_span = p.find('span', class_='t')
                if not text_span:
                    continue

                verse_text = text_span.get_text(strip=True)

                if verse_text:
                    verses.append((verse_number, verse_text))

            except (ValueError, AttributeError) as e:
                self.logger.warning(f"Error parsing verse: {e}")
                continue

        # Sort verses by number to ensure correct order
        verses.sort(key=lambda x: x[0])

        self.logger.info(f"Extracted {len(verses)} verses")
        return verses

    def scrape_chapter(self, book_id: int, book_url: str, chapter_number: int) -> bool:
        """Scrape a single chapter"""
        chapter_url = f"{book_url}/{chapter_number}"

        soup = self.get_page_content(chapter_url)
        if not soup:
            return False

        verses = self.parse_verses(soup)
        if not verses:
            self.logger.warning(f"No verses found for {chapter_url}")
            return False

        # Insert or update chapter
        chapter_id = self.chapter_model.insert(book_id, chapter_number, len(verses))

        # Prepare verses data for batch insert
        verses_data = [(chapter_id, verse_num, text) for verse_num, text in verses]

        # Insert verses
        rows_affected = self.verse_model.insert_batch(verses_data)

        self.logger.info(f"Chapter {chapter_number}: {rows_affected} verses processed")
        return True

    def scrape_book(self, book_data: Dict) -> bool:
        """Scrape all chapters of a book"""
        book_name = book_data['book']
        book_url = book_data['url']
        total_chapters = book_data['chapters']

        # Determine testament
        bible_data = self.load_bible_data()
        testament = 'old_testament' if book_data in bible_data['old_testament'] else 'new_testament'

        self.logger.info(f"Starting to scrape: {book_name} ({total_chapters} chapters)")

        # Insert book into database
        book_id = self.book_model.insert(book_name, testament, book_url, total_chapters)

        success_count = 0

        for chapter_num in range(1, total_chapters + 1):
            try:
                if self.scrape_chapter(book_id, book_url, chapter_num):
                    success_count += 1
                else:
                    self.logger.error(f"Failed to scrape {book_name} chapter {chapter_num}")

            except Exception as e:
                self.logger.error(f"Error scraping {book_name} chapter {chapter_num}: {e}")
                continue

        self.logger.info(f"Completed {book_name}: {success_count}/{total_chapters} chapters scraped")
        return success_count == total_chapters

    def load_bible_data(self) -> Dict:
        """Load the bible books configuration"""
        for filename in ['bible_books.json', 'Biblia web-scrapping.json']:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    content = f.read()

                if filename.endswith('web-scrapping.json'):
                    json_content = content.strip()
                    if json_content.startswith('bible_books = '):
                        json_content = json_content[14:]
                    json_content = json_content.rstrip(';').strip()
                else:
                    json_content = content

                return json.loads(json_content)

            except (FileNotFoundError, json.JSONDecodeError) as e:
                if filename == 'bible_books.json':
                    continue
                else:
                    self.logger.error(f"Failed to load bible data: {e}")
                    raise

    def scrape_all_books(self, testament: Optional[str] = None):
        """Scrape all books or books from a specific testament"""
        bible_data = self.load_bible_data()

        books_to_scrape = []

        if testament == 'old_testament' or testament is None:
            books_to_scrape.extend(bible_data.get('old_testament', []))

        if testament == 'new_testament' or testament is None:
            books_to_scrape.extend(bible_data.get('new_testament', []))

        self.logger.info(f"Starting to scrape {len(books_to_scrape)} books with Selenium")

        successful_books = 0

        for book_data in books_to_scrape:
            try:
                if self.scrape_book(book_data):
                    successful_books += 1

                # Short break between books
                time.sleep(3)

            except Exception as e:
                self.logger.error(f"Error scraping book {book_data['book']}: {e}")
                continue

        self.logger.info(f"Scraping completed: {successful_books}/{len(books_to_scrape)} books successfully scraped")
        return successful_books, len(books_to_scrape)

    def get_performance_summary(self) -> str:
        """Get a summary of scraping performance"""
        if self.request_count == 0:
            return "No requests made yet"

        success_rate = (self.success_count / self.request_count) * 100
        error_rate = (self.errors_count / self.request_count) * 100
        elapsed_time = (datetime.now() - self.start_time).total_seconds()
        pages_per_minute = (self.request_count / elapsed_time) * 60 if elapsed_time > 0 else 0

        return f"""
=== Selenium Scraping Performance ===
Total Pages: {self.request_count}
Success Rate: {success_rate:.1f}%
Error Rate: {error_rate:.1f}%
Pages per Minute: {pages_per_minute:.1f}
Total Time: {elapsed_time/60:.1f} minutes
"""

    def close(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()
            self.logger.info("Browser closed")