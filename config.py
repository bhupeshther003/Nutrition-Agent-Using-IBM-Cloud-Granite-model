"""
Configuration file for Multi-Agent Resume Screening System
Contains settings for IBM Watsonx.ai, database, and application
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Base configuration class"""
    
    # Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    # Database Configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///resume_screening.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # File Upload Configuration
    UPLOAD_FOLDER = 'uploads'
    REPORTS_FOLDER = 'reports'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'pdf', 'docx'}
    
    # IBM Watsonx.ai Configuration
    WATSONX_API_KEY = os.environ.get('WATSONX_API_KEY')
    WATSONX_PROJECT_ID = os.environ.get('WATSONX_PROJECT_ID')
    WATSONX_URL = os.environ.get('WATSONX_URL') or 'https://au-syd.ml.cloud.ibm.com'
    
    # IBM Granite Model Configuration
    GRANITE_MODEL_ID = os.environ.get('ibm/granite-guardian-3-8b') or 'ibm/granite-guardian-3-8b'
    
    # Model Parameters
    MODEL_PARAMETERS = {
        'decoding_method': 'greedy',
        'max_new_tokens': 1000,
        'min_new_tokens': 1,
        'temperature': 0.7,
        'top_k': 50,
        'top_p': 1,
        'repetition_penalty': 1.0
    }
    
    # Agent Configuration
    PARSER_AGENT_PROMPT = """You are a Resume Parser Agent. Extract structured information from resumes.
Extract: name, email, phone, skills (list), education (degrees, institutions, years), 
work experience (companies, positions, durations, responsibilities), certifications, and summary.
Return data in JSON format."""
    
    MATCHER_AGENT_PROMPT = """You are a Job Matcher Agent. Compare candidate profiles with job requirements.
Analyze skills match, experience relevance, education alignment, and overall fit.
Identify matching skills, missing skills, and relevant experience."""
    
    SCORING_AGENT_PROMPT = """You are a Scoring Agent. Calculate match percentage based on:
- Skills match (40%)
- Experience relevance (30%)
- Education alignment (20%)
- Additional factors (10%)
Return a score between 0-100 with breakdown."""
    
    FEEDBACK_AGENT_PROMPT = """You are a Feedback Agent. Generate detailed hiring insights.
Provide: strengths, gaps, recommendations, and overall assessment.
Be specific and actionable in your feedback."""
    
    # Scoring Weights
    SCORING_WEIGHTS = {
        'skills': 0.40,
        'experience': 0.30,
        'education': 0.20,
        'additional': 0.10
    }
    
    # Logging Configuration
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FILE = 'app.log'


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

# Made with Bob
