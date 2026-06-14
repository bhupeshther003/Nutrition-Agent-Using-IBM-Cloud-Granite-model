"""
Feedback Agent - Generates detailed hiring insights and recommendations
Uses IBM Granite model to provide actionable feedback
"""

import json
import logging
import re
from typing import Dict, Any

logger = logging.getLogger(__name__)


class FeedbackAgent:
    """Agent responsible for generating detailed feedback and recommendations"""
    
    def __init__(self, watsonx_client, config):
        """
        Initialize Feedback Agent
        
        Args:
            watsonx_client: WatsonxClient instance
            config: Configuration object
        """
        self.client = watsonx_client
        self.config = config
        self.prompt_template = config.FEEDBACK_AGENT_PROMPT
    
    def generate_feedback(self, candidate_data: Dict[str, Any],
                         match_data: Dict[str, Any],
                         score_data: Dict[str, Any],
                         job_description: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate comprehensive feedback for candidate
        
        Args:
            candidate_data (dict): Parsed candidate information
            match_data (dict): Matching analysis results
            score_data (dict): Scoring results
            job_description (dict): Job requirements
            
        Returns:
            dict: Detailed feedback and recommendations
        """
        try:
            logger.info(f"Generating feedback for: {candidate_data.get('name', 'Unknown')}")
            
            # Create feedback prompt
            prompt = self._create_feedback_prompt(
                candidate_data, match_data, score_data, job_description
            )
            
            # Generate feedback from AI
            response = self.client.generate_with_retry(prompt, max_tokens=1500)
            
            # Parse and structure the feedback
            feedback_data = self._parse_feedback_response(response)
            
            # Enhance with additional insights
            feedback_data = self._enhance_feedback(
                feedback_data, candidate_data, match_data, score_data
            )
            
            logger.info("Feedback generation completed successfully")
            return feedback_data
            
        except Exception as e:
            logger.error(f"Feedback generation failed: {str(e)}")
            return self._get_default_feedback_structure()
    
    def _create_feedback_prompt(self, candidate_data: Dict[str, Any],
                               match_data: Dict[str, Any],
                               score_data: Dict[str, Any],
                               job_description: Dict[str, Any]) -> str:
        """
        Create detailed prompt for feedback generation
        
        Args:
            candidate_data (dict): Candidate information
            match_data (dict): Matching analysis results
            score_data (dict): Scoring results
            job_description (dict): Job requirements
            
        Returns:
            str: Formatted prompt
        """
        prompt = f"""{self.prompt_template}

Job Position: {job_description.get('title', 'N/A')}

Candidate: {candidate_data.get('name', 'Unknown')}
Match Score: {score_data.get('total_score', 0):.1f}%

Detailed Analysis:
- Skills Score: {score_data.get('skills_score', 0):.1f}%
- Experience Score: {score_data.get('experience_score', 0):.1f}%
- Education Score: {score_data.get('education_score', 0):.1f}%

Matching Skills: {', '.join(match_data.get('matching_skills', [])[:10])}
Missing Skills: {', '.join(match_data.get('missing_skills', [])[:10])}

Experience Relevance: {match_data.get('experience_relevance', 'Unknown')}
Education Match: {match_data.get('education_match', 'Unknown')}
Overall Fit: {match_data.get('overall_fit', 'Unknown')}

Key Strengths: {', '.join(match_data.get('key_strengths', []))}
Areas of Concern: {', '.join(match_data.get('areas_of_concern', []))}

Generate a comprehensive hiring assessment with:
1. Executive Summary (2-3 sentences explaining why this candidate scored {score_data.get('total_score', 0):.1f}%)
2. Top 3-5 Strengths (specific and detailed)
3. Top 3-5 Gaps or Areas for Development
4. Hiring Recommendation (Strong Hire/Hire/Consider/Pass with justification)
5. Interview Focus Areas (3-5 specific topics to explore)
6. Onboarding Suggestions (if hired, what training/support needed)

Return as JSON:
{{
    "executive_summary": "...",
    "strengths": ["strength1", "strength2", "strength3"],
    "gaps": ["gap1", "gap2", "gap3"],
    "recommendation": "Strong Hire/Hire/Consider/Pass",
    "recommendation_justification": "...",
    "interview_focus": ["topic1", "topic2", "topic3"],
    "onboarding_suggestions": ["suggestion1", "suggestion2"]
}}

Return ONLY the JSON object.
"""
        return prompt
    
    def _parse_feedback_response(self, response: str) -> Dict[str, Any]:
        """
        Parse feedback from AI response
        
        Args:
            response (str): AI response
            
        Returns:
            dict: Parsed feedback data
        """
        try:
            # Try to find JSON in the response
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                return json.loads(json_str)
            else:
                return json.loads(response)
        except json.JSONDecodeError as e:
            logger.warning(f"Failed to parse JSON from feedback response: {str(e)}")
            # Try to extract information from text
            return self._extract_feedback_from_text(response)
    
    def _extract_feedback_from_text(self, text: str) -> Dict[str, Any]:
        """
        Extract feedback information from unstructured text
        
        Args:
            text (str): Response text
            
        Returns:
            dict: Extracted feedback
        """
        feedback = self._get_default_feedback_structure()
        
        # Try to extract summary
        summary_match = re.search(r'(?:summary|overview)[:\s]+(.+?)(?:\n\n|\n[A-Z])', text, re.IGNORECASE | re.DOTALL)
        if summary_match:
            feedback['executive_summary'] = summary_match.group(1).strip()[:500]
        
        # Try to extract recommendation
        rec_match = re.search(r'(?:recommendation|verdict)[:\s]+(Strong Hire|Hire|Consider|Pass)', text, re.IGNORECASE)
        if rec_match:
            feedback['recommendation'] = rec_match.group(1)
        
        return feedback
    
    def _enhance_feedback(self, feedback_data: Dict[str, Any],
                         candidate_data: Dict[str, Any],
                         match_data: Dict[str, Any],
                         score_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enhance feedback with additional insights
        
        Args:
            feedback_data (dict): Initial feedback
            candidate_data (dict): Candidate information
            match_data (dict): Matching analysis results
            score_data (dict): Scoring results
            
        Returns:
            dict: Enhanced feedback
        """
        # Ensure all required fields exist
        default = self._get_default_feedback_structure()
        for key in default.keys():
            if key not in feedback_data:
                feedback_data[key] = default[key]
        
        # Add strengths from match data if not present
        if not feedback_data.get('strengths') or len(feedback_data['strengths']) == 0:
            feedback_data['strengths'] = match_data.get('key_strengths', [])[:5]
        
        # Add gaps from match data if not present
        if not feedback_data.get('gaps') or len(feedback_data['gaps']) == 0:
            gaps = []
            missing_skills = match_data.get('missing_skills', [])
            if missing_skills:
                gaps.append(f"Missing {len(missing_skills)} required skills: {', '.join(missing_skills[:3])}")
            concerns = match_data.get('areas_of_concern', [])
            gaps.extend(concerns[:4])
            feedback_data['gaps'] = gaps
        
        # Generate recommendation if not present
        if not feedback_data.get('recommendation') or feedback_data['recommendation'] == 'Unknown':
            feedback_data['recommendation'] = self._determine_recommendation(score_data)
        
        # Generate detailed explanation
        feedback_data['detailed_explanation'] = self._create_detailed_explanation(
            candidate_data, match_data, score_data, feedback_data
        )
        
        return feedback_data
    
    def _determine_recommendation(self, score_data: Dict[str, Any]) -> str:
        """
        Determine hiring recommendation based on score
        
        Args:
            score_data (dict): Scoring results
            
        Returns:
            str: Recommendation
        """
        score = score_data.get('total_score', 0)
        
        if score >= 85:
            return 'Strong Hire'
        elif score >= 70:
            return 'Hire'
        elif score >= 50:
            return 'Consider'
        else:
            return 'Pass'
    
    def _create_detailed_explanation(self, candidate_data: Dict[str, Any],
                                    match_data: Dict[str, Any],
                                    score_data: Dict[str, Any],
                                    feedback_data: Dict[str, Any]) -> str:
        """
        Create detailed explanation of the assessment
        
        Args:
            candidate_data (dict): Candidate information
            match_data (dict): Matching analysis results
            score_data (dict): Scoring results
            feedback_data (dict): Feedback data
            
        Returns:
            str: Detailed explanation
        """
        name = candidate_data.get('name', 'This candidate')
        score = score_data.get('total_score', 0)
        recommendation = feedback_data.get('recommendation', 'Unknown')
        
        # Build explanation
        explanation = f"{name} matches {score:.1f}% with the job requirements. "
        
        # Add score context
        if score >= 85:
            explanation += "This is an excellent match with strong alignment across all key areas. "
        elif score >= 70:
            explanation += "This is a good match with solid qualifications. "
        elif score >= 50:
            explanation += "This is a moderate match with some gaps to consider. "
        else:
            explanation += "This match has significant gaps in key requirements. "
        
        # Add skills context
        matching_skills = match_data.get('matching_skills', [])
        missing_skills = match_data.get('missing_skills', [])
        
        if matching_skills:
            explanation += f"The candidate demonstrates {len(matching_skills)} of the required skills including {', '.join(matching_skills[:3])}. "
        
        if missing_skills:
            explanation += f"However, {len(missing_skills)} required skills are missing: {', '.join(missing_skills[:3])}. "
        
        # Add experience context
        exp_relevance = match_data.get('experience_relevance', 'Unknown')
        if exp_relevance.lower() == 'high':
            explanation += "Their experience is highly relevant to the role. "
        elif exp_relevance.lower() == 'medium':
            explanation += "Their experience is moderately relevant. "
        elif exp_relevance.lower() == 'low':
            explanation += "Their experience has limited relevance to this role. "
        
        # Add recommendation context
        explanation += f"Overall recommendation: {recommendation}."
        
        return explanation
    
    def _get_default_feedback_structure(self) -> Dict[str, Any]:
        """
        Get default feedback structure
        
        Returns:
            dict: Default structure
        """
        return {
            'executive_summary': 'Unable to generate summary',
            'strengths': [],
            'gaps': [],
            'recommendation': 'Unknown',
            'recommendation_justification': 'Unable to generate justification',
            'interview_focus': [],
            'onboarding_suggestions': [],
            'detailed_explanation': 'Unable to generate detailed explanation'
        }

# Made with Bob
