from fastapi import FastAPI, HTTPException, Depends, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import Optional, List
import os
import shutil
from datetime import datetime
import re
from extractor import extract_blood_values
from schema import UserCreate, UserResponse, ReportResponse, AnalysisResponse
from database.models import create_tables, get_db
from database.operations import (
    create_user, get_user_by_email, get_user_by_id, create_blood_test_report,
    save_analysis_result, get_user_reports, get_report_analyses, search_reports)
from crew.medical_crew import run_medical_analysis
from pydantic import BaseModel, EmailStr


app = FastAPI(title="Medical Blood Test Analysis API",
    description="API for analyzing blood test reports and providing medical, nutritional, and exercise recommendations",
    version="1.0.0"
)


app.add_middleware(CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,allow_methods=["*"],allow_headers=["*"])


UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

### init database
@app.on_event("startup")
async def startup_event():
    create_tables()


@app.get("/")
async def root():
    return {"message": "Medical Blood Test Analysis API", "version": "1.0.0"}

@app.post("/users/", response_model=UserResponse)
async def create_user_endpoint(user: UserCreate, db: Session = Depends(get_db)):
    """Ccreating a new suer"""
    try:
        db_user = create_user(db, user.name, user.email, user.age, user.gender)
        return UserResponse(
            id=db_user.id,
            name=db_user.name,
            email=db_user.email,
            age=db_user.age,
            gender=db_user.gender,
            created_at=db_user.created_at
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    """get user by id"""
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return UserResponse(
        id=user.id,
        name=user.name,
        email=user.email,
        age=user.age,
        gender=user.gender,
        created_at=user.created_at
    )

@app.get("/users/email/{email}", response_model=UserResponse)
async def get_user_by_email_endpoint(email: str, db: Session = Depends(get_db)):
    """Get user by email"""
    user = get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return UserResponse(
        id=user.id,
        name=user.name,
        email=user.email,
        age=user.age,
        gender=user.gender,
        created_at=user.created_at
    )

@app.post("/analyze-report/")
async def analyze_report_endpoint(file: UploadFile = File(...),user_email: str = Form(...),query: str = Form(...),db: Session = Depends(get_db)):
    """Upload and analyze blood test report"""
    
    ### check pdf is there or not
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    try:
        ### Extracting user data
        user = get_user_by_email(db, user_email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found. Please create user first.")
        
        ### Save the file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name =  f"{timestamp}_{file.filename}"
        file_path = os.path.join(UPLOAD_DIR, file_name)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        ## Extracting data from the crew 
        analysis_result = run_medical_analysis(query, file_path)
        ### Extracting information data from the result of crew 
        blood_values = extract_blood_values(str(analysis_result))
        
        ### SAve data to database
        db_report = create_blood_test_report(
            db, user.id, file.filename, file_path, query, blood_values
        )
        
        ## Getting the data of result
        analysis_text = str(analysis_result)
        
        # Save different types of analyses
        if "MEDICAL ANALYSIS" in analysis_text.upper():
            save_analysis_result(db, db_report.id, "medical", analysis_text)
        if "NUTRITIONAL ANALYSIS" in analysis_text.upper():
            save_analysis_result(db, db_report.id, "nutrition", analysis_text)
        if "EXERCISE PLAN" in analysis_text.upper():
            save_analysis_result(db, db_report.id, "exercise", analysis_text)
        
        return {
            "message": "Analysis completed successfully",
            "report_id": db_report.id,
            "analysis_result": analysis_text,
            "blood_values": blood_values
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

@app.get("/users/{user_id}/reports", response_model=List[ReportResponse])
async def get_user_reports_endpoint(user_id: int, db: Session = Depends(get_db)):
    """get the report of the user"""
    reports = get_user_reports(db, user_id)
    return [
        ReportResponse(
            id=report.id,
            user_id=report.user_id,
            file_name=report.file_name,
            upload_date=report.upload_date,
            query=report.query,
            hemoglobin=report.hemoglobin,
            total_cholesterol=report.total_cholesterol,
            hdl_cholesterol=report.hdl_cholesterol,
            ldl_cholesterol=report.ldl_cholesterol,
            triglycerides=report.triglycerides,
            fasting_glucose=report.fasting_glucose,
            hba1c=report.hba1c,
            vitamin_b12=report.vitamin_b12,
            vitamin_d=report.vitamin_d,
            tsh=report.tsh
        )
        for report in reports
    ]

@app.get("/reports/{report_id}/analyses", response_model=List[AnalysisResponse])
async def get_report_analyses_endpoint(report_id: int, db: Session = Depends(get_db)):
    """Get all analyses for a report"""
    analyses = get_report_analyses(db, report_id)
    return [
        AnalysisResponse(
            id=analysis.id,
            report_id=analysis.report_id,
            analysis_type=analysis.analysis_type,
            analysis_result=analysis.analysis_result,
            created_at=analysis.created_at
        )
        for analysis in analyses
    ]


@app.get("/search/reports/{user_id}")
async def search_reports_endpoint(user_id: int, q: str, db: Session = Depends(get_db)):
    """Search reports by query or filename"""
    reports = search_reports(db, user_id, q)
    return [
        {
            "id": report.id,
            "file_name": report.file_name,
            "query": report.query,
            "upload_date": report.upload_date
        }
        for report in reports
    ]


@app.delete("/reports/{report_id}")
async def delete_report_endpoint(report_id: int, db: Session = Depends(get_db)):
    """Delete a report and its analyses"""
    from database.operations import delete_report
    
    success = delete_report(db, report_id)
    if success:
        return {"message": "Report deleted successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to delete report")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)