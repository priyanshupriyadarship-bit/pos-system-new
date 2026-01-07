{\rtf1\ansi\ansicpg1252\cocoartf2867
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 cd pos-system\
source venv/bin/activate\
\
cat > backend/models/database.py << 'DATABASE'\
"""\
Database Connection and ORM Setup\
Handles SQLAlchemy engine, session management, and base model\
"""\
\
from sqlalchemy import create_engine\
from sqlalchemy.ext.declarative import declarative_base\
from sqlalchemy.orm import sessionmaker, Session\
from typing import Generator\
import os\
from dotenv import load_dotenv\
\
load_dotenv()\
\
# Database URL - supports SQLite (local) and PostgreSQL (production)\
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./database/pos.db")\
\
# Create SQLAlchemy engine\
engine = create_engine(\
    DATABASE_URL,\
    connect_args=\{"check_same_thread": False\} if "sqlite" in DATABASE_URL else \{\},\
    echo=True  # Log SQL queries for debugging\
)\
\
# Session factory\
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)\
\
# Base class for all models\
Base = declarative_base()\
\
# Dependency for FastAPI routes\
def get_db() -> Generator[Session, None, None]:\
    """\
    Database session dependency for FastAPI\
    Usage: db: Session = Depends(get_db)\
    """\
    db = SessionLocal()\
    try:\
        yield db\
    finally:\
        db.close()\
\
# Initialize database tables\
def init_db():\
    """Create all tables in the database"""\
    Base.metadata.create_all(bind=engine)\
    print("  Database tables created successfully")\
\
# Drop all tables (use with caution!)\
def reset_db():\
    """Drop all tables - USE CAREFULLY"""\
    Base.metadata.drop_all(bind=engine)\
    print("  All database tables dropped")\
\
if __name__ == "__main__":\
    print(f"Database URL: \{DATABASE_URL\}")\
    init_db()\
DATABASE\
\
echo "  Created backend/models/database.py"\
}