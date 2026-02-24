"""
FastAPI application for Todo Backend API
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .logging import logger
from .error_handler import register_error_handlers
from .db.db import initialize_database
from .routes.tasks import router as tasks_router

app = FastAPI(
    title="Todo Backend API",
    description="API for managing user tasks with user isolation and authentication",
    version="1.0.0",
    debug=settings.ENVIRONMENT == "development",
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc",  # Redoc
    openapi_url="/openapi.json"  # OpenAPI schema
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(tasks_router)

# Register error handlers
register_error_handlers(app)

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "todo-backend", "version": "1.0.0"}

# Startup and shutdown events
@app.on_event("startup")
async def startup_event():
    """Application startup event"""
    logger.info("Todo Backend API starting up...")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Port: {settings.PORT}")

    # Initialize database
    await initialize_database()
    logger.info("Database initialized successfully")

@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown event"""
    logger.info("Todo Backend API shutting down...")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=settings.PORT)