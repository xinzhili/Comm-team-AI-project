import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config, text
from sqlalchemy import pool

from alembic import context
from sqlalchemy.ext.asyncio import create_async_engine

from models.base import Base
from models.user import User
from models.chat_session import ChatSession

from dotenv import load_dotenv
load_dotenv()

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

database_url = os.getenv("DATABASE_URL")
database_name = os.getenv("DATABASE_NAME")

def include_name(name, type_, parent_names):
    if type_ == "schema":
        return name in ["testing"]
    else:
        return True

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    context.configure(
        url=database_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        version_table_schemas="testing",
        include_schemas=True,
        include_name=include_name
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    database_url_postgres = database_url.replace(f"/{database_name}", '/postgres')
    connectable_postgres_engine = create_async_engine(
        url=database_url_postgres,
        isolation_level='AUTOCOMMIT'
    )

    async with connectable_postgres_engine.connect() as connection_postgres:
        try:
            await connection_postgres.execute(text(f"CREATE DATABASE \"{database_name}\";"))
            print(f"Database: {database_name} created!")
        except Exception as e:
            print(f"Error; the database: {database_name} probably already exists")
            print(e)

    connectable = create_async_engine(database_url)

    async with connectable.connect() as connection:
        await connection.execute(text("CREATE SCHEMA IF NOT EXISTS testing"))
        await connection.commit()

        def do_run_migrations(conn):
            context.configure(
                connection=conn,
                target_metadata=target_metadata,
                url=database_url,
                version_table_schema="testing",
                include_schemas=True,
                include_name=include_name
            )

            with context.begin_transaction():
                context.run_migrations()

        await connection.run_sync(do_run_migrations)



if context.is_offline_mode():
    run_migrations_offline()
else:
    import asyncio
    asyncio.run(run_migrations_online())
