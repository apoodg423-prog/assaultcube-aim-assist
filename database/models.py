"""SQLAlchemy models for Ipro71 Nexus"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import JSON
import datetime

Base = declarative_base()

class Game(Base):
    __tablename__ = 'games'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    exe_path = Column(String, nullable=True)
    enabled = Column(Boolean, default=True)
    metadata = Column(Text, nullable=True)

class Profile(Base):
    __tablename__ = 'profiles'
    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    data = Column(Text, nullable=True)  # JSON serialized settings
    is_default = Column(Boolean, default=False)

class Setting(Base):
    __tablename__ = 'settings'
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, nullable=False)
    value = Column(Text, nullable=True)

class License(Base):
    __tablename__ = 'licenses'
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, nullable=False)
    license_type = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    activated_at = Column(DateTime, nullable=True)
    expires_at = Column(DateTime, nullable=True)
    status = Column(String, default='INVALID')

class LogEntry(Base):
    __tablename__ = 'logs'
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    level = Column(String, nullable=False)
    component = Column(String, nullable=True)
    message = Column(Text, nullable=True)
