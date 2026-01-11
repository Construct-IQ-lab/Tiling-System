from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.config import settings
from backend.database import init_db
from backend.routes import auth, admin, companies, projects, calculations

# Initialize database
init_db()

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="API for managing tiling projects, calculations, and material estimations",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
# Authentication
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])

# Admin routes
app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])

# Company routes
app.include_router(companies.router, prefix="/api/companies", tags=["Companies"])

# Legacy routes (to be implemented)
app.include_router(projects.router, prefix="/api/v1/projects", tags=["Projects"])
app.include_router(calculations.router, prefix="/api/v1/calculations", tags=["Calculations"])


@app.get("/", tags=["Root"])
def read_root():
    """Root endpoint"""
    return {
        "name": settings.APP_NAME,
        "version": settings.VERSION,
        "status": "running",
        "docs": "/docs"
    }


@app.get("/health", tags=["Health"])
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "version": settings.VERSION}