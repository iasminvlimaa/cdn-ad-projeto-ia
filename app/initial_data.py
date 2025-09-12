import logging
import os
from sqlalchemy import text
from alembic.config import Config
from alembic import command
from app.db.session import SessionLocal
from app.core.config import settings # <-- 1. Importar as configurações
from scripts.populate_db import populate_database

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

LOCK_FILE = "/tmp/db_init.lock"

def run_migrations():
    """Aplica as migrações do Alembic de forma programática."""
    logger.info("Iniciando migrações do banco de dados de forma programática...")
    try:
        # Cria uma configuração do Alembic em código, ignorando o arquivo .ini
        alembic_cfg = Config()
        alembic_cfg.set_main_option("script_location", "alembic")
        
        # Define a URL do banco de dados diretamente das nossas configurações
        # Esta é a correção principal
        alembic_cfg.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

        logger.info("Configuração do Alembic criada. Aplicando migrações (upgrade head)...")
        command.upgrade(alembic_cfg, "head")
        logger.info("Migrações aplicadas com sucesso.")
    except Exception as e:
        logger.error(f"Erro ao aplicar migrações: {e}")
        raise

def check_and_populate_data():
    # ... (esta função continua exatamente a mesma da versão anterior)
    db = SessionLocal()
    try:
        result = db.execute(text("SELECT COUNT(id) FROM escolas;")).scalar_one_or_none()
        if result is not None and result > 0:
            logger.info("O banco de dados já está populado.")
            return
        logger.info("O banco de dados está vazio. Iniciando script de população...")
        populate_database()
        logger.info("População do banco de dados concluída.")
    except Exception as e:
        if "relation \"escolas\" does not exist" in str(e).lower():
            logger.warning("Tabela 'escolas' não encontrada, populando pela primeira vez...")
            populate_database()
            logger.info("População do banco de dados concluída.")
        else:
            logger.error(f"Erro ao verificar ou popular o banco: {e}")
    finally:
        db.close()

def init_db():
    if os.path.exists(LOCK_FILE):
        logger.info("Lock file encontrado. A inicialização do banco de dados já foi executada.")
        return

    logger.info("Iniciando processo de inicialização do banco de dados...")
    
    run_migrations()
    check_and_populate_data()
    
    with open(LOCK_FILE, "w") as f:
        f.write("completed")
    
    logger.info("Processo de inicialização do banco de dados finalizado. Lock file criado.")