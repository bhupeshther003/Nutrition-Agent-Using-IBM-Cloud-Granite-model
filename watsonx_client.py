from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
from typing import List, Dict
from config import Config

from dotenv import load_dotenv

class WatsonxClient:
    """Client for IBM Watsonx.ai integration"""
    
    def __init__(self):
        """Initialize Watsonx client"""
        if not Config.WATSONX_API_KEY or not Config.WATSONX_PROJECT_ID:
            raise ValueError("Watsonx API key and Project ID must be set in environment variables")
        
        # Set up credentials
        self.credentials = Credentials(
            url=Config.WATSONX_URL,
            api_key=Config.WATSONX_API_KEY
        )
        
        # Initialize API client
        self.client = APIClient(self.credentials)
        self.client.set.default_project(Config.WATSONX_PROJECT_ID)
        
        # Initialize model
        self.model = ModelInference(
            model_id=Config.WATSONX_MODEL_ID,
            api_client=self.client,
            project_id=Config.WATSONX_PROJECT_ID
        )
    
    def generate_answer(self, question: str, context: List[Dict]) -> Dict:
        """Generate answer using RAG approach"""
        
        # Prepare context from retrieved documents
        context_text = self._format_context(context)
        
        # Create prompt
        prompt = self._create_prompt(question, context_text)
        
        # Generate parameters
        params = {
            "max_new_tokens": Config.WATSONX_MAX_TOKENS,
            "temperature": Config.WATSONX_TEMPERATURE,
            "top_p": 0.9,
            "top_k": 50,
            "repetition_penalty": 1.1
        }
        
        try:
            # Generate response
            response = self.model.generate_text(
                prompt=prompt,
                params=params
            )
            
            # Extract sources
            sources = self._extract_sources(context)
            
            return {
                'answer': response.strip(),
                'sources': sources,
                'success': True
            }
        
        except Exception as e:
            return {
                'answer': f"Error generating response: {str(e)}",
                'sources': [],
                'success': False,
                'error': str(e)
            }
    
    def _format_context(self, context: List[Dict]) -> str:
        """Format retrieved context for the prompt"""
        if not context:
            return "No relevant information found in the company policies."
        
        formatted_context = []
        for i, doc in enumerate(context, 1):
            text = doc.get('text', '')
            doc_name = doc.get('metadata', {}).get('document_name', 'Unknown')
            formatted_context.append(f"[Source {i} - {doc_name}]\n{text}")
        
        return "\n\n".join(formatted_context)
    
    def _create_prompt(self, question: str, context: str) -> str:
        """Create prompt for the model"""
        prompt = f"""You are a helpful company policy assistant. Your role is to answer employee questions about company policies accurately based on the provided context.

Context from Company Policy Documents:
{context}

Employee Question: {question}

Instructions:
1. Answer the question based ONLY on the information provided in the context above
2. If the context doesn't contain enough information to answer the question, say so clearly
3. Be concise and professional
4. If relevant, mention which policy document the information comes from
5. Do not make up information that is not in the context

Answer:"""
        
        return prompt
    
    def _extract_sources(self, context: List[Dict]) -> List[Dict]:
        """Extract source information from context"""
        sources = []
        seen_docs = set()
        
        for doc in context:
            metadata = doc.get('metadata', {})
            doc_name = metadata.get('document_name', 'Unknown')
            
            if doc_name not in seen_docs:
                sources.append({
                    'document': doc_name,
                    'relevance': 1.0 - doc.get('distance', 0)  # Convert distance to relevance score
                })
                seen_docs.add(doc_name)
        
        return sources
    
    def test_connection(self) -> bool:
        """Test connection to Watsonx"""
        try:
            # Try a simple generation
            response = self.model.generate_text(
                prompt="Hello",
                params={"max_new_tokens": 10}
            )
            return True
        except Exception as e:
            print(f"Connection test failed: {str(e)}")
            return False

# Made with Bob
