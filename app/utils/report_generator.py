"""
Report generator for creating downloadable PDF reports
"""

import os
import logging
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
import json

logger = logging.getLogger(__name__)


class ReportGenerator:
    """Class for generating PDF reports of screening results"""
    
    def __init__(self, reports_folder='reports'):
        """
        Initialize Report Generator
        
        Args:
            reports_folder (str): Folder to save reports
        """
        self.reports_folder = reports_folder
        os.makedirs(reports_folder, exist_ok=True)
    
    def generate_screening_report(self, job_data, candidates_data, session_data=None):
        """
        Generate comprehensive screening report
        
        Args:
            job_data (dict): Job description data
            candidates_data (list): List of candidate dictionaries
            session_data (dict, optional): Screening session data
            
        Returns:
            str: Path to generated PDF file
        """
        try:
            # Create filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            job_title = job_data.get('title', 'Job').replace(' ', '_')
            filename = f"screening_report_{job_title}_{timestamp}.pdf"
            filepath = os.path.join(self.reports_folder, filename)
            
            # Create PDF document
            doc = SimpleDocTemplate(filepath, pagesize=letter,
                                   rightMargin=72, leftMargin=72,
                                   topMargin=72, bottomMargin=18)
            
            # Container for the 'Flowable' objects
            elements = []
            
            # Define styles
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                textColor=colors.HexColor('#1a237e'),
                spaceAfter=30,
                alignment=TA_CENTER
            )
            
            heading_style = ParagraphStyle(
                'CustomHeading',
                parent=styles['Heading2'],
                fontSize=16,
                textColor=colors.HexColor('#283593'),
                spaceAfter=12,
                spaceBefore=12
            )
            
            # Add title
            title = Paragraph("Resume Screening Report", title_style)
            elements.append(title)
            elements.append(Spacer(1, 12))
            
            # Add job information
            elements.append(Paragraph("Job Information", heading_style))
            job_info = [
                ['Job Title:', job_data.get('title', 'N/A')],
                ['Date:', datetime.now().strftime('%B %d, %Y')],
                ['Total Candidates:', str(len(candidates_data))],
            ]
            
            if session_data:
                job_info.append(['Session Status:', session_data.get('status', 'N/A')])
            
            job_table = Table(job_info, colWidths=[2*inch, 4*inch])
            job_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e8eaf6')),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey)
            ]))
            elements.append(job_table)
            elements.append(Spacer(1, 20))
            
            # Add summary statistics
            elements.append(Paragraph("Summary Statistics", heading_style))
            
            if candidates_data:
                avg_score = sum(c.get('match_score', 0) for c in candidates_data) / len(candidates_data)
                top_score = max(c.get('match_score', 0) for c in candidates_data)
                
                stats_data = [
                    ['Average Match Score:', f"{avg_score:.1f}%"],
                    ['Highest Score:', f"{top_score:.1f}%"],
                    ['Strong Candidates (≥85%):', str(sum(1 for c in candidates_data if c.get('match_score', 0) >= 85))],
                    ['Good Candidates (70-84%):', str(sum(1 for c in candidates_data if 70 <= c.get('match_score', 0) < 85))],
                ]
                
                stats_table = Table(stats_data, colWidths=[2.5*inch, 1.5*inch])
                stats_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e8eaf6')),
                    ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                    ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                    ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
                    ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                    ('TOPPADDING', (0, 0), (-1, -1), 8),
                    ('GRID', (0, 0), (-1, -1), 1, colors.grey)
                ]))
                elements.append(stats_table)
            
            elements.append(Spacer(1, 20))
            
            # Add candidate rankings
            elements.append(Paragraph("Candidate Rankings", heading_style))
            elements.append(Spacer(1, 12))
            
            # Sort candidates by score
            sorted_candidates = sorted(candidates_data, key=lambda x: x.get('match_score', 0), reverse=True)
            
            # Add each candidate
            for idx, candidate in enumerate(sorted_candidates[:10], 1):  # Top 10 candidates
                self._add_candidate_section(elements, candidate, idx, styles)
                if idx < len(sorted_candidates) and idx < 10:
                    elements.append(Spacer(1, 15))
            
            # Build PDF
            doc.build(elements)
            
            logger.info(f"Report generated successfully: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Failed to generate report: {str(e)}")
            raise
    
    def _add_candidate_section(self, elements, candidate, rank, styles):
        """
        Add candidate section to report
        
        Args:
            elements (list): List of flowable elements
            candidate (dict): Candidate data
            rank (int): Candidate rank
            styles: ReportLab styles
        """
        # Candidate header
        name = candidate.get('name', 'Unknown')
        score = candidate.get('match_score', 0)
        
        # Determine color based on score
        if score >= 85:
            color = colors.HexColor('#2e7d32')  # Green
        elif score >= 70:
            color = colors.HexColor('#1976d2')  # Blue
        elif score >= 50:
            color = colors.HexColor('#f57c00')  # Orange
        else:
            color = colors.HexColor('#c62828')  # Red
        
        candidate_style = ParagraphStyle(
            'CandidateHeader',
            parent=styles['Heading3'],
            fontSize=14,
            textColor=color,
            spaceAfter=8
        )
        
        header_text = f"#{rank}. {name} - {score:.1f}% Match"
        elements.append(Paragraph(header_text, candidate_style))
        
        # Candidate details table
        details_data = [
            ['Email:', candidate.get('email', 'N/A')],
            ['Phone:', candidate.get('phone', 'N/A')],
        ]
        
        # Parse skills if JSON string
        skills = candidate.get('skills', '[]')
        if isinstance(skills, str):
            try:
                skills = json.loads(skills)
            except:
                skills = []
        
        if skills:
            details_data.append(['Skills:', ', '.join(skills[:5])])
        
        details_table = Table(details_data, colWidths=[1.2*inch, 4.8*inch])
        details_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
        ]))
        elements.append(details_table)
        elements.append(Spacer(1, 8))
        
        # Score breakdown
        score_data = [
            ['Skills:', f"{candidate.get('skills_score', 0):.1f}%"],
            ['Experience:', f"{candidate.get('experience_score', 0):.1f}%"],
            ['Education:', f"{candidate.get('education_score', 0):.1f}%"],
        ]
        
        score_table = Table(score_data, colWidths=[1.5*inch, 1*inch])
        score_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f5f5f5')),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
        ]))
        elements.append(score_table)
        
        # Add feedback if available
        feedback = candidate.get('detailed_feedback', '')
        if feedback:
            elements.append(Spacer(1, 8))
            feedback_style = ParagraphStyle(
                'Feedback',
                parent=styles['Normal'],
                fontSize=9,
                textColor=colors.HexColor('#424242')
            )
            elements.append(Paragraph(f"<b>Assessment:</b> {feedback[:300]}...", feedback_style))
    
    def generate_candidate_report(self, candidate_data, job_data):
        """
        Generate individual candidate report
        
        Args:
            candidate_data (dict): Candidate data
            job_data (dict): Job description data
            
        Returns:
            str: Path to generated PDF file
        """
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            name = candidate_data.get('name', 'Candidate').replace(' ', '_')
            filename = f"candidate_report_{name}_{timestamp}.pdf"
            filepath = os.path.join(self.reports_folder, filename)
            
            doc = SimpleDocTemplate(filepath, pagesize=letter)
            elements = []
            styles = getSampleStyleSheet()
            
            # Add title
            title = Paragraph(f"Candidate Assessment Report: {candidate_data.get('name', 'Unknown')}", 
                            styles['Title'])
            elements.append(title)
            elements.append(Spacer(1, 20))
            
            # Add detailed information
            # (Similar structure to above but more detailed for individual candidate)
            
            doc.build(elements)
            logger.info(f"Candidate report generated: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Failed to generate candidate report: {str(e)}")
            raise

# Made with Bob
