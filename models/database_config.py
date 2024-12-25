from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()

# Replace with your PostgreSQL URI
DATABASE_URI= "postgresql://postgres:none@localhost:5432/postgres"

# Create database engine and session factory
engine = create_engine(DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
