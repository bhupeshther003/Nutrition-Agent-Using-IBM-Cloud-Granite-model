from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from config import Config
from document_processor import DocumentProcessor
from vector_store import VectorStore
from watsonx_client import WatsonxClient

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

# Initialize components
Config.init_app(app)
vector_store = VectorStore()
watsonx_client = None
document_processor = DocumentProcessor()

# Chat history storage (in-memory for simplicity)
chat_history = []

def init_watsonx():
    """Initialize Watsonx client with error handling"""
    global watsonx_client
    try:
        watsonx_client = WatsonxClient()
        print("✓ Watsonx client initialized successfully")
        return True
    except Exception as e:
        print(f"✗ Failed to initialize Watsonx client: {str(e)}")
        print("  Please check your .env file and ensure WATSONX_API_KEY and WATSONX_PROJECT_ID are set")
        return False

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Render main page"""
    return render_template('index.html')

@app.route('/api/upload', methods=['POST'])
def upload_document():
    """Upload and process a document"""
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({
                'success': False,
                'error': f'Invalid file type. Allowed types: {", ".join(Config.ALLOWED_EXTENSIONS)}'
            }), 400
        
        # Save file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_filename = f"{timestamp}_{filename}"
        filepath = os.path.join(Config.UPLOAD_FOLDER, unique_filename)
        file.save(filepath)
        
        # Process document
        text = document_processor.process_document(filepath)
        
        # Chunk text
        chunks = document_processor.chunk_text(
            text,
            chunk_size=Config.CHUNK_SIZE,
            overlap=Config.CHUNK_OVERLAP
        )
        
        # Add to vector store
        num_chunks = vector_store.add_documents(
            chunks,
            document_name=filename,
            metadata={'upload_date': timestamp}
        )
        
        return jsonify({
            'success': True,
            'message': f'Document uploaded successfully. Processed {num_chunks} chunks.',
            'filename': filename,
            'chunks': num_chunks
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/ask', methods=['POST'])
def ask_question():
    """Answer a question using RAG"""
    try:
        if not watsonx_client:
            return jsonify({
                'success': False,
                'error': 'Watsonx client not initialized. Please check your configuration.'
            }), 500
        
        data = request.get_json()
        question = data.get('question', '').strip()
        
        if not question:
            return jsonify({'success': False, 'error': 'No question provided'}), 400
        
        # Search for relevant documents
        relevant_docs = vector_store.search(question, top_k=Config.TOP_K_RESULTS)
        
        if not relevant_docs:
            response = {
                'answer': "I couldn't find any relevant information in the company policy documents. Please try rephrasing your question or contact HR directly.",
                'sources': [],
                'success': True
            }
        else:
            # Generate answer using Watsonx
            response = watsonx_client.generate_answer(question, relevant_docs)
        
        # Add to chat history
        chat_entry = {
            'timestamp': datetime.now().isoformat(),
            'question': question,
            'answer': response['answer'],
            'sources': response.get('sources', [])
        }
        chat_history.append(chat_entry)
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/documents', methods=['GET'])
def get_documents():
    """Get list of uploaded documents"""
    try:
        stats = vector_store.get_collection_stats()
        return jsonify({
            'success': True,
            'documents': stats['documents'],
            'total_documents': stats['total_documents'],
            'total_chunks': stats['total_chunks']
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/documents/<document_name>', methods=['DELETE'])
def delete_document(document_name):
    """Delete a document from the vector store"""
    try:
        deleted_count = vector_store.delete_document(document_name)
        return jsonify({
            'success': True,
            'message': f'Deleted {deleted_count} chunks from {document_name}'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/history', methods=['GET'])
def get_history():
    """Get chat history"""
    try:
        # Return last 50 messages
        return jsonify({
            'success': True,
            'history': chat_history[-50:]
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/history', methods=['DELETE'])
def clear_history():
    """Clear chat history"""
    try:
        chat_history.clear()
        return jsonify({
            'success': True,
            'message': 'Chat history cleared'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'watsonx_initialized': watsonx_client is not None,
        'vector_store_initialized': vector_store is not None
    })

if __name__ == '__main__':
    print("=" * 60)
    print("Company Policy Assistant - RAG System")
    print("=" * 60)
    
    # Initialize Watsonx
    watsonx_initialized = init_watsonx()
    
    if not watsonx_initialized:
        print("\n⚠ WARNING: Running without Watsonx integration")
        print("  The system will accept uploads but cannot answer questions")
    
    print("\n" + "=" * 60)
    print("Starting Flask server...")
    print("=" * 60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)

# Made with Bob
