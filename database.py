from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Read DATABASE_URL from environment for flexibility (Postgres in production)
# Fallback to a local SQLite file for development
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./edumentor.db')

if DATABASE_URL.startswith('sqlite'):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    # For Postgres / MySQL etc. do not pass sqlite-specific args
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
