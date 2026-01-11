from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from database import Base, engine
from routes import projects, calculations, auth, admin, companies
from middleware import CompanyContextMiddleware

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="Multi-tenant SaaS platform for managing tiling projects, calculations, and material estimations",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CompanyContextMiddleware before CORS
app.add_middleware(CompanyContextMiddleware)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])
app.include_router(companies.router, prefix="/api/companies", tags=["Companies"])
app.include_router(projects.router, prefix="/api/v1/projects", tags=["Projects"])
app.include_router(calculations.router, prefix="/api/v1/calculations", tags=["Calculations"])


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    # Import models to register them with Base
    from models import Company, User, Project, Quote, Invoice
    # Create tables
    Base.metadata.create_all(bind=engine)


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