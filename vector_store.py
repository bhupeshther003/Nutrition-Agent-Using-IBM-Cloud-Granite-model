import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Optional
import uuid
from config import Config

class VectorStore:
    """Manage vector database for document storage and retrieval"""
    
    def __init__(self, persist_directory: str = None):
        """Initialize vector store with ChromaDB"""
        self.persist_directory = persist_directory or Config.VECTOR_DB_PATH
        
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(
            path=self.persist_directory,
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        
        # Initialize embedding model
        self.embedding_model = SentenceTransformer(Config.EMBEDDING_MODEL)
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name="company_policies",
            metadata={"description": "Company policy documents"}
        )
    
    def add_documents(self, chunks: List[Dict], document_name: str, metadata: Dict = None):
        """Add document chunks to vector store"""
        documents = []
        embeddings = []
        ids = []
        metadatas = []
        
        for i, chunk in enumerate(chunks):
            chunk_id = f"{document_name}_{uuid.uuid4().hex[:8]}_{i}"
            text = chunk['text']
            
            # Generate embedding
            embedding = self.embedding_model.encode(text).tolist()
            
            # Prepare metadata
            chunk_metadata = {
                'document_name': document_name,
                'chunk_index': i,
                'start': chunk.get('start', 0),
                'end': chunk.get('end', 0)
            }
            
            if metadata:
                chunk_metadata.update(metadata)
            
            documents.append(text)
            embeddings.append(embedding)
            ids.append(chunk_id)
            metadatas.append(chunk_metadata)
        
        # Add to collection
        self.collection.add(
            documents=documents,
            embeddings=embeddings,
            ids=ids,
            metadatas=metadatas
        )
        
        return len(chunks)
    
    def search(self, query: str, top_k: int = None) -> List[Dict]:
        """Search for relevant documents"""
        top_k = top_k or Config.TOP_K_RESULTS
        
        # Generate query embedding
        query_embedding = self.embedding_model.encode(query).tolist()
        
        # Search in collection
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=['documents', 'metadatas', 'distances']
        )
        
        # Format results
        formatted_results = []
        if results['documents'] and len(results['documents'][0]) > 0:
            for i in range(len(results['documents'][0])):
                formatted_results.append({
                    'text': results['documents'][0][i],
                    'metadata': results['metadatas'][0][i],
                    'distance': results['distances'][0][i]
                })
        
        return formatted_results
    
    def get_all_documents(self) -> List[str]:
        """Get list of all unique document names"""
        results = self.collection.get(include=['metadatas'])
        
        if not results['metadatas']:
            return []
        
        document_names = set()
        for metadata in results['metadatas']:
            if 'document_name' in metadata:
                document_names.add(metadata['document_name'])
        
        return sorted(list(document_names))
    
    def delete_document(self, document_name: str) -> int:
        """Delete all chunks of a specific document"""
        # Get all items
        results = self.collection.get(include=['metadatas'])
        
        # Find IDs to delete
        ids_to_delete = []
        for i, metadata in enumerate(results['metadatas']):
            if metadata.get('document_name') == document_name:
                ids_to_delete.append(results['ids'][i])
        
        # Delete items
        if ids_to_delete:
            self.collection.delete(ids=ids_to_delete)
        
        return len(ids_to_delete)
    
    def get_collection_stats(self) -> Dict:
        """Get statistics about the collection"""
        count = self.collection.count()
        documents = self.get_all_documents()
        
        return {
            'total_chunks': count,
            'total_documents': len(documents),
            'documents': documents
        }
    
    def reset_collection(self):
        """Reset the entire collection"""
        self.client.delete_collection(name="company_policies")
        self.collection = self.client.get_or_create_collection(
            name="company_policies",
            metadata={"description": "Company policy documents"}
        )

# Made with Bob
