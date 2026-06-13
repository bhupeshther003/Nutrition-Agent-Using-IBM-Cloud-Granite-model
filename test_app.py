"""
Test script for Company Policy Assistant
Tests the main functionality without running the full Flask app
"""

import os
from document_processor import DocumentProcessor
from vector_store import VectorStore
from config import Config

def test_document_processing():
    """Test document processing"""
    print("=" * 60)
    print("TEST 1: Document Processing")
    print("=" * 60)
    
    try:
        processor = DocumentProcessor()
        
        # Test text extraction
        text = processor.process_document('test_policy.txt')
        print(f"✓ Successfully extracted {len(text)} characters from test_policy.txt")
        
        # Test chunking
        chunks = processor.chunk_text(text, chunk_size=500, overlap=100)
        print(f"✓ Successfully created {len(chunks)} chunks")
        
        return True, chunks
    except Exception as e:
        print(f"✗ Document processing failed: {str(e)}")
        return False, []

def test_vector_store(chunks):
    """Test vector store"""
    print("\n" + "=" * 60)
    print("TEST 2: Vector Store")
    print("=" * 60)
    
    try:
        # Initialize vector store
        vector_store = VectorStore()
        print("✓ Vector store initialized")
        
        # Add documents
        num_added = vector_store.add_documents(
            chunks,
            document_name="test_policy.txt",
            metadata={'test': True}
        )
        print(f"✓ Added {num_added} chunks to vector store")
        
        # Test search
        results = vector_store.search("What is the leave policy?", top_k=3)
        print(f"✓ Search returned {len(results)} results")
        
        if results:
            print("\nTop result preview:")
            print(f"  Text: {results[0]['text'][:100]}...")
            print(f"  Distance: {results[0]['distance']:.4f}")
        
        return True, vector_store
    except Exception as e:
        print(f"✗ Vector store test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False, None

def test_watsonx_connection():
    """Test Watsonx connection"""
    print("\n" + "=" * 60)
    print("TEST 3: Watsonx.ai Connection")
    print("=" * 60)
    
    try:
        from watsonx_client import WatsonxClient
        
        client = WatsonxClient()
        print("✓ Watsonx client initialized")
        
        # Test connection
        if client.test_connection():
            print("✓ Successfully connected to Watsonx.ai")
            return True, client
        else:
            print("✗ Failed to connect to Watsonx.ai")
            return False, None
            
    except Exception as e:
        print(f"✗ Watsonx connection failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False, None

def test_rag_pipeline(client, vector_store):
    """Test complete RAG pipeline"""
    print("\n" + "=" * 60)
    print("TEST 4: RAG Pipeline (Question Answering)")
    print("=" * 60)
    
    try:
        # Search for relevant context
        question = "How many days of annual leave do employees get?"
        print(f"\nQuestion: {question}")
        
        results = vector_store.search(question, top_k=3)
        print(f"✓ Retrieved {len(results)} relevant chunks")
        
        # Generate answer
        response = client.generate_answer(question, results)
        
        if response['success']:
            print(f"✓ Answer generated successfully")
            print(f"\nAnswer: {response['answer']}")
            print(f"\nSources: {len(response['sources'])} documents")
            for source in response['sources']:
                print(f"  - {source['document']}")
            return True
        else:
            print(f"✗ Answer generation failed: {response.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"✗ RAG pipeline test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("COMPANY POLICY ASSISTANT - END-TO-END TEST")
    print("=" * 60 + "\n")
    
    # Test 1: Document Processing
    success1, chunks = test_document_processing()
    if not success1:
        print("\n✗ Tests failed at document processing stage")
        return
    
    # Test 2: Vector Store
    success2, vector_store = test_vector_store(chunks)
    if not success2:
        print("\n✗ Tests failed at vector store stage")
        return
    
    # Test 3: Watsonx Connection
    success3, client = test_watsonx_connection()
    if not success3:
        print("\n✗ Tests failed at Watsonx connection stage")
        print("\nNote: Make sure your .env file has valid credentials:")
        print("  - WATSONX_API_KEY")
        print("  - WATSONX_PROJECT_ID")
        print("  - WATSONX_URL")
        return
    
    # Test 4: RAG Pipeline
    success4 = test_rag_pipeline(client, vector_store)
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Document Processing: {'✓ PASSED' if success1 else '✗ FAILED'}")
    print(f"Vector Store: {'✓ PASSED' if success2 else '✗ FAILED'}")
    print(f"Watsonx Connection: {'✓ PASSED' if success3 else '✗ FAILED'}")
    print(f"RAG Pipeline: {'✓ PASSED' if success4 else '✗ FAILED'}")
    
    if all([success1, success2, success3, success4]):
        print("\n🎉 ALL TESTS PASSED! The application is ready to use.")
        print("\nNext steps:")
        print("1. Run: python app.py")
        print("2. Open: http://localhost:5000")
        print("3. Upload your company policy documents")
        print("4. Start asking questions!")
    else:
        print("\n⚠ Some tests failed. Please check the errors above.")
    
    print("=" * 60 + "\n")

if __name__ == "__main__":
    main()

# Made with Bob
