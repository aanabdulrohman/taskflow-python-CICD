import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

# Cek apakah aplikasi sedang berjalan dalam mode Unit Testing
TESTING = os.getenv("TESTING", "False").lower() in ("true", "1", "t")

if TESTING:
    # Gunakan SQLite in-memory untuk Pytest
    DATABASE_URL = "sqlite:///:memory:"
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
else:
    # Gunakan MySQL untuk Normal App Runtime
    DB_USER = os.getenv("MYSQL_USER", "taskuser")
    DB_PASSWORD = os.getenv("MYSQL_PASSWORD", "taskpassword")
    DB_HOST = os.getenv("MYSQL_HOST", "localhost")
    DB_PORT = os.getenv("MYSQL_PORT", "3306")
    DB_NAME = os.getenv("MYSQL_DATABASE", "taskflow_db")

    DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()