"""
Test script to verify all features are working correctly
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_environment_variables():
    """Test if all required environment variables are set"""
    print("=" * 60)
    print("Testing Environment Variables")
    print("=" * 60)
    
    required_vars = [
        'IBM_CLOUD_API_KEY',
        'IBM_WATSONX_PROJECT_ID',
        'IBM_WATSONX_URL',
        'FLASK_SECRET_KEY'
    ]
    
    all_set = True
    for var in required_vars:
        value = os.getenv(var)
        if value:
            # Mask sensitive data
            if 'KEY' in var or 'SECRET' in var:
                display_value = value[:10] + '...' if len(value) > 10 else '***'
            else:
                display_value = value
            print(f"[OK] {var}: {display_value}")
        else:
            print(f"[FAIL] {var}: NOT SET")
            all_set = False
    
    print()
    return all_set

def test_imports():
    """Test if all required packages are installed"""
    print("=" * 60)
    print("Testing Package Imports")
    print("=" * 60)
    
    packages = [
        ('flask', 'Flask'),
        ('dotenv', 'python-dotenv'),
        ('ibm_watsonx_ai', 'ibm-watsonx-ai'),
        ('requests', 'requests')
    ]
    
    all_imported = True
    for package, name in packages:
        try:
            __import__(package)
            print(f"[OK] {name} imported successfully")
        except ImportError as e:
            print(f"[FAIL] {name} import failed: {e}")
            all_imported = False
    
    print()
    return all_imported

def test_watsonx_connection():
    """Test IBM Watsonx.ai connection"""
    print("=" * 60)
    print("Testing IBM Watsonx.ai Connection")
    print("=" * 60)
    
    try:
        from ibm_watsonx_ai import Credentials
        from ibm_watsonx_ai.foundation_models import Model
        from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
        
        credentials = Credentials(
            url=os.getenv('IBM_WATSONX_URL'),
            api_key=os.getenv('IBM_CLOUD_API_KEY')
        )
        
        print(f"[OK] Credentials created successfully")
        print(f"  URL: {os.getenv('IBM_WATSONX_URL')}")
        
        project_id = os.getenv('IBM_WATSONX_PROJECT_ID')
        print(f"[OK] Project ID: {project_id}")
        
        # Try to create model instance
        model = Model(
            model_id='ibm/granite-13b-chat-v2',
            params={
                GenParams.DECODING_METHOD: "greedy",
                GenParams.MAX_NEW_TOKENS: 100,
                GenParams.MIN_NEW_TOKENS: 10,
                GenParams.TEMPERATURE: 0.7,
            },
            credentials=credentials,
            project_id=project_id
        )
        
        print(f"[OK] Model instance created successfully")
        print(f"  Model ID: ibm/granite-13b-chat-v2")
        
        # Try a simple test generation
        print("\nTesting model generation...")
        test_prompt = "Say 'Hello, I am NutriBot!' in one sentence."
        response = model.generate_text(prompt=test_prompt)
        print(f"[OK] Model response: {response[:100]}...")
        
        print("\n[OK] IBM Watsonx.ai connection successful!")
        return True
        
    except Exception as e:
        print(f"\n[FAIL] IBM Watsonx.ai connection failed: {str(e)}")
        print("\nTroubleshooting tips:")
        print("1. Check your IBM_CLOUD_API_KEY is correct")
        print("2. Verify IBM_WATSONX_PROJECT_ID is valid")
        print("3. Ensure your IBM Cloud account has Watsonx.ai access")
        print("4. Check if the service is active in your region")
        return False

def test_file_structure():
    """Test if all required files exist"""
    print("=" * 60)
    print("Testing File Structure")
    print("=" * 60)
    
    required_files = [
        'app.py',
        'requirements.txt',
        '.env',
        'templates/index.html',
        'static/style.css',
        'static/script.js',
        'README.md'
    ]
    
    all_exist = True
    for file in required_files:
        if os.path.exists(file):
            print(f"[OK] {file} exists")
        else:
            print(f"[FAIL] {file} missing")
            all_exist = False
    
    print()
    return all_exist

def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("NutriBot Application Test Suite")
    print("=" * 60 + "\n")
    
    results = {
        'Environment Variables': test_environment_variables(),
        'Package Imports': test_imports(),
        'File Structure': test_file_structure(),
        'Watsonx.ai Connection': test_watsonx_connection()
    }
    
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    for test_name, result in results.items():
        status = "[PASSED]" if result else "[FAILED]"
        print(f"{test_name}: {status}")
    
    all_passed = all(results.values())
    
    print("\n" + "=" * 60)
    if all_passed:
        print("[SUCCESS] ALL TESTS PASSED!")
        print("\nYour application is ready to run!")
        print("Start the server with: python app.py")
    else:
        print("[ERROR] SOME TESTS FAILED")
        print("\nPlease fix the issues above before running the application.")
    print("=" * 60 + "\n")
    
    return all_passed

if __name__ == '__main__':
    main()

# Made with Bob
