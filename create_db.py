import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
import logging

# Adicione os imports do seu projeto
from app.db.base import Base 
from app.db.models import Escola, Aluno, Professor # Garante que os modelos sejam carregados

logging.basicConfig(level=logging.INFO, format='%(levelname)-5.5s [%(name)s] %(message)s')

if __name__ == "__main__":
    load_dotenv()
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        logging.error("URL do banco de dados não encontrada. Verifique seu arquivo .env")
    else:
        logging.info("Criando as tabelas no banco de dados...")
        engine = create_engine(DATABASE_URL)
        # Isso cria todas as tabelas definidas em Base.metadata
        Base.metadata.create_all(bind=engine) 
        logging.info("Tabelas criadas com sucesso!")