from sqlalchemy.orm import Session
from database.models import User, BloodTestReport, AnalysisResult
from typing import Optional, List, Dict
import json

def create_user(db: Session, name: str, email: str, age: int = None, gender: str = None) -> User:
    """ Create a new user """
    db_user = User(name=name, email=email, age=age, gender=gender)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """ Get user by email """
    return db.query(User).filter(User.email == email).first()

def create_blood_test_report(db: Session, user_id: int, file_name: str, file_path: str, query: str,blood_values: Dict = None) -> BloodTestReport:
    """Create a new blood test report entry"""
    db_report = BloodTestReport(
        user_id=user_id,
        file_name=file_name,
        file_path=file_path,
        query=query
    )
    
    # Add blood values if provided
    if blood_values:
        for key, value in blood_values.items():
            if hasattr(db_report, key) and value is not None:
                setattr(db_report, key, value)
    
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report

def save_analysis_result(db: Session, report_id: int, analysis_type: str, result: str) -> AnalysisResult:
    """Save analysis result"""
    db_result = AnalysisResult(
        report_id=report_id,
        analysis_type=analysis_type,
        analysis_result=result
    )
    db.add(db_result)
    db.commit()
    db.refresh(db_result)
    return db_result

def get_user_reports(db: Session, user_id: int) -> List[BloodTestReport]:
    """Get all reports for a user"""
    return db.query(BloodTestReport).filter(BloodTestReport.user_id == user_id).all()

def get_report_analyses(db: Session, report_id: int) -> List[AnalysisResult]:
    """Get all analyses for a report"""
    return db.query(AnalysisResult).filter(AnalysisResult.report_id == report_id).all()

def update_blood_values(db: Session, report_id: int, blood_values: Dict):
    """Update blood test values for a report"""
    db_report = db.query(BloodTestReport).filter(BloodTestReport.id == report_id).first()
    if db_report:
        for key, value in blood_values.items():
            if hasattr(db_report, key) and value is not None:
                setattr(db_report, key, value)
        db.commit()
        db.refresh(db_report)
    return db_report