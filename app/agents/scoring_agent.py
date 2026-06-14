"""
Scoring Agent - Calculates match percentage and ranks candidates
Uses IBM Granite model and weighted scoring algorithm
"""

import json
import logging
import re
from typing import Dict, Any, List

logger = logging.getLogger(__name__)


class ScoringAgent:
    """Agent responsible for scoring and ranking candidates"""
    
    def __init__(self, watsonx_client, config):
        """
        Initialize Scoring Agent
        
        Args:
            watsonx_client: WatsonxClient instance
            config: Configuration object
        """
        self.client = watsonx_client
        self.config = config
        self.prompt_template = config.SCORING_AGENT_PROMPT
        self.weights = config.SCORING_WEIGHTS
    
    def calculate_score(self, candidate_data: Dict[str, Any], 
                       match_data: Dict[str, Any],
                       job_description: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate comprehensive match score for candidate
        
        Args:
            candidate_data (dict): Parsed candidate information
            match_data (dict): Matching analysis results
            job_description (dict): Job requirements
            
        Returns:
            dict: Scoring results with breakdown
        """
        try:
            logger.info(f"Calculating score for: {candidate_data.get('name', 'Unknown')}")
            
            # Calculate component scores
            skills_score = self._calculate_skills_score(match_data)
            experience_score = self._calculate_experience_score(candidate_data, match_data, job_description)
            education_score = self._calculate_education_score(candidate_data, match_data, job_description)
            additional_score = self._calculate_additional_score(candidate_data, match_data)
            
            # Calculate weighted total score
            total_score = (
                skills_score * self.weights['skills'] +
                experience_score * self.weights['experience'] +
                education_score * self.weights['education'] +
                additional_score * self.weights['additional']
            )
            
            # Use AI to validate and enhance scoring
            ai_score = self._get_ai_score_validation(
                candidate_data, match_data, job_description,
                skills_score, experience_score, education_score, total_score
            )
            
            # Prepare final score data
            score_data = {
                'total_score': round(total_score, 2),
                'skills_score': round(skills_score, 2),
                'experience_score': round(experience_score, 2),
                'education_score': round(education_score, 2),
                'additional_score': round(additional_score, 2),
                'ai_adjusted_score': round(ai_score, 2),
                'score_breakdown': self._create_score_breakdown(
                    skills_score, experience_score, education_score, additional_score
                )
            }
            
            logger.info(f"Score calculated: {total_score:.2f}%")
            return score_data
            
        except Exception as e:
            logger.error(f"Score calculation failed: {str(e)}")
            return self._get_default_score_structure()
    
    def _calculate_skills_score(self, match_data: Dict[str, Any]) -> float:
        """
        Calculate skills match score (0-100)
        
        Args:
            match_data (dict): Matching analysis results
            
        Returns:
            float: Skills score
        """
        matching_skills = match_data.get('matching_skills', [])
        missing_skills = match_data.get('missing_skills', [])
        
        if not matching_skills and not missing_skills:
            return 50.0  # Default if no data
        
        total_required = len(matching_skills) + len(missing_skills)
        if total_required == 0:
            return 50.0
        
        match_percentage = (len(matching_skills) / total_required) * 100
        
        # Bonus for having many matching skills
        if len(matching_skills) >= 5:
            match_percentage = min(100, match_percentage + 10)
        
        return match_percentage
    
    def _calculate_experience_score(self, candidate_data: Dict[str, Any],
                                    match_data: Dict[str, Any],
                                    job_description: Dict[str, Any]) -> float:
        """
        Calculate experience relevance score (0-100)
        
        Args:
            candidate_data (dict): Candidate information
            match_data (dict): Matching analysis results
            job_description (dict): Job requirements
            
        Returns:
            float: Experience score
        """
        experience_list = candidate_data.get('experience', [])
        experience_relevance = match_data.get('experience_relevance', 'Unknown').lower()
        
        # Base score from AI analysis
        relevance_scores = {
            'high': 90,
            'medium': 65,
            'low': 35,
            'unknown': 50
        }
        base_score = relevance_scores.get(experience_relevance, 50)
        
        # Adjust based on number of experiences
        if len(experience_list) >= 3:
            base_score = min(100, base_score + 10)
        elif len(experience_list) == 0:
            base_score = max(0, base_score - 20)
        
        return float(base_score)
    
    def _calculate_education_score(self, candidate_data: Dict[str, Any],
                                   match_data: Dict[str, Any],
                                   job_description: Dict[str, Any]) -> float:
        """
        Calculate education match score (0-100)
        
        Args:
            candidate_data (dict): Candidate information
            match_data (dict): Matching analysis results
            job_description (dict): Job requirements
            
        Returns:
            float: Education score
        """
        education_list = candidate_data.get('education', [])
        education_match = match_data.get('education_match', 'Unknown').lower()
        
        # Base score from AI analysis
        match_scores = {
            'yes': 100,
            'partial': 70,
            'no': 30,
            'unknown': 50
        }
        base_score = match_scores.get(education_match, 50)
        
        # Adjust based on education level
        if len(education_list) >= 2:
            base_score = min(100, base_score + 10)
        elif len(education_list) == 0:
            base_score = max(0, base_score - 30)
        
        return float(base_score)
    
    def _calculate_additional_score(self, candidate_data: Dict[str, Any],
                                    match_data: Dict[str, Any]) -> float:
        """
        Calculate additional factors score (0-100)
        
        Args:
            candidate_data (dict): Candidate information
            match_data (dict): Matching analysis results
            
        Returns:
            float: Additional score
        """
        score = 50.0  # Base score
        
        # Certifications bonus
        certifications = candidate_data.get('certifications', [])
        if len(certifications) > 0:
            score += min(20, len(certifications) * 5)
        
        # Key strengths bonus
        strengths = match_data.get('key_strengths', [])
        if len(strengths) >= 3:
            score += 15
        elif len(strengths) >= 1:
            score += 10
        
        # Penalty for areas of concern
        concerns = match_data.get('areas_of_concern', [])
        if len(concerns) > 3:
            score -= 15
        elif len(concerns) > 0:
            score -= 5
        
        return max(0, min(100, score))
    
    def _get_ai_score_validation(self, candidate_data: Dict[str, Any],
                                 match_data: Dict[str, Any],
                                 job_description: Dict[str, Any],
                                 skills_score: float,
                                 experience_score: float,
                                 education_score: float,
                                 total_score: float) -> float:
        """
        Use AI to validate and potentially adjust the calculated score
        
        Args:
            candidate_data (dict): Candidate information
            match_data (dict): Matching analysis results
            job_description (dict): Job requirements
            skills_score (float): Calculated skills score
            experience_score (float): Calculated experience score
            education_score (float): Calculated education score
            total_score (float): Calculated total score
            
        Returns:
            float: AI-adjusted score
        """
        try:
            prompt = f"""{self.prompt_template}

Candidate: {candidate_data.get('name', 'Unknown')}
Job: {job_description.get('title', 'Unknown')}

Calculated Scores:
- Skills: {skills_score:.1f}%
- Experience: {experience_score:.1f}%
- Education: {education_score:.1f}%
- Total: {total_score:.1f}%

Match Analysis:
- Matching Skills: {len(match_data.get('matching_skills', []))}
- Missing Skills: {len(match_data.get('missing_skills', []))}
- Experience Relevance: {match_data.get('experience_relevance', 'Unknown')}
- Education Match: {match_data.get('education_match', 'Unknown')}
- Overall Fit: {match_data.get('overall_fit', 'Unknown')}

Based on this analysis, provide a final adjusted score (0-100) that best represents the candidate's match.
Return only a number between 0 and 100.
"""
            
            response = self.client.generate_text(prompt, max_tokens=50)
            
            # Extract number from response
            numbers = re.findall(r'\d+\.?\d*', response)
            if numbers:
                ai_score = float(numbers[0])
                # Ensure score is within bounds
                ai_score = max(0, min(100, ai_score))
                # Don't deviate too much from calculated score
                if abs(ai_score - total_score) > 20:
                    ai_score = total_score
                return ai_score
            
        except Exception as e:
            logger.warning(f"AI score validation failed: {str(e)}")
        
        return total_score
    
    def _create_score_breakdown(self, skills_score: float, experience_score: float,
                               education_score: float, additional_score: float) -> str:
        """
        Create human-readable score breakdown
        
        Args:
            skills_score (float): Skills score
            experience_score (float): Experience score
            education_score (float): Education score
            additional_score (float): Additional score
            
        Returns:
            str: Score breakdown text
        """
        breakdown = f"""Score Breakdown:
• Skills Match: {skills_score:.1f}% (Weight: {self.weights['skills']*100:.0f}%)
• Experience Relevance: {experience_score:.1f}% (Weight: {self.weights['experience']*100:.0f}%)
• Education Alignment: {education_score:.1f}% (Weight: {self.weights['education']*100:.0f}%)
• Additional Factors: {additional_score:.1f}% (Weight: {self.weights['additional']*100:.0f}%)
"""
        return breakdown
    
    def _get_default_score_structure(self) -> Dict[str, Any]:
        """
        Get default score structure
        
        Returns:
            dict: Default structure
        """
        return {
            'total_score': 0.0,
            'skills_score': 0.0,
            'experience_score': 0.0,
            'education_score': 0.0,
            'additional_score': 0.0,
            'ai_adjusted_score': 0.0,
            'score_breakdown': 'Unable to calculate score'
        }
    
    @staticmethod
    def rank_candidates(candidates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Rank candidates by their scores
        
        Args:
            candidates (list): List of candidate dictionaries with scores
            
        Returns:
            list: Sorted and ranked candidates
        """
        # Sort by total_score in descending order
        sorted_candidates = sorted(
            candidates,
            key=lambda x: x.get('match_score', 0),
            reverse=True
        )
        
        # Assign ranks
        for rank, candidate in enumerate(sorted_candidates, start=1):
            candidate['rank'] = rank
        
        return sorted_candidates

# Made with Bob
