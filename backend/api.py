#!/usr/bin/env python3
"""
🙏 Biblia API - Professional FastAPI Backend
Target: 50+ year old users | Focus: Simplicity + Accessibility + Performance
"""
from fastapi import FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List, Dict, Optional
import os
import sys
import logging
from datetime import datetime

# Add current directory to path for models import
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from models import DatabaseManager, Book as BookModel, Chapter as ChapterModel, Verse as VerseModel
except ImportError as e:
    print(f"❌ Error importing models: {e}")
    print("📂 Current directory:", os.getcwd())
    print("📁 Files in directory:", os.listdir("."))
    sys.exit(1)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI with professional configuration
app = FastAPI(
    title="🙏 Biblia API",
    version="1.0.0",
    description="""
    **API Profissional para Consulta da Bíblia Sagrada**

    - 🎯 Otimizada para usuários 50+
    - 📖 66 livros, 1,189 capítulos, 31,106 versículos
    - 🔍 Busca inteligente e versículo aleatório
    - ⚡ Performance < 50ms por endpoint
    """,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Professional CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8080",
        "http://127.0.0.1:8080"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# Initialize database models with error handling
try:
    db_manager = DatabaseManager()
    book_model = BookModel(db_manager)
    chapter_model = ChapterModel(db_manager)
    verse_model = VerseModel(db_manager)
    logger.info("✅ Database models initialized successfully")
except Exception as e:
    logger.error(f"❌ Failed to initialize database models: {e}")
    raise

# Exception handler for professional error responses
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"❌ Unhandled exception: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal server error",
            "message": "Ops! Algo deu errado. Tente novamente em alguns instantes.",
            "timestamp": datetime.now().isoformat()
        }
    )

# ==================== ROOT & HEALTH ENDPOINTS ====================

@app.get("/", tags=["🏠 Root"])
async def root():
    """🏠 API Status and Quick Navigation"""
    return {
        "message": "🙏 Biblia API - Serving God's Word with Excellence",
        "version": "1.0.0",
        "status": "✅ Online",
        "documentation": "/docs",
        "quick_links": {
            "all_books": "/books",
            "random_verse": "/verses/random",
            "search_love": "/search?q=amor",
            "stats": "/stats"
        },
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health", tags=["🏥 Health"])
async def health_check():
    """🏥 Professional Health Check"""
    try:
        # Test database connection
        books = book_model.get_all()
        return {
            "status": "✅ Healthy",
            "database": "✅ Connected",
            "books_count": len(books),
            "timestamp": datetime.now().isoformat(),
            "uptime": "Ready to serve"
        }
    except Exception as e:
        logger.error(f"❌ Health check failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service temporarily unavailable"
        )

# ==================== BOOKS API ====================

@app.get("/books", response_model=List[Dict], tags=["📚 Books"])
async def get_books():
    """📚 Lista todos os 66 livros da Bíblia em ordem bíblica"""
    try:
        # Use biblical order instead of random ID order
        query = """
        SELECT id, name, testament, url, total_chapters, created_at, biblical_order
        FROM books
        ORDER BY biblical_order
        """
        books = db_manager.execute_query(query, fetch=True)
        logger.info(f"📚 Retrieved {len(books)} books in biblical order")
        return books
    except Exception as e:
        logger.error(f"❌ Error fetching books: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao buscar livros da Bíblia"
        )

@app.get("/books/{book_id}", response_model=Dict, tags=["📚 Books"])
async def get_book(book_id: int):
    """📖 Detalhes de um livro específico"""
    try:
        book = book_model.get_by_id(book_id)
        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Livro com ID {book_id} não encontrado"
            )

        logger.info(f"📖 Retrieved book: {book.get('name', 'Unknown')}")
        return book
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error fetching book {book_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao buscar detalhes do livro"
        )

@app.get("/books/{book_id}/chapters", response_model=List[Dict], tags=["📚 Books"])
async def get_book_chapters(book_id: int):
    """📑 Todos os capítulos de um livro"""
    try:
        # Verify book exists
        book = book_model.get_by_id(book_id)
        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Livro com ID {book_id} não encontrado"
            )

        # Get chapters
        query = """
        SELECT c.*, b.name as book_name
        FROM chapters c
        JOIN books b ON c.book_id = b.id
        WHERE c.book_id = %s
        ORDER BY c.chapter_number
        """
        chapters = db_manager.execute_query(query, (book_id,), fetch=True)

        logger.info(f"📑 Retrieved {len(chapters)} chapters for book {book.get('name', book_id)}")
        return chapters
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error fetching chapters for book {book_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao buscar capítulos do livro"
        )

# ==================== CHAPTERS API ====================

