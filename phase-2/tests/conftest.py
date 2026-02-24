"""
Configuration for testing in Todo Backend API
"""
import pytest
import asyncio
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession as SQLAlchemyAsyncSession
from contextlib import asynccontextmanager
from src.config import settings


# Create test database engine (using SQLite in memory for tests)
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

test_engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=False,
    poolclass=StaticPool,
    connect_args={"check_same_thread": False}
)


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for pytest-asyncio."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@asynccontextmanager
async def get_test_session():
    """Get a test database session."""
    async with AsyncSession(test_engine) as session:
        yield session


@pytest.fixture(autouse=True)
async def setup_test_db():
    """Set up the test database before each test."""
    # Create all tables
    async with test_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    yield

    # Optionally clean up after each test
    async with test_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)


@pytest.fixture
async def test_session():
    """Get a test session for individual tests."""
    async with AsyncSession(test_engine) as session:
        yield session
        await session.rollback()


# Test configuration
@pytest.fixture
def override_settings():
    """Override settings for testing."""
    # In a real scenario, we might want to override specific settings
    # For now, we'll just return the original settings
    return settings


# Additional fixtures for common test objects
@pytest.fixture
def sample_user_data():
    """Provide sample user data for tests."""
    return {
        "email": "test@example.com",
        "password": "SecurePassword123!"
    }


@pytest.fixture
def sample_task_data():
    """Provide sample task data for tests."""
    return {
        "title": "Test Task",
        "description": "This is a test task description"
    }


# Test utility functions
async def create_test_user(session, email="test@example.com", password="SecurePassword123!"):
    """Helper function to create a test user."""
    from src.models.user import User
    import bcrypt

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    user = User(email=email, password_hash=hashed_password)

    session.add(user)
    await session.commit()
    await session.refresh(user)

    return user


async def create_test_task(session, user_id, title="Test Task", description="Test Description"):
    """Helper function to create a test task."""
    from src.models.task import Task

    task = Task(title=title, description=description, user_id=user_id)

    session.add(task)
    await session.commit()
    await session.refresh(task)

    return task