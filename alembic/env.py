import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# Adicionado para carregar os modelos da sua aplicação
from app.db.base import Base
from app.db.models import Escola, Aluno, Professor # Garanta que todos os modelos estejam aqui

# Carrega a URL do banco de dados diretamente da variável de ambiente que a Render fornece
# Esta é a principal correção
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
# por exemplo:
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# outras opções podem ser configuradas aqui a partir do objeto config, como
# a URL do banco de dados, etc.
# Define a URL do banco de dados para o Alembic usar
config.set_main_option("sqlalchemy.url", database_url)


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
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
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_main_section, {}),
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