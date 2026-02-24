import asyncio
import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import text

# Load environment variables
load_dotenv()

# Get database URL
DATABASE_URL = os.getenv('DATABASE_URL')

if not DATABASE_URL:
    print('❌ ERROR: DATABASE_URL not found')
    exit(1)

try:
    # Create async engine
    url = DATABASE_URL.replace('postgresql://', 'postgresql+asyncpg://')
    url = url.replace('?sslmode=require', '')
    engine = create_async_engine(url, pool_size=5, max_overflow=10, pool_pre_ping=True)

    async def check_tables():
        async with AsyncSession(engine) as session:
            # Check all tables in public schema
            result = await session.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"))
            tables = result.scalars().all()
            print(f'Tables found in database: {tables}')

            # Show detailed table info for each table
            for table in tables:
                print(f'\nDetails for {table}:')
                desc = await session.execute(text(f"SELECT column_name, data_type, is_nullable, column_default FROM information_schema.columns WHERE table_name = '{table}' ORDER BY ordinal_position"))
                for row in desc:
                    col_name = row[0] if row[0] is not None else 'null'
                    data_type = row[1] if row[1] is not None else 'null'
                    is_nullable = row[2] if row[2] is not None else 'null'
                    col_default = row[3] if row[3] is not None else 'null'
                    print(f"   {col_name:15s} {data_type:15s} {is_nullable:10s} {col_default:15s}")

    asyncio.run(check_tables())

except Exception as e:
    print(f'Error: {str(e)}')
    raise