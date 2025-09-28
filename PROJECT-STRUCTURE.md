# 📁 Estrutura de Projeto Recomendada

## Estrutura Final Desejada:
```
biblia-app/
├── backend/                     # FastAPI
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py             # FastAPI app
│   │   ├── core/
│   │   │   ├── config.py       # Settings
│   │   │   ├── database.py     # DB connection
│   │   │   └── security.py     # Auth (futuro)
│   │   ├── api/
│   │   │   ├── v1/
│   │   │   │   ├── endpoints/
│   │   │   │   │   ├── books.py
│   │   │   │   │   ├── chapters.py
│   │   │   │   │   ├── verses.py
│   │   │   │   │   └── search.py
│   │   │   │   └── api.py      # Router principal
│   │   │   └── deps.py         # Dependencies
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── book.py         # SQLAlchemy models
│   │   │   ├── chapter.py
│   │   │   └── verse.py
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── book.py         # Pydantic schemas
│   │   │   ├── chapter.py
│   │   │   └── verse.py
│   │   └── services/
│   │       ├── __init__.py
│   │       ├── book_service.py
│   │       └── search_service.py
│   ├── alembic/                # Migrations
│   ├── requirements.txt
│   ├── .env.example
│   └── Dockerfile
│
├── frontend/                   # Nuxt 3
│   ├── components/
│   │   ├── Bible/
│   │   ├── Navigation/
│   │   └── UI/
│   ├── composables/
│   ├── layouts/
│   ├── pages/
│   ├── stores/                # Pinia
│   ├── plugins/
│   ├── server/
│   ├── public/
│   ├── package.json
│   ├── nuxt.config.ts
│   └── Dockerfile
│
├── scripts/                   # Utilitários
│   ├── scraping/
│   │   ├── selenium_scraper.py
│   │   ├── recover_failed.py
│   │   └── cleanup_database.py
│   ├── data/
│   │   ├── bible_books.json
│   │   └── database_schema.sql
│   └── logs/
│       ├── selenium_scraping.log
│       └── erro.txt
│
├── docker-compose.yml          # Development
├── docker-compose.prod.yml     # Production
├── .env.example
├── .gitignore
├── README.md
├── CLAUDE.md                   # Current system docs
├── stack.md                    # Architecture decisions
└── TASK-MASTER.md             # Development checklist
```

## Migração dos Arquivos Atuais:

### Backend Core:
- `models.py` → `backend/app/models/`
- `.env` → `backend/.env`
- `requirements.txt` → `backend/requirements.txt`

### Scripts de Scraping:
- `selenium_scraper.py` → `scripts/scraping/`
- `recover_failed.py` → `scripts/scraping/`
- `cleanup_database.py` → `scripts/scraping/`
- `continue_from_mateus.py` → `scripts/scraping/`

### Data Files:
- `bible_books.json` → `scripts/data/`
- `database_schema.sql` → `scripts/data/`

### Logs:
- `*.log`, `erro.txt` → `scripts/logs/`

### Documentation:
- Manter na raiz: `README.md`, `CLAUDE.md`, `stack.md`, `TASK-MASTER.md`

### Arquivos Obsoletos:
- `scraper.py` (versão antiga)
- `main.py` (será recriado)
- `test_scraper.py` (será recriado)
- `setup.py` (não necessário)
- `Dockerfile` (será movido)