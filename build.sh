#!/usr/bin/env bash
# exit on error
set -o errexit

# 1. Instala as dependências
pip install -r requirements.txt

# 2. Aplica as migrações do banco (cria as tabelas)
alembic upgrade head

# 3. POPULA O BANCO DE DADOS (APENAS DESTA VEZ)
echo "Iniciando a população do banco de dados..."
python populate_db.py