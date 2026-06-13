# Company Policy Assistant - RAG System

A powerful Retrieval-Augmented Generation (RAG) system built with Python, Flask, and IBM Watsonx.ai that helps employees quickly find answers to company policy questions.

## Features

- 📄 **Multi-format Document Support**: Upload PDF, DOCX, and TXT files
- 🔍 **Intelligent Search**: Vector-based semantic search using ChromaDB
- 🤖 **AI-Powered Answers**: Generate accurate responses using IBM Watsonx.ai
- 💬 **Modern Chat Interface**: Clean, responsive UI for easy interaction
- 📚 **Source References**: Every answer includes source document references
- 📝 **Chat History**: Track conversation history
- 🔄 **Document Management**: Easy upload and deletion of policy documents

## Architecture

```
┌─────────────────┐
│  User Interface │
│   (Flask App)   │
└────────┬────────┘
         │
    ┌────▼────┐
    │ Upload  │
    │Documents│
    └────┬────┘
         │
    ┌────▼────────────┐
    │ Document        │
    │ Processor       │
    │ (PDF/DOCX/TXT)  │
    └────┬────────────┘
         │
    ┌────▼────────────┐
    │ Text Chunking   │
    │ & Embedding     │
    └────┬────────────┘
         │
    ┌────▼────────────┐
    │ Vector Store    │
    │ (ChromaDB)      │
    └────┬────────────┘
         │
    ┌────▼────────────┐
    │ Question Asked  │
    └────┬────────────┘
         │
    ┌────▼────────────┐
    │ Semantic Search │
    │ (Top K Results) │
    └────┬────────────┘
         │
    ┌────▼────────────┐
    │ IBM Watsonx.ai  │
    │ (Answer Gen)    │
    └────┬────────────┘
         │
    ┌────▼────────────┐
    │ Response with   │
    │ Sources         │
    └─────────────────┘
```

## Prerequisites

- Python 3.8 or higher
- IBM Cloud account with Watsonx.ai access
- API Key and Project ID from IBM Watsonx.ai

## Installation

### 1. Clone or Download the Project

```bash
cd company-policy-assistant
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy `.env.example` to `.env`:

```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

Edit `.env` and add your IBM Watsonx.ai credentials:

```env
# IBM Watsonx.ai Configuration
WATSONX_API_KEY=your_api_key_here
WATSONX_PROJECT_ID=your_project_id_here
WATSONX_URL=https://us-south.ml.cloud.ibm.com

# Model Configuration
WATSONX_MODEL_ID=ibm/granite-13b-chat-v2
WATSONX_MAX_TOKENS=500
WATSONX_TEMPERATURE=0.7

# Application Configuration
FLASK_SECRET_KEY=your_secret_key_here
UPLOAD_FOLDER=uploads
VECTOR_DB_PATH=vector_db
MAX_CONTENT_LENGTH=16777216

# Embedding Model
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
```

### 5. Get IBM Watsonx.ai Credentials

