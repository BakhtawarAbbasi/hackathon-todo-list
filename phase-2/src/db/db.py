"""
Database connection module for Todo Backend API
"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
import logging

from ..config import settings

# Create logger
logger = logging.getLogger(__name__)

# Create async engine with connection pooling
engine: AsyncEngine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,  # Set to True for SQL query logging
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,
    pool_recycle=300,
    connect_args={"async_driver": "asyncpg"},
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Get database session for dependency injection
    """
    async with AsyncSession(engine) as session:
        yield session


async def create_tables():
    """
    Create all tables in the database
    """
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    logger.info("Database tables created successfully")


async def drop_tables():
    """
    Drop all tables in the database (use with caution!)
    """
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
    logger.info("Database tables dropped successfully")


async def database_health_check():
    """
    Perform a health check on the database connection
    """
    try:
        async with engine.begin() as conn:
            # Simple query to test connection
            await conn.execute("SELECT 1")
        return True
    except Exception as e:
        logger.error(f"Database health check failed: {str(e)}")
        return False


async def initialize_database():
    """
    Initialize the database with required tables and data
    """
    logger.info("Initializing database...")
    await create_tables()
    logger.info("Database initialization completed")