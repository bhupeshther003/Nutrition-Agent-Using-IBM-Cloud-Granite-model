# Multi-Agent Resume Screening System

A sophisticated AI-powered resume screening system built with Python, Flask, IBM Watsonx.ai, and IBM Granite models. This system uses four specialized AI agents to automatically parse, match, score, and provide detailed feedback on candidate resumes.

## 🌟 Features

### Multi-Agent Architecture
- **Parser Agent**: Extracts structured information from resumes (PDF/DOCX)
- **Matcher Agent**: Compares candidate profiles with job requirements
- **Scoring Agent**: Calculates match percentages and ranks candidates
- **Feedback Agent**: Generates detailed hiring insights and recommendations

### Key Capabilities
- ✅ Upload multiple resumes (PDF/DOCX format)
- ✅ AI-powered resume parsing and information extraction
- ✅ Intelligent skill matching and gap analysis
- ✅ Weighted scoring algorithm (Skills 40%, Experience 30%, Education 20%, Additional 10%)
- ✅ Automated candidate ranking
- ✅ Detailed AI-generated feedback and recommendations
- ✅ Modern, responsive web interface
- ✅ Downloadable PDF reports
- ✅ Database storage for all screening data

## 🏗️ Architecture

```
├── app/
│   ├── agents/              # AI Agents
│   │   ├── parser_agent.py
│   │   ├── matcher_agent.py
│   │   ├── scoring_agent.py
│   │   └── feedback_agent.py
│   ├── models/              # Database Models
│   │   └── models.py
│   ├── utils/               # Utilities
│   │   ├── document_processor.py
│   │   ├── watsonx_client.py
│   │   └── report_generator.py
│   ├── static/              # Frontend Assets
│   │   ├── css/
│   │   └── js/
│   └── templates/           # HTML Templates
├── uploads/                 # Resume uploads
├── reports/                 # Generated reports
├── app.py                   # Main Flask application
├── config.py                # Configuration
└── requirements.txt         # Dependencies
```

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- IBM Cloud account with Watsonx.ai access
- IBM Watsonx.ai API key and Project ID

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd resume-screening-system
```

### Step 2: Create Virtual Environment
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables
Create a `.env` file in the root directory:

```env
# IBM Watsonx.ai Configuration
WATSONX_API_KEY=your_watsonx_api_key_here
WATSONX_PROJECT_ID=your_project_id_here
WATSONX_URL=https://us-south.ml.cloud.ibm.com

# IBM Granite Model
GRANITE_MODEL_ID=ibm/granite-13b-chat-v2

# Flask Configuration
SECRET_KEY=your_secret_key_here
DEBUG=True

# Database Configuration
DATABASE_URL=sqlite:///resume_screening.db

# Logging
LOG_LEVEL=INFO
```

### Step 5: Initialize Database
```bash
python -c "from app import create_app; app = create_app(); app.app_context().push(); from app.models import db; db.create_all()"
```

## 🎯 Usage

### Start the Application
```bash
python app.py
```

The application will be available at `http://localhost:5000`

### Using the System

#### 1. Create Job Description
- Enter job title, description, required skills, experience, and education
- Click "Create Job & Continue"

#### 2. Upload Resumes
- Drag and drop resume files (PDF/DOCX) or click to browse
- Upload multiple resumes at once
- Click "Upload Resumes"

#### 3. Process Resumes
- Click "Start AI Processing"
- The system will:
  - Extract information from each resume
  - Match candidates with job requirements
  - Calculate scores and rankings
  - Generate detailed feedback

#### 4. View Results
- See ranked candidates with match percentages
- Review detailed scores (Skills, Experience, Education)
- Read AI-generated assessments
- Identify matching and missing skills

#### 5. Download Report
- Click "Download Report" to get a comprehensive PDF report
- Report includes all candidates, scores, and recommendations

## 🔧 Configuration

### Model Parameters
Adjust in `config.py`:
```python
MODEL_PARAMETERS = {
    'decoding_method': 'greedy',
    'max_new_tokens': 1000,
    'temperature': 0.7,
    'top_k': 50,
    'top_p': 1,
}
```

