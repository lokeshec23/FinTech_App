"""
Main FastAPI application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .config import settings
from .database import connect_to_mongo, close_mongo_connection
from .routes import auth


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    await connect_to_mongo()
    yield
    # Shutdown
    await close_mongo_connection()


# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
from .routes import expenses, emis, analytics, bank_accounts, assets, liabilities, upi, goals

app.include_router(auth.router)
app.include_router(expenses.router)
app.include_router(emis.router)
app.include_router(analytics.router)
app.include_router(bank_accounts.router)
app.include_router(assets.router)
app.include_router(liabilities.router)
app.include_router(upi.router)
app.include_router(goals.router)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring
    Used by Render to verify service health
    """
    from .database import database
    
    health_status = {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION
    }
    
    # Check database connectivity
    try:
        if database is not None:
            # Ping the database to verify connection
            await database.command("ping")
            health_status["database"] = "connected"
        else:
            health_status["database"] = "not initialized"
            health_status["status"] = "degraded"
    except Exception as e:
        health_status["database"] = "disconnected"
        health_status["status"] = "unhealthy"
        health_status["error"] = str(e)
    
    return health_status

