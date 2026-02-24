from sqlalchemy import text
import asyncio
import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

# Load environment variables from .env file
load_dotenv()

# Get database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("❌ ERROR: DATABASE_URL environment variable not found")
    print("Please check your .env file or set the DATABASE_URL variable")
    exit(1)

try:
    # Create async engine with async driver
    url = DATABASE_URL.replace('postgresql://', 'postgresql+asyncpg://')
    url = url.replace('?sslmode=require', '')  # Remove sslmode for asyncpg
    engine = create_async_engine(url, pool_size=5, max_overflow=10, pool_pre_ping=True, pool_recycle=300)

    async def check_tables():
        async with AsyncSession(engine) as session:
            print("DATABASE TABLES VERIFICATION")
            print("=" * 40)

            # Check users table
            print("\nChecking user table...")
            result = await session.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND table_name = 'user'"))
            users_exists = bool(result.scalars().first())
            if users_exists:
                print("users table exists")
                # Check table structure
                print("Table structure:")
                desc = await session.execute(text("SELECT column_name, data_type, is_nullable, column_default FROM information_schema.columns WHERE table_name = 'user' ORDER BY ordinal_position"))
                for row in desc:
                    col_name, data_type, is_nullable, col_default = row
                    if col_default is None:
                        col_default = "NULL"
                    print(f"   {col_name:15s} {data_type:15s} {is_nullable:10s} {col_default:15s}")
            else:
                print("users table does NOT exist")

            # Check tasks table
            print("\nChecking task table...")
            result = await session.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND table_name = 'task'"))
            tasks_exists = bool(result.scalars().first())
            if tasks_exists:
                print("tasks table exists")
                # Check table structure
                print("Table structure:")
                desc = await session.execute(text("SELECT column_name, data_type, is_nullable, column_default FROM information_schema.columns WHERE table_name = 'task' ORDER BY ordinal_position"))
                for row in desc:
                    col_name, data_type, is_nullable, col_default = row
                    if col_default is None:
                        col_default = "NULL"
                    print(f"   {col_name:15s} {data_type:15s} {is_nullable:10s} {col_default:15s}")
            else:
                print("tasks table does NOT exist")

            print("\n" + "=" * 40)

    asyncio.run(check_tables())
except Exception as e:
    print(f"Error connecting to database: {str(e)}")
    raise
