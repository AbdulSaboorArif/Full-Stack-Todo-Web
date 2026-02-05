from sqlmodel import Session, SQLModel, create_engine
from .config.settings import Config

# Create database engine
DATABASE_URL = Config.get_database_url()
engine = create_engine(DATABASE_URL)

# Create database tables
SQLModel.metadata.create_all(engine)


def get_db() -> Session:
    """Dependency to get database session"""
    with Session(engine) as session:
        yield session


def init_db() -> None:
    """Initialize database and create tables"""
    SQLModel.metadata.create_all(engine)


def drop_all_tables() -> None:
    """Drop all tables (for testing)"""
    SQLModel.metadata.drop_all(engine)