from sqlalchemy.orm import Session
from database.models import User, BloodTestReport, AnalysisResult
from typing import Optional, List, Dict
import json
from datetime import datetime

def create_user(db: Session, name: str, email: str, age: int = None, gender: str = None) -> User:
    """Creating a new user"""
    # Check if user already exists
    existing_user = get_user_by_email(db, email)
    if existing_user:
        return existing_user
    
    db_user = User(name=name, email=email, age=age, gender=gender)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Get user by email"""
    return db.query(User).filter(User.email == email).first()

def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    """get user by their id"""
    return db.query(User).filter(User.id == user_id).first()

def create_blood_test_report(db: Session, user_id: int, file_name: str, file_path: str, query: str, blood_values: Dict = None) -> BloodTestReport:
    """Create a new blood test report entry"""
    db_report = BloodTestReport(
        user_id=user_id,
        file_name=file_name,
        file_path=file_path,
        query=query
    )
    
    # Adding blood values if providedn from pdf
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
    return db.query(BloodTestReport).filter(BloodTestReport.user_id == user_id).order_by(BloodTestReport.upload_date.desc()).all()

def get_report_analyses(db: Session, report_id: int) -> List[AnalysisResult]:
    """Get all analyses for a report"""
    return db.query(AnalysisResult).filter(AnalysisResult.report_id == report_id).order_by(AnalysisResult.created_at.desc()).all()


def get_all_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    """Get all users with pagination"""
    return db.query(User).offset(skip).limit(limit).all()

def delete_user(db: Session, user_id: int) -> bool:
    """Delete a user and all related data"""
    try:
        # First delete all analysis results for user's reports
        user_reports = get_user_reports(db, user_id)
        for report in user_reports:
            db.query(AnalysisResult).filter(AnalysisResult.report_id == report.id).delete()
        
        # Delete all user's reports
        db.query(BloodTestReport).filter(BloodTestReport.user_id == user_id).delete()
        
        # Delete the user
        db.query(User).filter(User.id == user_id).delete()
        
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        return False

def delete_report(db: Session, report_id: int) -> bool:
    """Delete a report and all its analyses"""
    try:
        # Delete all analyses for this report
        db.query(AnalysisResult).filter(AnalysisResult.report_id == report_id).delete()
        
        # Delete the report
        db.query(BloodTestReport).filter(BloodTestReport.id == report_id).delete()
        
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        return False

def search_reports(db: Session, user_id: int, search_term: str) -> List[BloodTestReport]:
    """Search reports by query or file name"""
    return db.query(BloodTestReport).filter(
        BloodTestReport.user_id == user_id,
        (BloodTestReport.query.contains(search_term) | 
         BloodTestReport.file_name.contains(search_term))
    ).order_by(BloodTestReport.upload_date.desc()).all()

