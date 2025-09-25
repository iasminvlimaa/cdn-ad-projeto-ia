#!/usr/bin/env bash
# Encerra o script se qualquer comando falhar
set -o errexit

# 1. Instala as dependências do Python
pip install -r requirements.txt

# 2. Roda as migrações para CRIAR as tabelas (escolas, alunos, etc.)
echo "Running database migrations..."
alembic upgrade head

# 3. Roda o script para POPULAR as tabelas com dados
echo "Populating the database..."
python populate_db.py