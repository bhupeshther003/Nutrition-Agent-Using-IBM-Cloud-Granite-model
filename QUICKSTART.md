# Quick Start Guide

Get the Multi-Agent Resume Screening System up and running in 5 minutes!

## Prerequisites

- Python 3.8+
- IBM Watsonx.ai account with API key
- IBM Watsonx.ai Project ID

## Installation Steps

### 1. Clone and Setup

```bash
# Clone the repository
git clone <repository-url>
cd resume-screening-system

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

Create a `.env` file in the root directory:

```env
WATSONX_API_KEY=your_api_key_here
WATSONX_PROJECT_ID=your_project_id_here
WATSONX_URL=https://us-south.ml.cloud.ibm.com
GRANITE_MODEL_ID=ibm/granite-13b-chat-v2
SECRET_KEY=your_secret_key_here
DEBUG=True
```

### 3. Initialize Database

```bash
python setup.py
```

Or manually:

```bash
python -c "from app import create_app; app = create_app(); app.app_context().push(); from app.models import db; db.create_all()"
```

### 4. Run the Application

```bash
python app.py
```

Open your browser and navigate to: `http://localhost:5000`

## Usage Flow

### Step 1: Create Job Description
1. Enter job title (e.g., "Senior Software Engineer")
2. Add detailed job description
3. List required skills (comma-separated)
4. Specify experience and education requirements
5. Click "Create Job & Continue"

### Step 2: Upload Resumes
1. Drag and drop resume files (PDF/DOCX)
2. Or click to browse and select files
3. Click "Upload Resumes"
4. Click "Start AI Processing"

### Step 3: View Results
1. Wait for AI processing to complete
2. Review ranked candidates
3. Check match percentages and scores
4. Read AI-generated assessments
5. Download comprehensive PDF report

## Example Job Description

**Title:** Senior Software Engineer

**Description:**
```
We are seeking an experienced Senior Software Engineer to join our team. 
The ideal candidate will have strong expertise in Python, Flask, and AI/ML technologies.
You will be responsible for designing and implementing scalable backend systems,
working with AI models, and mentoring junior developers.
```

**Required Skills:**
```
Python, Flask, REST APIs, SQL, Machine Learning, Docker, Git, Agile
```

**Required Experience:** 5+ years

**Required Education:** Bachelor's in Computer Science or related field

## Troubleshooting

### Issue: Import errors
**Solution:** Make sure you're in the virtual environment and all dependencies are installed:
```bash
pip install -r requirements.txt
```

### Issue: Database errors
**Solution:** Delete the database file and reinitialize:
```bash
rm resume_screening.db
python setup.py
```

### Issue: Watsonx.ai connection errors
**Solution:** Verify your API key and project ID in the `.env` file

### Issue: File upload fails
**Solution:** Check file format (PDF/DOCX only) and size (max 16MB)

## Getting IBM Watsonx.ai Credentials

1. Go to [IBM Cloud](https://cloud.ibm.com/)
2. Create an account or log in
3. Navigate to Watsonx.ai service
4. Create a new project
5. Get your API key from IBM Cloud IAM
6. Copy your Project ID from the project settings

## System Requirements

- **RAM:** Minimum 4GB (8GB recommended)
- **Storage:** 1GB free space
- **Network:** Internet connection for Watsonx.ai API calls
- **Browser:** Modern browser (Chrome, Firefox, Safari, Edge)

## Performance Tips

1. **Batch Processing:** Upload multiple resumes at once for efficiency
2. **Network:** Ensure stable internet connection for API calls
3. **File Size:** Optimize resume file sizes for faster processing
4. **Caching:** Results are stored in database for quick retrieval

## Next Steps

- Customize scoring weights in `config.py`
- Modify UI in `app/templates/` and `app/static/`
- Add custom agents in `app/agents/`
- Integrate with your existing systems via API

## Support

For issues or questions:
- Check the main [README.md](README.md)
- Review error logs in `app.log`
- Create an issue on GitHub

---

**Happy Screening! 🚀**