from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from datetime import datetime
import os
from dotenv import load_load_env

load_load_env()

# Database configuration
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://localhost/insurance_leads')
db_engine = create_engine(DATABASE_URL)
Base = declarative_base()

class Lead(Base):
    __tablename__ = 'leads'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255))
    phone = Column(String(50))
    location = Column(String(255))
    profession = Column(String(255))
    source = Column(String(100), nullable=False)
    quality_score = Column(Float)
    status = Column(String(50), default='new')
    raw_data = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<Lead(name='{self.name}', source='{self.source}', quality_score={self.quality_score})>"

class LeadActivity(Base):
    __tablename__ = 'lead_activities'

    id = Column(Integer, primary_key=True)
    lead_id = Column(Integer, nullable=False)
    activity_type = Column(String(50), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<LeadActivity(lead_id={self.lead_id}, type='{self.activity_type}')>"

class ScrapingSession(Base):
    __tablename__ = 'scraping_sessions'

    id = Column(Integer, primary_key=True)
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True))
    source = Column(String(100), nullable=False)
    leads_found = Column(Integer, default=0)
    status = Column(String(50), default='running')
    error_log = Column(Text)

    def __repr__(self):
        return f"<ScrapingSession(source='{self.source}', leads_found={self.leads_found})>"

def init_db():
    """Initialize the database tables"""
    Base.metadata.create_all(db_engine)