1. Go to [IBM Cloud](https://cloud.ibm.com/)
2. Create a Watsonx.ai service instance
3. Get your API Key from IBM Cloud IAM
4. Get your Project ID from Watsonx.ai project settings

## Usage

### Start the Application

```bash
python app.py
```

The application will start on `http://localhost:5000`

### Upload Documents

1. Click on the upload area or drag and drop files
2. Supported formats: PDF, DOCX, TXT
3. Documents are automatically processed and indexed

### Ask Questions

1. Type your question in the chat input
2. Press Enter or click the send button
3. Receive AI-generated answers with source references

### Example Questions

- "What is the company's leave policy?"
- "How do I apply for remote work?"
- "What are the travel reimbursement guidelines?"
- "What is the security policy for handling sensitive data?"
- "How many sick days am I entitled to?"

## Project Structure

```
company-policy-assistant/
├── app.py                  # Flask application
├── config.py              # Configuration settings
├── document_processor.py  # Document parsing and chunking
├── vector_store.py        # ChromaDB vector database
├── watsonx_client.py      # IBM Watsonx.ai integration
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── .env                  # Your environment variables (create this)
├── README.md             # This file
├── templates/
│   └── index.html        # Main HTML template
├── static/
│   ├── style.css         # Stylesheet
│   └── script.js         # Frontend JavaScript
├── uploads/              # Uploaded documents (auto-created)
└── vector_db/            # Vector database storage (auto-created)
```

## Configuration

### Adjust RAG Parameters

Edit `config.py` to customize:

```python
# Text chunking
CHUNK_SIZE = 1000          # Characters per chunk
CHUNK_OVERLAP = 200        # Overlap between chunks

# Retrieval
TOP_K_RESULTS = 3          # Number of relevant chunks to retrieve

# Model parameters
WATSONX_MAX_TOKENS = 500   # Maximum response length
WATSONX_TEMPERATURE = 0.7  # Response creativity (0-1)
```

### Change Embedding Model

You can use different sentence-transformers models:

```env
# Faster, smaller model
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

# More accurate, larger model
EMBEDDING_MODEL=sentence-transformers/all-mpnet-base-v2
```

### Change Watsonx Model

Available models include:

- `ibm/granite-13b-chat-v2` (recommended)
- `meta-llama/llama-2-70b-chat`
- `google/flan-ul2`

## API Endpoints

### Upload Document
```
POST /api/upload
Content-Type: multipart/form-data
Body: file (PDF/DOCX/TXT)
```

### Ask Question
```
POST /api/ask
Content-Type: application/json
Body: {"question": "your question"}
```

### Get Documents
```
GET /api/documents
```

### Delete Document
```
DELETE /api/documents/<document_name>
```

### Get Chat History
```
GET /api/history
```

### Clear Chat History
```
DELETE /api/history
```

### Health Check
```
GET /api/health
```

## Troubleshooting

### Issue: "Watsonx client not initialized"

**Solution**: Check your `.env` file and ensure `WATSONX_API_KEY` and `WATSONX_PROJECT_ID` are set correctly.

### Issue: "Import errors" when starting

**Solution**: Make sure you've activated the virtual environment and installed all dependencies:
```bash
pip install -r requirements.txt
```

### Issue: "File upload fails"

**Solution**: Check file size (default max: 16MB) and format (PDF, DOCX, TXT only).

### Issue: "No relevant information found"

**Solution**: 
- Upload more relevant documents
- Try rephrasing your question
- Check if documents were processed successfully

## Performance Optimization

### For Large Document Collections

1. **Increase chunk size** for longer documents:
   ```python
   CHUNK_SIZE = 1500
   ```

2. **Adjust TOP_K_RESULTS** for more context:
   ```python
   TOP_K_RESULTS = 5
   ```

3. **Use a more powerful embedding model**:
   ```env
   EMBEDDING_MODEL=sentence-transformers/all-mpnet-base-v2
   ```

## Security Considerations

1. **API Keys**: Never commit `.env` file to version control
2. **File Upload**: Validate file types and sizes
3. **Production**: Use a production WSGI server (gunicorn, uWSGI)
4. **HTTPS**: Always use HTTPS in production
5. **Authentication**: Add user authentication for production use

## Deployment

### Using Gunicorn (Production)

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Using Docker

Create `Dockerfile`:

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

Build and run:

```bash
docker build -t policy-assistant .
docker run -p 5000:5000 --env-file .env policy-assistant
```

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

This project is provided as-is for educational and commercial use.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review IBM Watsonx.ai documentation
3. Open an issue in the repository

## Acknowledgments

- IBM Watsonx.ai for AI capabilities
- ChromaDB for vector storage
- Sentence Transformers for embeddings
- Flask for web framework

---

**Built with ❤️ for better employee experience**