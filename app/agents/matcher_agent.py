"""
Matcher Agent - Compares candidate profiles with job requirements
Uses IBM Granite model to analyze skill matches and experience relevance
"""

import json
import logging
import re
from typing import Dict, Any, List

logger = logging.getLogger(__name__)


class MatcherAgent:
    """Agent responsible for matching candidates with job requirements"""
    
    def __init__(self, watsonx_client, config):
        """
        Initialize Matcher Agent
        
        Args:
            watsonx_client: WatsonxClient instance
            config: Configuration object
        """
        self.client = watsonx_client
        self.config = config
        self.prompt_template = config.MATCHER_AGENT_PROMPT
    
    def match_candidate(self, candidate_data: Dict[str, Any], job_description: Dict[str, Any]) -> Dict[str, Any]:
        """
        Match candidate profile with job requirements
        
        Args:
            candidate_data (dict): Parsed candidate information
            job_description (dict): Job requirements
            
        Returns:
            dict: Matching analysis results
        """
        try:
            logger.info(f"Starting candidate matching for: {candidate_data.get('name', 'Unknown')}")
            
            # Create matching prompt
            prompt = self._create_matching_prompt(candidate_data, job_description)
            
            # Generate matching analysis
            response = self.client.generate_with_retry(prompt, max_tokens=1200)
            
            # Parse the response
            match_data = self._extract_match_data(response)
            
            # Perform additional analysis
            match_data = self._enhance_match_analysis(match_data, candidate_data, job_description)
            
            logger.info("Candidate matching completed successfully")
            return match_data
            
        except Exception as e:
            logger.error(f"Candidate matching failed: {str(e)}")
            return self._get_default_match_structure()
    
    def _create_matching_prompt(self, candidate_data: Dict[str, Any], job_description: Dict[str, Any]) -> str:
        """
        Create prompt for matching analysis
        
        Args:
            candidate_data (dict): Candidate information
            job_description (dict): Job requirements
            
        Returns:
            str: Formatted prompt
        """
        prompt = f"""{self.prompt_template}

Job Requirements:
Title: {job_description.get('title', 'N/A')}
Description: {job_description.get('description', 'N/A')[:1000]}
Required Skills: {job_description.get('required_skills', 'N/A')}
Required Experience: {job_description.get('required_experience', 'N/A')}
Required Education: {job_description.get('required_education', 'N/A')}

Candidate Profile:
Name: {candidate_data.get('name', 'N/A')}
Skills: {', '.join(candidate_data.get('skills', []))}
Experience: {json.dumps(candidate_data.get('experience', [])[:3])}
Education: {json.dumps(candidate_data.get('education', []))}
Summary: {candidate_data.get('summary', 'N/A')[:500]}

Analyze the match and return a JSON object with:
{{
    "matching_skills": ["skill1", "skill2"],
    "missing_skills": ["skill1", "skill2"],
    "experience_relevance": "High/Medium/Low",
    "experience_analysis": "Brief analysis of experience match",
    "education_match": "Yes/Partial/No",
    "education_analysis": "Brief analysis of education match",
    "overall_fit": "Excellent/Good/Fair/Poor",
    "key_strengths": ["strength1", "strength2"],
    "areas_of_concern": ["concern1", "concern2"]
}}

Return ONLY the JSON object.
"""
        return prompt
    
    def _extract_match_data(self, response: str) -> Dict[str, Any]:
        """
        Extract matching data from model response
        
        Args:
            response (str): Model response
            
        Returns:
            dict: Parsed matching data
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
            logger.warning(f"Failed to parse JSON from matching response: {str(e)}")
            return self._get_default_match_structure()
    
    def _enhance_match_analysis(self, match_data: Dict[str, Any], 
                                candidate_data: Dict[str, Any], 
                                job_description: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enhance match analysis with additional calculations
        
        Args:
            match_data (dict): Initial match data
            candidate_data (dict): Candidate information
            job_description (dict): Job requirements
            
        Returns:
            dict: Enhanced match data
        """
        # Ensure all required fields exist
        default = self._get_default_match_structure()
        for key in default.keys():
            if key not in match_data:
                match_data[key] = default[key]
        
        # Calculate skill match if not already done
        if not match_data.get('matching_skills'):
            match_data['matching_skills'] = self._calculate_skill_match(
                candidate_data.get('skills', []),
                job_description.get('required_skills', '')
            )
        
        # Calculate missing skills
        if not match_data.get('missing_skills'):
            match_data['missing_skills'] = self._calculate_missing_skills(
                candidate_data.get('skills', []),
                job_description.get('required_skills', ''),
                match_data.get('matching_skills', [])
            )
        
        return match_data
    
    def _calculate_skill_match(self, candidate_skills: List[str], required_skills: str) -> List[str]:
        """
        Calculate matching skills between candidate and job
        
        Args:
            candidate_skills (list): Candidate's skills
            required_skills (str): Required skills string
            
        Returns:
            list: Matching skills
        """
        if not required_skills:
            return []
        
        # Parse required skills (could be JSON or comma-separated)
        try:
            required = json.loads(required_skills)
            if isinstance(required, list):
                required_list = [s.lower().strip() for s in required]
            else:
                required_list = [required_skills.lower()]
        except:
            required_list = [s.lower().strip() for s in required_skills.split(',')]
        
        # Find matches
        candidate_lower = [s.lower().strip() for s in candidate_skills]
        matching = []
        
        for req_skill in required_list:
            for cand_skill in candidate_lower:
                if req_skill in cand_skill or cand_skill in req_skill:
                    matching.append(req_skill)
                    break
        
        return matching
    
    def _calculate_missing_skills(self, candidate_skills: List[str], 
                                  required_skills: str, 
                                  matching_skills: List[str]) -> List[str]:
        """
        Calculate missing skills
        
        Args:
            candidate_skills (list): Candidate's skills
            required_skills (str): Required skills string
            matching_skills (list): Already matched skills
            
        Returns:
            list: Missing skills
        """
        if not required_skills:
            return []
        
        try:
            required = json.loads(required_skills)
            if isinstance(required, list):
                required_list = [s.lower().strip() for s in required]
            else:
                required_list = [required_skills.lower()]
        except:
            required_list = [s.lower().strip() for s in required_skills.split(',')]
        
        matching_lower = [s.lower().strip() for s in matching_skills]
        missing = [skill for skill in required_list if skill not in matching_lower]
        
        return missing[:10]  # Limit to top 10 missing skills
    
    def _get_default_match_structure(self) -> Dict[str, Any]:
        """
        Get default match structure
        
        Returns:
            dict: Default structure
        """
        return {
            'matching_skills': [],
            'missing_skills': [],
            'experience_relevance': 'Unknown',
            'experience_analysis': 'Unable to analyze',
            'education_match': 'Unknown',
            'education_analysis': 'Unable to analyze',
            'overall_fit': 'Unknown',
            'key_strengths': [],
            'areas_of_concern': []
        }

# Made with Bob
