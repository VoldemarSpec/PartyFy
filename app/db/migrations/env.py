import asyncio
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import create_async_engine
from alembic import context
from app.db.base.base import Base
from app.db.config.config import db_settings
from app.db import models

target_metadata = Base.metadata




DATABASE_URL = db_settings.DATABASE_URL


fileConfig(context.config.config_file_name)


target_metadata = Base.metadata


engine = create_async_engine(DATABASE_URL, poolclass=pool.NullPool)

async def run_migrations_online():
    async with engine.begin() as conn:
        await conn.run_sync(do_run_migrations)

def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()

def run_migrations():
    asyncio.run(run_migrations_online())

run_migrations()
