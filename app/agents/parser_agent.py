"""
Parser Agent - Extracts structured information from resumes
Uses IBM Granite model to parse resume text into structured data
"""

import json
import logging
import re
from typing import Dict, Any

logger = logging.getLogger(__name__)


class ParserAgent:
    """Agent responsible for parsing resume text into structured data"""
    
    def __init__(self, watsonx_client, config):
        """
        Initialize Parser Agent
        
        Args:
            watsonx_client: WatsonxClient instance
            config: Configuration object
        """
        self.client = watsonx_client
        self.config = config
        self.prompt_template = config.PARSER_AGENT_PROMPT
    
    def parse_resume(self, resume_text: str) -> Dict[str, Any]:
        """
        Parse resume text and extract structured information
        
        Args:
            resume_text (str): Raw resume text
            
        Returns:
            dict: Structured candidate information
        """
        try:
            logger.info("Starting resume parsing...")
            
            # Create prompt for the model
            prompt = self._create_parsing_prompt(resume_text)
            
            # Generate response from Granite model
            response = self.client.generate_with_retry(prompt, max_tokens=1500)
            
            # Parse the response
            parsed_data = self._extract_json_from_response(response)
            
            # Validate and clean the parsed data
            validated_data = self._validate_parsed_data(parsed_data)
            
            logger.info("Resume parsing completed successfully")
            return validated_data
            
        except Exception as e:
            logger.error(f"Resume parsing failed: {str(e)}")
            return self._get_default_structure()
    
    def _create_parsing_prompt(self, resume_text: str) -> str:
        """
        Create a detailed prompt for resume parsing
        
        Args:
            resume_text (str): Raw resume text
            
        Returns:
            str: Formatted prompt
        """
        prompt = f"""{self.prompt_template}

Resume Text:
{resume_text[:4000]}  # Limit text to avoid token limits

Please extract and return the following information in valid JSON format:
{{
    "name": "Full name of the candidate",
    "email": "Email address",
    "phone": "Phone number",
    "skills": ["skill1", "skill2", "skill3"],
    "education": [
        {{
            "degree": "Degree name",
            "institution": "University/College name",
            "year": "Graduation year",
            "field": "Field of study"
        }}
    ],
    "experience": [
        {{
            "company": "Company name",
            "position": "Job title",
            "duration": "Time period",
            "responsibilities": ["responsibility1", "responsibility2"]
        }}
    ],
    "certifications": ["certification1", "certification2"],
    "summary": "Brief professional summary"
}}

Return ONLY the JSON object, no additional text.
"""
        return prompt
    
    def _extract_json_from_response(self, response: str) -> Dict[str, Any]:
        """
        Extract JSON from model response
        
        Args:
            response (str): Model response
            
        Returns:
            dict: Parsed JSON data
        """
        try:
            # Try to find JSON in the response
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                return json.loads(json_str)
            else:
                # If no JSON found, try parsing the entire response
                return json.loads(response)
        except json.JSONDecodeError as e:
            logger.warning(f"Failed to parse JSON from response: {str(e)}")
            # Try to extract information using regex as fallback
            return self._fallback_extraction(response)
    
    def _fallback_extraction(self, text: str) -> Dict[str, Any]:
        """
        Fallback method to extract information using regex
        
        Args:
            text (str): Text to extract from
            
        Returns:
            dict: Extracted information
        """
        data = self._get_default_structure()
        
        # Extract email
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        if emails:
            data['email'] = emails[0]
        
        # Extract phone
        phone_pattern = r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]'
        phones = re.findall(phone_pattern, text)
        if phones:
            data['phone'] = phones[0]
        
        # Extract name (first line often contains name)
        lines = text.split('\n')
        if lines:
            data['name'] = lines[0].strip()
        
        return data
    
    def _validate_parsed_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate and clean parsed data
        
        Args:
            data (dict): Parsed data
            
        Returns:
            dict: Validated data
        """
        default = self._get_default_structure()
        
        # Ensure all required fields exist
        for key in default.keys():
            if key not in data:
                data[key] = default[key]
        
        # Validate data types
        if not isinstance(data.get('skills'), list):
            data['skills'] = []
        
        if not isinstance(data.get('education'), list):
            data['education'] = []
        
        if not isinstance(data.get('experience'), list):
            data['experience'] = []
        
        if not isinstance(data.get('certifications'), list):
            data['certifications'] = []
        
        # Clean strings
        for key in ['name', 'email', 'phone', 'summary']:
            if isinstance(data.get(key), str):
                data[key] = data[key].strip()
        
        return data
    
    def _get_default_structure(self) -> Dict[str, Any]:
        """
        Get default data structure
        
        Returns:
            dict: Default structure
        """
        return {
            'name': '',
            'email': '',
            'phone': '',
            'skills': [],
            'education': [],
            'experience': [],
            'certifications': [],
            'summary': ''
        }

# Made with Bob
