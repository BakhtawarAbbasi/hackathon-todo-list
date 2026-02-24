"""
Database initialization script for Todo Backend API
"""
import asyncio
import sys
import os

# Add the src directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine
from ..config import settings


async def create_tables():
    """
    Create all database tables based on SQLModel definitions
    """
    print("Creating database tables...")

    # Create async engine
    engine = create_async_engine(settings.DATABASE_URL)

    async with engine.begin() as conn:
        # Create all tables defined in SQLModel models
        await conn.run_sync(SQLModel.metadata.create_all)

    print("Database tables created successfully!")


async def main():
    """
    Main function to run the database initialization
    """
    try:
        await create_tables()
        print("\nDatabase initialization completed successfully!")
        print("Tables created:")
        print("- users table")
        print("- tasks table")
        print("\nThe database is now ready for use.")

    except Exception as e:
        print(f"Error initializing database: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())