# Quick Setup Guide

Follow these steps to get your Company Policy Assistant up and running in minutes!

## Step 1: Install Python

Make sure you have Python 3.8 or higher installed:

```bash
python --version
```

If not installed, download from [python.org](https://www.python.org/downloads/)

## Step 2: Set Up Virtual Environment

Open terminal in the project directory:

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
```

You should see `(.venv)` in your terminal prompt.

## Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This will take a few minutes to download and install all required packages.

## Step 4: Get IBM Watsonx.ai Credentials

### 4.1 Create IBM Cloud Account
1. Go to [IBM Cloud](https://cloud.ibm.com/)
2. Sign up for a free account or log in

### 4.2 Create Watsonx.ai Instance
1. In IBM Cloud dashboard, search for "Watsonx.ai"
2. Click "Create" to create a new instance
3. Choose a plan (Lite/Free tier available)
4. Click "Create"

### 4.3 Get API Key
1. Go to [IBM Cloud API Keys](https://cloud.ibm.com/iam/apikeys)
2. Click "Create an IBM Cloud API key"
3. Give it a name (e.g., "Watsonx Policy Assistant")
4. Click "Create"
5. **Copy and save the API key** (you won't see it again!)

### 4.4 Get Project ID
1. Go to your Watsonx.ai instance
2. Click "Launch Watsonx.ai"
3. Create a new project or select existing one
4. Go to project settings (gear icon)
5. Copy the **Project ID**

## Step 5: Configure Environment

### 5.1 Create .env file

```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

### 5.2 Edit .env file

Open `.env` in a text editor and add your credentials:

```env
# Replace these with your actual values
WATSONX_API_KEY=your_actual_api_key_here
WATSONX_PROJECT_ID=your_actual_project_id_here

# Keep these as default or customize
WATSONX_URL=https://us-south.ml.cloud.ibm.com
WATSONX_MODEL_ID=ibm/granite-13b-chat-v2
WATSONX_MAX_TOKENS=500
WATSONX_TEMPERATURE=0.7

FLASK_SECRET_KEY=change-this-to-a-random-string
UPLOAD_FOLDER=uploads
VECTOR_DB_PATH=vector_db
MAX_CONTENT_LENGTH=16777216

EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
```

**Important**: Replace `your_actual_api_key_here` and `your_actual_project_id_here` with your real credentials!

## Step 6: Run the Application

```bash
python app.py
```

You should see:

```
============================================================
Company Policy Assistant - RAG System
============================================================
✓ Watsonx client initialized successfully

============================================================
Starting Flask server...
============================================================

 * Running on http://0.0.0.0:5000
```

## Step 7: Access the Application

Open your web browser and go to:

```
http://localhost:5000
```

## Step 8: Upload Your First Document

1. Click on the upload area or drag and drop a file
2. Supported formats: PDF, DOCX, TXT
3. Wait for "Document uploaded successfully" message

## Step 9: Ask Your First Question

1. Type a question in the chat input
2. Press Enter or click the send button
3. Get an AI-generated answer with source references!

## Troubleshooting

### "Watsonx client not initialized"

**Problem**: API credentials are incorrect or missing

**Solution**:
1. Check your `.env` file
2. Verify API key and Project ID are correct
3. Make sure there are no extra spaces
4. Restart the application

### "Module not found" errors

**Problem**: Dependencies not installed

**Solution**:
```bash
# Make sure virtual environment is activated
pip install -r requirements.txt
```

### "Port 5000 already in use"

**Problem**: Another application is using port 5000

**Solution**:
```bash
# Use a different port
python app.py --port 5001
```

Or edit `app.py` and change:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Upload fails

**Problem**: File too large or wrong format

**Solution**:
- Check file size (max 16MB by default)
- Ensure file is PDF, DOCX, or TXT
- Try a smaller file first

### No answers returned

**Problem**: No documents uploaded or question not clear

**Solution**:
1. Upload relevant policy documents first
2. Try rephrasing your question
3. Check if documents were processed (see document list)

## Testing the System

### Sample Questions to Try

After uploading a company policy document, try these:

1. "What is the leave policy?"
2. "How do I request time off?"
3. "What are the working hours?"
4. "What is the remote work policy?"
5. "How do I submit expenses?"

## Next Steps

### Add More Documents

Upload all your company policy documents:
- HR policies
- Leave policies
- Travel policies
- Security guidelines
- Code of conduct
- Benefits information

### Customize Settings

Edit `config.py` to adjust:
- Chunk size for document processing
- Number of results to retrieve
- Model parameters
- Upload limits

### Share with Team

Once configured, share the URL with your team:
```
http://your-server-ip:5000
```

For production deployment, see the main README.md

## Getting Help

If you encounter issues:

1. Check this guide first
2. Review the main README.md
3. Check IBM Watsonx.ai documentation
4. Verify all dependencies are installed
5. Check the console for error messages

## Security Reminder

⚠️ **Important**: 
- Never share your `.env` file
- Never commit `.env` to version control
- Keep your API keys secure
- Use HTTPS in production

---

**Congratulations! Your Company Policy Assistant is ready to use! 🎉**