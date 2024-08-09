# app/database.py
import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Read environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

# SQLAlchemy connection string
# SQLALCHEMY_DATABASE_URL = (DATABASE_URL)
# SQLALCHEMY_DATABASE_URL = (
#     f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
# )

# Create an asynchronous engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Create a configured session class with async capabilities
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Base class for your models
Base = declarative_base()

# Dependency to yield database session
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session