from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config.settings import Config
from .models.user import User
from .models.task import Task
from sqlmodel import Session, SQLModel, create_engine
from .middleware.auth import JWTAuthenticationMiddleware
from .middleware.logging import LoggingMiddleware, ErrorHandlerMiddleware, setup_logging
from .database import init_db

# Create database engine
DATABASE_URL = Config.get_database_url()
engine = create_engine(DATABASE_URL)

# Create database tables
SQLModel.metadata.create_all(engine)

# Initialize database
init_db()

# Initialize FastAPI app
app = FastAPI(
    title="Todo API",
    description="API for Todo Full-Stack Web Application",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=Config.get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add middleware
app.add_middleware(LoggingMiddleware)
app.add_middleware(ErrorHandlerMiddleware)

# Add JWT authentication middleware
app.add_middleware(JWTAuthenticationMiddleware)

@app.on_event("startup")
async def startup_event():
    """Startup event to initialize database and other services"""
    print("Todo API starting up...")
    print(f"Database URL: {DATABASE_URL}")
    print(f"CORS Origins: {Config.get_cors_origins()}")
    setup_logging(app)

@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event to clean up resources"""
    print("Todo API shutting down...")

@app.get("/")
async def root() -> dict[str, str]:
    """Root endpoint"""
    return {"message": "Todo API is running"}

@app.get("/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": str(datetime.utcnow())}

# Dependency to get database session
def get_db() -> Session:
    """Dependency to get database session"""
    with Session(engine) as session:
        yield session