"""
Database models for Multi-Agent Resume Screening System
Defines tables for candidates, job descriptions, and screening results
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class JobDescription(db.Model):
    """Model for storing job descriptions"""
    __tablename__ = 'job_descriptions'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    required_skills = db.Column(db.Text)  # JSON string
    required_experience = db.Column(db.String(100))
    required_education = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    candidates = db.relationship('Candidate', backref='job', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'required_skills': self.required_skills,
            'required_experience': self.required_experience,
            'required_education': self.required_education,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Candidate(db.Model):
    """Model for storing candidate information"""
    __tablename__ = 'candidates'
    
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job_descriptions.id'), nullable=False)
    
    # Personal Information
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200))
    phone = db.Column(db.String(50))
    
    # Resume Information
    resume_filename = db.Column(db.String(300), nullable=False)
    resume_path = db.Column(db.String(500), nullable=False)
    
    # Parsed Data (stored as JSON strings)
    skills = db.Column(db.Text)  # JSON array
    education = db.Column(db.Text)  # JSON array
    experience = db.Column(db.Text)  # JSON array
    certifications = db.Column(db.Text)  # JSON array
    summary = db.Column(db.Text)
    
    # Screening Results
    match_score = db.Column(db.Float, default=0.0)
    skills_score = db.Column(db.Float, default=0.0)
    experience_score = db.Column(db.Float, default=0.0)
    education_score = db.Column(db.Float, default=0.0)
    
    # Analysis
    matching_skills = db.Column(db.Text)  # JSON array
    missing_skills = db.Column(db.Text)  # JSON array
    strengths = db.Column(db.Text)
    gaps = db.Column(db.Text)
    recommendations = db.Column(db.Text)
    detailed_feedback = db.Column(db.Text)
    
    # Metadata
    rank = db.Column(db.Integer)
    status = db.Column(db.String(50), default='pending')  # pending, processed, error
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'job_id': self.job_id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'resume_filename': self.resume_filename,
            'skills': self.skills,
            'education': self.education,
            'experience': self.experience,
            'certifications': self.certifications,
            'summary': self.summary,
            'match_score': self.match_score,
            'skills_score': self.skills_score,
            'experience_score': self.experience_score,
            'education_score': self.education_score,
            'matching_skills': self.matching_skills,
            'missing_skills': self.missing_skills,
            'strengths': self.strengths,
            'gaps': self.gaps,
            'recommendations': self.recommendations,
            'detailed_feedback': self.detailed_feedback,
            'rank': self.rank,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class ScreeningSession(db.Model):
    """Model for tracking screening sessions"""
    __tablename__ = 'screening_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job_descriptions.id'), nullable=False)
    total_candidates = db.Column(db.Integer, default=0)
    processed_candidates = db.Column(db.Integer, default=0)
    status = db.Column(db.String(50), default='in_progress')  # in_progress, completed, failed
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'job_id': self.job_id,
            'total_candidates': self.total_candidates,
            'processed_candidates': self.processed_candidates,
            'status': self.status,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }

# Made with Bob
