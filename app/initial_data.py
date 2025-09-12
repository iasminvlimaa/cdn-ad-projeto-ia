import logging
import os # <-- Importar
from sqlalchemy import text
from alembic.config import Config
from alembic import command
from app.db.session import SessionLocal
from scripts.populate_db import populate_database

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- LÓGICA DE TRAVAMENTO (LOCK) ---
# O Render usa um sistema de arquivos temporário. Usaremos isso a nosso favor.
LOCK_FILE = "/tmp/db_init.lock"

def init_db():
    # Se o arquivo de lock já existe, significa que o processo já rodou.
    if os.path.exists(LOCK_FILE):
        logger.info("Lock file encontrado. A inicialização do banco de dados já foi executada.")
        return

    logger.info("Iniciando processo de inicialização do banco de dados...")
    
    # 1. Aplica as migrações para garantir que as tabelas existam
    try:
        alembic_cfg = Config("alembic.ini")
        command.upgrade(alembic_cfg, "head")
        logger.info("Migrações aplicadas com sucesso.")
    except Exception as e:
        logger.error(f"Erro ao aplicar migrações: {e}")
        # Se a migração falhar, não continuamos e não criamos o lock file.
        return 

    # 2. Verifica se precisa popular os dados
    db = SessionLocal()
    try:
        result = db.execute(text("SELECT COUNT(id) FROM escolas;")).scalar_one_or_none()
        if result is not None and result > 0:
            logger.info("O banco de dados já está populado.")
        else:
            logger.info("O banco de dados está vazio. Iniciando script de população...")
            populate_database()
            logger.info("População do banco de dados concluída.")
    except Exception:
        logger.info("Tabela 'escolas' não encontrada. Populando pela primeira vez...")
        populate_database()
        logger.info("População do banco de dados concluída.")
    finally:
        db.close()

    # 3. Cria o arquivo de lock para evitar futuras execuções
    with open(LOCK_FILE, "w") as f:
        f.write("completed")
    
    logger.info("Processo de inicialização do banco de dados finalizado. Lock file criado.")