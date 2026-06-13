import os
import PyPDF2
from docx import Document
from typing import List, Dict
import re

class DocumentProcessor:
    """Process and extract text from various document formats"""
    
    @staticmethod
    def extract_text_from_pdf(file_path: str) -> str:
        """Extract text from PDF file"""
        text = ""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
        except Exception as e:
            raise Exception(f"Error reading PDF: {str(e)}")
        return text
    
    @staticmethod
    def extract_text_from_docx(file_path: str) -> str:
        """Extract text from DOCX file"""
        text = ""
        try:
            doc = Document(file_path)
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
        except Exception as e:
            raise Exception(f"Error reading DOCX: {str(e)}")
        return text
    
    @staticmethod
    def extract_text_from_txt(file_path: str) -> str:
        """Extract text from TXT file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
        except Exception as e:
            raise Exception(f"Error reading TXT: {str(e)}")
        return text
    
    @staticmethod
    def process_document(file_path: str) -> str:
        """Process document based on file extension"""
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()
        
        if ext == '.pdf':
            return DocumentProcessor.extract_text_from_pdf(file_path)
        elif ext == '.docx':
            return DocumentProcessor.extract_text_from_docx(file_path)
        elif ext == '.txt':
            return DocumentProcessor.extract_text_from_txt(file_path)
        else:
            raise ValueError(f"Unsupported file format: {ext}")
    
    @staticmethod
    def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[Dict[str, str]]:
        """Split text into overlapping chunks"""
        # Clean the text
        text = re.sub(r'\s+', ' ', text).strip()
        
        chunks = []
        start = 0
        text_length = len(text)
        
        while start < text_length:
            end = start + chunk_size
            
            # If not the last chunk, try to break at sentence boundary
            if end < text_length:
                # Look for sentence endings near the chunk boundary
                sentence_end = text.rfind('.', start, end)
                if sentence_end != -1 and sentence_end > start + chunk_size // 2:
                    end = sentence_end + 1
            
            chunk = text[start:end].strip()
            if chunk:
                chunks.append({
                    'text': chunk,
                    'start': start,
                    'end': end
                })
            
            start = end - overlap
        
        return chunks
    
    @staticmethod
    def clean_text(text: str) -> str:
        """Clean and normalize text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep punctuation
        text = re.sub(r'[^\w\s.,!?;:()\-\']', '', text)
        return text.strip()

# Made with Bob