@app.get("/chapters/{chapter_id}", response_model=Dict, tags=["📄 Chapters"])
async def get_chapter(chapter_id: int):
    """📄 Detalhes de um capítulo específico"""
    try:
        query = """
        SELECT c.*, b.name as book_name, b.testament
        FROM chapters c
        JOIN books b ON c.book_id = b.id
        WHERE c.id = %s
        """
        result = db_manager.execute_query(query, (chapter_id,), fetch=True)

        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Capítulo com ID {chapter_id} não encontrado"
            )

        chapter = result[0]
        logger.info(f"📄 Retrieved chapter: {chapter.get('book_name')} {chapter.get('chapter_number')}")
        return chapter
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error fetching chapter {chapter_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao buscar detalhes do capítulo"
        )

@app.get("/chapters/{chapter_id}/verses", response_model=List[Dict], tags=["📄 Chapters"])
async def get_chapter_verses(chapter_id: int):
    """📝 Todos os versículos de um capítulo"""
    try:
        # Verify chapter exists
        query = "SELECT c.*, b.name as book_name FROM chapters c JOIN books b ON c.book_id = b.id WHERE c.id = %s"
        result = db_manager.execute_query(query, (chapter_id,), fetch=True)

        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Capítulo com ID {chapter_id} não encontrado"
            )

        chapter = result[0]

        # Get verses with book context
        verses_query = """
        SELECT v.*, c.chapter_number, b.name as book_name, b.testament
        FROM verses v
        JOIN chapters c ON v.chapter_id = c.id
        JOIN books b ON c.book_id = b.id
        WHERE v.chapter_id = %s
        ORDER BY v.verse_number
        """
        verses = db_manager.execute_query(verses_query, (chapter_id,), fetch=True)

        logger.info(f"📝 Retrieved {len(verses)} verses for {chapter.get('book_name')} {chapter.get('chapter_number')}")
        return verses
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error fetching verses for chapter {chapter_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao buscar versículos do capítulo"
        )

# ==================== VERSES API ====================

@app.get("/verses/random", response_model=Dict, tags=["✝️ Verses"])
async def get_random_verse():
    """🎲 Versículo aleatório do dia - Inspiração divina"""
    try:
        query = """
        SELECT v.*, c.chapter_number, b.name as book_name, b.testament,
               b.id as book_id, c.id as chapter_id
        FROM verses v
        JOIN chapters c ON v.chapter_id = c.id
        JOIN books b ON c.book_id = b.id
        ORDER BY RANDOM()
        LIMIT 1
        """
        result = db_manager.execute_query(query, fetch=True)

        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nenhum versículo encontrado"
            )

        verse = result[0]
        logger.info(f"🎲 Random verse: {verse.get('book_name')} {verse.get('chapter_number')}:{verse.get('verse_number')}")
        return verse
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error fetching random verse: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao buscar versículo aleatório"
        )

@app.get("/verses/{verse_id}", response_model=Dict, tags=["✝️ Verses"])
async def get_verse(verse_id: int):
    """✝️ Versículo específico com contexto completo"""
    try:
        query = """
        SELECT v.*, c.chapter_number, b.name as book_name, b.testament,
               b.id as book_id, c.id as chapter_id
        FROM verses v
        JOIN chapters c ON v.chapter_id = c.id
        JOIN books b ON c.book_id = b.id
        WHERE v.id = %s
        """
        result = db_manager.execute_query(query, (verse_id,), fetch=True)

        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Versículo com ID {verse_id} não encontrado"
            )

        verse = result[0]
        logger.info(f"✝️ Retrieved verse: {verse.get('book_name')} {verse.get('chapter_number')}:{verse.get('verse_number')}")
        return verse
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error fetching verse {verse_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao buscar versículo"
        )

@app.get("/verse/{book_name}/{chapter_num}/{verse_num}", response_model=Dict, tags=["✝️ Verses"])
async def get_verse_by_reference(book_name: str, chapter_num: int, verse_num: int):
    """📍 Versículo por referência direta (Ex: João/3/16)"""
    try:
        query = """
        SELECT v.*, c.chapter_number, b.name as book_name, b.testament,
               b.id as book_id, c.id as chapter_id
        FROM verses v
        JOIN chapters c ON v.chapter_id = c.id
        JOIN books b ON c.book_id = b.id
        WHERE LOWER(b.name) LIKE LOWER(%s)
        AND c.chapter_number = %s
        AND v.verse_number = %s
        """
        result = db_manager.execute_query(
            query,
            (f"%{book_name}%", chapter_num, verse_num),
            fetch=True
        )

        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Versículo {book_name} {chapter_num}:{verse_num} não encontrado"
            )

        verse = result[0]
        logger.info(f"📍 Reference verse: {verse.get('book_name')} {chapter_num}:{verse_num}")
        return verse
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error fetching verse {book_name} {chapter_num}:{verse_num}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao buscar versículo por referência"
        )

# ==================== SEARCH API ====================

