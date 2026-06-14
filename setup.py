"""
Setup script for Multi-Agent Resume Screening System
"""

import os
import sys
import subprocess


def create_directories():
    """Create necessary directories"""
    directories = [
        'app/agents',
        'app/models',
        'app/templates',
        'app/static/css',
        'app/static/js',
        'app/utils',
        'uploads',
        'reports'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    
    print("✓ Directories created successfully")


def create_env_file():
    """Create .env file from template if it doesn't exist"""
    if not os.path.exists('.env'):
        if os.path.exists('.env.example'):
            with open('.env.example', 'r') as example:
                with open('.env', 'w') as env:
                    env.write(example.read())
            print("✓ .env file created from template")
            print("⚠ Please update .env with your IBM Watsonx.ai credentials")
        else:
            print("⚠ .env.example not found")
    else:
        print("✓ .env file already exists")


def install_dependencies():
    """Install Python dependencies"""
    print("\nInstalling dependencies...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("✓ Dependencies installed successfully")
    except subprocess.CalledProcessError:
        print("✗ Failed to install dependencies")
        return False
    return True


def initialize_database():
    """Initialize the database"""
    print("\nInitializing database...")
    try:
        from app import create_app
        from app.models import db
        
        app = create_app()
        with app.app_context():
            db.create_all()
        
        print("✓ Database initialized successfully")
    except Exception as e:
        print(f"✗ Failed to initialize database: {str(e)}")
        return False
    return True


def main():
    """Main setup function"""
    print("=" * 60)
    print("Multi-Agent Resume Screening System - Setup")
    print("=" * 60)
    print()
    
    # Create directories
    print("Step 1: Creating directories...")
    create_directories()
    print()
    
    # Create .env file
    print("Step 2: Setting up environment variables...")
    create_env_file()
    print()
    
    # Install dependencies
    print("Step 3: Installing dependencies...")
    if not install_dependencies():
        print("\n⚠ Setup incomplete. Please install dependencies manually.")
        return
    print()
    
    # Initialize database
    print("Step 4: Initializing database...")
    if not initialize_database():
        print("\n⚠ Setup incomplete. Please initialize database manually.")
        return
    print()
    
    print("=" * 60)
    print("✓ Setup completed successfully!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Update .env file with your IBM Watsonx.ai credentials")
    print("2. Run: python app.py")
    print("3. Open: http://localhost:5000")
    print()


if __name__ == '__main__':
    main()

# Made with Bob
