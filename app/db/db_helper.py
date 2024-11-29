from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import get_config

# load config
config = get_config()
# create async engine

engine = create_async_engine(
    str(config.POSTGRES_DSN),
    echo=True,
)
# create async session
SessionFactory = async_sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


# create async session dependency
async def get_session():
    async with SessionFactory() as session:
        yield session
