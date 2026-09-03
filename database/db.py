"""Database layer using SQLAlchemy"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from pathlib import Path

DB_PATH = Path("nexus.db")
ENGINE = create_engine(f"sqlite:///{DB_PATH}", connect_args={"check_same_thread": False})
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=ENGINE))


def init_db():
    from database import models
    models.Base.metadata.create_all(bind=ENGINE)
