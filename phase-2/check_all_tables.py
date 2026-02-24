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

    async def check_all():
        async with AsyncSession(engine) as session:
            # Get all tables
            tables = await session.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"))
            all_tables = tables.scalars().all()
            print(f'All tables in database: {all_tables}')

            # Check what tables exist that match our expected models
            expected_tables = ['users', 'tasks']
            for expected in expected_tables:
                exists = any(t.lower() == expected for t in all_tables)
                print(f'{expected} table exists: {exists}')

    asyncio.run(check_all())

except Exception as e:
    print(f'Error: {str(e)}')
    raise