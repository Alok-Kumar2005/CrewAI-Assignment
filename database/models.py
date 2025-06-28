from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True)
    age = Column(Integer)
    gender = Column(String(10))
    created_at = Column(DateTime, default=datetime.utcnow)

class BloodTestReport(Base):
    __tablename__ = "blood_test_reports"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    file_name = Column(String(255))
    file_path = Column(String(500))
    upload_date = Column(DateTime, default=datetime.utcnow)
    query = Column(Text)
    
    # Blood test values
    hemoglobin = Column(Float, nullable=True)
    total_cholesterol = Column(Float, nullable=True)
    hdl_cholesterol = Column(Float, nullable=True)
    ldl_cholesterol = Column(Float, nullable=True)
    triglycerides = Column(Float, nullable=True)
    fasting_glucose = Column(Float, nullable=True)
    hba1c = Column(Float, nullable=True)
    vitamin_b12 = Column(Float, nullable=True)
    vitamin_d = Column(Float, nullable=True)
    tsh = Column(Float, nullable=True)

class AnalysisResult(Base):
    __tablename__ = "analysis_results"
    
    id = Column(Integer, primary_key=True, index=True)
    report_id = Column(Integer, index=True)
    analysis_type = Column(String(50))  # medical, nutrition, exercise
    analysis_result = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)



DATABASE_URL = "sqlite:///./medical_analysis.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()