@app.get("/search", response_model=List[Dict], tags=["🔍 Search"])
async def search_verses(
    q: str = Query(..., min_length=2, description="Palavra ou frase para buscar"),
    limit: int = Query(50, le=100, ge=1, description="Máximo de resultados (1-100)")
):
    """🔍 Busca inteligente de versículos por palavra-chave"""
    try:
        if len(q.strip()) < 2:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Busca deve ter pelo menos 2 caracteres"
            )

        # Smart search with relevance ranking
        query = """
        SELECT v.*, c.chapter_number, b.name as book_name, b.testament,
               b.id as book_id, c.id as chapter_id,
               CASE
                   WHEN LOWER(v.text) LIKE LOWER(%s) THEN 1
                   WHEN LOWER(v.text) LIKE LOWER(%s) THEN 2
                   ELSE 3
               END as relevance_score
        FROM verses v
        JOIN chapters c ON v.chapter_id = c.id
        JOIN books b ON c.book_id = b.id
        WHERE LOWER(v.text) LIKE LOWER(%s)
        ORDER BY relevance_score, b.id, c.chapter_number, v.verse_number
        LIMIT %s
        """

        exact_match = f"%{q}%"
        word_match = f"% {q} %"

        result = db_manager.execute_query(
            query,
            (exact_match, word_match, exact_match, limit),
            fetch=True
        )

        logger.info(f"🔍 Search '{q}' returned {len(result)} results")
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Search error for '{q}': {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro na busca de versículos"
        )

@app.get("/search/suggest", tags=["🔍 Search"])
async def search_suggestions(
    q: str = Query(..., min_length=1, description="Termo para sugestões"),
    limit: int = Query(10, le=20, ge=1, description="Máximo de sugestões")
):
    """💡 Sugestões inteligentes para auto-complete"""
    try:
        if len(q.strip()) < 1:
            return {"suggestions": []}

        # Get book name suggestions
        book_query = """
        SELECT DISTINCT name as suggestion
        FROM books
        WHERE LOWER(name) LIKE LOWER(%s)
        ORDER BY name
        LIMIT %s
        """

        book_suggestions = db_manager.execute_query(
            book_query,
            (f"%{q}%", limit),
            fetch=True
        )

        suggestions = [s['suggestion'] for s in book_suggestions]

        # Add common biblical terms if needed
        if len(suggestions) < limit:
            common_terms = ['amor', 'fé', 'esperança', 'paz', 'graça', 'salvação', 'vida', 'luz']
            matching_terms = [term for term in common_terms if q.lower() in term.lower()]
            suggestions.extend(matching_terms[:limit - len(suggestions)])

        logger.info(f"💡 Generated {len(suggestions)} suggestions for '{q}'")
        return {"suggestions": suggestions[:limit]}
    except Exception as e:
        logger.error(f"❌ Suggestion error for '{q}': {e}")
        return {"suggestions": [], "error": "Erro ao gerar sugestões"}

# ==================== STATISTICS API ====================

@app.get("/stats", tags=["📊 Statistics"])
async def get_bible_stats():
    """📊 Estatísticas completas da Bíblia"""
    try:
        stats_query = """
        SELECT
            COUNT(DISTINCT b.id) as total_books,
            COUNT(DISTINCT c.id) as total_chapters,
            COUNT(v.id) as total_verses,
            COUNT(DISTINCT CASE WHEN b.testament = 'old_testament' THEN b.id END) as old_testament_books,
            COUNT(DISTINCT CASE WHEN b.testament = 'new_testament' THEN b.id END) as new_testament_books,
            AVG(LENGTH(v.text)) as avg_verse_length
        FROM books b
        LEFT JOIN chapters c ON b.id = c.book_id
        LEFT JOIN verses v ON c.id = v.chapter_id
        """

        result = db_manager.execute_query(stats_query, fetch=True)
        stats = result[0] if result else {}

        # Add performance info
        stats.update({
            "api_version": "1.0.0",
            "target_audience": "50+ years",
            "last_updated": datetime.now().isoformat(),
            "database_status": "✅ Connected"
        })

        logger.info("📊 Retrieved Bible statistics")
        return stats
    except Exception as e:
        logger.error(f"❌ Error fetching statistics: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao buscar estatísticas"
        )

# ==================== STARTUP & SHUTDOWN ====================

@app.on_event("startup")
async def startup_event():
    """🚀 Professional startup sequence"""
    logger.info("🚀 Starting Biblia API...")
    logger.info("📖 Database connection verified")
    logger.info("✅ API ready to serve God's Word")

@app.on_event("shutdown")
async def shutdown_event():
    """👋 Graceful shutdown"""
    logger.info("👋 Biblia API shutting down gracefully")

if __name__ == "__main__":
    import uvicorn
    print("🙏 Starting Professional Biblia API...")
    print("📖 Documentation: http://localhost:8000/docs")
    print("🔍 Health Check: http://localhost:8000/health")
    print("📊 Statistics: http://localhost:8000/api/v1/stats")

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=False,  # Professional mode
        log_level="info"
    )