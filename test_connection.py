"""
Test script to verify IBM Watsonx.ai connection and configuration
"""

import os
import sys
from dotenv import load_dotenv

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Load environment variables
load_dotenv()

print("=" * 60)
print("Testing Multi-Agent Resume Screening System")
print("=" * 60)
print()

# Test 1: Check environment variables
print("Test 1: Checking environment variables...")
required_vars = ['WATSONX_API_KEY', 'WATSONX_PROJECT_ID', 'WATSONX_URL', 'GRANITE_MODEL_ID']
missing_vars = []

for var in required_vars:
    value = os.getenv(var)
    if value:
        # Mask API key for security
        if 'API_KEY' in var:
            display_value = value[:10] + '...' + value[-4:] if len(value) > 14 else '***'
        else:
            display_value = value
        print(f"  ✓ {var}: {display_value}")
    else:
        print(f"  ✗ {var}: NOT SET")
        missing_vars.append(var)

if missing_vars:
    print(f"\n❌ Missing environment variables: {', '.join(missing_vars)}")
    print("Please update your .env file with the required credentials.")
    sys.exit(1)
else:
    print("\n✓ All environment variables are set")

print()

# Test 2: Import modules
print("Test 2: Importing modules...")
try:
    from config import config
    print("  ✓ config module imported")
    
    from app.models import db, JobDescription, Candidate
    print("  ✓ database models imported")
    
    from app.utils import DocumentProcessor, create_watsonx_client
    print("  ✓ utility modules imported")
    
    from app.agents import ParserAgent, MatcherAgent, ScoringAgent, FeedbackAgent
    print("  ✓ agent modules imported")
    
    print("\n✓ All modules imported successfully")
except ImportError as e:
    print(f"\n❌ Import error: {str(e)}")
    print("Please ensure all dependencies are installed: pip install -r requirements.txt")
    sys.exit(1)

print()

# Test 3: Test Watsonx.ai connection
print("Test 3: Testing IBM Watsonx.ai connection...")
try:
    from app.utils import create_watsonx_client
    from config import config
    
    app_config = config['development']
    
    print(f"  - API URL: {app_config.WATSONX_URL}")
    print(f"  - Model ID: {app_config.GRANITE_MODEL_ID}")
    print(f"  - Connecting to Watsonx.ai...")
    
    client = create_watsonx_client(app_config)
    print("  ✓ Watsonx client initialized")
    
    # Test with a simple prompt
    print("  - Testing text generation...")
    test_response = client.generate_text("Hello, this is a test. Respond with 'OK'.", max_tokens=10)
    
    if test_response:
        print(f"  ✓ Text generation successful")
        print(f"    Response: {test_response[:100]}...")
    else:
        print("  ⚠ Text generation returned empty response")
    
    print("\n✓ Watsonx.ai connection test passed")
    
except Exception as e:
    print(f"\n❌ Watsonx.ai connection failed: {str(e)}")
    print("\nPossible issues:")
    print("  1. Invalid API key or Project ID")
    print("  2. Network connectivity issues")
    print("  3. Incorrect region URL")
    print("  4. Model not available in your region")
    print("\nPlease verify your credentials and try again.")
    sys.exit(1)

print()

# Test 4: Test database initialization
print("Test 4: Testing database initialization...")
try:
    import importlib.util
    spec = importlib.util.spec_from_file_location("app_module", "app.py")
    app_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(app_module)
    
    app = app_module.create_app('development')
    with app.app_context():
        db.create_all()
        print("  ✓ Database tables created")
    
    print("\n✓ Database initialization successful")
    
except Exception as e:
    print(f"\n❌ Database initialization failed: {str(e)}")
    sys.exit(1)

print()

# Test 5: Test document processor
print("Test 5: Testing document processor...")
try:
    from app.utils import DocumentProcessor
    
    # Test file validation
    assert DocumentProcessor.validate_file('test.pdf') == True
    assert DocumentProcessor.validate_file('test.docx') == True
    assert DocumentProcessor.validate_file('test.txt') == False
    
    print("  ✓ File validation working")
    print("\n✓ Document processor test passed")
    
except Exception as e:
    print(f"\n❌ Document processor test failed: {str(e)}")
    sys.exit(1)

print()
print("=" * 60)
print("✓ ALL TESTS PASSED!")
print("=" * 60)
print()
print("Your system is ready to use!")
print("Run: python app.py")
print("Then open: http://localhost:5000")
print()

# Made with Bob
