import logging
from sqlalchemy import text
from alembic.config import Config
from alembic import command
from app.db.session import SessionLocal
# Importamos a função do nosso script de população
from scripts.populate_db import populate_database

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_migrations():
    """Aplica as migrações do Alembic."""
    try:
        logger.info("Procurando por configurações do Alembic...")
        # Carrega a configuração do alembic.ini
        alembic_cfg = Config("alembic.ini")
        logger.info("Configuração encontrada. Aplicando migrações (upgrade head)...")
        # Executa o comando 'alembic upgrade head'
        command.upgrade(alembic_cfg, "head")
        logger.info("Migrações aplicadas com sucesso.")
    except Exception as e:
        logger.error(f"Erro ao aplicar migrações: {e}")
        raise

def check_and_populate_data():
    """Verifica se o banco de dados está vazio e o popula se necessário."""
    db = SessionLocal()
    try:
        # Verifica se a tabela 'escolas' já tem algum dado
        result = db.execute(text("SELECT COUNT(id) FROM escolas;")).scalar_one_or_none()
        
        if result is not None and result > 0:
            logger.info("O banco de dados já está populado. Nenhuma ação necessária.")
            return

        logger.info("O banco de dados está vazio. Iniciando o script de população...")
        # Chama a função do nosso script original para popular o banco
        populate_database()
        logger.info("População do banco de dados concluída.")

    except Exception as e:
        # A exceção pode acontecer se a tabela 'escolas' nem existir ainda
        if "relation \"escolas\" does not exist" in str(e).lower():
            logger.warning("Tabela 'escolas' não encontrada, o que é esperado na primeira execução.")
            logger.info("Iniciando o script de população...")
            populate_database()
            logger.info("População do banco de dados concluída.")
        else:
            logger.error(f"Erro ao verificar ou popular o banco: {e}")
    finally:
        db.close()

def init_db():
    logger.info("Iniciando processo de inicialização do banco de dados...")
    # 1. Aplica as migrações para garantir que as tabelas existam
    run_migrations()
    # 2. Verifica se precisa popular os dados e o faz se necessário
    check_and_populate_data()
    logger.info("Processo de inicialização do banco de dados finalizado.")