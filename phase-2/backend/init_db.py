from src.database import engine
from src.models.user import User
from src.models.task import Task

def init_db():
    """Initialize the database by creating all tables."""
    print("Creating database tables...")
    try:
        # Import all models to ensure they're registered with SQLModel
        from src.models.user import User  # noqa: F401
        from src.models.task import Task  # noqa: F401

        # Create all tables
        from sqlmodel import SQLModel
        SQLModel.metadata.create_all(engine)
        print("Database tables created successfully!")
    except Exception as e:
        print(f"Error creating database tables: {e}")
        raise

if __name__ == "__main__":
    init_db()