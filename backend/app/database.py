import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Load file .env jika dijalankan secara lokal (di luar Docker)
load_dotenv()

# Ambil nilai individu dari environment variable
DB_USER = os.getenv("MYSQL_USER", "taskuser")
DB_PASSWORD = os.getenv("MYSQL_PASSWORD", "taskpassword")
DB_HOST = os.getenv("MYSQL_HOST", "localhost")  # 'localhost' di lokal, 'db-service' di Docker
DB_PORT = os.getenv("MYSQL_PORT", "3306")
DB_NAME = os.getenv("MYSQL_DATABASE", "taskflow_db")

# Susun DATABASE_URL secara dinamis
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