### Scoring Weights
Customize scoring weights in `config.py`:
```python
SCORING_WEIGHTS = {
    'skills': 0.40,      # 40%
    'experience': 0.30,  # 30%
    'education': 0.20,   # 20%
    'additional': 0.10   # 10%
}
```

## 📊 API Endpoints

### Create Job
```http
POST /api/jobs
Content-Type: application/json

{
  "title": "Senior Software Engineer",
  "description": "Job description...",
  "required_skills": ["Python", "Flask", "AI"],
  "required_experience": "3-5 years",
  "required_education": "Bachelor's in CS"
}
```

### Upload Resumes
```http
POST /api/jobs/{job_id}/upload
Content-Type: multipart/form-data

resumes: [file1.pdf, file2.docx, ...]
```

### Process Resumes
```http
POST /api/jobs/{job_id}/process
```

### Get Results
```http
GET /api/jobs/{job_id}/results
```

### Download Report
```http
GET /api/jobs/{job_id}/report
```

## 🧪 Testing

### Run Tests
```bash
pytest tests/
```

### Test Individual Components
```python
# Test document processor
from app.utils import DocumentProcessor
text = DocumentProcessor.extract_text('path/to/resume.pdf')

# Test Watsonx client
from app.utils import create_watsonx_client
from config import config
client = create_watsonx_client(config['development'])
response = client.generate_text("Test prompt")
```

## 🎨 Customization

### Adding New Agents
1. Create new agent file in `app/agents/`
2. Implement agent class with required methods
3. Register agent in `app.py`
4. Update prompts in `config.py`

### Modifying UI
- Edit `app/templates/index.html` for structure
- Modify `app/static/css/style.css` for styling
- Update `app/static/js/main.js` for functionality

### Custom Scoring Logic
Modify `app/agents/scoring_agent.py`:
```python
def _calculate_custom_score(self, candidate_data, match_data):
    # Your custom scoring logic
    pass
```

## 🔒 Security Considerations

- Store API keys in environment variables, never in code
- Validate all file uploads
- Implement rate limiting for API endpoints
- Use HTTPS in production
- Sanitize user inputs
- Implement authentication for production use

## 🚀 Deployment

### Production Setup
1. Set `DEBUG=False` in `.env`
2. Use production-grade WSGI server (Gunicorn)
3. Set up reverse proxy (Nginx)
4. Use PostgreSQL instead of SQLite
5. Implement proper logging and monitoring

### Docker Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:create_app()"]
```

## 📝 Database Schema

### JobDescription
- id, title, description, required_skills, required_experience, required_education, created_at

### Candidate
- id, job_id, name, email, phone, resume_filename, resume_path
- skills, education, experience, certifications, summary
- match_score, skills_score, experience_score, education_score
- matching_skills, missing_skills, strengths, gaps, recommendations
- detailed_feedback, rank, status, created_at, updated_at

### ScreeningSession
- id, job_id, total_candidates, processed_candidates, status, started_at, completed_at

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- IBM Watsonx.ai for AI capabilities
- IBM Granite models for natural language processing
- Flask framework for web application
- ReportLab for PDF generation

## 📞 Support

For issues, questions, or contributions:
- Create an issue on GitHub
- Contact: [your-email@example.com]

## 🔄 Version History

### v1.0.0 (2024)
- Initial release
- Multi-agent architecture
- Resume parsing and matching
- Scoring and ranking
- PDF report generation
- Modern web interface

## 🎯 Future Enhancements

- [ ] Real-time processing with WebSockets
- [ ] Email notifications
- [ ] Interview scheduling integration
- [ ] Video resume analysis
- [ ] Multi-language support
- [ ] Advanced analytics dashboard
- [ ] API authentication
- [ ] Batch processing optimization
- [ ] Integration with ATS systems
- [ ] Mobile application

---

**Built with ❤️ using IBM Watsonx.ai and Granite Models**