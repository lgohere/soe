#!/bin/bash

# Script para backup do banco PostgreSQL local antes do deploy
# Execute este script antes de fazer o deploy no Coolify

set -e

# Configurações do banco local
DB_HOST="localhost"
DB_PORT="5432"
DB_NAME="bibliasoe"
DB_USER="soe"

# Data e hora para o nome do arquivo
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_DIR="./database_backups"
BACKUP_FILE="$BACKUP_DIR/biblia_backup_$TIMESTAMP.sql"

# Criar diretório de backup se não existir
mkdir -p "$BACKUP_DIR"

echo "🗃️  Iniciando backup do banco de dados..."
echo "📂 Banco: $DB_NAME"
echo "💾 Arquivo: $BACKUP_FILE"

# Realizar backup usando pg_dump
PGPASSWORD="aleluia100%100" pg_dump \
    -h "$DB_HOST" \
    -p "$DB_PORT" \
    -U "$DB_USER" \
    -d "$DB_NAME" \
    --no-owner \
    --no-privileges \
    --clean \
    --if-exists \
    > "$BACKUP_FILE"

if [ $? -eq 0 ]; then
    echo "✅ Backup realizado com sucesso!"
    echo "📄 Arquivo: $BACKUP_FILE"
    echo "📊 Tamanho: $(du -h "$BACKUP_FILE" | cut -f1)"

    # Mostrar estatísticas do backup
    echo ""
    echo "📈 Estatísticas do backup:"
    grep -c "INSERT INTO books" "$BACKUP_FILE" && echo "   Livros exportados" || echo "   0 livros encontrados"
    grep -c "INSERT INTO chapters" "$BACKUP_FILE" && echo "   Capítulos exportados" || echo "   0 capítulos encontrados"
    grep -c "INSERT INTO verses" "$BACKUP_FILE" && echo "   Versículos exportados" || echo "   0 versículos encontrados"

    echo ""
    echo "🚀 Para restaurar no Coolify, use este arquivo no container PostgreSQL:"
    echo "   docker exec -i biblia-db psql -U soe -d bibliasoe < $BACKUP_FILE"
    echo ""
    echo "💡 Ou copie o arquivo para o container e execute:"
    echo "   docker cp $BACKUP_FILE biblia-db:/tmp/"
    echo "   docker exec biblia-db psql -U soe -d bibliasoe -f /tmp/$(basename "$BACKUP_FILE")"

else
    echo "❌ Erro durante o backup!"
    exit 1
fi