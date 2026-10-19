# database/models.py
from sqlalchemy import (Column, Integer, String,
    Float, DateTime, Text)
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id            = Column(Integer, primary_key=True)
    username      = Column(String, unique=True)
    email         = Column(String, unique=True)
    password_hash = Column(String)
    created_at    = Column(DateTime,
                           default=datetime.utcnow)

class PredictionHistory(Base):
    __tablename__ = "predictions"
    id              = Column(Integer,primary_key=True)
    user_id         = Column(Integer)
    features        = Column(Text)  # JSON string
    predicted_price = Column(Float)
    timestamp       = Column(DateTime,
                             default=datetime.utcnow)

class FavoriteProperty(Base):
    __tablename__ = "favorites"
    id            = Column(Integer,primary_key=True)
    user_id       = Column(Integer)
    property_data = Column(Text)  # JSON string
    saved_at      = Column(DateTime,
                           default=datetime.utcnow)