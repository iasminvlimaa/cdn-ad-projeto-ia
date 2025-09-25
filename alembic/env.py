import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# Adicionado para carregar os modelos da sua aplicação
from app.db.base import Base
# A linha abaixo é importante para que o Alembic "veja" seus modelos
from app.db import models

# Carrega a URL do banco de dados diretamente da variável de ambiente que a Render fornece
database_url = os.getenv("DATABASE_URL")
if not database_url:
    # Para desenvolvimento local, podemos tentar pegar de um arquivo .env
    from dotenv import load_dotenv
    load_dotenv()
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("A variável de ambiente DATABASE_URL não está configurada.")

# esta é a configuração do Alembic, que fornece acesso aos valores
# do arquivo .ini em uso.
config = context.config

# Interprete o arquivo de configuração para o logging do Python.
# Esta linha basicamente configura os loggers.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# adicione aqui o objeto MetaData do seu modelo para o suporte a 'autogenerate'
target_metadata = Base.metadata

# Define a URL do banco de dados para o Alembic usar
config.set_main_option("sqlalchemy.url", database_url)


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    # CORREÇÃO AQUI: trocamos config.config_main_section por config.config_ini_section
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()