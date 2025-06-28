from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    age: Optional[int] = None
    gender: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    age: Optional[int]
    gender: Optional[str]
    created_at: datetime

class ReportResponse(BaseModel):
    id: int
    user_id: int
    file_name: str
    upload_date: datetime
    query: str
    hemoglobin: Optional[float]
    total_cholesterol: Optional[float]
    hdl_cholesterol: Optional[float]
    ldl_cholesterol: Optional[float]
    triglycerides: Optional[float]
    fasting_glucose: Optional[float]
    hba1c: Optional[float]
    vitamin_b12: Optional[float]
    vitamin_d: Optional[float]
    tsh: Optional[float]

class AnalysisResponse(BaseModel):
    id: int
    report_id: int
    analysis_type: str
    analysis_result: str
    created_at: datetime

class AnalysisRequest(BaseModel):
    user_email: EmailStr
    query: str
