from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from config import settings
from database import init_db
from middleware.company_context import CompanyContextMiddleware

# Import routers
from routes import auth, admin, companies, calculations


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events."""
    # Startup: Initialize database
    print("Initializing database...")
    init_db()
    print(f"Starting {settings.APP_NAME} v{settings.VERSION}")
    yield
    # Shutdown
    print("Shutting down application...")


# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="Multi-tenant tiling business management system with authentication and company management",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add custom middleware
app.add_middleware(CompanyContextMiddleware)

# Include routers
app.include_router(auth.router, prefix="/api")
app.include_router(admin.router, prefix="/api")
app.include_router(companies.router, prefix="/api")
app.include_router(calculations.router, prefix="/api")


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.VERSION,
        "docs": "/docs",
        "status": "operational"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "version": settings.VERSION
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
