"""
Database initialization script for Todo Backend API
"""
import asyncio
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import modules after loading environment and setting up path
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

# Import the actual models that should be created
from models.user import User
from models.task import Task


# Define settings class similar to what's in src/config.py
class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str = "hackathon-todo-list"
    PORT: int = 8000
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()


async def create_tables():
    """
    Create all database tables based on SQLModel definitions
    """
    print("Connecting to database...")
    # Mask sensitive parts for display
    display_url = settings.DATABASE_URL.replace('@', '[@]').replace(':', '[:]').replace('_', '[_]')
    print(f"Database URL: {display_url}")

    try:
        # Create async engine - need to use async driver
        url = settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")
        url = url.replace("?sslmode=require", "")  # Remove sslmode for asyncpg
        engine = create_async_engine(url, pool_size=5, max_overflow=10, pool_pre_ping=True, pool_recycle=300)

        print("Creating all tables...")
        async with engine.begin() as conn:
            # Create all tables defined in SQLModel models
            await conn.run_sync(SQLModel.metadata.create_all)

        print("Database tables created successfully!")
    except Exception as e:
        print(f"Error creating engine or tables: {str(e)}")
        raise


async def main():
    """
    Main function to run the database initialization
    """
    try:
        print("Starting database initialization...")
        await create_tables()
        print("\nDatabase initialization completed successfully!")
        print("Tables created:")
        print("- users table")
        print("- tasks table")
        print("\nThe database is now ready for use.")

    except Exception as e:
        print(f"Error initializing database: {str(e)}")
        print("\nPlease make sure:")
        print("1. Your DATABASE_URL in .env is correct")
        print("2. You have the necessary permissions to create tables")
        print("3. The database server is accessible")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())