"""
Main Flask application for Multi-Agent Resume Screening System
"""

import os
import json
import logging
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for
from werkzeug.utils import secure_filename
from config import config
from app.models import db, JobDescription, Candidate, ScreeningSession
from app.utils import DocumentProcessor, create_watsonx_client, ReportGenerator
from app.agents import ParserAgent, MatcherAgent, ScoringAgent, FeedbackAgent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def create_app(config_name='default'):
    """
    Application factory function
    
    Args:
        config_name (str): Configuration name
        
    Returns:
        Flask: Configured Flask application
    """
    # Specify template and static folders explicitly
    app = Flask(__name__,
                template_folder='app/templates',
                static_folder='app/static')
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    # Initialize components
    try:
        # Get the config object (not Flask's config dict)
        config_obj = config[config_name]
        
        watsonx_client = create_watsonx_client(config_obj)
        parser_agent = ParserAgent(watsonx_client, config_obj)
        matcher_agent = MatcherAgent(watsonx_client, config_obj)
        scoring_agent = ScoringAgent(watsonx_client, config_obj)
        feedback_agent = FeedbackAgent(watsonx_client, config_obj)
        report_generator = ReportGenerator(app.config['REPORTS_FOLDER'])
        
        # Store in app context
        app.watsonx_client = watsonx_client
        app.parser_agent = parser_agent
        app.matcher_agent = matcher_agent
        app.scoring_agent = scoring_agent
        app.feedback_agent = feedback_agent
        app.report_generator = report_generator
        
        logger.info("All agents initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize agents: {str(e)}")
        # Continue without agents for development
        app.watsonx_client = None
        app.parser_agent = None
        app.matcher_agent = None
        app.scoring_agent = None
        app.feedback_agent = None
        app.report_generator = ReportGenerator(app.config['REPORTS_FOLDER'])
    
    # Ensure upload and reports directories exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['REPORTS_FOLDER'], exist_ok=True)

    

    
    # Routes
    @app.route('/')
    def index():
        """Home page"""
        return render_template('index.html')
    
    @app.route('/api/jobs', methods=['POST'])
    def create_job():
        """Create new job description"""
        try:
            data = request.get_json()
            
            job = JobDescription(
                title=data.get('title'),
                description=data.get('description'),
                required_skills=json.dumps(data.get('required_skills', [])),
                required_experience=data.get('required_experience'),
                required_education=data.get('required_education')
            )
            
            db.session.add(job)
            db.session.commit()
            
            logger.info(f"Job created: {job.title} (ID: {job.id})")
            
            return jsonify({
                'success': True,
                'job_id': job.id,
                'message': 'Job description created successfully'
            }), 201
            
        except Exception as e:
            logger.error(f"Failed to create job: {str(e)}")
            db.session.rollback()
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    @app.route('/api/jobs/<int:job_id>/upload', methods=['POST'])
    def upload_resumes(job_id):
        """Upload resumes for a job"""
        try:
            # Check if job exists
            job = JobDescription.query.get_or_404(job_id)
            
            # Check if files were uploaded
            if 'resumes' not in request.files:
                return jsonify({
                    'success': False,
                    'error': 'No files uploaded'
                }), 400
            
            files = request.files.getlist('resumes')
            uploaded_files = []
            
            for file in files:
                if file and DocumentProcessor.validate_file(file.filename):
                    # Save file
                    filename = secure_filename(file.filename)
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    unique_filename = f"{timestamp}_{filename}"
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                    file.save(filepath)
                    
                    # Create candidate record
                    candidate = Candidate(
                        job_id=job_id,
                        name='Processing...',
                        resume_filename=filename,
                        resume_path=filepath,
                        status='pending'
                    )
                    db.session.add(candidate)
                    uploaded_files.append({
                        'filename': filename,
                        'path': filepath
                    })
            
            db.session.commit()
            
            logger.info(f"Uploaded {len(uploaded_files)} resumes for job {job_id}")
            
            return jsonify({
                'success': True,
                'uploaded_count': len(uploaded_files),
                'message': f'{len(uploaded_files)} resumes uploaded successfully'
            }), 200
            
        except Exception as e:
            logger.error(f"Failed to upload resumes: {str(e)}")
            db.session.rollback()
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    @app.route('/api/jobs/<int:job_id>/process', methods=['POST'])
    def process_resumes(job_id):
        """Process all resumes for a job"""
        try:
            job = JobDescription.query.get_or_404(job_id)
            candidates = Candidate.query.filter_by(job_id=job_id, status='pending').all()
            
            if not candidates:
                return jsonify({
                    'success': False,
                    'error': 'No pending candidates to process'
                }), 400
            
            # Create screening session
            session = ScreeningSession(
                job_id=job_id,
                total_candidates=len(candidates),
                status='in_progress'
            )
            db.session.add(session)
            db.session.commit()
            
            processed_count = 0
            job_data = job.to_dict()
            
            for candidate in candidates:
                try:
                    # Extract text from resume
                    resume_text = DocumentProcessor.extract_text(candidate.resume_path)
                    
                    # Parse resume
                    parsed_data = app.parser_agent.parse_resume(resume_text)
                    
                    # Update candidate with parsed data
                    candidate.name = parsed_data.get('name', 'Unknown')
                    candidate.email = parsed_data.get('email', '')
                    candidate.phone = parsed_data.get('phone', '')
                    candidate.skills = json.dumps(parsed_data.get('skills', []))
                    candidate.education = json.dumps(parsed_data.get('education', []))
                    candidate.experience = json.dumps(parsed_data.get('experience', []))
                    candidate.certifications = json.dumps(parsed_data.get('certifications', []))
                    candidate.summary = parsed_data.get('summary', '')
                    
                    # Match candidate with job
                    match_data = app.matcher_agent.match_candidate(parsed_data, job_data)
                    
                    candidate.matching_skills = json.dumps(match_data.get('matching_skills', []))
                    candidate.missing_skills = json.dumps(match_data.get('missing_skills', []))
                    
                    # Calculate score
                    score_data = app.scoring_agent.calculate_score(parsed_data, match_data, job_data)
                    
                    candidate.match_score = score_data.get('total_score', 0)
                    candidate.skills_score = score_data.get('skills_score', 0)
                    candidate.experience_score = score_data.get('experience_score', 0)
                    candidate.education_score = score_data.get('education_score', 0)
                    
                    # Generate feedback
                    feedback_data = app.feedback_agent.generate_feedback(
                        parsed_data, match_data, score_data, job_data
                    )
                    
                    candidate.strengths = json.dumps(feedback_data.get('strengths', []))
                    candidate.gaps = json.dumps(feedback_data.get('gaps', []))
                    candidate.recommendations = feedback_data.get('recommendation', '')
                    candidate.detailed_feedback = feedback_data.get('detailed_explanation', '')
                    
                    candidate.status = 'processed'
                    processed_count += 1
                    
                    logger.info(f"Processed candidate: {candidate.name} (Score: {candidate.match_score:.1f}%)")
                    
                except Exception as e:
                    logger.error(f"Failed to process candidate {candidate.id}: {str(e)}")
                    candidate.status = 'error'
            
            # Rank candidates
            all_candidates = Candidate.query.filter_by(job_id=job_id, status='processed').all()
            candidates_list = [c.to_dict() for c in all_candidates]
            ranked = ScoringAgent.rank_candidates(candidates_list)
            
            for ranked_candidate in ranked:
                candidate = Candidate.query.get(ranked_candidate['id'])
                if candidate:
                    candidate.rank = ranked_candidate['rank']
            
            # Update session
            session.processed_candidates = processed_count
            session.status = 'completed'
            session.completed_at = datetime.utcnow()
            
            db.session.commit()
            
            logger.info(f"Processing completed: {processed_count}/{len(candidates)} candidates")
            
            return jsonify({
                'success': True,
                'processed_count': processed_count,
                'total_count': len(candidates),
                'message': f'Processed {processed_count} candidates successfully'
            }), 200
            
        except Exception as e:
            logger.error(f"Failed to process resumes: {str(e)}")
            db.session.rollback()
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    @app.route('/api/jobs/<int:job_id>/results')
    def get_results(job_id):
        """Get screening results for a job"""
        try:
            job = JobDescription.query.get_or_404(job_id)
            candidates = Candidate.query.filter_by(job_id=job_id, status='processed')\
                                       .order_by(Candidate.rank).all()
            
            results = {
                'job': job.to_dict(),
                'candidates': [c.to_dict() for c in candidates],
                'total_candidates': len(candidates),
                'average_score': sum(c.match_score for c in candidates) / len(candidates) if candidates else 0
            }
            
            return jsonify(results), 200
            
        except Exception as e:
            logger.error(f"Failed to get results: {str(e)}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    @app.route('/api/jobs/<int:job_id>/report')
    def download_report(job_id):
        """Generate and download screening report"""
        try:
            job = JobDescription.query.get_or_404(job_id)
            candidates = Candidate.query.filter_by(job_id=job_id, status='processed')\
                                       .order_by(Candidate.rank).all()
            
            job_data = job.to_dict()
            candidates_data = [c.to_dict() for c in candidates]
            
            # Generate report
            report_path = app.report_generator.generate_screening_report(
                job_data, candidates_data
            )
            
            return send_file(
                report_path,
                as_attachment=True,
                download_name=os.path.basename(report_path)
            )
            
        except Exception as e:
            logger.error(f"Failed to generate report: {str(e)}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    @app.route('/api/health')
    def health_check():
        """Health check endpoint"""
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat()
        }), 200
    
    return app



if __name__ == '__main__':
    app = create_app(os.getenv('FLASK_ENV', 'development'))
    app.run(debug=True, host='0.0.0.0', port=5000)

# Made with Bob
