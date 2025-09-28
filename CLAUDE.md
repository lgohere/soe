# Bible Web Scraping Project

## 📖 Descrição
Sistema completo de web scraping para extrair todos os versículos da Bíblia (ACF - Almeida Corrigida Fiel) do site bibliaonline.com.br e armazenar em banco PostgreSQL. Projeto base para desenvolvimento de API bíblica.

## 🎯 Status Atual
✅ **COMPLETO** - Todos os dados extraídos com sucesso!

### Dados Coletados:
- **66 livros** da Bíblia (39 AT + 27 NT)
- **1.189 capítulos** completos
- **31.106 versículos** extraídos
- **100% de cobertura** - nenhum livro incompleto

## 🏗️ Arquitetura

### Backend:
- **Python 3.11+**
- **FastAPI** (API REST)
- **PostgreSQL** (banco local)
- **Selenium WebDriver** (Chrome headless)
- **BeautifulSoup4** (parsing HTML)
- **psycopg2** (conexão PostgreSQL)

### Frontend:
- **Nuxt 3** (Vue.js)
- **TypeScript**
- **Tailwind CSS**
- **Server-Side Rendering (SSR)**

### Estrutura do Banco:
```sql
books (66 registros)
├── id, name, testament, url, total_chapters, created_at, biblical_order

chapters (1.189 registros)
├── id, book_id, chapter_number, total_verses, scraped_at

verses (31.106 registros)
├── id, chapter_id, verse_number, text, created_at

-- View consolidada:
bible_verses
├── book_name, testament, chapter_number, verse_number, verse_text
```

## 📁 Estrutura de Arquivos

```
biblia-webscrapping/
├── CLAUDE.md                    # Este arquivo
├── README.md                    # Documentação técnica
├── requirements.txt             # Dependências Python
├── .env                        # Configurações do banco
├──
├── # Configuração de dados
├── bible_books.json            # Configuração limpa dos livros
├── Biblia web-scrapping.json   # Configuração original
├──
├── # Scripts principais
├── selenium_scraper.py         # Scraper principal com Selenium
├── selenium_main.py            # CLI para scraping
├── models.py                   # Modelos do banco de dados
├──
├── # Scripts de apoio
├── recover_failed.py           # Recupera capítulos que falharam
├── cleanup_database.py         # Limpa duplicatas do banco
├── continue_from_mateus.py     # Continua scraping do NT
├── test_scraper.py            # Testes do sistema
├──
├── # Arquivos de banco
├── database_schema.sql         # Schema completo do PostgreSQL
├──
├── # Logs
├── selenium_scraping.log       # Logs detalhados do scraping
└── erro.txt                   # Log de erros processados
```

## 🚀 Como Usar

### Pré-requisitos:
```bash
# Instalar dependências
pip install -r requirements.txt

# PostgreSQL rodando com banco 'bibliasoe'
# Usuário 'soe' configurado no .env
```

### Comandos Principais:

```bash
# 1. Inicializar banco (primeira vez)
python selenium_main.py --init-db

# 2. Testar scraping com livro pequeno
python selenium_main.py --book "Judas"

# 3. Scraping completo (já realizado)
python selenium_main.py

# 4. Ver estatísticas
python selenium_main.py --stats

# 5. Recuperar capítulos que falharam
python recover_failed.py

# 6. Limpar duplicatas (já executado)
python cleanup_database.py
```

### Consultas Úteis:

```sql
-- Ver versículos de um capítulo
SELECT verse_number, verse_text
FROM bible_verses
WHERE book_name = 'Gênesis' AND chapter_number = 1;

-- Estatísticas gerais
SELECT testament, COUNT(DISTINCT book_name) as books,
       COUNT(DISTINCT concat(book_name, chapter_number)) as chapters,
       COUNT(*) as verses
FROM bible_verses
GROUP BY testament;

-- Buscar versículos por palavra
SELECT book_name, chapter_number, verse_number, verse_text
FROM bible_verses
WHERE verse_text ILIKE '%amor%'
LIMIT 10;
```

## 🔧 Configuração

### Banco de Dados (.env):
```env
DATABASE_URL=postgresql://soe:aleluia100%100@localhost:5432/bibliasoe
DB_HOST=localhost
DB_PORT=5432
DB_NAME=bibliasoe
DB_USER=soe
DB_PASSWORD=aleluia100%100
```

### Selenium (Otimizado):
- Chrome headless automático
- Delays inteligentes (1-2s)
- Retry com recuperação de browser
- Timeouts robustos (20s)
- Logs detalhados

## 📊 Performance

### Velocidade Atual:
- ~10-15 páginas/minuto
- ~3-4 segundos por capítulo
- Sistema robusto com retry automático

### Recursos do Sistema:
- Rate limiting respeitoso
- Recuperação automática de falhas
- Limpeza automática de duplicatas
- Logs completos para debug

## 🎯 Próximos Passos

### Para Deploy:
1. **Backup do banco:**
   ```bash
   pg_dump -U soe -d bibliasoe > biblia_backup.sql
   ```

2. **Docker para VPS:**
   - Criar Dockerfile da API
   - docker-compose com PostgreSQL
   - Restaurar dados no container

3. **API Development:**
   - Endpoints REST para livros/capítulos/versículos
   - Sistema de busca
   - Paginação
   - Cache

### Melhorias Futuras:
- [ ] API REST completa
- [ ] Sistema de busca avançada
- [ ] Cache Redis
- [ ] Rate limiting na API
- [ ] Documentação Swagger
- [ ] Frontend web

## 🛠️ Comandos Úteis

```bash
# Verificar dados no banco
python -c "from models import *; db = DatabaseManager();
cursor = db.execute_query('SELECT COUNT(*) FROM bible_verses', fetch=True);
print(f'Total verses: {cursor[0][\"count\"]}')"

# Backup rápido
pg_dump -U soe -d bibliasoe --no-owner --no-privileges > backup_$(date +%Y%m%d).sql

# Restaurar em outro banco
psql -U usuario -d novo_banco < backup_file.sql
```

## 📝 Logs e Debug

### Logs Importantes:
- `selenium_scraping.log` - Logs completos do scraping
- `erro.txt` - Erros processados e recuperados

### Monitoramento:
```bash
# Ver progresso em tempo real
tail -f selenium_scraping.log

# Verificar últimos erros
grep "ERROR" selenium_scraping.log | tail -10
```

## ✅ Validação dos Dados

### Testes Realizados:
- ✅ Todos os 66 livros coletados
- ✅ Numeração sequencial de versículos
- ✅ Textos completos e legíveis
- ✅ Estrutura consistente
- ✅ Zero duplicatas após limpeza
- ✅ Encoding UTF-8 correto

### Exemplo de Dados:
```
Gênesis 1:1 → "No princípio criou Deus os céus e a terra."
João 3:16 → "Porque Deus amou o mundo de tal maneira..."
Apocalipse 22:21 → "A graça de nosso Senhor Jesus Cristo..."
```

---

**Status: PRODUÇÃO READY** 🚀
**Última atualização:** Setembro 2024
**Dados coletados:** 100% completos